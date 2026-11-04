
# Phase 4 & 5 — Part 2: Approvals, Transfers, Maintenance and End-of-Life

**Project:** Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System  
**Course:** COSC336 — Introduction to Software Engineering  
**Group:** 5  
**Contributor:** Mubarak Saif Mubarak Jarash Alkhyeli  

## 1. Scope and Design Basis

This section covers eight use cases: **UC-11** Approve or Reject Transfer, **UC-12** Confirm Receipt, **UC-13** Report Defect, **UC-14** Record Repair, **UC-15** View Asset History, **UC-16** Approve Disposal, **UC-24** Schedule Inspection, and **UC-25** Approve Donation or Recycling.

The designs trace to **FR-APR, FR-TRF, FR-MNT, FR-HST, FR-DSP, FR-USR, FR-NTF,** and **FR-AUD** in Phase 3.

Relevant database tables are `APPROVAL`, `TRANSFER`, `MAINTENANCE_TICKET`, `REPAIR_RECORD`, `END_OF_LIFE_REQUEST`, and `ASSET_HISTORY`.

The shared data stores are D3 Asset History, D6 Approvals, D7 Transfers, D8 Maintenance Records, and D9 End-of-Life Requests.

The transfer and maintenance state models are in Phase 3 Sections 6.2.1 and 6.2.2, respectively.

The team's consolidated architecture and entity-relationship model belong in `00_architecture_and_shared_design.md`.

### 1.1 Key Design Rules

- The owning Department Representative (DR) must approve asset release before the Administrator (AD) can give final transfer approval.
- A rejection requires a reason containing at least 10 characters.
- Each completed approval stage stores the approver, decision, timestamp, and reason when applicable.
- A transfer must receive the required approvals before scheduling and handover.
- The receiving Requester (RQ) confirms receipt before custody and location are updated.
- Assets under repair or involved in conflicting active transfers cannot be transferred.
- Repair work requires Administrator authorisation, and a separate authorised user verifies completed repairs.
- Disposal requires Administrator and Finance Officer approval. Donation and recycling require Administrator approval.
- All important decisions are recorded in the system's history and audit records.

## 2. Context Diagram

The context diagram shows the interactions between the Circular Campus System and its external users. The system is represented as a single process, while each actor exchanges relevant information with it.

```mermaid
flowchart LR
    RQ[Requester]
    DR[Department Representative]
    AC[Asset Custodian]
    AD[Administrator]
    MS[Maintenance Staff]
    FO[Finance Officer]
    SA[System Administrator]
    SO[Sustainability Officer]
    PO[Procurement Officer]
    SYS((Circular Campus System))

    RQ -->|Asset requests, defect reports, receipt confirmation| SYS
    SYS -->|Matches, request status, notifications| RQ

    DR -->|Release approval, handover arrangements| SYS
    SYS -->|Approval tasks, transfer updates| DR

    AC -->|Asset records, handover information, defect reports| SYS
    SYS -->|Assigned transfers, asset status| AC

    AD -->|Final approval or rejection decisions| SYS
    SYS -->|Approval queue, exceptions, reports| AD

    MS -->|Inspection and repair information| SYS
    SYS -->|Tickets and assignments| MS

    FO -->|Disposal approval or rejection| SYS
    SYS -->|Disposal approval requests| FO

    SA -->|Account and role changes| SYS
    SYS -->|User and access records| SA

    SO -->|Sustainability report requests| SYS
    SYS -->|Reuse and sustainability indicators| SO

    PO -->|Procurement and reuse enquiries| SYS
    SYS -->|Existing asset and reuse information| PO
```

The context diagram focuses on the system boundary and its external interactions. Internal components such as controllers, services, databases, and the notification module are not shown.

## 3. Sequence Diagrams

The following sequence diagrams describe how the main components of the system interact to complete each use case.

### 3.1 UC-11 — Approve or Reject Transfer

The Administrator reviews a pending transfer request and chooses to approve or reject it. Approval requires the owning department's release permission and a valid asset status.

