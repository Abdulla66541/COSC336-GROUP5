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
| Use Case ID | UC-05 |
| Name | Submit Request |
| Primary actor | Requester (RQ) |
| Secondary actor | AI Service (supports matching after submission) |
| Goal | Allow a requester to submit a complete resource request so that the system can process and match it with available assets. |
| Priority | Must |
| Preconditions | 1. The user is logged in as an RQ. 2. The user has permission to submit resource requests. 3. The requester has the information required to complete the request. |
| Trigger | The user clicks "Submit new request". |
| Main flow | 1. The system shows the resource request form. 2. The user enters the category, purpose, specifications, quantity, preferred condition, urgency, location, and required date. 3. The system checks that all required fields are completed. 4. The system validates the entered values, including quantity and date. 5. The user submits the request. 6. The system creates a unique request ID. 7. The system sets the request status to "Submitted". 8. The system stores the request information for later search, matching, reservation, and approval processes. 9. The system confirms that the request was successfully submitted. |
| Alternative flows | 2a. The user leaves a required field empty: the system highlights the missing field and asks the user to complete it. 3a. The quantity is invalid or not positive: the system rejects the value and asks the user to enter a valid quantity. 3b. The required date is invalid: the system asks the user to enter a valid date. 5a. The user cancels before submission: the system does not create the request and returns to the previous screen. |
| Exceptions | E1. The system is unavailable: the request is not submitted and the user is informed to try again. E2. The request cannot be saved: the system displays an error and does not mark the request as submitted. |
| Postconditions | Success: a valid request exists with a unique request ID and status "Submitted", and its information is available for later processing. Failure: no submitted request is created and any incomplete entry remains unsaved or as a draft according to the system behaviour. |
| Business rules | BR-01 (all required request fields must be completed before submission), BR-02 (request quantity must be a positive number), BR-03 (the required date must be valid), BR-04 (only an authenticated requester with the required permission may submit a request). |
| Related FRs | FR-REQ |
| Related NFRs | Security, usability, validation, and system availability requirements. |

## UC-02 – Edit asset

| Field | Description |
|---|---|
| **Name** | Asset Custodian (AC), Department Representative (DR) |
| **Preconditions** | The user is logged in, the asset exists, and the user has permission to edit the asset. |
| **Trigger** | The user selects the option to edit an existing asset. |
| **Main flow** | 1. The user opens an existing asset record. <br> 2. The user selects Edit. <br> 3. The system displays the current asset information. <br> 4. The user changes one or more asset fields. <br> 5. The user submits the changes. <br> 6. The system validates the updated information. <br> 7. The system saves the valid changes. <br> 8. The system confirms that the asset was updated successfully. |
| **Alternative flows** | **A1:** If required information is missing or invalid, the system identifies the problem and does not save the changes. <br><br> **A2:** If the user cancels before submitting, the system keeps the existing asset information unchanged. <br><br> **A3:** If the user does not have permission to edit the asset, the system denies the action. |
| **Postconditions** | The valid changes are stored in the asset record. If the edit is cancelled or rejected, the original asset information remains unchanged. |
| **Related FRs** | FR-AST |
