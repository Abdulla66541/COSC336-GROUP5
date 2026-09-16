# Circular Campus Project
## Phase 1 – Initial Plan and Requirement Gathering Document

**University:** Khalifa University  
**Course:** COSC 336  
**Group:** Group 5  
**Prepared by:** Group 5  
**Date:** September 2026  
**Version:** 1.0

---

## Revision History

| Version | Date | Description |
|---|---|---|
| 1.0 | September 2026 | Initial Phase 1 submission |

---

## Table of Contents

1. Introduction
2. Problem Statement
3. Project Overview
4. Stakeholder Analysis and Current Process
5. Requirements Gathering
6. Initial Requirements Specification
7. Project Plan and Success Criteria
8. Appendix A – Glossary
9. Appendix B – Interview Notes
10. References

---

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


# 4. Stakeholder Analysis and Current Process

This section outlines the key stakeholders for the proposed system, their roles and permissions, and provides a snapshot of the current process without the integrated system.
The current-process analysis below is not fully detailed in the project brief, so is to be viewed as a preliminary understanding that may be further developed later.

## 4.1 Stakeholder Identification

### 4.1.1 Department Representatives
Represent their department(s), determine resource requirements, track requests and may be involved in transfer decisions. They require to see the assets of the departments and the available assets on the campus.

### 4.1.2 Asset Custodians
Maintain asset information such as location, condition, availability and custody. They can also be involved in inspections, transfers, asset release/receipt.

### 4.1.3 Requesters
Look for resources and make requests. They require access to assets available, status of requests generated by AI.

### 4.1.4 Administrators
Operating of support systems, user management and workflow activities. They should have user access, asset access, requests, approvals and reports.

### 4.1.5 Procurement Officers
Consider the campus assets and needs before making new purchases. They need request, asset and cost information.

### 4.1.6 Finance Officers
Discuss the economic consequences of reusing, repairing, transferring and buying. They might employ asset values, repair costs, transfer costs and savings estimates.

### 4.1.7 Maintenance Staff
Inspect, maintain and repair assets. They must have access to asset condition, defects, maintenance history and repair records.

### 4.1.8 Sustainability Officers
Track environmental outcomes like re-use, waste diversion, asset-life extension and estimated carbon-emission reductions.

### 4.1.9 System Administrators
Manage technical configuration, access control, security and system availability.

### 4.1.10 Course Instructor and Lab Instructor
Act as the project client and evaluators. They review project documentation, GitHub history, testing and demonstrations.

### 4.1.11 Group 5 Development Team
Plans, designs, develops, tests and documents the system.


## 4.2 Stakeholder Mapping

The following table presents an initial mapping of stakeholders to the features they use, the information they require, their permissions, their responsibilities and possible approval decisions.

Exact authorization and approval rules will be refined during later requirement analysis because the project description does not define every university policy or approval boundary in detail.

