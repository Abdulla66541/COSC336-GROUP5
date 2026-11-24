"""AI 3 - Sustainable-action advice (owner: Mubarak). UC-28.

Recommends Reuse, Repair, Donate, Recycle or Dispose for an asset, with
reasons. Disposal is always the last option (BR-10). Accepting the advice
changes nothing: transfers and disposals still need approval (FR-AI-49).
"""
from app.abdulla.ai_core import AIFacade, AIFeature, AIResult
from app.models import Asset

ACTIONS = ("Reuse", "Repair", "Donate", "Recycle", "Dispose")


class AdviceFeature(AIFeature):
    name = "advice"
    prompt = ("Recommend ONE action for this campus asset: Reuse, Repair, Donate, Recycle or Dispose. Dispose only if "
              "nothing else fits. Return {\"action\": str, \"reasons\": [str], \"repair_cost\": number, "
              "\"new_cost\": number, \"confidence\": 0-1, \"explanation\": str}. Data: {data}")

    def is_valid(self, content):
        return content.get("action") in ACTIONS and isinstance(content.get("reasons"), list)

    def fallback(self):
        d = self.data
        cond, age, value = d["condition"], d.get("age_years") or 0, d["est_value_aed"]
        repair_cost = d.get("est_repair_cost") or round(value * {"Broken": 0.35, "Poor": 0.2}.get(cond, 0.05))
        new_cost = round(value * 1.6)
        reasons = []
        if cond in ("New", "Good", "Fair"):
            action = "Reuse"
            reasons.append(f"condition is {cond}; it can serve another department as is")
            if new_cost:
                reasons.append(f"avoids a new purchase of about AED {new_cost:,.0f}")
        elif new_cost and repair_cost < 0.5 * new_cost and age < 8:
            action = "Repair"
            reasons.append(f"estimated repair AED {repair_cost:,.0f} vs about AED {new_cost:,.0f} new")
            reasons.append(f"{age} years old, still within useful life")
        elif cond == "Poor":
            action = "Donate"
            reasons.append("still usable but not worth repairing for campus use")
        elif d.get("material_type") or d.get("category") in ("IT Equipment", "AV Equipment", "Furniture"):
            action = "Recycle"
            reasons.append("not repairable at sensible cost; materials can be recovered")
            if d.get("category") in ("IT Equipment", "AV Equipment"):
                reasons.append("electronics should go to a certified e-waste recycler")
        else:
            action = "Dispose"
            reasons.append("no reuse, repair, donation or recycling route found (disposal is the last option)")
        conf = {"Reuse": 0.8, "Repair": 0.7, "Donate": 0.6, "Recycle": 0.65, "Dispose": 0.5}[action]
        return AIResult(content={"action": action, "reasons": reasons, "repair_cost": repair_cost, "new_cost": new_cost},
                        confidence=conf,
                        explanation="Rules: reuse if usable; repair if cost < 50% of new and age < 8 years; "
                                    "then donate, recycle, and dispose last (BR-10).")


class RecommendationService:
    def __init__(self, db, facade=None):
        self.db = db
        self.facade = facade or AIFacade(db)

    def recommend(self, asset_id, est_repair_cost=None):
        a = Asset.get(self.db, asset_id)
        cat = self.db.execute("SELECT name FROM category WHERE category_id=?", (a.category_id,)).fetchone()["name"]
        data = {"name": a.name, "description": a.description, "condition": a.condition, "age_years": a.age_years(),
                "est_value_aed": a.est_value_aed, "material_type": a.material_type, "category": cat,
                "est_repair_cost": est_repair_cost}
        return self.facade.request(AdviceFeature(data, asset_id=asset_id))
