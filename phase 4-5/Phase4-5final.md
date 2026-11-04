# Phase 4 & 5 - Design Document (Shared Part)

**Project:** Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System
**Course:** COSC 336, Khalifa University, Fall 2026 | **Group:** 5 | **Lab instructor:** Eng. Dina Atia

This file holds what all four of us share: the architecture, the context diagram, the Level 0 DFD, the ER diagram and the data rules. Each member has their own file with sequence diagrams, a class diagram and UI mockups.



| File | Owner | Use cases covered |
|---|---|---|
| `00_architecture_and_shared_design.md` | All | Whole system |
| `01_part1_assets_marketplace_requests.md` | Mohammed Al Ali | UC-01 to UC-10 |
| `02_part2_approvals_transfers_maintenance.md` | Mubarak | UC-11 to UC-16, UC-24, UC-25 |
| `03_part3_users_reports_notifications_audit.md` | Mohammed Alketbi | UC-17 to UC-23 |
| `04_part4_ai_and_sustainability.md` | Abdulla | UC-26 to UC-35 |

---

# 1. Introduction

## 1.1 Purpose

This document describes how the system will be built. Phase 3 said what the system must do. Phases 4 and 5 say how: the architecture (Phase 4) and the detailed design (Phase 5).

## 1.2 Design Goals

| Goal | What it means | Phase 3 link |
|---|---|---|
| Keep the classic layer and the AI layer apart | The system must still work if the AI Service is down | NFR-04, FR-AI-X-08 |
| Human decides | AI only suggests. A person approves | BR-11, FR-AI-X-14 to 17 |
| Everything is traceable | History and audit records can never be edited | BR-13, BR-14, FR-HST-03, FR-AUD-03 |
| Role based access | Every action checks the user's role and department | BR-16, NFR-08 to 11, FR-USR-06 |
| Easy to change | The AI provider can be swapped without changing the business logic | Phase 1 design goal |
| Simple to test | Business logic is separate from the screens and the database | Phase 7 plan |

---

# 2. System Architecture (Phase 4)

## 2.1 Architecture Style

We use a **layered (three-tier) web architecture**: a browser front end, an application server with the business logic, and a database. The AI layer and the notification service are outside services that are reached only through adapters.

```mermaid
flowchart TB
    subgraph CLIENT["Presentation layer (browser)"]
        UI["Web pages<br/>HTML, CSS, JavaScript"]
    end
    subgraph SERVER["Application layer (web server)"]
        API["REST API controllers"]
        AUTH["Security module<br/>login, roles, department checks"]
        SVC["Business services<br/>assets, marketplace, requests,<br/>approvals, transfers, maintenance,<br/>users, reports, sustainability"]
        AIM["AI module<br/>classification, matching, recommendation,<br/>assistant, reporting"]
        NOTI["Notification module"]
        AUD["Audit and history module"]
    end
    subgraph DATA["Data layer"]
        DB[("Database<br/>assets, requests, transfers,<br/>users, logs")]
        FILES["File storage<br/>photos and documents"]
    end
    subgraph EXT["External services"]
        LLM["AI Service<br/>language model and embeddings"]
        MAIL["Email service"]
    end
    UI -->|"HTTPS requests"| API
    API --> AUTH
    API --> SVC
    SVC --> AIM
    SVC --> NOTI
    SVC --> AUD
    SVC --> DB
    SVC --> FILES
    AUD --> DB
    AIM -->|"AI adapter, 15 s timeout"| LLM
    NOTI -->|"mail adapter"| MAIL
```

## 2.2 Layers and Their Jobs

| Layer | Job | Main rule |
|---|---|---|
| Presentation | Shows pages, checks simple input (empty fields, wrong format) and calls the API | No business rules here |
| API controllers | Receive requests, call the security module, call one service, return the answer | One controller per feature group |
| Security module | Checks login, role and department before every action (FR-USR-06) | Denied attempts go to the audit log (FR-AUD-01) |
| Business services | Hold all the rules: BR-01 to BR-19, state changes, validation | Only layer that talks to the database |
| AI module | Builds the AI request, removes personal data, calls the AI Service, checks the answer, saves it in the AI log | AI never changes data by itself (BR-11) |
| Audit and history module | Writes history and audit entries after every change | Entries are append-only (BR-13, BR-14) |
| Notification module | Creates in-app messages and optional emails | A failed email never stops a workflow (FR-NTF error rules) |
| Data layer | Stores data and uploaded files | Passwords are stored as hashes (NFR-08) |

## 2.3 Proposed Technology

These choices can change. They follow the Phase 1 resources list (Python and/or JavaScript, a database, an AI/LLM service, GitHub, draw.io).

| Part | Choice | Why |
|---|---|---|
| Front end | HTML, CSS, JavaScript | Simple. Runs in any browser (Phase 1 assumption) |
| Back end | Python with Flask (or FastAPI) | Easy to learn. Good AI libraries |
| Database | SQLite for the prototype. Same tables work in PostgreSQL | No server to install. Synthetic data only |
| AI Service | Any free or student-tier language model with an embeddings API, used only through the adapter | Free tier only (Phase 1 constraint) |
| Email | SMTP or a mail API behind a mail adapter | Optional channel (FR-NTF-03) |
| Tests | pytest (back end) | Needed for the 60% coverage goal in Phase 7 |
| Version control | GitHub, small commits by each member | 10% of every phase mark |

## 2.4 AI Integration Design

The AI module is built around one interface, so the AI provider can be changed without touching the business services.

```mermaid
flowchart LR
    S["Business service<br/>for example Asset Service"] -->|"asks for a suggestion"| F["AI Facade"]
    F --> P["Privacy filter<br/>removes personal data (NFR-14)"]
    P --> A["AI Adapter<br/>one interface, many providers"]
    A -->|"request, max 15 s"| E["AI Service"]
    E -->|"answer and confidence"| A
    A --> V["Answer checker<br/>format and confidence threshold"]
    V --> L[("AI Output Log<br/>model id, model version,<br/>prompt version, confidence")]
    V -->|"suggestion or fallback"| F
    F -->|"result to show to the user"| S
    A -.->|"timeout or error"| FB["Fallback<br/>keyword search or rules"]
    FB -.-> F
```

| Rule | Design decision | Requirement |
|---|---|---|
| AI never decides | The AI module has no write access to assets, requests, transfers or approvals. It only returns suggestions | BR-11, FR-AI-X-14 to 17 |
| Show confidence | Every result carries a confidence value. Low confidence shows a warning | FR-AI-X-01, FR-AI-X-02 |
| Fallback | If the AI Service is slow (over 15 s) or down, the system uses keyword search or fixed rules and tells the user | NFR-04, FR-AI-X-08 to 10 |
| Log everything | Model id, model version, prompt version, time and result are saved for every output | FR-AI-X-05 to 07, FR-AI-X-11 to 13 |
| Override is saved | When a user changes a suggestion, the final value and reason are saved | FR-AI-X-03, FR-AI-X-04, BR-12 |
| No personal data | Names, emails and IDs of people are removed before the request leaves the system | NFR-14 |

## 2.5 Security Design

| Topic | Design | Requirement |
|---|---|---|
| Login | Email and password. Passwords of 12 to 128 characters, stored as hashes | FR-USR-03, FR-USR-04 |
| Roles | Nine roles (DR, AC, RQ, AD, PO, FO, MS, SO, SA). The permission matrix of Phase 3 (Section 2.4) is stored as a table and checked in the security module | BR-16, FR-USR-06 |
| Department rule | A user only changes records of their own department unless the role allows more | BR-16 |
| No self approval | The approver can never be the requester | BR-07 |
| Audit | Every change, approval, role change, export and denied attempt creates an audit row | BR-14, FR-AUD-01 |
| Upload safety | Photos only JPG, JPEG or PNG up to 5 MB. Documents only PDF or DOCX up to 10 MB | FR-AST-07, FR-AST-08 |

## 2.6 Deployment View

```mermaid
flowchart LR
    U["User browser<br/>laptop or desktop"] -->|"HTTPS"| W["Application server<br/>Flask app"]
    W --> D[("Database file or server")]
    W --> F["Upload folder"]
    W -->|"HTTPS"| A["AI Service (cloud)"]
    W -->|"SMTP or API"| M["Email service"]
```

For the prototype everything except the AI Service and email runs on one machine.

## 2.7 Module Layout and Ownership

```text
circular-campus/
  app/
    controllers/        one file per feature group
    services/           business rules (assets, marketplace, requests, approvals,
                        transfers, maintenance, users, reports, sustainability)
    ai/                 facade, privacy filter, adapter, fallback, output log
    security/           login, roles, department checks
    audit/              history and audit writers
    notifications/      in-app and email
    models/             database classes (see ER diagram)
  templates/ static/    web pages
  tests/
  docs/phase4-5/        this design
```

| Module | Owner (design part) |
|---|---|
| Asset, marketplace, request, search, reservation | Part 1 - Mohammed Al Ali |
| Approval, transfer, maintenance, history, end of life | Part 2 - Mubarak |
| Users, security, reports, notifications, audit | Part 3 - Mohammed Alketbi |
| AI module and sustainability | Part 4 - Abdulla |

---

# 3. Context Diagram

The context diagram shows the whole system as one process and everything outside it. It has no data stores. Every arrow has its own name.

<img width="2340" height="1300" alt="00_context_diagram" src="https://github.com/user-attachments/assets/96e19ed9-6db4-4f7e-8210-fd724ca9187b" />


| External entity | Type | Sends to the system | Receives from the system |
|---|---|---|---|
| Administrator (AD) | Person | Approval decisions | Approval requests and reports |
| Department Representative (DR) | Person | Asset and request data | Request status and reports |
| Asset Custodian (AC) | Person | Asset records | Asset history |
| Requester (RQ) | Person | Search and request details | Search results |
| Procurement Officer (PO) | Person | Report request | Purchase reports |
| Finance Officer (FO) | Person | Disposal approval | Cost reports |
| Maintenance Staff (MS) | Person | Repair records | Maintenance tickets |
| Sustainability Officer (SO) | Person | Recommendation review | Sustainability dashboard |
| Notification Service | External system | Delivery status | Notification messages |
| AI Service | External system | AI result | AI request |
| System Administrator (SA) | Person | Role settings | Audit logs |

---|---|---|---|
| Department Representative (DR) | Person | Asset, listing and request data | Request status and department reports |
| Asset Custodian (AC) | Person | Asset records and receipt confirmations | Asset history and inspection notices |
| Requester (RQ) | Person | Search queries and request details | Search results and reservation status |
| Administrator (AD) | Person | Approval decisions and account data | Approval requests, reports and audit logs |
| Procurement Officer (PO) | Person | Report requests | Reuse options and purchase reports |
| System Administrator (SA) | Person | Role settings and model settings | Audit logs and system status |
| Finance Officer (FO) | Person | Disposal approvals | Cost and savings reports |
| Maintenance Staff (MS) | Person | Inspection and repair records | Maintenance tickets |
| Sustainability Officer (SO) | Person | Recommendation reviews | Sustainability dashboard |
| AI Service | External system | AI results with confidence | AI requests without personal data |
| Notification Service | External system | Delivery status | Notification messages |

---

# 4. Data Flow Diagram, Level 0

## 4.1 DFD Rules Used

These come from the lecture slides:

- A process name starts with a verb. Every process has at least one input and one output.
- A data flow has one direction and a noun phrase as its label.
- No data flow goes between two data stores.
- No data flow goes between a data store and an external entity. A process is always in between.
- No data flow goes between two external entities.
- Every object has a unique name.

Drawing symbols in the Level 0 picture: a rounded box with a number on top is a process, a black number box with a name beside it is a data store, and a plain box is an external entity.

## 4.2 Level 0 Diagram

The picture follows the lecture notation. To keep it readable, roles of the same kind are grouped in two boxes (the context diagram above shows each role on its own): "Department Staff" means DR and AC, and "Procurement and Sustainability Officers" means PO and SO. The picture is large, so click it on GitHub to zoom in.

<img width="3512" height="1834" alt="00_level0_dfd" src="https://github.com/user-attachments/assets/5097741d-830f-4974-a4dd-02b791591178" />



## 4.3 Process List

| No. | Process | Main inputs | Main outputs | Data stores | Design part |
|---|---|---|---|---|---|
| 1.0 | Manage Users and Access | Account and role settings | User records, login result | D1 | Part 3 |
| 2.0 | Manage Assets | Asset details, suggestions | Asset records, asset events | D2, D3 | Part 1 |
| 3.0 | Handle Marketplace and Requests | Listing and request details, search queries | Listings, requests, search results | D4, D5 | Part 1 |
| 4.0 | Process Approvals and Transfers | Pending requests, decisions, receipt confirmation | Approval and transfer records | D6, D7 | Part 2 |
| 5.0 | Manage Maintenance and End of Life | Defect and repair records, disposal approval | Maintenance and end of life records | D8, D9 | Part 2 |
| 6.0 | Run AI Functions | Classification and match requests, reviews | Suggestions, recommendations, AI output records | D10 | Part 4 |
| 7.0 | Calculate Sustainability Figures | Reuse and repair data | Sustainability figures, dashboard | D11 | Part 4 |
| 8.0 | Generate Reports | Report requests, figures | Reports | D12 | Part 3 |
| 9.0 | Send Notifications | Notification events | Notification messages and records | D13 | Part 3 |
| 10.0 | Record Audit Events | Audit events | Audit entries, audit log view | D14 | Part 3 |

---

# 5. Entity Relationship Diagram

The ER diagram is the shared database design. Each member uses the tables that belong to their part (see the table after the diagram).

