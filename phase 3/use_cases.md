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

| Field | Description |
|---|---|
| Use case ID | UC-02 |
| Primary actor | AC, DR |
| Goal | Correct or update the details of an existing asset. |
| Preconditions | The user is AC or DR for the owning department. The asset exists and is not disposed. |
| Trigger | The user opens an asset and clicks "Edit". |
| Main flow | 1. The system shows the asset form with current values. 2. The user changes one or more fields. 3. The system checks the new values. 4. The user clicks "Save". 5. The system updates the asset. 6. The system records the old and new values in the history and audit log. |
| Alternative flows | 3a. A value is invalid: the system highlights it. 4a. The user cancels: nothing changes. 5a. Someone else edited the asset in the meantime: the system shows the newer version and asks the user to reload. |
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

