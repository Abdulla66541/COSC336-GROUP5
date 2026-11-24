"""Routes for Abdulla: C7 sustainability dashboard, AI 2 matching and ranking, AI 5 generated report."""
from datetime import date

from flask import Blueprint, Response, abort, flash, g, redirect, render_template, request, url_for

from app.abdulla.ai_core import AIOutputLogger
from app.abdulla.ai_report import AIReportService
from app.abdulla.matching import MatchingService
from app.abdulla.sustainability_service import SustainabilityService
from app.db import get_db
from app.models import Request
from app.mohammed_al_ali.request_service import ReservationService
from app.mohammed_alketbi.security import require
from app.mubarak.states import DomainError

bp = Blueprint("ai", __name__, template_folder="templates")
T = "abdulla/"


# ---------------- AI 2 matching and ranking (UC-27) ----------------
@bp.route("/requests/<int:request_id>/matches")
@require("request.create")
def matches(request_id):
    db = get_db()
    req = Request.get(db, request_id)
    if not req or req.requester_id != g.user.user_id:
        abort(403)
    result = MatchingService(db).find_matches(request_id) if req.status == "Submitted" else None
    return render_template(T + "matches.html", req=req, result=result)


@bp.route("/requests/<int:request_id>/reserve/<int:asset_id>", methods=["POST"])
@require("request.create")
def reserve(request_id, asset_id):
    db = get_db()
    try:
        asset = ReservationService(db).reserve(asset_id, request_id, g.user)
        rank = request.form.get("ai_rank")
        if request.form.get("ai_output_id", type=int) and rank not in (None, "1"):     # BR-12
            AIOutputLogger(db).override(request.form.get("ai_output_id", type=int), g.user.user_id,
                                        f"asset:{asset_id}", f"Requester chose rank {rank}")
        flash(f"'{asset.name}' reserved for 7 days. The owning department has been asked to approve.", "success")
    except DomainError as e:
        flash(str(e), "danger")
        return redirect(url_for("ai.matches", request_id=request_id))
    return redirect(url_for("requests.mine"))


@bp.route("/requests/<int:request_id>/reject-matches", methods=["POST"])
@require("request.create")
def reject_matches(request_id):
    out_id = request.form.get("ai_output_id", type=int)
    if out_id:
        AIOutputLogger(get_db()).override(out_id, g.user.user_id, "rejected all",
                                          request.form.get("reason") or "None suitable")
    flash("Noted. Your request stays open; you can search the marketplace yourself.", "success")
    return redirect(url_for("assets.search"))


# ---------------- C7 sustainability dashboard (UC-31) ----------------
@bp.route("/dashboard")
@require("dashboard.view")
def dashboard():
    svc = SustainabilityService(get_db())
    start, end = request.args.get("start") or None, request.args.get("end") or None
    return render_template(T + "dashboard.html", metrics=svc.metrics(start, end), factors=svc.factors(),
                           start=start, end=end)


# ---------------- AI 5 generated report (UC-30) ----------------
@bp.route("/ai-reports", methods=["GET", "POST"])
@require("ai.report")
def ai_reports():
    svc = AIReportService(get_db())
    if request.method == "POST":
        try:
            rid = svc.generate(request.form.get("start"), request.form.get("end"), g.user)
            return redirect(url_for("ai.ai_report", report_id=rid))
        except DomainError as e:
            flash(str(e), "danger")
    today = date.today()
    return render_template(T + "ai_reports.html", reports=svc.list(),
                           default_start=today.replace(day=1).isoformat(), default_end=today.isoformat())


@bp.route("/ai-reports/<int:report_id>", methods=["GET", "POST"])
@require("ai.report")
def ai_report(report_id):
    svc = AIReportService(get_db())
    if request.method == "POST":
        try:
            svc.mark_reviewed(report_id, request.form.get("text"), g.user)
            flash("Report marked as reviewed. It can now be exported.", "success")
        except DomainError as e:
            flash(str(e), "danger")
        return redirect(url_for("ai.ai_report", report_id=report_id))
    rep = svc.get(report_id)
    if not rep:
        abort(404)
    return render_template(T + "ai_report.html", r=rep)


@bp.route("/ai-reports/<int:report_id>/export")
@require("ai.report")
def ai_report_export(report_id):
    try:
        text = AIReportService(get_db()).export_text(report_id)
    except DomainError as e:
        flash(str(e), "danger")
        return redirect(url_for("ai.ai_report", report_id=report_id))
    return Response(text, mimetype="text/plain",
                    headers={"Content-Disposition": f"attachment; filename=ai_report_{report_id}.txt"})