```mermaid
sequenceDiagram
    autonumber
    actor AD as Administrator
    participant UI as Approval Page
    participant C as Approval Controller
    participant S as Approval Service
    participant DB as Database
    participant N as Notification Module

    AD->>UI: Open pending transfer requests
    UI->>C: Get pending requests
    C->>S: Validate AD session and permissions

    alt Access denied
        S-->>C: Permission error
        C-->>UI: Access denied
        UI-->>AD: Display error
    else Authorised
        S->>DB: Read pending approvals
        DB-->>S: Request list
        S-->>C: Pending requests
        C-->>UI: Display request list

        AD->>UI: Select request and submit decision
        UI->>C: Send decision and optional reason
        C->>S: Validate request and decision
        S->>DB: Read current request, approvals, asset
        DB-->>S: Current records

        alt Request is not pending or user is not allowed
            S-->>C: Decision blocked
            C-->>UI: Explain restriction

        else Rejection selected
            alt Reason shorter than 10 characters
                S-->>C: Invalid reason
                C-->>UI: Ask for valid reason
            else Valid reason
                S->>DB: Save rejection, reason and audit record
                DB-->>S: Rejection saved
                S->>N: Create rejection notifications
                S-->>C: Transfer rejected
                C-->>UI: Display confirmation
            end

        else Approval selected
            S->>DB: Check DR release and conflicting asset states
            DB-->>S: Validation outcome

            alt Release approval missing or asset unavailable
                S-->>C: Approval blocked
                C-->>UI: Display reason
            else All conditions satisfied
                S->>DB: Save AD approval and mark transfer Approved
                S->>DB: Save approver, time and audit entry
                DB-->>S: Transaction saved
                S->>N: Create approval notifications
                S-->>C: Transfer approved for scheduling
                C-->>UI: Display confirmation
            end
        end
    end
```

A pending approval older than 48 hours is flagged as overdue, and the Administrator receives a notification according to FR-APR-06.

### 3.2 UC-12 — Confirm Receipt

The receiving Requester confirms that the asset has arrived. The system updates ownership and location only after successful confirmation.

```mermaid
sequenceDiagram
    autonumber
    actor RQ as Receiving Requester
    participant UI as Transfer Page
    participant C as Transfer Controller
    participant S as Transfer Service
    participant A as Asset Service
    participant DB as Database
    participant N as Notification Module

    RQ->>UI: Open transfer and confirm receipt or report issue
    UI->>C: Submit receipt outcome and optional evidence
    C->>S: Check user role and receiving department
    S->>DB: Read transfer and its current state
    DB-->>S: Transfer details

    alt Wrong user or transfer not In Transit
        S-->>C: Action blocked
        C-->>UI: Show restriction

    else Damaged or incorrect asset reported
        S->>DB: Record discrepancy and remain In Transit
        S->>N: Notify responsible staff and AD
        S-->>C: Discrepancy recorded
        C-->>UI: Show unresolved status

    else Correct receipt confirmed
        S->>DB: Record receipt and set Received
        S->>A: Finalise custody and location change
        A->>DB: Save new and previous custodian and location
        DB-->>A: Asset updated
        A-->>S: Update complete
        S->>DB: Set transfer Completed and request Fulfilled
        S->>DB: Add asset history and audit records
        S->>N: Notify previous custodian and requester
        S-->>C: Receipt completed
        C-->>UI: Show confirmation
    end
```

### 3.3 UC-13 — Report Defect

An Asset Custodian or Requester reports a problem with an existing asset. The system creates a maintenance ticket and notifies the maintenance team.

