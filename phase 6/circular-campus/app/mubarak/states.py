"""C6 - Allowed states and moves (owner: Mubarak). Phase 3 section 6.2; design doc section 6.

Every status change in the system goes through `check_move`, so a move
that is not in these tables is refused on the server (core feature C6).
"""
from app.models import DomainError  # noqa: F401  (re-exported for other modules)


class StateMachine:
    def __init__(self, name: str, moves: dict):
        self.name = name
        self.moves = moves

    @property
    def states(self):
        return list(self.moves)

    def can_move(self, current: str, new: str) -> bool:
        return new in self.moves.get(current, ())

    def check_move(self, current: str, new: str):
        if not self.can_move(current, new):
            raise DomainError(f"{self.name} cannot move from '{current}' to '{new}'.")


AssetStatus = StateMachine("Asset", {
    "Draft":          ("Registered",),
    "Registered":     ("Available", "In Maintenance", "Donated", "Recycled", "Disposed", "Retired"),
    "Available":      ("Reserved", "Registered", "In Maintenance"),
    "Reserved":       ("Available", "In Transfer"),
    "In Transfer":    ("Registered", "Available"),
    "In Maintenance": ("Registered", "Retired"),
    "Retired":        ("Donated", "Recycled", "Disposed"),
    "Donated":        (),
    "Recycled":       (),
    "Disposed":       (),
})

RequestStatus = StateMachine("Request", {
    "Draft":             ("Submitted", "Cancelled"),
    "Submitted":         ("Matched / Reserved", "Cancelled", "Expired"),
    "Matched / Reserved": ("Approved", "Rejected", "Submitted", "Cancelled"),
    "Approved":          ("Fulfilled", "Cancelled"),
    "Rejected":          ("Submitted",),
    "Cancelled":         (),
    "Expired":           (),
    "Fulfilled":         (),
})

TransferStatus = StateMachine("Transfer", {
    "Pending Approval": ("Approved", "Rejected", "Cancelled"),
    "Approved":         ("Scheduled", "Cancelled"),
    "Scheduled":        ("In Transit", "Received", "Cancelled"),
    "In Transit":       ("Received",),
    "Received":         ("Completed",),
    "Rejected":         (),
    "Cancelled":        (),
    "Completed":        (),
})

MaintenanceStatus = StateMachine("Maintenance ticket", {
    "Reported":        ("Inspected",),
    "Inspected":       ("Repair Approved", "Not Repairable"),
    "Repair Approved": ("In Repair",),
    "In Repair":       ("Completed",),
    "Completed":       ("Verified",),
    "Verified":        (),
    "Not Repairable":  (),
})

ReservationStatus = StateMachine("Reservation", {
    "Active":    ("Expired", "Released", "Converted"),
    "Expired":   (),
    "Released":  (),
    "Converted": (),
})

CONDITIONS = ["New", "Good", "Fair", "Poor", "Broken"]
URGENCIES = ["Low", "Medium", "High"]
