"""AI 5 - Generated report (owner: Abdulla). UC-30, FR-AI-60 to 70.

The database calculates every number. The AI only writes the text around
them. Every figure in the text is checked against the data and mismatches
are flagged. A report cannot be exported before a person marks it reviewed.
"""
import re

from app.abdulla.ai_core import AIFacade, AIFeature, AIResult
from app.abdulla.sustainability_service import SustainabilityService
from app.db import now, transaction
from app.mubarak.states import DomainError

NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")


def numbers_in(text):
    return {n.replace(",", "") for n in NUMBER.findall(text or "")}


class ReportFeature(AIFeature):
    name = "report"
    prompt = ("Write a short plain-English sustainability summary (4-6 sentences) for campus managers using ONLY the "
              "'figures' and 'activity' given. Copy numbers exactly; do not calculate new ones. Call money, waste and "
              "CO2e values estimates. Return {\"text\": str, \"confidence\": 0-1, \"explanation\": str}. Data: {data}")

    def is_valid(self, content):
        return isinstance(content.get("text"), str) and len(content["text"]) > 20

    def fallback(self):
        f, a, p = self.data["figures"], self.data["activity"], self.data["period"]
        text = (
            f"Circular Campus summary for {p}. "
            f"{a['requests_submitted']} request(s) were submitted and {a['requests_fulfilled']} were fulfilled through "
            f"{a['transfers_completed']} completed transfer(s). "
            f"In total {f['Items reused']} item(s) were reused between departments, avoiding purchases worth an "
            f"estimated {f['Purchases avoided (est.)']}. "
            f"This diverted an estimated {f['Waste diverted (est.)']} kg of waste and avoided an estimated "
            f"{f['CO2e avoided (est.)']} kg CO2e. "
            f"{f['Repairs completed']} repair(s) kept equipment in use, and {a['listings_published']} item(s) were "
            f"published as surplus. The reuse rate was {f['Reuse rate']}. "
            "All money, waste and carbon values are estimates; see the Sustainability page for formulas and sources."
        )
        return AIResult(content={"text": text}, confidence=0.9,
                        explanation="Template text filled with the database figures.")


class AIReportService:
    def __init__(self, db, facade=None):
        self.db = db
        self.facade = facade or AIFacade(db)

    def activity(self, start, end):
        def q(sql):
            return self.db.execute(sql, (start, end)).fetchone()[0]
        return {
            "requests_submitted": q("SELECT COUNT(*) FROM request WHERE date(created_at) BETWEEN ? AND ?"),
            "requests_fulfilled": q("SELECT COUNT(*) FROM request r JOIN transfer t USING(request_id)"
                                    " WHERE t.status='Completed' AND date(t.received_at) BETWEEN ? AND ?"),
            "transfers_completed": q("SELECT COUNT(*) FROM transfer WHERE status='Completed'"
                                     " AND date(received_at) BETWEEN ? AND ?"),
            "listings_published": q("SELECT COUNT(*) FROM listing WHERE date(published_at) BETWEEN ? AND ?"),
        }

    def check_figures(self, text, figures, activity, period_dates):
        """FR-AI-66: every number in the text must come from the data."""
        allowed = set()
        for v in list(figures.values()) + list(activity.values()) + list(period_dates):
            allowed |= numbers_in(str(v))
        allowed |= {"2"} if "CO2e" in text else set()       # the "2" in CO2e
        return sorted(n for n in numbers_in(text) if n not in allowed)

    def generate(self, start, end, user):
        if not start or not end or start > end:
            raise DomainError("Choose a valid period (start before end).")
        figures = SustainabilityService(self.db).raw_numbers(start, end)
        activity = self.activity(start, end)
        period = f"{start} to {end}"
        result = self.facade.request(ReportFeature({"figures": figures, "activity": activity, "period": period}))
        text = result.content["text"]
        flags = self.check_figures(text, figures, activity, (start, end))
        with transaction(self.db):
            cur = self.db.execute(
                "INSERT INTO ai_report (period_start, period_end, text, flags, status, ai_output_id, created_by,"
                " created_at) VALUES (?,?,?,?, 'Not reviewed', ?,?,?)",
                (start, end, text, ", ".join(flags), result.output_id, user.user_id, now()))
        return cur.lastrowid

    def mark_reviewed(self, report_id, text, user):
        rep = self.get(report_id)
        if not rep:
            raise DomainError("Report not found.")
        if not (text or "").strip():
            raise DomainError("The report text cannot be empty.")
        figures = SustainabilityService(self.db).raw_numbers(rep["period_start"], rep["period_end"])
        flags = self.check_figures(text, figures, self.activity(rep["period_start"], rep["period_end"]),
                                   (rep["period_start"], rep["period_end"]))
        if flags:
            raise DomainError("These numbers do not match the data: " + ", ".join(flags) +
                              ". Fix them before marking the report as reviewed.")
        with transaction(self.db):
            self.db.execute("UPDATE ai_report SET text=?, flags='', status='Reviewed', reviewed_by=?, reviewed_at=?"
                            " WHERE report_id=?", (text.strip(), user.user_id, now(), report_id))
            if text.strip() != rep["text"]:
                self.facade.logger.override(rep["ai_output_id"], user.user_id, "edited text", "Edited by reviewer")

    def get(self, report_id):
        return self.db.execute("SELECT r.*, u.name AS creator, v.name AS reviewer FROM ai_report r"
                               " JOIN user u ON u.user_id=r.created_by LEFT JOIN user v ON v.user_id=r.reviewed_by"
                               " WHERE report_id=?", (report_id,)).fetchone()

    def list(self):
        return self.db.execute("SELECT r.*, u.name AS creator FROM ai_report r JOIN user u ON u.user_id=r.created_by"
                               " ORDER BY report_id DESC").fetchall()

    def export_text(self, report_id):
        rep = self.get(report_id)
        if not rep:
            raise DomainError("Report not found.")
        if rep["status"] != "Reviewed":
            raise DomainError("A report cannot be shared before it is reviewed (FR-AI-70).")
        return (f"Circular Campus - AI-assisted sustainability report\nPeriod: {rep['period_start']} to "
                f"{rep['period_end']}\nReviewed by: {rep['reviewer']} on {rep['reviewed_at']}\n\n{rep['text']}\n")