```mermaid
erDiagram
    DEPARTMENT ||--o{ USER : "has"
    DEPARTMENT ||--o{ ASSET : "owns"
    DEPARTMENT ||--o{ REQUEST : "makes"
    USER ||--o{ ASSET : "is custodian of"
    USER ||--o{ REQUEST : "submits"
    CATEGORY ||--o{ ASSET : "classifies"
    ASSET ||--o{ ASSET_MEDIA : "has"
    ASSET ||--o{ LISTING : "is published as"
    ASSET ||--o{ RESERVATION : "is reserved in"
    REQUEST ||--o{ RESERVATION : "creates"
    USER ||--o{ WATCHLIST_ITEM : "follows"
    ASSET ||--o{ WATCHLIST_ITEM : "is followed in"
    REQUEST ||--o{ APPROVAL : "needs"
    ASSET ||--o{ APPROVAL : "is subject of"
    USER ||--o{ APPROVAL : "decides"
    REQUEST ||--o| TRANSFER : "results in"
    ASSET ||--o{ TRANSFER : "moves in"
    ASSET ||--o{ MAINTENANCE_TICKET : "has"
    MAINTENANCE_TICKET ||--o{ REPAIR_RECORD : "contains"
    ASSET ||--o{ END_OF_LIFE_REQUEST : "ends with"
    ASSET ||--o{ ASSET_HISTORY : "records"
    USER ||--o{ AUDIT_LOG : "performs"
    USER ||--o{ NOTIFICATION : "receives"
    ASSET ||--o{ AI_OUTPUT : "gets"
    REQUEST ||--o{ AI_OUTPUT : "gets"
    AI_OUTPUT ||--o{ AI_OVERRIDE : "is changed by"
    AI_OUTPUT ||--o{ AI_FEEDBACK : "gets"
    REQUEST ||--o{ REUSE_EVENT : "causes"
    ASSET ||--o{ REUSE_EVENT : "is reused in"
    CATEGORY ||--o{ EMISSION_FACTOR : "has"
    USER ||--o{ REPORT : "generates"

    DEPARTMENT {
        int dept_id PK
        string name
        int rep_user_id FK
    }
    USER {
        int user_id PK
        string name
        string email UK
        string password_hash
        string role
        int dept_id FK
        string status
        boolean email_notifications
    }
    CATEGORY {
        int category_id PK
        string name
        string subcategory
    }
    ASSET {
        int asset_id PK
        string tag_number UK
        string name
        string description
        int category_id FK
        int quantity
        int owner_dept_id FK
        int custodian_id FK
        string location
        date purchase_date
        decimal est_value_aed
        string condition
        string material_type
        string status
        boolean active
    }
    ASSET_MEDIA {
        int media_id PK
        int asset_id FK
        string kind
        string file_path
        int size_kb
    }
    LISTING {
        int listing_id PK
        int asset_id FK
        int published_by FK
        datetime published_at
        datetime expires_at
        string status
    }
    REQUEST {
        int request_id PK
        int requester_id FK
        int dept_id FK
        string category
        string purpose
        string specifications
        int quantity
        string preferred_condition
        string urgency
        string location
        date required_date
        string status
    }
    RESERVATION {
        int reservation_id PK
        int asset_id FK
        int request_id FK
        int quantity
        datetime reserved_at
        datetime expires_at
        string status
    }
    WATCHLIST_ITEM {
        int watch_id PK
        int user_id FK
        int asset_id FK
        string saved_search
    }
    APPROVAL {
        int approval_id PK
        string action_type
        int asset_id FK
        int request_id FK
        int approver_id FK
        string decision
        string reason
        datetime decided_at
        string status
    }
    TRANSFER {
        int transfer_id PK
        int asset_id FK
        int request_id FK
        int from_dept_id FK
        int to_dept_id FK
        date handover_date
        string handover_location
        string status
        int received_by FK
        datetime received_at
        string discrepancy_note
    }
    MAINTENANCE_TICKET {
        int ticket_id PK
        int asset_id FK
        int reported_by FK
        int assigned_to FK
        string description
        datetime inspection_at
        string status
    }
    REPAIR_RECORD {
        int repair_id PK
        int ticket_id FK
        int performed_by FK
        string action
        decimal cost_aed
        date repair_date
    }
    END_OF_LIFE_REQUEST {
        int eol_id PK
        int asset_id FK
        string action
        string reason
        string alternatives_assessment
        string status
        string recipient
    }
    ASSET_HISTORY {
        int event_id PK
        int asset_id FK
        string event_type
        int actor_id FK
        datetime event_time
        string related_record
        string details
    }
    ROLE_PERMISSION {
        int permission_id PK
        string role
        string function_name
        boolean allowed
    }
    AUDIT_LOG {
        int audit_id PK
        int actor_id FK
        string action
        string record_ref
        string outcome
        string old_value
        string new_value
        datetime event_time
    }
    NOTIFICATION {
        int notification_id PK
        int user_id FK
        string event_type
        string message
        string status
        datetime created_at
    }
    AI_OUTPUT {
        int ai_output_id PK
        string function_name
        int asset_id FK
        int request_id FK
        string model_id
        string model_version
        string prompt_version
        decimal confidence
        string content
        datetime created_at
    }
    AI_OVERRIDE {
        int override_id PK
        int ai_output_id FK
        int user_id FK
        string final_value
        string reason
        datetime created_at
    }
    AI_FEEDBACK {
        int feedback_id PK
        int ai_output_id FK
        int user_id FK
        int rating
        string comment
    }
    REUSE_EVENT {
        int reuse_id PK
        int asset_id FK
        int request_id FK
        string event_type
        decimal avoided_value_aed
        datetime event_time
    }
    EMISSION_FACTOR {
        int factor_id PK
        int category_id FK
        decimal kg_co2e_per_unit
        string source
    }
    REPORT {
        int report_id PK
        string report_type
        int generated_by FK
        date period_start
        date period_end
        boolean ai_generated
        boolean reviewed
        string content
    }
```

## 5.1 Tables by Design Part

| Part | Tables | Data stores |
|---|---|---|
| Part 1 | CATEGORY, ASSET, ASSET_MEDIA, LISTING, REQUEST, RESERVATION, WATCHLIST_ITEM (kept in D5) | D2, D4, D5 |
| Part 2 | APPROVAL, TRANSFER, MAINTENANCE_TICKET, REPAIR_RECORD, END_OF_LIFE_REQUEST, ASSET_HISTORY | D3, D6, D7, D8, D9 |
| Part 3 | DEPARTMENT, USER, REPORT, NOTIFICATION, AUDIT_LOG | D1, D12, D13, D14 |
| Part 4 | AI_OUTPUT, AI_OVERRIDE, AI_FEEDBACK, REUSE_EVENT, EMISSION_FACTOR | D10, D11 |

## 5.2 Main Data Rules

| Rule | Table and column | Source |
|---|---|---|
| Asset ID is unique and created by the system | ASSET.asset_id | FR-AST-02 |
| Quantity is a whole number of 1 or more | ASSET.quantity, REQUEST.quantity | FR-AST-04, FR-REQ-03 |
| Estimated value is 0 AED or more | ASSET.est_value_aed | FR-AST-05 |
| Purchase date is not in the future | ASSET.purchase_date | FR-AST-06 |
| Urgency is only Low, Medium or High | REQUEST.urgency | FR-REQ-05 |
| A listing expires 30 days after publishing | LISTING.expires_at | FR-MKT-04 |
| A reservation expires 7 days after it is made if not approved | RESERVATION.expires_at | BR-04, FR-RSV-05 |
| Repair cost is not negative | REPAIR_RECORD.cost_aed | FR-MNT error rules |
| History and audit rows are never edited or deleted. A correction is a new row | ASSET_HISTORY, AUDIT_LOG | BR-13, BR-14, FR-HST-03, FR-AUD-03 |
| Approver is not the requester | APPROVAL.approver_id | BR-07 |
| One active transfer per asset | TRANSFER.asset_id + status | Phase 3, 6.2.3 |
| Emission factor is stored with its source | EMISSION_FACTOR.source | FR-SUS-25 |

---

# 6. State Models Used by the Design

The allowed states are the ones from Phase 3, Section 6.2. The classes and sequence diagrams in the member files use the same names.

| Object | States |
|---|---|
| Asset | Draft, Registered, Available / Published, Reserved, In Transfer, In Maintenance, Retired, Donated, Recycled, Disposed |
| Request | Draft, Submitted, Matched / Reserved, Approved, Rejected, Cancelled, Expired, Fulfilled |
| Transfer | Requested, Pending Approval, Approved, Rejected, Cancelled, Scheduled, In Transit, Received, Completed |
| Maintenance ticket | Reported, Inspected, Repair Approved, In Repair, Completed, Verified, Not Repairable |
| Reservation | Active, Expired, Released, Converted |
| Listing | Active, Withdrawn, Expired |

---



# Phase 4 & 5 - Part 1: Assets, Marketplace and Requests

Owner: Mohammed Al Ali Use cases: UC-01 to UC-10 (Register asset, Edit asset, Publish surplus asset, Withdraw listing, Submit request, Search and filter assets, Reserve asset, Track request, Cancel request, Save asset to watchlist) Requirement groups: FR-AST, FR-MKT, FR-REQ, FR-SRC, FR-RSV Data stores: D2 Assets, D4 Listings, D5 Requests and Reservations (watchlist items are kept in D5). D3 Asset History is written to, but it belongs to Part 2. Tables: CATEGORY, ASSET, ASSET_MEDIA, LISTING, REQUEST, RESERVATION, WATCHLIST_ITEM

Shared diagrams (architecture, the one Level 0 DFD, ER diagram) are in 00_architecture_and_shared_design.md.

---

## 1. Sequence Diagrams


### 1.1 UC-01 Register Asset

```mermaid
sequenceDiagram
    autonumber
    actor AC as Asset Custodian
    participant UI as Web Page
    participant AssetController
    participant Security
    participant AssetService
    participant AIFacade
    participant AIService as AI Service
    participant DB as Database
    participant Audit as History and Audit

    AC->>UI: Click "Register new asset"
    UI-->>AC: Show registration form
    AC->>UI: Enter details and photos, click Submit
    UI->>AssetController: POST /assets
    activate AssetController
    AssetController->>Security: checkPermission(user, "register asset")
    Security-->>AssetController: allowed
    AssetController->>AssetService: registerAsset(data)
    activate AssetService
    AssetService->>AssetService: validate fields, quantity, value, date, files
    alt a field is invalid
        AssetService-->>AssetController: list of invalid fields
        AssetController-->>UI: errors
        UI-->>AC: Highlight the fields
    else all fields are valid
        AssetService->>DB: find asset with same tag number
        DB-->>AssetService: result
        alt tag number already exists
            AssetService-->>UI: existing asset
            UI-->>AC: Show existing asset, cancel or correct
        else tag number is new
            AssetService->>AIFacade: suggestCategory(title, description, specs, image)
            activate AIFacade
            AIFacade->>AIService: classify (no personal data)
            alt answer within 15 seconds
                AIService-->>AIFacade: category, tags, confidence
                AIFacade-->>AssetService: suggestion and confidence
            else no answer in 15 seconds
                AIFacade-->>AssetService: no suggestion (fallback)
            end
            deactivate AIFacade
            AssetService-->>UI: suggestion (if any)
            UI-->>AC: Show category with confidence
            AC->>UI: Accept or change the category
            UI->>AssetService: confirmed category
            AssetService->>DB: save asset with status "Registered" and media
            DB-->>AssetService: asset ID
            AssetService->>Audit: record history and audit entries
            AssetService-->>AssetController: asset ID
            deactivate AssetService
            AssetController-->>UI: success
            deactivate AssetController
            UI-->>AC: Confirm and offer to publish
        end
    end
```

### 1.2 UC-02 Edit Asset

```mermaid
sequenceDiagram
    autonumber
    actor U as AC or DR
    participant UI as Web Page
    participant AssetController
    participant AssetService
    participant DB as Database
    participant Audit as History and Audit

    U->>UI: Open asset and click "Edit"
    UI->>AssetController: GET /assets/{id}
    AssetController->>AssetService: getAsset(id)
    AssetService->>DB: read asset
    DB-->>AssetService: current values
    AssetService-->>UI: asset data
    UI-->>U: Show edit form
    U->>UI: Change details and click "Save"
    UI->>AssetController: PUT /assets/{id}
    activate AssetController
    AssetController->>AssetService: updateAsset(id, data, version)
    activate AssetService
    AssetService->>AssetService: check permission and validate fields
    alt a field is invalid
        AssetService-->>AssetController: list of invalid fields
        AssetController-->>UI: errors
        UI-->>U: Highlight the fields
    else fields are valid
        AssetService->>DB: compare version number
        DB-->>AssetService: current version
        alt asset was changed by someone else
            AssetService-->>AssetController: conflict
            AssetController-->>UI: message
            UI-->>U: Show "Please reload the asset"
        else no conflict
            AssetService->>DB: save new values
            AssetService->>Audit: record old and new values
            AssetService-->>AssetController: done
            deactivate AssetService
            AssetController-->>UI: success
            deactivate AssetController
            UI-->>U: Show "Asset updated"
        end
    end
```

### 1.3 UC-03 Publish Surplus Asset

```mermaid
sequenceDiagram
    autonumber
    actor U as AC or DR
    participant UI as Web Page
    participant MarketplaceController
    participant MarketplaceService
    participant AIFacade
    participant DB as Database
    participant Audit as History and Audit

    U->>UI: Click "Publish as surplus"
    UI->>MarketplaceController: POST /listings/prepare
    activate MarketplaceController
    MarketplaceController->>MarketplaceService: prepare(assetId)
    activate MarketplaceService
    MarketplaceService->>DB: read asset status
    DB-->>MarketplaceService: status
    alt asset cannot be published (for example in transfer)
        MarketplaceService-->>MarketplaceController: refused
        MarketplaceController-->>UI: message
        UI-->>U: Show the reason
    else asset can be published
        MarketplaceService->>AIFacade: suggestTitleAndKeywords(asset)
        AIFacade-->>MarketplaceService: suggestion or fallback
        MarketplaceService-->>UI: publication form
        U->>UI: Review and confirm
        UI->>MarketplaceController: POST /listings
        MarketplaceController->>MarketplaceService: publish(assetId, data)
        MarketplaceService->>DB: look for similar active listings
        DB-->>MarketplaceService: result
        alt possible duplicate
            MarketplaceService-->>UI: warning with the existing listing
            UI-->>U: Ask to cancel or continue
        else no duplicate
            MarketplaceService->>DB: save listing "Active" (expires in 30 days)
            MarketplaceService->>Audit: record history entry
            MarketplaceService-->>MarketplaceController: listing ID
            deactivate MarketplaceService
            MarketplaceController-->>UI: success
            deactivate MarketplaceController
            UI-->>U: Show "Listing published"
        end
    end
```

### 1.4 UC-04 Withdraw Listing

```mermaid
sequenceDiagram
    autonumber
    actor U as AC or DR
    participant UI as Web Page
    participant MarketplaceController
    participant MarketplaceService
    participant DB as Database
    participant Audit as History and Audit
    participant Noti as Notification Module

    U->>UI: Click "Withdraw listing"
    UI->>MarketplaceController: POST /listings/{id}/withdraw
    activate MarketplaceController
    MarketplaceController->>MarketplaceService: withdraw(listingId)
    activate MarketplaceService
    MarketplaceService->>DB: read listing and related transfer
    DB-->>MarketplaceService: status
    alt an approved transfer exists
        MarketplaceService-->>MarketplaceController: blocked
        MarketplaceController-->>UI: message
        UI-->>U: Show "A transfer is already approved"
    else withdrawal is allowed
        MarketplaceService-->>UI: ask for a reason
        U->>UI: Enter reason and confirm
        UI->>MarketplaceService: confirm withdrawal
        MarketplaceService->>DB: set listing "Withdrawn"
        MarketplaceService->>Audit: record history entry
        MarketplaceService->>Noti: notify requesters with open reservations
        MarketplaceService-->>MarketplaceController: done
        deactivate MarketplaceService
        MarketplaceController-->>UI: success
        deactivate MarketplaceController
        UI-->>U: Show "Listing withdrawn"
    end
```

### 1.5 UC-05 Submit Request