```mermaid
sequenceDiagram
    autonumber
    actor U as Custodian or Requester
    participant UI as Asset Page
    participant C as Maintenance Controller
    participant S as Maintenance Service
    participant DB as Database
    participant N as Notification Module

    U->>UI: Open asset and report defect
    UI-->>U: Display defect form
    U->>UI: Enter description, condition and optional photo
    UI->>C: Submit defect report
    C->>S: Validate user and defect information
    S->>DB: Check asset exists
    DB-->>S: Asset record or not found

    alt Invalid asset or incomplete information
        S-->>C: Validation error
        C-->>UI: Display error

    else Valid report
        S->>DB: Create ticket with status Reported
        S->>DB: Mark asset unavailable for new reservations or transfers
        S->>DB: Save defect history and audit event
        S->>N: Notify maintenance team
        S-->>C: Ticket ID
        C-->>UI: Show ticket confirmation
    end
```

### 3.4 UC-24 — Schedule Inspection

Maintenance Staff schedules an inspection for an existing defect ticket. The system checks the ticket and asset status before saving the schedule.

```mermaid
sequenceDiagram
    autonumber
    actor MS as Maintenance Staff
    participant UI as Maintenance Page
    participant C as Maintenance Controller
    participant S as Maintenance Service
    participant DB as Database
    participant N as Notification Module

    MS->>UI: Open reported ticket and choose inspection time
    UI->>C: Submit assigned staff, date and time
    C->>S: Validate assignment and ticket
    S->>DB: Read ticket, asset and existing schedule
    DB-->>S: Current records

    alt Invalid ticket, staff, date or conflicting transfer
        S-->>C: Scheduling blocked
        C-->>UI: Display correction needed

    else Details valid
        S->>DB: Save inspection schedule and assignee
        S->>DB: Record scheduling audit event
        S->>N: Notify assigned staff and custodian
        S-->>C: Inspection scheduled
        C-->>UI: Display confirmation
    end
```

### 3.5 UC-14 — Record Repair

The assigned Maintenance Staff records the repair details, including the work performed, cost, and repair result.

```mermaid
sequenceDiagram
    autonumber
    actor MS as Assigned Maintenance Staff
    participant UI as Maintenance Page
    participant C as Maintenance Controller
    participant S as Maintenance Service
    participant DB as Database
    participant N as Notification Module

    MS->>UI: Open ticket and submit repair details
    UI->>C: Send work, parts, cost and result
    C->>S: Validate staff and repair details
    S->>DB: Read ticket, assignee and approval state
    DB-->>S: Current ticket

    alt Not assigned or repair not authorised
        S-->>C: Permission or approval error
        C-->>UI: Display restriction

    else Negative cost or incomplete details
        S-->>C: Invalid repair information
        C-->>UI: Request correction

    else Valid repair
        S->>DB: Save repair action and non-negative AED cost

        alt Repair work completed
            S->>DB: Set ticket Completed and await verification
        else Not repairable
            S->>DB: Set ticket Not Repairable with reason
        else Further work needed
            S->>DB: Keep ticket In Repair
        end

        S->>DB: Record repair history and audit entry
        S->>N: Notify custodian and relevant staff
        S-->>C: Repair record saved
        C-->>UI: Display updated ticket
    end
```

A completed repair must be verified by another authorised Maintenance Staff member or Asset Custodian before the asset becomes available again.

### 3.6 UC-15 — View Asset History

An authorised user opens an asset's history to review previous activities, including transfers, inspections, and repairs.

```mermaid
sequenceDiagram
    autonumber
    actor U as Authorised User
    participant UI as Asset Page
    participant C as History Controller
    participant S as History Service
    participant DB as Database

    U->>UI: Open asset history
    UI->>C: Request history for asset
    C->>S: Check role and access to asset

    alt Access denied
        S->>DB: Save denied-access audit event
        S-->>C: Access denied
        C-->>UI: Display restriction

    else Access granted
        S->>DB: Read ordered asset history records
        DB-->>S: Events with timestamps and references
        S-->>C: History timeline
        C-->>UI: Display dated events and linked records
    end
```

Asset history records are read-only. Corrections are stored as new entries referring to the original event.

### 3.7 UC-16 — Approve Disposal

The Administrator reviews a disposal request and its alternatives assessment. Both Administrator and Finance Officer approval are required before disposal can proceed.

