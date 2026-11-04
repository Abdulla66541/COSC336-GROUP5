1. Sequence Diagrams
1.1 UC-11 Approve or Reject Transfer
sequenceDiagram
    autonumber
    actor AD as Administrator
    participant UI as Web Page
    participant ApprovalController
    participant Security
    participant ApprovalService
    participant TransferService
    participant DB as Database
    participant Audit as History and Audit
    participant Noti as Notification Module

    AD->>UI: Open approval queue
    UI->>ApprovalController: GET /approvals?status=pending
    ApprovalController->>Security: checkPermission(AD, "approve")
    Security-->>ApprovalController: allowed
    ApprovalController->>ApprovalService: getPending()
    ApprovalService->>DB: read pending approvals
    DB-->>ApprovalService: list
    ApprovalService-->>UI: approval list
    UI-->>AD: Show requests, assets and history
    AD->>UI: Select a request and click "Approve" or "Reject"
    UI->>ApprovalController: POST /approvals/{id}/decision
    activate ApprovalController
    ApprovalController->>ApprovalService: decide(approvalId, decision, reason, userId)
    activate ApprovalService
    ApprovalService->>DB: read approval, request and asset
    DB-->>ApprovalService: current states
    alt approver is also the requester (BR-07)
        ApprovalService-->>ApprovalController: blocked
        ApprovalController-->>UI: message
        UI-->>AD: Show "You cannot approve your own request"
    else request or asset state has changed
        ApprovalService-->>ApprovalController: refused with current state
        ApprovalController-->>UI: message
        UI-->>AD: Show current state
    else department representative release is missing (FR-APR-02)
        ApprovalService-->>ApprovalController: refused, release approval needed
        ApprovalController-->>UI: message
        UI-->>AD: Show "Waiting for department approval"
    else decision is "Approve"
        ApprovalService->>DB: save decision, set transfer "Approved", asset "In Transfer"
        ApprovalService->>TransferService: createTransfer(requestId, assetId)
        TransferService->>DB: save transfer record
        ApprovalService->>Audit: record approver, decision, time
        ApprovalService->>Noti: notify requester and custodian
    else decision is "Reject"
        ApprovalService->>ApprovalService: check reason has 10 characters or more
        ApprovalService->>DB: save rejection, release reservation, asset "Available / Published"
        ApprovalService->>Audit: record decision and reason
        ApprovalService->>Noti: notify requester
    end
    ApprovalService-->>ApprovalController: result
    deactivate ApprovalService
    ApprovalController-->>UI: result
    deactivate ApprovalController
    UI-->>AD: Show result
Overdue approvals (runs every hour)
sequenceDiagram
    autonumber
    participant Timer as Hourly Timer
    participant ApprovalService
    participant DB as Database
    participant Noti as Notification Module

    Timer->>ApprovalService: markOverdueApprovals()
    ApprovalService->>DB: find pending approvals older than 48 hours
    DB-->>ApprovalService: list
    loop for each approval in the list
        ApprovalService->>DB: set flag "overdue"
        ApprovalService->>Noti: notify Administrator
    end
1.2 UC-12 Confirm Receipt
sequenceDiagram
    autonumber
    actor U as DR or AC (receiving department)
    participant UI as Web Page
    participant TransferController
    participant Security
    participant TransferService
    participant AssetService
    participant DB as Database
    participant Audit as History and Audit
    participant Noti as Notification Module

    U->>UI: Open the approved transfer, click "Confirm receipt"
    UI->>TransferController: POST /transfers/{id}/receipt
    activate TransferController
    TransferController->>Security: checkPermission(user, "confirm receipt")
    Security-->>TransferController: allowed (receiving department)
    TransferController->>TransferService: confirmReceipt(transferId, note, photo)
    activate TransferService
    TransferService->>DB: read transfer
    DB-->>TransferService: transfer with status
    alt transfer was cancelled
        TransferService-->>TransferController: ended, show status
        TransferController-->>UI: message
        UI-->>U: Show "Transfer was cancelled"
    else user reports a damaged or wrong asset
        TransferService->>DB: save discrepancy note, keep transfer open
        TransferService->>Noti: notify Administrator
        TransferService-->>TransferController: problem recorded
        TransferController-->>UI: message
        UI-->>U: Show "Problem reported"
    else receipt is confirmed
        TransferService->>DB: set transfer "Received"
        TransferService->>AssetService: changeOwner(assetId, newDept, newCustodian, newLocation)
        AssetService->>DB: update owner, save previous owner and location
        DB-->>AssetService: saved
        AssetService-->>TransferService: done
        TransferService->>DB: set transfer "Completed" and request "Fulfilled"
        TransferService->>Audit: record history and audit entries
        TransferService->>Noti: notify previous owner
        TransferService-->>TransferController: completed
        deactivate TransferService
        TransferController-->>UI: success
        deactivate TransferController
        UI-->>U: Show "Ownership updated"
    end
