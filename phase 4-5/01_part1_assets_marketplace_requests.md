# Phase 4 & 5 – Part 1: Assets, Marketplace and Requests

**Use Cases:** UC-01 to UC-10

**Requirement Groups:** FR-AST, FR-MKT, FR-REQ, FR-SRC, FR-RSV

**Main Classes:** Asset, Category, AssetMedia, Listing, Request, Reservation, WatchlistItem

The shared architecture, context diagram, Level 0 DFD, and ER diagram are documented in `00_architecture_and_shared_design.md`.

The Data Flow Diagrams for this part are handled separately by another team member.

---

# 1. Sequence Diagrams

Sequence diagrams show how users interact with the system and how information moves between the website, services, and database.

The diagrams below cover UC-01 to UC-10.

## 1.1 UC-01 Register Asset

This use case allows an Asset Custodian or Department Representative to register a new asset.

The system checks the asset details, prevents duplicates, and may use AI to suggest a category.

```mermaid
sequenceDiagram
    actor U as AC or DR
    participant UI as Web Page
    participant S as AssetService
    participant DB as Database
    participant AI as AI Module

    U->>UI: Enter asset details
    UI->>S: Submit asset
    S->>S: Check permission and validate

    alt Invalid information
        S-->>UI: Show errors
    else Valid information
        S->>DB: Check duplicate tag
        DB-->>S: Result

        alt Duplicate found
            S-->>UI: Show duplicate warning
        else No duplicate
            S->>AI: Suggest category
            AI-->>S: Suggestion or fallback
            S-->>UI: Show suggestion
            U->>UI: Confirm category
            UI->>S: Save asset
            S->>DB: Store asset
            S->>DB: Record asset history
            S-->>UI: Registration successful
        end
    end
```

### Explanation

The user enters the asset information, such as name, category, quantity, condition, location, and department.

The system validates the information and checks whether the asset tag already exists.

AI may suggest a category, but the user confirms the final category.

If AI does not respond within 15 seconds, the user can choose the category manually.

Finally, the asset is saved and its registration is recorded in history.

**Related Requirements:** FR-AST, FR-AI, BR-11, BR-13.

---

## 1.2 UC-02 Edit Asset

This use case allows an authorized user to update an existing asset record.

```mermaid
sequenceDiagram
    actor U as AC or DR
    participant UI as Web Page
    participant S as AssetService
    participant DB as Database

    U->>UI: Open asset and click Edit
    UI->>S: Get asset details
    S->>DB: Read asset
    DB-->>S: Current information
    S-->>UI: Show edit form

    U->>UI: Change details and click Save
    UI->>S: Submit changes
    S->>S: Check permission and validate

    alt Invalid information
        S-->>UI: Show errors
    else Valid information
        S->>DB: Check latest version
        DB-->>S: Version result

        alt Asset was changed by someone else
            S-->>UI: Ask user to reload
        else No conflict
            S->>DB: Save new values
            S->>DB: Record old and new values
            S-->>UI: Update successful
        end
    end
```

### Explanation

The user opens an existing asset and clicks Edit.

The system displays the current asset information.

After the user makes changes, the system validates them.

If the asset was already modified by another user, the system asks the user to reload the latest version.

Otherwise, the changes are saved and the previous information remains in history.

**Related Requirements:** FR-AST, FR-HST, FR-AUD, BR-13, BR-14.

---

## 1.3 UC-03 Publish Surplus Asset

This use case allows an Asset Custodian or Department Representative to publish an unused asset in the marketplace.

```mermaid
sequenceDiagram
    actor U as AC or DR
    participant UI as Web Page
    participant S as MarketplaceService
    participant DB as Database
    participant AI as AI Module

    U->>UI: Click Publish as Surplus
    UI->>S: Request publication
    S->>DB: Check asset availability
    DB-->>S: Asset status

    alt Asset cannot be published
        S-->>UI: Show error
    else Asset is eligible
        S->>AI: Suggest title and keywords
        AI-->>S: Suggestion or fallback
        S-->>UI: Show publication form
        U->>UI: Review and confirm
        UI->>S: Publish asset
        S->>DB: Check existing listings
        DB-->>S: Duplicate check

        alt Possible duplicate
            S-->>UI: Warn user to review
        else No duplicate
            S->>DB: Save listing
            S-->>UI: Publication successful
        end
    end
```

### Explanation

The user selects an asset and chooses Publish as Surplus.

The system checks whether the asset can be published.

