"""Tests for Mubarak: C5 approve and transfer, C6 states and history, AI 3 advice."""
import sqlite3

import pytest

from app.models import Approval, Asset, Request, Transfer
from app.mubarak.states import AssetStatus, DomainError, TransferStatus
from app.mubarak.approval_service import ApprovalService
from app.mubarak.maintenance_service import EndOfLifeService, MaintenanceService
from app.mohammed_al_ali.request_service import RequestService, ReservationService
from app.mubarak.transfer_service import TransferService
from app.mohammed_alketbi.security import SecurityService
from conftest import request_data

CHAIRS = 2   # seed: "Ergonomic office chairs", 10 units, Engineering


def reserve_chairs(db, user, email="hessa@campus.test", qty="4"):
    u = user(email)
    req = RequestService(db).submit_request(request_data(quantity=qty), u)
    asset = ReservationService(db).reserve(CHAIRS, req.request_id, u)
    approval = Approval.where(db, "request_id=?", (req.request_id,))[0]
    return u, req, asset, approval


def test_reserve_splits_batch_and_creates_pending_approval(db, user):
    _, req, asset, approval = reserve_chairs(db, user)
    assert asset.quantity == 4 and asset.status == "Reserved"
    assert Asset.get(db, CHAIRS).quantity == 6 and Asset.get(db, CHAIRS).status == "Available"
    assert approval.status == "Pending"
    assert Request.get(db, req.request_id).status == "Matched / Reserved"


def test_no_self_approval(db, user):
    # Sara is the Engineering rep; she requests Engineering-owned... use CS laptops (asset 5) requested by Omar (CS rep)
    sara = user("sara.rep@campus.test")
    req = RequestService(db).submit_request(request_data(category="Laptop", quantity="1"), sara)
    ReservationService(db).reserve(5, req.request_id, sara)
    approval = Approval.where(db, "request_id=?", (req.request_id,))[0]
    admin_sara = sara
    admin_sara.role = "admin"    # even an admin cannot approve their own request
    with pytest.raises(DomainError, match="own request"):
        ApprovalService(db).decide(approval.approval_id, "Approved", "", admin_sara)


def test_only_owning_department_rep_can_approve(db, user):
    _, _, _, approval = reserve_chairs(db, user)
    with pytest.raises(DomainError):
        ApprovalService(db).decide(approval.approval_id, "Approved", "", user("omar.rep@campus.test"))  # CS rep


def test_reject_needs_reason_and_releases_item(db, user):
    _, req, asset, approval = reserve_chairs(db, user)
    sara = user("sara.rep@campus.test")
    with pytest.raises(DomainError):
        ApprovalService(db).decide(approval.approval_id, "Rejected", "", sara)
    ApprovalService(db).decide(approval.approval_id, "Rejected", "Needed for exams", sara)
    assert Asset.get(db, asset.asset_id).status == "Available"
    assert Request.get(db, req.request_id).status == "Rejected"


def test_full_transfer_changes_owner_only_after_receipt(db, user):
    hessa, req, asset, approval = reserve_chairs(db, user)
    ApprovalService(db).decide(approval.approval_id, "Approved", "", user("sara.rep@campus.test"))
    a = Asset.get(db, asset.asset_id)
    assert a.status == "In Transfer" and a.owner_dept_id != hessa.dept_id      # not moved yet (BR-06)

    t = Transfer.where(db, "request_id=?", (req.request_id,))[0]
    with pytest.raises(DomainError):
        TransferService(db).confirm_receipt(t.transfer_id, user("ali@campus.test"))  # not the receiver
    TransferService(db).confirm_receipt(t.transfer_id, hessa)

    a = Asset.get(db, asset.asset_id)
    assert (a.owner_dept_id, a.custodian_id, a.status) == (hessa.dept_id, hessa.user_id, "Registered")
    assert Transfer.get(db, t.transfer_id).status == "Completed"
    assert Request.get(db, req.request_id).status == "Fulfilled"
    events = [r["event_type"] for r in db.execute("SELECT event_type FROM asset_history WHERE asset_id=?", (a.asset_id,))]
    assert events[-3:] == ["Available -> Reserved", "Reserved -> In Transfer", "In Transfer -> Registered"]
    kinds = {r["event_type"] for r in db.execute("SELECT event_type FROM notification")}
    assert {"request.made", "request.approved", "transfer.received"} <= kinds


def test_last_item_cannot_go_to_two_people(db, user):
    hessa, ali = user("hessa@campus.test"), user("ali@campus.test")
    # Projector-free example: the 2 oscilloscopes (asset 4). Both ask for 2.
    r1 = RequestService(db).submit_request(request_data(category="Instrument", quantity="2"), hessa)
    r2 = RequestService(db).submit_request(request_data(category="Instrument", quantity="2"), ali)
    ReservationService(db).reserve(4, r1.request_id, hessa)
    with pytest.raises(DomainError, match="no longer available"):
        ReservationService(db).reserve(4, r2.request_id, ali)


def test_asset_state_machine_rejects_illegal_moves():
    assert AssetStatus.can_move("Available", "Reserved")
    assert not AssetStatus.can_move("Available", "Disposed")
    assert not AssetStatus.can_move("Disposed", "Available")
    with pytest.raises(DomainError):
        TransferStatus.check_move("Pending Approval", "Completed")