If nobody confirms in 14 days, a daily timer sends a reminder and flags the transfer (BR-08, UC-12 alternative flow 3a).
1.3 UC-13 Report Defect
sequenceDiagram
    autonumber
    actor U as AC, DR, RQ, MS or AD
    participant UI as Web Page
    participant MaintenanceController
    participant MaintenanceService
    participant DB as Database
    participant Audit as History and Audit
    participant Noti as Notification Module

    U->>UI: Click "Report defect" on an asset
    UI-->>U: Show defect form
    U->>UI: Enter description, condition, optional photo
    UI->>MaintenanceController: POST /tickets
    activate MaintenanceController
    MaintenanceController->>MaintenanceService: reportDefect(assetId, description, condition)
    activate MaintenanceService
    MaintenanceService->>DB: check asset ID
    DB-->>MaintenanceService: asset or not found
    alt asset ID is not valid
        MaintenanceService-->>MaintenanceController: error
        MaintenanceController-->>UI: error
        UI-->>U: Show "Invalid asset"
    else asset is valid
        MaintenanceService->>DB: save ticket "Reported", set asset "In Maintenance"
        alt photo upload fails
            MaintenanceService-->>UI: report saved, photo can be added later
        end
        MaintenanceService->>Audit: record defect event
        MaintenanceService->>Noti: notify maintenance team
        MaintenanceService-->>MaintenanceController: ticket ID
        deactivate MaintenanceService
        MaintenanceController-->>UI: success
        deactivate MaintenanceController
        UI-->>U: Show ticket ID
    end
1.4 UC-24 Schedule Inspection
sequenceDiagram
    autonumber
    actor MS as Maintenance Staff
    participant UI as Web Page
    participant MaintenanceController
    participant MaintenanceService
    participant DB as Database
    participant Noti as Notification Module

    MS->>UI: Open ticket, click "Schedule inspection"
    UI-->>MS: Show last inspection date
    MS->>UI: Pick staff member, date and time
    UI->>MaintenanceController: POST /tickets/{id}/inspection
    MaintenanceController->>MaintenanceService: scheduleInspection(ticketId, staff, dateTime)
    MaintenanceService->>DB: read asset status
    DB-->>MaintenanceService: status
    alt asset is in transfer
        MaintenanceService-->>UI: warning, suggest new date
        UI-->>MS: Show warning
    else asset is free
        MaintenanceService->>DB: save inspection schedule
        MaintenanceService->>Noti: notify custodian and remind on the day
        MaintenanceService-->>UI: saved
        UI-->>MS: Show confirmation
    end
1.5 UC-14 Record Repair
sequenceDiagram
    autonumber
    actor MS as Maintenance Staff
    participant UI as Web Page
    participant MaintenanceController
    participant MaintenanceService
    participant DB as Database
    participant Audit as History and Audit
    participant Noti as Notification Module

    MS->>UI: Open ticket, click "Record repair"
    UI-->>MS: Show repair form
    MS->>UI: Enter work done, parts, cost in AED, result
    UI->>MaintenanceController: POST /tickets/{id}/repairs
    activate MaintenanceController
    MaintenanceController->>MaintenanceService: recordRepair(ticketId, details)
    activate MaintenanceService
    MaintenanceService->>DB: read ticket
    DB-->>MaintenanceService: ticket status and assignee
    alt ticket is assigned to someone else
        MaintenanceService-->>UI: blocked, show current assignee
    else ticket is not "Repair Approved" or "In Repair"
        MaintenanceService-->>UI: blocked, repair needs Administrator approval
    else cost is negative
        MaintenanceService-->>UI: highlight cost field
    else details are valid
        MaintenanceService->>DB: save repair record
        alt result is repaired
            MaintenanceService->>DB: set ticket "Completed", update asset condition
        else result is not repairable
            MaintenanceService->>DB: set ticket "Not Repairable"
            MaintenanceService->>Noti: notify Administrator (see UC-25 and UC-16)
        end
        MaintenanceService->>Audit: record repair event
        MaintenanceService->>Noti: notify custodian
        MaintenanceService-->>MaintenanceController: saved
        deactivate MaintenanceService
        MaintenanceController-->>UI: success
        deactivate MaintenanceController
        UI-->>MS: Show repair in history
    end
