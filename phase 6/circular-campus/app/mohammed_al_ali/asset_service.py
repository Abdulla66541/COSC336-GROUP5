"""C2 Departments and assets, C3 Publish and search (owner: Mohammed Al Ali)."""
from datetime import date, datetime, timedelta

from app.mohammed_alketbi.audit import AuditService
from app.db import now, transaction
from app.models import Asset, Category, Listing
from app.mubarak.states import CONDITIONS, AssetStatus, DomainError
from app.mubarak.history_service import HistoryService

LISTING_DAYS = 30   # FR-MKT-04


class AssetService:
    def __init__(self, db):
        self.db = db
        self.history = HistoryService(db)
        self.audit = AuditService(db)

    # ----- validation (section 5.2 data rules) -----
    def validate(self, data):
        errors = []
        if not (data.get("name") or "").strip():
            errors.append("Name is required.")
        if not data.get("category_id"):
            errors.append("Category is required.")
        elif not str(data["category_id"]).isdigit() or not Category.get(self.db, int(data["category_id"])):
            errors.append("Choose a valid category.")
        try:
            if int(data.get("quantity", 0)) < 1:
                errors.append("Quantity must be a whole number of 1 or more.")
        except (TypeError, ValueError):
            errors.append("Quantity must be a whole number of 1 or more.")
        try:
            if float(data.get("est_value_aed") or 0) < 0:
                errors.append("Estimated value must be 0 AED or more.")
        except ValueError:
            errors.append("Estimated value must be a number.")
        if data.get("condition") not in CONDITIONS:
            errors.append("Condition must be one of: " + ", ".join(CONDITIONS) + ".")
        pd = data.get("purchase_date")
        if pd:
            try:
                if date.fromisoformat(pd) > date.today():
                    errors.append("Purchase date cannot be in the future.")
            except ValueError:
                errors.append("Purchase date must be a valid date.")
        return errors

    def find_duplicate(self, tag_number):
        row = self.db.execute("SELECT * FROM asset WHERE tag_number = ?", (tag_number,)).fetchone()
        return Asset(row) if row else None

    def next_tag(self):
        n = self.db.execute("SELECT COALESCE(MAX(asset_id),0)+1 FROM asset").fetchone()[0]
        tag = f"CC-{n:05d}"
        while self.find_duplicate(tag):
            n += 1
            tag = f"CC-{n:05d}"
        return tag

    # ----- status changes: the ONLY place an asset's status is written -----
    def change_status(self, asset, new_status, actor_id, details=None, related=None):
        AssetStatus.check_move(asset.status, new_status)
        self.db.execute("UPDATE asset SET status=? WHERE asset_id=?", (new_status, asset.asset_id))
        self.history.record(asset.asset_id, f"{asset.status} -> {new_status}", actor_id, related, details)
        self.audit.log(actor_id, "asset.status", f"asset:{asset.asset_id}", old={"status": asset.status},
                       new={"status": new_status})
        asset.status = new_status
        return asset

    # ----- register / update -----
    def register_asset(self, data, user):
        errors = self.validate(data)
        if errors:
            raise DomainError(" ".join(errors))
        if user.role not in ("custodian", "dept_rep", "admin"):
            raise DomainError("Only custodians, department representatives or admins can register assets (BR-02).")
        try:
            owner_dept = int(data.get("owner_dept_id") or user.dept_id)
        except ValueError:
            raise DomainError("Choose a valid department.")
        if not self.db.execute("SELECT 1 FROM department WHERE dept_id=?", (owner_dept,)).fetchone():
            raise DomainError("Choose a valid department.")
        if user.role != "admin" and owner_dept != user.dept_id:
            raise DomainError("You can only register assets for your own department (BR-02).")
        with transaction(self.db):
            tag = (data.get("tag_number") or "").strip() or self.next_tag()
            if self.find_duplicate(tag):
                raise DomainError(f"Tag number {tag} already exists.")
            cur = self.db.execute(
                "INSERT INTO asset (tag_number, name, description, category_id, quantity, owner_dept_id,"
                " custodian_id, location, purchase_date, est_value_aed, condition, material_type, tags, status)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?, 'Draft')",
                (tag, data["name"].strip(), (data.get("description") or "").strip(), int(data["category_id"]),
                 int(data["quantity"]), owner_dept, int(data.get("custodian_id") or user.user_id),
                 (data.get("location") or "").strip(), data.get("purchase_date") or None,
                 float(data.get("est_value_aed") or 0), data["condition"],
                 (data.get("material_type") or "").strip(), (data.get("tags") or "").strip()))
            asset = Asset.get(self.db, cur.lastrowid)
            self.history.record(asset.asset_id, "Created", user.user_id, None, f"Tag {tag}")
            self.audit.log(user.user_id, "asset.create", f"asset:{asset.asset_id}", new=asset.as_dict())
            self.change_status(asset, "Registered", user.user_id, "Condition recorded: " + asset.condition)
        return Asset.get(self.db, asset.asset_id)

    def update_asset(self, asset_id, data, user, security):
        asset = Asset.get(self.db, asset_id)
        if not asset:
            raise DomainError("Asset not found.")
        if not security.can_manage_asset(user, asset):
            raise DomainError("You cannot edit an asset of another department (BR-02).")
        if asset.status not in ("Draft", "Registered", "Available"):
            raise DomainError(f"An asset that is {asset.status} cannot be edited now (BR-05).")
        merged = {**asset.as_dict(), **{k: v for k, v in data.items() if v is not None}}
        errors = self.validate(merged)
        if errors:
            raise DomainError(" ".join(errors))
        fields = ["name", "description", "category_id", "quantity", "location", "purchase_date",
                  "est_value_aed", "condition", "material_type", "tags"]
        with transaction(self.db):
            self.db.execute(
                "UPDATE asset SET " + ", ".join(f"{f}=?" for f in fields) + " WHERE asset_id=?",
                [(merged[f] or None) if f == "purchase_date" else merged[f] for f in fields] + [asset_id])
            changed = {f: merged[f] for f in fields if str(merged[f]) != str(asset.as_dict()[f])}
            if changed:
                self.history.record(asset_id, "Updated", user.user_id, None, ", ".join(changed))
                self.audit.log(user.user_id, "asset.update", f"asset:{asset_id}",
                               old={f: asset.as_dict()[f] for f in changed}, new=changed)
        return Asset.get(self.db, asset_id)

    # ----- marketplace -----
    def publish(self, asset_id, user, security):
        asset = Asset.get(self.db, asset_id)
        if not asset:
            raise DomainError("Asset not found.")
        if not security.can_manage_asset(user, asset):
            raise DomainError("Only the owning department can publish this asset.")
        if asset.status != "Registered":
            raise DomainError(f"Only a Registered asset can be published (it is {asset.status}) (BR-03).")
        with transaction(self.db):
            published = datetime.now()
            cur = self.db.execute(
                "INSERT INTO listing (asset_id, published_by, published_at, expires_at, status)"
                " VALUES (?,?,?,?, 'Active')",
                (asset_id, user.user_id, published.isoformat(timespec="seconds"),
                 (published + timedelta(days=LISTING_DAYS)).isoformat(timespec="seconds")))
            self.change_status(asset, "Available", user.user_id, "Published as surplus", f"listing:{cur.lastrowid}")
        return asset

    def withdraw(self, asset_id, user, security):
        asset = Asset.get(self.db, asset_id)
        if not security.can_manage_asset(user, asset):
            raise DomainError("Only the owning department can withdraw this listing.")
        with transaction(self.db):
            self.db.execute("UPDATE listing SET status='Withdrawn' WHERE asset_id=? AND status='Active'", (asset_id,))
            self.change_status(asset, "Registered", user.user_id, "Listing withdrawn")

    def expire_old_listings(self):
        with transaction(self.db):
            rows = self.db.execute(
                "SELECT l.listing_id, l.asset_id FROM listing l JOIN asset a ON a.asset_id=l.asset_id"
                " WHERE l.status='Active' AND l.expires_at < ? AND a.status='Available'", (now(),)).fetchall()
            for r in rows:
                self.db.execute("UPDATE listing SET status='Expired' WHERE listing_id=?", (r["listing_id"],))
                self.change_status(Asset.get(self.db, r["asset_id"]), "Registered", None, "Listing expired after 30 days")

    def split_for_reservation(self, asset, qty, actor_id):
        """Take `qty` units out of a batch into a new asset record so the rest
        stays on the marketplace. Must run inside a transaction."""
        if qty == asset.quantity:
            return asset
        tag = f"{asset.tag_number}-S{self.db.execute('SELECT COUNT(*) FROM asset WHERE tag_number LIKE ?', (asset.tag_number + '-S%',)).fetchone()[0] + 1}"
        self.db.execute("UPDATE asset SET quantity = quantity - ? WHERE asset_id=?", (qty, asset.asset_id))
        cur = self.db.execute(
            "INSERT INTO asset (tag_number, name, description, category_id, quantity, owner_dept_id, custodian_id,"
            " location, purchase_date, est_value_aed, condition, material_type, tags, status)"
            " SELECT ?, name, description, category_id, ?, owner_dept_id, custodian_id, location, purchase_date,"
            " est_value_aed, condition, material_type, tags, 'Available' FROM asset WHERE asset_id=?",
            (tag, qty, asset.asset_id))
        child = Asset.get(self.db, cur.lastrowid)
        self.history.record(asset.asset_id, "Split", actor_id, f"asset:{child.asset_id}",
                            f"{qty} unit(s) moved to {tag}")
        self.history.record(child.asset_id, "Created by split", actor_id, f"asset:{asset.asset_id}",
                            f"{qty} unit(s) from {asset.tag_number}")
        return child

    # ----- queries -----
    def categories(self):
        return Category.where(self.db, order="name, subcategory")

    def for_department(self, dept_id):
        return self.db.execute(
            "SELECT a.*, c.name AS category_name, c.subcategory, d.name AS dept_name, u.name AS custodian_name"
            " FROM asset a JOIN category c ON c.category_id=a.category_id JOIN department d ON d.dept_id=a.owner_dept_id"
            " JOIN user u ON u.user_id=a.custodian_id WHERE (? IS NULL OR a.owner_dept_id=?) AND a.active=1"
            " ORDER BY a.asset_id DESC", (dept_id, dept_id)).fetchall()

    def detail(self, asset_id):
        return self.db.execute(
            "SELECT a.*, c.name AS category_name, c.subcategory, d.name AS dept_name, u.name AS custodian_name"
            " FROM asset a JOIN category c ON c.category_id=a.category_id JOIN department d ON d.dept_id=a.owner_dept_id"
            " JOIN user u ON u.user_id=a.custodian_id WHERE a.asset_id=?", (asset_id,)).fetchone()


