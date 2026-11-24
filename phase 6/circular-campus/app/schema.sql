-- Circular Campus database (SQLite). Tables follow the ER diagram in
-- phase 4-5/00_architecture_and_shared_design.md, section 5.

PRAGMA foreign_keys = ON;

-- ---------- Part 3: departments, users, permissions ----------
CREATE TABLE department (
    dept_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL UNIQUE,
    rep_user_id  INTEGER
);

CREATE TABLE user (
    user_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name                TEXT NOT NULL,
    email               TEXT NOT NULL UNIQUE,
    password_hash       TEXT NOT NULL,
    role                TEXT NOT NULL CHECK (role IN ('requester','custodian','dept_rep','admin')),
    dept_id             INTEGER NOT NULL REFERENCES department(dept_id),
    status              TEXT NOT NULL DEFAULT 'Active' CHECK (status IN ('Active','Deactivated')),
    email_notifications INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE role_permission (
    permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role          TEXT NOT NULL,
    function_name TEXT NOT NULL,
    allowed       INTEGER NOT NULL DEFAULT 1,
    UNIQUE (role, function_name)
);

-- ---------- Part 1: assets, marketplace, requests ----------
CREATE TABLE category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    subcategory TEXT NOT NULL DEFAULT '',
    UNIQUE (name, subcategory)
);