```mermaid
sequenceDiagram
    autonumber
    actor AD as Administrator
    actor FO as Finance Officer
    participant UI as End-of-Life Page
    participant C as End-of-Life Controller
    participant S as End-of-Life Service
    participant DB as Database
    participant N as Notification Module

    AD->>UI: Review disposal request and alternatives
    UI->>C: Submit AD decision
    C->>S: Check AD permissions and request
    S->>DB: Read asset, request and alternatives assessment
    DB-->>S: Current records

    alt Invalid assessment or active repair or transfer
        S-->>C: Decision blocked
        C-->>UI: Display reason

    else AD rejects with valid reason
        S->>DB: Save rejection and audit record
        S->>N: Notify requester and custodian
        S-->>C: Rejected
        C-->>UI: Display outcome

    else AD approves
        S->>DB: Record AD approval and wait for FO decision
        S->>N: Notify Finance Officer

        FO->>UI: Review disposal and submit decision
        UI->>C: Submit FO decision and optional reason
        C->>S: Validate FO role, state and decision

        alt FO rejection reason missing or invalid
            S-->>C: Request valid reason
            C-->>UI: Display validation message

        else FO rejects
            S->>DB: Save FO rejection and audit record
            S->>N: Notify relevant users
            S-->>C: Disposal rejected
            C-->>UI: Display outcome

        else FO approves
            S->>DB: Save FO approval and audit record
            S->>N: Notify staff that disposal is authorised
            S-->>C: Approved for disposal
            C-->>UI: Display authorisation

            Note over S,DB: After confirmation that disposal occurred

            S->>DB: Record completion, destination and date
            S->>DB: Mark asset Disposed and remove listing
            S->>DB: Add asset history and audit entry
        end
    end
```

### 3.8 UC-25 — Approve Donation or Recycling

The Administrator reviews a donation or recycling request. Unlike disposal, these actions require Administrator approval without a separate Finance Officer decision.

```mermaid
sequenceDiagram
    autonumber
    actor AD as Administrator
    participant UI as End-of-Life Page
    participant C as End-of-Life Controller
    participant S as End-of-Life Service
    participant DB as Database
    participant N as Notification Module

    AD->>UI: Open donation or recycling request
    UI->>C: Submit AD approval or rejection
    C->>S: Validate AD role, reason and request state
    S->>DB: Read request and asset status
    DB-->>S: Current records

    alt Active repair, transfer, or invalid request
        S-->>C: Action blocked
        C-->>UI: Display reason

    else AD rejects
        alt Rejection reason shorter than 10 characters
            S-->>C: Invalid reason
            C-->>UI: Ask for valid reason
        else Valid reason
            S->>DB: Save rejection and audit entry
            S->>N: Notify relevant users
            S-->>C: Rejected
            C-->>UI: Display outcome
        end

    else AD approves
        S->>DB: Save approval and audit entry
        S->>N: Notify responsible staff
        S-->>C: Approved for action
        C-->>UI: Display authorisation

        Note over S,DB: After confirmation that action occurred

        S->>DB: Record date and destination or recipient
        S->>DB: Mark asset Donated or Recycled and remove listing
        S->>DB: Add asset history and audit entry
    end
```

## 4. Class Diagram

The class diagram represents the main entities and services responsible for approval workflows, asset transfers, maintenance, and end-of-life management.

