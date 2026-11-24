"""Demo data. Synthetic only: no real people or university records."""
from datetime import date, timedelta

from app.db import now
from app.mohammed_alketbi.security import PERMISSIONS, AuthService

DEMO_PASSWORD = "Password123!"

DEPARTMENTS = ["Engineering", "Computer Science", "Biology", "Business School", "Library"]

USERS = [  # name, email, role, department
    ("Admin User", "admin@campus.test", "admin", "Library"),
    ("Sara Eng Rep", "sara.rep@campus.test", "dept_rep", "Engineering"),
    ("Omar CS Rep", "omar.rep@campus.test", "dept_rep", "Computer Science"),
    ("Layla Bio Rep", "layla.rep@campus.test", "dept_rep", "Biology"),
    ("Khalid Eng Custodian", "khalid@campus.test", "custodian", "Engineering"),
    ("Mona CS Custodian", "mona@campus.test", "custodian", "Computer Science"),
    ("Yousef Biz Custodian", "yousef@campus.test", "custodian", "Business School"),
    ("Hessa Requester", "hessa@campus.test", "requester", "Biology"),
    ("Ali Requester", "ali@campus.test", "requester", "Computer Science"),
    ("Noura Requester", "noura@campus.test", "requester", "Engineering"),
]

# name, subcategory, kg CO2e per unit, kg weight per unit
CATEGORIES = [
    ("IT Equipment", "Monitor", 250, 5),
    ("IT Equipment", "Laptop", 300, 2),
    ("IT Equipment", "Desktop Computer", 350, 9),
    ("IT Equipment", "Printer", 180, 12),
    ("AV Equipment", "Projector", 150, 4),
    ("AV Equipment", "Audio/Video", 100, 6),
    ("Furniture", "Chair", 70, 12),
    ("Furniture", "Desk/Table", 120, 30),
    ("Furniture", "Storage", 110, 35),
    ("Lab Equipment", "Instrument", 200, 8),
    ("Books", "Textbook", 3, 1),
    ("Office Supplies", "General", None, 2),   # no factor on purpose: dashboard shows "not enough data"
]
FACTOR_SOURCE = ("ILLUSTRATIVE value for the prototype. Typical order of magnitude from manufacturer product "
                 "carbon footprint (PCF) and furniture EPD sheets. Replace with a cited figure before final report.")

# owner dept, custodian email, name, description, category (sub), qty, condition, value AED, years old, location, publish?
ASSETS = [
    ("Engineering", "khalid@campus.test", "Dell 24-inch monitor", "Dell P2419H, small scratch on bezel", "Monitor", 6, "Good", 650, 3, "Eng Building B, Room 204", True),
    ("Engineering", "khalid@campus.test", "Ergonomic office chairs", "Black mesh chairs with armrests", "Chair", 10, "Good", 400, 2, "Eng Building A, Store", True),
    ("Engineering", "khalid@campus.test", "Epson classroom projector", "Epson EB-X41, bulb broken", "Projector", 1, "Broken", 1800, 6, "Eng Building A, Room 101", False),
    ("Engineering", "khalid@campus.test", "Digital oscilloscope", "Rigol 100 MHz 2-channel oscilloscope", "Instrument", 2, "Good", 2200, 4, "Eng Lab 3", True),
    ("Computer Science", "mona@campus.test", "Lenovo ThinkPad laptops", "ThinkPad T14, 16GB RAM, batteries worn", "Laptop", 4, "Fair", 2500, 4, "CS Building, Room 12", True),
    ("Computer Science", "mona@campus.test", "Lab desks", "Wooden computer lab desks 120cm", "Desk/Table", 8, "Fair", 550, 7, "CS Building, Lab 2", True),
    ("Computer Science", "mona@campus.test", "HP LaserJet printer", "HP M404dn, prints faded pages", "Printer", 1, "Poor", 1200, 5, "CS Office", False),
    ("Business School", "yousef@campus.test", "Accounting textbooks", "Financial accounting textbooks, 2023 edition", "Textbook", 30, "Good", 180, 1, "Business Library Room", True),
    ("Business School", "yousef@campus.test", "Filing cabinets", "4-drawer steel filing cabinets", "Storage", 3, "Good", 900, 6, "Business Admin Office", True),
    ("Business School", "yousef@campus.test", "Conference speaker", "USB conference speaker and microphone", "Audio/Video", 2, "New", 700, 0, "Business Meeting Room", True),
]


def seed(db):
    auth = AuthService(db)
    db.execute("BEGIN")
    for role, perms in PERMISSIONS.items():
        for p in perms:
            db.execute("INSERT INTO role_permission (role, function_name, allowed) VALUES (?,?,1)", (role, p))
    dept = {}
    for name in DEPARTMENTS:
        dept[name] = db.execute("INSERT INTO department (name) VALUES (?)", (name,)).lastrowid
    users = {}
    for name, email, role, d in USERS:
        users[email] = db.execute(
            "INSERT INTO user (name, email, password_hash, role, dept_id) VALUES (?,?,?,?,?)",
            (name, email, auth.hash_password(DEMO_PASSWORD), role, dept[d])).lastrowid
        if role == "dept_rep":
            db.execute("UPDATE department SET rep_user_id=? WHERE dept_id=?", (users[email], dept[d]))
    cats = {}
    for name, sub, co2, kg in CATEGORIES:
        cid = db.execute("INSERT INTO category (name, subcategory) VALUES (?,?)", (name, sub)).lastrowid
        cats[sub] = cid
        if co2 is not None:
            db.execute("INSERT INTO emission_factor (category_id, kg_co2e_per_unit, kg_weight_per_unit, source)"
                       " VALUES (?,?,?,?)", (cid, co2, kg, FACTOR_SOURCE))
    for i, (d, email, name, desc, sub, qty, cond, value, years, loc, publish) in enumerate(ASSETS, start=1):
        purchased = (date.today() - timedelta(days=365 * years + 30)).isoformat()
        status = "Available" if publish else "Registered"
        aid = db.execute(
            "INSERT INTO asset (tag_number, name, description, category_id, quantity, owner_dept_id, custodian_id,"
            " location, purchase_date, est_value_aed, condition, material_type, tags, status)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (f"CC-{i:05d}", name, desc, cats[sub], qty, dept[d], users[email], loc, purchased, value, cond, "",
             sub.lower(), status)).lastrowid
        for ev in (["Created", "Draft -> Registered"] + (["Registered -> Available"] if publish else [])):
            db.execute("INSERT INTO asset_history (asset_id, event_type, actor_id, event_time, details)"
                       " VALUES (?,?,?,?,?)", (aid, ev, users[email], now(), "Demo data"))
        if publish:
            db.execute("INSERT INTO listing (asset_id, published_by, published_at, expires_at, status)"
                       " VALUES (?,?,?,?, 'Active')", (aid, users[email], now(),
                                                       (date.today() + timedelta(days=30)).isoformat()))
    db.execute("COMMIT")
