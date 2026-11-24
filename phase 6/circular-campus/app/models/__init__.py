"""Shared model classes (shared setup). Each one wraps a database row (see the ER diagram) and
holds the small rules that belong to that object."""
from datetime import datetime


class DomainError(Exception):
    """A business rule was broken. The message is shown to the user."""


class Model:
    table = ""
    key = ""

    def __init__(self, row):
        self._row = dict(row)
        for k, v in self._row.items():
            setattr(self, k, v)

    @property
    def id(self):
        return self._row[self.key]

    def as_dict(self):
        return dict(self._row)

    @classmethod
    def get(cls, db, pk):
        row = db.execute(f"SELECT * FROM {cls.table} WHERE {cls.key} = ?", (pk,)).fetchone()
        return cls(row) if row else None

    @classmethod
    def where(cls, db, sql="1=1", params=(), order=None):
        order_by = f" ORDER BY {order}" if order else f" ORDER BY {cls.key} DESC"
        rows = db.execute(f"SELECT * FROM {cls.table} WHERE {sql}{order_by}", params).fetchall()
        return [cls(r) for r in rows]


# ---------- Part 3 ----------
class Department(Model):
    table, key = "department", "dept_id"


class User(Model):
    table, key = "user", "user_id"

    def is_active(self):
        return self.status == "Active"


class Notification(Model):
    table, key = "notification", "notification_id"


class AuditLogEntry(Model):
    table, key = "audit_log", "audit_id"


# ---------- Part 1 ----------
class Category(Model):
    table, key = "category", "category_id"

    @property
    def label(self):
        return f"{self.name} / {self.subcategory}" if self.subcategory else self.name


class Asset(Model):
    table, key = "asset", "asset_id"

    def is_available(self):
        return self.status == "Available" and bool(self.active)

    def age_years(self):
        if not self.purchase_date:
            return None
        d = datetime.fromisoformat(self.purchase_date)
        return round((datetime.now() - d).days / 365, 1)


class Listing(Model):
    table, key = "listing", "listing_id"


class Request(Model):
    table, key = "request", "request_id"

    def can_edit(self):
        return self.status in ("Draft", "Submitted")


class Reservation(Model):
    table, key = "reservation", "reservation_id"

    def is_expired(self):
        return self.status == "Active" and self.expires_at < datetime.now().isoformat()


# ---------- Part 2 ----------
class Approval(Model):
    table, key = "approval", "approval_id"


class Transfer(Model):
    table, key = "transfer", "transfer_id"


class MaintenanceTicket(Model):
    table, key = "maintenance_ticket", "ticket_id"


class RepairRecord(Model):
    table, key = "repair_record", "repair_id"


class EndOfLifeRequest(Model):
    table, key = "end_of_life_request", "eol_id"

    def has_assessment(self):
        return len((self.alternatives_assessment or "").strip()) >= 10


class AssetHistoryEvent(Model):
    table, key = "asset_history", "event_id"


# ---------- Part 4 ----------
class AIOutput(Model):
    table, key = "ai_output", "ai_output_id"


class ReuseEvent(Model):
    table, key = "reuse_event", "reuse_id"


class EmissionFactor(Model):
    table, key = "emission_factor", "factor_id"
