# Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System

## Phase 2 – Feasibility Document

**Khalifa University – Department of Computer Science**

**COSC 336 – Introduction to Software Engineering – Fall 2026**

**Prepared by:** Group 5 – Mohammed Alketbi (100067035), Abdulla, Mohammed Al Ali, Mubarak

**Prepared for:** Eng. Dina Atia, Lab Instructor

**Date:** September 2026

**Version:** 0.1 (Draft)

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
