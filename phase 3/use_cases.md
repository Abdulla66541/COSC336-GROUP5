## 7. Use Cases

### 7.1 Use Case Catalogue

| ID | Use case | Primary actor | Related FRs |
|----|----------|---------------|-------------|
| UC-01 | Register asset | AC, DR | FR-AST |
| UC-02 | Edit asset | AC, DR | FR-AST |
| UC-03 | Publish surplus asset | DR, AC | FR-MKT |
| UC-04 | Withdraw listing | DR, AC | FR-MKT |
| UC-05 | Submit request | RQ | FR-REQ |
| UC-06 | Search and filter assets | RQ, all users | FR-SRC |
| UC-07 | Reserve asset | RQ | FR-RSV |
| UC-08 | Track request | RQ | FR-REQ |
| UC-09 | Cancel request | RQ | FR-REQ, FR-RSV |
| UC-10 | Save asset to watchlist | RQ | FR-SRC |
| UC-11 | Approve or reject transfer | AD | FR-APR, FR-TRF |
| UC-12 | Confirm receipt | RQ | FR-TRF |
| UC-13 | Report defect | AC, RQ | FR-MNT |
| UC-14 | Record repair | MS | FR-MNT |
| UC-15 | View asset history | AC, AD | FR-HST |
| UC-16 | Approve disposal | AD, FO | FR-DSP, FR-APR |
| UC-17 | Create user | SA | FR-USR |
| UC-18 | Assign role | SA | FR-USR |
| UC-19 | Deactivate user | SA | FR-USR |
| UC-20 | Log in | All users | FR-USR |
| UC-21 | Generate report | AD, FO, SO | FR-RPT |
| UC-22 | View audit log | SA, AD | FR-AUD |
| UC-23 | Receive notification | All users | FR-NTF |
| UC-24 | Schedule inspection | MS | FR-MNT |
| UC-25 | Approve donation or recycling | AD | FR-DSP, FR-APR |
| UC-26 | Classify asset (AI) | AC | FR-AI |
| UC-27 | View, accept or override match | RQ, AC | FR-AI |
| UC-28 | Review sustainability recommendation | SO | FR-AI, FR-SUS |
| UC-29 | Ask the assistant | All users | FR-AI |
| UC-30 | Generate AI report | AD, SO | FR-AI, FR-RPT |
| UC-31 | View sustainability dashboard | SO, AD | FR-SUS |
| UC-32 | Override an AI output | AC, AD, SO | FR-AI (BR-11, BR-12) |
| UC-33 | Detect duplicate listings | AC | FR-AI, FR-MKT |
| UC-34 | Predict maintenance need | MS | FR-AI, FR-MNT |
| UC-35 | Submit AI feedback | All users | FR-AI |

Actor codes: DR Department Representative, AC Asset Custodian, RQ Requester, AD Administrator, FO Finance Officer, MS Maintenance Staff, SO Sustainability Officer, SA System Administrator. PO (Procurement Officer) uses UC-06 and UC-21.


## 7.3 Use Case Descriptions (UC-01 to UC-35)

Actor codes: DR Department Representative, AC Asset Custodian, RQ Requester, AD Administrator, FO Finance Officer, MS Maintenance Staff, SO Sustainability Officer, SA System Administrator, PO Procurement Officer.
All use cases except UC-20 need the user to be logged in (UC-20).

---

### Group A: Assets and Marketplace (UC-01 to UC-04, UC-06, UC-10)

#### UC-01 Register asset

| Field | Description |
|---|---|
| Use case ID | UC-01 |
| Primary actor | AC, DR |
| Secondary actor | AI Service |
| Goal | Add a new asset to the system so it can be tracked from the start. |
| Preconditions | The user is logged in as AC or DR for the owning department. The asset is not already in the system. |
| Trigger | The user clicks "Register new asset". |
| Main flow | 1. The system shows the registration form. 2. The user enters name, category, tag number, condition, quantity and location, and can add photos. 3. The system checks required fields and that the tag number is new. 4. The system asks the AI Service for a category and shows it with a confidence score. 5. The user accepts or changes the category. 6. The system saves the asset with a unique ID and status "Registered". 7. The system records the history and audit entries. 8. The system confirms and offers to publish the asset. |
| Alternative flows | 2a. The user is not finished: the system saves a draft. 3a. A required field is empty: the system highlights it. 3b. The tag number already exists: the system shows the existing asset and the user cancels or corrects. 4a. The AI does not answer within 15 s: the user picks a category by hand. 5a. The user disagrees with the AI: the system saves the user's choice and keeps the suggestion in the log. |
| Postconditions | Success: a new asset exists, not yet public. Failure: no asset is created. |
| Rules and FRs | BR-11, BR-12, BR-13, BR-14; FR-AST, FR-AI, FR-HST, FR-AUD |

