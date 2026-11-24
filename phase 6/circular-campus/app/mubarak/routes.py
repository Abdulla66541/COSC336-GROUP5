"""Routes for Mubarak: C5 approve and transfer, C6 states and history (with maintenance
and end of life), AI 3 sustainable-action advice."""
from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from app.abdulla.ai_core import AIOutputLogger
from app.db import get_db
from app.models import Asset
from app.mohammed_alketbi.security import SecurityService, require
from app.mubarak.advice import RecommendationService
from app.mubarak.approval_service import ApprovalService
from app.mubarak.maintenance_service import EndOfLifeService, MaintenanceService
from app.mubarak.states import CONDITIONS, DomainError
from app.mubarak.transfer_service import TransferService

bp = Blueprint("workflow", __name__, template_folder="templates")
T = "mubarak/"


# ---------------- C5 approvals (UC-11) ----------------
@bp.route("/approvals")
@require("approval.decide")
def approvals():
    db = get_db()
    return render_template(T + "approvals.html", items=ApprovalService(db).get_pending(g.user),
                           eol=EndOfLifeService(db).pending() if g.user.role == "admin" else [],
                           overdue=TransferService(db).overdue())


@bp.route("/approvals/<int:approval_id>", methods=["POST"])
@require("approval.decide")
def decide(approval_id):
    try:
        a = ApprovalService(get_db()).decide(approval_id, request.form.get("decision"), request.form.get("reason"), g.user)
        flash(f"Request {a.status.lower()}.", "success")
    except DomainError as e:
        flash(str(e), "danger")
    return redirect(url_for("workflow.approvals"))


# ---------------- C5 transfers (UC-12) ----------------
@bp.route("/transfers")
@require("transfer.confirm")
def transfers():
    rows = get_db().execute(
        "SELECT t.*, a.name AS asset_name, a.tag_number, fd.name AS from_dept, td.name AS to_dept,"
        " r.requester_id, a.custodian_id FROM transfer t JOIN asset a ON a.asset_id=t.asset_id"
        " JOIN department fd ON fd.dept_id=t.from_dept_id JOIN department td ON td.dept_id=t.to_dept_id"
        " JOIN request r ON r.request_id=t.request_id"
        " WHERE (? = 'admin' OR r.requester_id=? OR t.from_dept_id=? OR t.to_dept_id=?) ORDER BY t.transfer_id DESC",
        (g.user.role, g.user.user_id, g.user.dept_id, g.user.dept_id)).fetchall()
    return render_template(T + "transfers.html", items=rows)


@bp.route("/transfers/<int:transfer_id>/schedule", methods=["POST"])
@require("transfer.confirm")
def schedule(transfer_id):
    try:
        TransferService(get_db()).schedule(transfer_id, request.form.get("handover_date"),
                                           request.form.get("handover_location"), g.user)
        flash("Handover scheduled.", "success")
    except DomainError as e:
        flash(str(e), "danger")
    return redirect(url_for("workflow.transfers"))


@bp.route("/transfers/<int:transfer_id>/receive", methods=["POST"])
@require("transfer.confirm")
def receive(transfer_id):
    try:
        TransferService(get_db()).confirm_receipt(transfer_id, g.user, request.form.get("discrepancy_note"))
        flash("Receipt confirmed. The asset now belongs to your department.", "success")
    except DomainError as e:
        flash(str(e), "danger")
    return redirect(url_for("workflow.transfers"))


# ---------------- C6 maintenance (UC-13, UC-24, UC-14) ----------------
@bp.route("/maintenance")
@require("maintenance.manage")
def maintenance():
    return render_template(T + "maintenance.html", items=MaintenanceService(get_db()).open_tickets(),
                           conditions=CONDITIONS)


@bp.route("/assets/<int:asset_id>/defect", methods=["POST"])
@require("maintenance.report")
def report_defect(asset_id):
    try:
        MaintenanceService(get_db()).report_defect(asset_id, request.form.get("description"), g.user)
        flash("Defect reported. The asset is now In Maintenance.", "success")
    except DomainError as e:
        flash(str(e), "danger")
    return redirect(url_for("assets.detail", asset_id=asset_id))


@bp.route("/maintenance/<int:ticket_id>/<action>", methods=["POST"])
@require("maintenance.manage")
def maintenance_action(ticket_id, action):
    svc = MaintenanceService(get_db())
    try:
        if action == "inspect":
            svc.inspect(ticket_id, request.form.get("repairable") == "yes", g.user)
        elif action == "repair":
            svc.record_repair(ticket_id, request.form.get("action"), request.form.get("cost_aed"), g.user)
        elif action == "verify":
            svc.verify(ticket_id, request.form.get("condition"), g.user)
        else:
            abort(404)
        flash("Maintenance ticket updated.", "success")
    except DomainError as e:
        flash(str(e), "danger")
    return redirect(url_for("workflow.maintenance"))


# ---------------- C6 end of life (UC-16, UC-25) ----------------
@bp.route("/assets/<int:asset_id>/end-of-life", methods=["POST"])
@require("eol.create")
def end_of_life(asset_id):
    db = get_db()
    f = request.form
    try:
        EndOfLifeService(db).create_request(asset_id, f.get("action"), f.get("reason"), f.get("assessment"),
                                            f.get("recipient"), g.user, SecurityService(db))
        flash("Sent to the administrator for approval.", "success")
    except DomainError as e:
        flash(str(e), "danger")
    return redirect(url_for("assets.detail", asset_id=asset_id))


@bp.route("/end-of-life/<int:eol_id>", methods=["POST"])
@require("eol.decide")
def eol_decide(eol_id):
    try:
        EndOfLifeService(get_db()).admin_decision(eol_id, request.form.get("decision"), request.form.get("reason"), g.user)
        flash("Decision saved.", "success")
    except DomainError as e:
        flash(str(e), "danger")
    return redirect(url_for("workflow.approvals"))


# ---------------- AI 3 sustainable-action advice (UC-28) ----------------
@bp.route("/assets/<int:asset_id>/advice", methods=["GET", "POST"])
@require("ai.advice")
def advice(asset_id):
    db = get_db()
    asset = Asset.get(db, asset_id)
    if not asset or not SecurityService(db).can_manage_asset(g.user, asset):
        abort(403)
    if request.method == "POST":           # the custodian disagrees: log it (BR-12)
        out_id = request.form.get("ai_output_id", type=int)
        if not out_id or not db.execute("SELECT 1 FROM ai_output WHERE ai_output_id=?", (out_id,)).fetchone():
            abort(400)
        AIOutputLogger(db).override(out_id, g.user.user_id, request.form.get("final_action"), request.form.get("reason"))
        return render_template(T + "advice.html", a=asset, r=None, saved=True)
    result = RecommendationService(db).recommend(asset_id, request.args.get("repair_cost", type=float))
    return render_template(T + "advice.html", a=asset, r=result, saved=False)
