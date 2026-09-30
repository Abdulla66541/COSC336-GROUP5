# Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System

## Phase 2 – Feasibility Document

**Khalifa University – Department of Computer Science**

**COSC 336 – Introduction to Software Engineering – Fall 2026**

**Prepared by:** Group 5 – Mohammed Alketbi (100067035), Abdulla, Mohammed Al Ali, Mubarak

**Prepared for:** Eng. Dina Atia, Lab Instructor

**Date:** September 2026



---

# 1. Introduction

## 1.1 Purpose of this Study

Phase 1 defined what we want to build. This document asks a different question: can we actually build it, with four students, one semester, no budget and no access to real university data — and is it worth building at all?

A feasibility study exists to support a go/no-go decision before serious design and development effort is committed. It examines the project from several angles — market, technical, financial, operational, schedule, data and AI, and legal — and for each one asks whether the project is achievable and under what conditions. The output is a recommendation, not a description.

## 1.2 Project Recap

The proposed system is an internal web platform for Khalifa University that registers campus assets, publishes surplus items to an internal marketplace, lets departments request and reserve them, manages approvals and transfers, records the full life cycle of each asset, and adds an AI layer for semantic matching, classification, sustainability recommendations, a natural-language assistant and generated reports. The full scope, stakeholders and initial requirements are in the Phase 1 document (`docs/phase1/Phase1_Final.md`) and are not repeated here.

## 1.3 How this Document is Organised

Sections 2 and 3 set the context (stakeholders and existing solutions). Sections 4 to 9 assess feasibility dimension by dimension: technical, financial, operational, schedule, data and AI, and legal/policy. Section 10 consolidates the risks, and Section 11 gives the recommendation and the action plan for Phase 3.

# 2. Stakeholder Summary

Phase 1 identified eleven stakeholder groups and mapped them to features, data and permissions. For the feasibility study, what matters is each group's main interest and the condition under which the system is feasible *for them*.

| Stakeholder | Main interest | Feasibility condition |
|---|---|---|
| Department representatives | Get needed equipment quickly without a purchase request | Search and request must be faster than emailing procurement |
| Asset custodians | Keep records accurate with minimal extra work | Registration must be quick; AI classification must reduce typing, not add review burden |
| Requesters | Find items that fit their need | Matching must return relevant results, not noise |
| Administrators | Clear, auditable approvals | Approval rules must be explicit and enforced by the system, not by AI |
| Procurement officers | Avoid unnecessary purchases | Surplus must be visible at the moment a purchase is considered |
| Finance officers | Trustworthy savings figures | Every estimate must show its assumption |
| Maintenance staff | One place for repair history | History must follow the asset across transfers |
| Sustainability officers | Reportable indicators | Waste-diversion and CO₂ estimates must be explainable and labelled as estimates |
| System administrators | Security and low maintenance | Standard stack, role-based access, audit log |
| Instructors (client) | Evidence of process and learning | Regular commits, documented decisions, honest limitations |
| Group 5 (developers) | Deliverable within the semester | Scope limited to Must requirements; free tools only |

The common thread is that feasibility depends less on technology and more on keeping the workflow simpler than the current informal process. If using the system takes longer than sending an email, nobody will use it.

# 3. Market Analysis

## 3.1 Existing Solutions

Asset management is a mature software category, so the first question is whether something already does what we propose. We looked at four types of existing solution.

**Enterprise asset management (EAM) suites** such as SAP EAM and IBM Maximo are built for large organisations. They track ownership, location, purchase value, depreciation and maintenance schedules in depth, and integrate with finance and procurement. They are expensive to licence and implement, are designed around compliance and accounting rather than reuse, and do not include an internal marketplace or semantic matching between surplus and demand.

**IT asset management (ITAM) tools** such as ServiceNow ITAM and Asset Panda focus on hardware and software inventory, check-in/check-out and audits. They are strong on tracking and reporting but again treat an asset as something to be accounted for, not something to be redistributed. Cross-department reuse is not a native workflow.

**Open-source asset registers** such as Snipe-IT provide free inventory tracking with roles, custody assignment, maintenance logs and audit history. They prove that the classic layer of our system is standard, well-understood functionality that a small team can implement. They have no request/matching workflow, no sustainability metrics and no AI.

**University surplus and reuse programmes.** Some universities run internal "surplus property" web pages or use platforms such as Warp It (UK) to list unwanted furniture and equipment for other departments to claim. These are the closest match to our idea. They typically work as simple listings with manual search; matching depends on the requester browsing, categories are fixed, and impact reporting (avoided purchases, waste diverted) is either manual or absent.

## 3.2 Comparison