| Stakeholder | Features They Use | Data They Need | Permissions | Responsibilities | Approval Decisions |
|---|---|---|---|---|---|
| Department Representatives | Asset search, surplus publication, requests, request tracking, transfer tracking | Department assets, available resources, request and transfer status | View relevant resources and perform permitted departmental actions | Represent departmental needs and coordinate resource sharing | May participate in departmental request or transfer decisions where authorized |
| Asset Custodians | Asset registration, asset updates, inspections, transfer and life-cycle tracking | Asset details, condition, location, custody, maintenance and transfer history | Create or update assets under their responsibility | Maintain accurate asset records and custody information | May confirm release or receipt where authorized |
| Requesters | Search, filtering, AI matching, request submission, reservation and status tracking | Asset availability, specifications, quantity, condition, location and request status | Search resources and submit permitted requests | Describe resource requirements accurately and monitor requests | Normally no high-level approval authority unless separately assigned |
| Administrators | User management, workflow administration, reports and operational monitoring | Users, assets, requests, transfers, approvals and activity records | Administrative permissions based on assigned role | Support system operation and administrative workflows | May perform administrative approvals where explicitly authorized |
| Procurement Officers | Resource search, request review, cost comparison and reports | Resource requests, available assets, values and relevant costs | View procurement-related information | Consider internal reuse before unnecessary new purchases | Procurement decisions remain subject to university procedures |
| Finance Officers | Financial reports and cost/savings analysis | Asset values, repair cost, transfer cost and estimated savings | Access authorized financial information | Review the financial effects of resource decisions | Financial approval authority depends on university policy |
| Maintenance Staff | Defect reporting, inspection, maintenance and repair tracking | Condition, defect information, repair history, status and cost | Update assigned maintenance and inspection records | Inspect, maintain and repair resources and record results | May recommend maintenance-related actions; high-impact actions require authorized approval |
| Sustainability Officers | Sustainability dashboard, reports and recommendation review | Reuse, repair, waste-diversion and carbon information | View sustainability information and reports | Monitor environmental outcomes and sustainability indicators | May advise on sustainable actions |
| System Administrators | Access control, security, configuration and audit monitoring | User roles, logs, configuration and technical status | Elevated technical administration access | Maintain secure and reliable operation of the platform | Technical administration decisions |
| Course Instructor / Lab Instructor | Documentation review, GitHub history, testing evidence and demonstrations | Requirements, designs, commits, test results and project documentation | Review project artefacts | Evaluate the project and provide academic feedback | Academic evaluation and acceptance decisions |
| Group 5 Development Team | GitHub, development, documentation, design and testing tools | Requirements, source code, designs, test data and feedback | Development access to project resources | Design, implement, test and document the solution | Technical design decisions within project requirements |


## 4.3 Current As-Is Process

### 4.3.1 Surplus Assets
A department may determine that an asset is surplus or underutilized and other departments may not be aware of its surplus or underutilized status.

### 4.3.2 Resource Requests
If a department requires a resource, it can either check locally or proceed with the department's procurement process. If there is no central visibility, the appropriate assets in other departments might be overlooked.

### 4.3.3 Resource Matching
If the proposed system is not implemented, there is no semantic matching between the request and available assets that is integrated with AI.

### 4.3.4 Transfer and Approval
If an appropriate asset is identified, the appropriate parties may need to arrange for approvals, asset transfers and location changes.

### 4.3.5 Maintenance and Repair
Maintenance activities can be recorded separately and this makes it difficult to see the full life of an asset.

### 4.3.6 Donation, Recycling and Disposal
When an asset is no longer useful, actions such as donation, recycling, retirement or disposal may be considered depending on its condition and university policy.


## 4.4 Gaps Identified

- Inadequate visibility of excess assets departmentally.
- Appropriate resources might not be identified before new resources are purchased.
- Resource matching can be done through verbal communication or precise descriptions.
- The asset history might be broken up.
- The information for maintenance and transfer may not be centralized.
- Financial benefits of reusing are not necessarily measurable.
- Environmental benefits might not always be monitored.
- Lack of intelligent support for reuse, repair, transfer and recycling decisions.


 ## 4.5 Section Summary

Analysis of the stakeholders reveals that the proposed system is required to be usable by different stakeholders who have different responsibilities, information needs and levels of authority. So role-based access and well-defined approval boundaries are important aspects of the system.

The current-process analysis focuses on the main issue that the project is tackling: useful resources could be available within the university but if they are not visible, coordinated and tracked through their life cycle, they may not be reused effectively.

The proposed system aims to fill these gaps by integrating a structured asset-management and resource-exchange platform with AI-driven classification and semantic matching, sustainability recommendations, and natural-language interaction and reporting. Important approvals and high impact life cycle decisions still lie with human users.





# 5. Requirements Gathering

## 5.1 Requirements Gathering Methodology

The requirements for the Circular Campus system were gathered mainly through document analysis and short stakeholder interviews. The project description and the COSC336 project slides were reviewed to understand the main purpose of the system, the required functionalities, the users involved, and the information that needs to be stored.

The document analysis was also used to identify the five classic system functionalities and the five AI-enhanced functionalities. Particular attention was given to the information required when registering assets and creating requests.

### Document Analysis

The following documents were reviewed:

- ProjectSeptember2026.docx
- COSC336_Circular_Campus_Project_Fall2026.pdf

The documents helped identify the main system functions, user roles, required data, AI features, sustainability goals, and project constraints.

### Interviews

Short interviews were prepared to understand how potential users currently deal with university assets and what they would expect from the proposed system.

#### Interview 1 – Lab Technician

**Role:** Lab Technician  
**Date:** 16/09/2026

Questions focused on equipment tracking, damaged equipment, maintenance, and finding available assets.

**Expected / sample findings:**

- Equipment may be tracked using spreadsheets or other manual records.
- It can be difficult to know whether unused equipment is available in another lab or department.
- Maintenance and repair history should be connected to each asset.
- Photos, location, condition, and availability are important when deciding whether an asset can be reused.

#### Interview 2 – Department Administrator

**Role:** Department Administrator / Secretary  
**Date:** 16/09/2026

Questions focused on asset requests, approvals, department transfers, and record keeping.

**Expected / sample findings:**

- Requests between departments may depend heavily on emails or direct communication.
- Staff need to know who owns an asset and who is responsible for approving its transfer.
- Users should be able to see whether a request is pending, approved, rejected, or completed.
- Previous ownership and transfer information should remain available after an asset changes departments.

#### Interview 3 – IT / Facilities Staff

**Role:** IT or Facilities Staff  
**Date:** 16/09/2026

Questions focused on asset condition, repairs, disposal, permissions, and sustainability.

**Expected / sample findings:**

- Maintenance and inspection records should be stored with the related asset.
- Damaged or unused assets should be considered for repair, reuse, donation, or recycling before disposal.
- Important asset information should only be changed by authorized users.
- A central system could reduce unnecessary purchases by making existing assets easier to locate and reuse.


## 5.2 Summary of Gathered Requirements

The gathered requirements were grouped into the following main themes.

### Asset Management

The system needs to maintain complete information about university assets, including their description, quantity, ownership, location, value, condition, photos, and supporting documents.

### Requests and Reservations

Users need to be able to search for assets and submit requests based on their needs. Requests should contain enough information for the system and approving staff to understand what is required.

### Approval and Transfer

Asset transfers should follow a controlled approval process. The system should record approval decisions and update the ownership and location of transferred assets.

### Inspection and Life-Cycle Tracking

The system should maintain the history of each asset, including inspections, maintenance, repairs, transfers, reuse, donation, recycling, and disposal.

### User and Access Management

Different users have different responsibilities, so the system should control which information and functions they are allowed to access.

### Artificial Intelligence

AI should support the system by finding suitable assets, helping classify assets, providing sustainability recommendations, answering questions, and producing useful reports.

### Sustainability

The system should support the Circular Campus idea by encouraging reuse, repair, donation, and recycling before purchasing replacements or disposing of assets.

### Reporting

Users should be able to view useful information about assets, requests, transfers, maintenance, reuse, and sustainability activities.


## 5.3 Requirement Prioritisation

The MoSCoW method was used to give an initial priority to the main requirements.

| Requirement | Priority | Reason |
|---|---|---|
| Asset registration | Must | Assets need to be registered before they can be managed |
| Asset information management | Must | Accurate information is needed throughout the asset life cycle |
| Asset search | Must | Users need to find available assets |
| Request and reservation | Must | Departments need a formal way to request assets |
| Approval and transfer | Must | Transfers require authorization and proper records |
| Inspection and life-cycle tracking | Must | The system needs to maintain asset history |
| User and access management | Must | Different users require different permissions |
| AI asset matching | Must | Required AI functionality of the project |
| AI classification | Must | Required AI functionality of the project |
| Sustainability recommendations | Must | Supports the main Circular Campus objective |
| LLM assistant | Must | Required AI functionality of the project |
| Generative AI reporting | Must | Required AI functionality of the project |
| Advanced analytics | Could | Useful but not required for the first working version |
| External system integration | Could | Can be considered as a future enhancement |


# 6. Initial Requirements Specification

## 6.1 Asset Registration

The Asset Registration function allows authorized users to create and maintain records for university assets.

