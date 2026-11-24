"""AI 4 - Assistant (owner: Mohammed Alketbi). UC-29, FR-AI-50 to 59.

Answers questions using only data the user is allowed to see: published
surplus, their own department's assets, their own requests and the system
rules. It never performs actions: asked to approve, transfer or dispose,
it refuses and points to the right page (FR-AI-58, FR-AI-59).
"""
import re

from app.abdulla.ai_core import AIFacade, AIFeature, AIResult, stems

ACTION_VERBS = r"(approve|reject|dispose( of)?|delete|remove|publish|withdraw|cancel|transfer|reserve|recycle|donate|move)"
ACTION_PATTERN = re.compile(rf"^\s*(please\s+|can you\s+|could you\s+|would you\s+|i want you to\s+)?{ACTION_VERBS}\b"
                            rf"|\b{ACTION_VERBS}\b.*\b(for me|on my behalf|right now|now)\b", re.I)
REFUSAL_PAGES = {
    "approve": "an approver must decide it on the Approvals page",
    "reject": "an approver must decide it on the Approvals page",
    "dispose": "use the Donate, recycle or dispose form on the asset page; an administrator must approve it",
    "recycle": "use the Donate, recycle or dispose form on the asset page; an administrator must approve it",
    "donate": "use the Donate, recycle or dispose form on the asset page; an administrator must approve it",
    "delete": "assets are never deleted; their history is kept (BR-13)",
    "transfer": "a transfer starts from a request and needs approval on the Approvals page",
    "reserve": "open your request's AI matches or the asset page and press Reserve yourself",
}

# System rules the assistant may explain (Phase 3 business rules)
POLICIES = [
    ({"reservation", "reserve", "reserved", "hold", "long"},
     "A reserved item is held for 7 days. If it is not approved in that time, the reservation expires and the item "
     "goes back to the marketplace (BR-04)."),
    ({"approve", "approves", "approval", "approver", "who"},
     "Transfers are approved by the representative of the department that owns the item, or by an administrator. "
     "Nobody can approve their own request (BR-06, BR-07)."),
    ({"owner", "ownership", "receive", "received", "receipt", "confirm"},
     "Ownership, custodian and location change only when the receiver confirms receipt on the Transfers page (BR-08)."),
    ({"dispose", "disposal", "recycle", "donate", "donation", "throw"},
     "Disposal is the last option. You must explain why reuse, transfer, repair, donation and recycling do not fit, "
     "and an administrator must approve it (BR-09, BR-10)."),
    ({"listing", "listed", "publish", "published", "expire", "expires"},
     "A published listing stays on the marketplace for 30 days, then returns to Registered."),
    ({"co2", "carbon", "sustainability", "dashboard", "waste", "estimate", "estimates"},
     "Sustainability numbers are estimates calculated from recorded reuse, repair, donation and recycling events. "
     "Each number on the dashboard shows its formula and source (BR-17)."),
    ({"maintenance", "repair", "broken", "defect", "fix"},
     "Report a defect from the asset page. The asset goes to In Maintenance until a repair is verified."),
]