| Solution type | Asset register | Internal marketplace | Semantic / AI matching | Sustainability metrics | Cost for KU |
|---|---|---|---|---|---|
| EAM suites (SAP, Maximo) | Yes, deep | No | No | Partial (depreciation, not reuse) | High licence + implementation |
| ITAM tools (ServiceNow, Asset Panda) | Yes | No | No | No | Subscription per asset/user |
| Open-source registers (Snipe-IT) | Yes | No | No | No | Free, self-hosted |
| University surplus sites / Warp It | Basic listing | Yes, manual | No (keyword only) | Basic counts, often manual | Subscription or in-house |
| **Proposed system** | Yes | Yes | Yes, with explanations | Yes, estimated and labelled | Free tools (prototype) |

## 3.3 Conclusion

No existing solution combines an asset life-cycle register, an internal reuse marketplace, meaning-based matching between supply and requests, sustainability recommendations and generated impact reporting. The pieces exist separately, which is reassuring for feasibility — the classic layer is proven technology — but the combination, and the AI layer in particular, is where the project adds value. The market gap is real, and it is also exactly the gap the course project is designed to explore: a conventional system extended with AI where AI is useful.
# 4. Technical Feasibility

## 4.1 Proposed Architecture

The system will use a simple layered architecture, which is the most common and best-understood pattern for a web application of this size:

- **Presentation layer** – a web front-end for all roles (forms for registration and requests, search and filter pages, approval screens, dashboards, the assistant chat window).
- **Application layer** – business logic: validation, approval workflows, state changes (asset states, request states, transfer states), notifications, role checks.
- **AI and analytics layer** – classification, semantic matching and ranking, sustainability recommendation, LLM assistant and report generation. Every function in this layer returns a recommendation plus a confidence level and an explanation, never a final decision.
- **Data layer** – a relational database for users, departments, assets, categories, requests, matches, approvals, transfers, maintenance records, sustainability impacts, notifications, model versions and audit logs, plus a vector index for asset and request embeddings.

The AI layer is deliberately separated so that if an AI service is unavailable, the application layer falls back to keyword search and rule-based recommendations and the system keeps working.

## 4.2 Proposed Technology Stack

| Component | Proposed choice | Why it is feasible |
|---|---|---|
| Back-end | Python with FastAPI (or Flask) | Team has Python experience from earlier courses; fast to build APIs; excellent AI library support |
| Front-end | HTML/CSS/JavaScript, optionally React | Standard web skills; no build tooling required for the simple option |
| Database | SQLite for development, PostgreSQL for the demo | Free, relational, well documented; PostgreSQL supports pgvector for embeddings |
| AI – embeddings and LLM | Free-tier LLM API (e.g. an OpenAI/Gemini/Groq student or free tier) or an open-source model run locally (e.g. via Ollama) | Zero cost within quota; embeddings give semantic similarity; prompts with a fixed category list give classification |
| Vector search | pgvector, or in-memory cosine similarity for the prototype dataset | Dataset is small (hundreds of items), so no specialised infrastructure is needed |
| Authentication | Local username/password with hashed passwords and role table | No dependency on KU identity systems |
| Version control | Git + GitHub | Required by the course; already set up |
| Diagrams and design | draw.io / PlantUML | Free |
| Hosting | Local machines for the demo; free-tier cloud (e.g. Render, Railway) optional | No budget needed |

## 4.3 Integration

The prototype integrates with no external university systems. Authentication, department lists and asset data are local. The only external dependency is the AI API, which is isolated behind the AI layer with a fallback. This removes the biggest technical risk in most enterprise projects — integration with legacy systems — at the cost of realism, which is acceptable for a prototype and stated as a limitation.

## 4.4 Team Skills versus Required Skills

| Skill needed | Current level in team | Gap and plan |
|---|---|---|
| Python web development | Intermediate | None significant; FastAPI documentation is enough |
| Relational database design | Intermediate (from database course) | None; ER modelling is part of Phase 5 |
| Front-end (HTML/CSS/JS) | Basic to intermediate | Keep the UI simple; use a CSS framework (e.g. Bootstrap) to save time |
| Calling an LLM/embedding API | Basic | Short self-study in Phase 3; one member (Design and AI lead) builds a small proof of concept early |
| Prompt design for classification and explanation | Basic | Iterate with the synthetic dataset in Phase 6; keep prompts in version control |
| Git/GitHub | Basic, improving | Already operational after Phase 1 |
| Testing (unit/integration) | Basic | Learn pytest basics; testing plan in Phase 7 |

The only real gap is practical AI integration, and it is a bounded one: calling an embeddings endpoint, computing cosine similarity and prompting an LLM with a fixed set of categories are well-documented tasks. Building a small proof of concept before Phase 4 will confirm this and remove the uncertainty early.

## 4.5 Hardware and Software Requirements

Development needs only the team's laptops, a modern browser, Python 3, VS Code, Git and internet access for the AI API. Demonstration can run on one laptop. No servers, licences or special hardware are required.

## 4.6 Technical Verdict

**Technically feasible.** The classic layer uses standard, proven technology that the team already knows. The AI layer is achievable with free-tier services and a small dataset, provided that:

