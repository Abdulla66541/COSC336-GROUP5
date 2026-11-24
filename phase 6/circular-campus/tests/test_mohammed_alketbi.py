"""Tests for Mohammed Alketbi: C1 login and roles, C8 notifications, C9 report, AI 4 assistant."""
from conftest import request_data


def test_wrong_password_and_deactivated_user(app, db):
    c = app.test_client()
    assert c.post("/login", data={"email": "hessa@campus.test", "password": "nope"}).status_code == 200
    db.execute("UPDATE user SET status='Deactivated' WHERE email='ali@campus.test'")
    r = c.post("/login", data={"email": "ali@campus.test", "password": "Password123!"})
    assert r.status_code == 200 and b"deactivated" in r.data


def test_pages_need_login(app):
    r = app.test_client().get("/requests/")
    assert r.status_code == 302 and "/login" in r.location


def test_server_refuses_actions_outside_role(login):
    c = login("hessa@campus.test")                    # requester
    assert c.get("/approvals").status_code == 403
    assert c.post("/approvals/1", data={"decision": "Approved"}).status_code == 403   # direct POST, no button
    assert c.post("/assets/1/publish").status_code == 403
    assert c.get("/reports/audit").status_code == 403


def test_three_roles_see_different_menus(login):
    assert b"Approvals" not in login("hessa@campus.test").get("/").data
    assert b"Approvals" in login("sara.rep@campus.test").get("/").data
    assert b"Audit log" in login("admin@campus.test").get("/").data


def test_csv_export(login):
    c = login("hessa@campus.test")
    c.post("/requests/new", data=request_data())
    admin = login("admin@campus.test")
    r = admin.get("/reports/export.csv")
    assert r.status_code == 200 and r.mimetype == "text/csv"
    lines = r.data.decode().strip().splitlines()
    assert lines[0].startswith("request_id,") and len(lines) == 2


def test_notification_on_request(login):
    c = login("hessa@campus.test")
    c.post("/requests/new", data=request_data())
    assert b"was submitted" in c.get("/notifications").data


def test_no_open_redirect_after_login(app):
    r = app.test_client().post("/login?next=//evil.com", data={"email": "hessa@campus.test", "password": "Password123!"})
    assert r.location == "/"


def test_bad_input_never_crashes(login):
    k = login("khalid@campus.test")
    assert k.post("/assets/new", data={"name": "x", "category_id": "999", "quantity": "1",
                                       "condition": "Good"}).status_code == 200      # form shown again with error
    assert k.post("/assets/3/advice", data={}).status_code == 400
    a = login("admin@campus.test")
    assert a.post("/transfers/999/schedule", data={}).status_code == 302
    assert a.post("/maintenance/999/inspect").status_code == 302
    assert a.post("/maintenance/1/explode").status_code == 404


# ---------------- AI 4 assistant ----------------
from app.mohammed_alketbi.assistant import AssistantService  # noqa: E402


def test_assistant_refuses_actions(db, user):
    hessa = user("hessa@campus.test")
    for q in ["Approve my transfer", "please dispose of the projector", "can you approve R-0001",
              "transfer the chairs to me now"]:
        a = AssistantService(db).ask(q, hessa).content
        assert a["kind"] == "refused" and a["answer"].startswith("I cannot"), q
    assert db.execute("SELECT COUNT(*) FROM ai_output WHERE function_name='assistant'").fetchone()[0] == 4


def test_assistant_finds_items_by_department(db, user):
    a = AssistantService(db).ask("Which chairs are available in Engineering?", user("hessa@campus.test")).content
    assert a["kind"] == "search" and "Ergonomic office chairs" in a["answer"] and a["asset_ids"] == [2]


def test_assistant_explains_rules(db, user):
    a = AssistantService(db).ask("How long is an item reserved?", user("hessa@campus.test")).content
    assert a["kind"] == "rules" and "7 days" in a["answer"]
    a = AssistantService(db).ask("Who approves a transfer?", user("hessa@campus.test")).content
    assert "representative" in a["answer"]


def test_assistant_my_requests_and_unknown(db, user):
    hessa = user("hessa@campus.test")
    assert "no requests" in AssistantService(db).ask("what is the status of my requests", hessa).content["answer"]
    assert AssistantService(db).ask("what's the weather tomorrow", hessa).content["kind"] == "cannot_answer"


def test_assistant_only_uses_visible_data(db, user):
    # The Epson projector is Engineering's and NOT published: a Biology requester must not see it
    a = AssistantService(db).ask("Is there a projector?", user("hessa@campus.test")).content
    assert "Epson" not in a["answer"]
    a = AssistantService(db).ask("Is there a projector?", user("khalid@campus.test")).content   # Engineering custodian
    assert "Epson" in a["answer"]


def test_assistant_page_and_feedback(login, db):
    c = login("hessa@campus.test")
    page = c.post("/assistant", data={"question": "Which monitors are available?"}, follow_redirects=True).data.decode()
    assert "Dell 24-inch monitor" in page
    oid = db.execute("SELECT MAX(ai_output_id) FROM ai_output").fetchone()[0]
    c.post(f"/assistant/feedback/{oid}", data={"rating": "5"})
    assert db.execute("SELECT rating FROM ai_feedback").fetchone()[0] == 5
