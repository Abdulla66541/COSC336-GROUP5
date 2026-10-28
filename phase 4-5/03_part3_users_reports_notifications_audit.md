# Phase 4 & 5 – Part 3: Users, Access, Reports, Notifications and Audit

**Owner:** Mohammed Alketbi
**Use cases:** UC-17 Create user, UC-18 Assign role, UC-19 Deactivate user, UC-20 Log in, UC-21 Generate report, UC-22 View audit log, UC-23 Receive notification
**Requirement groups:** FR-USR, FR-RPT, FR-NTF, FR-AUD (and the security rules BR-07, BR-14, BR-16, NFR-08 to 11)
**Data stores:** D1 Users, D12 Reports, D13 Notifications, D14 Audit Log
**Tables:** DEPARTMENT, USER, ROLE_PERMISSION, REPORT, NOTIFICATION, AUDIT_LOG

Shared diagrams (architecture, context, Level 0 DFD, ER diagram) are in `00_architecture_and_shared_design.md`.

---

# 1. Data Flow Diagrams, Level 1

## 1.1 Process 1.0 – Manage Users and Access

<img width="4620" height="1552" alt="01_1_1_process_1_0_manage_users_and_access drawio" src="https://github.com/user-attachments/assets/fd004703-7757-4d2f-a726-b679e181b2d7" />






| Process | Does what | Requirements |
|---|---|---|
| 1.1 Log In | Checks email, password and active status. Shows one general error if the login is wrong | FR-USR-03, NFR-08 |
| 1.2 Create User | Creates an account with a unique email. Self-registration makes an inactive Requester account | FR-USR-01, FR-USR-02 |
| 1.3 Assign Role | Changes the role. Never changes it for an inactive account | FR-USR-05, BR-16 |
| 1.4 Deactivate User | Blocks login. Open requests and approvals must be moved first. The last active administrator cannot deactivate itself | FR-USR-05 and its error rules |

## 1.2 Process 8.0 – Generate Reports

<img width="6448" height="1814" alt="2 drawio" src="https://github.com/user-attachments/assets/501316ca-f9b4-491b-90ff-87aa66a52b49" />


| Process | Does what | Requirements |
|---|---|---|
| 8.1 Collect Report Data | Reads the data the user may see, applies the filters (date range, department, category, status). Financial data only for FO, AD and other allowed roles | FR-RPT-01, FR-RPT-02, FR-RPT-04 |
| 8.2 Format and Export Report | Shows the report or makes a CSV with report name and time. Shows "No results found." when empty | FR-RPT-03, NFR-02 |

## 1.3 Processes 9.0 and 10.0 – Notifications and Audit

<img width="5920" height="1526" alt="01_1_1_process_1_0_manage_users_and_access drawio (2)" src="https://github.com/user-attachments/assets/d9cc6227-ea61-438a-88ef-9d101cf6026b" />


| Process | Does what | Requirements |
|---|---|---|
| 9.1 Create Notification | Finds the users involved in an event and creates in-app messages | FR-NTF-01, FR-NTF-02, FR-NTF-04 |
| 9.2 Deliver Notification | Sends an email to users who turned it on. If the email fails, the workflow continues and the in-app message stays | FR-NTF-03 and its error rules |
| 9.3 Show Notifications | Shows only the user's own messages. The user marks them as read | FR-NTF-04 |
| 10.1 Record Audit Entry | Writes audit ID, actor, action, record, time, outcome and old and new values. Passwords are never stored | FR-AUD-01, FR-AUD-02, BR-14 |
| 10.2 Show Audit Log | Shows and filters entries by user, action, record and date. Only AD and SA | FR-AUD-04, FR-AUD-03 |


---

# 2. Sequence Diagrams

## 2.1 UC-20 Log In

<img width="2848" height="2464" alt="01_1_1_process_1_0_manage_users_and_access drawio (3)" src="https://github.com/user-attachments/assets/13517bcc-f1d0-4808-96ab-e9fdfb460c27" />


Both wrong-password and inactive-account give the same message, so nobody can find out which emails exist (FR-USR error rules).

## 2.2 Self-Registration (FR-USR-02)

<img width="3750" height="1880" alt="5 drawio" src="https://github.com/user-attachments/assets/81e5387a-aead-4944-b409-9344ce34c6d8" />


## 2.3 UC-17 Create User

<img width="3688" height="2382" alt="6 drawio" src="https://github.com/user-attachments/assets/82cfe126-2bae-4758-8b95-fa9ad4f031ab" />


## 2.4 UC-18 Assign Role

<img width="2472" height="2130" alt="7 drawio" src="https://github.com/user-attachments/assets/d8744bf7-2603-48a6-858a-82606505f7a6" />


## 2.5 UC-19 Deactivate User

<img width="3144" height="2068" alt="8 drawio" src="https://github.com/user-attachments/assets/20add6f3-3f17-4230-a296-943c8b6606a4" />