1. a proof of concept for embeddings-based matching and LLM classification is completed before the design phase;
2. the AI layer is isolated behind an interface with a rule-based fallback;
3. the UI is kept simple and scope is limited to the Must requirements from Phase 1.

The main technical risks — API quota, prompt quality on synthetic data and the team's limited AI experience — are addressed in Sections 8 and 10.

# 5. Financial (Economic) Feasibility

The financial feasibility analysis is used to determine if the proposed system can be developed with the resources that are available to the project team and if the benefits of the proposed system are worth the cost.

The direct monetary cost for the prototype for the semester is expected to be minimal since it will be developed by four students with existing laptops, university facilities, GitHub, free development tools, and free tier services.

## 5.1 Development and Infrastructure Cost

For planning purposes, the team assumes approximately 120 hours of work per member during the semester.

| Item | Estimate |
|---|---:|
| Team members | 4 |
| Estimated effort per member | 120 hours |
| Total estimated effort | 480 student-hours |
| Direct student labour cost | 0 AED |
| GitHub | 0 AED |
| Development tools | 0 AED |
| Database | 0 AED initially |
| Web hosting | 0 AED initially |
| AI services | 0 AED initially |

The 120-hour estimate is a planning assumption rather than a measured value.

The prototype can use mainly free tools and services. However, free tiers may include limits on storage, requests, tokens, processing time, or inactivity. If those limits are reached, the team can reduce usage, use local tools, or move to another suitable free alternative.

## 5.2 Long-Term Cost

Other costs would likely be introduced if the system would be adopted by Khalifa University in the future.

Possible costs include:

- production hosting;
- data security and recovery;
- cybersecurity and monitoring;
- technical support;
- software maintenance;
- AI application development;
- user training; and
- integration with existing University systems.

The costs cannot currently be precisely determined due to the fact that the number of future users, the level of use of the system and the requirements for the production infrastructure are still unknown.

## 5.3 Expected Financial Benefits

The primary anticipated financial gain is the avoidance of unnecessary purchases through the reuse of resources that are already available in the university.

Other potential benefits are:

- reducing duplicate purchases;
- reducing the number of assets required; and
- making repairs rather than replacements of appropriate assets;
- lowering the costs of disposal and storage; and
- saving manpower hours in finding resources.

Studies on university reuse programmes indicate that the costs of procurement and disposal can be reduced through internal redistribution. The savings of other universities are not necessarily a reliable indicator of Khalifa University's savings.

## 5.4 Illustrative Cost-Saving Example

The project team cannot access Khalifa University's actual procurement data at this time, and an accurate savings estimate cannot be determined.

As an example, the team estimates that it is possible to re-use 5% of the equipment it buys.

Suppose that the annual expenditure on equipment was hypothetically AED 500,000:

**0.05 × 500,000 AED = 25,000 AED**

This would be equivalent to 25,000 AED in foregone purchases.

This is an indicative example only and not an actual expenditure or savings made by Khalifa University.

## 5.5 Cost-Benefit Summary

| Area | Cost / Benefit | Assessment |
|---|---|---|
| Student development | 480 student-hours | Significant effort but no direct salary cost |
| Development tools | Very low | Free/open-source tools available |
| Hosting and database | Very low | Free-tier or local options available |
| AI services | Low but uncertain | Depends on free-tier limits |
| Avoided purchases | Potential benefit | Depends on actual reuse |
| Asset-life extension | Potential benefit | May delay replacement |
| Reduced disposal/storage | Potential benefit | Depends on actual use |
| Production maintenance | Unknown | Requires future analysis |

## 5.6 Financial Feasibility Verdict

The project is economically viable to be a prototype for a semester, since it can be created primarily by using existing hardware and free or low-cost services.

It is not possible to calculate an ROI at the production level at this time without actual University procurement, maintenance, hosting, and usage data.

The direct monetary cost of the prototype is low, so that even if a few purchases are avoided, the direct cost of the prototype can be more than the direct cost of the purchase.


# 6. Operational Feasibility

Operational feasibility is the assessment of the viability of the system to the intended users and adopters.

The key stakeholders are the department representatives, asset custodians, requesters, administrators, procurement officers, finance officers, maintenance staff, and sustainability officers.

## 6.1 Stakeholder Adoption

| Stakeholder | Possible Issue | Mitigation |
|---|---|---|
| Department Representatives | Reluctance to release assets | Keep ownership and approval decisions under human control |
| Asset Custodians | Extra data-entry work | Use simple forms and AI-assisted classification |
| Requesters | Distrust of AI recommendations | Explain recommendations and keep normal search available |
| Administrators | Too many approval steps | Use clear and simple workflows |
| Procurement Officers | Reuse checks may slow purchasing | Make internal search and matching quick |
| Finance Officers | Savings estimates may be unclear | Separate confirmed values from estimates |
| Maintenance Staff | Extra recording work | Keep maintenance forms short and simple |
| Sustainability Officers | Environmental estimates may be uncertain | Clearly explain assumptions |