**Priority:** Must

- **REQ-01:** The system shall allow authorized users to register a new asset.
- **REQ-02:** The system shall store the asset name and description.
- **REQ-03:** The system shall store the asset category and quantity.
- **REQ-04:** The system shall store the asset owner and department.
- **REQ-05:** The system shall store the current location of the asset.
- **REQ-06:** The system shall store the purchase date and asset value.
- **REQ-07:** The system shall store the current condition of the asset.
- **REQ-08:** The system shall allow users to attach photos and documents to an asset record.


## 6.2 Request and Reservation

The Request and Reservation function allows users to request assets that are required by their department.

**Priority:** Must

- **REQ-09:** The system shall allow authorized users to create an asset request.
- **REQ-10:** A request shall include the required asset category and purpose.
- **REQ-11:** A request shall allow the user to enter required specifications and quantity.
- **REQ-12:** A request shall include the preferred asset condition and level of urgency.
- **REQ-13:** A request shall contain the required location and date.
- **REQ-14:** The system shall allow users to view the current status of their requests.


## 6.3 Approval and Transfer

The Approval and Transfer function manages the authorization and movement of assets between users or departments.

**Priority:** Must

- **REQ-15:** The system shall allow authorized users to approve or reject an asset request.
- **REQ-16:** The system shall record the approval or rejection decision.
- **REQ-17:** The system shall record the user responsible for an approval decision.
- **REQ-18:** The system shall update the asset owner, department, and location after an approved transfer.
- **REQ-19:** The system shall maintain a history of asset transfers.


## 6.4 Inspection and Life-Cycle Tracking

This functionality keeps a record of the condition and activities related to an asset throughout its life cycle.

**Priority:** Must

- **REQ-20:** The system shall allow authorized staff to record an asset inspection.
- **REQ-21:** The system shall allow maintenance and repair activities to be recorded.
- **REQ-22:** The system shall maintain a history of changes to an asset's condition.
- **REQ-23:** The system shall record important life-cycle events such as reuse, repair, donation, recycling, and disposal.
- **REQ-24:** The system shall allow users to view the previous history of an asset.


## 6.5 User and Access Management

This functionality controls system access based on the responsibilities of each type of user.

**Priority:** Must

- **REQ-25:** The system shall require users to authenticate before accessing protected functions.
- **REQ-26:** The system shall assign permissions according to the user's role.
- **REQ-27:** Administrators shall be able to create, update, and deactivate user accounts.
- **REQ-28:** The system shall prevent unauthorized users from performing restricted actions.


## 6.6 AI Matching

AI Matching helps connect asset requests with existing assets that may satisfy the user's needs.

**Priority:** Must

- **REQ-29:** The system shall compare information in an asset request with available asset records.
- **REQ-30:** The system shall recommend suitable existing assets to the requester.
- **REQ-31:** The system shall provide information explaining why an asset may be suitable for the request.
- **REQ-32:** Users shall be able to accept or ignore an AI-generated match.


## 6.7 AI Classification

AI Classification helps users assign an appropriate category to newly registered assets.

**Priority:** Must

- **REQ-33:** The system shall analyse asset information and suggest an appropriate category.
- **REQ-34:** The user shall be able to review the suggested category before accepting it.
- **REQ-35:** Authorized users shall be able to correct an incorrect AI classification.


## 6.8 Sustainability Recommendation

The Sustainability Recommendation function helps users decide what should happen to assets that are damaged, unused, or no longer required.

**Priority:** Must

- **REQ-36:** The system shall consider the condition and available information of an asset before providing a sustainability recommendation.
- **REQ-37:** The system shall be able to recommend reuse, repair, donation, recycling, or disposal when appropriate.
- **REQ-38:** The system shall present the recommendation to an authorized user before any final action is taken.
- **REQ-39:** The final sustainability decision shall remain under human control.


## 6.9 LLM Assistant

The LLM Assistant allows users to interact with the system using normal language instead of only using menus and filters.

**Priority:** Must

