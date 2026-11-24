"""Tests for Abdulla: C7 sustainability dashboard, AI 2 matching and ranking, AI 5 generated report,
and the shared AI layer."""
import pytest

from app.abdulla.ai_core import AIFacade, AIResult, PrivacyFilter
from app.abdulla.ai_report import AIReportService
from app.abdulla.matching import MatchingService
from app.abdulla.sustainability_service import SustainabilityService
from app.models import Approval, DomainError
from app.mohammed_al_ali.request_service import RequestService, ReservationService
from app.mubarak.approval_service import ApprovalService
from app.mubarak.transfer_service import TransferService
from conftest import request_data

TODAY_RANGE = ("2000-01-01", "2099-12-31")


def complete_chair_transfer(db, user):
    hessa = user("hessa@campus.test")
    req = RequestService(db).submit_request(request_data(), hessa)
    ReservationService(db).reserve(2, req.request_id, hessa)
    ApprovalService(db).decide(Approval.where(db, "request_id=?", (req.request_id,))[0].approval_id,
                               "Approved", "", user("sara.rep@campus.test"))
    t = db.execute("SELECT transfer_id FROM transfer WHERE request_id=?", (req.request_id,)).fetchone()[0]
    TransferService(db).confirm_receipt(t, hessa)


# ---------------- AI 2 matching ----------------
def test_matching_returns_top5_with_score_and_reason(db, user):
    req = RequestService(db).submit_request(request_data(), user("hessa@campus.test"))
    matches = MatchingService(db).find_matches(req.request_id).content["matches"]
    assert 1 <= len(matches) <= 5
    assert matches[0]["asset"]["name"] == "Ergonomic office chairs"
    assert matches[0]["score"] >= matches[-1]["score"] and "same category" in matches[0]["reason"]


def test_matching_excludes_own_department(db, user):
    req = RequestService(db).submit_request(request_data(category="Laptop"), user("ali@campus.test"))  # CS
    ids = [m["asset_id"] for m in MatchingService(db).find_matches(req.request_id).content["matches"]]
    assert 5 not in ids          # CS's own laptops are not suggested


class BadModel:
    """Returns an asset id that is not in the listings: must be rejected."""
    enabled = True

    def send(self, feature, data):
        return AIResult(content={"matches": [{"asset_id": 999, "score": 99, "reason": "x"}]}, confidence=0.9,
                        explanation="", model_id="test-llm", used_fallback=False)


def test_invalid_model_answer_falls_back(db, user):
    req = RequestService(db).submit_request(request_data(), user("hessa@campus.test"))
    r = MatchingService(db, AIFacade(db, adapter=BadModel())).find_matches(req.request_id)
    assert r.model_id == "rules" and r.content["matches"][0]["asset_id"] == 2


class DownModel:
    enabled = True

    def send(self, feature, data):
        raise TimeoutError("model down")


def test_model_timeout_falls_back(db, user):
    req = RequestService(db).submit_request(request_data(), user("hessa@campus.test"))
    assert MatchingService(db, AIFacade(db, adapter=DownModel())).find_matches(req.request_id).used_fallback


def test_privacy_filter_removes_personal_data():
    clean = PrivacyFilter().remove_personal_data({"purpose": "mail me at a.b@campus.test or +971 50 123 4567",
                                                  "requester_id": 7, "category": "Chair"})
    assert clean == {"purpose": "mail me at [email] or [phone]", "category": "Chair"}


# ---------------- C7 dashboard ----------------
def test_dashboard_counts_reuse_after_transfer(db, user):
    complete_chair_transfer(db, user)
    m = {x["name"]: x for x in SustainabilityService(db).metrics()}
    assert m["Items reused"]["value"] == "4"
    assert m["Purchases avoided (est.)"]["value"] == "AED 1,600"     # 4 x AED 400
    assert m["Waste diverted (est.)"]["value"] == "48"                # 4 x 12 kg
    assert m["CO2e avoided (est.)"]["value"] == "280"                 # 4 x 70 kg
    assert all(x["formula"] and x["source"] for x in m.values())


def test_dashboard_page_for_rep_not_requester(login):
    assert login("sara.rep@campus.test").get("/dashboard").status_code == 200
    assert login("hessa@campus.test").get("/dashboard").status_code == 403


# ---------------- AI 5 generated report ----------------
def test_ai_report_uses_only_database_figures(db, user):
    complete_chair_transfer(db, user)
    svc = AIReportService(db)
    rid = svc.generate(*TODAY_RANGE, user("admin@campus.test"))
    rep = svc.get(rid)
    assert rep["status"] == "Not reviewed" and rep["flags"] == ""
    assert "4 item(s) were reused" in rep["text"] and "AED 1,600" in rep["text"]


def test_ai_report_cannot_be_exported_before_review(db, user):
    svc = AIReportService(db)
    rid = svc.generate(*TODAY_RANGE, user("admin@campus.test"))
    with pytest.raises(DomainError, match="reviewed"):
        svc.export_text(rid)
    svc.mark_reviewed(rid, svc.get(rid)["text"], user("sara.rep@campus.test"))
    assert "Reviewed by: Sara Eng Rep" in svc.export_text(rid)


def test_ai_report_flags_wrong_numbers(db, user):
    complete_chair_transfer(db, user)
    svc = AIReportService(db)
    rid = svc.generate(*TODAY_RANGE, user("admin@campus.test"))
    wrong = svc.get(rid)["text"].replace("AED 1,600", "AED 25,000")
    with pytest.raises(DomainError, match="25000"):
        svc.mark_reviewed(rid, wrong, user("admin@campus.test"))
    assert svc.get(rid)["status"] == "Not reviewed"


class WrongNumberModel:
    enabled = True

    def send(self, feature, data):
        return AIResult(content={"text": "This month 99 items were reused, saving AED 25,000 (estimate)."},
                        confidence=0.9, explanation="", model_id="test-llm", used_fallback=False)


def test_ai_report_flags_model_invented_numbers(db, user):
    svc = AIReportService(db, AIFacade(db, adapter=WrongNumberModel()))
    rep = svc.get(svc.generate(*TODAY_RANGE, user("admin@campus.test")))
    assert "99" in rep["flags"] and "25000" in rep["flags"]


def test_ai_report_pages(login):
    a = login("admin@campus.test")
    r = a.post("/ai-reports", data={"start": "2026-01-01", "end": "2026-12-31"}, follow_redirects=True)
    assert b"Please review before sharing" in r.data
    assert a.get("/ai-reports/1/export", follow_redirects=True).data.count(b"cannot be shared") == 1
    assert login("hessa@campus.test").get("/ai-reports").status_code == 403