class SearchService:
    """Search and filter published surplus (C3). Only Available assets are
    visible campus-wide (BR-16)."""

    def __init__(self, db):
        self.db = db

    def search(self, keywords="", category_id=None, condition=None, dept_id=None, sort="newest"):
        sql = ("SELECT a.*, c.name AS category_name, c.subcategory, d.name AS dept_name"
               " FROM asset a JOIN category c ON c.category_id=a.category_id"
               " JOIN department d ON d.dept_id=a.owner_dept_id WHERE a.status='Available' AND a.active=1")
        params = []
        for word in (keywords or "").split():
            sql += " AND (a.name LIKE ? OR a.description LIKE ? OR a.tags LIKE ? OR c.name LIKE ? OR c.subcategory LIKE ?)"
            params += [f"%{word}%"] * 5
        if category_id:
            sql += " AND a.category_id = ?"
            params.append(int(category_id))
        if condition:
            sql += " AND a.condition = ?"
            params.append(condition)
        if dept_id:
            sql += " AND a.owner_dept_id = ?"
            params.append(int(dept_id))
        sql += {"value": " ORDER BY a.est_value_aed DESC", "name": " ORDER BY a.name"}.get(sort, " ORDER BY a.asset_id DESC")
        return self.db.execute(sql, params).fetchall()
