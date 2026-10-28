# Phase 4 & 5 – Part 1: Assets, Marketplace and Requests

**Owner:** Mohammed Al Ali

**Use Cases:** UC-01 to UC-10

**Requirement Groups:** FR-AST, FR-MKT, FR-REQ, FR-SRC, FR-RSV

**Data Stores:** D2 Assets, D4 Listings, D5 Requests and Reservations. Watchlist items are included in D5. D3 Asset History is written to but belongs to Part 2.

**Tables:** CATEGORY, ASSET, ASSET_MEDIA, LISTING, REQUEST, RESERVATION, WATCHLIST_ITEM

Shared architecture, context diagram, Level 0 DFD, ER diagram, and data rules are defined in `00_architecture_and_shared_design.md`.

---

# 1. Data Flow Diagrams – Level 1

Level 1 Data Flow Diagrams show how the major system processes are divided into smaller processes.

They identify the actors, data stores, inputs, and outputs involved in asset management, the marketplace, and resource requests.

## 1.1 Process 2.0 – Manage Assets

Process 2.0 handles asset registration, editing, and deactivation.

Asset Custodians and Department Representatives provide asset details. The system validates this information and stores asset records in D2 Assets.

Important changes are also recorded in D3 Asset History.

```mermaid
flowchart LR
    AC["Asset Custodian"]
    DR["Department Representative"]

    P21("2.1 Register Asset")
    P22("2.2 Update Asset")
    P23("2.3 Deactivate Asset")
    P6("6.0 Run AI Functions")
    P4("4.0 Process Approvals and Transfers")

    D2[["D2 Assets"]]
    D3[["D3 Asset History"]]

    AC -->|"Asset details"| P21
    DR -->|"Asset details"| P21
    D2 -->|"Existing tag numbers"| P21
    P21 -->|"Classification request"| P6
    P6 -->|"Category suggestion"| P21
    P21 -->|"New asset record"| D2
    P21 -->|"Registration event"| D3
    P21 -->|"Registration result"| AC

    AC -->|"Changed asset details"| P22
    DR -->|"Changed asset details"| P22
    D2 -->|"Current asset record"| P22
    P4 -->|"Ownership change"| P22
    P22 -->|"Updated asset record"| D2
    P22 -->|"Change event"| D3
    P22 -->|"Update result"| AC

    AC -->|"Deactivation order"| P23
    D2 -->|"Asset status"| P23
    P23 -->|"Inactive asset record"| D2
    P23 -->|"Deactivation event"| D3
    P23 -->|"Deactivation result"| AC
```

### Process Description

| Process | Description | Related Requirements |
|---|---|---|
| 2.1 Register Asset | Validates asset fields, checks the unique tag number, requests an optional AI category suggestion, and saves the asset | FR-AST-01 to 08, FR-AI-01 to 15 |
| 2.2 Update Asset | Allows authorized users to change asset information while recording the previous values | FR-AST-09, BR-13 |
| 2.3 Deactivate Asset | Marks an asset as inactive | FR-AST-10 |

The asset registration process uses AI for optional classification suggestions. However, users remain responsible for confirming the final category.

---

## 1.2 Process 3.0 – Handle Marketplace and Requests

Process 3.0 manages marketplace publication, withdrawal, asset searching, request submission, reservations, request tracking, cancellation, and watchlists.

```mermaid
flowchart LR
    DR["Department Representative"]
    AC["Asset Custodian"]
    RQ["Requester"]

    P31("3.1 Publish Listing")
    P32("3.2 Withdraw Listing")
    P33("3.3 Search Assets")
    P34("3.4 Submit Request")
    P35("3.5 Reserve Asset")
    P36("3.6 Track and Cancel Request")
    P37("3.7 Save to Watchlist")
    P6("6.0 Run AI Functions")

    D2[["D2 Assets"]]
    D4[["D4 Listings"]]
    D5[["D5 Requests and Reservations"]]

    DR -->|"Publish order"| P31
    AC -->|"Publish order"| P31
    D2 -->|"Asset status"| P31
    P31 -->|"New listing"| D4
    P31 -->|"Publish result"| DR

    DR -->|"Withdraw order"| P32
    AC -->|"Withdraw order"| P32
    D4 -->|"Active listing"| P32
    P32 -->|"Withdrawn listing"| D4
    P32 -->|"Withdraw result"| AC

    RQ -->|"Keywords and filters"| P33
    D4 -->|"Active listings"| P33
    D2 -->|"Published asset data"| P33
    P33 -->|"Search results"| RQ

    RQ -->|"Request details"| P34
    P34 -->|"Match request"| P6
    P6 -->|"Ranked matches"| P34
    P34 -->|"New request"| D5
    P34 -->|"Submit result"| RQ

    RQ -->|"Reserve order"| P35
    D2 -->|"Available quantity"| P35
    D5 -->|"Active reservations"| P35
    P35 -->|"New reservation"| D5
    P35 -->|"Reservation result"| RQ

    RQ -->|"Cancel order"| P36
    D5 -->|"Request status"| P36
    P36 -->|"Updated request"| D5
    P36 -->|"Request status view"| RQ

    RQ -->|"Watch order"| P37
    P37 -->|"Watchlist item"| D5
    P37 -->|"Watch result"| RQ
```

### Process Description

| Process | Description | Related Requirements |
|---|---|---|
| 3.1 Publish Listing | Checks whether an asset can be published and creates an active marketplace listing | FR-MKT-01, FR-MKT-02 |
| 3.2 Withdraw Listing | Removes a published listing from the active marketplace results | FR-MKT-03 |
| 3.3 Search Assets | Searches published assets using keywords, filters, and sorting | FR-SRC-01 to 05, NFR-02 |
| 3.4 Submit Request | Validates a resource request, stores it, and asks for matching suggestions | FR-REQ-01 to 06 |
| 3.5 Reserve Asset | Checks availability and creates a reservation if the quantity is available | FR-RSV-01 to 05, BR-04 |
| 3.6 Track and Cancel Request | Displays request status and allows cancellation when permitted | FR-REQ-07 to 09 |
| 3.7 Save to Watchlist | Saves an asset or search to the Requester's watchlist | FR-SRC-06, FR-SRC-07 |

D2 contains asset records, D4 contains marketplace listings, and D5 contains requests, reservations, and watchlist information.

---