#### UC-02 Edit asset

| **Field** | **Description** |
|---|---|
| Use case ID | UC-02 |
| Primary actor | AC, DR |
| Goal | Correct or update the details of an existing asset. |
| Preconditions | The user is AC or DR for the owning department. The asset exists and is not disposed. |
| Trigger | The user opens an asset and clicks "Edit". |
| Main flow | 1. The system shows the asset form with current values. 2. The user changes one or more fields. 3. The system checks the new values. 4. The user clicks "Save". 5. The system updates the asset. 6. The system records the old and new values in the history and audit log. |
| Alternative flows | 4a. The user cancels: nothing changes. |
| Exception flows | 3a. A value is invalid: the system highlights it and does not save the changes. 5a. Someone else edited the asset in the meantime: the system shows the newer version and asks the user to reload. |
| Postconditions | Success: the asset shows the new values and the old ones stay in the history. Failure: the asset is unchanged. |
| Rules and FRs | BR-13, BR-14; FR-AST, FR-HST, FR-AUD |

#### UC-03 Publish surplus asset

| Field | Description |
|---|---|
| Use case ID | UC-03 |
| Primary actor | DR, AC |
| Secondary actor | AI Service, Notification Service |
| Goal | Make an unused asset visible to other departments so it can be reused. |
| Preconditions | The asset is registered and has no open request, reservation or disposal case. |
| Trigger | The user clicks "Publish as surplus" on an asset. |
| Main flow | 1. The system shows the publish form filled from the asset record. 2. The user checks title, condition, quantity, location and pickup notes. 3. The system asks the AI Service for a better title and keywords. 4. The user accepts or edits them. 5. The system checks for duplicate listings. 6. The user confirms publication. 7. The system sets the status to "Available" and shows the listing to authorised users. 8. The system records the action and notifies users who watch similar assets. |
| Alternative flows | 3a. The AI does not answer within 15 s: the user writes the text by hand. 5a. A duplicate is found: the system shows it and the user cancels or continues. 6a. The user cancels: nothing is published. |
| Postconditions | Success: the asset is listed and searchable. Failure: the asset keeps its old status. |
| Rules and FRs | BR-11, BR-13, BR-14; FR-MKT, FR-AI, FR-NTF |

#### UC-04 Withdraw listing

| Field | Description |
|---|---|
| Use case ID | UC-04 |
| Primary actor | DR, AC |
| Goal | Take a published asset off the marketplace. |
| Preconditions | The asset is published and the user belongs to the owning department. |
| Trigger | The user clicks "Withdraw listing". |
| Main flow | 1. The system shows the listing and any open requests. 2. The user gives a reason. 3. The system asks for confirmation. 4. The user confirms. 5. The system hides the listing and sets the asset status back to "In use". 6. The system notifies requesters with open requests. 7. The system records the action. |
| Alternative flows | 1a. An approved transfer is in progress: the system blocks the withdrawal and explains why. 4a. The user cancels: the listing stays. |
| Postconditions | Success: the listing is no longer visible. Failure: the listing stays. |
| Rules and FRs | BR-06, BR-14; FR-MKT, FR-NTF |

#### UC-06 Search and filter assets

