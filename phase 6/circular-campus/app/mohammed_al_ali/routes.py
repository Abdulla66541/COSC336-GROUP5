"""Routes for Mohammed Al Ali: C2 assets, C3 publish and search, C4 requests, AI 1 classification."""
from flask import Blueprint, abort, flash, g, jsonify, redirect, render_template, request, url_for

from app.abdulla.ai_core import AIOutputLogger
from app.db import get_db
from app.models import Department
from app.mohammed_al_ali.asset_service import AssetService, SearchService
from app.mohammed_al_ali.classification import ClassificationService
from app.mohammed_al_ali.request_service import RequestService, ReservationService
from app.mohammed_alketbi.security import SecurityService, login_required, require
from app.mubarak.history_service import HistoryService
from app.mubarak.states import CONDITIONS, URGENCIES, DomainError

assets = Blueprint("assets", __name__, template_folder="templates")
requests_bp = Blueprint("requests", __name__, url_prefix="/requests", template_folder="templates")
T = "mohammed_al_ali/"


# ---------------- C3 search ----------------
@assets.route("/search")
@require("search")
def search():
    db = get_db()
    f = request.args
    results = SearchService(db).search(f.get("q", ""), f.get("category_id"), f.get("condition"),
                                       f.get("dept_id"), f.get("sort", "newest"))
    return render_template(T + "search.html", results=results, categories=AssetService(db).categories(),
                           departments=Department.where(db, order="name"), conditions=CONDITIONS, f=f)


# ---------------- C2 assets ----------------
@assets.route("/assets")
@login_required
def my_assets():
    dept = None if g.user.role == "admin" else g.user.dept_id    # BR-16: unpublished assets only for owners
    return render_template(T + "assets.html", assets=AssetService(get_db()).for_department(dept))


@assets.route("/assets/new", methods=["GET", "POST"])
@require("asset.create")
def new_asset():
    db = get_db()
    svc = AssetService(db)
    form = request.form
    if request.method == "POST":
        try:
            asset = svc.register_asset(form.to_dict(), g.user)
            ai_id = form.get("ai_output_id", type=int)
            chosen = f"{form.get('category_id')}|{form.get('condition')}"
            if ai_id and form.get("ai_suggested") and form.get("ai_suggested") != chosen:   # BR-12
                AIOutputLogger(db).override(ai_id, g.user.user_id, chosen, "Edited by custodian")
            flash(f"Asset {asset.tag_number} registered.", "success")
            return redirect(url_for("assets.detail", asset_id=asset.asset_id))
        except DomainError as e:
            flash(str(e), "danger")
    return render_template(T + "asset_form.html", categories=svc.categories(), conditions=CONDITIONS,
                           departments=Department.where(db, order="name"), form=form)


@assets.route("/assets/<int:asset_id>")
@login_required
def detail(asset_id):
    db = get_db()
    asset = AssetService(db).detail(asset_id)
    if not asset:
        abort(404)
    owner = g.user.role == "admin" or g.user.dept_id == asset["owner_dept_id"]
    involved = db.execute("SELECT 1 FROM transfer t JOIN request r USING(request_id) WHERE t.asset_id=? AND"
                          " (r.requester_id=? OR t.from_dept_id=? OR t.to_dept_id=?)",
                          (asset_id, g.user.user_id, g.user.dept_id, g.user.dept_id)).fetchone()
    if asset["status"] != "Available" and not owner and not involved:
        abort(403)            # BR-16
    my_open = db.execute("SELECT * FROM request WHERE requester_id=? AND status='Submitted'"
                         " ORDER BY request_id DESC", (g.user.user_id,)).fetchall()
    manage = SecurityService(db).can_manage_asset(g.user, _Row(asset))
    return render_template(T + "asset_detail.html", a=asset, history=HistoryService(db).get_history(asset_id),
                           my_open=my_open, manage=manage, conditions=CONDITIONS)