## 6.2 Main Operational Challenges

Key challenges in operation are that of data entry, reluctance to share assets across departments, slow approval, inaccurate asset details, lack of trust in AI suggestions, and reluctance to alter current workflows.

Simple interfaces, straightforward approval processes, easy-to-understand AI explanations, accurate status tracking, and human oversight of critical decisions can help mitigate these challenges.

## 6.3 Training and Change Management

Users should be given short training based on the role they are assigned to, depending on the tasks they do.

Training should include:

- gathering information; and
- updating asset information;
- reviewing approvals;
- recording maintenance activities;
- understanding financial and sustainability indicators; and
Awareness of the limits of AI suggestions.

The system should also be clear that AI is a tool for decision making and not a substitute for decisions made by authorised personnel.

Feedback should be gathered while testing to make sure that confusing or inefficient workflows can be improved.

## 6.4 Operational Feasibility Verdict

If: The proposed system is operationally feasible;

1. Data entry is easy and efficient;
2. approval and ownership decisions are still under approved human control; and
3. users are provided with the necessary training and guidance.

If so, the proposed workflows should be feasible for the intended users and appropriate for further development.

# 6. 



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

# 8. Data and AI Feasibility

## 8.1 Data availability and test dataset

Phase 1 Sections 3.4 and 3.7 rule out real university data and live KU integrations. Accordingly, this feasibility claim concerns a **synthetic prototype**, not operational deployment or proof of university-wide savings. We can create a reproducible dataset of **120 assets across eight categories and four fictional departments; 40 requests; 20 inspection/maintenance records; 15 approved or rejected transfer histories; and 12 simulated procurement comparisons**. These counts are proposed test targets, not records that already exist. Each asset needs an ID, name, description, category, quantity, owning department, location, purchase date/value, condition and availability; optional sample photos or documents must be non-sensitive. Requests need purpose, specifications, quantity, preferred condition, urgency, required location/date and status. Inspection and transfer records need linked IDs, dates, decisions, actors represented by fictional accounts and before/after status. Procurement comparisons need an assumed replacement price and explicit outcome so reports never mistake a suggested match for an avoided purchase. These fields map to Phase 1 Section 6, especially REQ-01–24 and REQ-44–47.

Create the dataset from a fixed random seed plus hand-written realistic cases. Include synonym pairs ("lab stool"/"laboratory seating"), near misses (wrong dimensions or quantity), unavailable or damaged assets, conflicting department names, missing optional descriptions, duplicate IDs and rejected transfers. Keep a clean reference version and a separate flawed test version so validation can be measured without silently repairing all errors. Team members should review examples for plausibility; fabricated records must be labelled synthetic throughout the interface and reports.

| Data type | Availability, completeness and consistency check | Privacy and consequence for feasibility |
|---|---|---|
| Assets and requests | Generated locally; require IDs, categories, quantity, condition and status; validate positive quantities, shared category vocabulary and compatible units. Optional text may be incomplete, reducing match quality. | Use fictional departments/users and generic locations. No real inventory or identities. |
| Inspections and maintenance | Simulate defect, inspection date, action and cost where known; link each event to an existing asset and preserve chronological order. Missing cost must remain unknown, not zero. | Avoid real equipment identifiers and safety claims. Unknown condition should require human inspection. |
| Transfers and approvals | Record request, asset, approval actor/decision, custody and timestamps; reject transfers from unavailable assets or without authorized approval. | Fictional actors; role restrictions and audit history still need testing. |
| Procurement and impact estimates | Simulated replacement prices and comparison events only; clearly distinguish requested, matched, approved and actually reused assets. Emissions factors must be sourced or presented as illustrative assumptions. | No real purchasing or finance records; estimated savings and CO₂ cannot be reported as KU outcomes. |

Local schema checks, required-field rules and referential checks can establish completeness and internal consistency of the sample. They **cannot establish representativeness** of KU inventory, genuine user behaviour, purchase prices or environmental impact. A synthetically clean dataset may make AI performance look better than it would in practice, so the flawed test cases should be included in evaluation and results labelled “on synthetic test data.”

## 8.2 Feasibility of the five AI functions

The baseline must work with free or locally available tools and no model training from scratch. A free API is an option, not an assumed guaranteed quota; service limits and terms need checking when a provider is chosen. Use local embeddings where possible, and only send fabricated, minimal records to any external service. Phase 1 Section 5.3 marks all five functions Must, so each needs a demonstrable implementation and an explicit failure path.

