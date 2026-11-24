"""C4 Request and track, with reservations (owner: Mohammed Al Ali)."""
from datetime import date, datetime, timedelta

from app.mohammed_alketbi.audit import AuditService
from app.db import now, transaction
from app.models import Asset, Request, Reservation
from app.mubarak.states import URGENCIES, DomainError, RequestStatus
from app.mohammed_alketbi.notifications import NotificationService

RESERVATION_DAYS = 7   # BR-04


class RequestService:
    def __init__(self, db):
        self.db = db
        self.audit = AuditService(db)
        self.notes = NotificationService(db)

    def change_status(self, req, new_status, actor_id):
        RequestStatus.check_move(req.status, new_status)
        self.db.execute("UPDATE request SET status=? WHERE request_id=?", (new_status, req.request_id))
        self.audit.log(actor_id, "request.status", f"request:{req.request_id}",
                       old={"status": req.status}, new={"status": new_status})
        req.status = new_status
        return req

    def validate(self, data):
        errors = []
        for field, label in (("category", "Category"), ("purpose", "Purpose"), ("required_date", "Required date")):
            if not (data.get(field) or "").strip():
                errors.append(f"{label} is required (BR-19).")
        try:
            if int(data.get("quantity", 0)) < 1:
                errors.append("Quantity must be 1 or more.")
        except (TypeError, ValueError):
            errors.append("Quantity must be a whole number.")
        if data.get("urgency") not in URGENCIES:
            errors.append("Urgency must be Low, Medium or High.")
        if data.get("required_date"):
            try:
                if date.fromisoformat(data["required_date"]) < date.today():
                    errors.append("Required date cannot be in the past.")
            except ValueError:
                errors.append("Required date must be a valid date.")
        return errors

    def submit_request(self, data, user):
        errors = self.validate(data)
        if errors:
            raise DomainError(" ".join(errors))
        with transaction(self.db):
            cur = self.db.execute(
                "INSERT INTO request (requester_id, dept_id, category, purpose, specifications, quantity,"
                " preferred_condition, urgency, location, required_date, status, created_at)"
                " VALUES (?,?,?,?,?,?,?,?,?,?, 'Submitted', ?)",
                (user.user_id, user.dept_id, data["category"].strip(), data["purpose"].strip(),
                 (data.get("specifications") or "").strip(), int(data["quantity"]),
                 data.get("preferred_condition") or "Any", data["urgency"],
                 (data.get("location") or "").strip(), data["required_date"], now()))
            req = Request.get(self.db, cur.lastrowid)
            self.audit.log(user.user_id, "request.create", f"request:{req.request_id}", new=req.as_dict())
            self.notes.notify("request.submitted", [user.user_id],
                              f"Your request R-{req.request_id:04d} ({req.quantity} x {req.category}) was submitted.")
        return req

    def cancel_request(self, request_id, user):
        req = Request.get(self.db, request_id)
        if not req or req.requester_id != user.user_id:
            raise DomainError("You can only cancel your own requests.")
        if req.status not in ("Draft", "Submitted", "Matched / Reserved"):
            raise DomainError(f"A request that is {req.status} cannot be cancelled. "
                              "If it was approved, receive the item or ask the approver.")
        with transaction(self.db):
            res = Reservation.where(self.db, "request_id=? AND status='Active'", (request_id,))
            for r in res:
                ReservationService(self.db).release(r.reservation_id, user.user_id, "Request cancelled")
            self.db.execute("UPDATE approval SET status='Cancelled' WHERE request_id=? AND status='Pending'", (request_id,))
            self.db.execute("UPDATE transfer SET status='Cancelled' WHERE request_id=? AND status='Pending Approval'", (request_id,))
            self.change_status(Request.get(self.db, request_id), "Cancelled", user.user_id)

    def expire_old_requests(self):
        today = date.today().isoformat()
        with transaction(self.db):
            for req in Request.where(self.db, "status='Submitted' AND required_date < ?", (today,)):
                self.change_status(req, "Expired", None)
                self.notes.notify("request.expired", [req.requester_id],
                                  f"Request R-{req.request_id:04d} expired: the required date passed (BR-19).")

    def mine(self, user_id):
        return self.db.execute(
            "SELECT r.*, (SELECT a.name FROM reservation s JOIN asset a ON a.asset_id=s.asset_id"
            "   WHERE s.request_id=r.request_id ORDER BY s.reservation_id DESC LIMIT 1) AS asset_name,"
            " (SELECT t.status FROM transfer t WHERE t.request_id=r.request_id ORDER BY t.transfer_id DESC LIMIT 1) AS transfer_status,"
            " (SELECT t.transfer_id FROM transfer t WHERE t.request_id=r.request_id ORDER BY t.transfer_id DESC LIMIT 1) AS transfer_id"
            " FROM request r WHERE r.requester_id=? ORDER BY r.request_id DESC", (user_id,)).fetchall()