| Field | Description |
|---|---|
| Use case ID | UC-06 |
| Primary actor | RQ and all users (including PO) |
| Goal | Find an available asset quickly. |
| Preconditions | The user is logged in. |
| Trigger | The user types in the search box or opens the filters. |
| Main flow | 1. The user enters keywords. 2. The user selects filters such as category, department, condition and location. 3. The system searches the published assets. 4. The system shows the results sorted by relevance with photo, name and status. 5. The user opens an asset to see its details. |
| Alternative flows | 3a. Nothing is found: the system suggests removing filters or asking the assistant (UC-29). 3b. The search takes too long: the system shows a message and the user tries again. |
| Postconditions | The user sees matching assets. No data changes. |
| Rules and FRs | FR-SRC, FR-MKT; NFR performance (results in 3 s) |

#### UC-10 Save asset to watchlist

| Field | Description |
|---|---|
| Use case ID | UC-10 |
| Primary actor | RQ |
| Goal | Follow an asset or a search and get notified when something fits. |
| Preconditions | The user is logged in. |
| Trigger | The user clicks "Watch" on an asset or a saved search. |
| Main flow | 1. The system shows the watch options (this asset, or this search). 2. The user picks one. 3. The system saves the watch. 4. The system confirms. 5. Later, when a matching asset is published or changes status, the system sends a notification (UC-23). |
| Alternative flows | 2a. The user already watches it: the system offers to stop watching. 5a. The user turns notifications off: the watch stays but no message is sent. |
| Postconditions | The watch is saved and appears in the user's list. |
| Rules and FRs | FR-SRC, FR-NTF |

### Group B: Requests and Transfers (UC-05, UC-07 to UC-09, UC-11, UC-12)

#### UC-05 Submit request

| Field | Description |
|---|---|
| Use case ID | UC-05 |
| Primary actor | RQ |
| Goal | Ask for a published asset. |
| Preconditions | The asset is published and available. |
| Trigger | The user clicks "Request this asset". |
| Main flow | 1. The system shows the asset details. 2. The user enters quantity, purpose and needed-by date. 3. The system checks availability. 4. The system creates the request with status "Pending". 5. The system notifies the asset owner. |
| Alternative flows | 3a. The asset is already reserved: the system offers a waiting list or similar assets. 2a. The user cancels: no request is created. |
| Postconditions | A pending request exists and appears in "Track request". |
| Rules and FRs | BR-04; FR-REQ, FR-NTF |

#### UC-07 Reserve asset

| Field | Description |
|---|---|
| Use case ID | UC-07 |
| Primary actor | RQ |
| Goal | Hold an asset for one requester while the request is processed. |
| Preconditions | The asset is available and the user has no other active reservation on it. |
| Trigger | The user clicks "Reserve". |
| Main flow | 1. The system shows the terms, including the 7-day expiry. 2. The user confirms. 3. The system marks the asset "Reserved" for this user. 4. The system starts the 7-day timer. 5. The system notifies the owner and the user. |
| Alternative flows | 3a. Someone reserved it first: the system rejects and shows other options. 4a. The timer reaches 7 days without approval: the reservation expires and the asset becomes "Available". |
| Postconditions | The asset is held for exactly one user. |
| Rules and FRs | BR-04; FR-RSV |

#### UC-08 Track request

| Field | Description |
|---|---|
| Use case ID | UC-08 |
| Primary actor | RQ |
| Goal | See where a request is in the process. |
| Preconditions | The user has at least one request. |
| Trigger | The user opens "My requests". |
| Main flow | 1. The system lists the user's requests with status. 2. The user opens one. 3. The system shows the timeline: submitted, reserved, approved or rejected, received. 4. The system shows the next step and who must act. |
| Alternative flows | 1a. The user has no requests: the system shows a message and a link to search. 3a. A request was rejected: the system shows the reason. |
| Postconditions | The user sees the current status. No data changes. |
| Rules and FRs | FR-REQ, FR-HST |

#### UC-09 Cancel request

| Field | Description |
|---|---|
| Use case ID | UC-09 |
| Primary actor | RQ |
| Goal | Withdraw a request that is no longer needed. |
| Preconditions | The request is "Pending" or "Reserved" and has not been received. |
| Trigger | The user clicks "Cancel request". |
| Main flow | 1. The system shows the request. 2. The user confirms the cancellation. 3. The system sets the status to "Cancelled". 4. The system releases any reservation. 5. The system notifies the asset owner. |
| Alternative flows | 1a. The transfer is already approved: the system explains that the administrator must cancel it. 2a. The user changes their mind: nothing changes. |
| Postconditions | The request is closed and the asset is available again. |
| Rules and FRs | BR-04, BR-14; FR-REQ, FR-RSV |

