"""Routes for Mohammed Alketbi: C1 login and roles, C8 notifications, C9 basic report, AI 4 assistant."""
from flask import (Blueprint, Response, abort, flash, g, redirect, render_template, request, session,
                   url_for)

from app.abdulla.ai_core import AIOutputLogger
from app.db import get_db
from app.mohammed_alketbi.assistant import AssistantService
from app.mohammed_alketbi.audit import AuditService
from app.mohammed_alketbi.notifications import NotificationService
from app.mohammed_alketbi.report_service import ReportService
from app.mohammed_alketbi.security import AuthService, require

bp = Blueprint("auth", __name__, template_folder="templates")
T = "mohammed_alketbi/"


# ---------------- C1 login ----------------
@bp.route("/login", methods=["GET", "POST"])
def login():
    db = get_db()
    if request.method == "POST":
        user, error = AuthService(db).login(request.form.get("email"), request.form.get("password"))
        AuditService(db).log(user.user_id if user else None, "login", request.form.get("email"),
                             outcome="OK" if user else "FAILED")
        if user:
            session.clear()
            session["user_id"] = user.user_id
            nxt = request.args.get("next")
            return redirect(nxt if nxt and nxt.startswith("/") and not nxt.startswith("//") else url_for("main.home"))
        flash(error, "danger")
    demo = db.execute("SELECT u.name, u.email, u.role, d.name AS dept FROM user u"
                      " JOIN department d USING(dept_id) ORDER BY u.user_id").fetchall()
    return render_template(T + "login.html", demo=demo)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# ---------------- C8 notifications ----------------
@bp.route("/notifications")
@require("notifications")
def notifications():
    svc = NotificationService(get_db())
    page = render_template(T + "notifications.html", items=svc.for_user(g.user.user_id))
    svc.mark_all_read(g.user.user_id)
    return page


# ---------------- C9 basic report ----------------
def _report_filters():
    start, end = request.args.get("start") or None, request.args.get("end") or None
    return start, end, None if g.user.role == "admin" else g.user.dept_id   # reps see their own department


@bp.route("/reports/")
@require("report.view")
def report():
    svc = ReportService(get_db())
    start, end, dept = _report_filters()
    if start and end and not svc.validate_date_range(start, end):
        flash("Start date must be before end date.", "danger")
        start = end = None
    return render_template(T + "report.html", rows=svc.requests_and_transfers(start, end, dept), start=start, end=end)


@bp.route("/reports/export.csv")
@require("report.view")
def export_csv():
    svc = ReportService(get_db())
    start, end, dept = _report_filters()
    return Response(svc.export_csv(svc.requests_and_transfers(start, end, dept)), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=requests_transfers.csv"})


@bp.route("/reports/audit")
@require("audit.view")
def audit():
    return render_template(T + "audit.html", rows=AuditService(get_db()).recent())


# ---------------- AI 4 assistant (UC-29) ----------------
@bp.route("/assistant", methods=["GET", "POST"])
@require("ai.assistant")
def assistant():
    chat = session.get("chat", [])
    if request.method == "POST":
        result = AssistantService(get_db()).ask(request.form.get("question"), g.user)
        if result:
            chat.append({"q": request.form.get("question", "").strip()[:500], "a": result.content["answer"],
                         "ids": result.content.get("asset_ids", []), "id": result.output_id,
                         "model": result.model_id})
            session["chat"] = chat[-8:]
        return redirect(url_for("auth.assistant"))
    return render_template(T + "assistant.html", chat=chat)


@bp.route("/assistant/feedback/<int:output_id>", methods=["POST"])
@require("ai.assistant")
def assistant_feedback(output_id):
    rating = request.form.get("rating", type=int)
    if rating not in (1, 5):
        abort(400)
    AIOutputLogger(get_db()).feedback(output_id, g.user.user_id, rating)
    flash("Thanks for the feedback.", "success")
    return redirect(url_for("auth.assistant"))


@bp.route("/assistant/clear", methods=["POST"])
@require("ai.assistant")
def assistant_clear():
    session.pop("chat", None)
    return redirect(url_for("auth.assistant"))