```mermaid
classDiagram
    class Approval {
        +int approvalId
        +String actionType
        +int assetId
        +int requestId
        +int approverId
        +String decision
        +String reason
        +DateTime decidedAt
        +String status
        +boolean overdueFlag
        +approve(userId) void
        +reject(userId, reason) void
    }

    class Transfer {
        +int transferId
        +int assetId
        +int requestId
        +int fromDeptId
        +int toDeptId
        +Date handoverDate
        +String handoverLocation
        +String status
        +int receivedBy
        +DateTime receivedAt
        +String discrepancyNote
        +schedule(date, location) void
        +markInTransit() void
        +confirmReceipt(userId) void
        +reportDiscrepancy(note) void
    }

    class MaintenanceTicket {
        +int ticketId
        +int assetId
        +int reportedBy
        +int assignedTo
        +String description
        +DateTime inspectionAt
        +String status
        +scheduleInspection(staff, dateTime) void
        +approveRepair(adminId) void
        +verify(userId) void
        +markNotRepairable() void
    }

    class RepairRecord {
        +int repairId
        +int ticketId
        +int performedBy
        +String action
        +Decimal costAed
        +Date repairDate
        +String result
        +isCostValid() boolean
    }

    class EndOfLifeRequest {
        +int eolId
        +int assetId
        +String action
        +String reason
        +String alternativesAssessment
        +String recipient
        +String status
        +hasAssessment() boolean
        +needsFinanceApproval() boolean
        +completeAction() void
    }

    class AssetHistoryEvent {
        +int eventId
        +int assetId
        +String eventType
        +int actorId
        +DateTime eventTime
        +String relatedRecord
        +String details
    }

    class ApprovalService {
        +createApproval(action, assetId, requestId) Approval
        +getPending() List
        +decide(id, decision, reason, userId) Approval
        +markOverdueApprovals() void
    }

    class TransferService {
        +schedule(id, date, location) Transfer
        +confirmReceipt(id, result, note) Transfer
        +reportDiscrepancy(id, note) void
    }

    class MaintenanceService {
        +reportDefect(assetId, description, condition) MaintenanceTicket
        +scheduleInspection(ticketId, staff, dateTime) void
        +recordRepair(ticketId, details) RepairRecord
        +verifyRepair(ticketId, userId) void
    }

    class EndOfLifeService {
        +createRequest(assetId, action, reason) EndOfLifeRequest
        +adminDecision(id, decision, reason) void
        +financeDecision(id, decision, reason) void
        +completeAction(id, details) void
    }

    class HistoryService {
        +record(assetId, type, actorId, reference) AssetHistoryEvent
        +getHistory(assetId) List
    }

    class ApprovalController {
        +getPending() Response
        +postDecision() Response
    }

    class TransferController {
        +postReceipt() Response
    }

    class MaintenanceController {
        +postTicket() Response
        +postInspection() Response
        +postRepair() Response
    }

    class EndOfLifeController {
        +postAdminDecision() Response
        +postFinanceDecision() Response
    }

    class HistoryController {
        +getHistory() Response
    }

    MaintenanceTicket "1" --> "0..*" RepairRecord : includes
    Transfer "1" --> "1..*" Approval : requires

    ApprovalController ..> ApprovalService
    TransferController ..> TransferService
    MaintenanceController ..> MaintenanceService
    EndOfLifeController ..> EndOfLifeService
    HistoryController ..> HistoryService

    ApprovalService ..> Approval
    ApprovalService ..> TransferService
    TransferService ..> Transfer
    TransferService ..> HistoryService

    MaintenanceService ..> MaintenanceTicket
    MaintenanceService ..> RepairRecord

    EndOfLifeService ..> EndOfLifeRequest
    EndOfLifeService ..> ApprovalService
    HistoryService ..> AssetHistoryEvent
```

### 4.1 Class Responsibilities

| Class | Main Responsibility | Related Requirements |
|---|---|---|
| ApprovalService | Handles final decisions, release checks, overdue approvals and approval records | FR-APR-01–07 |
| TransferService | Manages scheduling, receipt confirmation, discrepancies and transfer completion | FR-TRF-01–05 |
| MaintenanceService | Manages defect tickets, inspections, repair records and verification | FR-MNT-01–05 |
| EndOfLifeService | Handles donation, recycling and disposal approval and completion | FR-DSP-01–05 |
| HistoryService | Records and retrieves asset history without modifying previous events | FR-HST-01–03 |

## 5. User Interface Mockups

The following interface mockups show the main pages used for approvals, transfers, maintenance, and asset history.

