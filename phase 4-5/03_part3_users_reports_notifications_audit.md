# Phase 4 & 5 – Part 3: Users, Access, Reports, Notifications and Audit

**Owner:** Mohammed Alketbi
**Use cases:** UC-17 Create user, UC-18 Assign role, UC-19 Deactivate user, UC-20 Log in, UC-21 Generate report, UC-22 View audit log, UC-23 Receive notification
**Requirement groups:** FR-USR, FR-RPT, FR-NTF, FR-AUD (and the security rules BR-07, BR-14, BR-16, NFR-08 to 11)
**Data stores:** D1 Users, D12 Reports, D13 Notifications, D14 Audit Log
**Tables:** DEPARTMENT, USER, ROLE_PERMISSION, REPORT, NOTIFICATION, AUDIT_LOG

Shared diagrams (architecture, the one Level 0 DFD, ER diagram) are in `00_architecture_and_shared_design.md`.

---

# 1. Sequence Diagrams

## 1.1 UC-20 Log In

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant UI as Web Page
    participant AuthController
    participant AuthService
    participant DB as Database
    participant Audit as History and Audit

    U->>UI: Open the login page
    UI-->>U: Show login form
    U->>UI: Enter email and password, click "Log in"
    UI->>AuthController: POST /login
    activate AuthController
    AuthController->>AuthService: login(email, password)
    activate AuthService
    AuthService->>DB: find user by email
    DB-->>AuthService: user record or nothing
    alt email not found or password is wrong
        AuthService->>Audit: record failed login
        AuthService-->>AuthController: failed
        AuthController-->>UI: general error
        UI-->>U: Show "Email or password is not correct"
    else account is inactive
        AuthService->>Audit: record denied login
        AuthService-->>AuthController: failed
        AuthController-->>UI: general error
        UI-->>U: Show "Email or password is not correct"
    else login is correct
        AuthService->>AuthService: create session with role and department
        AuthService->>Audit: record successful login
        AuthService-->>AuthController: session
        deactivate AuthService
        AuthController-->>UI: session cookie and role
        deactivate AuthController
        UI-->>U: Show home page for the role
    end
```

Both wrong-password and inactive-account give the same message, so nobody can find out which emails exist (FR-USR error rules).

## 1.2 Self-Registration (FR-USR-02)

```mermaid
sequenceDiagram
    autonumber
    actor V as New user
    participant UI as Web Page
    participant AuthController
    participant UserService
    participant DB as Database
    participant Noti as Notification Module
    actor SA as System Administrator

    V->>UI: Click "Register", enter name, email, department, password
    UI->>AuthController: POST /register
    AuthController->>UserService: selfRegister(data)
    UserService->>UserService: check password length 12 to 128 characters
    UserService->>DB: check that email is unique
    alt email exists or password is invalid
        UserService-->>AuthController: error
        AuthController-->>UI: error
        UI-->>V: Show the problem
    else data is valid
        UserService->>DB: save user with role "Requester" and status "Inactive"
        UserService->>Noti: notify administrators
        Noti->>SA: "New account waiting for activation"
        UserService-->>AuthController: saved
        AuthController-->>UI: saved
        UI-->>V: Show "Wait for activation"
    end
```

## 1.3 UC-17 Create User

```mermaid
sequenceDiagram
    autonumber
    actor SA as System Administrator
    participant UI as Web Page
    participant UserController
    participant Security
    participant UserService
    participant DB as Database
    participant Noti as Notification Module
    participant Audit as History and Audit

    SA->>UI: Open "Users", click "Add user"
    UI-->>SA: Show form
    SA->>UI: Enter name, email, department, role
    UI->>UserController: POST /users
    activate UserController
    UserController->>Security: checkPermission(SA, "manage users")
    Security-->>UserController: allowed
    UserController->>UserService: createUser(data)
    activate UserService
    UserService->>DB: check that email is unique
    DB-->>UserService: result
    alt email already exists or format is wrong
        UserService-->>UserController: error
        UserController-->>UI: error
        UI-->>SA: Highlight the email field
    else data is valid
        UserService->>DB: save user with a first password setup link
        UserService->>Audit: record account creation
        UserService->>Noti: send activation email
        opt email service is down
            Noti-->>UserService: failed, queued for retry
        end
        UserService-->>UserController: user ID
        deactivate UserService
        UserController-->>UI: success
        deactivate UserController
        UI-->>SA: Show "Account created"
    end