| AI function and Phase 1 requirement | Small feasible implementation | What to evaluate and show to the user | Failure path and limitation |
|---|---|---|---|
| Semantic matching (REQ-29–32) | Embed request and asset descriptions, rank by similarity, then filter on availability, quantity and essential specifications. A local vector comparison is sufficient for 120 assets. | On hand-labelled request/asset pairs, record whether useful candidates appear in the top three; show matched words/specifications, unmet constraints and a **relative similarity score**, not a probability of correctness. Phase 1's 70% usefulness target needs user ratings or a clearly labelled proxy. | Keyword/filter search remains available. Similar text cannot prove physical compatibility; users accept or ignore suggestions. |
| Asset classification (REQ-33–35) | Prompt a free or local LLM to choose **only** from the fixed eight-category list; validate its output against that list. | Compare suggestions with hand-labelled categories; show category, reason and a low-confidence/needs-review flag when the output is invalid or ambiguous. User confirms or corrects it. | Default to manual category selection; do not save an unchecked suggestion. |
| Sustainability recommendation (REQ-36–39) | Apply explicit condition, inspection, availability and repair-cost rules first; optionally ask an LLM to explain the selected option in plain language. | Display input facts, rule used, missing evidence and the recommendation; test repairable, reusable, unsafe/unknown and end-of-life examples. | Show rule-based advice without LLM text. Missing inspection or cost means “requires review,” never an automatic disposal or safety decision. |
| LLM assistant (REQ-40–43) | Retrieve relevant rows from the local database using role-limited search, pass only those rows with the question to a model, and link the answer to returned asset IDs. | Test answer grounding, unauthorized-data queries, nonexistent assets and refusal to approve transfers. Show source record IDs and say when no evidence was found. | Offer ordinary search and status pages if the model is unavailable or cannot answer reliably. The assistant must not perform approvals. |
| Generative reports (REQ-44–47) | Calculate counts, reuse rates and estimated savings in code; pass aggregated figures to an LLM solely for a short narrative. | Check every figure against the underlying table and label assumptions and synthetic data. A user reviews before sharing. | Export the calculated table and a fixed-text summary if generation fails. An LLM must not invent quantities or emissions factors. |

Model-generated text does not come with a calibrated confidence probability. Therefore, the interface should use **“suggested,” “needs review,” or “no reliable result”** based on measurable rules, while showing similarity scores only as relative rankings. The team can report classification agreement, top-three matching relevance, hallucination counts and fallback success on its labelled synthetic cases; it cannot claim real-world accuracy from these results. Keep an audit of accepted and overridden suggestions so the prototype shows why human oversight matters.

**Data and AI verdict:** feasible as a synthetic-data demonstration of all five Must AI functions, provided the team freezes a common schema and category list early, evaluates known good and failure cases, and retains rule-based or manual paths whenever the AI service fails. It does not establish readiness to process KU data or to automate asset, procurement or safety decisions.

# 9. Legal, Ethical and Policy Constraints

The proposed system must consider legal, security, licensing, university-policy, safety, and ethical constraints. These constraints affect how the system collects data, controls access, uses AI services, and supports asset-management decisions. They do not prevent development of the prototype, but they must be considered throughout the system design.

## 9.1 Data Privacy

The system may process information relating to university users together with asset, request, transfer, inspection, and maintenance records. Some records could contain personal information such as names, university identifiers, contact information, departments, or records of actions performed by users.

The project must consider the UAE Federal Decree-Law No. 45 of 2021 concerning the Protection of Personal Data when personal data is processed.

During development and testing, the project will use synthetic data instead of real Khalifa University personal or operational data wherever possible. Synthetic data allows the team to create realistic asset records, requests, transfers, maintenance records, and user accounts without using information belonging to real students or staff.

The system should also minimise the amount of personal information processed. Information that is not required for a particular function should not be sent to an external AI service.

For example, an AI asset-matching request may require an asset category, description, quantity, condition, technical requirements, and location. It would normally not require the requester's real name, university ID, or contact information.

Khalifa University has a public website privacy policy that describes measures for protecting personal information collected through its website. However, the policy states that it applies to information collected online through the website. Therefore, a real deployment of this project would require confirmation of the university's applicable internal privacy, security, and data-handling requirements.

**Design response:** use synthetic data during development, minimise personal information, restrict access by role, and avoid sending unnecessary identifiable or confidential information to external AI services.

## 9.2 Security

The system will contain information about assets, users, requests, approvals, transfers, inspections, and maintenance activities. Unauthorized access or modification could result in incorrect records, unauthorized transfers, or loss of accountability.

The system should therefore use role-based access control. Each user should only be able to perform actions that are appropriate for their assigned role. For example, a requester may submit an asset request, while approval of a transfer should only be available to an authorised role.

Important actions should also be recorded in an audit trail. The audit trail should record information such as the user responsible for an action, the action performed, the affected asset or request, and the time of the action.

Authentication information should be protected, passwords should not be stored as plain text, and user input should be validated before it is processed or stored.

**Design response:** implement authentication, role-based permissions, protected credentials, input validation, and audit logging for important system actions.

