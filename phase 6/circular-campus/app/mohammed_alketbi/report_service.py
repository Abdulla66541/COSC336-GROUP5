"""C9 Basic report with CSV export (owner: Mohammed Alketbi)."""
import csv
import io
from datetime import date


class ReportService:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def validate_date_range(start, end):
        try:
            return date.fromisoformat(start) <= date.fromisoformat(end)
        except (TypeError, ValueError):
            return False

    def requests_and_transfers(self, start=None, end=None, dept_id=None):
        sql = ("SELECT r.request_id, r.created_at, u.name AS requester, d.name AS requesting_dept, r.category,"
               " r.quantity, r.urgency, r.status AS request_status, a.tag_number, a.name AS asset_name,"
               " fd.name AS from_dept, t.transfer_id, t.status AS transfer_status, t.received_at"
               " FROM request r JOIN user u ON u.user_id=r.requester_id JOIN department d ON d.dept_id=r.dept_id"
               " LEFT JOIN transfer t ON t.transfer_id=(SELECT MAX(transfer_id) FROM transfer WHERE request_id=r.request_id)"
               " LEFT JOIN asset a ON a.asset_id=t.asset_id LEFT JOIN department fd ON fd.dept_id=t.from_dept_id"
               " WHERE 1=1")
        params = []
        if start:
            sql += " AND date(r.created_at) >= ?"
            params.append(start)
        if end:
            sql += " AND date(r.created_at) <= ?"
            params.append(end)
        if dept_id:
            sql += " AND (r.dept_id = ? OR t.from_dept_id = ?)"
            params += [dept_id, dept_id]
        return self.db.execute(sql + " ORDER BY r.request_id DESC", params).fetchall()

    COLUMNS = ["request_id", "created_at", "requester", "requesting_dept", "category", "quantity", "urgency",
               "request_status", "tag_number", "asset_name", "from_dept", "transfer_id", "transfer_status", "received_at"]

    def export_csv(self, rows):
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(self.COLUMNS)
        for r in rows:
            w.writerow([r[c] for c in self.COLUMNS])
        return buf.getvalue()