```

## 1.4 UC-18 Assign Role

```mermaid
sequenceDiagram
    autonumber
    actor SA as System Administrator
    participant UI as Web Page
    participant UserController
    participant UserService
    participant DB as Database
    participant Audit as History and Audit

    SA->>UI: Open a user, click "Change role"
    UI->>UserController: GET /roles
    UserController-->>UI: role list
    UI-->>SA: Show roles
    SA->>UI: Select role, click "Save"
    UI->>UserController: PUT /users/{id}/role
    activate UserController
    UserController->>UserService: assignRole(userId, role)
    activate UserService
    UserService->>DB: read user
    DB-->>UserService: user with status
    alt user is inactive (was deactivated meanwhile)
        UserService-->>UserController: cancelled
        UserController-->>UI: message
        UI-->>SA: Show "User is inactive"
    else user is active
        UserService->>DB: save new role
        UserService->>Audit: record old and new role
        UserService-->>UserController: done
        deactivate UserService
        UserController-->>UI: success
        deactivate UserController
        UI-->>SA: Show "Role updated"
    end
```

## 1.5 UC-19 Deactivate User

```mermaid
sequenceDiagram
    autonumber
    actor SA as System Administrator
    participant UI as Web Page
    participant UserController
    participant UserService
    participant DB as Database
    participant Audit as History and Audit

    SA->>UI: Open a user, click "Deactivate"
    UI->>UserController: PUT /users/{id}/deactivate
    activate UserController
    UserController->>UserService: deactivate(userId)
    activate UserService
    UserService->>DB: count active administrators, read open requests and approvals
    DB-->>UserService: counts and list
    alt user is the last active administrator
        UserService-->>UserController: blocked
        UserController-->>UI: message
        UI-->>SA: Show "Keep at least one active administrator"
    else user has open requests or approvals
        UserService-->>UserController: list of open items
        UserController-->>UI: list
        UI-->>SA: Show list, ask to reassign first
    else user can be deactivated
        UserService->>DB: set status "Inactive", end all sessions
        UserService->>Audit: record deactivation
        UserService-->>UserController: done
        deactivate UserService
        UserController-->>UI: success
        deactivate UserController
        UI-->>SA: Show "User deactivated"
    end
```

## 1.6 UC-21 Generate Report

```mermaid
sequenceDiagram
    autonumber
    actor U as AD, FO, PO, SO (DR, AC, MS own department)
    participant UI as Web Page
    participant ReportController
    participant Security
    participant ReportService
    participant DB as Database
    participant Audit as History and Audit

    U->>UI: Open "Reports", choose type, set filters
    UI->>ReportController: POST /reports
    activate ReportController
    ReportController->>Security: checkPermission(user, report type)
    alt user may not see this report (for example financial data)
        Security-->>ReportController: denied
        ReportController->>Audit: record denied attempt
        ReportController-->>UI: access denied
        UI-->>U: Show "No access"
    else user may see the report
        Security-->>ReportController: allowed with department scope
        ReportController->>ReportService: generate(type, filters, scope)
        activate ReportService
        ReportService->>ReportService: check date range
        alt date range is invalid
            ReportService-->>ReportController: error
            ReportController-->>UI: error
            UI-->>U: Show "Invalid date range"
        else date range is valid
            ReportService->>DB: read data for the report
            alt data source times out
                DB-->>ReportService: timeout
                ReportService-->>UI: offer to run the report in the background
            else data is read
                DB-->>ReportService: rows
                alt no rows
                    ReportService-->>UI: empty report
                    UI-->>U: Show "No results found."
                else rows found
                    ReportService->>DB: save report record
                    ReportService-->>ReportController: report
                    deactivate ReportService
                    ReportController-->>UI: report
                    deactivate ReportController
                    UI-->>U: Show report
                    opt user clicks "Export CSV"
                        U->>UI: Export
                        UI->>ReportController: GET /reports/{id}/csv
                        ReportController->>Audit: record export
                        ReportController-->>UI: CSV file with name and time
                    end
                end
            end
        end
    end
```

## 1.7 UC-22 View Audit Log

```mermaid
sequenceDiagram
    autonumber
    actor U as SA or AD
    participant UI as Web Page
    participant AuditController
    participant Security
    participant AuditService
    participant DB as Database

    U->>UI: Open "Audit log", set filters (user, action, record, dates)
    UI->>AuditController: GET /audit?filters=...
    activate AuditController
    AuditController->>Security: checkPermission(user, "view audit")
    alt user is not SA or AD
        Security-->>AuditController: denied
        AuditController-->>UI: access denied
        UI-->>U: Show "No access"
    else user is SA or AD
        Security-->>AuditController: allowed
        AuditController->>AuditService: search(filters)
        activate AuditService
        AuditService->>DB: read entries (read only)
        DB-->>AuditService: entries
        alt result is too large
            AuditService-->>AuditController: ask for a narrower filter
            AuditController-->>UI: message
            UI-->>U: Show "Narrow your filter"
        else result fits
            AuditService-->>AuditController: entries
            deactivate AuditService
            AuditController-->>UI: entries
            deactivate AuditController
            UI-->>U: Show entries
        end
    end