AI may suggest a better title or keywords, but the user can change them.

The system also checks for possible duplicate listings.

If a duplicate is found, the user is warned and can review it before deciding whether to continue.

When publication is confirmed, the listing becomes available to authorized users.

**Related Requirements:** FR-MKT, FR-AI, FR-NTF, BR-11, BR-13.

---

## 1.4 UC-04 Withdraw Listing

This use case allows an authorized user to remove a marketplace listing.

```mermaid
sequenceDiagram
    actor U as AC or DR
    participant UI as Web Page
    participant S as MarketplaceService
    participant DB as Database
    participant N as Notifications

    U->>UI: Click Withdraw Listing
    UI->>S: Request withdrawal
    S->>DB: Check listing and transfer
    DB-->>S: Current status

    alt Approved transfer exists
        S-->>UI: Withdrawal blocked
    else Withdrawal allowed
        S-->>UI: Ask for reason
        U->>UI: Enter reason and confirm
        UI->>S: Confirm withdrawal
        S->>DB: Mark listing Withdrawn
        S->>DB: Record withdrawal
        S->>N: Notify affected users
        S-->>UI: Withdrawal successful
    end
```

### Explanation

The user selects Withdraw Listing.

The system checks whether an approved transfer is already in progress.

If an approved transfer exists, withdrawal is blocked.

Otherwise, the user enters a reason and confirms.

The system marks the listing as Withdrawn and notifies affected requesters.

**Related Requirements:** FR-MKT, FR-NTF, BR-06, BR-14.

---

## 1.5 UC-05 Submit Request

This use case allows a Requester to submit a request for a resource.

```mermaid
sequenceDiagram
    actor RQ as Requester
    participant UI as Web Page
    participant S as RequestService
    participant DB as Database
    participant AI as AI Module

    RQ->>UI: Fill request form
    UI->>S: Submit request
    S->>S: Validate information

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

The system checks the information and creates the request.

The request receives a unique ID and its status becomes Submitted.

AI may suggest matching assets based on the request details.

If AI is unavailable, the system uses normal search as a fallback.

**Related Requirements:** FR-REQ, FR-AI, NFR-04.

---

## 1.6 UC-06 Search and Filter Assets

This use case allows users to search for available assets using keywords and filters.

```mermaid
sequenceDiagram
    actor RQ as Requester
    participant UI as Web Page
    participant S as SearchService
    participant DB as Database

    RQ->>UI: Enter keywords and filters
    UI->>S: Search assets
    S->>S: Check filters and permissions

    alt Invalid filters
        S-->>UI: Show filter error
    else Valid filters
        S->>DB: Find published assets
        DB-->>S: Matching records

        alt No results
            S-->>UI: No matching assets
        else Results found
            S-->>UI: Display matching assets
        end
    end
```

### Explanation

The user enters keywords and may filter assets by category, condition, department, location, quantity, or other criteria.

The system validates the filters and searches available listings.

Only assets that the user is authorized to view are displayed.

If no assets match, the system displays "No matching resources found".

**Related Requirements:** FR-SRC, FR-MKT, NFR-02.

---

## 1.7 UC-07 Reserve Asset

This use case allows a Requester to reserve an available asset.

```mermaid
sequenceDiagram
    actor RQ as Requester
    participant UI as Web Page
    participant S as ReservationService
    participant DB as Database

    RQ->>UI: Click Reserve
    UI->>S: Request reservation
    S->>DB: Check asset availability
    DB-->>S: Status and free quantity

    alt Asset unavailable or quantity insufficient
        S-->>UI: Reservation rejected
    else Reservation allowed
        S->>DB: Save 7-day reservation
        S->>DB: Update reserved quantity
        S->>DB: Record reservation event
        S-->>UI: Reservation confirmed
    end
```

### Explanation

The Requester selects an available asset and clicks Reserve.

The system checks the asset's availability and existing reservations.

If the requested quantity is not available, the reservation is rejected.

Otherwise, the system creates the reservation.

The reservation expires after seven days if the required approval is not completed.

**Related Requirements:** FR-RSV, BR-04.

---

## 1.8 UC-08 Track Request

This use case allows a Requester to check the progress of an existing request.

```mermaid
sequenceDiagram
    actor RQ as Requester
    participant UI as Web Page
    participant S as RequestService
    participant DB as Database

    RQ->>UI: Open My Requests
    UI->>S: Get my requests
    S->>DB: Find requests for user
    DB-->>S: Request list

    alt No requests
        S-->>UI: Show empty list
    else Requests found
        S-->>UI: Show request list
        RQ->>UI: Select a request
        UI->>S: Get request status
        S->>DB: Read request details
        DB-->>S: Status and history
        S-->>UI: Show progress and next step
    end