```mermaid
sequenceDiagram
    autonumber
    actor RQ as Requester
    participant UI as Web Page
    participant RequestController
    participant RequestService
    participant AIFacade
    participant DB as Database
    participant Audit as History and Audit
    participant Noti as Notification Module

    RQ->>UI: Click "Create request"
    UI-->>RQ: Show request form
    RQ->>UI: Enter category, purpose, quantity, urgency, location, date
    UI->>RequestController: POST /requests
    activate RequestController
    RequestController->>RequestService: submitRequest(data)
    activate RequestService
    RequestService->>RequestService: validate (quantity 1 or more, date not in the past, urgency Low, Medium or High)
    alt data is invalid
        RequestService-->>RequestController: errors
        RequestController-->>UI: errors
        UI-->>RQ: Show invalid fields
    else data is valid
        RequestService->>DB: save request with status "Submitted"
        DB-->>RequestService: request ID
        RequestService->>Audit: record audit entry
        RequestService->>Noti: notify department representative
        RequestService->>AIFacade: findMatches(request)
        AIFacade-->>RequestService: ranked matches or fallback list
        RequestService-->>RequestController: request ID and matches
        deactivate RequestService
        RequestController-->>UI: success
        deactivate RequestController
        UI-->>RQ: Show request ID and suggested assets
    end
```

### 1.6 UC-06 Search and Filter Assets

```mermaid
sequenceDiagram
    autonumber
    actor RQ as Requester
    participant UI as Web Page
    participant SearchController
    participant Security
    participant SearchService
    participant DB as Database

    RQ->>UI: Type keywords and choose filters
    UI->>SearchController: GET /assets/search?q=...&filters=...
    activate SearchController
    SearchController->>Security: checkPermission(user, "search")
    Security-->>SearchController: allowed and visible departments
    SearchController->>SearchService: search(keywords, filters, sort)
    activate SearchService
    SearchService->>SearchService: check filters (minimum is not above maximum)
    alt filter range is invalid
        SearchService-->>SearchController: error message
        SearchController-->>UI: error
        UI-->>RQ: Show "Invalid range"
    else filters are valid
        SearchService->>DB: query published assets the user may see
        DB-->>SearchService: matching assets
        alt no assets found
            SearchService-->>SearchController: empty list
            SearchController-->>UI: empty list
            UI-->>RQ: Show "No matching resources found"
        else assets found
            SearchService->>SearchService: sort results
            SearchService-->>SearchController: result list
            deactivate SearchService
            SearchController-->>UI: result list
            deactivate SearchController
            UI-->>RQ: Show results
        end
    end
```

### 1.7 UC-07 Reserve Asset

```mermaid
sequenceDiagram
    autonumber
    actor RQ as Requester
    participant UI as Web Page
    participant ReservationController
    participant ReservationService
    participant DB as Database
    participant Audit as History and Audit
    participant Noti as Notification Module

    RQ->>UI: Click "Reserve" on an asset
    UI->>ReservationController: POST /reservations
    activate ReservationController
    ReservationController->>ReservationService: reserve(assetId, requestId, quantity)
    activate ReservationService
    ReservationService->>DB: read asset status and free quantity
    DB-->>ReservationService: status and quantity
    alt asset is not available or another active reservation exists
        ReservationService-->>ReservationController: rejected, asset is taken
        ReservationController-->>UI: message
        UI-->>RQ: Show "Asset is not available"
    else quantity is higher than free quantity
        ReservationService-->>ReservationController: rejected, not enough quantity
        ReservationController-->>UI: message
        UI-->>RQ: Show "Not enough quantity"
    else reservation is possible
        ReservationService->>DB: save reservation (expires in 7 days) and set asset "Reserved"
        DB-->>ReservationService: reservation ID
        ReservationService->>Audit: record history and audit entries
        ReservationService->>Noti: notify approver and owner
        ReservationService-->>ReservationController: reservation ID and expiry date
        deactivate ReservationService
        ReservationController-->>UI: success
        deactivate ReservationController
        UI-->>RQ: Show reservation and expiry date
    end
```

### 1.8 UC-08 Track Request

```mermaid
sequenceDiagram
    autonumber
    actor RQ as Requester
    participant UI as Web Page
    participant RequestController
    participant RequestService
    participant DB as Database

    RQ->>UI: Open "My requests"
    UI->>RequestController: GET /requests/mine
    RequestController->>RequestService: getMyRequests(userId)
    RequestService->>DB: read requests of the user
    DB-->>RequestService: list
    alt user has no requests
        RequestService-->>UI: empty list
        UI-->>RQ: Show "No requests yet"
    else requests found
        RequestService-->>UI: request list
        UI-->>RQ: Show requests with status
        RQ->>UI: Select a request
        UI->>RequestController: GET /requests/{id}
        RequestController->>RequestService: getStatus(id)
        RequestService->>DB: read status and history
        DB-->>RequestService: details
        RequestService-->>UI: status, history and next step
        UI-->>RQ: Show progress
    end
```

### 1.9 UC-09 Cancel Request

```mermaid
sequenceDiagram
    autonumber
    actor RQ as Requester
    participant UI as Web Page
    participant RequestController
    participant RequestService
    participant DB as Database
    participant Audit as History and Audit
    participant Noti as Notification Module

    RQ->>UI: Click "Cancel request"
    UI->>RequestController: POST /requests/{id}/cancel
    activate RequestController
    RequestController->>RequestService: cancelRequest(id)
    activate RequestService
    RequestService->>DB: read request status
    DB-->>RequestService: status
    alt a transfer is already approved
        RequestService-->>RequestController: blocked
        RequestController-->>UI: message
        UI-->>RQ: Show "Ask an administrator to cancel"
    else cancellation is allowed
        RequestService-->>UI: ask for confirmation
        RQ->>UI: Confirm
        UI->>RequestService: confirm cancellation
        RequestService->>DB: set request "Cancelled", release any reservation
        RequestService->>Audit: record history entry
        RequestService->>Noti: notify asset owner
        RequestService-->>RequestController: done
        deactivate RequestService
        RequestController-->>UI: success
        deactivate RequestController
        UI-->>RQ: Show "Request cancelled"
    end
```

### 1.10 UC-10 Save Asset to Watchlist

```mermaid
sequenceDiagram
    autonumber
    actor RQ as Requester
    participant UI as Web Page
    participant SearchController
    participant SearchService
    participant DB as Database

    RQ->>UI: Click "Watch" on an asset or a search
    UI->>SearchController: POST /watchlist
    SearchController->>SearchService: saveToWatchlist(userId, item)
    SearchService->>DB: check for an existing watch
    DB-->>SearchService: result
    alt already watched
        SearchService-->>UI: already in the watchlist
        UI-->>RQ: Offer to stop watching
    else new watch
        SearchService->>DB: save watchlist item
        SearchService-->>UI: saved
        UI-->>RQ: Show "Added to your watchlist"
    end
```

### 1.11 Reservation Expiry (runs every day)

This is the system action behind FR-RSV-05 and BR-04.

```mermaid
sequenceDiagram
    autonumber
    participant Timer as Daily Timer
    participant ReservationService
    participant DB as Database
    participant Audit as History and Audit
    participant Noti as Notification Module

    Timer->>ReservationService: expireOldReservations()
    activate ReservationService
    ReservationService->>DB: find active reservations older than 7 days without approval
    DB-->>ReservationService: list
    loop for each reservation in the list
        ReservationService->>DB: set reservation "Expired" and asset "Available / Published"
        ReservationService->>Audit: record history entry
        ReservationService->>Noti: notify requester
    end
    deactivate ReservationService
```

---

---

## 2. Class Diagram

Entity classes match the ER tables. Service classes hold the rules (BR and FR). Controller classes only receive requests and call one service.

```mermaid
classDiagram
    class Category {
        +int categoryId
        +String name
        +String subcategory
    }
    class Asset {
        +int assetId
        +String tagNumber
        +String name
        +String description
        +int quantity
        +String location
        +Date purchaseDate
        +Decimal estValueAed
        +String condition
        +String materialType
        +AssetStatus status
        +boolean active
        +isAvailable() boolean
        +reserve(qty) void
        +deactivate() void
    }
    class AssetMedia {
        +int mediaId
        +String kind
        +String filePath
        +int sizeKb
        +isValidType() boolean
        +isValidSize() boolean
    }
    class Listing {
        +int listingId
        +DateTime publishedAt
        +DateTime expiresAt
        +ListingStatus status
        +withdraw() void
        +expire() void
    }
    class Request {
        +int requestId
        +String category
        +String purpose
        +String specifications
        +int quantity
        +String preferredCondition
        +Urgency urgency
        +String location
        +Date requiredDate
        +RequestStatus status
        +cancel() void
        +canEdit() boolean
    }
    class Reservation {
        +int reservationId
        +int quantity
        +DateTime reservedAt
        +DateTime expiresAt
        +ReservationStatus status
        +isExpired() boolean
        +release() void
    }
    class WatchlistItem {
        +int watchId
        +String savedSearch
    }
    class AssetStatus {
        <<enumeration>>
        Draft
        Registered
        AvailablePublished
        Reserved
        InTransfer
        InMaintenance
        Retired
        Donated
        Recycled
        Disposed
    }
    class RequestStatus {
        <<enumeration>>
        Draft
        Submitted
        MatchedReserved
        Approved
        Rejected
        Cancelled
        Expired
        Fulfilled
    }
    class Urgency {
        <<enumeration>>
        Low
        Medium
        High
    }
    class ListingStatus {
        <<enumeration>>
        Active
        Withdrawn
        Expired
    }
    class ReservationStatus {
        <<enumeration>>
        Active
        Expired
        Released
        Converted
    }

    class AssetService {
        +registerAsset(data) Asset
        +updateAsset(id, data) Asset
        +deactivateAsset(id) void
        +validate(data) List
        +findDuplicate(tagNumber) Asset
    }
    class MarketplaceService {
        +publish(assetId) Listing
        +withdraw(listingId) void
        +expireOldListings() void
    }
    class RequestService {
        +submitRequest(data) Request
        +editRequest(id, data) Request
        +cancelRequest(id) void
        +getStatus(id) RequestStatus
    }
    class ReservationService {
        +reserve(assetId, requestId, qty) Reservation
        +release(id) void
        +expireOldReservations() void
    }
    class SearchService {
        +search(keywords, filters, sort) List
        +saveToWatchlist(userId, assetOrSearch) WatchlistItem
    }
    class AssetController {
        +postAsset() Response
        +putAsset() Response
        +deleteAsset() Response
    }
    class MarketplaceController {
        +postListing() Response
        +deleteListing() Response
    }
    class RequestController {
        +postRequest() Response
        +putRequest() Response
        +cancelRequest() Response
        +getRequests() Response
    }
    class SearchController {
        +getSearch() Response
        +postWatch() Response
    }

    Category "1" --> "0..*" Asset : classifies
    Asset "1" --> "0..*" AssetMedia : has
    Asset "1" --> "0..*" Listing : is published as
    Asset "1" --> "0..*" Reservation : is reserved in
    Request "1" --> "0..*" Reservation : creates
    Asset "1" --> "0..*" WatchlistItem : is followed in
    Asset --> AssetStatus
    Request --> RequestStatus
    Request --> Urgency
    Listing --> ListingStatus
    Reservation --> ReservationStatus

    AssetController ..> AssetService
    MarketplaceController ..> MarketplaceService
    RequestController ..> RequestService
    RequestController ..> ReservationService
    SearchController ..> SearchService
    AssetService ..> Asset
    MarketplaceService ..> Listing
    RequestService ..> Request
    ReservationService ..> Reservation
    SearchService ..> Asset
    SearchService ..> WatchlistItem
```

| Class | Role | Rule it enforces |
| --- | --- | --- |
| AssetService | Register, edit, deactivate assets | FR-AST-01 to 10, BR-01, BR-02, BR-13 |
| MarketplaceService | Publish, withdraw, expire listings | FR-MKT-01 to 04, BR-05 |
| RequestService | Submit, edit, cancel, track requests | FR-REQ-01 to 09 |
| ReservationService | Reserve and expire reservations | FR-RSV-01 to 05, BR-04 |
| SearchService | Search, filter, sort, watchlist | FR-SRC-01 to 07, NFR-02, BR-16 |

---

## 3. User Interface Mockups

These are simple wireframes. Real screens will use the same fields and buttons.

### 3.1 Register Asset (UC-01)

```text
+----------------------------------------------------------------------+
|  Circular Campus        [Marketplace] [My assets] [Requests]  (AC) v |
+----------------------------------------------------------------------+
|  Register new asset                                                  |
| Class diagram |
|  Name *            [__________________________]                      |
|  Tag number *      [______________]    (must be new)                 |
|  Description       [__________________________________________]      |
|  Category *        [ Select v ]   AI suggestion: [Laboratory chairs]  |
|                                   Confidence: 82 %  [Accept][Change] |
|  Quantity *        [ 1 ]    Estimated value (AED) [ 0.00 ]           |
|  Owner / Dept *    [ Computer Science v ]                            |
|  Location *        [______________]  Purchase date [ yyyy-mm-dd ]    |
|  Condition *       ( ) Good  ( ) Fair  ( ) Needs repair              |
|  Availability *    ( ) In use  ( ) Surplus                           |
|  Photos            [Choose files]  JPG, JPEG, PNG, max 5 MB          |
|  Documents         [Choose files]  PDF, DOCX, max 10 MB              |
| Class diagram |
|  * required                       [ Save as draft ]  [ Register ]    |
+----------------------------------------------------------------------+
```

### 3.2 Marketplace and Search (UC-06, UC-10)

```text
+----------------------------------------------------------------------+
|  Marketplace                                                         |
|  Search: [ laboratory seating ____________ ] [Search]                |
| Class diagram |
|  Filters            |  Sort by: [ Publication date v ]               |
|  Category   [ v ]   |  ------------------------------------------   |
|  Condition  [ v ]   |  [img] Lab bench stool        Qty 20          |
|  Department [ v ]   |        Computer Science, Good, AED 150 each    |
|  Location   [ v ]   |        [View] [Reserve] [Watch]                |
|  Quantity   [ ]-[ ] |  ------------------------------------------   |
|  Value AED  [ ]-[ ] |  [img] Office chair           Qty 6           |
|  Age (years)[ ]-[ ] |        Business, Fair, AED 90 each             |
|  Status     [ v ]   |        [View] [Reserve] [Watch]                |
|  [Apply filters]    |  ------------------------------------------   |
|  [Save this search] |  Page 1 of 3          [Prev] [Next]            |
+----------------------------------------------------------------------+
|  When nothing matches: "No matching resources found"                 |
+----------------------------------------------------------------------+
```

### 3.3 Create Request (UC-05)

```text
+----------------------------------------------------------------------+
|  New resource request                                                |
| Class diagram |
|  Category *        [ Furniture v ]                                   |
|  Purpose *         [______________________________________]          |
|  Specifications    [______________________________________]          |
|  Quantity *        [ 10 ]                                            |
|  Preferred cond.   [ Good v ]                                        |
|  Urgency *         ( ) Low   ( ) Medium   ( ) High                   |
|  Location *        [______________]  Required date * [ yyyy-mm-dd ]  |
| Class diagram |
|  [ Cancel ]                                [ Submit request ]        |
+----------------------------------------------------------------------+
|  After submit: "Request R-0042 created. Suggested assets:"           |
|   1. Lab bench stool (match 91 %)  [View]                            |
+----------------------------------------------------------------------+
```

### 3.4 My Requests and Reservations (UC-08, UC-09)