#### UC-11 Approve or reject transfer

| Field | Description |
|---|---|
| Use case ID | UC-11 |
| Primary actor | AD |
| Goal | Decide whether an asset may move to the requester. |
| Preconditions | A request is waiting for approval. |
| Trigger | The administrator opens the approval queue and picks a request. |
| Main flow | 1. The system shows the request, the asset and the history. 2. The administrator clicks "Approve". 3. The system asks for confirmation. 4. The system sets the status to "Approved" and records who approved it and when. 5. The system notifies the requester and the custodian. |
| Alternative flows | 2a. The administrator clicks "Reject": a reason is required and the asset is released. 5a. The requester does not confirm receipt within 14 days: the system flags the transfer. |
| Postconditions | The decision is stored and cannot be changed. |
| Rules and FRs | BR-06, BR-08, BR-13; FR-APR, FR-TRF, FR-NTF |

#### UC-12 Confirm receipt

| Field | Description |
|---|---|
| Use case ID | UC-12 |
| Primary actor | RQ |
| Goal | Confirm that the asset arrived, so ownership can move. |
| Preconditions | The transfer is approved and the asset was handed over. |
| Trigger | The user opens the approved request and clicks "Confirm receipt". |
| Main flow | 1. The system shows the asset and the handover details. 2. The user checks the condition and adds a note or photo if needed. 3. The user confirms. 4. The system moves the asset to the requester's department. 5. The system sets the request to "Completed". 6. The system records the history and notifies the previous owner. |
| Alternative flows | 2a. The asset is damaged or wrong: the user clicks "Report problem" and the administrator is notified (UC-13). 3a. 14 days pass without confirmation: the system sends a reminder and flags the transfer. |
| Postconditions | Success: ownership has changed and the history is updated. |
| Rules and FRs | BR-08, BR-13; FR-TRF, FR-HST |

---

### Group C: Maintenance and Life Cycle (UC-13 to UC-16, UC-24, UC-25)

#### UC-13 Report defect

| Field | Description |
|---|---|
| Use case ID | UC-13 |
| Primary actor | AC, RQ |
| Goal | Tell maintenance that an asset is faulty. |
| Preconditions | The asset exists and the user holds it or has just received it. |
| Trigger | The user clicks "Report defect". |
| Main flow | 1. The system shows the defect form. 2. The user describes the problem, picks a severity and adds photos. 3. The system creates a maintenance ticket. 4. The system sets the asset to "Needs inspection" and removes it from the marketplace if listed. 5. The system notifies maintenance staff. |
| Alternative flows | 2a. The description is empty: the system asks for it. 3a. A ticket is already open for the same defect: the system links to it. |
| Postconditions | A ticket exists and the asset cannot be requested until inspected. |
| Rules and FRs | BR-14; FR-MNT, FR-NTF; NFR safety inspection |

#### UC-14 Record repair

| Field | Description |
|---|---|
| Use case ID | UC-14 |
| Primary actor | MS |
| Goal | Log the work done on an asset. |
| Preconditions | A maintenance ticket is assigned to the user. |
| Trigger | The user opens the ticket and clicks "Record repair". |
| Main flow | 1. The system shows the ticket. 2. The user enters the work done, parts used, cost and time. 3. The user sets the result: repaired, partly repaired or not repairable. 4. The system saves the repair record. 5. The system updates the asset condition and status. 6. The system notifies the custodian. |
| Alternative flows | 3a. The asset is not repairable: the system suggests recycling or disposal and notifies the administrator (UC-25, UC-16). |
| Postconditions | The ticket is closed and the repair is in the asset history. |
| Rules and FRs | BR-13, BR-14; FR-MNT, FR-HST |

#### UC-15 View asset history

