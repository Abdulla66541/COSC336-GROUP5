"""C6 Asset history (owner: Mubarak). FR-HST. Append-only."""
from app.db import now
from app.models import AssetHistoryEvent


class HistoryService:
    def __init__(self, db):
        self.db = db

    def record(self, asset_id, event_type, actor_id, related_record=None, details=None):
        self.db.execute(
            "INSERT INTO asset_history (asset_id, event_type, actor_id, event_time, related_record, details)"
            " VALUES (?,?,?,?,?,?)",
            (asset_id, event_type, actor_id, now(), related_record, details))

    def get_history(self, asset_id):
        rows = self.db.execute(
            "SELECT h.*, u.name AS actor_name, u.role AS actor_role FROM asset_history h"
            " LEFT JOIN user u ON u.user_id = h.actor_id WHERE h.asset_id = ? ORDER BY h.event_id",
            (asset_id,)).fetchall()
        return [AssetHistoryEvent(r) for r in rows]