```text
+----------------------------------------------------------------------+
|  My requests                                                         |
| Class diagram |
|  ID      Asset / Need        Status               Reserved until     |
|  R-0042  Lab seating x10     Matched / Reserved   2026-11-05         |
|  R-0039  Projector x1        Approved             -                  |
|  R-0031  Monitors x20        Submitted            -                  |
| Class diagram |
|  [View details]  [Edit]  [Cancel request]                            |
| Class diagram |
|  Cancel is blocked once a transfer is approved:                      |
|  "Ask an administrator to cancel this request."                      |
+----------------------------------------------------------------------+
```

---

## 4. Traceability

| Diagram | Use case | Requirements |
| --- | --- | --- |
| Sequence 1.1 | UC-01 Register asset | FR-AST-01 to 08, FR-AI-01 to 15, NFR-04 |
| Sequence 1.2 | UC-02 Edit asset | FR-AST-09, BR-13 |
| Sequence 1.3 | UC-03 Publish surplus asset | FR-MKT-01, FR-MKT-02, FR-MKT-04 |
| Sequence 1.4 | UC-04 Withdraw listing | FR-MKT-03 |
| Sequence 1.5 | UC-05 Submit request | FR-REQ-01 to 06 |
| Sequence 1.6 | UC-06 Search and filter assets | FR-SRC-01 to 05 |
| Sequence 1.7, 1.11 | UC-07 Reserve asset | FR-RSV-01 to 05 |
| Sequence 1.8 | UC-08 Track request | FR-REQ-09 |
| Sequence 1.9 | UC-09 Cancel request | FR-REQ-07, FR-REQ-08 |
| Sequence 1.10 | UC-10 Save asset to watchlist | FR-SRC-06, FR-SRC-07 |
| Class diagram (AssetService) | Deactivate asset (part of UC-02) | FR-AST-10 |




# Phase 4 & 5 — Part 2: Approvals, Transfers, Maintenance and End-of-Life

**Project:** Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System  
**Course:** COSC336 — Introduction to Software Engineering  
**Group:** 5  
**Contributor:** Mubarak Saif Mubarak Jarash Alkhyeli  

## 1. Scope and Design Basis

This section covers eight use cases: **UC-11** Approve or Reject Transfer, **UC-12** Confirm Receipt, **UC-13** Report Defect, **UC-14** Record Repair, **UC-15** View Asset History, **UC-16** Approve Disposal, **UC-24** Schedule Inspection, and **UC-25** Approve Donation or Recycling.

The designs trace to **FR-APR, FR-TRF, FR-MNT, FR-HST, FR-DSP, FR-USR, FR-NTF,** and **FR-AUD** in Phase 3.

Relevant database tables are `APPROVAL`, `TRANSFER`, `MAINTENANCE_TICKET`, `REPAIR_RECORD`, `END_OF_LIFE_REQUEST`, and `ASSET_HISTORY`.

The shared data stores are D3 Asset History, D6 Approvals, D7 Transfers, D8 Maintenance Records, and D9 End-of-Life Requests.

The transfer and maintenance state models are in Phase 3 Sections 6.2.1 and 6.2.2, respectively.

The team's consolidated architecture and entity-relationship model belong in `00_architecture_and_shared_design.md`.

### 1.1 Key Design Rules

- The owning Department Representative (DR) must approve asset release before the Administrator (AD) can give final transfer approval.
- A rejection requires a reason containing at least 10 characters.
- Each completed approval stage stores the approver, decision, timestamp, and reason when applicable.
- A transfer must receive the required approvals before scheduling and handover.
- The receiving Requester (RQ) confirms receipt before custody and location are updated.
- Assets under repair or involved in conflicting active transfers cannot be transferred.
- Repair work requires Administrator authorisation, and a separate authorised user verifies completed repairs.
- Disposal requires Administrator and Finance Officer approval. Donation and recycling require Administrator approval.
- All important decisions are recorded in the system's history and audit records.

## 2. Context Diagram

The context diagram shows the interactions between the Circular Campus System and its external users. The system is represented as a single process, while each actor exchanges relevant information with it.

```mermaid
flowchart LR
    RQ[Requester]
    DR[Department Representative]
    AC[Asset Custodian]
    AD[Administrator]
    MS[Maintenance Staff]
    FO[Finance Officer]
    SA[System Administrator]
    SO[Sustainability Officer]
    PO[Procurement Officer]
    SYS((Circular Campus System))

    RQ -->|Asset requests, defect reports, receipt confirmation| SYS
    SYS -->|Matches, request status, notifications| RQ

    DR -->|Release approval, handover arrangements| SYS
    SYS -->|Approval tasks, transfer updates| DR

    AC -->|Asset records, handover information, defect reports| SYS
    SYS -->|Assigned transfers, asset status| AC

    AD -->|Final approval or rejection decisions| SYS
    SYS -->|Approval queue, exceptions, reports| AD

    MS -->|Inspection and repair information| SYS
    SYS -->|Tickets and assignments| MS

    FO -->|Disposal approval or rejection| SYS
    SYS -->|Disposal approval requests| FO

    SA -->|Account and role changes| SYS
    SYS -->|User and access records| SA

    SO -->|Sustainability report requests| SYS
    SYS -->|Reuse and sustainability indicators| SO

    PO -->|Procurement and reuse enquiries| SYS
    SYS -->|Existing asset and reuse information| PO
```

The context diagram focuses on the system boundary and its external interactions. Internal components such as controllers, services, databases, and the notification module are not shown.

## 3. Sequence Diagrams

The following sequence diagrams describe how the main components of the system interact to complete each use case.

### 3.1 UC-11 — Approve or Reject Transfer

The Administrator reviews a pending transfer request and chooses to approve or reject it. Approval requires the owning department's release permission and a valid asset status.

```mermaid
sequenceDiagram
    autonumber
    actor AD as Administrator
    participant UI as Approval Page
    participant C as Approval Controller
    participant S as Approval Service
    participant DB as Database
    participant N as Notification Module

    AD->>UI: Open pending transfer requests
    UI->>C: Get pending requests
    C->>S: Validate AD session and permissions

    alt Access denied
        S-->>C: Permission error
        C-->>UI: Access denied
        UI-->>AD: Display error
    else Authorised
        S->>DB: Read pending approvals
        DB-->>S: Request list
        S-->>C: Pending requests
        C-->>UI: Display request list

        AD->>UI: Select request and submit decision
        UI->>C: Send decision and optional reason
        C->>S: Validate request and decision
        S->>DB: Read current request, approvals, asset
        DB-->>S: Current records

        alt Request is not pending or user is not allowed
            S-->>C: Decision blocked
            C-->>UI: Explain restriction

        else Rejection selected
            alt Reason shorter than 10 characters
                S-->>C: Invalid reason
                C-->>UI: Ask for valid reason
            else Valid reason
                S->>DB: Save rejection, reason and audit record
                DB-->>S: Rejection saved
                S->>N: Create rejection notifications
                S-->>C: Transfer rejected
                C-->>UI: Display confirmation
            end

        else Approval selected
            S->>DB: Check DR release and conflicting asset states
            DB-->>S: Validation outcome

            alt Release approval missing or asset unavailable
                S-->>C: Approval blocked
                C-->>UI: Display reason
            else All conditions satisfied
                S->>DB: Save AD approval and mark transfer Approved
                S->>DB: Save approver, time and audit entry
                DB-->>S: Transaction saved
                S->>N: Create approval notifications
                S-->>C: Transfer approved for scheduling
                C-->>UI: Display confirmation
            end
        end
    end
```

A pending approval older than 48 hours is flagged as overdue, and the Administrator receives a notification according to FR-APR-06.

### 3.2 UC-12 — Confirm Receipt

The receiving Requester confirms that the asset has arrived. The system updates ownership and location only after successful confirmation.

```mermaid
sequenceDiagram
    autonumber
    actor RQ as Receiving Requester
    participant UI as Transfer Page
    participant C as Transfer Controller
    participant S as Transfer Service
    participant A as Asset Service
    participant DB as Database
    participant N as Notification Module

    RQ->>UI: Open transfer and confirm receipt or report issue
    UI->>C: Submit receipt outcome and optional evidence
    C->>S: Check user role and receiving department
    S->>DB: Read transfer and its current state
    DB-->>S: Transfer details

    alt Wrong user or transfer not In Transit
        S-->>C: Action blocked
        C-->>UI: Show restriction

    else Damaged or incorrect asset reported
        S->>DB: Record discrepancy and remain In Transit
        S->>N: Notify responsible staff and AD
        S-->>C: Discrepancy recorded
        C-->>UI: Show unresolved status

    else Correct receipt confirmed
        S->>DB: Record receipt and set Received
        S->>A: Finalise custody and location change
        A->>DB: Save new and previous custodian and location
        DB-->>A: Asset updated
        A-->>S: Update complete
        S->>DB: Set transfer Completed and request Fulfilled
        S->>DB: Add asset history and audit records
        S->>N: Notify previous custodian and requester
        S-->>C: Receipt completed
        C-->>UI: Show confirmation
    end
```

### 3.3 UC-13 — Report Defect

An Asset Custodian or Requester reports a problem with an existing asset. The system creates a maintenance ticket and notifies the maintenance team.

```mermaid
sequenceDiagram
    autonumber
    actor U as Custodian or Requester
    participant UI as Asset Page
    participant C as Maintenance Controller
    participant S as Maintenance Service
    participant DB as Database
    participant N as Notification Module

    U->>UI: Open asset and report defect
    UI-->>U: Display defect form
    U->>UI: Enter description, condition and optional photo
    UI->>C: Submit defect report
    C->>S: Validate user and defect information
    S->>DB: Check asset exists
    DB-->>S: Asset record or not found

    alt Invalid asset or incomplete information
        S-->>C: Validation error
        C-->>UI: Display error

    else Valid report
        S->>DB: Create ticket with status Reported
        S->>DB: Mark asset unavailable for new reservations or transfers
        S->>DB: Save defect history and audit event
        S->>N: Notify maintenance team
        S-->>C: Ticket ID
        C-->>UI: Show ticket confirmation
    end
```

### 3.4 UC-24 — Schedule Inspection

Maintenance Staff schedules an inspection for an existing defect ticket. The system checks the ticket and asset status before saving the schedule.

```mermaid
sequenceDiagram
    autonumber
    actor MS as Maintenance Staff
    participant UI as Maintenance Page
    participant C as Maintenance Controller
    participant S as Maintenance Service
    participant DB as Database
    participant N as Notification Module

    MS->>UI: Open reported ticket and choose inspection time
    UI->>C: Submit assigned staff, date and time
    C->>S: Validate assignment and ticket
    S->>DB: Read ticket, asset and existing schedule
    DB-->>S: Current records

    alt Invalid ticket, staff, date or conflicting transfer
        S-->>C: Scheduling blocked
        C-->>UI: Display correction needed

    else Details valid
        S->>DB: Save inspection schedule and assignee
        S->>DB: Record scheduling audit event
        S->>N: Notify assigned staff and custodian
        S-->>C: Inspection scheduled
        C-->>UI: Display confirmation
    end
```

### 3.5 UC-14 — Record Repair

The assigned Maintenance Staff records the repair details, including the work performed, cost, and repair result.

```mermaid
sequenceDiagram
    autonumber
    actor MS as Assigned Maintenance Staff
    participant UI as Maintenance Page
    participant C as Maintenance Controller
    participant S as Maintenance Service
    participant DB as Database
    participant N as Notification Module

    MS->>UI: Open ticket and submit repair details
    UI->>C: Send work, parts, cost and result
    C->>S: Validate staff and repair details
    S->>DB: Read ticket, assignee and approval state
    DB-->>S: Current ticket

    alt Not assigned or repair not authorised
        S-->>C: Permission or approval error
        C-->>UI: Display restriction

    else Negative cost or incomplete details
        S-->>C: Invalid repair information
        C-->>UI: Request correction

    else Valid repair
        S->>DB: Save repair action and non-negative AED cost

        alt Repair work completed
            S->>DB: Set ticket Completed and await verification
        else Not repairable
            S->>DB: Set ticket Not Repairable with reason
        else Further work needed
            S->>DB: Keep ticket In Repair
        end

        S->>DB: Record repair history and audit entry
        S->>N: Notify custodian and relevant staff
        S-->>C: Repair record saved
        C-->>UI: Display updated ticket
    end
```

A completed repair must be verified by another authorised Maintenance Staff member or Asset Custodian before the asset becomes available again.

### 3.6 UC-15 — View Asset History

An authorised user opens an asset's history to review previous activities, including transfers, inspections, and repairs.

```mermaid
sequenceDiagram
    autonumber
    actor U as Authorised User
    participant UI as Asset Page
    participant C as History Controller
    participant S as History Service
    participant DB as Database

    U->>UI: Open asset history
    UI->>C: Request history for asset
    C->>S: Check role and access to asset

    alt Access denied
        S->>DB: Save denied-access audit event
        S-->>C: Access denied
        C-->>UI: Display restriction

    else Access granted
        S->>DB: Read ordered asset history records
        DB-->>S: Events with timestamps and references
        S-->>C: History timeline
        C-->>UI: Display dated events and linked records
    end
```

Asset history records are read-only. Corrections are stored as new entries referring to the original event.

### 3.7 UC-16 — Approve Disposal

The Administrator reviews a disposal request and its alternatives assessment. Both Administrator and Finance Officer approval are required before disposal can proceed.

```mermaid
sequenceDiagram
    autonumber
    actor AD as Administrator
    actor FO as Finance Officer
    participant UI as End-of-Life Page
    participant C as End-of-Life Controller
    participant S as End-of-Life Service
    participant DB as Database
    participant N as Notification Module

    AD->>UI: Review disposal request and alternatives
    UI->>C: Submit AD decision
    C->>S: Check AD permissions and request
    S->>DB: Read asset, request and alternatives assessment
    DB-->>S: Current records

    alt Invalid assessment or active repair or transfer
        S-->>C: Decision blocked
        C-->>UI: Display reason

    else AD rejects with valid reason
        S->>DB: Save rejection and audit record
        S->>N: Notify requester and custodian
        S-->>C: Rejected
        C-->>UI: Display outcome

    else AD approves
        S->>DB: Record AD approval and wait for FO decision
        S->>N: Notify Finance Officer

        FO->>UI: Review disposal and submit decision
        UI->>C: Submit FO decision and optional reason
        C->>S: Validate FO role, state and decision

        alt FO rejection reason missing or invalid
            S-->>C: Request valid reason
            C-->>UI: Display validation message

        else FO rejects
            S->>DB: Save FO rejection and audit record
            S->>N: Notify relevant users
            S-->>C: Disposal rejected
            C-->>UI: Display outcome

        else FO approves
            S->>DB: Save FO approval and audit record
            S->>N: Notify staff that disposal is authorised
            S-->>C: Approved for disposal
            C-->>UI: Display authorisation

            Note over S,DB: After confirmation that disposal occurred

            S->>DB: Record completion, destination and date
            S->>DB: Mark asset Disposed and remove listing
            S->>DB: Add asset history and audit entry
        end
    end
```

### 3.8 UC-25 — Approve Donation or Recycling

The Administrator reviews a donation or recycling request. Unlike disposal, these actions require Administrator approval without a separate Finance Officer decision.

