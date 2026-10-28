# Phase 4 & 5 – Part 1: Assets, Marketplace and Requests

**Use Cases:** UC-01 to UC-10

**Requirement Groups:** FR-AST, FR-MKT, FR-REQ, FR-SRC, FR-RSV

**Data Stores:** D2 Assets, D4 Listings, D5 Requests and Reservations. D3 Asset History is also updated, but belongs to Part 2.

**Tables:** CATEGORY, ASSET, ASSET_MEDIA, LISTING, REQUEST, RESERVATION, WATCHLIST_ITEM

The shared architecture, context diagram, Level 0 DFD, and ER diagram are in `00_architecture_and_shared_design.md`.

---

# 1. Data Flow Diagrams – Level 1

Level 1 Data Flow Diagrams show how the main processes from the Level 0 DFD are divided into smaller processes.

This part covers Process 2.0 (Manage Assets) and Process 3.0 (Handle Marketplace and Requests).

## 1.1 Process 2.0 – Manage Assets

This process handles asset registration, editing, and deactivation.

Asset Custodians and Department Representatives provide asset details. The system validates and saves the information in D2 Assets.

Important changes are also recorded in D3 Asset History.

```mermaid
flowchart LR
    AC[Asset Custodian]
    DR[Department Representative]

    P21(2.1 Register Asset)
    P22(2.2 Update Asset)
    P23(2.3 Deactivate Asset)

    D2[(D2 Assets)]
    D3[(D3 Asset History)]
    AI[6.0 AI Functions]
    P4[4.0 Approvals and Transfers]

    AC -->|Asset details| P21
    DR -->|Asset details| P21
    D2 -->|Existing tag numbers| P21
    P21 -->|New asset| D2
    P21 -->|History event| D3
    P21 -->|Classification request| AI
    AI -->|Suggestion| P21
    P21 -->|Registration result| AC

    AC -->|Edit details| P22
    DR -->|Edit details| P22
    D2 -->|Current record| P22
    P4 -->|Ownership change| P22
    P22 -->|Updated asset| D2
    P22 -->|Change history| D3
    P22 -->|Update result| AC

    AC -->|Deactivate request| P23
    D2 -->|Asset status| P23
    P23 -->|Inactive record| D2
    P23 -->|History event| D3
    P23 -->|Deactivation result| AC
```

### Process Description

| Process | Description | Requirements |
|---|---|---|
| 2.1 Register Asset | Checks asset information, prevents duplicate tag numbers, gets an optional AI category suggestion, and saves the asset | FR-AST-01 to 08, FR-AI-01 to 15 |
| 2.2 Update Asset | Changes asset information and records the previous values in history | FR-AST-09, BR-13 |
| 2.3 Deactivate Asset | Marks an asset as inactive | FR-AST-10 |

The main data stores used by this process are:

- **D2 Assets:** Contains the current asset information.
- **D3 Asset History:** Stores important changes made to assets.

The AI module can suggest asset categories during registration, but the user confirms the final category.

---

## 1.2 Process 3.0 – Handle Marketplace and Requests

This process handles publishing assets, withdrawing listings, searching, submitting requests, making reservations, tracking requests, cancelling requests, and saving watchlists.

```mermaid
flowchart LR
    DR[Department Representative]
    AC[Asset Custodian]
    RQ[Requester]

    P31(3.1 Publish Listing)
    P32(3.2 Withdraw Listing)
    P33(3.3 Search Assets)
    P34(3.4 Submit Request)
    P35(3.5 Reserve Asset)
    P36(3.6 Track and Cancel)
    P37(3.7 Save Watchlist)

    D2[(D2 Assets)]
    D4[(D4 Listings)]
    D5[(D5 Requests)]
    AI[6.0 AI Functions]

    DR -->|Publish order| P31
    AC -->|Publish order| P31
    D2 -->|Asset details| P31
    P31 -->|New listing| D4
    P31 -->|Result| DR

    DR -->|Withdraw order| P32
    AC -->|Withdraw order| P32
    D4 -->|Current listing| P32
    P32 -->|Updated listing| D4

    RQ -->|Search filters| P33
    D4 -->|Active listings| P33
    P33 -->|Results| RQ

    RQ -->|Request details| P34
    P34 -->|New request| D5
    P34 -->|Match request| AI
    AI -->|Matches| P34
    P34 -->|Confirmation| RQ

    RQ -->|Reserve order| P35
    D2 -->|Available quantity| P35
    D5 -->|Existing reservations| P35
    P35 -->|Reservation| D5
    P35 -->|Result| RQ

    RQ -->|Track or cancel| P36
    D5 -->|Request status| P36
    P36 -->|Updated request| D5
    P36 -->|Status| RQ

    RQ -->|Watch asset or search| P37
    P37 -->|Watchlist item| D5
    P37 -->|Confirmation| RQ
```

