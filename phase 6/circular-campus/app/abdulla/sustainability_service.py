"""C7 Sustainability dashboard (owner: Abdulla). FR-SUS.

Every number is calculated by the database from recorded events. All are
shown as ESTIMATES with their formula and source (BR-17).
"""


class SustainabilityService:
    def __init__(self, db):
        self.db = db

    def _period(self, start, end):
        sql, params = "", []
        if start:
            sql += " AND date(e.event_time) >= ?"
            params.append(start)
        if end:
            sql += " AND date(e.event_time) <= ?"
            params.append(end)
        return sql, params

    def metrics(self, start=None, end=None):
        p_sql, p = self._period(start, end)
        base = ("FROM reuse_event e JOIN asset a ON a.asset_id=e.asset_id"
                " LEFT JOIN emission_factor f ON f.category_id=a.category_id WHERE 1=1" + p_sql)

        reused = self.db.execute(f"SELECT COALESCE(SUM(e.quantity),0) {base} AND e.event_type='transfer'", p).fetchone()[0]
        avoided = self.db.execute(f"SELECT COALESCE(SUM(e.avoided_value_aed),0) {base} AND e.event_type='transfer'", p).fetchone()[0]
        diverted_kg = self.db.execute(
            f"SELECT COALESCE(SUM(e.quantity * f.kg_weight_per_unit),0) {base}"
            " AND e.event_type IN ('transfer','repair','donate','recycle')", p).fetchone()[0]
        co2 = self.db.execute(
            f"SELECT COALESCE(SUM(e.quantity * f.kg_co2e_per_unit),0) {base}"
            " AND e.event_type IN ('transfer','repair','donate') AND f.factor_id IS NOT NULL", p).fetchone()[0]
        missing = self.db.execute(
            f"SELECT COUNT(*) {base} AND f.factor_id IS NULL", p).fetchone()[0]
        repaired = self.db.execute(f"SELECT COUNT(*) {base} AND e.event_type='repair'", p).fetchone()[0]

        considered = self.db.execute(
            "SELECT COUNT(DISTINCT asset_id) FROM asset_history WHERE event_type LIKE '%-> Available'").fetchone()[0]
        reuse_rate = round(100 * self.db.execute(
            f"SELECT COUNT(DISTINCT e.asset_id) {base} AND e.event_type='transfer'", p).fetchone()[0] / considered, 1) \
            if considered else None

        return [
            {"name": "Items reused", "value": f"{int(reused)}", "unit": "items",
             "formula": "Sum of quantities in completed transfers between departments",
             "source": "This system's transfer records (reuse_event table)"},
            {"name": "Purchases avoided (est.)", "value": f"AED {avoided:,.0f}", "unit": "AED",
             "formula": "Sum over reused items of (estimated value per unit x quantity)",
             "source": "Estimated value entered by the custodian at registration"},
            {"name": "Waste diverted (est.)", "value": f"{diverted_kg:,.0f}", "unit": "kg",
             "formula": "Sum over reused, donated and recycled items, plus 1 unit per verified repair, of (quantity x typical weight per unit)",
             "source": "Typical weight per category (table at the bottom of this page)"},
            {"name": "CO2e avoided (est.)", "value": f"{co2:,.0f}", "unit": "kg CO2e",
             "formula": "Sum over reused and donated items, plus 1 unit per verified repair, of (quantity x emission factor of the category)",
             "source": "Emission factor per category, stored with its source (FR-SUS-25)"
                       + (f". {missing} event(s) have no factor: 'not enough data'" if missing else "")},
            {"name": "Reuse rate", "value": f"{reuse_rate}%" if reuse_rate is not None else "Not enough data",
             "unit": "%", "formula": "(assets reused or transferred / assets published for reuse) x 100",
             "source": "Phase 3 section 4.21 formula; this system's records"},
            {"name": "Repairs completed", "value": f"{repaired}", "unit": "repairs",
             "formula": "Count of verified repairs (asset kept in use instead of replaced)",
             "source": "Maintenance tickets marked Verified"},
        ]

    def raw_numbers(self, start=None, end=None):
        """Numbers only, for the AI summary (the AI never calculates them)."""
        return {m["name"]: m["value"] for m in self.metrics(start, end)}

    def factors(self):
        return self.db.execute(
            "SELECT f.*, c.name, c.subcategory FROM emission_factor f JOIN category c ON c.category_id=f.category_id"
            " ORDER BY c.name, c.subcategory").fetchall()
