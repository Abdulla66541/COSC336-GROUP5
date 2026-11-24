"""C5 Approvals (owner: Mubarak). UC-11, BR-06, BR-07."""
from app.mohammed_alketbi.audit import AuditService
from app.db import now, transaction
from app.models import Approval, Asset, Request, Reservation, Transfer
from app.mubarak.states import DomainError
from app.mohammed_alketbi.notifications import NotificationService
from app.mubarak.transfer_service import TransferService


class ApprovalService:
    def __init__(self, db):
        self.db = db
        self.audit = AuditService(db)
        self.notes = NotificationService(db)

    def create_transfer_approval(self, asset, req, requester):
        """Called when an item is reserved: opens a pending approval and a
        transfer record in 'Pending Approval'."""
        with transaction(self.db):
            cur = self.db.execute(
                "INSERT INTO approval (action_type, asset_id, request_id, status, created_at)"
                " VALUES ('transfer', ?, ?, 'Pending', ?)", (asset.asset_id, req.request_id, now()))
            self.db.execute(
                "INSERT INTO transfer (asset_id, request_id, quantity, from_dept_id, to_dept_id, status, created_at)"
                " VALUES (?,?,?,?,?, 'Pending Approval', ?)",
                (asset.asset_id, req.request_id, req.quantity, asset.owner_dept_id, req.dept_id, now()))
            self.audit.log(requester.user_id, "approval.create", f"approval:{cur.lastrowid}")
            approvers = [u for u in self.notes.approvers_for_dept(asset.owner_dept_id) if u != requester.user_id]
            self.notes.notify("request.made", approvers + [asset.custodian_id],
                              f"{requester.name} requested '{asset.name}' (x{req.quantity}) for R-{req.request_id:04d}."
                              " Approval needed.")
            return Approval.get(self.db, cur.lastrowid)

    def can_decide(self, user, approval):
        """Approver must be a dept rep of the owning department or an admin,
        and never the person who made the request (BR-07)."""
        asset = Asset.get(self.db, approval.asset_id)
        req = Request.get(self.db, approval.request_id) if approval.request_id else None
        if req and req.requester_id == user.user_id:
            return False, "You cannot approve your own request (BR-07)."
        if user.role == "admin":
            return True, None
        if user.role == "dept_rep" and user.dept_id == asset.owner_dept_id:
            return True, None
        return False, "Only the owning department's representative or an admin can decide (BR-06)."

    def get_pending(self, user):
        rows = self.db.execute(
            "SELECT p.*, a.name AS asset_name, a.tag_number, a.owner_dept_id, a.quantity AS asset_qty,"
            " r.purpose, r.quantity, r.urgency, r.requester_id, u.name AS requester_name, d.name AS to_dept"
            " FROM approval p JOIN asset a ON a.asset_id=p.asset_id"
            " LEFT JOIN request r ON r.request_id=p.request_id LEFT JOIN user u ON u.user_id=r.requester_id"
            " LEFT JOIN department d ON d.dept_id=r.dept_id"
            " WHERE p.status='Pending' AND p.action_type='transfer' ORDER BY p.approval_id").fetchall()
        return [r for r in rows if self.can_decide(user, Approval(r))[0]]

    def decide(self, approval_id, decision, reason, user):
        from app.mohammed_al_ali.asset_service import AssetService
        from app.mohammed_al_ali.request_service import RequestService, ReservationService

        if decision not in ("Approved", "Rejected"):
            raise DomainError("Decision must be Approved or Rejected.")
        if decision == "Rejected" and not (reason or "").strip():
            raise DomainError("A reason is required when rejecting.")
        with transaction(self.db):
            approval = Approval.get(self.db, approval_id)
            if not approval or approval.status != "Pending":
                raise DomainError("This approval is no longer pending.")
            ok, why = self.can_decide(user, approval)
            if not ok:
                self.audit.log(user.user_id, "approval.decide", f"approval:{approval_id}", outcome="DENIED")
                raise DomainError(why)

            self.db.execute("UPDATE approval SET approver_id=?, decision=?, reason=?, decided_at=?, status=?"
                            " WHERE approval_id=?", (user.user_id, decision, reason, now(), decision, approval_id))
            self.audit.log(user.user_id, "approval.decide", f"approval:{approval_id}",
                           old={"status": "Pending"}, new={"status": decision, "reason": reason})

            req = Request.get(self.db, approval.request_id)
            transfer = Transfer.where(self.db, "request_id=? AND status='Pending Approval'", (req.request_id,))[0]
            reservation = Reservation.where(self.db, "request_id=? AND status='Active'", (req.request_id,))
            asset = Asset.get(self.db, approval.asset_id)
            transfers = TransferService(self.db)

            if decision == "Approved":
                transfers.change_status(transfer, "Approved", user.user_id)
                if reservation:
                    self.db.execute("UPDATE reservation SET status='Converted' WHERE reservation_id=?",
                                    (reservation[0].reservation_id,))
                AssetService(self.db).change_status(asset, "In Transfer", user.user_id,
                                                    f"Transfer approved by {user.name}", f"transfer:{transfer.transfer_id}")
                RequestService(self.db).change_status(req, "Approved", user.user_id)
                self.notes.notify("request.approved", [req.requester_id, asset.custodian_id],
                                  f"R-{req.request_id:04d} approved: '{asset.name}' will be transferred. "
                                  "Confirm receipt when you get it.")
            else:
                transfers.change_status(transfer, "Rejected", user.user_id)
                if reservation:
                    ReservationService(self.db).release(reservation[0].reservation_id, user.user_id,
                                                        f"Request rejected: {reason}")
                RequestService(self.db).change_status(req, "Rejected", user.user_id)
                self.notes.notify("request.rejected", [req.requester_id],
                                  f"R-{req.request_id:04d} was rejected: {reason}")
        return Approval.get(self.db, approval_id)