CREATE TABLE asset (
    asset_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_number    TEXT NOT NULL UNIQUE,
    name          TEXT NOT NULL,
    description   TEXT NOT NULL DEFAULT '',
    category_id   INTEGER NOT NULL REFERENCES category(category_id),
    quantity      INTEGER NOT NULL CHECK (quantity >= 1),
    owner_dept_id INTEGER NOT NULL REFERENCES department(dept_id),
    custodian_id  INTEGER NOT NULL REFERENCES user(user_id),
    location      TEXT NOT NULL DEFAULT '',
    purchase_date TEXT,
    est_value_aed REAL NOT NULL DEFAULT 0 CHECK (est_value_aed >= 0),
    condition     TEXT NOT NULL CHECK (condition IN ('New','Good','Fair','Poor','Broken')),
    material_type TEXT NOT NULL DEFAULT '',
    tags          TEXT NOT NULL DEFAULT '',
    status        TEXT NOT NULL,
    active        INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE listing (
    listing_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id     INTEGER NOT NULL REFERENCES asset(asset_id),
    published_by INTEGER NOT NULL REFERENCES user(user_id),
    published_at TEXT NOT NULL,
    expires_at   TEXT NOT NULL,
    status       TEXT NOT NULL CHECK (status IN ('Active','Withdrawn','Expired'))
);

CREATE TABLE request (
    request_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    requester_id        INTEGER NOT NULL REFERENCES user(user_id),
    dept_id             INTEGER NOT NULL REFERENCES department(dept_id),
    category            TEXT NOT NULL,
    purpose             TEXT NOT NULL,
    specifications      TEXT NOT NULL DEFAULT '',
    quantity            INTEGER NOT NULL CHECK (quantity >= 1),
    preferred_condition TEXT NOT NULL DEFAULT 'Any',
    urgency             TEXT NOT NULL CHECK (urgency IN ('Low','Medium','High')),
    location            TEXT NOT NULL DEFAULT '',
    required_date       TEXT NOT NULL,
    status              TEXT NOT NULL,
    created_at          TEXT NOT NULL
);

CREATE TABLE reservation (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id       INTEGER NOT NULL REFERENCES asset(asset_id),
    request_id     INTEGER NOT NULL REFERENCES request(request_id),
    quantity       INTEGER NOT NULL CHECK (quantity >= 1),
    reserved_at    TEXT NOT NULL,
    expires_at     TEXT NOT NULL,
    status         TEXT NOT NULL CHECK (status IN ('Active','Expired','Released','Converted'))
);

-- ---------- Part 2: approvals, transfers, maintenance, history ----------
CREATE TABLE approval (
    approval_id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type TEXT NOT NULL,
    asset_id    INTEGER REFERENCES asset(asset_id),
    request_id  INTEGER REFERENCES request(request_id),
    approver_id INTEGER REFERENCES user(user_id),
    decision    TEXT,
    reason      TEXT,
    decided_at  TEXT,
    status      TEXT NOT NULL CHECK (status IN ('Pending','Approved','Rejected','Cancelled')),
    created_at  TEXT NOT NULL
);

CREATE TABLE transfer (
    transfer_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id          INTEGER NOT NULL REFERENCES asset(asset_id),
    request_id        INTEGER REFERENCES request(request_id),
    quantity          INTEGER NOT NULL DEFAULT 1,
    from_dept_id      INTEGER NOT NULL REFERENCES department(dept_id),
    to_dept_id        INTEGER NOT NULL REFERENCES department(dept_id),
    handover_date     TEXT,
    handover_location TEXT,
    status            TEXT NOT NULL,
    received_by       INTEGER REFERENCES user(user_id),
    received_at       TEXT,
    discrepancy_note  TEXT,
    created_at        TEXT NOT NULL
);

CREATE TABLE maintenance_ticket (
    ticket_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id      INTEGER NOT NULL REFERENCES asset(asset_id),
    reported_by   INTEGER NOT NULL REFERENCES user(user_id),
    assigned_to   INTEGER REFERENCES user(user_id),
    description   TEXT NOT NULL,
    inspection_at TEXT,
    status        TEXT NOT NULL,
    created_at    TEXT NOT NULL
);

CREATE TABLE repair_record (
    repair_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id    INTEGER NOT NULL REFERENCES maintenance_ticket(ticket_id),
    performed_by INTEGER NOT NULL REFERENCES user(user_id),
    action       TEXT NOT NULL,
    cost_aed     REAL NOT NULL CHECK (cost_aed >= 0),
    repair_date  TEXT NOT NULL
);

CREATE TABLE end_of_life_request (
    eol_id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id                INTEGER NOT NULL REFERENCES asset(asset_id),
    requested_by            INTEGER NOT NULL REFERENCES user(user_id),
    action                  TEXT NOT NULL CHECK (action IN ('Donate','Recycle','Dispose')),
    reason                  TEXT NOT NULL,
    alternatives_assessment TEXT NOT NULL DEFAULT '',
    status                  TEXT NOT NULL,
    recipient               TEXT,
    created_at              TEXT NOT NULL
);

-- History is append-only (BR-13): triggers below block UPDATE and DELETE.
CREATE TABLE asset_history (
    event_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id       INTEGER NOT NULL REFERENCES asset(asset_id),
    event_type     TEXT NOT NULL,
    actor_id       INTEGER REFERENCES user(user_id),
    event_time     TEXT NOT NULL,
    related_record TEXT,
    details        TEXT
);
CREATE TRIGGER asset_history_no_update BEFORE UPDATE ON asset_history
BEGIN SELECT RAISE(ABORT, 'asset history cannot be changed (BR-13)'); END;
CREATE TRIGGER asset_history_no_delete BEFORE DELETE ON asset_history
BEGIN SELECT RAISE(ABORT, 'asset history cannot be deleted (BR-13)'); END;

CREATE TABLE audit_log (
    audit_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    actor_id   INTEGER REFERENCES user(user_id),
    action     TEXT NOT NULL,
    record_ref TEXT,
    outcome    TEXT NOT NULL,
    old_value  TEXT,
    new_value  TEXT,
    event_time TEXT NOT NULL
);
CREATE TRIGGER audit_no_update BEFORE UPDATE ON audit_log
BEGIN SELECT RAISE(ABORT, 'audit log cannot be changed (BR-13)'); END;
CREATE TRIGGER audit_no_delete BEFORE DELETE ON audit_log
BEGIN SELECT RAISE(ABORT, 'audit log cannot be deleted (BR-13)'); END;

CREATE TABLE notification (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES user(user_id),
    event_type      TEXT NOT NULL,
    message         TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'Unread' CHECK (status IN ('Unread','Read')),
    created_at      TEXT NOT NULL
);

-- ---------- Part 4: AI and sustainability ----------
CREATE TABLE ai_output (
    ai_output_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    function_name  TEXT NOT NULL,
    asset_id       INTEGER REFERENCES asset(asset_id),
    request_id     INTEGER REFERENCES request(request_id),
    model_id       TEXT NOT NULL,
    model_version  TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    confidence     REAL,
    content        TEXT NOT NULL,
    created_at     TEXT NOT NULL
);

CREATE TABLE ai_override (
    override_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    ai_output_id INTEGER NOT NULL REFERENCES ai_output(ai_output_id),
    user_id      INTEGER NOT NULL REFERENCES user(user_id),
    final_value  TEXT NOT NULL,
    reason       TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE ai_feedback (
    feedback_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    ai_output_id INTEGER NOT NULL REFERENCES ai_output(ai_output_id),
    user_id      INTEGER NOT NULL REFERENCES user(user_id),
    rating       INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment      TEXT
);

CREATE TABLE reuse_event (
    reuse_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id          INTEGER NOT NULL REFERENCES asset(asset_id),
    request_id        INTEGER REFERENCES request(request_id),
    event_type        TEXT NOT NULL,
    quantity          INTEGER NOT NULL DEFAULT 1,
    avoided_value_aed REAL NOT NULL DEFAULT 0,
    event_time        TEXT NOT NULL
);

CREATE TABLE emission_factor (
    factor_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id      INTEGER NOT NULL REFERENCES category(category_id),
    kg_co2e_per_unit REAL NOT NULL,
    kg_weight_per_unit REAL NOT NULL DEFAULT 0,
    source           TEXT NOT NULL
);

-- AI 5: generated reports. Cannot be exported until reviewed (FR-AI-70).
CREATE TABLE ai_report (
    report_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    period_start TEXT NOT NULL,
    period_end   TEXT NOT NULL,
    text         TEXT NOT NULL,
    flags        TEXT NOT NULL DEFAULT '',
    status       TEXT NOT NULL CHECK (status IN ('Not reviewed','Reviewed')),
    ai_output_id INTEGER REFERENCES ai_output(ai_output_id),
    created_by   INTEGER NOT NULL REFERENCES user(user_id),
    created_at   TEXT NOT NULL,
    reviewed_by  INTEGER REFERENCES user(user_id),
    reviewed_at  TEXT
);
