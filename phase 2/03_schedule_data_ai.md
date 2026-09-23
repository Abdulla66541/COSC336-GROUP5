# 7. Schedule Feasibility

## 7.1 Capacity against the Phase 1 timeline

Phase 1 Section 7.2 sets eight phases, but gives Phases 7 and 8 the same submission week. To test that plan, this study assumes **four students can each contribute six focused project hours per week**, including writing, coding, review and integration. The figures below are planning estimates, not recorded times or guaranteed availability. The first two rows describe completed or current documentation work; the remaining rows test the time left for delivery. Phase 8 has no separate duration in Phase 1, so its work shares Phase 7's week rather than receiving another week of capacity.

| Phase and deliverable | Phase 1 duration / submission week | Estimated team capacity | Estimated effort | Assessment |
|---|---|---:|---:|---|
| 1. Initial plan and requirements | 1 week / Sep 14 | 24 h | 20 h | Reference baseline; actual hours were not recorded. |
| 2. Feasibility document | 1 week / Sep 21 | 24 h | 22 h | Tight once individual review and PDF assembly are included. |
| 3. Requirements document | 2 weeks / Oct 5 | 48 h | 40 h | 8 h of estimated room for changes. |
| 4–5. Architecture and detailed design | 3 weeks / Oct 26 | 72 h | 66 h | Only 6 h of room; data schema and role rules must be settled early. |
| 6. Draft implementation | 3 weeks / Nov 16 | **96 h with a temporary increase to 8 h/person/week** | 90 h | Six h of room even with increased availability. At the normal 6 h rate, capacity is 72 h and the shortfall is 18 h. |
| 7. Test cases | Shared week / Nov 23 | 24 h shared with Phase 8 | 18 h | Cannot be scheduled as a separate full week. |
| 8. Final project and demonstration | Same week / Nov 23 | **No additional capacity** | 24 h | Combined Phases 7–8 need 42 h against 24 h normally available: an 18 h shortfall. |

**Recovery plan:** prepare at least 18 h of test-case writing, regression checks, report templates and demo material during Phases 4–6; then the remaining 24 h of final-week work fits the normal four-person week. This is an allocation target, not spare time already available: earlier phases have little slack. Implementation also requires each member to commit roughly two extra hours per week during Phase 6. If that availability cannot be confirmed, the team must reduce implementation effort by at least 18 h while retaining every Must requirement in a demonstrable form.

## 7.2 Dependencies and schedule controls

The critical sequence is **Phase 3 requirements → data schema and permissions in Phases 4–5 → asset/request workflow and AI integration in Phase 6 → tests and demonstration**. Dataset definitions, category names and role permissions must be agreed before building the AI functions; changing them late would also require updating test data, prompts and reports. The prototype depends on team laptops, GitHub access and an available free AI service or local model, but has no dependency on live KU systems. If an API is unavailable, local keyword search, fixed classification rules, rule-based sustainability advice and standard reports keep the core workflows demonstrable; AI-dependent criteria must still be shown separately and any missing AI capability reported honestly.

The team should finish a small end-to-end path first: create an asset, search and request it, approve a transfer, record its history and produce a basic report. AI suggestions can then be attached to that path. Agree on one shared dataset and API contract in the design phase, integrate each feature as it is completed, and write tests alongside implementation rather than starting them in Phase 7. Review progress against the hours above weekly; a missed schema agreement or a Phase 6 feature still unintegrated at the midpoint triggers reassignment and a simpler implementation of the same Must requirement. Advanced analytics and external integration are already marked Could in Phase 1 Section 5.3 and receive no time allocation.

**Schedule verdict:** feasible for a local prototype **if** the team confirms the extra Phase 6 hours, completes at least 18 h of final-week preparation earlier, and limits each Must requirement to a small, testable workflow. It is not feasible on the baseline six-hour weekly assumption alone without those adjustments.
