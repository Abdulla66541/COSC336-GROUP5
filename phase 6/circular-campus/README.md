# Circular Campus: Phase 6 Draft Implementation

COSC 336, Group 5. A working prototype of the Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System. It follows the Phase 4 & 5 design and the Phase 6 work distribution.

## Who built what

| Member | Folder | Core features | AI features |
|---|---|---|---|
| **Mohammed Al Ali** | `app/mohammed_al_ali/` | C2 Departments and assets · C3 Publish and search · C4 Request and track | AI 1 Classification and tagging |
| **Mubarak** | `app/mubarak/` | C5 Approve and transfer · C6 States and history | AI 3 Sustainable-action advice |
| **Mohammed Alketbi** | `app/mohammed_alketbi/` | C1 Login and roles · C8 Notifications · C9 Basic report | AI 4 Assistant |
| **Abdulla** | `app/abdulla/` | C7 Sustainability dashboard | AI 2 Matching and ranking · AI 5 Generated report |
| Shared setup | `app/` (top level) | App start-up, database schema from the ER diagram, demo data, page layout | Shared AI layer lives in `app/abdulla/ai_core.py` |

Each member folder contains that person's services (classes from their class diagram), `routes.py` (their pages and URLs), `templates/` (their HTML) and a test file in `tests/test_<name>.py`.

## Implementation environment

| Item | Choice |
|---|---|
| Language | Python 3.8+ |
| Web framework | Flask (one blueprint per member) |
| Database | SQLite, tables from our ER diagram (`app/schema.sql`) |
| Interface | HTML, CSS, Bootstrap 5 (loaded from a CDN, so the demo needs internet for styling) |
| AI features | LLM API through `LlmAdapter`, with a rule-based fallback |
| Code sharing | GitHub, one folder per member |

## Run it

```bash
cd "phase 6/circular-campus"
pip install -r requirements.txt
python run.py            # open http://127.0.0.1:5000
python -m pytest -q      # 69 automated tests
```

On first run the database is created in `instance/` with synthetic demo data. To reset it, delete the `instance/` folder.

**To use a real language model**, set `AI_API_KEY` (and optionally `AI_BASE_URL` and `AI_MODEL`) for any OpenAI-compatible API before `python run.py`. Without a key, every AI feature uses its rule-based fallback, so the demo always works offline.

**Demo accounts** (password `Password123!` for all of them):

| Email | Role | Department |
|---|---|---|
| admin@campus.test | Administrator | Library |
| sara.rep@campus.test | Department Representative (approver) | Engineering |
| omar.rep@campus.test | Department Representative (approver) | Computer Science |
| khalid@campus.test | Asset Custodian | Engineering |
| mona@campus.test | Asset Custodian | Computer Science |
| hessa@campus.test | Requester | Biology |
| ali@campus.test | Requester | Computer Science |

## Demo script (about 6 minutes)

1. **Mohammed Alketbi (C1):** log in as each role and show that the menus differ. As hessa, try opening `/approvals`: the server refuses with 403.
2. **Mohammed Al Ali (C2, C3, AI 1):** as khalid, register an asset "HP laptop, cracked screen" → **✨ Suggest** → Accept → Register → Publish. Then search the marketplace by keyword, category and condition.
3. **Mohammed Al Ali (C4) and Abdulla (AI 2):** as hessa, request "Chair" ×4 → the AI shows matches with score and reason → Accept & reserve.
4. **Mubarak (C5, C6):** as sara.rep, approve it (try it as omar.rep first: refused). As khalid, schedule the handover. As hessa, confirm receipt: owner and department change only now. Open the asset to show its full history.
5. **Mubarak (AI 3):** as khalid, open the broken projector → **✨ AI advice** → Repair, with reasons.
6. **Mohammed Alketbi (C8, C9, AI 4):** show the 🔔 notifications. As hessa, open ✨ Assistant and ask "Which chairs are available in Engineering?", then "Approve my transfer" (it refuses). As admin, open Manage → Report and export CSV.
7. **Abdulla (C7, AI 5):** as admin, open the Sustainability dashboard, then **Generate AI report**. Export is disabled until someone marks the report reviewed.

## AI layer (shared)

`AIFacade` → `PrivacyFilter` → `LlmAdapter` → answer check. The rule-based fallback is used when there is no API key, on a timeout or error, or when the answer is invalid or low-confidence. Each AI feature is an `AIFeature` subclass in its owner's folder, carrying its own prompt, answer check and fallback rules. Every output is stored in `AI_OUTPUT`, and every edit or rejection in `AI_OVERRIDE` (BR-12). The AI never approves, transfers or disposes of anything (BR-11).

## Known limitations (for the Phase 7 and 8 reports)

- The fallback matching uses keyword overlap with simple plural handling, not true semantic embeddings.
- **The emission factors and weights in `app/seed.py` are illustrative placeholders. Replace them with cited figures before the final report.**
- The Finance Officer sign-off for assets over AED 5,000 (BR-09) is recorded by the admin. There is no separate finance role yet.
- There is no CSRF protection and no email channel. This is a prototype for local demo only, with synthetic data.
- Bootstrap loads from a CDN. Without internet the pages still work, but without styling.