def test_history_cannot_be_edited_or_deleted(db):
    with pytest.raises(sqlite3.DatabaseError):
        db.execute("UPDATE asset_history SET details='x'")
    db.execute("INSERT INTO audit_log (action, outcome, event_time) VALUES ('test', 'OK', '2026-01-01')")
    with pytest.raises(sqlite3.DatabaseError):
        db.execute("DELETE FROM audit_log")


def test_in_maintenance_asset_cannot_be_reserved(db, user):
    khalid, hessa = user("khalid@campus.test"), user("hessa@campus.test")
    MaintenanceService(db).report_defect(1, "Screen flickers", khalid)
    req = RequestService(db).submit_request(request_data(category="Monitor", quantity="1"), hessa)
    with pytest.raises(DomainError):
        ReservationService(db).reserve(1, req.request_id, hessa)


def test_maintenance_cycle_returns_asset_to_service(db, user):
    khalid, admin = user("khalid@campus.test"), user("admin@campus.test")
    svc = MaintenanceService(db)
    t = svc.report_defect(1, "Screen flickers", khalid)
    svc.inspect(t.ticket_id, True, admin)
    with pytest.raises(DomainError):
        svc.record_repair(t.ticket_id, "Replaced cable", "-10", admin)
    svc.record_repair(t.ticket_id, "Replaced cable", "40", admin)
    svc.verify(t.ticket_id, "Good", admin)
    assert Asset.get(db, 1).status == "Registered"


def test_disposal_needs_assessment_and_admin(db, user):
    khalid, admin = user("khalid@campus.test"), user("admin@campus.test")
    eol = EndOfLifeService(db)
    with pytest.raises(DomainError, match="BR-10"):
        eol.create_request(3, "Dispose", "Broken", "", None, khalid, SecurityService(db))
    e = eol.create_request(3, "Recycle", "Bulb and board broken", "", None, khalid, SecurityService(db))
    with pytest.raises(DomainError):
        eol.admin_decision(e.eol_id, "Approved", "", khalid)
    eol.admin_decision(e.eol_id, "Approved", "", admin)
    assert Asset.get(db, 3).status == "Recycled"


def test_cannot_cancel_after_approval(db, user):
    hessa, req, asset, approval = reserve_chairs(db, user)
    ApprovalService(db).decide(approval.approval_id, "Approved", "", user("sara.rep@campus.test"))
    with pytest.raises(DomainError, match="cannot be cancelled"):
        RequestService(db).cancel_request(req.request_id, hessa)
    assert Asset.get(db, asset.asset_id).status == "In Transfer"


def test_cancel_before_approval_releases_item(db, user):
    hessa, req, asset, _ = reserve_chairs(db, user)
    RequestService(db).cancel_request(req.request_id, hessa)
    assert Asset.get(db, asset.asset_id).status == "Available"
    assert Transfer.where(db, "request_id=?", (req.request_id,))[0].status == "Cancelled"


def test_other_department_cannot_report_defect(db, user):
    with pytest.raises(DomainError):
        MaintenanceService(db).report_defect(1, "x", user("mona@campus.test"))     # CS custodian, Eng asset
    assert Asset.get(db, 1).status == "Available"


def test_eol_rejects_unknown_action_and_duplicates(db, user):
    khalid, eol = user("khalid@campus.test"), EndOfLifeService(db)
    with pytest.raises(DomainError):
        eol.create_request(3, "Burn", "x", "", None, khalid, SecurityService(db))
    eol.create_request(3, "Recycle", "Broken", "", None, khalid, SecurityService(db))
    with pytest.raises(DomainError, match="pending"):
        eol.create_request(3, "Donate", "x", "", None, khalid, SecurityService(db))


def test_expired_reservation_returns_item(db, user):
    hessa, req, asset, approval = reserve_chairs(db, user)
    db.execute("UPDATE reservation SET expires_at='2000-01-01' WHERE request_id=?", (req.request_id,))
    ReservationService(db).expire_old_reservations()
    assert Asset.get(db, asset.asset_id).status == "Available"
    assert Request.get(db, req.request_id).status == "Submitted"
    assert Approval.get(db, approval.approval_id).status == "Cancelled"


# ---------------- AI 3 sustainable-action advice ----------------
from app.mubarak.advice import RecommendationService  # noqa: E402


def test_advice_projector_example(db):
    r = RecommendationService(db).recommend(3, est_repair_cost=120)      # Epson projector, bulb broken
    assert r.content["action"] == "Repair" and r.content["reasons"]


def test_advice_reuse_for_good_condition(db):
    assert RecommendationService(db).recommend(2).content["action"] == "Reuse"     # good chairs


def test_advice_never_disposes_recyclable_items(db):
    db.execute("UPDATE asset SET purchase_date='2010-01-01' WHERE asset_id=3")     # old broken projector
    assert RecommendationService(db).recommend(3, est_repair_cost=5000).content["action"] == "Recycle"


def test_advice_override_is_logged(login, db):
    k = login("khalid@campus.test")
    page = k.get("/assets/3/advice").data.decode()
    import re
    oid = re.search(r'name="ai_output_id" value="(\d+)"', page).group(1)
    k.post("/assets/3/advice", data={"ai_output_id": oid, "final_action": "Recycle", "reason": "no spare parts"})
    assert db.execute("SELECT final_value FROM ai_override").fetchone()[0] == "Recycle"
