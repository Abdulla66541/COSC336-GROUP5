"""Shared home page (shared setup)."""
from flask import Blueprint, g, render_template

from app.db import get_db
from app.mohammed_alketbi.security import login_required

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def home():
    db = get_db()
    stats = {
        "available": db.execute("SELECT COUNT(*) FROM asset WHERE status='Available'").fetchone()[0],
        "my_requests": db.execute("SELECT COUNT(*) FROM request WHERE requester_id=? AND status NOT IN"
                                  " ('Fulfilled','Cancelled','Expired','Rejected')", (g.user.user_id,)).fetchone()[0],
        "pending": db.execute("SELECT COUNT(*) FROM approval WHERE status='Pending'").fetchone()[0],
        "to_receive": db.execute("SELECT COUNT(*) FROM transfer t JOIN request r USING(request_id) WHERE"
                                 " r.requester_id=? AND t.status IN ('Approved','Scheduled','In Transit')",
                                 (g.user.user_id,)).fetchone()[0],
    }
    return render_template("home.html", stats=stats)