| Field | Description |
|---|---|
| Use case ID | UC-15 |
| Primary actor | AC, AD |
| Goal | See everything that happened to an asset. |
| Preconditions | The user may see this asset (own department, or administrator). |
| Trigger | The user opens the "History" tab of an asset. |
| Main flow | 1. The system loads the history. 2. The system shows events in time order: registered, edited, published, transferred, repaired, disposed. 3. The user filters by event type or date. 4. The user opens an event to see who did it and when. |
| Alternative flows | 1a. The user has no permission: the system shows an access-denied message. 2a. The history is long: the system shows it page by page. |
| Postconditions | The user sees the history. No data changes. |
| Rules and FRs | BR-13; FR-HST |

#### UC-16 Approve disposal

| Field | Description |
|---|---|
| Use case ID | UC-16 |
| Primary actor | AD; FO when the value is above AED 5,000 |
| Goal | Allow an asset to be removed from the campus when reuse is not possible. |
| Preconditions | A disposal request exists. The asset has no open request. Donation and recycling were considered. |
| Trigger | The administrator opens the disposal request. |
| Main flow | 1. The system shows value, condition, history and the options already tried. 2. The administrator approves. 3. If the value is above AED 5,000, the system sends it to the finance officer. 4. The system asks for confirmation. 5. The system sets the asset to "Disposed" and records the decision. |
| Alternative flows | 2a. The administrator sends it to donation or recycling instead (UC-25). 3a. The finance officer rejects: the disposal is cancelled. |
| Postconditions | The asset is closed, but its history stays readable. |
| Rules and FRs | BR-09, BR-10, BR-13; FR-DSP, FR-APR |

#### UC-24 Schedule inspection

| Field | Description |
|---|---|
| Use case ID | UC-24 |
| Primary actor | MS |
| Goal | Plan a safety or condition check. |
| Preconditions | The asset exists. |
| Trigger | The user clicks "Schedule inspection" or a defect was reported. |
| Main flow | 1. The system shows the asset and its last inspection date. 2. The user picks a date and the type of inspection. 3. The system saves the schedule. 4. The system notifies the custodian. 5. On the day, the system reminds the user. |
| Alternative flows | 2a. The date clashes with another inspection: the system suggests the next free slot. 5a. The inspection is missed: the system flags it as overdue. |
| Postconditions | An inspection is scheduled. |
| Rules and FRs | FR-MNT, FR-NTF; NFR safety inspection |

#### UC-25 Approve donation or recycling

| Field | Description |
|---|---|
| Use case ID | UC-25 |
| Primary actor | AD |
| Goal | Send an unused asset to donation or recycling instead of disposal. |
| Preconditions | A donation or recycling request exists. |
| Trigger | The administrator opens the request. |
| Main flow | 1. The system shows the asset, its condition and the proposed route. 2. The administrator checks the receiving party or recycler. 3. The administrator approves. 4. The system asks for confirmation. 5. The system sets the status to "Donated" or "Recycled" and records the decision. 6. The system notifies the owner and the sustainability officer. |
| Alternative flows | 3a. The administrator rejects: a reason is required and the request goes back to the owner. |
| Postconditions | The asset leaves the campus inventory and the sustainability numbers are updated. |
| Rules and FRs | BR-09, BR-10, BR-13; FR-DSP, FR-APR, FR-SUS |

---

### Group D: Administration and Reporting (UC-17 to UC-23)

#### UC-17 Create user

| Field | Description |
|---|---|
| Use case ID | UC-17 |
| Primary actor | SA |
| Goal | Give a new person access to the system. |
| Preconditions | The system administrator is logged in. |
| Trigger | The user clicks "Add user". |
| Main flow | 1. The system shows the user form. 2. The administrator enters name, university email and department. 3. The system checks that the email is new. 4. The system creates the account. 5. The system sends an activation email. 6. The administrator assigns a role (UC-18). |
| Alternative flows | 3a. The email already exists: the system shows the existing account. 5a. The email cannot be sent: the system shows an error and offers to resend. |
| Postconditions | An inactive account exists until the user activates it. |
| Rules and FRs | BR-14; FR-USR, FR-AUD |

#### UC-18 Assign role

