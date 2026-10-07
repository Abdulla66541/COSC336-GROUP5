## 7. Use Cases

### 7.1 Use Case Catalogue

| ID     | Use case            | Actor(s)         | Related FRs      |
|--------|---------------------|------------------|-----------------|
| UC-01  | Register asset      | AC, DR           | FR-AST          |
| UC-02  | Edit asset          | AC, DR           | FR-AST          |
| UC-03  | Publish surplus asset     | DR, AC          | FR-MKT          |
| UC-04  | Withdraw listing    | DR, AC           | FR-MKT          |
| UC-05  | Submit request      | RQ               | FR-REQ          |

| UC-06 | Search and filter assets | RQ, All Users | FR-SRC |
|-------|--------------------------|---------------|--------|
| UC-07 | Reserve asset | RQ | FR-RSV |
| UC-08 | Track request | RQ | FR-REQ |
| UC-09 | Cancel request | RQ | FR-REQ, FR-RSV |
| UC-10 | Save asset to watchlist | RQ | FR-SRC |




### UC-01 Register Asset

| Field | Description |
|---|---|
| **Use case ID** | UC-01 |
| **Name** | Register asset |
| **Primary actor** | Asset Custodian (AC); Department Representative (DR) |
| **Secondary actor** | AI Service (suggests a category) |
| **Goal** | Add a new asset to the system so it can be tracked from the start. |
| **Priority** | Must |
| **Preconditions** | 1. The user is logged in as AC or DR. 2. The user belongs to the department that owns the asset. 3. The asset is not already in the system. |
| **Trigger** | The user clicks "Register new asset". |
| **Main flow** | 1. The system shows the registration form. 2. The user enters the name, category, tag number, condition, quantity and location, and can add photos. 3. The system checks the required fields and that the tag number is new. 4. The system asks the AI Service for a category and shows it with a confidence score. 5. The user accepts or changes the category. 6. The system saves the asset with a unique ID and status "Registered". 7. The system records the history and audit log entries. 8. The system shows a confirmation and offers to publish the asset. |
| **Alternative flows** | 2a. The user is not finished: the system saves a draft. 3a. A required field is empty: the system highlights it and the user fixes it. 3b. The tag number already exists: the system shows the existing asset and the user cancels or corrects the number. 4a. The AI does not answer within 15 seconds: the user picks a category by hand. 5a. The user disagrees with the AI: the system saves the user's choice and keeps the AI suggestion in the log. |
| **Exceptions** | E1. A photo is too large or the wrong type: the system rejects it and keeps the other data. E2. The system is down: the form data is kept so the user can try again. |
| **Postconditions** | Success: the asset exists with a unique ID, status "Registered", and history and audit entries. It is not public yet. Failure: no asset is created, and any draft is kept. |
| **Business rules** | BR-11 (the AI only suggests, the user decides), BR-12 (the suggestion, confidence and user choice are recorded), BR-13 (history cannot be changed), BR-14 (every change is in the audit log). |
| **Related FRs** | FR-AST, FR-AI, FR-HST, FR-AUD |
| **Related NFRs** | NFR-06 (confirm important actions), NFR-16 (easy to use), NFR-17 (AI is explained) |
### UC-05 Submit Request

| Field | Description |
|---|---|
| **ID** | UC-05 |
| **Name** | Submit Request |
| **Actor** | RQ (Requester) |
| **Preconditions** | The requester is logged in and has permission to submit a resource request. |
| **Trigger** | The requester selects the option to create a new resource request. |
| **Main Flow** | 1. The requester opens the resource request form. 2. The system displays the required request fields. 3. The requester enters the category, purpose, specifications, quantity, preferred condition, urgency, location, and required date. 4. The system validates the entered information. 5. The requester submits the request. 6. The system creates a unique request record. 7. The system assigns the request the **Submitted** status. 8. The system confirms that the request has been submitted. |
| **Alternative Flows** | **A1. Missing required information:** The system identifies the missing fields and asks the requester to complete them. **A2. Invalid quantity:** The system rejects the request and asks the requester to enter a valid positive quantity. **A3. Invalid required date:** The system rejects the request and asks the requester to enter a valid date. **A4. User does not have permission:** The system denies submission and displays an appropriate access message. |
| **Postconditions** | A valid resource request is stored in the system with a unique request ID and **Submitted** status. |
| **Related FRs** | FR-REQ |