class AssistantFeature(AIFeature):
    name = "assistant"
    prompt = ("Answer the user's 'question' using ONLY 'assets', 'my_requests' and 'rules' below. If the answer is not "
              "in the data say you cannot answer. Never claim to approve, transfer or dispose of anything. Return "
              "{\"answer\": str, \"asset_ids\": [int], \"confidence\": 0-1, \"explanation\": str}. Data: {data}")

    def is_valid(self, content):
        ids = {a["asset_id"] for a in self.data["assets"]}
        return isinstance(content.get("answer"), str) and all(i in ids for i in content.get("asset_ids", []))

    def fallback(self):
        q = self.data["question"]
        qw = stems(q)
        raw = set(re.findall(r"[a-z]+", q.lower()))
        # 1. the user's own requests
        if "my" in raw and raw & {"request", "requests", "status"}:
            reqs = self.data["my_requests"]
            if not reqs:
                return self._answer("You have no requests yet.", [], 0.8, "my_requests")
            lines = [f"R-{r['request_id']:04d}: {r['quantity']} x {r['category']} is {r['status']}" for r in reqs[:5]]
            return self._answer("Your latest requests: " + "; ".join(lines) + ".", [], 0.85, "my_requests")
        # 2. rules
        best = max(POLICIES, key=lambda p: len(p[0] & qw))
        policy_hits = len(best[0] & qw)
        # 3. search the data the user may see
        found = []
        for a in self.data["assets"]:
            have = stems(f"{a['name']} {a['description']} {a['tags']} {a['category_name']} {a['subcategory']}")
            dept_hit = a["dept_name"].lower() in q.lower()
            score = len(qw & have) * 2 + (1 if dept_hit else 0)
            depts_named = [d for d in self.data["departments"] if d.lower() in q.lower()]
            if depts_named and not dept_hit:
                continue
            if score >= 2:
                found.append((score, a))
        found = [a for _, a in sorted(found, key=lambda x: -x[0])][:5]
        if found and policy_hits < 2:
            items = ", ".join(f"{a['tag_number']} {a['name']} ({a['quantity']} x, {a['condition']}, "
                              f"{a['dept_name']}, {a['status']})" for a in found)
            return self._answer(f"I found {len(found)} item(s): {items}.", [a["asset_id"] for a in found], 0.75, "search")
        if policy_hits:
            return self._answer(best[1], [], 0.7, "rules")
        return self._answer("I cannot answer that from the system's data. I can help you find surplus items, check "
                            "your requests, or explain the rules (reservations, approvals, transfers, disposal).",
                            [], 0.3, "cannot_answer")

    @staticmethod
    def _answer(text, ids, conf, kind):
        return AIResult(content={"answer": text, "asset_ids": ids, "kind": kind}, confidence=conf,
                        explanation=f"Rule-based answer ({kind}) from data you are allowed to see.")


class AssistantService:
    def __init__(self, db, facade=None):
        self.db = db
        self.facade = facade or AIFacade(db)

    def refuse_action(self, question):
        """FR-AI-58/59: refuse any request to act. Checked before the AI is called."""
        m = ACTION_PATTERN.search(question or "")
        if not m:
            return None
        verb = next((v for v in REFUSAL_PAGES if v in m.group(0).lower()), "approve")
        return f"I cannot {verb} anything for you. I only give information; {REFUSAL_PAGES[verb]}."

    def visible_assets(self, user):
        """BR-16: published items for everyone, plus the user's own department's assets."""
        return [dict(r) for r in self.db.execute(
            "SELECT a.asset_id, a.tag_number, a.name, a.description, a.tags, a.quantity, a.condition, a.status,"
            " c.name AS category_name, c.subcategory, d.name AS dept_name FROM asset a"
            " JOIN category c USING(category_id) JOIN department d ON d.dept_id=a.owner_dept_id"
            " WHERE a.active=1 AND (a.status='Available' OR a.owner_dept_id=? OR ?='admin')",
            (user.dept_id, user.role))]

    def ask(self, question, user):
        question = (question or "").strip()[:500]
        if not question:
            return None
        refusal = self.refuse_action(question)
        if refusal:
            feature = AssistantFeature({"question": question})
            result = AIResult(content={"answer": refusal, "asset_ids": [], "kind": "refused"}, confidence=1.0,
                              explanation="Action requests are always refused (FR-AI-58, FR-AI-59).")
            return self.facade.logger.save(feature, result)
        data = {
            "question": question,
            "assets": self.visible_assets(user),
            "my_requests": [dict(r) for r in self.db.execute(
                "SELECT request_id, category, quantity, status, required_date FROM request WHERE requester_id=?"
                " ORDER BY request_id DESC", (user.user_id,))],
            "departments": [r["name"] for r in self.db.execute("SELECT name FROM department")],
            "rules": [p[1] for p in POLICIES],
        }
        return self.facade.request(AssistantFeature(data))