```mermaid
sequenceDiagram
    autonumber
    actor AD as Administrator
    participant UI as End-of-Life Page
    participant C as End-of-Life Controller
    participant S as End-of-Life Service
    participant DB as Database
    participant N as Notification Module

    AD->>UI: Open donation or recycling request
    UI->>C: Submit AD approval or rejection
    C->>S: Validate AD role, reason and request state
    S->>DB: Read request and asset status
    DB-->>S: Current records

    alt Active repair, transfer, or invalid request
        S-->>C: Action blocked
        C-->>UI: Display reason

    else AD rejects
        alt Rejection reason shorter than 10 characters
            S-->>C: Invalid reason
            C-->>UI: Ask for valid reason
        else Valid reason
            S->>DB: Save rejection and audit entry
            S->>N: Notify relevant users
            S-->>C: Rejected
            C-->>UI: Display outcome
        end

    else AD approves
        S->>DB: Save approval and audit entry
        S->>N: Notify responsible staff
        S-->>C: Approved for action
        C-->>UI: Display authorisation

        Note over S,DB: After confirmation that action occurred

        S->>DB: Record date and destination or recipient
        S->>DB: Mark asset Donated or Recycled and remove listing
        S->>DB: Add asset history and audit entry
    end
```

## 4. Class Diagram

The class diagram represents the main entities and services responsible for approval workflows, asset transfers, maintenance, and end-of-life management.

```mermaid
classDiagram
    class Approval {
        +int approvalId
        +String actionType
        +int assetId
        +int requestId
        +int approverId
        +String decision
        +String reason
        +DateTime decidedAt
        +String status
        +boolean overdueFlag
        +approve(userId) void
        +reject(userId, reason) void
    }

    class Transfer {
        +int transferId
        +int assetId
        +int requestId
        +int fromDeptId
        +int toDeptId
        +Date handoverDate
        +String handoverLocation
        +String status
        +int receivedBy
        +DateTime receivedAt
        +String discrepancyNote
        +schedule(date, location) void
        +markInTransit() void
        +confirmReceipt(userId) void
        +reportDiscrepancy(note) void
    }

    class MaintenanceTicket {
        +int ticketId
        +int assetId
        +int reportedBy
        +int assignedTo
        +String description
        +DateTime inspectionAt
        +String status
        +scheduleInspection(staff, dateTime) void
        +approveRepair(adminId) void
        +verify(userId) void
        +markNotRepairable() void
    }

    class RepairRecord {
        +int repairId
        +int ticketId
        +int performedBy
        +String action
        +Decimal costAed
        +Date repairDate
        +String result
        +isCostValid() boolean
    }

    class EndOfLifeRequest {
        +int eolId
        +int assetId
        +String action
        +String reason
        +String alternativesAssessment
        +String recipient
        +String status
        +hasAssessment() boolean
        +needsFinanceApproval() boolean
        +completeAction() void
    }

    class AssetHistoryEvent {
        +int eventId
        +int assetId
        +String eventType
        +int actorId
        +DateTime eventTime
        +String relatedRecord
        +String details
    }

    class ApprovalService {
        +createApproval(action, assetId, requestId) Approval
        +getPending() List
        +decide(id, decision, reason, userId) Approval
        +markOverdueApprovals() void
    }

    class TransferService {
        +schedule(id, date, location) Transfer
        +confirmReceipt(id, result, note) Transfer
        +reportDiscrepancy(id, note) void
    }

    class MaintenanceService {
        +reportDefect(assetId, description, condition) MaintenanceTicket
        +scheduleInspection(ticketId, staff, dateTime) void
        +recordRepair(ticketId, details) RepairRecord
        +verifyRepair(ticketId, userId) void
    }

    class EndOfLifeService {
        +createRequest(assetId, action, reason) EndOfLifeRequest
        +adminDecision(id, decision, reason) void
        +financeDecision(id, decision, reason) void
        +completeAction(id, details) void
    }

    class HistoryService {
        +record(assetId, type, actorId, reference) AssetHistoryEvent
        +getHistory(assetId) List
    }

    class ApprovalController {
        +getPending() Response
        +postDecision() Response
    }

    class TransferController {
        +postReceipt() Response
    }

    class MaintenanceController {
        +postTicket() Response
        +postInspection() Response
        +postRepair() Response
    }

    class EndOfLifeController {
        +postAdminDecision() Response
        +postFinanceDecision() Response
    }

    class HistoryController {
        +getHistory() Response
    }

    MaintenanceTicket "1" --> "0..*" RepairRecord : includes
    Transfer "1" --> "1..*" Approval : requires

    ApprovalController ..> ApprovalService
    TransferController ..> TransferService
    MaintenanceController ..> MaintenanceService
    EndOfLifeController ..> EndOfLifeService
    HistoryController ..> HistoryService

    ApprovalService ..> Approval
    ApprovalService ..> TransferService
    TransferService ..> Transfer
    TransferService ..> HistoryService

    MaintenanceService ..> MaintenanceTicket
    MaintenanceService ..> RepairRecord

    EndOfLifeService ..> EndOfLifeRequest
    EndOfLifeService ..> ApprovalService
    HistoryService ..> AssetHistoryEvent
```

### 4.1 Class Responsibilities

| Class | Main Responsibility | Related Requirements |
|---|---|---|
| ApprovalService | Handles final decisions, release checks, overdue approvals and approval records | FR-APR-01–07 |
| TransferService | Manages scheduling, receipt confirmation, discrepancies and transfer completion | FR-TRF-01–05 |
| MaintenanceService | Manages defect tickets, inspections, repair records and verification | FR-MNT-01–05 |
| EndOfLifeService | Handles donation, recycling and disposal approval and completion | FR-DSP-01–05 |
| HistoryService | Records and retrieves asset history without modifying previous events | FR-HST-01–03 |

## 5. User Interface Mockups

The following interface mockups show the main pages used for approvals, transfers, maintenance, and asset history.

### 5.1 Approval Queue (UC-11, UC-16, UC-25)

```text
+------------------------------------------------------------------+
| Approvals                                        Administrator    |
| Filter: [Pending v]      Type: [All v]                            |
+------------------------------------------------------------------+
| ID      Type        Asset              From -> To       Waiting   |
| A-101   Transfer    Lab bench stool    CS -> Business   6 h       |
| A-099   Disposal    Old projector      Engineering      52 h      |
| A-097   Recycling   Old monitors       IT               20 h      |
|                                        [Open selected]            |
+------------------------------------------------------------------+
| Selected: A-101    Request: R-0042                                |
| Owner department release approval: APPROVED                      |
| Asset condition: Good      Active conflict: None                 |
| Rejection reason (minimum 10 characters): [_________________]    |
|                                  [Reject]  [Approve]             |
+------------------------------------------------------------------+
```

The Administrator can view pending requests, review approval details, and submit a final decision.

### 5.2 Receipt Confirmation (UC-12)

```text
+------------------------------------------------------------------+
| Transfer T-0031                        Status: In Transit         |
| Asset: Lab bench stool x20                                       |
| From: Computer Science          To: Business School             |
| Handover: 2026-11-04           Location: Library                 |
+------------------------------------------------------------------+
| Receiving Requester: [signed-in user]                            |
| Condition: ( ) As expected   ( ) Damaged or incorrect            |
| Discrepancy note: [__________________________________________]   |
| Optional photo: [Choose file]                                    |
|                     [Report problem]  [Confirm receipt]          |
+------------------------------------------------------------------+
```

The receiving Requester confirms receipt or reports a discrepancy. A damaged or incorrect asset does not automatically complete the transfer.

### 5.3 Defect Report (UC-13)

```text
+------------------------------------------------------------------+
| Report a defect                                                  |
| Asset ID *        [A-2045]  Projector                            |
| Description *     [__________________________________________]   |
| Reported condition: ( ) Good ( ) Fair ( ) Needs Repair           |
| Photo (optional): [Choose file]                                  |
| Date: Automatically recorded                                     |
|                                        [Cancel]  [Submit report]  |
+------------------------------------------------------------------+
```

The user enters the asset information and describes the problem. The system creates a maintenance ticket when the information is valid.

### 5.4 Inspection and Repair (UC-24, UC-14)

```text
+------------------------------------------------------------------+
| Maintenance ticket M-0210        Status: Repair Approved         |
| Asset: A-2045 Projector                                         |
| Inspection: [2026-11-05 10:00]  Assigned staff: [MS-02]          |
|                                             [Schedule inspection]|
+------------------------------------------------------------------+
| Repair history                                                   |
| Date         Work performed                Cost (AED)             |
| 2026-11-06   Lamp unit replaced            180.00                 |
+------------------------------------------------------------------+
| New repair record                                                |
| Work done *: [_______________________________________________]   |
| Cost (AED) *: [0.00]                                             |
| Result: ( ) Completed ( ) Further work ( ) Not repairable        |
|                                                   [Save repair]  |
+------------------------------------------------------------------+
| Verification: Different authorised staff member or custodian    |
| Verified condition: ( ) Good ( ) Fair ( ) Needs Repair           |
|                                                   [Verify]       |
+------------------------------------------------------------------+
```

Maintenance Staff can schedule inspections, record repair work and costs, and verify the repair result.

### 5.5 End-of-Life Decision (UC-16, UC-25)

```text
+------------------------------------------------------------------+
| End-of-life request E-0014                                      |
| Asset: Old projector             Action: Dispose                 |
| Reason: Cannot be repaired                                     |
| Alternatives assessed: Reuse / Transfer / Repair / Donation      |
|                        / Recycling                              |
+------------------------------------------------------------------+
| Administrator decision: Pending                                 |
| Finance Officer decision: Required for disposal                 |
| Reason for rejection (minimum 10 characters): [______________]  |
|                                        [Reject]  [Approve]        |
| Note: Final asset status changes only after action completion.  |
+------------------------------------------------------------------+
```

The Administrator reviews the request and the alternatives assessment. Disposal additionally requires Finance Officer approval.

### 5.6 Asset History (UC-15)

```text
+------------------------------------------------------------------+
| Asset history: A-2045 Projector                                 |
| Date        Event         Actor           Related record         |
| 2026-09-02  Registered    Custodian       -                      |
| 2026-09-10  Published     Custodian       L-0044                 |
| 2026-09-20  Transferred   Administrator   T-0031                 |
| 2026-10-21  Defect        Requester       M-0210                 |
| 2026-10-24  Repaired      Maint. staff    R-0090                 |
+------------------------------------------------------------------+
| Entries are read-only. Corrections create linked new entries.   |
+------------------------------------------------------------------+
```

The asset history displays previous activities in chronological order, including the date, event, responsible user, and related record.

## 6. Traceability

The following table connects the diagrams and interface mockups to their related use cases and functional requirements.

| Diagram / Mockup | Use Case | Related Requirements |
|---|---|---|
| Sequence 3.1, UI 5.1 | UC-11 Approve or Reject Transfer | FR-APR-01, 02, 03, 05, 06, 07; FR-TRF-01 |
| Sequence 3.2, UI 5.2 | UC-12 Confirm Receipt | FR-TRF-03, 04, 05; FR-HST-01 |
| Sequence 3.3, UI 5.3 | UC-13 Report Defect | FR-MNT-01; FR-HST-01 |
| Sequence 3.4, UI 5.4 | UC-24 Schedule Inspection | FR-MNT-02; FR-NTF-01 |
| Sequence 3.5, UI 5.4 | UC-14 Record Repair | FR-MNT-03, 04, 05; FR-HST-01 |
| Sequence 3.6, UI 5.6 | UC-15 View Asset History | FR-HST-01, 02, 03; FR-USR-06 |
| Sequence 3.7, UI 5.1/5.5 | UC-16 Approve Disposal | FR-DSP-01–05; FR-APR-03, 04, 05, 07 |
| Sequence 3.8, UI 5.1/5.5 | UC-25 Approve Donation or Recycling | FR-DSP-01, 03, 04, 05; FR-APR-03, 05, 07 |
| Context Diagram Section 2 | System Boundary and External Actors | FR-APR, FR-TRF, FR-MNT, FR-DSP, FR-USR |
| Class Diagram Section 4 | Workflow and Application Services | FR-APR, FR-TRF, FR-MNT, FR-HST, FR-DSP |

## 7. Design Consistency and Notes

### 7.1 Transfer Approval

The Department Representative must approve releasing the asset before the Administrator gives final transfer approval. A rejected request cannot proceed to scheduling or handover.

### 7.2 Transfer Completion

Administrator approval changes the transfer status to Approved, but does not immediately change ownership, custody, or location.

These details are updated only after the receiving Requester confirms receipt.

### 7.3 Maintenance Verification

A repair marked Completed must still be verified by an authorised staff member or Asset Custodian before the asset can return to service.

### 7.4 Disposal Approval

Disposal requires both Administrator and Finance Officer approval under the Phase 3 requirements. Donation and recycling require Administrator approval.

An approved end-of-life request does not immediately mark an asset as Donated, Recycled, or Disposed. The status changes only after the authorised action is confirmed complete.

### 7.5 Notifications and Audit Records

The system records important approval decisions, transfer updates, maintenance activities, and end-of-life actions.

Relevant users receive notifications when a workflow changes. Audit records contain the responsible actor, action, timestamp, and outcome.

### 7.6 Shared Design Documents

The context diagram provides a high-level representation of external system interactions.

The sequence diagrams describe the order of interactions between components, while the class diagram represents the main entities and services.

The shared architecture and entity-relationship diagram are maintained separately in `00_architecture_and_shared_design.md`.

This separation keeps the individual design document focused on approvals, transfers, maintenance, and end-of-life management.

# Phase 4 & 5 – Part 3: Users, Access, Reports, Notifications and Audit

**Owner:** Mohammed Alketbi
**Use cases:** UC-17 Create user, UC-18 Assign role, UC-19 Deactivate user, UC-20 Log in, UC-21 Generate report, UC-22 View audit log, UC-23 Receive notification
**Requirement groups:** FR-USR, FR-RPT, FR-NTF, FR-AUD (and the security rules BR-07, BR-14, BR-16, NFR-08 to 11)
**Data stores:** D1 Users, D12 Reports, D13 Notifications, D14 Audit Log
**Tables:** DEPARTMENT, USER, ROLE_PERMISSION, REPORT, NOTIFICATION, AUDIT_LOG

Shared diagrams (architecture, the one Level 0 DFD, ER diagram) are in `00_architecture_and_shared_design.md`.

---

# 1. Sequence Diagrams

## 1.1 UC-20 Log In

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant UI as Web Page
    participant AuthController
    participant AuthService
    participant DB as Database
    participant Audit as History and Audit

    U->>UI: Open the login page
    UI-->>U: Show login form
    U->>UI: Enter email and password, click "Log in"
    UI->>AuthController: POST /login
    activate AuthController
    AuthController->>AuthService: login(email, password)
    activate AuthService
    AuthService->>DB: find user by email
    DB-->>AuthService: user record or nothing
    alt email not found or password is wrong
        AuthService->>Audit: record failed login
        AuthService-->>AuthController: failed
        AuthController-->>UI: general error
        UI-->>U: Show "Email or password is not correct"
    else account is inactive
        AuthService->>Audit: record denied login
        AuthService-->>AuthController: failed
        AuthController-->>UI: general error
        UI-->>U: Show "Email or password is not correct"
    else login is correct
        AuthService->>AuthService: create session with role and department
        AuthService->>Audit: record successful login
        AuthService-->>AuthController: session
        deactivate AuthService
        AuthController-->>UI: session cookie and role
        deactivate AuthController
        UI-->>U: Show home page for the role
    end
