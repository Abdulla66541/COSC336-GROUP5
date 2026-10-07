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