| Field | Description |
|---|---|
| Use case ID | UC-18 |
| Primary actor | SA |
| Goal | Give a user the right permissions. |
| Preconditions | The user account exists. |
| Trigger | The administrator opens a user and clicks "Change role". |
| Main flow | 1. The system shows the current roles. 2. The administrator picks one or more roles. 3. The system shows the permissions this gives. 4. The administrator confirms. 5. The system saves the roles. 6. The system records the change. |
| Alternative flows | 4a. The administrator cancels: nothing changes. 5a. The change would remove the last system administrator: the system blocks it. |
| Postconditions | The user has the new permissions from the next login. |
| Rules and FRs | BR-14; FR-USR, FR-AUD |

#### UC-19 Deactivate user

| Field | Description |
|---|---|
| Use case ID | UC-19 |
| Primary actor | SA |
| Goal | Remove access for someone who has left or should no longer use the system. |
| Preconditions | The account exists and is active. |
| Trigger | The administrator clicks "Deactivate" on a user. |
| Main flow | 1. The system shows open requests and assets held by the user. 2. The administrator confirms. 3. The system disables the account and ends active sessions. 4. The system flags open items for reassignment. 5. The system records the action. |
| Alternative flows | 2a. The administrator cancels: nothing changes. 1a. The user is the only custodian of an asset: the system asks for a replacement first. |
| Postconditions | The user cannot log in. Their past records stay. |
| Rules and FRs | BR-13, BR-14; FR-USR, FR-AUD |

#### UC-20 Log in

| Field | Description |
|---|---|
| Use case ID | UC-20 |
| Primary actor | All users |
| Goal | Enter the system securely. |
| Preconditions | The user has an active account. |
| Trigger | The user opens the system. |
| Main flow | 1. The system shows the login page. 2. The user enters university email and password. 3. The system checks them. 4. The system loads the user's role. 5. The system shows the home page for that role. |
| Alternative flows | 3a. Wrong password: the system shows an error and lets the user try again. 3b. Too many failed attempts: the system locks the account for a short time. 3c. The account is deactivated: the system shows an access message. |
| Postconditions | The user has a session. Every failed or successful login is logged. |
| Rules and FRs | BR-14; FR-USR; NFR security |

#### UC-21 Generate report

| Field | Description |
|---|---|
| Use case ID | UC-21 |
| Primary actor | AD, FO, SO (PO may view) |
| Goal | Get a summary of assets, costs or reuse. |
| Preconditions | The user has report permission. |
| Trigger | The user opens "Reports". |
| Main flow | 1. The system shows the report types. 2. The user picks a type, period and department. 3. The system collects the data. 4. The system shows the report with tables and charts. 5. The user exports it to PDF or CSV. |
| Alternative flows | 3a. There is no data for the period: the system says so. 3b. The report takes too long: the system runs it in the background and notifies the user when done. |
| Postconditions | The report is shown or exported. The export is logged. |
| Rules and FRs | BR-14; FR-RPT |

#### UC-22 View audit log

| Field | Description |
|---|---|
| Use case ID | UC-22 |
| Primary actor | SA, AD |
| Goal | Check who did what and when. |
| Preconditions | The user has audit permission. |
| Trigger | The user opens "Audit log". |
| Main flow | 1. The system shows the latest log entries. 2. The user filters by user, action or date. 3. The system shows the matching entries. 4. The user opens an entry to see details. 5. The user exports the result if needed. |
| Alternative flows | 3a. No entries match: the system says so. |
| Postconditions | The user sees the log. Log entries cannot be edited or deleted. |
| Rules and FRs | BR-13, BR-14; FR-AUD |

#### UC-23 Receive notification

| Field | Description |
|---|---|
| Use case ID | UC-23 |
| Primary actor | All users |
| Secondary actor | Notification Service |
| Goal | Be told about events that need attention. |
| Preconditions | The user has an active account. |
| Trigger | An event happens, such as a new request, an approval or an expiring reservation. |
| Main flow | 1. The system finds who must be told. 2. The system creates the message. 3. The Notification Service sends it by email and in-app. 4. The user sees it in the notification list. 5. The user opens it and the system marks it as read. |
| Alternative flows | 3a. Email delivery fails: the in-app message is still shown and the system retries later. 4a. The user turned this type off: no message is sent. |
| Postconditions | The user has been informed. |
| Rules and FRs | FR-NTF |

---

