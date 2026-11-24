"""AI 2 - Matching and ranking (owner: Abdulla). UC-27.

Ranks published surplus for a request and returns the top 5 with a score
and a reason. The requester picks one (or none); choices are logged.
"""
from app.abdulla.ai_core import AIFacade, AIFeature, AIResult, stems
from app.models import Request

RANK = {"New": 5, "Good": 4, "Fair": 3, "Poor": 2, "Broken": 1, "Any": 0}


class MatchFeature(AIFeature):
    name = "match"
    prompt = ("Rank the 'listings' for this 'request'. Return at most 5 as {\"matches\": [{\"asset_id\": int, "
              "\"score\": 0-100, \"reason\": str}], \"confidence\": 0-1, \"explanation\": str}. Only use asset_ids "
              "from the listings. Data: {data}")

    def is_valid(self, content):
        ids = {a["asset_id"] for a in self.data["listings"]}
        m = content.get("matches")
        return isinstance(m, list) and len(m) <= 5 and all(x.get("asset_id") in ids for x in m)

    def fallback(self):
        req, listings = self.data["request"], self.data["listings"]
        need = stems(f"{req['category']} {req['purpose']} {req['specifications']}")
        scored = []
        for a in listings:
            cat_words = stems(f"{a['category_name']} {a['subcategory']}")
            have = stems(f"{a['name']} {a['description']} {a['tags']}") | cat_words
            overlap = need & have
            s_text = round(40 * len(overlap) / max(1, len(need)))
            cat_hit = req["category"].lower() in f"{a['category_name']} {a['subcategory']}".lower() or \
                bool(stems(req["category"]) & cat_words)
            s_cat = 25 if cat_hit else 0
            pref = RANK.get(req["preferred_condition"], 0)
            s_cond = 0 if a["condition"] == "Broken" else \
                (15 if RANK[a["condition"]] >= pref else max(0, 15 - 5 * (pref - RANK[a["condition"]])))
            s_qty = 10 if a["quantity"] >= req["quantity"] else 0
            s_loc = 5 if req["location"] and req["location"].split()[0].lower() in (a["location"] or "").lower() else 0
            s_urg = {"High": 5, "Medium": 3, "Low": 1}[req["urgency"]] if s_qty else 0
            reasons = (["same category"] if cat_hit else []) + \
                (["matches " + ", ".join(sorted(overlap)[:3])] if overlap else []) + \
                [f"{a['condition'].lower()} condition",
                 f"{a['quantity']} available" if s_qty else f"only {a['quantity']} available"] + \
                (["nearby"] if s_loc else [])
            if not cat_hit and not overlap:
                continue                      # unrelated item: never suggest it
            scored.append({"asset_id": a["asset_id"], "reason": ", ".join(reasons),
                           "score": min(100, s_text + s_cat + s_cond + s_qty + s_loc + s_urg)})
        scored = [s for s in sorted(scored, key=lambda s: -s["score"]) if s["score"] >= 20][:5]
        return AIResult(content={"matches": scored}, confidence=round(scored[0]["score"] / 100, 2) if scored else 0.0,
                        explanation="score = keyword similarity (40) + category (25) + condition (15) "
                                    "+ quantity (10) + location (5) + urgency (5)")


class MatchingService:
    def __init__(self, db, facade=None):
        self.db = db
        self.facade = facade or AIFacade(db)

    def find_matches(self, request_id):
        req = Request.get(self.db, request_id)
        listings = [dict(r) for r in self.db.execute(
            "SELECT a.*, c.name AS category_name, c.subcategory FROM asset a JOIN category c USING(category_id)"
            " WHERE a.status='Available' AND a.active=1 AND a.owner_dept_id != ?", (req.dept_id,))]
        result = self.facade.request(MatchFeature({"request": req.as_dict(), "listings": listings},
                                                  request_id=request_id))
        by_id = {a["asset_id"]: a for a in listings}
        result.content["matches"] = [dict(m, asset=by_id[m["asset_id"]]) for m in result.content["matches"]
                                     if m["asset_id"] in by_id]
        return result
