"""C8 In-app notifications (owner: Mohammed Alketbi)."""
from app.db import now
from app.models import Notification


class NotificationService:
    def __init__(self, db):
        self.db = db

    def notify(self, event_type, user_ids, message):
        for uid in {u for u in user_ids if u}:
            self.db.execute(
                "INSERT INTO notification (user_id, event_type, message, created_at) VALUES (?,?,?,?)",
                (uid, event_type, message, now()))

    def approvers_for_dept(self, dept_id):
        """Department representatives of a department, plus all admins."""
        rows = self.db.execute(
            "SELECT user_id FROM user WHERE status='Active' AND"
            " ((role='dept_rep' AND dept_id=?) OR role='admin')", (dept_id,)).fetchall()
        return [r["user_id"] for r in rows]

    def for_user(self, user_id):
        return Notification.where(self.db, "user_id = ?", (user_id,))

    def unread_count(self, user_id):
        return self.db.execute(
            "SELECT COUNT(*) FROM notification WHERE user_id=? AND status='Unread'", (user_id,)).fetchone()[0]

    def mark_all_read(self, user_id):
        self.db.execute("UPDATE notification SET status='Read' WHERE user_id=?", (user_id,))