@assets.route("/assets/<int:asset_id>/edit", methods=["POST"])
@require("asset.update")
def edit(asset_id):
    db = get_db()
    try:
        AssetService(db).update_asset(asset_id, request.form.to_dict(), g.user, SecurityService(db))
        flash("Asset updated.", "success")
    except DomainError as e:
        flash(str(e), "danger")
    return redirect(url_for("assets.detail", asset_id=asset_id))


@assets.route("/assets/<int:asset_id>/publish", methods=["POST"])
@require("asset.publish")
def publish(asset_id):
    db = get_db()
    try:
        AssetService(db).publish(asset_id, g.user, SecurityService(db))
        flash("Published to the marketplace for 30 days.", "success")
    except DomainError as e:
        flash(str(e), "danger")
    return redirect(url_for("assets.detail", asset_id=asset_id))


@assets.route("/assets/<int:asset_id>/withdraw", methods=["POST"])
@require("asset.publish")
def withdraw(asset_id):
    db = get_db()
    try:
        AssetService(db).withdraw(asset_id, g.user, SecurityService(db))
        flash("Listing withdrawn.", "success")
    except DomainError as e:
        flash(str(e), "danger")
    return redirect(url_for("assets.detail", asset_id=asset_id))


# ---------------- AI 1 classification ----------------
@assets.route("/ai/classify", methods=["POST"])
@require("ai.classify")
def classify():
    """Called by the asset form. Returns a suggestion; the custodian decides."""
    data = request.get_json(silent=True) or request.form
    r = ClassificationService(get_db()).classify(data.get("name", ""), data.get("description", ""))
    return jsonify({"ai_output_id": r.output_id, "category_id": r.content["category_id"],
                    "category_label": r.content.get("category_label"), "condition": r.content["condition"],
                    "tags": r.content["tags"], "confidence": r.confidence, "explanation": r.explanation,
                    "model": r.model_id, "low_confidence": r.confidence < 0.5})


# ---------------- C4 requests ----------------
@requests_bp.route("/")
@require("request.view_own")
def mine():
    return render_template(T + "requests.html", items=RequestService(get_db()).mine(g.user.user_id))


@requests_bp.route("/new", methods=["GET", "POST"])
@require("request.create")
def new():
    db = get_db()
    if request.method == "POST":
        try:
            req = RequestService(db).submit_request(request.form.to_dict(), g.user)
            flash(f"Request R-{req.request_id:04d} submitted. Here are the best matches.", "success")
            return redirect(url_for("ai.matches", request_id=req.request_id))      # AI 2 (Abdulla)
        except DomainError as e:
            flash(str(e), "danger")
    cats = AssetService(db).categories()
    names = sorted({c.name for c in cats} | {c.subcategory for c in cats if c.subcategory})
    return render_template(T + "request_form.html", form=request.form, urgencies=URGENCIES,
                           conditions=["Any"] + CONDITIONS, categories=names)


@requests_bp.route("/reserve-asset/<int:asset_id>", methods=["POST"])
@require("request.create")
def reserve_from_asset(asset_id):
    """Reserve from the asset page for one of my open requests."""
    request_id = request.form.get("request_id", type=int)
    if not request_id:
        flash("Choose one of your requests.", "danger")
        return redirect(url_for("assets.detail", asset_id=asset_id))
    try:
        asset = ReservationService(get_db()).reserve(asset_id, request_id, g.user)
        flash(f"'{asset.name}' reserved for 7 days. The owning department has been asked to approve.", "success")
        return redirect(url_for("requests.mine"))
    except DomainError as e:
        flash(str(e), "danger")
        return redirect(url_for("assets.detail", asset_id=asset_id))


@requests_bp.route("/<int:request_id>/cancel", methods=["POST"])
@require("request.create")
def cancel(request_id):
    try:
        RequestService(get_db()).cancel_request(request_id, g.user)
        flash("Request cancelled.", "success")
    except DomainError as e:
        flash(str(e), "danger")
    return redirect(url_for("requests.mine"))


class _Row:
    def __init__(self, row):
        self.__dict__.update(dict(row))
