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
