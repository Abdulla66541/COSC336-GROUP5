"""C6 life cycle: maintenance (UC-13, UC-24, UC-14) and end of life (UC-16, UC-25) (owner: Mubarak)."""
from datetime import date

from app.mohammed_alketbi.audit import AuditService
from app.db import now, transaction
from app.models import Asset, EndOfLifeRequest, MaintenanceTicket
from app.mubarak.states import DomainError, MaintenanceStatus
from app.mohammed_alketbi.notifications import NotificationService
from app.mohammed_al_ali.asset_service import AssetService

FINANCE_LIMIT_AED = 5000   # BR-09


class MaintenanceService:
    def __init__(self, db):
        self.db = db
        self.assets = AssetService(db)
        self.audit = AuditService(db)
        self.notes = NotificationService(db)

    def _move(self, ticket, new_status, actor_id):
        MaintenanceStatus.check_move(ticket.status, new_status)
        self.db.execute("UPDATE maintenance_ticket SET status=? WHERE ticket_id=?", (new_status, ticket.ticket_id))
        self.assets.history.record(ticket.asset_id, f"Maintenance: {new_status}", actor_id, f"ticket:{ticket.ticket_id}")
        self.audit.log(actor_id, "maintenance.status", f"ticket:{ticket.ticket_id}",
                       old={"status": ticket.status}, new={"status": new_status})
        ticket.status = new_status

    def report_defect(self, asset_id, description, user):
        if not (description or "").strip():
            raise DomainError("Describe the defect.")
        with transaction(self.db):
            asset = Asset.get(self.db, asset_id)
            if not asset:
                raise DomainError("Asset not found.")
            if user.role != "admin" and user.dept_id != asset.owner_dept_id:
                raise DomainError("Only the owning department or an admin can report a defect on this asset.")
            if asset.status not in ("Registered", "Available"):
                raise DomainError(f"An asset that is {asset.status} cannot go to maintenance now (BR-05).")
            if asset.status == "Available":
                self.db.execute("UPDATE listing SET status='Withdrawn' WHERE asset_id=? AND status='Active'", (asset_id,))
            cur = self.db.execute(
                "INSERT INTO maintenance_ticket (asset_id, reported_by, description, status, created_at)"
                " VALUES (?,?,?, 'Reported', ?)", (asset_id, user.user_id, description.strip(), now()))
            self.assets.change_status(asset, "In Maintenance", user.user_id, description.strip(), f"ticket:{cur.lastrowid}")
            admins = [r["user_id"] for r in self.db.execute("SELECT user_id FROM user WHERE role='admin'")]
            self.notes.notify("maintenance.reported", admins, f"Defect reported on '{asset.name}': {description}")
            return MaintenanceTicket.get(self.db, cur.lastrowid)

    def _ticket(self, ticket_id):
        t = MaintenanceTicket.get(self.db, ticket_id)
        if not t:
            raise DomainError("Ticket not found.")
        return t

    def inspect(self, ticket_id, repairable, user):
        with transaction(self.db):
            t = self._ticket(ticket_id)
            self.db.execute("UPDATE maintenance_ticket SET inspection_at=?, assigned_to=? WHERE ticket_id=?",
                            (now(), user.user_id, ticket_id))
            self._move(t, "Inspected", user.user_id)
            if repairable:
                self._move(t, "Repair Approved", user.user_id)
            else:
                self._move(t, "Not Repairable", user.user_id)
                self.assets.change_status(Asset.get(self.db, t.asset_id), "Retired", user.user_id,
                                          "Inspection: not repairable")

    def record_repair(self, ticket_id, action, cost_aed, user):
        try:
            cost = float(cost_aed)
        except (TypeError, ValueError):
            raise DomainError("Repair cost must be a number.")
        if cost < 0:
            raise DomainError("Repair cost cannot be negative.")
        if not (action or "").strip():
            raise DomainError("Describe the repair.")
        with transaction(self.db):
            t = self._ticket(ticket_id)
            self._move(t, "In Repair", user.user_id)
            self.db.execute("INSERT INTO repair_record (ticket_id, performed_by, action, cost_aed, repair_date)"
                            " VALUES (?,?,?,?,?)", (ticket_id, user.user_id, action.strip(), cost, date.today().isoformat()))
            self._move(t, "Completed", user.user_id)

    def verify(self, ticket_id, condition, user):
        with transaction(self.db):
            t = self._ticket(ticket_id)
            self._move(t, "Verified", user.user_id)
            asset = Asset.get(self.db, t.asset_id)
            if condition and condition not in ("New", "Good", "Fair", "Poor", "Broken"):
                raise DomainError("Invalid condition.")
            if condition:
                self.db.execute("UPDATE asset SET condition=? WHERE asset_id=?", (condition, asset.asset_id))
            self.assets.change_status(asset, "Registered", user.user_id, f"Repair verified; condition now {condition}")
            # one repaired unit per ticket (conservative estimate for batches)
            self.db.execute("INSERT INTO reuse_event (asset_id, event_type, quantity, avoided_value_aed, event_time)"
                            " VALUES (?, 'repair', 1, 0, ?)", (asset.asset_id, now()))

    def open_tickets(self):
        return self.db.execute(
            "SELECT t.*, a.name AS asset_name, a.tag_number, u.name AS reporter FROM maintenance_ticket t"
            " JOIN asset a ON a.asset_id=t.asset_id JOIN user u ON u.user_id=t.reported_by"
            " WHERE t.status NOT IN ('Verified','Not Repairable') ORDER BY t.ticket_id").fetchall()


