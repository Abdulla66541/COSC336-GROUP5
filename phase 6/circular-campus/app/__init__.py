"""Circular Campus - Flask application factory (shared setup).

Each member's code lives in their own folder and is plugged in here:
    mohammed_alketbi/  C1 login and roles, C8 notifications, C9 report, AI 4 assistant
    mohammed_al_ali/   C2 assets, C3 publish and search, C4 requests, AI 1 classification
    mubarak/           C5 approve and transfer, C6 states and history, AI 3 advice
    abdulla/           C7 sustainability dashboard, AI 2 matching, AI 5 generated report
"""
import os

from flask import Flask, g, render_template

from app import db as database
from app.mohammed_alketbi.security import ROLES, can, load_user


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        DATABASE=os.path.join(app.instance_path, "circular_campus.sqlite"),
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)
    if not os.path.exists(app.config["DATABASE"]):   # first run: create tables and demo data
        from app.seed import seed
        conn = database.connect(app.config["DATABASE"])
        database.init_schema(conn)
        seed(conn)
        conn.close()

    app.teardown_appcontext(database.close_db)
    app.before_request(load_user)

    @app.before_request
    def housekeeping():
        """Expire old listings, reservations and requests (BR-04, BR-19)."""
        from app.mohammed_al_ali.asset_service import AssetService
        from app.mohammed_al_ali.request_service import RequestService, ReservationService
        db = database.get_db()
        ReservationService(db).expire_old_reservations()
        AssetService(db).expire_old_listings()
        RequestService(db).expire_old_requests()

    @app.context_processor
    def inject():
        from app.mohammed_alketbi.notifications import NotificationService
        unread = NotificationService(database.get_db()).unread_count(g.user.user_id) if g.get("user") else 0
        return {"can": can, "unread": unread, "ROLES": ROLES}

    from app import home
    from app.abdulla import routes as abdulla
    from app.mohammed_al_ali import routes as mohammed_al_ali
    from app.mohammed_alketbi import routes as mohammed_alketbi
    from app.mubarak import routes as mubarak
    for bp in (home.bp, mohammed_alketbi.bp, mohammed_al_ali.assets, mohammed_al_ali.requests_bp,
               mubarak.bp, abdulla.bp):
        app.register_blueprint(bp)

    @app.errorhandler(403)
    def forbidden(_e):
        return render_template("error.html", code=403,
                               message="Your role does not have permission for this action."), 403

    @app.errorhandler(400)
    def bad_request(_e):
        return render_template("error.html", code=400, message="That request was not valid."), 400

    @app.errorhandler(500)
    def server_error(_e):
        return render_template("error.html", code=500,
                               message="Something went wrong. The action was not saved."), 500

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("error.html", code=404, message="Page not found."), 404

    @app.cli.command("init-db")
    def init_db_command():
        """Create the tables and load the demo data."""
        from app.seed import seed
        conn = database.connect(app.config["DATABASE"])
        database.init_schema(conn)
        seed(conn)
        conn.close()
        print("Database created with demo data.")

    return app