```

### Explanation

The Requester opens the My Requests page.

The system retrieves the user's requests and displays their current statuses.

When the user selects a request, the system shows the status, progress, and next required action.

If the user has no requests, an empty-list message is displayed.

**Related Requirements:** FR-REQ, FR-HST.

---

## 1.9 UC-09 Cancel Request

This use case allows a Requester to cancel a request that is no longer needed.

```mermaid
sequenceDiagram
    actor RQ as Requester
    participant UI as Web Page
    participant S as RequestService
    participant DB as Database
    participant N as Notifications

    RQ->>UI: Click Cancel Request
    UI->>S: Request cancellation
    S->>DB: Check request status
    DB-->>S: Current status

    alt Cancellation not allowed
        S-->>UI: Administrator required
    else Cancellation allowed
        S-->>UI: Ask for confirmation
        RQ->>UI: Confirm cancellation
        UI->>S: Cancel request
        S->>DB: Set status Cancelled
        S->>DB: Release any reservation
        S->>N: Notify asset owner
        S-->>UI: Cancellation successful
    end
```

### Explanation

The Requester selects Cancel Request.

The system checks whether the request is still eligible for cancellation.

If a transfer has already been approved, the Requester must contact an Administrator.

Otherwise, the request is cancelled and any active reservation is released.

The asset owner is also notified.

**Related Requirements:** FR-REQ, FR-RSV, BR-04, BR-14.

---

## 1.10 UC-10 Save Asset to Watchlist

This use case allows a Requester to save an asset or search to their watchlist.

```mermaid
sequenceDiagram
    actor RQ as Requester
    participant UI as Web Page
    participant S as SearchService
    participant DB as Database
    participant N as Notifications

    RQ->>UI: Click Watch
    UI-->>RQ: Show watch options
    RQ->>UI: Select asset or search
    UI->>S: Save watchlist item
    S->>DB: Check existing watch
    DB-->>S: Result

    alt Already watched
        S-->>UI: Offer to stop watching
    else New watch
        S->>DB: Save watchlist item
        S-->>UI: Watch saved
    end

    opt Matching asset appears later
        S->>N: Notify if enabled
    end
```

### Explanation

The Requester selects Watch on an asset or saved search.

The system checks whether it is already in the watchlist.

If it is not already saved, a new watchlist entry is created.

The system may notify the Requester when a matching asset becomes available, depending on notification settings.

**Related Requirements:** FR-SRC, FR-NTF.

---

## 1.11 Automatic Reservation Expiry

The system checks reservations automatically and releases those that have expired.

```mermaid
sequenceDiagram
    participant T as Daily Timer
    participant S as ReservationService
    participant DB as Database
    participant N as Notifications

    T->>S: Check old reservations
    S->>DB: Find unapproved reservations past 7 days
    DB-->>S: Expired reservations

    loop Each expired reservation
        S->>DB: Mark reservation Expired
        S->>DB: Release reserved quantity
        S->>DB: Record expiry event
        S->>N: Notify requester
    end
```

### Explanation

A daily timer starts the reservation expiry check.

The system identifies active reservations that have exceeded seven days without the required approval.

It marks them as Expired and releases the reserved quantity.

The Requester is notified about the expiry.

**Related Requirements:** FR-RSV-05, BR-04.

---

# 2. Class Diagram

The class diagram shows the main classes used in the asset, marketplace, and request modules.

Entity classes store information, while service classes handle system operations.

```mermaid
classDiagram
    class Category {
        +int categoryId
        +string name
    }

    class Asset {
        +int assetId
        +string tagNumber
        +string name
        +int quantity
        +string status
    }

    class AssetMedia {
        +int mediaId
        +string filePath
    }

    class Listing {
        +int listingId
        +string status
    }

    class Request {
        +int requestId
        +int quantity
        +string status
    }

    class Reservation {
        +int reservationId
        +int quantity
        +date expiresAt
        +string status
    }

    class WatchlistItem {
        +int watchId
        +string savedSearch
    }

    class AssetService {
        +registerAsset()
        +updateAsset()
        +deactivateAsset()
    }

    class MarketplaceService {
        +publish()
        +withdraw()
        +expireOldListings()
    }

    class RequestService {
        +submitRequest()
        +editRequest()
        +cancelRequest()
        +getStatus()
    }

    class SearchService {
        +search()
        +saveToWatchlist()
    }

    class ReservationService {
        +reserve()
        +release()
        +expireOldReservations()
    }

    Category "1" --> "0..*" Asset
    Asset "1" --> "0..*" AssetMedia
    Asset "1" --> "0..*" Listing
    Asset "1" --> "0..*" Reservation
    Request "1" --> "0..*" Reservation
    Asset "1" --> "0..*" WatchlistItem

    AssetService ..> Asset
    MarketplaceService ..> Listing
    RequestService ..> Request
    SearchService ..> Asset
    SearchService ..> WatchlistItem
    ReservationService ..> Reservation