### Group E: AI Layer and Sustainability (UC-26 to UC-35)

#### UC-26 Classify asset (AI)

| Field | Description |
|---|---|
| Use case ID | UC-26 |
| Primary actor | AC |
| Secondary actor | AI Service |
| Goal | Get a suggested category for an asset. |
| Preconditions | The asset has a name or description. |
| Trigger | The user registers or edits an asset, or clicks "Suggest category". |
| Main flow | 1. The system sends the text and photo to the AI Service. 2. The AI Service returns a category, a confidence score and a short reason. 3. The system shows them. 4. The user accepts or changes the category. 5. The system saves the final choice and the suggestion. |
| Alternative flows | 2a. No answer within 15 s: the user picks by hand. 4a. The confidence is low: the system warns the user to check. |
| Postconditions | The asset has a category chosen by a person. |
| Rules and FRs | BR-11, BR-12; FR-AI, FR-AST |

#### UC-27 View, accept or override match

| Field | Description |
|---|---|
| Use case ID | UC-27 |
| Primary actor | RQ, AC |
| Secondary actor | AI Service |
| Goal | See which assets or requests fit best and decide on them. |
| Preconditions | A request or a listing exists. |
| Trigger | The user opens "Suggested matches". |
| Main flow | 1. The system sends the request or listing to the AI Service. 2. The AI Service returns ranked matches with a confidence score and a reason. 3. The system shows them. 4. The user accepts one. 5. The system links the match and records the suggestion and the decision. |
| Alternative flows | 4a. The user rejects or picks another asset: the system stores the override (UC-32). 2a. No answer within 15 s: the system falls back to normal search (UC-06). |
| Postconditions | Nothing happens without the user's confirmation. |
| Rules and FRs | BR-11, BR-12; FR-AI, FR-SRC |

#### UC-28 Review sustainability recommendation

| Field | Description |
|---|---|
| Use case ID | UC-28 |
| Primary actor | SO |
| Secondary actor | AI Service |
| Goal | Check AI advice on reuse, repair, recycling or disposal. |
| Preconditions | The asset has history and a condition. |
| Trigger | The user opens the "Recommendations" list. |
| Main flow | 1. The system shows assets with a recommended next step. 2. The user opens one. 3. The system shows the advice, the reason, the confidence and the expected saving. 4. The user accepts, changes or rejects it. 5. The system records the decision. |
| Alternative flows | 4a. The user rejects it: a short reason is stored (UC-32). 1a. No recommendations exist: the system says so. |
| Postconditions | The decision is recorded. The advice is only applied if a person approves it. |
| Rules and FRs | BR-11, BR-12; FR-AI, FR-SUS |

#### UC-29 Ask the assistant

| Field | Description |
|---|---|
| Use case ID | UC-29 |
| Primary actor | All users |
| Secondary actor | AI Service |
| Goal | Get help in plain language, for example "Where can I find a projector?" |
| Preconditions | The user is logged in. |
| Trigger | The user opens the assistant chat. |
| Main flow | 1. The user types a question. 2. The system sends it to the AI Service with only the data the user may see. 3. The AI Service answers. 4. The system shows the answer with links to the assets or pages used. 5. The user follows a link or asks another question. |
| Alternative flows | 3a. No answer within 15 s: the system says the assistant is unavailable and suggests normal search. 4a. The assistant cannot answer: it says so and does not guess. |
| Postconditions | The conversation is saved for the user. No asset data is changed by the assistant. |
| Rules and FRs | BR-11; FR-AI; NFR privacy |

#### UC-30 Generate AI report

| Field | Description |
|---|---|
| Use case ID | UC-30 |
| Primary actor | AD, SO |
| Secondary actor | AI Service |
| Goal | Get a written summary of the data in a report. |
| Preconditions | The user has report permission and data exists. |
| Trigger | The user clicks "Write summary" on a report (UC-21). |
| Main flow | 1. The system sends the report data to the AI Service. 2. The AI Service writes a short summary with key findings. 3. The system shows the text next to the figures. 4. The user edits it. 5. The user saves or exports the report. |
| Alternative flows | 2a. No answer within 15 s: the report is shown without a summary. 3a. A figure in the text does not match the data: the user corrects it before saving. |
| Postconditions | The report has a summary checked by a person. |
| Rules and FRs | BR-11, BR-12; FR-AI, FR-RPT |