- **REQ-40:** The system shall allow users to ask questions using natural language.
- **REQ-41:** The assistant shall provide answers using information available in the system.
- **REQ-42:** The assistant shall help users locate relevant assets or system information.
- **REQ-43:** The assistant shall not make final approval, transfer, or disposal decisions for authorized staff.


## 6.10 Generative AI Reporting

Generative AI Reporting helps create summaries and reports from information stored in the Circular Campus system.

**Priority:** Must

- **REQ-44:** The system shall generate reports using stored system information.
- **REQ-45:** Generated reports shall be able to summarize asset reuse, transfers, maintenance, and sustainability activities.
- **REQ-46:** Users shall be able to review generated reports before they are used or shared.
- **REQ-47:** Generated reports shall be based on available system data and should not knowingly add unsupported information.


## 6.11 Non-Functional Requirements

### Performance

- **NFR-01:** Normal system pages should load within a reasonable amount of time under expected university usage.
- **NFR-02:** Asset searches and filters should return results quickly enough for normal user interaction.

### Safety

- **NFR-03:** AI recommendations shall not automatically perform irreversible actions such as transferring, donating, recycling, or disposing of an asset.

### Security

- **NFR-04:** Users shall only be allowed to access information and functions permitted by their assigned role.
- **NFR-05:** Sensitive user and asset information shall be protected from unauthorized access.

### Software Quality Attributes

- **NFR-06:** The system should provide a clear and easy-to-use interface for its intended users.
- **NFR-07:** The system should be maintainable so that functions can be updated or extended during later project phases.

### Business Rules

- **NFR-08:** Asset transfers, approvals, and final disposal decisions shall only be completed by users with the required authority.
- **NFR-09:** AI-generated recommendations shall support human decisions rather than replace required human approvals.
- **NFR-10:** Important changes to asset ownership, condition, and life-cycle status should remain recorded for future reference.




# 7. Success Criteria and Project Plan

## 7.1 Measurable Success Criteria
The success of the Circular Campus Asset Reuse and Management System will be evaluated using measurable criteria. These criteria cover system functionality, user acceptance, AI usefulness, financial savings, asset reuse, and sustainability impact.

| Area | Success Criterion | Measurement |
|---|---|---|
| Functional Performance | The system successfully implements the essential project requirements. | 100% of the Must-have functional requirements are implemented and pass testing. |
| User Acceptance | The system is understandable and useful for intended university users. | At least 80% positive feedback during User Acceptance Testing (UAT). |
| AI Match Usefulness | AI-generated asset matches are relevant to user requests. | At least 70% of AI-generated matches are rated as relevant or useful during testing. |
| Avoided Purchases | The system helps departments find reusable assets before purchasing new items. | Record the number and estimated value of purchases avoided through internal reuse. |
| Reuse and Repair | The system encourages assets to be reused, transferred, or repaired instead of discarded. | Track the percentage and number of registered assets that are reused, transferred, or repaired. |
| Sustainability Outcomes | The system contributes to reducing university waste and environmental impact. | Track assets diverted from disposal and provide an estimated amount of waste and CO2 emissions avoided where suitable data is available. |

## 7.2 Preliminary Timeline
The project is divided into eight phases according to the course project schedule. Each phase has a defined deliverable and contributes to the gradual development of the system.

| Phase | Submission Deadline | Duration | Main Deliverable | Weight |
|---|---|---|---|---|
| Phase 1 | In the labs of the week of Sep 14th, 2026 | 1 Week | Initial Plan and Requirement Gathering Document | 10% |
| Phase 2 | In the labs of the week of Sept 21st, 2026 | 1 Week | Feasibility Document | 10% |
| Phase 3 | In the labs of the week of Oct 5th, 2026 | 2 Weeks | Requirements Document | 10% |
| Phases 4 & 5 | In the labs of the week of Oct 26th, 2026 | 3 Weeks | Design Document (Architecture and Detailed Design) | 20% |
| Phase 6 | In the labs of the week of Nov 16th, 2026 | 3 Weeks | Draft Implementation with Major Features | 20% |
| Phase 7 | In the labs of the week of Nov 23rd, 2026 | 1 Week | Details of Test Cases | 10% |
| Phase 8 | In the labs of the week of Nov 23rd, 2026 | Not specified | Final Project, Presentation and Demonstration | 20% |