```

Both wrong-password and inactive-account give the same message, so nobody can find out which emails exist (FR-USR error rules).

## 1.2 Self-Registration (FR-USR-02)

```mermaid
sequenceDiagram
    autonumber
    actor V as New user
    participant UI as Web Page
    participant AuthController
    participant UserService
    participant DB as Database
    participant Noti as Notification Module
    actor SA as System Administrator

    V->>UI: Click "Register", enter name, email, department, password
    UI->>AuthController: POST /register
    AuthController->>UserService: selfRegister(data)
    UserService->>UserService: check password length 12 to 128 characters
    UserService->>DB: check that email is unique
    alt email exists or password is invalid
        UserService-->>AuthController: error
        AuthController-->>UI: error
        UI-->>V: Show the problem
    else data is valid
        UserService->>DB: save user with role "Requester" and status "Inactive"
        UserService->>Noti: notify administrators
        Noti->>SA: "New account waiting for activation"
        UserService-->>AuthController: saved
        AuthController-->>UI: saved
        UI-->>V: Show "Wait for activation"
    end
```

## 1.3 UC-17 Create User

```mermaid
sequenceDiagram
    autonumber
    actor SA as System Administrator
    participant UI as Web Page
    participant UserController
    participant Security
    participant UserService
    participant DB as Database
    participant Noti as Notification Module
    participant Audit as History and Audit

    SA->>UI: Open "Users", click "Add user"
    UI-->>SA: Show form
    SA->>UI: Enter name, email, department, role
    UI->>UserController: POST /users
    activate UserController
    UserController->>Security: checkPermission(SA, "manage users")
    Security-->>UserController: allowed
    UserController->>UserService: createUser(data)
    activate UserService
    UserService->>DB: check that email is unique
    DB-->>UserService: result
    alt email already exists or format is wrong
        UserService-->>UserController: error
        UserController-->>UI: error
        UI-->>SA: Highlight the email field
    else data is valid
        UserService->>DB: save user with a first password setup link
        UserService->>Audit: record account creation
        UserService->>Noti: send activation email
        opt email service is down
            Noti-->>UserService: failed, queued for retry
        end
        UserService-->>UserController: user ID
        deactivate UserService
        UserController-->>UI: success
        deactivate UserController
        UI-->>SA: Show "Account created"
    end
```

## 1.4 UC-18 Assign Role

```mermaid
sequenceDiagram
    autonumber
    actor SA as System Administrator
    participant UI as Web Page
    participant UserController
    participant UserService
    participant DB as Database
    participant Audit as History and Audit

    SA->>UI: Open a user, click "Change role"
    UI->>UserController: GET /roles
    UserController-->>UI: role list
    UI-->>SA: Show roles
    SA->>UI: Select role, click "Save"
    UI->>UserController: PUT /users/{id}/role
    activate UserController
    UserController->>UserService: assignRole(userId, role)
    activate UserService
    UserService->>DB: read user
    DB-->>UserService: user with status
    alt user is inactive (was deactivated meanwhile)
        UserService-->>UserController: cancelled
        UserController-->>UI: message
        UI-->>SA: Show "User is inactive"
    else user is active
        UserService->>DB: save new role
        UserService->>Audit: record old and new role
        UserService-->>UserController: done
        deactivate UserService
        UserController-->>UI: success
        deactivate UserController
        UI-->>SA: Show "Role updated"
    end
```

## 1.5 UC-19 Deactivate User

```mermaid
sequenceDiagram
    autonumber
    actor SA as System Administrator
    participant UI as Web Page
    participant UserController
    participant UserService
    participant DB as Database
    participant Audit as History and Audit

    SA->>UI: Open a user, click "Deactivate"
    UI->>UserController: PUT /users/{id}/deactivate
    activate UserController
    UserController->>UserService: deactivate(userId)
    activate UserService
    UserService->>DB: count active administrators, read open requests and approvals
    DB-->>UserService: counts and list
    alt user is the last active administrator
        UserService-->>UserController: blocked
        UserController-->>UI: message
        UI-->>SA: Show "Keep at least one active administrator"
    else user has open requests or approvals
        UserService-->>UserController: list of open items
        UserController-->>UI: list
        UI-->>SA: Show list, ask to reassign first
    else user can be deactivated
        UserService->>DB: set status "Inactive", end all sessions
        UserService->>Audit: record deactivation
        UserService-->>UserController: done
        deactivate UserService
        UserController-->>UI: success
        deactivate UserController
        UI-->>SA: Show "User deactivated"
    end
```

## 1.6 UC-21 Generate Report

```mermaid
sequenceDiagram
    autonumber
    actor U as AD, FO, PO, SO (DR, AC, MS own department)
    participant UI as Web Page
    participant ReportController
    participant Security
    participant ReportService
    participant DB as Database
    participant Audit as History and Audit

    U->>UI: Open "Reports", choose type, set filters
    UI->>ReportController: POST /reports
    activate ReportController
    ReportController->>Security: checkPermission(user, report type)
    alt user may not see this report (for example financial data)
        Security-->>ReportController: denied
        ReportController->>Audit: record denied attempt
        ReportController-->>UI: access denied
        UI-->>U: Show "No access"
    else user may see the report
        Security-->>ReportController: allowed with department scope
        ReportController->>ReportService: generate(type, filters, scope)
        activate ReportService
        ReportService->>ReportService: check date range
        alt date range is invalid
            ReportService-->>ReportController: error
            ReportController-->>UI: error
            UI-->>U: Show "Invalid date range"
        else date range is valid
            ReportService->>DB: read data for the report
            alt data source times out
                DB-->>ReportService: timeout
                ReportService-->>UI: offer to run the report in the background
            else data is read
                DB-->>ReportService: rows
                alt no rows
                    ReportService-->>UI: empty report
                    UI-->>U: Show "No results found."
                else rows found
                    ReportService->>DB: save report record
                    ReportService-->>ReportController: report
                    deactivate ReportService
                    ReportController-->>UI: report
                    deactivate ReportController
                    UI-->>U: Show report
                    opt user clicks "Export CSV"
                        U->>UI: Export
                        UI->>ReportController: GET /reports/{id}/csv
                        ReportController->>Audit: record export
                        ReportController-->>UI: CSV file with name and time
                    end
                end
            end
        end
    end
```

## 1.7 UC-22 View Audit Log

```mermaid
sequenceDiagram
    autonumber
    actor U as SA or AD
    participant UI as Web Page
    participant AuditController
    participant Security
    participant AuditService
    participant DB as Database

    U->>UI: Open "Audit log", set filters (user, action, record, dates)
    UI->>AuditController: GET /audit?filters=...
    activate AuditController
    AuditController->>Security: checkPermission(user, "view audit")
    alt user is not SA or AD
        Security-->>AuditController: denied
        AuditController-->>UI: access denied
        UI-->>U: Show "No access"
    else user is SA or AD
        Security-->>AuditController: allowed
        AuditController->>AuditService: search(filters)
        activate AuditService
        AuditService->>DB: read entries (read only)
        DB-->>AuditService: entries
        alt result is too large
            AuditService-->>AuditController: ask for a narrower filter
            AuditController-->>UI: message
            UI-->>U: Show "Narrow your filter"
        else result fits
            AuditService-->>AuditController: entries
            deactivate AuditService
            AuditController-->>UI: entries
            deactivate AuditController
            UI-->>U: Show entries
        end
    end
```

## 1.8 UC-23 Receive Notification

```mermaid
sequenceDiagram
    autonumber
    participant Svc as Any Service (for example ApprovalService)
    participant NotificationService
    participant DB as Database
    participant Mail as Email Service
    actor U as User
    participant UI as Web Page

    Svc->>NotificationService: notify(eventType, involvedUsers)
    activate NotificationService
    NotificationService->>DB: save one in-app notification per user (status "Unread")
    opt user turned on email notifications
        NotificationService->>Mail: send email
        alt email service is down
            Mail-->>NotificationService: failed
            NotificationService->>DB: keep message, queue email for retry
        else email sent
            Mail-->>NotificationService: delivery status
        end
    end
    deactivate NotificationService
    U->>UI: Open the page, see the bell with a number
    UI->>NotificationService: GET /notifications (own only)
    NotificationService->>DB: read own notifications
    DB-->>NotificationService: list
    NotificationService-->>UI: list
    UI-->>U: Show messages
    U->>UI: Click a message
    UI->>NotificationService: PUT /notifications/{id}/read
    NotificationService->>DB: set status "Read"
```

---

# 2. Class Diagram

```mermaid
classDiagram
    class Department {
        +int deptId
        +String name
        +int repUserId
    }
    class User {
        +int userId
        +String name
        +String email
        +String passwordHash
        +Role role
        +int deptId
        +UserStatus status
        +boolean emailNotifications
        +isActive() boolean
        +checkPassword(pw) boolean
        +deactivate() void
    }
    class RolePermission {
        +Role role
        +String action
        +String scope
        +allows(action) boolean
    }
    class Report {
        +int reportId
        +String reportType
        +int generatedBy
        +Date periodStart
        +Date periodEnd
        +boolean aiGenerated
        +boolean reviewed
        +String content
        +exportCsv() File
    }
    class Notification {
        +int notificationId
        +int userId
        +String eventType
        +String message
        +NotificationStatus status
        +DateTime createdAt
        +markRead() void
    }
    class AuditLogEntry {
        +int auditId
        +int actorId
        +String action
        +String recordRef
        +String outcome
        +String oldValue
        +String newValue
        +DateTime eventTime
    }
    class Role {
        <<enumeration>>
        DR
        AC
        RQ
        AD
        PO
        FO
        MS
        SO
        SA
    }
    class UserStatus {
        <<enumeration>>
        Active
        Inactive
    }
    class NotificationStatus {
        <<enumeration>>
        Unread
        Read
    }

    class AuthService {
        +login(email, password) Session
        +logout(session) void
        +selfRegister(data) User
    }
    class SecurityService {
        +checkPermission(user, action, record) boolean
        +departmentScope(user) List
        +isOwnDepartment(user, record) boolean
    }
    class UserService {
        +createUser(data) User
        +assignRole(userId, role) void
        +deactivate(userId) void
        +validatePassword(pw) boolean
    }
    class ReportService {
        +generate(type, filters, scope) Report
        +exportCsv(reportId) File
        +validateDateRange(from, to) boolean
    }
    class NotificationService {
        +notify(eventType, users) void
        +list(userId) List
        +markRead(id) void
        +retryEmails() void
    }
    class AuditService {
        +record(actor, action, record, outcome, oldValue, newValue) void
        +search(filters) List
    }
    class AuthController {
        +postLogin() Response
        +postRegister() Response
    }
    class UserController {
        +postUser() Response
        +putRole() Response
        +putDeactivate() Response
    }
    class ReportController {
        +postReport() Response
        +getCsv() Response
    }
    class AuditController {
        +getAudit() Response
    }
    class NotificationController {
        +getNotifications() Response
        +putRead() Response
    }

    Department "1" --> "0..*" User : has
    User --> Role
    User --> UserStatus
    Notification --> NotificationStatus
    User "1" --> "0..*" Notification : receives
    User "1" --> "0..*" AuditLogEntry : performs
    User "1" --> "0..*" Report : generates
    RolePermission --> Role

    AuthController ..> AuthService
    UserController ..> UserService
    ReportController ..> ReportService
    AuditController ..> AuditService
    NotificationController ..> NotificationService
    AuthService ..> User
    AuthService ..> AuditService
    UserService ..> User
    UserService ..> AuditService
    ReportService ..> Report
    ReportService ..> SecurityService
    NotificationService ..> Notification
    SecurityService ..> RolePermission
    SecurityService ..> User