```

## 1.8 UC-23 Receive Notification

```mermaid
sequenceDiagram
    autonumber
    participant Svc as Any Service (for example ApprovalService)
    participant NotificationService
    participant DB as Database
    participant Mail as Email Service
    actor U as User
    participant UI as Web Page

    Svc->>NotificationService: notify(eventType, involvedUsers)
    activate NotificationService
    NotificationService->>DB: save one in-app notification per user (status "Unread")
    opt user turned on email notifications
        NotificationService->>Mail: send email
        alt email service is down
            Mail-->>NotificationService: failed
            NotificationService->>DB: keep message, queue email for retry
        else email sent
            Mail-->>NotificationService: delivery status
        end
    end
    deactivate NotificationService
    U->>UI: Open the page, see the bell with a number
    UI->>NotificationService: GET /notifications (own only)
    NotificationService->>DB: read own notifications
    DB-->>NotificationService: list
    NotificationService-->>UI: list
    UI-->>U: Show messages
    U->>UI: Click a message
    UI->>NotificationService: PUT /notifications/{id}/read
    NotificationService->>DB: set status "Read"
```

---

# 2. Class Diagram

```mermaid
classDiagram
    class Department {
        +int deptId
        +String name
        +int repUserId
    }
    class User {
        +int userId
        +String name
        +String email
        +String passwordHash
        +Role role
        +int deptId
        +UserStatus status
        +boolean emailNotifications
        +isActive() boolean
        +checkPassword(pw) boolean
        +deactivate() void
    }
    class RolePermission {
        +Role role
        +String action
        +String scope
        +allows(action) boolean
    }
    class Report {
        +int reportId
        +String reportType
        +int generatedBy
        +Date periodStart
        +Date periodEnd
        +boolean aiGenerated
        +boolean reviewed
        +String content
        +exportCsv() File
    }
    class Notification {
        +int notificationId
        +int userId
        +String eventType
        +String message
        +NotificationStatus status
        +DateTime createdAt
        +markRead() void
    }
    class AuditLogEntry {
        +int auditId
        +int actorId
        +String action
        +String recordRef
        +String outcome
        +String oldValue
        +String newValue
        +DateTime eventTime
    }
    class Role {
        <<enumeration>>
        DR
        AC
        RQ
        AD
        PO
        FO
        MS
        SO
        SA
    }
    class UserStatus {
        <<enumeration>>
        Active
        Inactive
    }
    class NotificationStatus {
        <<enumeration>>
        Unread
        Read
    }

    class AuthService {
        +login(email, password) Session
        +logout(session) void
        +selfRegister(data) User
    }
    class SecurityService {
        +checkPermission(user, action, record) boolean
        +departmentScope(user) List
        +isOwnDepartment(user, record) boolean
    }
    class UserService {
        +createUser(data) User
        +assignRole(userId, role) void
        +deactivate(userId) void
        +validatePassword(pw) boolean
    }
    class ReportService {
        +generate(type, filters, scope) Report
        +exportCsv(reportId) File
        +validateDateRange(from, to) boolean
    }
    class NotificationService {
        +notify(eventType, users) void
        +list(userId) List
        +markRead(id) void
        +retryEmails() void
    }
    class AuditService {
        +record(actor, action, record, outcome, oldValue, newValue) void
        +search(filters) List
    }
    class AuthController {
        +postLogin() Response
        +postRegister() Response
    }
    class UserController {
        +postUser() Response
        +putRole() Response
        +putDeactivate() Response
    }
    class ReportController {
        +postReport() Response
        +getCsv() Response
    }
    class AuditController {
        +getAudit() Response
    }
    class NotificationController {
        +getNotifications() Response
        +putRead() Response
    }

    Department "1" --> "0..*" User : has
    User --> Role
    User --> UserStatus
    Notification --> NotificationStatus
    User "1" --> "0..*" Notification : receives
    User "1" --> "0..*" AuditLogEntry : performs
    User "1" --> "0..*" Report : generates
    RolePermission --> Role

    AuthController ..> AuthService
    UserController ..> UserService
    ReportController ..> ReportService
    AuditController ..> AuditService
    NotificationController ..> NotificationService
    AuthService ..> User
    AuthService ..> AuditService
    UserService ..> User
    UserService ..> AuditService
    ReportService ..> Report
    ReportService ..> SecurityService
    NotificationService ..> Notification
    SecurityService ..> RolePermission
    SecurityService ..> User