1.6 UC-16 Approve Disposal (and UC-25 Approve Donation or Recycling)
For donation or recycling the same flow is used, but only the Administrator decides and the Finance Officer step is skipped.
sequenceDiagram
    autonumber
    actor AD as Administrator
    actor FO as Finance Officer
    participant UI as Web Page
    participant EndOfLifeController
    participant EndOfLifeService
    participant ApprovalService
    participant DB as Database
    participant Audit as History and Audit
    participant Noti as Notification Module

    AD->>UI: Open disposal request
    UI->>EndOfLifeController: GET /end-of-life/{id}
    EndOfLifeController->>EndOfLifeService: getRequest(id)
    EndOfLifeService->>DB: read request, asset, assessment, repair history
    DB-->>EndOfLifeService: data
    EndOfLifeService-->>UI: request details
    UI-->>AD: Show asset, reason and alternatives assessment
    AD->>UI: Click "Approve"
    UI->>EndOfLifeController: POST /end-of-life/{id}/approve
    activate EndOfLifeController
    EndOfLifeController->>EndOfLifeService: approve(id, userId)
    activate EndOfLifeService
    alt alternatives assessment is missing (BR-10)
        EndOfLifeService-->>EndOfLifeController: blocked
        EndOfLifeController-->>UI: message
        UI-->>AD: Show "Assess alternatives first"
    else asset is in transfer or repair
        EndOfLifeService-->>EndOfLifeController: blocked
        EndOfLifeController-->>UI: message
        UI-->>AD: Show the reason
    else request can be approved
        EndOfLifeService->>ApprovalService: record Administrator approval
        alt value is above AED 5,000 (BR-09)
            EndOfLifeService->>Noti: ask Finance Officer
            Noti-->>FO: Notification
            FO->>UI: Open request and approve or reject
            UI->>EndOfLifeController: POST /end-of-life/{id}/finance-decision
            EndOfLifeController->>EndOfLifeService: financeDecision(id, decision)
            alt Finance Officer rejects
                EndOfLifeService->>DB: keep asset status unchanged
                EndOfLifeService->>Audit: record rejection
            else Finance Officer approves
                EndOfLifeService->>DB: set asset "Disposed", remove from marketplace
                EndOfLifeService->>Audit: record history and audit entries
            end
        else value is AED 5,000 or less
            EndOfLifeService->>DB: set asset "Disposed", remove from marketplace
            EndOfLifeService->>Audit: record history and audit entries
        end
        EndOfLifeService->>Noti: notify custodian and requester
        EndOfLifeService-->>EndOfLifeController: result
        deactivate EndOfLifeService
        EndOfLifeController-->>UI: result
        deactivate EndOfLifeController
        UI-->>AD: Show result
    end
1.7 UC-15 View Asset History
sequenceDiagram
    autonumber
    actor U as AC, DR, AD, FO, MS or SO
    participant UI as Web Page
    participant HistoryController
    participant Security
    participant HistoryService
    participant DB as Database
    participant Audit as History and Audit

    U->>UI: Open asset, click "History"
    UI->>HistoryController: GET /assets/{id}/history
    HistoryController->>Security: checkPermission(user, "view history", asset)
    alt user has no access to this asset
        Security-->>HistoryController: denied
        HistoryController->>Audit: record denied attempt (FR-AUD-01)
        HistoryController-->>UI: access denied
        UI-->>U: Show "No access"
    else user has access
        Security-->>HistoryController: allowed
        HistoryController->>HistoryService: getHistory(assetId)
        HistoryService->>DB: read events in time order
        DB-->>HistoryService: events
        HistoryService-->>HistoryController: events
        HistoryController-->>UI: events
        UI-->>U: Show timeline with event, date, user and record
    end