### 5.1 Approval Queue (UC-11, UC-16, UC-25)

```text
+------------------------------------------------------------------+
| Approvals                                        Administrator    |
| Filter: [Pending v]      Type: [All v]                            |
+------------------------------------------------------------------+
| ID      Type        Asset              From -> To       Waiting   |
| A-101   Transfer    Lab bench stool    CS -> Business   6 h       |
| A-099   Disposal    Old projector      Engineering      52 h      |
| A-097   Recycling   Old monitors       IT               20 h      |
|                                        [Open selected]            |
+------------------------------------------------------------------+
| Selected: A-101    Request: R-0042                                |
| Owner department release approval: APPROVED                      |
| Asset condition: Good      Active conflict: None                 |
| Rejection reason (minimum 10 characters): [_________________]    |
|                                  [Reject]  [Approve]             |
+------------------------------------------------------------------+
```

The Administrator can view pending requests, review approval details, and submit a final decision.

### 5.2 Receipt Confirmation (UC-12)

```text
+------------------------------------------------------------------+
| Transfer T-0031                        Status: In Transit         |
| Asset: Lab bench stool x20                                       |
| From: Computer Science          To: Business School             |
| Handover: 2026-11-04           Location: Library                 |
+------------------------------------------------------------------+
| Receiving Requester: [signed-in user]                            |
| Condition: ( ) As expected   ( ) Damaged or incorrect            |
| Discrepancy note: [__________________________________________]   |
| Optional photo: [Choose file]                                    |
|                     [Report problem]  [Confirm receipt]          |
+------------------------------------------------------------------+
```

The receiving Requester confirms receipt or reports a discrepancy. A damaged or incorrect asset does not automatically complete the transfer.

### 5.3 Defect Report (UC-13)

```text
+------------------------------------------------------------------+
| Report a defect                                                  |
| Asset ID *        [A-2045]  Projector                            |
| Description *     [__________________________________________]   |
| Reported condition: ( ) Good ( ) Fair ( ) Needs Repair           |
| Photo (optional): [Choose file]                                  |
| Date: Automatically recorded                                     |
|                                        [Cancel]  [Submit report]  |
+------------------------------------------------------------------+
```

The user enters the asset information and describes the problem. The system creates a maintenance ticket when the information is valid.

### 5.4 Inspection and Repair (UC-24, UC-14)

```text
+------------------------------------------------------------------+
| Maintenance ticket M-0210        Status: Repair Approved         |
| Asset: A-2045 Projector                                         |
| Inspection: [2026-11-05 10:00]  Assigned staff: [MS-02]          |
|                                             [Schedule inspection]|
+------------------------------------------------------------------+
| Repair history                                                   |
| Date         Work performed                Cost (AED)             |
| 2026-11-06   Lamp unit replaced            180.00                 |
+------------------------------------------------------------------+
| New repair record                                                |
| Work done *: [_______________________________________________]   |
| Cost (AED) *: [0.00]                                             |
| Result: ( ) Completed ( ) Further work ( ) Not repairable        |
|                                                   [Save repair]  |
+------------------------------------------------------------------+
| Verification: Different authorised staff member or custodian    |
| Verified condition: ( ) Good ( ) Fair ( ) Needs Repair           |
|                                                   [Verify]       |
+------------------------------------------------------------------+
```

Maintenance Staff can schedule inspections, record repair work and costs, and verify the repair result.

### 5.5 End-of-Life Decision (UC-16, UC-25)

```text
+------------------------------------------------------------------+
| End-of-life request E-0014                                      |
| Asset: Old projector             Action: Dispose                 |
| Reason: Cannot be repaired                                     |
| Alternatives assessed: Reuse / Transfer / Repair / Donation      |
|                        / Recycling                              |
+------------------------------------------------------------------+
| Administrator decision: Pending                                 |
| Finance Officer decision: Required for disposal                 |
| Reason for rejection (minimum 10 characters): [______________]  |
|                                        [Reject]  [Approve]        |
| Note: Final asset status changes only after action completion.  |
+------------------------------------------------------------------+
```

