# 4. The functional requirements, including assets, marketplace, requests and search.

This section specifies the purpose of asset registration,
The resource publication, resource request, search and filtering, and reservation are all achieved.
and request management.

Each requirement is written so that it describes what the system shall do and is each requirement a description.
Can be confirmed at a later test.


The process of registering assets and conducting inventories.

**Priority:** Essential

### 4.1.1 Description

The Asset Registration and Inventory feature allows authorised Asset
Records for custodians and Department Representatives to create and maintain.
university assets. The information in each record includes what is required to identify,
locate, value and manage the asset during its life cycle.

### 4.1.2 Stimulus and Response

| Stimulus | System Response |
|---|---|
| AC or DR selects Register New Asset | The system displays the asset registration form |
| User submits valid asset information | The system creates the asset and assigns a unique ID |
| User submits invalid information | The system identifies the invalid fields and does not create the asset |
| AC or DR edits an asset | The system validates and saves the new values |
| Authorised user deactivates an asset | The system marks the asset as inactive |

### 4.1.3 Functional Requirements

An authorised user shall be able to record an asset with the following details: Name, Description, Category, Quantity, Owner, Department, Location, Purchase Date, Estimated Value, Condition, Availability, Photographs and Supporting Documents.

The system shall provide a unique asset ID for each asset that is successfully registered.

Before registration the system shall ask for asset name, category, quantity, owner, department, location, condition and availability.

FR-AST-04: The system shall refuse to accept an asset quantity that is not an integer of 1 or more.

The system shall deny an estimated asset value less than 0 AED.

A purchase date cannot be later than the current date (FR-AST-06).

The system shall only accept asset photographs in a format of JPG, JPEG or PNG and a maximum size of 5 MB per image.

Document(s) submitted as supporting documents shall be acceptable as PDF or DOCX format with a maximum size of 10 MB per document.

FR-AST-09: An authorised user is allowed to edit an existing asset record.

FR-AST-10: An authorised user should be able to deactivate an existing asset record.

### 4.1.4 Error Handling

- If a required field is empty, the system shall identify the missing field.
- If the numeric value or date entered is invalid, then the system shall refuse the value entered.
- If an attachment is not of a supported type or is too large, the system shall not accept the attachment.
If a duplicate asset record is found, the system shall display the existing asset record before creating a new record.
- If the user is not authorized to edit an asset, then the system shall refuse the action.


## 4.2 Resource Publication / Marketplace

**Priority:** Essential

### 4.2.1 Description

The Resource Publication and Marketplace feature enables authorised users to:
Publish excess, underused or unwanted assets for other authorized parties to use.
campus users can find and reuse them.

### 4.2.2 Stimulus and Response

| Stimulus | System Response |
|---|---|
| AC or DR selects Publish as Surplus | The system checks whether the asset can be published |
| User confirms publication | The system creates an active marketplace listing |
| User withdraws a listing | The system removes the listing from active marketplace results |
| Listing reaches its expiry date | The system marks the listing as expired |

### 4.2.3 Functional Requirements

The system shall enable an authorised AC or DR to report a registered asset as surplus, underutilised or unwanted.

The system shall be able to display marketplace listings that are active only to authorised users.

The system shall enable an authorised AC/DR of the owning department to remove an active marketplace listing.

If a marketplace listing has not been renewed, the system shall automatically expire the listing after 30 days of the listing's publication.

### 4.2.4 Error Handling

- The system shall not allow publication if the asset is not found.
The system shall not publish if the asset is currently subject to an open transfer, reservation or disposal process that prevents the publication of the asset.
The system shall provide warning if another listing is created for the same asset when an active listing exists for the asset.
- The system shall refuse the action if the user does not have publication permission.
– If an approved transfer is currently underway, withdrawal of the listing shall be denied.


## 4.3 Resource Request Submission

**Priority:** Essential

### 4.3.1 Description

With the Resource Request Submission feature, Requesters can write a
The resource they require and submit their request for processing.

### 4.3.2 Stimulus and Response

| Stimulus | System Response |
|---|---|
| RQ selects Request This Asset or Create Request | The system displays the request form |
| RQ submits valid information | The system creates the request |
| RQ submits invalid information | The system identifies the invalid information |
| RQ edits an eligible request | The system validates and stores the changes |
| RQ cancels an eligible request | The system closes the request and releases any related reservation |

### 4.3.3 Functional Requirements

The system shall enable an authorised Requester to establish a Request which shall include the following: category, purpose, specifications, quantity, preferred condition, urgency, location, required date.

A request shall not be allowed to be submitted until the system has been presented with a category, a purpose, a quantity, an urgency, a location and a required date.

A requested quantity not an integer of at least 1 shall be rejected by the system.

Fails to accept a required date that is before the current date.

The system shall allow only Low, Medium or High for the urgency value.

FR-REQ-06: The system shall return a unique request ID for every request that is successfully submitted.

The system shall provide a Requester with the ability to change a request prior to approval or finalization.

The system shall enable a Requester to cancel a request when cancellation is allowed in the request workflow.

The system should enable a Requester to see the status and progress of each request submitted.

### 4.3.4 Error Handling