```

| Class | Role | Rule it enforces |
|---|---|---|
| AuthService | Login, logout, self-registration | FR-USR-02 to 04, NFR-08 |
| SecurityService | One place that checks role, department and active status before every action | FR-USR-06, BR-07, BR-16 |
| UserService | Create, change role, deactivate | FR-USR-01, FR-USR-05, last administrator rule |
| ReportService | Build, filter and export reports | FR-RPT-01 to 04 |
| NotificationService | Create, deliver and list notifications | FR-NTF-01 to 04 |
| AuditService | Writes entries (never edits or deletes) and searches them | FR-AUD-01 to 04, BR-14 |
| RolePermission | Stores the permission matrix of Phase 3 (Section 2.4) as data | BR-16 |

---

# 3. User Interface Mockups

## 3.1 Login and Register (UC-20, FR-USR-02)

```text
+----------------------------------------------+
|        Circular Campus Resource Exchange     |
|                                              |
|   Email      [______________________]        |
|   Password   [______________________]        |
|                                              |
|              [        Log in        ]        |
|   No account?  Register as a requester       |
|                                              |
|   Wrong details show one general message:    |
|   "Email or password is not correct"         |
+----------------------------------------------+
```

## 3.2 User Management (UC-17, UC-18, UC-19)

```text
+----------------------------------------------------------------------+
|  Users                                         (System Administrator)|
|  Search [__________]  Role [ All v ]  Status [ All v ] [ + Add user ]|
|                                                                      |
|  Name            Email            Dept       Role   Status           |
|  A. Hassan       a.h@univ.ae      CS         DR     Active           |
|  K. Saeed        k.s@univ.ae      Business   RQ     Inactive         |
|  M. Rashid       m.r@univ.ae      IT         SA     Active           |
|                                                                      |
|  [Change role]  [Deactivate]  [Activate]                             |
+----------------------------------------------------------------------+
|  Add user                                                            |
|  Name *  [__________]   Email * [______________]                     |
|  Department * [ v ]     Role * [ v ]                                 |
|                                    [ Cancel ]  [ Create account ]    |
+----------------------------------------------------------------------+
```

## 3.3 Reports (UC-21)

```text
+----------------------------------------------------------------------+
|  Reports                                                             |
|  Report  [ Completed transfers v ]                                   |
|  From [ yyyy-mm-dd ]  To [ yyyy-mm-dd ]  Department [ All v ]        |
|  Category [ All v ]   Status [ All v ]              [ Generate ]     |
|                                                                      |
|  Completed transfers, 2026-09-01 to 2026-09-30     Made 2026-10-01   |
|  Asset            From      To          Date         Value (AED)*    |
|  Lab bench stool  CS        Business    2026-09-20   3,000           |
|  Projector        IT        Eng.        2026-09-25   1,800           |
|                                                                      |
|  * Value column only for FO, AD and allowed roles                    |
|                                                  [ Export CSV ]      |
|  Empty result: "No results found."                                   |
+----------------------------------------------------------------------+
```

## 3.4 Audit Log (UC-22)

```text
+----------------------------------------------------------------------+
|  Audit log                                      (SA or Administrator)|
|  User [____]  Action [ All v ]  Record [____]  From [ ]  To [ ]      |
|                                                    [ Search ]        |
|                                                                      |
|  Time              User   Action          Record  Outcome            |
|  2026-10-21 09:12  AD01   Approve         A-101   Success            |
|  2026-10-21 09:20  RQ07   Approve         A-101   Denied             |
|  2026-10-21 10:02  SA01   Change role     U-33    Success            |
|  Details: old value DR -> new value AC                               |
|                                                                      |
|  Read only. Entries cannot be edited or deleted.                     |
+----------------------------------------------------------------------+
```

## 3.5 Notifications (UC-23)

```text
+----------------------------------------------------------------------+
|  Circular Campus                                [ Bell (3) ]  (RQ) v |
+----------------------------------------------------------------------+
|  Notifications                                                       |
|  * Your request R-0042 was approved                       5 min ago  |
|  * Transfer T-0031 is ready for pickup                    2 h ago    |
|    Reservation of Lab bench stool expires in 1 day        1 day ago  |
|                                                                      |
|  (* = unread)                       [ Mark all as read ]             |
|  Settings: [x] Also send me emails                                   |
+----------------------------------------------------------------------+
```

---

# 4. Traceability

| Diagram | Use case | Requirements |
|---|---|---|
| Sequence 1.3 | UC-17 Create user | FR-USR-01, FR-USR-02, FR-AUD-01 |
| Sequence 1.4 | UC-18 Assign role | FR-USR-05, BR-16 |
| Sequence 1.5 | UC-19 Deactivate user | FR-USR-05 |
| Sequence 1.1, 1.2 | UC-20 Log in | FR-USR-02 to 04, FR-USR-06 |
| Sequence 1.6 | UC-21 Generate report | FR-RPT-01 to 04 |
| Sequence 1.7 | UC-22 View audit log | FR-AUD-01 to 04 |
| Sequence 1.8 | UC-23 Receive notification | FR-NTF-01 to 04 |