### Process Description

| Process | Description | Requirements |
|---|---|---|
| 3.1 Publish Listing | Publishes a registered asset on the marketplace | FR-MKT-01, FR-MKT-02 |
| 3.2 Withdraw Listing | Removes an active listing from the marketplace | FR-MKT-03 |
| 3.3 Search Assets | Searches and filters published assets | FR-SRC-01 to 05 |
| 3.4 Submit Request | Creates a resource request and asks AI for matching assets | FR-REQ-01 to 06 |
| 3.5 Reserve Asset | Reserves an available asset after checking quantity and conflicts | FR-RSV-01 to 05 |
| 3.6 Track and Cancel | Displays request status and processes cancellation when allowed | FR-REQ-07 to 09 |
| 3.7 Save Watchlist | Saves an asset or search to the user's watchlist | FR-SRC-06, FR-SRC-07 |

The marketplace module also supports automatic listing expiry according to FR-MKT-04.

The main data stores are:

- **D2 Assets:** Contains the asset records.
- **D4 Listings:** Contains published marketplace listings.
- **D5 Requests and Reservations:** Contains requests, reservations, and watchlist information.

---

# 2. Sequence Diagrams

Sequence diagrams show how the user interface, services, and database interact when a user performs a function.

The following diagrams focus on the main actions and alternative outcomes.

## 2.1 UC-01 Register Asset

An Asset Custodian enters asset details. The system validates the information, checks for duplicates, and may use AI to suggest a category.

```mermaid
sequenceDiagram
    actor AC as Asset Custodian
    participant UI as Web Page
    participant S as AssetService
    participant DB as Database
    participant AI as AI Service

    AC->>UI: Enter asset details
    UI->>S: Submit asset
    S->>S: Check permission and validate

    alt Invalid information
        S-->>UI: Show errors
    else Valid information
        S->>DB: Check duplicate asset
        DB-->>S: Result
        alt Duplicate found
            S-->>UI: Show existing asset
        else No duplicate
            S->>AI: Suggest category
            AI-->>S: Suggestion or timeout
            S-->>UI: Show suggestion if available
            AC->>UI: Confirm category
            UI->>S: Save asset
            S->>DB: Store asset and history
            S-->>UI: Registration successful
        end
    end
```

### Explanation

The Asset Custodian fills in the registration form.

The AssetService validates the submitted details and checks whether the asset already exists.

If the information is valid, the AI service may suggest a category. The user reviews the suggestion before the asset is saved.

If the AI service does not respond within 15 seconds, the user can choose the category manually.

The system then saves the asset and records the registration event in history.

---

## 2.2 UC-05 Submit Request

A Requester fills in a resource request. The system checks the details, saves the request, and looks for matching assets.

```mermaid
sequenceDiagram
    actor RQ as Requester
    participant UI as Web Page
    participant S as RequestService
    participant DB as Database
    participant AI as AI Service

    RQ->>UI: Fill request form
    UI->>S: Submit request
    S->>S: Validate details

    alt Invalid request
        S-->>UI: Show errors
    else Valid request
        S->>DB: Save request
        DB-->>S: Request ID
        S->>AI: Find matching assets
        AI-->>S: Matches or fallback
        S-->>UI: Show request and matches
    end
```

### Explanation

The Requester enters the category, purpose, quantity, urgency, location, and required date.

The system validates the input before saving the request.

If the information is valid, a request ID is generated and the request status becomes **Submitted**.

The AI service can suggest suitable assets based on the request information.

If AI is unavailable, the system can use normal search to find possible matches.

---

## 2.3 UC-06 Search and Filter Assets

The Requester enters keywords and filters. The system checks the input and searches published assets.

```mermaid
sequenceDiagram
    actor RQ as Requester
    participant UI as Web Page
    participant S as SearchService
    participant DB as Database

    RQ->>UI: Enter keywords and filters
    UI->>S: Search request
    S->>S: Check access and filters

    alt Invalid filters
        S-->>UI: Show filter error
    else Valid filters
        S->>DB: Find published assets
        DB-->>S: Matching records
        S-->>UI: Search results
        UI-->>RQ: Display matching assets
    end
```

### Explanation

The Requester enters a keyword and may select filters such as category, department, condition, or location.

The SearchService checks the filters and retrieves matching published assets.

Only assets that the user is authorized to view are displayed.

If no assets match, the system displays **"No matching resources found"**.

---