class EndOfLifeService:
    def __init__(self, db):
        self.db = db
        self.assets = AssetService(db)
        self.audit = AuditService(db)
        self.notes = NotificationService(db)

    def create_request(self, asset_id, action, reason, assessment, recipient, user, security):
        asset = Asset.get(self.db, asset_id)
        if action not in ("Donate", "Recycle", "Dispose"):
            raise DomainError("Action must be Donate, Recycle or Dispose.")
        if not asset or not security.can_manage_asset(user, asset):
            raise DomainError("You cannot request end-of-life for this asset.")
        if self.db.execute("SELECT 1 FROM end_of_life_request WHERE asset_id=? AND status='Pending'",
                           (asset_id,)).fetchone():
            raise DomainError("This asset already has a pending end-of-life request.")
        if asset.status not in ("Registered", "Retired"):
            raise DomainError(f"An asset that is {asset.status} cannot be donated, recycled or disposed (BR-05).")
        if not (reason or "").strip():
            raise DomainError("A reason is required (BR-09).")
        if action == "Dispose" and len((assessment or "").strip()) < 10:
            raise DomainError("Before disposal, explain why reuse, transfer, repair, donation and recycling "
                              "do not fit (BR-10).")
        with transaction(self.db):
            cur = self.db.execute(
                "INSERT INTO end_of_life_request (asset_id, requested_by, action, reason, alternatives_assessment,"
                " status, recipient, created_at) VALUES (?,?,?,?,?, 'Pending', ?, ?)",
                (asset_id, user.user_id, action, reason.strip(), (assessment or "").strip(), recipient, now()))
            self.assets.history.record(asset_id, f"End-of-life requested: {action}", user.user_id, f"eol:{cur.lastrowid}", reason)
            admins = [r["user_id"] for r in self.db.execute("SELECT user_id FROM user WHERE role='admin'")]
            self.notes.notify("eol.requested", admins, f"{action} requested for '{asset.name}': {reason}")
            return EndOfLifeRequest.get(self.db, cur.lastrowid)

    def admin_decision(self, eol_id, decision, reason, user):
        if user.role != "admin":
            raise DomainError("Only an administrator can approve donation, recycling or disposal (BR-09).")
        with transaction(self.db):
            e = EndOfLifeRequest.get(self.db, eol_id)
            if decision not in ("Approved", "Rejected"):
                raise DomainError("Decision must be Approved or Rejected.")
            if not e or e.status != "Pending":
                raise DomainError("This request was already decided.")
            if e.requested_by == user.user_id:
                raise DomainError("You cannot approve your own request (BR-07).")
            asset = Asset.get(self.db, e.asset_id)
            if decision == "Rejected":
                self.db.execute("UPDATE end_of_life_request SET status='Rejected' WHERE eol_id=?", (eol_id,))
                self.assets.history.record(asset.asset_id, "End-of-life rejected", user.user_id, f"eol:{eol_id}", reason)
            else:
                final = {"Donate": "Donated", "Recycle": "Recycled", "Dispose": "Disposed"}[e.action]
                self.db.execute("UPDATE end_of_life_request SET status='Completed' WHERE eol_id=?", (eol_id,))
                note = reason or ""
                if asset.est_value_aed * asset.quantity > FINANCE_LIMIT_AED:
                    note += " [Value above AED 5,000: Finance Officer sign-off recorded by admin (BR-09)]"
                self.assets.change_status(asset, final, user.user_id, note.strip(), f"eol:{eol_id}")
                self.db.execute("UPDATE asset SET active=0 WHERE asset_id=?", (asset.asset_id,))
                if e.action in ("Donate", "Recycle"):
                    self.db.execute("INSERT INTO reuse_event (asset_id, event_type, quantity, avoided_value_aed, event_time)"
                                    " VALUES (?,?,?,0,?)", (asset.asset_id, e.action.lower(), asset.quantity, now()))
            self.audit.log(user.user_id, "eol.decide", f"eol:{eol_id}", new={"decision": decision, "reason": reason})
            self.notes.notify("eol.decided", [e.requested_by], f"{e.action} of '{asset.name}' was {decision.lower()}.")

    def pending(self):
        return self.db.execute(
            "SELECT e.*, a.name AS asset_name, a.tag_number, a.est_value_aed, a.quantity, u.name AS requester"
            " FROM end_of_life_request e JOIN asset a ON a.asset_id=e.asset_id JOIN user u ON u.user_id=e.requested_by"
            " WHERE e.status='Pending' ORDER BY e.eol_id").fetchall()