## 9.3 Intellectual Property and Licensing

The project may use external software libraries, frameworks, databases, AI models, and APIs. These components may have different licences and terms of use.

Before using a third-party component, the team should check its licence and comply with any required conditions. The team should also keep a record of the important external libraries and services used in the project.

The project repository uses the MIT License. The MIT License allows the software to be used, modified, and distributed, provided that the required copyright and licence notice is retained.

The MIT License applied to the team's own project does not replace the licences or terms of third-party libraries, AI models, APIs, or datasets. Each external component remains subject to its own licence or terms.

If an external AI API is selected, its terms of service, usage limits, permitted uses, and data-handling conditions should be reviewed before integration.

**Design response:** document major third-party components, check their licences before use, retain required licence notices, and review the terms of external AI services before integrating them.

## 9.4 Procurement and Asset Ownership Rules

The system should support asset-management decisions rather than automatically make decisions that require university authorization.

Actions that affect asset ownership, custody, transfer, donation, disposal, or procurement should only be completed by users who have the appropriate authority. An AI recommendation should not automatically cause an asset to be transferred, donated, or disposed of.

For example, the system may recommend transferring an unused computer to another department, but the actual transfer should require approval from the appropriate authorised user.

The system should also maintain the history of important asset changes, including previous custody, locations, transfers, and approvals. This helps maintain accountability when responsibility for an asset changes.

The exact approval rules for a real Khalifa University deployment would need to be confirmed against the university's applicable procurement and asset-management procedures.

**Design response:** enforce role-based approval permissions, preserve asset history, and require authorised human approval for transfers, disposal, donation, procurement, and other important asset-management decisions.

## 9.5 Safety Constraints

Some university assets may require inspection or maintenance before they can safely be transferred or reused. This may be particularly important for laboratory equipment, electrical equipment, damaged assets, or equipment that requires calibration.

The system should not assume that every available asset is automatically safe or suitable for reuse. Asset condition, inspection status, and maintenance history should be considered before an item is transferred.

Where necessary, the system should allow an asset to be marked as requiring inspection, maintenance, or approval before the transfer is completed.

An AI recommendation should not be treated as proof that physical equipment is safe to use. Safety-sensitive decisions should remain under the control of appropriately qualified personnel.

**Design response:** record condition, inspection, and maintenance information, allow assets to be marked as requiring inspection, and keep safety-related approval under human control.

## 9.6 Ethical Use of AI

The project includes AI-based resource matching, AI-assisted asset classification, sustainability recommendations, an LLM-powered assistant, and generative AI reporting.

These functions may improve efficiency, but AI-generated results can be inaccurate, incomplete, biased, or difficult to explain. For example, an AI model may misunderstand a departmental request or recommend an asset that is not actually suitable.

AI outputs should therefore be presented as recommendations rather than guaranteed decisions. Where possible, the system should provide supporting information that helps the user understand a recommendation, such as category, condition, quantity, location, technical compatibility, or similarity score.

Important decisions should remain under human control. AI should not independently approve asset transfers, change ownership or custody, authorise disposal, or make procurement decisions.

Generative reports should be based on information available in the system. Important figures and conclusions should be supported by the underlying records rather than generated without evidence.

The team should also consider possible bias in AI recommendations. Testing should include different asset categories and request types so that the team can identify situations where the AI performs poorly.

If an AI service is unavailable or produces an unreliable result, essential system functions should still be usable without depending completely on AI.

**Design response:** use AI as decision support, maintain human oversight, provide supporting information where possible, test AI outputs, and provide non-AI fallback behaviour for essential functions.

## 9.7 Course AI Policy

AI functionality is a required part of the project. The system is expected to include AI-based resource matching, AI-assisted asset classification, sustainability recommendations, an LLM-powered assistant, and generative AI reporting.

The use of AI tools during the preparation of coursework and documentation is a separate issue and must follow the COSC 336 Assessment Details and any instructions provided by the instructor or lab engineer.

Each team member remains responsible for understanding and being able to explain the work submitted under their name.

**Design response:** implement the required AI functionality as part of the system while following the course rules concerning the use of AI tools during development and documentation.

## 9.8 Feasibility Conclusion

The identified legal, ethical, policy, security, licensing, and safety constraints do not prevent development of the proposed prototype.

The project is considered feasible provided that synthetic data is used during development where possible, personal information is minimised, external AI services are used carefully, third-party licences and terms are respected, role-based permissions are enforced, and important asset-management decisions remain under authorised human control.

A future deployment using real Khalifa University systems or operational data would require additional review of the university's applicable internal privacy, security, procurement, asset-management, and safety requirements.

# 10. Risk Assessment

The Phase 1 risk assessment identified several technical, schedule, data, and team-related risks. During the feasibility study, these risks are reviewed in more detail to determine how they could affect successful development of the system.

