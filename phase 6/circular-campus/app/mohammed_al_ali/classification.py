"""AI 1 - Classification and tagging (owner: Mohammed Al Ali). UC-26.

Suggests a category, condition and tags from the asset's name and
description. The custodian accepts or edits; edits are logged (BR-12).
"""
import re

from app.abdulla.ai_core import AIFacade, AIFeature, AIResult, words

# keyword -> (category name, subcategory)
KEYWORDS = {
    ("monitor", "screen", "display"): ("IT Equipment", "Monitor"),
    ("laptop", "notebook", "macbook", "thinkpad"): ("IT Equipment", "Laptop"),
    ("desktop", "pc", "computer", "workstation", "tower"): ("IT Equipment", "Desktop Computer"),
    ("printer", "scanner", "copier"): ("IT Equipment", "Printer"),
    ("projector", "beamer"): ("AV Equipment", "Projector"),
    ("speaker", "microphone", "camera", "tv", "television"): ("AV Equipment", "Audio/Video"),
    ("chair", "chairs", "stool", "seat", "seating"): ("Furniture", "Chair"),
    ("desk", "desks", "table", "tables", "bench"): ("Furniture", "Desk/Table"),
    ("cabinet", "shelf", "shelves", "bookcase", "locker", "drawer"): ("Furniture", "Storage"),
    ("microscope", "beaker", "centrifuge", "oscilloscope", "multimeter", "pipette", "balance", "incubator"):
        ("Lab Equipment", "Instrument"),
    ("book", "books", "textbook", "textbooks", "journal", "manual"): ("Books", "Textbook"),
    ("whiteboard", "stapler", "stationery", "paper", "binder", "shredder"): ("Office Supplies", "General"),
}
CONDITION_WORDS = [
    (("broken", "not working", "dead", "cracked screen", "doesn't turn on", "faulty"), "Broken"),
    (("worn", "torn", "heavy wear", "very old", "rusty"), "Poor"),
    (("scratch", "scratches", "scratched", "minor", "small dent", "used"), "Good"),
    (("sealed", "brand new", "unused", "unopened", "new"), "New"),
]
BRANDS = ("dell", "hp", "lenovo", "apple", "epson", "samsung", "acer", "asus", "canon")


class ClassifyFeature(AIFeature):
    name = "classify"
    prompt = ("Suggest a category (choose ONLY an id from 'categories'), a condition (New, Good, Fair, Poor, Broken) "
              "and up to 5 short tags for this asset. Return {\"category_id\": int, \"category_label\": str, "
              "\"condition\": str, \"tags\": [str], \"confidence\": 0-1, \"explanation\": str}. Data: {data}")

    def is_valid(self, content):
        ids = {c["id"] for c in self.data["categories"]}
        return content.get("category_id") in ids and content.get("condition") in ("New", "Good", "Fair", "Poor", "Broken")

    def fallback(self):
        text = f"{self.data.get('name', '')} {self.data.get('description', '')}".lower()
        tokens, name_tokens = words(text), words(self.data.get("name", ""))
        hits, best = 0, None
        for keys, cat in KEYWORDS.items():
            # a keyword in the item name counts double (e.g. "HP laptop, cracked screen" is a laptop)
            n = sum(2 if k in name_tokens else 1 for k in keys if k in tokens)
            if n > hits:
                hits, best = n, cat
        cat_id = next((c["id"] for c in self.data["categories"] if best and (c["name"], c["subcategory"]) == best), None)
        condition, cond_word = "Fair", None
        for keys, cond in CONDITION_WORDS:
            found = next((k for k in keys if k in text), None)
            if found:
                condition, cond_word = cond, found
                break
        size = re.search(r"(\d{2})\s*(?:-|\s)?\s*(?:inch|in\b|\")", text)
        brand = next((b for b in BRANDS if b in tokens), None)
        tags = [t for t in [best[1].lower() if best else None, brand, f"{size.group(1)}-inch" if size else None,
                            cond_word] if t]
        confidence = round(min(0.95, 0.45 + 0.25 * hits + (0.1 if cond_word else 0) + (0.05 if brand else 0)), 2) \
            if best else 0.2
        why = [f"keyword match for {best[0]} / {best[1]}"] if best else ["no known keywords"]
        why.append(f"'{cond_word}' suggests condition {condition}" if cond_word
                   else "no condition words found, defaulted to Fair")
        return AIResult(content={"category_id": cat_id, "condition": condition, "tags": tags,
                                 "category_label": f"{best[0]} / {best[1]}" if best else "Unknown"},
                        confidence=confidence, explanation="; ".join(why))


class ClassificationService:
    def __init__(self, db, facade=None):
        self.db = db
        self.facade = facade or AIFacade(db)

    def classify(self, name, description):
        cats = [{"id": r["category_id"], "name": r["name"], "subcategory": r["subcategory"]}
                for r in self.db.execute("SELECT * FROM category")]
        return self.facade.request(ClassifyFeature({"name": name, "description": description, "categories": cats}))
