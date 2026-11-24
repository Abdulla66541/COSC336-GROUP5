import os
import sys
from datetime import date, timedelta

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from app.db import connect  # noqa: E402
from app.models import User  # noqa: E402

PW = "Password123!"


@pytest.fixture
def app(tmp_path):
    return create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.sqlite"), "SECRET_KEY": "test"})


@pytest.fixture
def db(app):
    conn = connect(app.config["DATABASE"])
    yield conn
    conn.close()


@pytest.fixture
def user(db):
    def get(email):
        return User(db.execute("SELECT * FROM user WHERE email=?", (email,)).fetchone())
    return get


@pytest.fixture
def login(app):
    def do(email):
        c = app.test_client()
        r = c.post("/login", data={"email": email, "password": PW})
        assert r.status_code == 302, f"login failed for {email}"
        return c
    return do


def future(days=10):
    return (date.today() + timedelta(days=days)).isoformat()


def request_data(**kw):
    d = {"category": "Chair", "purpose": "Seating for new lab", "specifications": "office chair with armrests",
         "quantity": "4", "preferred_condition": "Good", "urgency": "High", "location": "Bio Building Lab 4",
         "required_date": future()}
    d.update(kw)
    return d