The table below includes both preventive mitigation actions and contingency plans. Mitigation describes what the team will do to reduce the chance or impact of a risk, while the contingency plan describes what the team will do if the risk actually occurs.

| Risk | Likelihood | Impact | Mitigation | Contingency Plan | Owner |
|---|---|---|---|---|---|
| Free-tier AI API quota is exhausted or the service becomes unavailable | Medium | High | Monitor API usage, minimise unnecessary calls, cache results where possible, and keep essential functions independent of AI. | Switch to another available free service or temporarily use rule-based/manual functionality so core system features continue working. | AI/Development Lead |
| Synthetic data is not realistic enough to evaluate the system properly | Medium | High | Create a dataset containing different asset categories, conditions, departments, requests, transfers, and maintenance records based on the Phase 1 requirements. | Expand or revise the synthetic dataset and add missing edge cases before final testing. | Requirements Lead |
| Team lacks enough experience with AI integration | Medium | High | Start AI experiments early, use simple approaches first, divide research between team members, and document successful examples. | Reduce AI complexity and implement a simpler solution such as basic embeddings, fixed prompts, or deterministic fallback rules. | AI/Development Lead |
| AI produces inaccurate or irrelevant recommendations | Medium | High | Test the AI using different asset and request examples, display supporting information, and keep humans responsible for final decisions. | Disable or limit the unreliable AI feature and use manual search, filters, or rule-based recommendations until it can be improved. | AI/Development Lead |
| Project scope becomes too large for the available time | Medium | High | Prioritise the Must-have requirements defined during requirements gathering and avoid adding unnecessary features. | Remove or postpone Should-have and Could-have features and concentrate development effort on the core system. | Project Coordinator |
| Phases 7 and 8 have deadlines in the same week | High | High | Begin testing before Phase 7, prepare test cases during implementation, and avoid leaving final integration until the last week. | Freeze new features, focus only on fixing critical defects, and divide testing, documentation, and presentation work between team members. | Project Coordinator / All Members |
| Phase 6 implementation takes longer than expected | Medium | High | Develop core functions incrementally during earlier phases and test individual components as they are completed. | Reduce lower-priority functionality and focus on completing a stable version of the Must-have features. | Development/Testing Lead |
| A team member becomes temporarily unavailable | Medium | Medium | Maintain documentation, use regular GitHub commits, and ensure more than one member understands important project components. | Reassign urgent tasks between available members and adjust lower-priority work if necessary. | Project Coordinator |
| GitHub conflicts, accidental deletion, or integration problems occur | Low | Medium | Commit frequently with meaningful messages, review changes before merging, and avoid editing the same section simultaneously. | Restore a previous Git version, resolve conflicts manually, and use commit history to recover lost work. | All Members |
| External software, library, or AI-service terms change | Low | Medium | Check licences and service terms before depending on an external tool and avoid unnecessary vendor-specific dependencies. | Replace the affected component with an alternative library, model, or service that meets the project requirements. | Development Lead |
| Sensitive information is accidentally included in AI requests | Low | High | Use synthetic data, minimise data sent to external services, and avoid including names, university IDs, or confidential information in prompts. | Stop sending affected data, remove it from test inputs where possible, review the integration, and change the application so only necessary non-sensitive fields are sent. | Development Lead |
| Insufficient time remains for complete testing | Medium | High | Begin unit and functional testing during development and prepare test cases before Phase 7. | Prioritise testing of Must-have functions and high-risk workflows such as authentication, approvals, transfers, and AI recommendations. | Development/Testing Lead |

## 10.1 Overall Risk Evaluation

The project contains several risks, but none of the identified risks currently make the proposed system infeasible.

The most important risks are the limited project schedule, dependence on free AI services, the quality of synthetic test data, AI accuracy, and the possibility that the planned scope becomes too large.

These risks can be controlled by keeping the Must-have requirements as the main development priority, testing AI functions early, maintaining non-AI fallback options, preparing realistic synthetic data, and beginning testing before the final project phases.

The team should review the risk table during each phase and update the likelihood, impact, mitigation, and contingency plans if project conditions change.

# 11. Recommendation and Action Plan

## 11.1 Overall Recommendation

Based on the feasibility analysis, the recommendation is to **proceed with the project, with conditions**.

The proposed Circular Campus Resource Exchange and Asset Life Cycle Management System is feasible as a student software-engineering project as long as the team keeps the scope controlled, prioritises the Must-have requirements, uses realistic synthetic data for development and testing, and avoids making the core system completely dependent on external AI services.

The classic asset-management functions should form the reliable foundation of the system. AI functionality should then be added where it provides clear value, such as resource matching, classification, sustainability recommendations, natural-language interaction, and report generation.

Important decisions such as transfer approval, disposal, changes in asset custody, and procurement-related actions should remain under authorised human control.

The team should therefore continue to Phase 3 while resolving the main technical, data, scope, and AI decisions identified in this feasibility study.

## 11.2 Feasibility Summary

