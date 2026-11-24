"""Tests for Mohammed Al Ali: C2 assets, C3 publish and search, C4 requests, AI 1 classification."""
import pytest

from app.models import Asset
from app.mubarak.states import DomainError
from app.mohammed_alketbi.security import SecurityService
from app.mohammed_al_ali.asset_service import AssetService, SearchService
from app.mohammed_al_ali.request_service import RequestService
from conftest import future, request_data


def asset_data(**kw):
    d = {"name": "Test monitor", "description": "24 inch", "category_id": "1", "quantity": "2",
         "condition": "Good", "est_value_aed": "500", "location": "Room 1", "purchase_date": "2022-01-01"}
    d.update(kw)
    return d


def test_register_asset_creates_registered_asset_with_history(db, user):
    a = AssetService(db).register_asset(asset_data(), user("khalid@campus.test"))
    assert a.status == "Registered" and a.tag_number.startswith("CC-")
    events = [r["event_type"] for r in db.execute("SELECT event_type FROM asset_history WHERE asset_id=?", (a.asset_id,))]
    assert events == ["Created", "Draft -> Registered"]


@pytest.mark.parametrize("bad", [{"quantity": "0"}, {"est_value_aed": "-5"}, {"purchase_date": future()},
                                 {"condition": "Excellent"}, {"name": ""}])
def test_register_asset_validation(db, user, bad):
    with pytest.raises(DomainError):
        AssetService(db).register_asset(asset_data(**bad), user("khalid@campus.test"))


def test_requester_cannot_register_assets(db, user):
    with pytest.raises(DomainError):
        AssetService(db).register_asset(asset_data(), user("hessa@campus.test"))


def test_publish_only_registered_assets(db, user):
    svc, khalid = AssetService(db), user("khalid@campus.test")
    a = svc.register_asset(asset_data(), khalid)
    svc.publish(a.asset_id, khalid, SecurityService(db))
    assert Asset.get(db, a.asset_id).status == "Available"
    with pytest.raises(DomainError):
        svc.publish(a.asset_id, khalid, SecurityService(db))   # already published


def test_other_department_cannot_publish(db, user):
    a = AssetService(db).register_asset(asset_data(), user("khalid@campus.test"))
    with pytest.raises(DomainError):
        AssetService(db).publish(a.asset_id, user("mona@campus.test"), SecurityService(db))


def test_search_filters(db):
    s = SearchService(db)
    assert any("monitor" in r["name"].lower() for r in s.search("monitor"))
    assert all(r["condition"] == "Good" for r in s.search(condition="Good"))
    assert all(r["status"] == "Available" for r in s.search())      # BR-16
    assert not any(r["name"] == "Epson classroom projector" for r in s.search("projector"))  # not published


def test_submit_and_track_request(db, user):
    hessa = user("hessa@campus.test")
    req = RequestService(db).submit_request(request_data(), hessa)
    assert req.status == "Submitted"
    assert [r["request_id"] for r in RequestService(db).mine(hessa.user_id)] == [req.request_id]


@pytest.mark.parametrize("bad", [{"category": ""}, {"purpose": ""}, {"quantity": "0"}, {"urgency": "Urgent"},
                                 {"required_date": "2000-01-01"}])
def test_request_validation(db, user, bad):
    with pytest.raises(DomainError):
        RequestService(db).submit_request(request_data(**bad), user("hessa@campus.test"))


def test_invalid_category_is_a_validation_error(db, user):
    with pytest.raises(DomainError, match="valid category"):
        AssetService(db).register_asset(asset_data(category_id="999"), user("khalid@campus.test"))


def test_cannot_edit_locked_asset(db, user):
    db.execute("UPDATE asset SET status='In Transfer' WHERE asset_id=1")
    with pytest.raises(DomainError):
        AssetService(db).update_asset(1, {"quantity": "50"}, user("khalid@campus.test"), SecurityService(db))


# ---------------- AI 1 classification ----------------
from app.abdulla.ai_core import AIFacade, AIResult  # noqa: E402
from app.mohammed_al_ali.classification import ClassificationService  # noqa: E402


def test_classification_example_from_brief(db):
    r = ClassificationService(db).classify("Dell 24-inch monitor", "small scratch")
    assert r.content["category_label"] == "IT Equipment / Monitor"
    assert r.content["condition"] == "Good"
    assert "dell" in r.content["tags"] and "24-inch" in r.content["tags"] and r.confidence >= 0.8
    assert db.execute("SELECT COUNT(*) FROM ai_output WHERE function_name='classify'").fetchone()[0] == 1


def test_classification_name_wins_over_description(db):
    r = ClassificationService(db).classify("HP laptop", "cracked screen, not working")
    assert r.content["category_label"] == "IT Equipment / Laptop" and r.content["condition"] == "Broken"


def test_classification_unknown_is_low_confidence(db):
    r = ClassificationService(db).classify("Thing", "")
    assert r.content["category_id"] is None and r.confidence < 0.5


class LowConfidenceModel:
    enabled = True

    def send(self, feature, data):
        return AIResult(content={"category_id": 1, "condition": "Good"}, confidence=0.1, explanation="",
                        model_id="test-llm", used_fallback=False)


def test_low_confidence_model_answer_is_not_used(db):
    r = ClassificationService(db, AIFacade(db, adapter=LowConfidenceModel())).classify("office chair", "")
    assert r.model_id == "rules" and r.content["category_label"] == "Furniture / Chair"


def test_custodian_edit_of_ai_suggestion_is_logged(login, db):
    k = login("khalid@campus.test")
    sug = k.post("/ai/classify", json={"name": "Dell monitor", "description": ""}).json
    k.post("/assets/new", data={"name": "Dell monitor", "category_id": "7", "condition": "Fair", "quantity": "1",
                                "ai_output_id": sug["ai_output_id"], "ai_suggested": f"{sug['category_id']}|{sug['condition']}"})
    assert db.execute("SELECT COUNT(*) FROM ai_override").fetchone()[0] == 1