```

| Class | Role | Rule it enforces |
|---|---|---|
| AuthService | Login, logout, self-registration | FR-USR-02 to 04, NFR-08 |
| SecurityService | One place that checks role, department and active status before every action | FR-USR-06, BR-07, BR-16 |
| UserService | Create, change role, deactivate | FR-USR-01, FR-USR-05, last administrator rule |
| ReportService | Build, filter and export reports | FR-RPT-01 to 04 |
| NotificationService | Create, deliver and list notifications | FR-NTF-01 to 04 |
| AuditService | Writes entries (never edits or deletes) and searches them | FR-AUD-01 to 04, BR-14 |
| RolePermission | Stores the permission matrix of Phase 3 (Section 2.4) as data | BR-16 |

---

# 3. User Interface Mockups

## 3.1 Login and Register (UC-20, FR-USR-02)

```text
+----------------------------------------------+
|        Circular Campus Resource Exchange     |
|                                              |
|   Email      [______________________]        |
|   Password   [______________________]        |
|                                              |
|              [        Log in        ]        |
|   No account?  Register as a requester       |
|                                              |
|   Wrong details show one general message:    |
|   "Email or password is not correct"         |
+----------------------------------------------+
```

## 3.2 User Management (UC-17, UC-18, UC-19)

```text
+----------------------------------------------------------------------+
|  Users                                         (System Administrator)|
|  Search [__________]  Role [ All v ]  Status [ All v ] [ + Add user ]|
|                                                                      |
|  Name            Email            Dept       Role   Status           |
|  A. Hassan       a.h@univ.ae      CS         DR     Active           |
|  K. Saeed        k.s@univ.ae      Business   RQ     Inactive         |
|  M. Rashid       m.r@univ.ae      IT         SA     Active           |
|                                                                      |
|  [Change role]  [Deactivate]  [Activate]                             |
+----------------------------------------------------------------------+
|  Add user                                                            |
|  Name *  [__________]   Email * [______________]                     |
|  Department * [ v ]     Role * [ v ]                                 |
|                                    [ Cancel ]  [ Create account ]    |
+----------------------------------------------------------------------+
```

## 3.3 Reports (UC-21)

```text
+----------------------------------------------------------------------+
|  Reports                                                             |
|  Report  [ Completed transfers v ]                                   |
|  From [ yyyy-mm-dd ]  To [ yyyy-mm-dd ]  Department [ All v ]        |
|  Category [ All v ]   Status [ All v ]              [ Generate ]     |
|                                                                      |
|  Completed transfers, 2026-09-01 to 2026-09-30     Made 2026-10-01   |
|  Asset            From      To          Date         Value (AED)*    |
|  Lab bench stool  CS        Business    2026-09-20   3,000           |
|  Projector        IT        Eng.        2026-09-25   1,800           |
|                                                                      |
|  * Value column only for FO, AD and allowed roles                    |
|                                                  [ Export CSV ]      |
|  Empty result: "No results found."                                   |
+----------------------------------------------------------------------+
```

## 3.4 Audit Log (UC-22)

```text
+----------------------------------------------------------------------+
|  Audit log                                      (SA or Administrator)|
|  User [____]  Action [ All v ]  Record [____]  From [ ]  To [ ]      |
|                                                    [ Search ]        |
|                                                                      |
|  Time              User   Action          Record  Outcome            |
|  2026-10-21 09:12  AD01   Approve         A-101   Success            |
|  2026-10-21 09:20  RQ07   Approve         A-101   Denied             |
|  2026-10-21 10:02  SA01   Change role     U-33    Success            |
|  Details: old value DR -> new value AC                               |
|                                                                      |
|  Read only. Entries cannot be edited or deleted.                     |
+----------------------------------------------------------------------+
```

## 3.5 Notifications (UC-23)

```text
+----------------------------------------------------------------------+
|  Circular Campus                                [ Bell (3) ]  (RQ) v |
+----------------------------------------------------------------------+
|  Notifications                                                       |
|  * Your request R-0042 was approved                       5 min ago  |
|  * Transfer T-0031 is ready for pickup                    2 h ago    |
|    Reservation of Lab bench stool expires in 1 day        1 day ago  |
|                                                                      |
|  (* = unread)                       [ Mark all as read ]             |
|  Settings: [x] Also send me emails                                   |
+----------------------------------------------------------------------+
```

---

# 4. Traceability

| Diagram | Use case | Requirements |
|---|---|---|
| Sequence 1.3 | UC-17 Create user | FR-USR-01, FR-USR-02, FR-AUD-01 |
| Sequence 1.4 | UC-18 Assign role | FR-USR-05, BR-16 |
| Sequence 1.5 | UC-19 Deactivate user | FR-USR-05 |
| Sequence 1.1, 1.2 | UC-20 Log in | FR-USR-02 to 04, FR-USR-06 |
| Sequence 1.6 | UC-21 Generate report | FR-RPT-01 to 04 |
| Sequence 1.7 | UC-22 View audit log | FR-AUD-01 to 04 |
| Sequence 1.8 | UC-23 Receive notification | FR-NTF-01 to 04 |

# Phase 4 & 5 - Part 4: AI Layer and Sustainability

**Owner:** Abdulla

**Use cases:** UC-26 Classify asset, UC-27 Review AI match, UC-28 Review sustainability recommendation, UC-29 Ask the assistant, UC-30 Generate AI report, UC-31 View sustainability dashboard, UC-32 Override an AI output, UC-33 Detect duplicate listings, UC-34 Predict maintenance need, UC-35 Submit AI feedback

**Requirement groups:** FR-AI-01 to FR-AI-70, FR-AI-X-01 to FR-AI-X-17, FR-SUS-01 to FR-SUS-31

**Data stores:** D10 AI Output Log, D11 Sustainability Records (reads D2, D4, D5, D8)

**Tables:** AI_OUTPUT, AI_OVERRIDE, AI_FEEDBACK, REUSE_EVENT, EMISSION_FACTOR

Shared diagrams (architecture, AI integration design, the one Level 0 DFD, ER diagram) are in `00_architecture_and_shared_design.md`. Read Section 2.4 there first. Every AI use case below uses the same path: service, AI Facade, privacy filter, AI Adapter, AI Service, answer checker, AI Output Log.


# 1. Sequence Diagrams

## 1.1 UC-26 Classify Asset

```mermaid
sequenceDiagram
    autonumber
    actor AC as Asset Custodian
    participant UI as Web Page
    participant AIController
    participant ClassificationService
    participant AIFacade
    participant Privacy as PrivacyFilter
    participant Adapter as AIAdapter
    participant AIService as AI Service
    participant Log as AIOutputLogger
    participant DB as Database

    AC->>UI: Click "Suggest category" on the form
    UI->>AIController: POST /ai/classify (title, description, specs, image)
    activate AIController
    AIController->>ClassificationService: classify(assetData)
    activate ClassificationService
    ClassificationService->>AIFacade: request("classification", data)
    activate AIFacade
    AIFacade->>Privacy: removePersonalData(data)
    Privacy-->>AIFacade: clean data
    AIFacade->>Adapter: send(clean data, promptVersion)
    Adapter->>AIService: classify

    alt answer within 15 seconds
        AIService-->>Adapter: category, subcategory, tags, material, confidence
        Adapter-->>AIFacade: result

        alt answer is not valid
            AIFacade-->>ClassificationService: ignore, ask user to choose by hand
        else confidence is below threshold
            AIFacade-->>ClassificationService: result with warning
        else answer is good
            AIFacade-->>ClassificationService: result
        end

    else no answer in 15 seconds
        Adapter-->>AIFacade: timeout
        AIFacade-->>ClassificationService: no suggestion, fallback used
    end

    deactivate AIFacade
    ClassificationService->>Log: save(modelId, modelVersion, promptVersion, confidence, result)
    Log->>DB: insert AI output
    ClassificationService-->>AIController: suggestion, confidence, warning or fallback notice
    deactivate ClassificationService
    AIController-->>UI: suggestion
    deactivate AIController
    UI-->>AC: Show category, tags, confidence
    AC->>UI: Accept or change

    Note over UI,DB: The suggestion is saved as the final classification only after the user accepts it (FR-AI-15). A change is saved as an override (UC-32).
```


## 1.2 UC-27 Review AI Match

```mermaid
sequenceDiagram
    autonumber
    actor U as RQ, AC, DR, AD or PO
    participant UI as Web Page
    participant AIController
    participant MatchingService
    participant AIFacade
    participant AIService as AI Service
    participant SearchService
    participant Log as AIOutputLogger
    participant OverrideService

    U->>UI: Open a request, click "Find matches"
    UI->>AIController: POST /ai/match (request id)
    activate AIController
    AIController->>MatchingService: findMatches(requestId)
    activate MatchingService
    MatchingService->>MatchingService: read request and active listings
    MatchingService->>AIFacade: request("matching", request, listings)
    activate AIFacade
    AIFacade->>AIService: embed and compare (no personal data)

    alt answer within 15 seconds
        AIService-->>AIFacade: ranked list, scores, reasons, confidence
        AIFacade-->>MatchingService: matches

        alt no matches
            MatchingService->>SearchService: normal search (UC-06)
            SearchService-->>MatchingService: results
        end

    else no answer in 15 seconds
        AIFacade-->>MatchingService: fallback
        MatchingService->>SearchService: keyword search (UC-06)
        SearchService-->>MatchingService: results
    end

    deactivate AIFacade
    MatchingService->>Log: save result and versions
    MatchingService-->>AIController: ranked matches (score 0 to 100, reasons)
    deactivate MatchingService
    AIController-->>UI: matches
    deactivate AIController
    UI-->>U: Show list with score and reasons

    alt confidence is low
        UI-->>U: Show warning "Please check this match"
    end

    alt user accepts a match
        U->>UI: Click "Reserve" (UC-07)
        Note over UI: The AI never reserves or approves by itself (FR-AI-35).
    else user rejects or chooses another asset
        U->>UI: Choose another asset
        UI->>OverrideService: saveOverride(output, finalValue)
    end
```


## 1.3 UC-28 Review Sustainability Recommendation

```mermaid
sequenceDiagram
    autonumber
    actor SO as Sustainability Officer
    participant UI as Web Page
    participant AIController
    participant RecommendationService
    participant AIFacade
    participant AIService as AI Service
    participant DB as Database
    participant Log as AIOutputLogger
    participant OverrideService

    SO->>UI: Open an asset, click "Recommend action"
    UI->>AIController: POST /ai/recommend (asset id)
    activate AIController
    AIController->>RecommendationService: recommend(assetId)
    activate RecommendationService
    RecommendationService->>DB: read condition, repair history, status, value
    DB-->>RecommendationService: asset data

    alt not enough data
        RecommendationService-->>AIController: "not enough data"
        AIController-->>UI: message
        UI-->>SO: Show "Not enough data"

    else enough data
        RecommendationService->>AIFacade: request("recommendation", data)
        AIFacade->>AIService: analyse (no personal data)

        alt valid answer
            AIService-->>AIFacade: action, reason, confidence
            AIFacade-->>RecommendationService: recommendation
            RecommendationService->>RecommendationService: disposal only if all other actions are not possible (BR-10)
            RecommendationService->>Log: save output and versions
            RecommendationService-->>AIController: recommendation with explanation
            deactivate RecommendationService
            AIController-->>UI: recommendation
            deactivate AIController
            UI-->>SO: Show action, reason, confidence

        else answer invalid or timeout
            AIFacade-->>RecommendationService: hidden, error logged
            RecommendationService-->>UI: no recommendation
        end

        alt Sustainability Officer accepts
            SO->>UI: Click "Accept"
            UI->>OverrideService: markReviewed(output)
            Note over UI,OverrideService: Accepting does not change the asset. A transfer, donation, recycling or disposal still needs the approval flow of Part 2 (FR-AI-49).

        else Sustainability Officer rejects or changes
            SO->>UI: Click "Reject" and enter a reason
            UI->>OverrideService: saveOverride(output, finalValue, reason)
            OverrideService->>Log: save override with user and time
        end
    end
```


## 1.4 UC-29 Ask the Assistant

```mermaid
sequenceDiagram
    autonumber
    actor U as User (any role except SA)
    participant UI as Web Page
    participant AIController
    participant Security
    participant AssistantService
    participant Privacy as PrivacyFilter
    participant AIFacade
    participant AIService as AI Service
    participant DB as Database
    participant Log as AIOutputLogger

    U->>UI: Type a question in the assistant box
    UI->>AIController: POST /ai/ask (question)
    activate AIController
    AIController->>Security: checkPermission(user, "assistant")
    Security-->>AIController: allowed with visible data scope
    AIController->>AssistantService: ask(question, userScope)
    activate AssistantService
    AssistantService->>Privacy: removePersonalData(question)
    Privacy-->>AssistantService: clean question
    AssistantService->>DB: read data the user may see (assets, requests, history, policy text)
    DB-->>AssistantService: data
    AssistantService->>AIFacade: request("assistant", question, data)
    AIFacade->>AIService: answer from this data

    alt answer is related and based on system data
        AIService-->>AIFacade: answer, confidence
        AIFacade-->>AssistantService: answer

    else answer is unrelated or no data
        AIFacade-->>AssistantService: standard "cannot answer"

    else no answer in 15 seconds
        AIFacade-->>AssistantService: fallback to normal search
    end

    AssistantService->>Log: save question type, answer and versions
    AssistantService-->>AIController: answer
    deactivate AssistantService
    AIController-->>UI: answer
    deactivate AIController
    UI-->>U: Show answer

    Note over UI,AssistantService: If the user asks it to approve a transfer or dispose of an asset, the assistant refuses and points to the approval page (FR-AI-58, FR-AI-59).
```


## 1.5 UC-30 Generate AI Report

```mermaid
sequenceDiagram
    autonumber
    actor U as AD, SO, FO or PO
    participant UI as Web Page
    participant AIController
    participant AIReportService
    participant SustainabilityService
    participant AIFacade
    participant AIService as AI Service
    participant DB as Database
    participant Log as AIOutputLogger

    U->>UI: Choose report type and period, click "Generate"
    UI->>AIController: POST /ai/reports
    activate AIController
    AIController->>AIReportService: generate(type, period, user)
    activate AIReportService
    AIReportService->>SustainabilityService: getFigures(period)
    SustainabilityService-->>AIReportService: figures and assumptions
    AIReportService->>DB: read summaries (requests, listings, transfers, maintenance)
    DB-->>AIReportService: summary data

    alt data set is too large
        AIReportService->>AIReportService: shorten the data and tell the user
    end

    AIReportService->>AIFacade: request("report", summary data)
    AIFacade->>AIService: write the summary text
    AIService-->>AIFacade: draft text
    AIFacade-->>AIReportService: draft
    AIReportService->>AIReportService: check every figure in the text against the data

    alt a figure does not match
        AIReportService->>AIReportService: flag the text for the reviewer
    end

    AIReportService->>Log: save draft and versions
    AIReportService->>DB: save report as "aiGenerated, not reviewed"
    AIReportService-->>AIController: draft report with period
    deactivate AIReportService
    AIController-->>UI: draft
    deactivate AIController
    UI-->>U: Show draft with banner "AI generated, please review"
    U->>UI: Edit if needed, click "Mark as reviewed"
    UI->>AIReportService: markReviewed(reportId, userId)
    AIReportService->>DB: set reviewed

    Note over UI,DB: A report cannot be shared before it is reviewed (FR-AI-70).
```


## 1.6 UC-31 View Sustainability Dashboard

```mermaid
sequenceDiagram
    autonumber
    actor U as SO, AD, FO or PO
    participant UI as Web Page
    participant DashboardController
    participant Security
    participant SustainabilityService
    participant DB as Database

    U->>UI: Open "Sustainability"
    UI->>DashboardController: GET /sustainability?period=...&dept=...
    activate DashboardController
    DashboardController->>Security: checkPermission(user, "dashboard")
    Security-->>DashboardController: allowed with scope
    DashboardController->>SustainabilityService: getFigures(period, scope)
    activate SustainabilityService
    SustainabilityService->>DB: read reuse events, repair records, asset values, emission factors

    alt data source is down
        DB-->>SustainabilityService: error
        SustainabilityService-->>DashboardController: last saved figures with date

    else data is read
        DB-->>SustainabilityService: rows
        SustainabilityService->>SustainabilityService: waste diversion, avoided purchases, life extension, reuse rate, repair rate, savings

        alt emission factor is missing
            SustainabilityService->>SustainabilityService: set CO2e to "not enough data" (FR-SUS-30)
        else emission factor exists
            SustainabilityService->>SustainabilityService: CO2e = quantity x emission factor
        end

        SustainabilityService->>SustainabilityService: mark estimates and list assumptions
        SustainabilityService-->>DashboardController: figures with assumptions
    end

    deactivate SustainabilityService
    DashboardController-->>UI: figures
    deactivate DashboardController
    UI-->>U: Show charts, estimates marked, assumptions on request

    opt user exports the view
        U->>UI: Click "Export"
        UI-->>U: CSV file
    end
```


## 1.7 UC-32 Override an AI Output

```mermaid
sequenceDiagram
    autonumber
    actor U as AC, DR, AD or SO
    participant UI as Web Page
    participant AIController
    participant Security
    participant OverrideService
    participant DB as Database
    participant Audit as History and Audit

    U->>UI: Click "Change" on an AI suggestion
    UI-->>U: Show override form
    U->>UI: Choose final value and enter a reason
    UI->>AIController: POST /ai/outputs/{id}/override
    activate AIController
    AIController->>Security: checkPermission(user, "override AI")

    alt user has no permission
        Security-->>AIController: denied
        AIController->>Audit: record denied attempt
        AIController-->>UI: access denied
        UI-->>U: Show "No permission"

    else user has permission
        Security-->>AIController: allowed
        AIController->>OverrideService: saveOverride(outputId, finalValue, reason, userId)
        activate OverrideService
        OverrideService->>DB: save override with user, time, final value and reason

        alt reason cannot be saved
            DB-->>OverrideService: error
            OverrideService-->>AIController: override not applied
            AIController-->>UI: error
            UI-->>U: Show "Try again"

        else saved
            DB-->>OverrideService: saved
            OverrideService->>Audit: record override
            OverrideService-->>AIController: done
            deactivate OverrideService
            AIController-->>UI: success
            deactivate AIController
            UI-->>U: Show the final value
        end
    end