2. Class Diagram
classDiagram
    class Approval {
        +int approvalId
        +String actionType
        +int assetId
        +int requestId
        +int approverId
        +ApprovalDecision decision
        +String reason
        +DateTime decidedAt
        +ApprovalStatus status
        +isOverdue() boolean
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
        +TransferStatus status
        +int receivedBy
        +DateTime receivedAt
        +String discrepancyNote
        +schedule(date, place) void
        +markInTransit() void
        +confirmReceipt(userId) void
        +reportDiscrepancy(note) void
        +cancel() void
    }
    class MaintenanceTicket {
        +int ticketId
        +int assetId
        +int reportedBy
        +int assignedTo
        +String description
        +DateTime inspectionAt
        +TicketStatus status
        +scheduleInspection(staff, dateTime) void
        +approveRepair(adminId) void
        +complete() void
        +verify(userId) void
        +markNotRepairable() void
    }
    class RepairRecord {
        +int repairId
        +int performedBy
        +String action
        +Decimal costAed
        +Date repairDate
        +isCostValid() boolean
    }
    class EndOfLifeRequest {
        +int eolId
        +int assetId
        +EolAction action
        +String reason
        +String alternativesAssessment
        +String recipient
        +EolStatus status
        +hasAssessment() boolean
        +needsFinanceApproval() boolean
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
    class ApprovalStatus {
        <<enumeration>>
        Pending
        Approved
        Rejected
        Overdue
    }
    class TransferStatus {
        <<enumeration>>
        Requested
        PendingApproval
        Approved
        Rejected
        Cancelled
        Scheduled
        InTransit
        Received
        Completed
    }
    class TicketStatus {
        <<enumeration>>
        Reported
        Inspected
        RepairApproved
        InRepair
        Completed
        Verified
        NotRepairable
    }
    class EolAction {
        <<enumeration>>
        Donate
        Recycle
        Dispose
    }

    class ApprovalService {
        +createApproval(action, assetId, requestId) Approval
        +getPending() List
        +decide(id, decision, reason, userId) Approval
        +markOverdueApprovals() void
    }
    class TransferService {
        +createTransfer(requestId, assetId) Transfer
        +schedule(id, date, place) Transfer
        +confirmReceipt(id, note) Transfer
        +sendReminders() void
    }
    class MaintenanceService {
        +reportDefect(assetId, description, condition) MaintenanceTicket
        +scheduleInspection(ticketId, staff, dateTime) void
        +recordRepair(ticketId, details) RepairRecord
        +verifyRepair(ticketId, userId) void
    }
    class EndOfLifeService {
        +createRequest(assetId, action, reason) EndOfLifeRequest
        +approve(id, userId) void
        +financeDecision(id, decision) void
        +complete(id) void
    }
    class HistoryService {
        +record(assetId, eventType, actorId, ref) AssetHistoryEvent
        +getHistory(assetId) List
    }
    class ApprovalController {
        +getPending() Response
        +postDecision() Response
    }
    class TransferController {
        +postSchedule() Response
        +postReceipt() Response
    }
    class MaintenanceController {
        +postTicket() Response
        +postInspection() Response
        +postRepair() Response
    }
    class EndOfLifeController {
        +getRequest() Response
        +postApprove() Response
        +postFinanceDecision() Response
    }
    class HistoryController {
        +getHistory() Response
    }

    MaintenanceTicket "1" --> "0..*" RepairRecord : contains
    Approval --> ApprovalStatus
    Transfer --> TransferStatus
    MaintenanceTicket --> TicketStatus
    EndOfLifeRequest --> EolAction

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


Class
Role
Rule it enforces
ApprovalService
Creates and decides approvals, finds overdue ones
FR-APR-01 to 07, BR-06, BR-07
TransferService
Creates, schedules and completes transfers
FR-TRF-01 to 05, BR-08, Phase 3 state model 6.2.3
MaintenanceService
Tickets, inspections, repairs, verification
FR-MNT-01 to 05, Phase 3 state model 6.2.4
EndOfLifeService
Donation, recycling and disposal requests
FR-DSP-01 to 05, BR-09, BR-10
HistoryService
Writes and reads the asset history, never edits
FR-HST-01 to 03, BR-13
3. User Interface Mockups
3.1 Approval Queue (UC-11, UC-16, UC-25)
+----------------------------------------------------------------------+
|  Approvals                                          (Administrator)  |
|  Show: [ Pending v ]    Type: [ All v ]                              |
| Class diagram |
|  ID     Type       Asset            From -> To        Waiting        |
|  A-101  Transfer   Lab bench stool  CS -> Business    6 h            |
|  A-099  Disposal   Old projector    Eng.              OVERDUE 52 h   |
|  A-097  Recycling  Monitors x8      IT                20 h           |
| Class diagram |
|  [Open selected]                                                     |
+----------------------------------------------------------------------+
|  Details of A-101                                                    |
|  Request R-0042 by ........  Asset history [View]                   |
|  Department approval: DONE (Computer Science)                        |
| Class diagram |
|  Rejection reason (10+ characters): [____________________________]   |
|                              [ Reject ]            [ Approve ]       |
+----------------------------------------------------------------------+
3.2 Transfer and Confirm Receipt (UC-12)
+----------------------------------------------------------------------+
|  Transfer T-0031                      Status: In Transit             |
|  Asset: Lab bench stool x20          From: Computer Science          |
|  To: Business School                 Handover: 2026-11-04, Library   |
| Class diagram |
|  Check the asset:                                                    |
|  Condition on arrival: ( ) As described   ( ) Damaged or wrong       |
|  Note: [______________________________________________]             |
|  Photo: [Choose file]                                                |
| Class diagram |
|  [ Report problem ]                    [ Confirm receipt ]           |
| Class diagram |
|  Reminder: confirm within 14 days of handover.                       |
+----------------------------------------------------------------------+
3.3 Report Defect (UC-13)
+----------------------------------------------------------------------+
|  Report a defect                                                     |
|  Asset ID *         [ A-2045 ]  (Projector, Room 3.12)               |
|  Description *      [______________________________________]         |
|  Reported condition ( ) Good  ( ) Fair  ( ) Needs repair             |
|  Photo              [Choose file]                                    |
|  Date               2026-10-21 (automatic)                           |
| Class diagram |
|  [ Cancel ]                                [ Send report ]           |
+----------------------------------------------------------------------+
3.4 Maintenance Ticket (UC-14, UC-24)
+----------------------------------------------------------------------+
|  Ticket M-0210       Asset A-2045        Status: Repair Approved     |
|  Inspection: 2026-10-23 10:00  by M. Staff       [Change date]       |
| Class diagram |
|  Repair records                                                      |
|  Date        Work done              Cost (AED)                       |
|  2026-10-24  Replaced lamp          180.00                           |
| Class diagram |
|  New record:                                                         |
|  Work done *   [__________________]  Cost (AED) * [ 0.00 ]           |
|  Result        ( ) Repaired  ( ) Partly  ( ) Not repairable          |
|                                          [ Save repair ]             |
|  Verification (another staff member or the custodian):               |
|  Condition ( ) Good  ( ) Fair  ( ) Needs repair   [ Verify ]         |
+----------------------------------------------------------------------+
3.5 End of Life Request (UC-16, UC-25)
+----------------------------------------------------------------------+
|  End of life request E-0014                                          |
|  Asset: Old projector   Value: AED 6,200   Requested action: Dispose |
|  Reason: [ Cannot be repaired, lamp unit damaged ]                   |
| Class diagram |
|  Alternatives assessed (all required for disposal)                   |
|  [x] Reuse   [x] Transfer   [x] Repair   [x] Donation   [x] Recycling|
| Class diagram |
|  Approvals                                                           |
|  Administrator:      Approved  2026-10-21                            |
|  Finance Officer:    Waiting   (value above AED 5,000)               |
| Class diagram |
|  [ Reject ]                                    [ Approve ]           |
+----------------------------------------------------------------------+
3.6 Asset History (UC-15)
+----------------------------------------------------------------------+
|  History of A-2045 Projector                                         |
| Class diagram |
|  Date        Event          By             Related record            |
|  2026-09-02  Registered     K. Custodian   -                         |
|  2026-09-10  Published      K. Custodian   L-0044                    |
|  2026-09-20  Transferred    Administrator  T-0031                    |
|  2026-10-21  Defect         M. Student     M-0210                    |
|  2026-10-24  Repaired       M. Staff       R-0090                    |
| Class diagram |
|  History cannot be edited. Corrections are added as new entries.     |
+----------------------------------------------------------------------+
4. Traceability


Diagram
Use case
Requirements
Sequence 1.1
UC-11 Approve or reject transfer
FR-APR-01 to 07, FR-TRF-01, BR-06, BR-07
Sequence 1.2
UC-12 Confirm receipt
FR-TRF-02 to 05, BR-08
Sequence 1.3
UC-13 Report defect
FR-MNT-01
Sequence 1.5
UC-14 Record repair
FR-MNT-03 to 05
Sequence 1.7
UC-15 View asset history
FR-HST-01 to 03
Sequence 1.6
UC-16 Approve disposal
FR-DSP-01 to 05, FR-APR-04, BR-09, BR-10
Sequence 1.4
UC-24 Schedule inspection
FR-MNT-02
Sequence 1.6
UC-25 Approve donation or recycling
FR-DSP-03 to 05, FR-APR-03
