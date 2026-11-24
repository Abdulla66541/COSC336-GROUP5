"""C1 support - audit log writer (owner: Mohammed Alketbi). BR-14. Rows are append-only; the database triggers
refuse any UPDATE or DELETE (BR-13)."""
import json

from app.db import now


class AuditService:
    def __init__(self, db):
        self.db = db

    def log(self, actor_id, action, record_ref, outcome="OK", old=None, new=None):
        self.db.execute(
            "INSERT INTO audit_log (actor_id, action, record_ref, outcome, old_value, new_value, event_time)"
            " VALUES (?,?,?,?,?,?,?)",
            (actor_id, action, record_ref, outcome,
             json.dumps(old, default=str) if old is not None else None,
             json.dumps(new, default=str) if new is not None else None,
             now()),
        )

    def recent(self, limit=200):
        return self.db.execute(
            "SELECT a.*, u.name AS actor_name FROM audit_log a LEFT JOIN user u ON u.user_id = a.actor_id"
            " ORDER BY audit_id DESC LIMIT ?", (limit,)).fetchall()