class ReservationService:
    """Reserving an asset for a request. Runs in one locked transaction so
    the last unit can never be reserved by two people (core feature C5)."""

    def __init__(self, db):
        self.db = db
        self.audit = AuditService(db)
        self.notes = NotificationService(db)

    def reserve(self, asset_id, request_id, user):
        from app.mohammed_al_ali.asset_service import AssetService
        from app.mubarak.approval_service import ApprovalService

        assets = AssetService(self.db)
        with transaction(self.db):
            req = Request.get(self.db, request_id)
            if not req or req.requester_id != user.user_id:
                raise DomainError("You can only reserve for your own request.")
            if req.status != "Submitted":
                raise DomainError(f"Request R-{request_id:04d} is {req.status}; it already has an item or is closed.")
            asset = Asset.get(self.db, asset_id)       # read again inside the lock
            if not asset or not asset.is_available():
                raise DomainError("This item is no longer available. Someone else may have reserved it.")
            if asset.owner_dept_id == req.dept_id:
                raise DomainError("This item already belongs to your department.")
            if req.quantity > asset.quantity:
                raise DomainError(f"Only {asset.quantity} unit(s) are available; your request needs {req.quantity}.")
            active = self.db.execute("SELECT COUNT(*) FROM reservation WHERE asset_id=? AND status='Active'",
                                     (asset_id,)).fetchone()[0]
            if active:
                raise DomainError("This item already has an active reservation (BR-04).")

            target = assets.split_for_reservation(asset, req.quantity, user.user_id)
            reserved_at = datetime.now()
            cur = self.db.execute(
                "INSERT INTO reservation (asset_id, request_id, quantity, reserved_at, expires_at, status)"
                " VALUES (?,?,?,?,?, 'Active')",
                (target.asset_id, request_id, req.quantity, reserved_at.isoformat(timespec="seconds"),
                 (reserved_at + timedelta(days=RESERVATION_DAYS)).isoformat(timespec="seconds")))
            assets.change_status(target, "Reserved", user.user_id, f"Reserved for request R-{request_id:04d}",
                                 f"reservation:{cur.lastrowid}")
            RequestService(self.db).change_status(req, "Matched / Reserved", user.user_id)
            ApprovalService(self.db).create_transfer_approval(target, req, user)
        return target

    def release(self, reservation_id, actor_id, reason, new_status="Released"):
        from app.mohammed_al_ali.asset_service import AssetService
        with transaction(self.db):
            res = Reservation.get(self.db, reservation_id)
            if res.status != "Active":
                return
            self.db.execute("UPDATE reservation SET status=? WHERE reservation_id=?", (new_status, reservation_id))
            asset = Asset.get(self.db, res.asset_id)
            if asset.status == "Reserved":
                AssetService(self.db).change_status(asset, "Available", actor_id, reason)

    def expire_old_reservations(self):
        """BR-04: a reservation not approved within 7 days expires."""
        with transaction(self.db):
            for res in Reservation.where(self.db, "status='Active' AND expires_at < ?", (now(),)):
                self.release(res.reservation_id, None, "Reservation expired after 7 days", "Expired")
                self.db.execute("UPDATE approval SET status='Cancelled', reason='Reservation expired'"
                                " WHERE request_id=? AND status='Pending'", (res.request_id,))
                self.db.execute("UPDATE transfer SET status='Cancelled' WHERE request_id=? AND status='Pending Approval'",
                                (res.request_id,))
                req = Request.get(self.db, res.request_id)
                if req.status == "Matched / Reserved":
                    RequestService(self.db).change_status(req, "Submitted", None)
                self.notes.notify("reservation.expired", [req.requester_id],
                                  f"Your reservation for R-{req.request_id:04d} expired before approval.")
