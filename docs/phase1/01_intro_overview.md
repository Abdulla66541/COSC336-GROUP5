# Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System

## Phase 1 -Initial Plan and Requirement Gathering Document

**Khalifa University -Department of Computer Science**

**COSC 336-Introduction to Software Engineering-Fall2026**

**Prepared by:** Group 5 – Mohammed Alketbi, Abdulla, Mohammed Al Ali, Mubarak

**Prepared for:** Eng. Dina Atia, Lab Instructor

**Date:** September 2026



---

# 1. Introduction

## 1.1 Project Concept

Imagine a lab in one building throwing away twenty working monitors, while a department in the next building is filling out a purchase order for twenty new ones. Nobody did anything wrong; they simply had no way of knowing about each other. This happens across universities every year with furniture, computers, lab equipment, books and office supplies. The resources exist, but the connection between the people who have them and the people who need them does not.

Our project is that connection. We propose an internal web platform for Khalifa University that follows every campus asset through its whole life: from the day it is registered, through use, transfer, maintenance and repair, to the day it is finally donated, recycled or retired. The system is built in two layers.

The **classic layer** is the solid foundation: an asset register, a marketplace where departments publish surplus or unused items, a way for other departments to search, request and reserve them, approval and transfer workflows, maintenance and inspection records, and user accounts with clearly defined roles and permissions. This layer is rule-based, predictable and transparent.

The **AI layer** makes the foundation smart. It matches available assets to departmental requests by meaning rather than exact keywords, so a request for "laboratory seating" can find an item listed as "lab bench stool". It suggests categories and tags when a new asset is registered, recommends the most sustainable action for an asset (reuse, transfer, repair, donate, recycle or retire), lets users search and ask questions in plain language through an LLM assistant, and generates readable reports on savings, waste diverted and estimated carbon reductions.

The guiding idea is the circular economy: keep resources in use for as long as possible and recover their value at the end. In practice, before any department buys something new, the system should be able to answer one simple question: *does this already exist somewhere on campus?*

## 1.2 Purpose of this Document

This document is the Phase 1 deliverable of the COSC 336 running project: Planning and Requirement Gathering. Before we design or build anything, the team and the client need to agree on what problem we are solving, for whom, and what "done" looks like. This document records that agreement.

Specifically, it:

- defines the problem, scope, objectives, assumptions and expected benefits of the system;
- identifies all stakeholders and maps each one to the features they use, the data they need, their permissions, their responsibilities and the approval decisions they make;
- describes how surplus assets, requests, transfers, maintenance and disposal are handled today, without the system;
- explains how we gathered requirements, summarises and prioritises them, and presents an initial requirements specification;
- defines measurable success criteria so that we can judge the project objectively at the end; and
- presents a preliminary project plan covering the timeline, milestones, methodology, team roles, dependencies, risks and resources for the remaining seven phases.

The intended readers are the lab instructor and course instructor, who act as the client, and the four members of Group 5, who act as the development team. This document is the baseline for the Feasibility Study in Phase 2 and the detailed Requirements Analysis in Phase 3, and it will be updated as our understanding of the problem improves.


# 2. Problem Statement

The challenge does not lie in a lack of reusable resources in the University. The problem lies in the absence of a connection between already existing resources and departments that could use them.

Currently, the information about assets is scattered. A conventional asset register may inform us about the ownership, location, purchase date, and write-off of a particular item. This kind of data can tell us nothing about the unused nature of the resource, the plan of another department to buy something similar, or the best sustainable practice regarding the reuse of this item.

It comes as no surprise that the lack of such an approach leads to duplication of purchases, unused resources kept in storage for many years or just disposed of instead of redistribution, lack of maintenance and repair records due to changes in possession of the asset, manual search based on personal connections, and the inability to measure the savings and sustainability achieved through internal reuse practices.

Also, current solutions suffer from the rigidity of keywords and fixed categories. An application for "laboratory seating" will never lead to the discovery of an "lab bench stool", although these two are actually one item.

Our solution solves these problems by providing the university with a single platform that makes surplus assets visible, matches the supply with the demand using a combination of strict criteria and semantic artificial intelligence, ensures that transfer of each asset passes predefined approval stages, gathers all life-cycle events in one place and quantifies the outcome of reuse and savings in terms of financial gains and emission reductions. All decisions are made by authorized users, artificial intelligence suggests.

### 3.1 Summary Description of the Proposed System

Two-tier, role-based web application with one database and one interface.

**Classic tier (baseline):**
1. **Asset registration & publication** – registration of assets with complete details and publication of surplus items in an internal marketplace.
2. **Requesting & reservation of resources** – requesting resources and searching and filtering the available items, reserving them and monitoring their status.
3. **Approvals & transfer management** – approvals workflow for releases, transfers, donations, recycling and disposals, recording any changes of custody and location.
4. **Inspections & life-cycle tracking** – complete asset history and a maintenance component for defects, repairs and related costings.
5. **User and access management** – authentication and role-based permissions and standard reports for all campus roles.