No submission shall be made for failure to provide information.
Invalid quantities or dates will be rejected.
The system shall not allow edits to a request once it is in a state where editing by the requester is not allowed.
- The system shall not allow a Requester to edit another user's request.
In the event that a cancellation is not possible due to an already approved transfer, the system shall state that the cancellation requires an authorised administrator.


## 4.4 Search and Filtering

**Priority:** Essential

### 4.4.1 Description

The Search and Filtering feature allows authorised users to locate suitable
published assets using keywords, filters and sorting options. Requesters can
also save assets or searches to a watchlist.

### 4.4.2 Stimulus and Response

| Stimulus | System Response |
|---|---|
| User enters keywords | The system searches published assets |
| User selects filters | The system restricts results to assets matching the selected criteria |
| User chooses a sorting option | The system reorders the results |
| Search returns no matches | The system displays an empty-result message |
| RQ selects Watch | The system saves the asset or search to the Requester's watchlist |

### 4.4.3 Functional Requirements

**FR-SRC-01:** The system shall allow authorised users to search published assets using keywords.

**FR-SRC-02:** The system shall allow users to filter assets by category, condition, department, location, quantity, availability, asset age, estimated value and life-cycle status.

**FR-SRC-03:** The system shall allow more than one search filter to be applied at the same time.

**FR-SRC-04:** The system shall allow users to sort search results by supported criteria including asset name, estimated value, purchase date and publication date.

**FR-SRC-05:** The system shall display "No matching resources found" when a valid search returns zero matching assets.

**FR-SRC-06:** The system shall allow a Requester to save an asset to a personal watchlist.

**FR-SRC-07:** The system shall allow a Requester to save a search to a personal watchlist.

### 4.4.4 Error Handling

- Invalid numeric filter ranges shall be rejected.
- A minimum filter value greater than its maximum value shall be rejected.
- A search with no results shall not be treated as a system failure.
- The system shall not display asset information that the user is not authorised to view.
- If an asset or search is already being watched, the system shall not create a duplicate watch entry.


## 4.5 Reservation and Request Management

**Priority:** Essential

### 4.5.1 Description

The Reservation and Request Management feature allows a Requester to express
interest in an available asset and reserve it while the related request is
processed.

### 4.5.2 Stimulus and Response

| Stimulus | System Response |
|---|---|
| RQ expresses interest in an asset | The system records the interest |
| RQ selects Reserve | The system checks current availability |
| Reservation is valid | The system marks the asset as Reserved |
| Another active reservation exists | The system rejects the conflicting reservation |
| Reservation reaches seven days without approval | The system expires the reservation and makes the asset available again |

### 4.5.3 Functional Requirements

**FR-RSV-01:** The system shall allow an authorised Requester to express interest in an available asset.

**FR-RSV-02:** The system shall allow a Requester to reserve an available asset when the requested quantity is available.

**FR-RSV-03:** The system shall prevent the same available quantity of an asset from being reserved by more than one Requester at the same time.

**FR-RSV-04:** The system shall record the asset, Requester, requested quantity, reservation time and reservation status for each reservation.

**FR-RSV-05:** The system shall automatically expire a reservation after 7 days if the required approval has not been completed.

### 4.5.4 Error Handling

- A reservation shall be rejected if the asset is no longer available.
- A reservation shall be rejected if the required quantity exceeds the available quantity.
- A conflicting reservation shall not replace the existing valid reservation.
- If a reservation expires, the system shall make the reserved asset available again.
- A user without reservation permission shall not be permitted to reserve an asset.


# 6.1 Asset and Request State Models

The following state models define the allowed states, transitions and actors
for assets and resource requests.


## 6.1.1 Asset State Model

| Current State | Next State | Trigger | Actor |
|---|---|---|---|
| Draft | Registered | Valid asset registration is completed | AC, DR |
| Registered | Available/Published | Asset is published to the marketplace | AC, DR |
| Available/Published | Reserved | A valid reservation is created | RQ / System |
| Reserved | Available/Published | Reservation expires after 7 days or is released | System / RQ |
| Reserved | In Transfer | Required transfer approval is granted | AD |
| In Transfer | Registered | Transfer and receipt are completed and asset information is updated | AC, DR |
| Registered | In Maintenance | A defect or maintenance need is recorded | AC / MS |
| Available/Published | In Maintenance | A defect or maintenance need is recorded | AC / MS |
| In Maintenance | Registered | Repair or maintenance is completed | MS |
| Registered | Retired | Retirement is authorised | AD |
| Registered | Donated | Donation is authorised | AD |
| Registered | Recycled | Recycling is authorised | AD |
| Registered | Disposed | Disposal is authorised | AD / FO when required |


## 6.1.2 Request State Model

| Current State | Next State | Trigger | Actor |
|---|---|---|---|
| Draft | Submitted | RQ submits a valid request | RQ |
| Submitted | Matched/Reserved | A suitable asset is matched or reserved | RQ / System |
| Submitted | Cancelled | RQ cancels the request | RQ |
| Submitted | Expired | Request validity ends | System |
| Matched/Reserved | Approved | Authorised approval is granted | AD |
| Matched/Reserved | Rejected | Authorised approval is rejected | AD |
| Matched/Reserved | Cancelled | RQ cancels before transfer approval | RQ |
| Approved | Fulfilled | Asset is successfully provided and received | System / Authorised user |
| Approved | Cancelled | An authorised administrator cancels the approved request | AD |
