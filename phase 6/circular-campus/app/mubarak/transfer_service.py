"""C5 Transfers (owner: Mubarak). UC-12, BR-06, BR-08."""
from app.mohammed_alketbi.audit import AuditService
from app.db import now, transaction
from app.models import Asset, Request, Transfer
from app.mubarak.states import DomainError, TransferStatus
from app.mohammed_alketbi.notifications import NotificationService


class TransferService:
    def __init__(self, db):
        self.db = db
        self.audit = AuditService(db)
        self.notes = NotificationService(db)

    def change_status(self, transfer, new_status, actor_id):
        TransferStatus.check_move(transfer.status, new_status)
        self.db.execute("UPDATE transfer SET status=? WHERE transfer_id=?", (new_status, transfer.transfer_id))
        self.audit.log(actor_id, "transfer.status", f"transfer:{transfer.transfer_id}",
                       old={"status": transfer.status}, new={"status": new_status})
        transfer.status = new_status
        return transfer

    def _get(self, transfer_id):
        t = Transfer.get(self.db, transfer_id)
        if not t:
            raise DomainError("Transfer not found.")
        return t

    def schedule(self, transfer_id, handover_date, location, user):
        with transaction(self.db):
            t = self._get(transfer_id)
            asset = Asset.get(self.db, t.asset_id)
            if user.role != "admin" and user.user_id != asset.custodian_id and \
                    not (user.role == "dept_rep" and user.dept_id == t.from_dept_id):
                raise DomainError("Only the sending custodian, its department rep or an admin can schedule.")
            if not handover_date or not (location or "").strip():
                raise DomainError("Handover date and location are required.")
            self.change_status(t, "Scheduled", user.user_id)
            self.db.execute("UPDATE transfer SET handover_date=?, handover_location=? WHERE transfer_id=?",
                            (handover_date, location.strip(), transfer_id))
            req = Request.get(self.db, t.request_id)
            self.notes.notify("transfer.scheduled", [req.requester_id],
                              f"Handover for '{asset.name}' set for {handover_date} at {location}.")

    def confirm_receipt(self, transfer_id, user, discrepancy_note=None):
        """The receiver confirms. Only then do owner, custodian and location
        change (BR-06, BR-08)."""
        from app.mohammed_al_ali.asset_service import AssetService
        from app.mohammed_al_ali.request_service import RequestService

        with transaction(self.db):
            t = self._get(transfer_id)
            req = Request.get(self.db, t.request_id)
            if user.user_id != req.requester_id:
                raise DomainError("Only the person who requested the item can confirm receipt.")
            if t.status == "Approved":                       # no handover booked: schedule for today
                self.change_status(t, "Scheduled", user.user_id)
            self.change_status(t, "Received", user.user_id)
            self.db.execute("UPDATE transfer SET received_by=?, received_at=?, discrepancy_note=? WHERE transfer_id=?",
                            (user.user_id, now(), discrepancy_note or None, transfer_id))
            asset = Asset.get(self.db, t.asset_id)
            old = {"owner_dept_id": asset.owner_dept_id, "custodian_id": asset.custodian_id, "location": asset.location}
            new_location = req.location or asset.location
            self.db.execute("UPDATE asset SET owner_dept_id=?, custodian_id=?, location=? WHERE asset_id=?",
                            (t.to_dept_id, user.user_id, new_location, asset.asset_id))
            self.audit.log(user.user_id, "asset.ownership", f"asset:{asset.asset_id}", old=old,
                           new={"owner_dept_id": t.to_dept_id, "custodian_id": user.user_id, "location": new_location})
            AssetService(self.db).change_status(asset, "Registered", user.user_id,
                                                f"Received by {user.name}; owner changed to new department"
                                                + (f". Note: {discrepancy_note}" if discrepancy_note else ""),
                                                f"transfer:{transfer_id}")
            self.change_status(t, "Completed", user.user_id)
            RequestService(self.db).change_status(req, "Fulfilled", user.user_id)
            # Reuse event drives the sustainability dashboard (Part 4)
            self.db.execute(
                "INSERT INTO reuse_event (asset_id, request_id, event_type, quantity, avoided_value_aed, event_time)"
                " VALUES (?,?, 'transfer', ?, ?, ?)",
                (asset.asset_id, req.request_id, t.quantity, asset.est_value_aed * t.quantity, now()))
            self.notes.notify("transfer.received", [asset.custodian_id] + self.notes.approvers_for_dept(t.from_dept_id),
                              f"{user.name} received '{asset.name}'. Transfer T-{transfer_id:04d} completed.")

    def overdue(self, days=14):
        """BR-08: transfers not completed within 14 days are reported."""
        return self.db.execute(
            "SELECT t.*, a.name AS asset_name FROM transfer t JOIN asset a ON a.asset_id=t.asset_id"
            " WHERE t.status IN ('Approved','Scheduled','In Transit') AND julianday('now') - julianday(t.created_at) > ?",
            (days,)).fetchall()
