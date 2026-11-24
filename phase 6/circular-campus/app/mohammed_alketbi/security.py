"""C1 - Login, roles and server-side permission checks (owner: Mohammed Alketbi).

Every protected route uses @require(permission). Hiding a button in the
page is never the only check: the server refuses the action too.
"""
from functools import wraps

from flask import abort, g, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db
from app.models import User

ROLES = {
    "requester": "Requester",
    "custodian": "Asset Custodian",
    "dept_rep": "Department Representative (approver)",
    "admin": "Administrator",
}

# Permission matrix (Phase 3, section 2.4). Seeded into ROLE_PERMISSION.
PERMISSIONS = {
    "requester": ["search", "request.create", "request.view_own", "transfer.confirm",
                  "ai.assistant", "notifications"],
    "custodian": ["search", "asset.create", "asset.update", "asset.publish", "maintenance.report",
                  "request.create", "request.view_own", "transfer.confirm", "ai.classify",
                  "ai.advice", "eol.create", "notifications", "history.view", "ai.assistant"],
    "dept_rep":  ["search", "asset.create", "asset.update", "asset.publish", "maintenance.report",
                  "request.create", "request.view_own", "transfer.confirm", "approval.decide",
                  "ai.classify", "ai.advice", "eol.create", "history.view", "dashboard.view",
                  "report.view", "notifications", "finance.view", "ai.assistant", "ai.report"],
    "admin":     ["search", "asset.create", "asset.update", "asset.publish", "maintenance.report",
                  "maintenance.manage", "request.create", "request.view_own", "transfer.confirm",
                  "approval.decide", "eol.decide", "eol.create", "ai.classify", "ai.advice",
                  "history.view", "dashboard.view", "report.view", "report.publish", "audit.view",
                  "user.manage", "notifications", "finance.view", "ai.assistant", "ai.report"],
}


class AuthService:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def hash_password(pw):
        return generate_password_hash(pw)

    def login(self, email, password):
        row = self.db.execute("SELECT * FROM user WHERE email = ?", ((email or "").strip().lower(),)).fetchone()
        if not row or not check_password_hash(row["password_hash"], password or ""):
            return None, "Wrong email or password."
        user = User(row)
        if not user.is_active():
            return None, "This account is deactivated (BR-18)."
        return user, None


class SecurityService:
    def __init__(self, db):
        self.db = db

    def check_permission(self, user, function_name):
        if user is None:
            return False
        row = self.db.execute(
            "SELECT allowed FROM role_permission WHERE role=? AND function_name=?",
            (user.role, function_name)).fetchone()
        return bool(row and row["allowed"])

    @staticmethod
    def is_own_department(user, dept_id):
        return user.role == "admin" or user.dept_id == dept_id

    def can_manage_asset(self, user, asset):
        """BR-02: custodian or dept rep of the owning department, or admin."""
        if user.role == "admin":
            return True
        return user.dept_id == asset.owner_dept_id and user.role in ("custodian", "dept_rep")


def load_user():
    uid = session.get("user_id")
    g.user = None
    if uid:
        user = User.get(get_db(), uid)
        if user and user.is_active():
            g.user = user
        else:
            session.clear()


def login_required(view):
    @wraps(view)
    def wrapped(*a, **kw):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))
        return view(*a, **kw)
    return wrapped


def require(permission):
    def deco(view):
        @wraps(view)
        def wrapped(*a, **kw):
            if g.user is None:
                return redirect(url_for("auth.login", next=request.path))
            if not SecurityService(get_db()).check_permission(g.user, permission):
                abort(403)
            return view(*a, **kw)
        return wrapped
    return deco


def can(permission):
    """Used in templates to decide which buttons to show (the server still checks)."""
    return SecurityService(get_db()).check_permission(g.get("user"), permission)