The timeline will be used to monitor progress and ensure that each major deliverable is completed before the required laboratory submission period.
## 7.3 Milestones and Deliverables
Each project phase represents a major milestone. The team will use these milestones to track progress and ensure that the required work is completed before moving to later stages.

| Phase | Milestone | Deliverable |
|---|---|---|
| Phase 1 | Project planning and initial requirements completed | Initial Plan and Requirement Gathering Document |
| Phase 2 | Project feasibility evaluated | Feasibility Document |
| Phase 3 | Detailed system requirements defined | Requirements Document |
| Phases 4 & 5 | System architecture and detailed design completed | Design Document (Architecture and Detailed Design) |
| Phase 6 | Major system functionality implemented | Draft Implementation with Major Features |
| Phase 7 | System testing prepared and documented | Details of Test Cases |
| Phase 8 | Final system completed and demonstrated | Final Project, Presentation and Demonstration |

The team will review the work completed at each milestone before continuing to the next stage. This will help identify missing requirements, design problems, implementation issues, and testing concerns early in the project.
## 7.4 Development Methodology
The team proposes to use an Agile-inspired development approach throughout the project. The project phases will be treated as development iterations in which the team plans the required work, produces the expected deliverables, reviews the results, and improves the system based on feedback.

This approach is suitable because the project is divided into several phases with separate deliverables. Instead of attempting to complete the entire system at once, the team can progressively develop the requirements, design, implementation, testing, and final system.

The weekly laboratory environment also supports an iterative approach because the team can receive feedback from the instructor and lab engineer and use that feedback to improve later work.

An iterative methodology is particularly useful for the AI-enhanced features of the project. AI-based resource matching, AI-assisted asset classification, sustainability optimization, the LLM-powered assistant, and generative AI reporting may require experimentation and refinement before satisfactory results are achieved.

The general development cycle will be:

**Plan → Develop → Test and Review → Receive Feedback → Improve → Continue to the Next Phase**

Although the project will use Agile principles, the team will continue to follow the official course phase deadlines and required deliverables.
## 7.5 Team Structure and Roles
The project team consists of four members. Each member has a primary responsibility while also contributing to reviews, development, testing, and documentation when required.

| Team Member | Proposed Primary Role | Phase 1 Responsibility | Preliminary Later Responsibility |
|---|---|---|---|
| Mohammed Alketbi | Project Coordinator | Introduction, problem statement, project overview, and final document assembly | Coordinate project integration, documentation, and selected core modules |
| Mohammed Al Ali | Design and AI Lead | Stakeholder analysis and current-process analysis | Support system/interface design and AI-related components |
| Mubarak | Requirements Lead | Requirements gathering and initial requirements specification | Maintain requirements and support requirements-based testing |
| Abdulla | Development and Testing Lead | Success criteria, timeline, methodology, roles, risks, resources, and AI reflection | Support implementation, integration, and system testing |

The exact ownership of implementation modules may be adjusted during the design phase depending on workload, technical difficulty, and each member's experience.

Although each member has a primary role, the project will not depend entirely on one person for any major component. Team members will review each other's work and share enough information so that progress can continue if one member is temporarily unavailable.

All members are also responsible for maintaining clear GitHub commit history so that their individual contributions can be identified.
## 7.6 Dependencies, Risks and Resource Allocation
### 7.6.1 Project Dependencies

Several project activities depend on the successful completion of earlier work.

- Requirements must be understood before detailed system design can be completed.
- The system design should define the main structure before major implementation begins.
- Implementation must reach a usable stage before complete system testing can be performed.
- AI-based functions depend on having suitable asset and request data for testing and evaluation.
- Some AI functions may depend on access to an external AI model or API.
- Sustainability calculations depend on having enough information to estimate avoided purchases, waste diversion, and environmental impact.
- Final integration depends on team members completing their assigned work on time.

These dependencies will be reviewed during each project phase so that delays can be identified and handled early.