**AI tier (extended):**
1. **AI-driven resource matching** – matching of listings with requests using meaning matching with compatibility score, ranking and an explanation in plain language.
2. **AI-assisted classification** – recommending the category, tags and missing details for new assets.
3. **Sustainability optimisation** – recommending re-use, transfers, repairs, donations, recycling or disposing of assets and estimating their environmental impact.
4. **LLM-powered assistant** – natural language search, requesting and questioning.
5. **Generative AI reporting** – summaries of the activity and its financial and sustainability impact.

All AI-generated decisions are recommendation only, final decisions are made by authorised users.

### 3.2 Problem Description and Context

The current university asset management system is focused on audits and keeping records rather than reusing. Where the reuse is practiced, it is done via emails and personal communication. There are three trends that render the situation timely for change: the need for reporting sustainability that becomes a legal requirement soon (in accordance with the UAE Net Zero 2050 strategy), the budget considerations and the availability of advanced large language models that can automatically match meanings, classify resources and generate reports.

Academically, this is a running project for the COSC 336 course where the students implement the entire software life cycle and compare the deterministic, rule-based approach with the adaptive, AI-enhanced one.

### 3.3 Business Objectives and Project Objectives

**Business objectives**: reduce unnecessary procurement; increase asset lifespan; avoid waste going to landfills; keep the complete, auditable record of the whole lifecycle of assets; calculate financial and environmental impact of the processes and simplify them for non-technical employees.

**Project objectives:**
- **O1** – Implement the five classic functions using conventional software engineering.
- **O2** – Implement the five AI functions with explanations, confidence levels, user override and fallback behaviour.
- **O3** – Determine and calculate sustainability metrics (number of avoided purchases, savings, re-use rate, increased lifespan, waste diverted, estimated CO₂ reduction).
- **O4** – Compare the classic and AI-enhanced approaches explicitly in documentation.
- **O5** – Apply professional practice in all eight phases of software life cycle as reflected in regular individual commits on GitHub.

## 3.4 Project Constraints

| Constraint | Description |
|---|---|
| Budget | No budget; only free or educational tier products and AI services are allowed. |
| Timeline | One semester with fixed 8 phases; deadlines provided by the course. |
| People | Four students working part-time; no help from outside people. |
| Data | No real university data; only synthetic sample data which means limitations in AI accuracy claims. |
| Technology | No integration with real university systems; local login; external or open-source AI model. |
| Process | Using Git/GitHub and committing changes by individual authors (10% of each phase mark). |
| Integrity | Following course policy on AI; no collaboration with any other group. |

## 3.5 Assumptions

- Instructors are a client who decides requirements and accept the system.
- Departments are willing to publish excesses and think about transfer rather than purchase something new.
- It is possible to define common category list and unique ID system for prototype.
- Free-tier services of AI stay available; otherwise the system switches to keyword search and rules.
- Sustainability numbers are estimated using average values from literature and uncertainties of estimation are specified.
- User has a browser; mobile application is not required.
- All four members are accessible and commit via their own Git/GitHub account.

## 3.6 Expected Benefits

| Category | Benefit |
|---|---|
| Financial | Reduction in duplications; lower costs of storage and waste removal; savings can be measured. |
| Environmental | Increased longevity of assets; higher share of reuse and recycling; reduction of amount in landfills and embodied carbon footprint. |
| Operational | One searchable catalogue of all assets; faster match; clear approval process; history that follows an asset. |
| Organisational | Equitable distribution of assets between departments; contributes to sustainability goals of university. |
| Academic | Practical experience of a full asset lifecycle and responsible AI integration skills for team members. |


## 3.7 Scope of the Project

### 3.7.1 In Scope

- User accounts, authentication and role-based access control for nine defined roles; departments management.
- Registration of assets with complete information, status management and assistance in classification from the AI.
- Marketplace for surplus inventory with searching and filtering options.
- Submit requests, reserve assets, check their status.
- AI semantic matching with scores, ranking, reasons and possibility to override the result.
- Approvals and transfers including processes of donation, recycling and disposal.
- Asset's life-cycle history and maintenance/repair tracking.
- Sustainability recommendations, indicators and dashboard.
- LLM assistance, notifications, standard and AI-powered reports.
- Engineering deliverables: plan, feasibility study, requirements, design (architecture, UML, DFD, mockups), code, tests, final report and demonstration.

### 3.7.2 Out of Scope

- Connection to live ERP, financial, purchasing or identification systems of the university.
- Real transactions such as payments, purchase orders and invoices.
- Hardware, i.e. barcode/RFID scanners and IoT devices.
- Training machine learning algorithms from scratch.
- Interaction with organizations outside the university.
- Legally binding sustainability accounting, all numbers should be marked as estimates.
- Support multi-language interface, mobile applications, offline mode.

### 3.7.3 Possible Future Enhancements

- Demand prediction for more efficiency of surplus asset utilization.
- Procurement integration that automatically searches for alternative inventory within the organization.
- Barcode/QR scanning and support Arabic language.