```

## 2.1 Main Classes

| Class | Purpose |
|---|---|
| Category | Stores asset categories |
| Asset | Stores the main asset information |
| AssetMedia | Stores references to photographs and documents |
| Listing | Represents an asset published on the marketplace |
| Request | Represents a resource request |
| Reservation | Stores reservation details and expiry |
| WatchlistItem | Represents a watched asset or saved search |

## 2.2 Service Classes

| Class | Responsibility | Related Requirements |
|---|---|---|
| AssetService | Register, edit, and deactivate assets | FR-AST-01 to 10 |
| MarketplaceService | Publish, withdraw, and expire listings | FR-MKT-01 to 04 |
| RequestService | Submit, edit, cancel, and track requests | FR-REQ-01 to 09 |
| SearchService | Search, filter, sort, and manage watchlists | FR-SRC-01 to 07 |
| ReservationService | Create, release, and expire reservations | FR-RSV-01 to 05 |

The class diagram is simplified to show the main classes and relationships.

The complete database structure is described in the shared ER diagram.

---

# 3. User Interface Mockups

The wireframes below show the main screens in the asset, marketplace, and request modules.

They are simple layouts showing the information and buttons needed by users.

## 3.1 Register Asset – UC-01

```text
+----------------------------------------------------------------------+
| Circular Campus          [Marketplace] [My Assets] [Requests]        |
+----------------------------------------------------------------------+
| Register New Asset                                                   |
|                                                                      |
| Name *           [__________________________]                        |
| Tag number *     [______________]                                    |
| Description      [____________________________________]              |
| Category *       [Select category v]                                 |
|                                                                      |
| AI suggestion: Laboratory chairs                                     |
| Confidence: 82%                       [Accept] [Change]              |
|                                                                      |
| Quantity *       [1]                                                 |
| Estimated value  [0.00] AED                                          |
| Department *     [Computer Science v]                                |
| Location *       [__________________________]                        |
| Purchase date    [yyyy-mm-dd]                                        |
|                                                                      |
| Condition *      ( ) Good  ( ) Fair  ( ) Needs repair                |
| Availability *   ( ) In use  ( ) Surplus                             |
|                                                                      |
| Photos           [Choose files]                                      |
| Documents        [Choose files]                                      |
|                                                                      |
| * Required               [Save as Draft] [Register]                  |
+----------------------------------------------------------------------+
```

### Screen Description

The Register Asset screen allows Asset Custodians and Department Representatives to create asset records.

The form includes the asset's name, tag number, category, quantity, department, location, condition, purchase date, estimated value, and attachments.

The system validates the information before saving.

An optional AI category suggestion may be accepted or changed by the user.

---

## 3.2 Marketplace and Search – UC-03, UC-04, UC-06, UC-07, UC-10

```text
+----------------------------------------------------------------------+
| Marketplace                                                          |
+----------------------------------------------------------------------+
| Search: [laboratory seating________________] [Search]                |
|                                                                      |
| Filters                 Sort by: [Publication Date v]                |
|                                                                      |
| Category    [v]          -------------------------------------       |
| Condition   [v]          Lab Bench Stool - Quantity: 20             |
| Department  [v]          Computer Science - Good                    |
| Location    [v]          AED 150 each                                |
| Quantity    [_]-[_]      [View] [Reserve] [Watch]                    |
|                                                                      |
| Value AED   [_]-[_]      -------------------------------------       |
| Age         [_]-[_]      Office Chair - Quantity: 6                 |
| Status      [v]          Business - Fair                             |
|                          AED 90 each                                 |
| [Apply Filters]          [View] [Reserve] [Watch]                    |
| [Save Search]                                                        |
|                                                                      |
|                         Page 1 of 3 [Previous] [Next]               |
+----------------------------------------------------------------------+
| No results: "No matching resources found"                            |
+----------------------------------------------------------------------+
```

### Screen Description

The marketplace screen allows authorized users to search published assets.

Users can filter results by category, condition, department, location, quantity, value, age, and status.

Requesters can view asset details, reserve available assets, watch assets, and save searches.

Authorized asset owners can publish or withdraw listings through the asset and listing details pages.

---

## 3.3 Create Request – UC-05

```text
+----------------------------------------------------------------------+
| New Resource Request                                                 |
+----------------------------------------------------------------------+
|                                                                      |
| Category *          [Furniture v]                                    |
| Purpose *           [____________________________]                   |
| Specifications      [____________________________]                   |
| Quantity *          [10]                                             |
| Preferred condition [Good v]                                         |
|                                                                      |
| Urgency *           ( ) Low  ( ) Medium  ( ) High                    |
| Location *          [____________________]                           |
| Required date *     [yyyy-mm-dd]                                     |
|                                                                      |
| [Cancel]                                  [Submit Request]            |
+----------------------------------------------------------------------+
| Request R-0042 created                                               |
|                                                                      |
| Suggested assets:                                                    |
| 1. Lab Bench Stool - Match 91%                 [View]                |
+----------------------------------------------------------------------+
```

### Screen Description

The Create Request screen allows Requesters to submit information about the resources they need.

The system validates the form and creates a new request.

After submission, matching assets may be suggested by the AI module.

---

## 3.4 My Requests and Reservations – UC-08, UC-09

```text
+----------------------------------------------------------------------+
| My Requests                                                          |
+----------------------------------------------------------------------+
|                                                                      |
| ID      Asset / Need       Status                 Reserved Until     |
| -------------------------------------------------------------------- |
| R-0042  Lab Seating x10    Matched / Reserved     2026-11-05         |
| R-0039  Projector x1       Approved               -                  |
| R-0031  Monitors x20       Submitted              -                  |
|                                                                      |
| [View Details]     [Edit]     [Cancel Request]                        |
|                                                                      |
| Cancellation blocked after transfer approval:                        |
| "Ask an administrator to cancel this request."                       |
+----------------------------------------------------------------------+
```

### Screen Description

The My Requests screen allows Requesters to check the progress of their requests.

It displays request status, reservation expiry date, and available actions.

The user can edit or cancel a request only when permitted by the workflow.

---

# 4. Traceability

The traceability table connects the Phase 4 and 5 design elements to the Phase 3 use cases and functional requirements.

| Design Element | Use Case | Related Requirements |
|---|---|---|
| Sequence 1.1, AssetService | UC-01 Register Asset | FR-AST-01 to 08, FR-AI |
| Sequence 1.2, AssetService | UC-02 Edit Asset | FR-AST-09, FR-HST, FR-AUD |
| Sequence 1.3, MarketplaceService | UC-03 Publish Surplus Asset | FR-MKT-01, FR-MKT-02 |
| Sequence 1.4, MarketplaceService | UC-04 Withdraw Listing | FR-MKT-03, FR-NTF |
| Sequence 1.5, RequestService | UC-05 Submit Request | FR-REQ-01 to 06 |
| Sequence 1.6, SearchService | UC-06 Search and Filter Assets | FR-SRC-01 to 05 |
| Sequence 1.7, ReservationService | UC-07 Reserve Asset | FR-RSV-01 to 05, BR-04 |
| Sequence 1.8, RequestService | UC-08 Track Request | FR-REQ-09 |
| Sequence 1.9, RequestService | UC-09 Cancel Request | FR-REQ-08, FR-RSV |
| Sequence 1.10, SearchService | UC-10 Save Asset to Watchlist | FR-SRC-06, FR-SRC-07 |
| Sequence 1.11, ReservationService | Automatic Reservation Expiry | FR-RSV-05, BR-04 |
| AssetService | Asset Deactivation | FR-AST-10 |
| RequestService | Request Editing | FR-REQ-07 |
| MarketplaceService | Automatic Listing Expiry | FR-MKT-04 |

## 4.1 Design Consistency

The sequence diagrams show the interactions between users, services, databases, and supporting modules.

The class diagram identifies the main entities and services used in the system.

The UI mockups show how users access these functions.

The DFDs are handled separately by another team member and should be checked against these designs when the full group document is assembled.
