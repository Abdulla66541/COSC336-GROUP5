"""Shared AI layer (owner: Abdulla). Design doc section 2.4, Part 4 class diagram.

Every AI feature calls the facade the same way:

    AIFacade(db).request(feature)

where `feature` is an AIFeature that carries its own prompt, answer check
and rule-based fallback. Flow:

    PrivacyFilter -> LlmAdapter (only if AI_API_KEY is set)
                  -> feature.is_valid + confidence check
    FallbackService path if: no key, timeout/error, invalid or low-confidence answer
    AIOutputLogger saves every result in AI_OUTPUT

The AI only suggests. A person always accepts, edits or rejects (BR-11, BR-12).
"""
import json
import os
import re
import urllib.request
from dataclasses import dataclass, field

from app.db import now

LOW_CONFIDENCE = 0.5


@dataclass
class AIResult:
    content: dict
    confidence: float
    explanation: str
    model_id: str = "rules"
    model_version: str = "1.0"
    prompt_version: str = "fallback-v1"
    used_fallback: bool = True
    output_id: int = None
    extra: dict = field(default_factory=dict)


class AIFeature:
    """Base class for one AI feature. Each owner writes a subclass."""
    name = ""                 # stored in AI_OUTPUT.function_name
    prompt = ""               # sent to the model; {data} is replaced with JSON
    prompt_version = "v1"

    def __init__(self, data, asset_id=None, request_id=None):
        self.data = data
        self.asset_id = asset_id
        self.request_id = request_id

    def is_valid(self, content: dict) -> bool:
        return True

    def fallback(self) -> AIResult:
        raise NotImplementedError


class PrivacyFilter:
    """Removes personal data before anything is sent to an outside model."""
    EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
    PHONE = re.compile(r"\+?\d[\d\s-]{7,}\d")
    PERSONAL_KEYS = ("requester_name", "custodian_name", "email", "user_id", "requester_id", "custodian_id",
                     "password_hash", "actor_name")

    def remove_personal_data(self, data):
        if isinstance(data, str):
            return self.PHONE.sub("[phone]", self.EMAIL.sub("[email]", data))
        if isinstance(data, dict):
            return {k: self.remove_personal_data(v) for k, v in data.items() if k not in self.PERSONAL_KEYS}
        if isinstance(data, list):
            return [self.remove_personal_data(v) for v in data]
        return data


class LlmAdapter:
    """Calls any OpenAI-compatible chat API. Set AI_API_KEY (and optionally
    AI_BASE_URL, AI_MODEL). Without a key, every feature uses its fallback."""

    def __init__(self):
        self.api_key = os.environ.get("AI_API_KEY")
        self.base_url = os.environ.get("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.model_id = os.environ.get("AI_MODEL", "gpt-4o-mini")
        self.timeout_seconds = 15

    @property
    def enabled(self):
        return bool(self.api_key)

    def send(self, feature: AIFeature, clean_data) -> AIResult:
        system = ("You help a university asset-exchange system. Reply ONLY with one JSON object. "
                  "Use only the data given. Never invent numbers. If unsure, set confidence low.")
        body = json.dumps({
            "model": self.model_id,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": feature.prompt.replace("{data}", json.dumps(clean_data, default=str))}],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }).encode()
        req = urllib.request.Request(f"{self.base_url}/chat/completions", data=body, headers={
            "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
            out = json.loads(json.loads(resp.read())["choices"][0]["message"]["content"])
        return AIResult(content=out, confidence=float(out.get("confidence", 0)),
                        explanation=out.get("explanation", ""), model_id=self.model_id,
                        model_version=self.model_id, prompt_version=f"{feature.name}-{feature.prompt_version}",
                        used_fallback=False)


class AIOutputLogger:
    def __init__(self, db):
        self.db = db

    def save(self, feature, result):
        cur = self.db.execute(
            "INSERT INTO ai_output (function_name, asset_id, request_id, model_id, model_version, prompt_version,"
            " confidence, content, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (feature.name, feature.asset_id, feature.request_id, result.model_id, result.model_version,
             result.prompt_version, result.confidence,
             json.dumps({"content": result.content, "explanation": result.explanation}, default=str), now()))
        result.output_id = cur.lastrowid
        return result

    def override(self, ai_output_id, user_id, final_value, reason=None):
        """BR-12: every edit or rejection of an AI suggestion is logged."""
        if not self.db.execute("SELECT 1 FROM ai_output WHERE ai_output_id=?", (ai_output_id,)).fetchone():
            return
        self.db.execute("INSERT INTO ai_override (ai_output_id, user_id, final_value, reason, created_at)"
                        " VALUES (?,?,?,?,?)", (ai_output_id, user_id, final_value, reason, now()))

    def feedback(self, ai_output_id, user_id, rating, comment=None):
        if not self.db.execute("SELECT 1 FROM ai_output WHERE ai_output_id=?", (ai_output_id,)).fetchone():
            return
        self.db.execute("INSERT INTO ai_feedback (ai_output_id, user_id, rating, comment) VALUES (?,?,?,?)",
                        (ai_output_id, user_id, rating, comment))


class AIFacade:
    def __init__(self, db, adapter=None):
        self.db = db
        self.privacy = PrivacyFilter()
        self.adapter = adapter or LlmAdapter()
        self.logger = AIOutputLogger(db)

    def request(self, feature: AIFeature) -> AIResult:
        result = None
        if getattr(self.adapter, "enabled", False) and feature.prompt:
            try:
                result = self.adapter.send(feature, self.privacy.remove_personal_data(feature.data))
                if not feature.is_valid(result.content) or result.confidence < LOW_CONFIDENCE:
                    result = None
            except Exception:      # timeout, network error, bad JSON -> fallback (design 2.4)
                result = None
        if result is None:
            result = feature.fallback()
            result.prompt_version = f"{feature.name}-fallback-v1"
        return self.logger.save(feature, result)


STOP = {"a", "an", "the", "for", "and", "or", "of", "with", "to", "in", "on", "need", "needs", "our", "we",
        "x", "is", "are", "at", "lab", "please", "some", "new", "used", "any", "there", "what", "which", "how",
        "do", "does", "can", "i", "me", "my", "it", "be", "have", "has", "available", "show", "list", "find"}


def words(text):
    """Lower-case content words, used by the rule-based fallbacks."""
    return {w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if w not in STOP and len(w) > 1}


def stem(w):
    """Very small plural stemmer: monitors -> monitor, boxes -> box, shelves -> shelf."""
    if len(w) > 4 and w.endswith("ves"):
        return w[:-3] + "f"
    if len(w) > 4 and w.endswith(("ches", "shes", "xes", "sses")):
        return w[:-2]
    if len(w) > 3 and w.endswith("s") and not w.endswith(("ss", "us", "is")):
        return w[:-1]
    return w


def stems(text):
    return {stem(w) for w in words(text)}
