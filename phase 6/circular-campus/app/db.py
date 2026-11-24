"""Database access: one SQLite connection per web request."""
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime

from flask import current_app, g


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def connect(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path, isolation_level=None, timeout=10)  # autocommit; we open transactions ourselves
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = connect(current_app.config["DATABASE"])
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@contextmanager
def transaction(db: sqlite3.Connection):
    """BEGIN IMMEDIATE takes the write lock at the start, so two users can
    never reserve or transfer the same last item at the same time."""
    if db.in_transaction:          # nested call: join the outer transaction
        yield db
        return
    db.execute("BEGIN IMMEDIATE")
    try:
        yield db
        db.execute("COMMIT")
    except Exception:
        db.execute("ROLLBACK")
        raise


def init_schema(db: sqlite3.Connection):
    schema = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema, encoding="utf-8") as f:
        db.executescript(f.read())