```


## 1.8 UC-33 Detect Duplicate Listings

```mermaid
sequenceDiagram
    autonumber
    actor AC as Asset Custodian
    participant UI as Web Page
    participant MarketplaceService
    participant DuplicateDetector
    participant AIFacade
    participant AIService as AI Service
    participant Log as AIOutputLogger

    AC->>UI: Click "Publish" on an asset
    UI->>MarketplaceService: publish(assetId)
    MarketplaceService->>DuplicateDetector: checkDuplicates(asset)
    DuplicateDetector->>AIFacade: request("duplicate check", asset, active listings)

    alt AI Service available
        AIFacade->>AIService: compare similarity
        AIService-->>AIFacade: similar listings with scores
        AIFacade-->>DuplicateDetector: result
        DuplicateDetector->>Log: save output and versions

        alt a similar listing is found
            DuplicateDetector-->>UI: warning with the existing listing
            UI-->>AC: Show both listings, ask to cancel or continue

        else score is borderline
            DuplicateDetector-->>UI: show both listings, ask the user to decide

        else no duplicate
            DuplicateDetector-->>MarketplaceService: no duplicate
            MarketplaceService-->>UI: listing created
        end

    else AI Service not available
        AIFacade-->>DuplicateDetector: skipped
        DuplicateDetector-->>UI: continue, tell the user the check was skipped
    end
```


## 1.9 UC-34 Predict Maintenance Need

```mermaid
sequenceDiagram
    autonumber
    actor MS as Maintenance Staff
    participant UI as Web Page
    participant AIController
    participant MaintenancePredictor
    participant DB as Database
    participant AIFacade
    participant AIService as AI Service
    participant Log as AIOutputLogger

    MS->>UI: Open "Maintenance forecast"
    UI->>AIController: GET /ai/maintenance-forecast
    AIController->>MaintenancePredictor: predict()
    MaintenancePredictor->>DB: read assets, age, condition, repair history
    DB-->>MaintenancePredictor: asset data
    MaintenancePredictor->>AIFacade: request("forecast", data)

    alt valid answer within 15 seconds
        AIFacade->>AIService: rank assets by risk
        AIService-->>AIFacade: ranked list with reasons
        AIFacade-->>MaintenancePredictor: result
        MaintenancePredictor->>Log: save output and versions
        MaintenancePredictor-->>UI: list
        UI-->>MS: Show assets with risk and reason
        MS->>UI: Open an asset and click "Schedule inspection" (UC-24)

    else not enough data for an asset
        MaintenancePredictor-->>UI: list with "not enough data" for that asset

    else no answer or invalid answer
        AIFacade-->>MaintenancePredictor: fallback
        MaintenancePredictor-->>UI: plain inspection schedule instead
    end
```


## 1.10 UC-35 Submit AI Feedback

```mermaid
sequenceDiagram
    autonumber
    actor U as Any user
    participant UI as Web Page
    participant AIController
    participant FeedbackService
    participant DB as Database

    U->>UI: Click "Was this helpful?" under an AI result
    UI-->>U: Show rating and comment box
    U->>UI: Choose rating, write comment, click "Send"
    UI->>AIController: POST /ai/outputs/{id}/feedback
    AIController->>FeedbackService: save(outputId, userId, rating, comment)
    FeedbackService->>DB: check for same feedback from the same user

    alt same feedback was already sent
        FeedbackService-->>UI: kept one entry
        UI-->>U: Show "Thank you"

    else feedback is new
        FeedbackService->>DB: save feedback

        alt save fails
            DB-->>FeedbackService: error
            FeedbackService-->>UI: error, keep the comment
            UI-->>U: Show "Try again"

        else saved
            DB-->>FeedbackService: saved
            FeedbackService-->>UI: success
            UI-->>U: Show "Thank you"
        end
    end
```


# 2. Class Diagram

## 2.1 AI Module (design pattern: Facade + Adapter)

```mermaid
classDiagram
    class AIFacade {
        +request(function, data) AIResult
        -applyFallback(function, data) AIResult
        -checkConfidence(result) boolean
    }

    class PrivacyFilter {
        +removePersonalData(data) Data
    }

    class AIAdapter {
        <<interface>>
        +send(data, promptVersion) AIResult
    }

    class LlmAdapter {
        -String modelId
        -String modelVersion
        -int timeoutSeconds
        +send(data, promptVersion) AIResult
    }

    class FallbackService {
        +keywordSearch(request) List
        +fixedRules(asset) Recommendation
        +plainSchedule() List
    }

    class AnswerChecker {
        +isValid(result) boolean
        +isLowConfidence(result) boolean
    }

    class AIOutputLogger {
        +save(function, data, result) AIOutput
    }

    class AIResult {
        +String content
        +Decimal confidence
        +String explanation
        +String modelId
        +String modelVersion
        +String promptVersion
    }

    class AIOutput {
        +int aiOutputId
        +String functionName
        +int assetId
        +int requestId
        +String modelId
        +String modelVersion
        +String promptVersion
        +Decimal confidence
        +String content
        +DateTime createdAt
    }

    class AIOverride {
        +int overrideId
        +int aiOutputId
        +int userId
        +String finalValue
        +String reason
        +DateTime createdAt
    }

    class AIFeedback {
        +int feedbackId
        +int aiOutputId
        +int userId
        +int rating
        +String comment
    }

    AIFacade --> PrivacyFilter
    AIFacade --> AIAdapter
    AIFacade --> FallbackService
    AIFacade --> AnswerChecker
    AIFacade --> AIOutputLogger
    AIAdapter <|.. LlmAdapter
    AIAdapter ..> AIResult
    AIOutputLogger ..> AIOutput
    AIOutput "1" --> "0..*" AIOverride : is changed by
    AIOutput "1" --> "0..*" AIFeedback : gets
```


## 2.2 AI Functions and Sustainability

```mermaid
classDiagram
    class ClassificationService {
        +classify(assetData) Suggestion
    }

    class MatchingService {
        +findMatches(requestId) List
        -score(request, listing) int
    }

    class RecommendationService {
        +recommend(assetId) Recommendation
        -disposalOnlyLast(options) Recommendation
    }

    class AssistantService {
        +ask(question, userScope) Answer
        -refuseAction(question) boolean
    }

    class AIReportService {
        +generate(type, period, user) Report
        +markReviewed(reportId, userId) void
        -checkFigures(text, data) boolean
    }

    class DuplicateDetector {
        +checkDuplicates(asset) List
    }

    class MaintenancePredictor {
        +predict() List
    }

    class OverrideService {
        +saveOverride(outputId, finalValue, reason, userId) AIOverride
        +markReviewed(outputId) void
    }

    class FeedbackService {
        +save(outputId, userId, rating, comment) AIFeedback
    }

    class SustainabilityService {
        +recordReuseEvent(assetId, requestId) ReuseEvent
        +getFigures(period, scope) Figures
        +wasteDiversion(period) Decimal
        +avoidedPurchases(period) int
        +lifeExtension(assetId) int
        +reuseRate(period) Decimal
        +repairRate(period) Decimal
        +financialSavings(period) Decimal
        +carbonReduction(period) Decimal
    }

    class ReuseEvent {
        +int reuseId
        +int assetId
        +int requestId
        +String eventType
        +Decimal avoidedValueAed
        +DateTime eventTime
    }

    class EmissionFactor {
        +int factorId
        +int categoryId
        +Decimal kgCo2ePerUnit
        +String source
    }

    class Figures {
        +Decimal value
        +boolean isEstimate
        +String assumptions
        +String numerator
        +String denominator
    }

    class AIController {
        +postClassify() Response
        +postMatch() Response
        +postRecommend() Response
        +postAsk() Response
        +postReport() Response
        +postOverride() Response
        +postFeedback() Response
        +getForecast() Response
    }

    class DashboardController {
        +getFigures() Response
    }

    AIController ..> ClassificationService
    AIController ..> MatchingService
    AIController ..> RecommendationService
    AIController ..> AssistantService
    AIController ..> AIReportService
    AIController ..> OverrideService
    AIController ..> FeedbackService
    AIController ..> MaintenancePredictor
    DashboardController ..> SustainabilityService
    AIReportService ..> SustainabilityService
    SustainabilityService ..> ReuseEvent
    SustainabilityService ..> EmissionFactor
    SustainabilityService ..> Figures
    ClassificationService ..> AIFacade
    MatchingService ..> AIFacade
    RecommendationService ..> AIFacade
    AssistantService ..> AIFacade
    AIReportService ..> AIFacade
    DuplicateDetector ..> AIFacade
    MaintenancePredictor ..> AIFacade
```

| Class | Role | Rule it enforces |
|---|---|---|
| AIFacade | Single door to the AI layer. Applies the privacy filter, adapter, checker, fallback and logger in the same order every time | BR-11, NFR-04, NFR-14 |
| PrivacyFilter | Removes names, emails and IDs of people | NFR-14 |
| AIAdapter / LlmAdapter | One interface. A new provider only needs a new adapter class | Design goal "easy to change" |
| FallbackService | Keyword search, fixed rules, plain schedule | FR-AI-X-08 to 10 |
| AIOutputLogger | Saves model, version, prompt version, confidence and result | FR-AI-X-05 to 07, FR-AI-X-11 to 13 |
| OverrideService | Saves override, final value and reason | FR-AI-X-03, FR-AI-X-04, BR-12 |
| SustainabilityService | The formulas and the "estimate" marks | FR-SUS-01 to 31 |


## 2.3 Sustainability Formulas

From Phase 3, Section 4.21:

**Reuse rate (%)** = (assets reused or transferred / assets considered for reuse) x 100

**Repair rate (%)** = (assets repaired / assets needing a disposition decision) x 100

**Estimated carbon reduction (kg CO2e)** = activity quantity x emission factor, with the emission factor and its source shown on screen


# 3. User Interface Mockups

## 3.1 AI Match Review (UC-27)

```text
+----------------------------------------------------------------------+
|  Matches for request R-0042: "laboratory seating x10"                |
|                                                                      |
|  Rank  Asset                 Score  Why                              |
|  1     Lab bench stool x20   91     Same purpose, stock is enough,   |
|                                     Good condition, same campus      |
|  2     Office chair x6       64     Not enough quantity, Fair        |
|                                                                      |
|  Confidence: High            AI suggestions need your decision.      |
|  [ Reserve #1 ]  [ Choose another asset ]  [ Was this helpful? ]     |
+----------------------------------------------------------------------+
|  Low confidence example:                                             |
|  ! The AI is not sure about this match. Please check it.             |
+----------------------------------------------------------------------+
```


## 3.2 Sustainability Recommendation (UC-28, UC-32)

```text
+----------------------------------------------------------------------+
|  Recommended action for A-2045 Projector                             |
|                                                                      |
|  Suggested: REPAIR              Confidence: 74 %                     |
|  Why: Repair cost is low and the asset is 3 years old.               |
|  Other options: Transfer, Refurbish, Recycle                         |
|  Disposal is the last option.                                        |
|                                                                      |
|  [ Accept ]   [ Change ]   [ Reject ]                                |
|                                                                      |
|  Change or reject:                                                   |
|  Final value [ Transfer v ]   Reason * [____________________]        |
|                                                [ Save override ]     |
|                                                                      |
|  Accepting does not change the asset. Approvals are still needed.    |
+----------------------------------------------------------------------+
```


## 3.3 Assistant (UC-29)

```text
+----------------------------------------------------------------------+
|  Assistant                                                           |
|                                                                      |
|  You:        Which projectors are available in Engineering?          |
|  Assistant:  2 projectors are published by Engineering:              |
|              A-2045 (Good) and A-2051 (Fair).  [Open A-2045]         |
|                                                                      |
|  You:        Approve the transfer of A-2045 for me.                  |
|  Assistant:  I cannot approve transfers. An administrator must       |
|              approve it on the Approvals page.                       |
|                                                                      |
|  [ Type your question here ______________________ ] [ Send ]          |
|  [ Was this helpful? ]                                               |
+----------------------------------------------------------------------+
```


## 3.4 AI Report Review (UC-30)

```text
+----------------------------------------------------------------------+
|  AI report: Monthly summary, September 2026                          |
|  ! AI generated. Please review before sharing.                       |
|                                                                      |
|  Period: 2026-09-01 to 2026-09-30                                   |
|  Summary: 14 assets were reused. 6 purchases were avoided with an    |
|  estimated value of AED 21,000 (estimate).                           |
|  Flagged: "AED 25,000" does not match the data (AED 21,000).         |
|                                                                      |
|  [ Edit text ]   [ Regenerate ]   [ Mark as reviewed ]               |
|  Status: Not reviewed             [ Export ] (disabled until reviewed)|
+----------------------------------------------------------------------+
```


## 3.5 Sustainability Dashboard (UC-31)

```text
+----------------------------------------------------------------------+
|  Sustainability                  Period [ Sep 2026 v ] Dept [ All v ]|
|                                                                      |
|  Assets reused    Avoided purchases   Savings (est.)   CO2e (est.)   |
|  14               6                   AED 21,000       380 kg        |
|                                                                      |
|  Reuse rate  70 %  (14 of 20)         Repair rate 50 % (5 of 10)     |
|  Waste diverted  38 items             Life extension 26 months (est.)|
|                                                                      |
|  [bar chart: reuse by month]          [pie: actions taken]           |
|                                                                      |
|  Values marked "est." are estimates. [Show assumptions] [Export]     |
|  Missing emission factor: "Not enough data"                          |
+----------------------------------------------------------------------+
```


## 3.6 Duplicate Warning (UC-33) and Maintenance Forecast (UC-34)

```text
+----------------------------------------------+   +--------------------------------------+
|  Possible duplicate listing                  |   |  Maintenance forecast                |
|                                              |   |                                      |
|  New: Lab bench stool x20 (CS)               |   |  Asset      Risk     Reason          |
|  Existing: Lab bench stool x20 (CS) L-0044   |   |  A-2045     High     5 repairs, 6 y  |
|  Similarity: 93 %                            |   |  A-2102     Medium   Age 4 y         |
|  [ Cancel ]   [ Publish anyway ]             |   |  A-2201     -        Not enough data |
+----------------------------------------------+   |  [Schedule inspection]               |
                                                   +--------------------------------------+
```


# 4. Traceability

| Diagram | Use case | Requirements |
|---|---|---|
| Sequence 1.1 | UC-26 Classify asset | FR-AI-01 to 15, FR-AI-X-01, FR-AI-X-02 |
| Sequence 1.2 | UC-27 Review AI match | FR-AI-16 to 35 |
| Sequence 1.3 | UC-28 Review sustainability recommendation | FR-AI-36 to 49, FR-SUS-27 to 31 |
| Sequence 1.4 | UC-29 Ask the assistant | FR-AI-50 to 59 |
| Sequence 1.5 | UC-30 Generate AI report | FR-AI-60 to 70 |
| Sequence 1.6 | UC-31 View sustainability dashboard | FR-SUS-01 to 31 |
| Sequence 1.7 | UC-32 Override an AI output | FR-AI-X-03, FR-AI-X-04, BR-12 |
| Sequence 1.8 | UC-33 Detect duplicate listings | No functional requirement in Phase 3 yet |
| Sequence 1.9 | UC-34 Predict maintenance need | No functional requirement in Phase 3 yet |
| Sequence 1.10 | UC-35 Submit AI feedback | No functional requirement in Phase 3 yet |
| AI module class diagram | All AI use cases | FR-AI-X-05 to 17, NFR-04, NFR-14 |

