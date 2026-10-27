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

```mermaid
flowchart LR
    SA["System Administrator"]
    AD["Administrator"]
    U["Any user"]

    P11("1.1 Log In")
    P12("1.2 Create User")
    P13("1.3 Assign Role")
    P14("1.4 Deactivate User")
    P10("10.0 Record Audit Events")

    D1[["D1 Users"]]
    D5[["D5 Requests and Reservations"]]

    U -->|"Email and password"| P11
    D1 -->|"Account record"| P11
    P11 -->|"Login result"| U
    P11 -->|"Audit event"| P10

    SA -->|"New account data"| P12
    AD -->|"New account data"| P12
    U -->|"Self-registration data"| P12
    D1 -->|"Existing email addresses"| P12
    P12 -->|"New user record"| D1
    P12 -->|"Account result"| SA
    P12 -->|"Audit event"| P10

    SA -->|"Role change order"| P13
    AD -->|"Role change order"| P13
    D1 -->|"Current role record"| P13
    P13 -->|"Updated user record"| D1
    P13 -->|"Role change result"| SA
    P13 -->|"Audit event"| P10

    SA -->|"Deactivation order"| P14
    AD -->|"Deactivation order"| P14
    D1 -->|"Account record"| P14
    D5 -->|"Open items of the user"| P14
    P14 -->|"Inactive user record"| D1
    P14 -->|"Deactivation result"| SA
    P14 -->|"Audit event"| P10
```

| Process | Does what | Requirements |
|---|---|---|
| 1.1 Log In | Checks email, password and active status. Shows one general error if the login is wrong | FR-USR-03, NFR-08 |
| 1.2 Create User | Creates an account with a unique email. Self-registration makes an inactive Requester account | FR-USR-01, FR-USR-02 |
| 1.3 Assign Role | Changes the role. Never changes it for an inactive account | FR-USR-05, BR-16 |
| 1.4 Deactivate User | Blocks login. Open requests and approvals must be moved first. The last active administrator cannot deactivate itself | FR-USR-05 and its error rules |

## 1.2 Process 8.0 – Generate Reports

```mermaid
flowchart LR
    AD["Administrator"]
    PO["Procurement Officer"]
    FO["Finance Officer"]
    SO["Sustainability Officer"]

    P81("8.1 Collect Report Data")
    P82("8.2 Format and Export Report")
    P10("10.0 Record Audit Events")

    D2[["D2 Assets"]]
    D5[["D5 Requests and Reservations"]]
    D6[["D6 Approvals"]]
    D7[["D7 Transfers"]]
    D8[["D8 Maintenance Records"]]
    D11[["D11 Sustainability Records"]]
    D12[["D12 Reports"]]

    AD -->|"Report type and filters"| P81
    PO -->|"Report type and filters"| P81
    FO -->|"Report type and filters"| P81
    SO -->|"Report type and filters"| P81
    D2 -->|"Asset data"| P81
    D5 -->|"Request data"| P81
    D6 -->|"Approval data"| P81
    D7 -->|"Transfer data"| P81
    D8 -->|"Maintenance data"| P81
    D11 -->|"Sustainability figures"| P81
    P81 -->|"Report data set"| P82
    P82 -->|"Report record"| D12
    P82 -->|"Report on screen or CSV file"| AD
    P82 -->|"Report on screen or CSV file"| FO
    P82 -->|"Export event"| P10
```

| Process | Does what | Requirements |
|---|---|---|
| 8.1 Collect Report Data | Reads the data the user may see, applies the filters (date range, department, category, status). Financial data only for FO, AD and other allowed roles | FR-RPT-01, FR-RPT-02, FR-RPT-04 |
| 8.2 Format and Export Report | Shows the report or makes a CSV with report name and time. Shows "No results found." when empty | FR-RPT-03, NFR-02 |

## 1.3 Processes 9.0 and 10.0 – Notifications and Audit

```mermaid
flowchart LR
    NS["Notification Service"]
    U["Any user"]
    AD["Administrator"]
    SA["System Administrator"]

    P91("9.1 Create Notification")
    P92("9.2 Deliver Notification")
    P93("9.3 Show Notifications")
    P101("10.1 Record Audit Entry")
    P102("10.2 Show Audit Log")
    P4("4.0 Process Approvals and Transfers")
    P5("5.0 Manage Maintenance and End of Life")
    P1("1.0 Manage Users and Access")

    D1[["D1 Users"]]
    D13[["D13 Notifications"]]
    D14[["D14 Audit Log"]]

    P4 -->|"Notification events"| P91
    P5 -->|"Notification events"| P91
    D1 -->|"Recipient settings"| P91
    P91 -->|"New notification"| D13
    P91 -->|"Notification to send"| P92
    P92 -->|"Email message"| NS
    NS -->|"Delivery status"| P92
    P92 -->|"Delivery result"| D13

    U -->|"Notification request"| P93
    D13 -->|"Own notifications"| P93
    P93 -->|"Notification list"| U
    P93 -->|"Read mark"| D13

    P1 -->|"Audit events"| P101
    P4 -->|"Audit events"| P101
    P101 -->|"Audit entry"| D14

    AD -->|"Audit filter"| P102
    SA -->|"Audit filter"| P102
    D14 -->|"Audit entries"| P102
    P102 -->|"Audit log view"| AD
    P102 -->|"Audit log view"| SA
```

| Process | Does what | Requirements |
|---|---|---|
| 9.1 Create Notification | Finds the users involved in an event and creates in-app messages | FR-NTF-01, FR-NTF-02, FR-NTF-04 |
| 9.2 Deliver Notification | Sends an email to users who turned it on. If the email fails, the workflow continues and the in-app message stays | FR-NTF-03 and its error rules |
| 9.3 Show Notifications | Shows only the user's own messages. The user marks them as read | FR-NTF-04 |
| 10.1 Record Audit Entry | Writes audit ID, actor, action, record, time, outcome and old and new values. Passwords are never stored | FR-AUD-01, FR-AUD-02, BR-14 |
| 10.2 Show Audit Log | Shows and filters entries by user, action, record and date. Only AD and SA | FR-AUD-04, FR-AUD-03 |

> 
---