| Dimension | Verdict | Key Condition |
|---|---|---|
| Technical Feasibility | Feasible | Use a manageable technology stack and keep the system architecture suitable for the team's available skills and project duration. |
| Financial Feasibility | Feasible | Use free or low-cost development tools, hosting, databases, and AI services during the prototype stage. |
| Operational Feasibility | Feasible with conditions | Workflows must be easy to understand, role responsibilities must be clear, and unnecessary data entry should be reduced. |
| Schedule Feasibility | Feasible with conditions | Must-have requirements must be prioritised and development and testing must begin early enough to avoid pressure during the final phases. |
| Data Feasibility | Feasible for the prototype | A realistic synthetic dataset must be created because real Khalifa University operational data is not currently available to the team. |
| AI Feasibility | Feasible with limitations | AI functions should be tested on synthetic data, important outputs should be reviewed by users, and fallback behaviour should be available if an AI service fails. |
| Legal, Ethical and Policy Feasibility | Feasible with conditions | Personal data should be minimised, licences and service terms must be respected, and important decisions must remain under authorised human control. |
| Risk Feasibility | Manageable | Major risks must be reviewed regularly and contingency plans should be used if schedule, API, data, or scope problems occur. |

Overall, no feasibility dimension currently requires the project to be stopped. However, several dimensions depend on controlling the project scope and validating important technical decisions early.

## 11.3 Phase 3 Action Plan

The main objective before and during Phase 3 is to convert the current feasibility decisions into clear and testable system requirements.

The following actions should be completed:

| Action | Proposed Owner | Expected Result |
|---|---|---|
| Confirm the final technology stack | Design/AI Lead and Development/Testing Lead | Agreed backend, frontend, database, and AI technologies |
| Finalise the synthetic dataset design | Requirements Lead | Defined asset, request, user, transfer, inspection, maintenance, and related test-data fields |
| Review and lock the Must-have requirements | Requirements Lead with all team members | Agreed set of essential functional requirements for implementation |
| Review AI requirements for the five AI functions | Design/AI Lead | Clear and realistic AI requirements that can be tested during later phases |
| Define fallback behaviour for AI-dependent functions | Development/Testing Lead | Core workflows remain usable when an AI API is unavailable or unreliable |
| Confirm user roles and approval boundaries | Requirements Lead and Project Coordinator | Clear permissions and responsibilities for each stakeholder role |
| Review security and privacy requirements | Development/Testing Lead | Requirements for authentication, role-based access, audit logging, and data minimisation |
| Check third-party licences and selected AI-service terms | Development/Testing Lead | Record of important external dependencies and their usage conditions |
| Review workload and assign later modules | Project Coordinator with all team members | Clear responsibility for design, implementation, testing, and documentation tasks |
| Review Phase 3 work before submission | All team members | Consistent Requirements Document with no missing or conflicting requirements |

The proposed ownership can be mapped to the team's existing roles:

- **Mohammed Alketbi:** Project Coordinator
- **Mohammed Al Ali:** Design and AI Lead
- **Mubarak:** Requirements Lead
- **Abdulla:** Development and Testing Lead

These assignments may be adjusted by the team if responsibilities change during Phase 3.

## 11.4 Scope Reduction Triggers

The team should reduce project scope if continuing with all planned features would put the Must-have requirements or final submission at risk.

Scope reduction should be considered if one or more of the following situations occurs:

- Core Must-have requirements are still unclear after the Phase 3 requirements work.
- The selected AI service cannot be integrated reliably within the available development time.
- Free-tier AI limits prevent sufficient development or testing.
- The synthetic dataset requires significantly more work than expected.
- The team falls behind during the design or implementation phases.
- Major system functions remain unstable close to the testing phase.
- A team member becomes unavailable for an extended period.
- Too much development time is being spent on optional features instead of the core workflows.

If scope reduction becomes necessary, the team should take the following actions in order:

1. Protect all Must-have requirements.
2. Postpone Could-have requirements.
3. Postpone lower-priority Should-have requirements if necessary.
4. Simplify AI functions rather than removing the core classic functionality.
5. Use simpler interfaces or workflows where they still satisfy the required functionality.
6. Focus development and testing on the most important end-to-end workflows.
7. Freeze new features when necessary so that remaining time can be used for integration, testing, documentation, and demonstration.

The project should only continue adding optional functionality when the core system is stable and the Must-have requirements are on schedule.

## 11.5 Final Feasibility Decision

The final recommendation of this feasibility study is **GO, with conditions**.

The project should proceed to Phase 3 because the proposed system can be developed using the available team, tools, project schedule, and prototype resources.

The main conditions are that the team must control the project scope, prioritise Must-have requirements, use suitable synthetic data, validate AI functions early, maintain non-AI fallback options for essential workflows, and keep important decisions under human control.

If these conditions are followed, the project remains suitable for continued development through the remaining software-engineering phases.