#### UC-31 View sustainability dashboard

| Field | Description |
|---|---|
| Use case ID | UC-31 |
| Primary actor | SO, AD |
| Goal | See how much the campus saves through reuse. |
| Preconditions | The user has dashboard permission. |
| Trigger | The user opens "Sustainability". |
| Main flow | 1. The system loads the figures. 2. The system shows assets reused, items recycled, money saved and estimated CO2 avoided. 3. The user picks a period or department. 4. The system updates the charts. 5. The user exports the view. |
| Alternative flows | 1a. Data is incomplete: the system shows a warning and the date of the last update. |
| Postconditions | The user sees the figures. No data changes. |
| Rules and FRs | FR-SUS, FR-RPT |

#### UC-32 Override an AI output

| Field | Description |
|---|---|
| Use case ID | UC-32 |
| Primary actor | AC, AD, SO |
| Goal | Replace an AI suggestion with the user's own decision. |
| Preconditions | The AI produced a suggestion that is shown to the user. |
| Trigger | The user clicks "Change" or "Reject" on a suggestion. |
| Main flow | 1. The system shows the suggestion. 2. The user chooses another value or rejects it. 3. The system asks for a short reason. 4. The user enters it. 5. The system saves the user's value, the original suggestion and the reason. |
| Alternative flows | 3a. The user skips the reason: the system accepts it but marks the reason as empty. |
| Postconditions | The final value is the user's. The override is available for review (UC-35). |
| Rules and FRs | BR-11, BR-12, BR-14; FR-AI, FR-AUD |

#### UC-33 Detect duplicate listings

| Field | Description |
|---|---|
| Use case ID | UC-33 |
| Primary actor | AC |
| Secondary actor | AI Service |
| Goal | Avoid listing the same asset twice. |
| Preconditions | The user is registering or publishing an asset. |
| Trigger | The user saves a new asset or listing. |
| Main flow | 1. The system sends the new text to the AI Service. 2. The AI Service compares it with existing listings. 3. The AI Service returns possible duplicates with a similarity score. 4. The system shows them. 5. The user decides whether they are the same. |
| Alternative flows | 4a. No duplicates: the system continues. 5a. The user says it is the same asset: the system opens the existing record. 2a. No answer within 15 s: the check is skipped. |
| Postconditions | The user decided; the system did not merge or delete anything alone. |
| Rules and FRs | BR-11, BR-12; FR-AI, FR-MKT |

#### UC-34 Predict maintenance need

| Field | Description |
|---|---|
| Use case ID | UC-34 |
| Primary actor | MS |
| Secondary actor | AI Service |
| Goal | See which assets are likely to need service soon. |
| Preconditions | Assets have age, repair and inspection history. |
| Trigger | The user opens "Maintenance forecast". |
| Main flow | 1. The system sends the asset data to the AI Service. 2. The AI Service returns assets ranked by risk, with a reason. 3. The system shows the list. 4. The user opens an asset. 5. The user schedules an inspection (UC-24) or ignores the suggestion. |
| Alternative flows | 2a. Not enough history: the system shows "not enough data". 2b. No answer within 15 s: the system shows the plain inspection schedule instead. |
| Postconditions | No action is taken without the user's decision. |
| Rules and FRs | BR-11, BR-12; FR-AI, FR-MNT |

#### UC-35 Submit AI feedback

| Field | Description |
|---|---|
| Use case ID | UC-35 |
| Primary actor | All users |
| Goal | Tell the team whether an AI answer was useful. |
| Preconditions | The user has seen an AI output. |
| Trigger | The user clicks the thumbs up or thumbs down on an AI output. |
| Main flow | 1. The system shows the feedback options. 2. The user picks "Helpful" or "Not helpful" and can add a comment. 3. The system saves the rating with the AI output it refers to. 4. The system thanks the user. |
| Alternative flows | 2a. The user closes the box: nothing is saved. |
| Postconditions | The feedback is stored and administrators can review it. |
| Rules and FRs | BR-12; FR-AI |