### 7.6.2 Project Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| AI API becomes unavailable, limited, or expensive | Medium | High | Use free-tier or alternative services where possible and keep non-AI fallback functionality for essential processes. |
| Lack of realistic university asset data | High | Medium | Create representative sample datasets containing realistic asset categories, quantities, conditions, locations, and requests. |
| Team member becomes temporarily unavailable | Medium | Medium | Keep work documented on GitHub, commit regularly, and make sure other members understand the main project components. |
| Project scope becomes too large | Medium | High | Prioritise Must-have requirements first and postpone lower-priority enhancements if necessary. |
| AI produces inaccurate or irrelevant recommendations | Medium | High | Test AI results using multiple examples and require human review for important decisions. |
| AI recommendations are difficult to explain | Medium | Medium | Present AI results as suggestions and provide supporting information where possible. |
| Sensitive university information is sent to an external AI service | Medium | High | Avoid sending unnecessary personal or confidential information and use controlled test data during development. |
| GitHub conflicts or lost work | Low | Medium | Commit frequently, use meaningful commit messages, and review changes before merging. |
| Insufficient time for testing | Medium | High | Begin testing individual functions during development instead of waiting until the final project phase. |

### 7.6.3 Resource Allocation

The team will use available software and university resources to minimise project cost.

Expected resources include:

- **GitHub:** version control, documentation, collaboration, and tracking individual contributions.
- **Visual Studio Code:** software development environment.
- **Python and/or JavaScript:** implementation of application functionality where appropriate.
- **Database technology:** storage of assets, requests, users, transfers, inspections, and life-cycle information.
- **AI/LLM service:** experimentation and implementation of AI-enhanced functionality.
- **draw.io:** preparation of system diagrams and design models.
- **University laboratory facilities:** development, testing, demonstrations, and instructor feedback.
- **Sample datasets:** testing both classic and AI-enhanced system functions.

Resources will be allocated according to the needs of each project phase. Team members will also share responsibility for reviewing and testing integrated components.
## 7.7 Classic vs AI-Enhanced Approach Reflection
The proposed system combines traditional software functions with AI-enhanced functionality. Both approaches are useful, but they should be used for different types of tasks.

Traditional or deterministic software is more suitable when the system must follow clear and predictable rules. Examples include user permissions, asset quantities, reservation status, transfer approvals, ownership records, custody information, and audit history. These functions require consistent and reliable behaviour. For example, the system should use fixed rules to determine whether a user has permission to approve a transfer instead of allowing an AI model to make that decision.

AI is more suitable for tasks that involve interpretation, recommendations, classification, or natural-language interaction. In this project, AI can help match available assets with departmental requests, recommend categories and tags for assets, suggest sustainability actions, support users through an LLM-powered assistant, and generate summaries and reports.

AI-based resource matching can be useful because a request and an asset listing may describe the same need using different words. AI can compare factors such as meaning, technical compatibility, condition, quantity, location, and urgency to suggest potentially suitable resources.

AI-assisted classification can recommend categories, tags, and standardised descriptions for newly registered assets. Sustainability optimisation can also recommend whether an asset should be reused, transferred, repaired, refurbished, donated, recycled, or retired.

However, AI should support human users rather than replace them in important decisions. Actions such as approving transfers, changing asset custody, approving purchases, or disposing of university property should remain under human control.

A suitable process is:

**AI Suggests → Human Reviews → Human Approves or Rejects**

There are also risks when using AI. AI-generated results may be inaccurate, irrelevant, biased, or difficult to explain. An AI model may misunderstand a request or recommend an unsuitable asset. Users should therefore be able to review recommendations before acting on them.

Privacy is another important concern. Asset records and user requests may contain internal university information. The system should avoid sending unnecessary personal, confidential, or sensitive information to external AI services.

For this reason, a hybrid approach is suitable for the project. Traditional software rules should control functions that require accuracy, security, permissions, and accountability. AI should be used for functions that benefit from flexible interpretation, recommendations, natural-language interaction, and generated summaries.

The purpose of the AI components is to assist users and improve efficiency while keeping important decisions under human control.