The Administrator reviews the request and the alternatives assessment. Disposal additionally requires Finance Officer approval.

### 5.6 Asset History (UC-15)

```text
+------------------------------------------------------------------+
| Asset history: A-2045 Projector                                 |
| Date        Event         Actor           Related record         |
| 2026-09-02  Registered    Custodian       -                      |
| 2026-09-10  Published     Custodian       L-0044                 |
| 2026-09-20  Transferred   Administrator   T-0031                 |
| 2026-10-21  Defect        Requester       M-0210                 |
| 2026-10-24  Repaired      Maint. staff    R-0090                 |
+------------------------------------------------------------------+
| Entries are read-only. Corrections create linked new entries.   |
+------------------------------------------------------------------+
```

The asset history displays previous activities in chronological order, including the date, event, responsible user, and related record.

## 6. Traceability

The following table connects the diagrams and interface mockups to their related use cases and functional requirements.

| Diagram / Mockup | Use Case | Related Requirements |
|---|---|---|
| Sequence 3.1, UI 5.1 | UC-11 Approve or Reject Transfer | FR-APR-01, 02, 03, 05, 06, 07; FR-TRF-01 |
| Sequence 3.2, UI 5.2 | UC-12 Confirm Receipt | FR-TRF-03, 04, 05; FR-HST-01 |
| Sequence 3.3, UI 5.3 | UC-13 Report Defect | FR-MNT-01; FR-HST-01 |
| Sequence 3.4, UI 5.4 | UC-24 Schedule Inspection | FR-MNT-02; FR-NTF-01 |
| Sequence 3.5, UI 5.4 | UC-14 Record Repair | FR-MNT-03, 04, 05; FR-HST-01 |
| Sequence 3.6, UI 5.6 | UC-15 View Asset History | FR-HST-01, 02, 03; FR-USR-06 |
| Sequence 3.7, UI 5.1/5.5 | UC-16 Approve Disposal | FR-DSP-01–05; FR-APR-03, 04, 05, 07 |
| Sequence 3.8, UI 5.1/5.5 | UC-25 Approve Donation or Recycling | FR-DSP-01, 03, 04, 05; FR-APR-03, 05, 07 |
| Context Diagram Section 2 | System Boundary and External Actors | FR-APR, FR-TRF, FR-MNT, FR-DSP, FR-USR |
| Class Diagram Section 4 | Workflow and Application Services | FR-APR, FR-TRF, FR-MNT, FR-HST, FR-DSP |

## 7. Design Consistency and Notes

### 7.1 Transfer Approval

The Department Representative must approve releasing the asset before the Administrator gives final transfer approval. A rejected request cannot proceed to scheduling or handover.

### 7.2 Transfer Completion

Administrator approval changes the transfer status to Approved, but does not immediately change ownership, custody, or location.

These details are updated only after the receiving Requester confirms receipt.

### 7.3 Maintenance Verification

A repair marked Completed must still be verified by an authorised staff member or Asset Custodian before the asset can return to service.

### 7.4 Disposal Approval

Disposal requires both Administrator and Finance Officer approval under the Phase 3 requirements. Donation and recycling require Administrator approval.

An approved end-of-life request does not immediately mark an asset as Donated, Recycled, or Disposed. The status changes only after the authorised action is confirmed complete.

### 7.5 Notifications and Audit Records

The system records important approval decisions, transfer updates, maintenance activities, and end-of-life actions.

Relevant users receive notifications when a workflow changes. Audit records contain the responsible actor, action, timestamp, and outcome.

### 7.6 Shared Design Documents

The context diagram provides a high-level representation of external system interactions.

The sequence diagrams describe the order of interactions between components, while the class diagram represents the main entities and services.

The shared architecture and entity-relationship diagram are maintained separately in `00_architecture_and_shared_design.md`.

This separation keeps the individual design document focused on approvals, transfers, maintenance, and end-of-life management.
