# Phase 3 – Requirements Document
## 4.6–4.14 Workflow and Administration Features

**Project:** Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System

**Group:** 5  
**Contributor:** Mubarak

This section explains the requirements for approvals, transfers, maintenance, asset history, disposal, user management, notifications, reports, and audit logging.

The requirements are written using "shall" to make them specific and testable.

**Actor codes:**
- AD = Administrator
- DR = Department Representative
- AC = Asset Custodian
- RQ = Requester
- MS = Maintenance Staff
- FO = Finance Officer
- SA = System Administrator
- SO = Sustainability Officer
- PO = Procurement Officer

---

## 4.6 Approval Workflows (FR-APR)

**Description:**  
The system manages approval requests for reservations, transfers, donations, recycling, and disposal. Every decision must be made by an authorised user and recorded.

**Priority:** Essential

**Stimulus and Response:**  
A user submits a request requiring approval. The system sends it to the correct approver. The approver accepts or rejects the request, and the system updates its status.

### Functional Requirements

**FR-APR-01:** The system shall create an approval record with a unique approval ID, action type, asset ID, requester ID, and status whenever an approval-required action is submitted.

**FR-APR-02:** The system shall require approval from the owning department's Department Representative before the Administrator approves an asset transfer.

**FR-APR-03:** The system shall allow only the Administrator to give final approval or rejection for reservations, transfers, donations, and recycling requests.

**FR-APR-04:** The system shall require approval from both the Administrator and Finance Officer before a disposal request is completed.

**FR-APR-05:** The system shall require a rejection reason containing at least 10 characters whenever an approval request is rejected.

**FR-APR-06:** The system shall mark an approval request as overdue and notify the Administrator if it remains pending for more than 48 hours.

**FR-APR-07:** The system shall record the approver ID, decision, timestamp, and rejection reason when applicable.

**Error Handling:**
- Unauthorised users cannot approve requests.
- Requests cannot skip required approval stages.
- Rejected requests cannot continue to transfer.
- Completed approval decisions cannot be submitted again.

- ---

## 4.7 Transfer Management (FR-TRF)

**Description:**  
The system tracks approved asset transfers between departments, including collection arrangements, receipt confirmation, and custody changes.

**Priority:** Essential

**Stimulus and Response:**  
After approval, the responsible user arranges the transfer. The receiving user confirms receipt, and the system updates the asset's custodian and location.

### Functional Requirements

**FR-TRF-01:** The system shall prevent an active transfer from being created unless the required release and transfer approvals are completed.

**FR-TRF-02:** The system shall allow the responsible Department Representative or Asset Custodian to record the collection or delivery date, handover location, and receiving department.

**FR-TRF-03:** The system shall mark an asset as unavailable when its transfer status becomes In Transit to prevent another reservation.

**FR-TRF-04:** The system shall allow the receiving Requester to confirm receipt or report a discrepancy using the transfer ID.

**FR-TRF-05:** The system shall update the asset's custodian and location only after receipt confirmation and shall preserve the previous custodian, location, timestamp, and supporting documents.

**Error Handling:**
- Transfers without approval are blocked.
- Only the assigned receiving department can confirm receipt.
- Damaged or incorrect deliveries remain unresolved until reviewed.
- Transfers already in transit cannot be cancelled through the normal cancellation process

---

## 4.8 Inspection, Maintenance and Repair (FR-MNT)

**Description:**  
The system allows users to report damaged assets, request inspections, record repairs, and update asset conditions.

**Priority:** Essential

**Stimulus and Response:**  
A user reports a defect. Maintenance staff inspect the asset and record the findings. If a repair is approved, the repair work is completed and verified.

### Functional Requirements

**FR-MNT-01:** The system shall allow an Asset Custodian or Requester to submit a defect report containing the asset ID, description, date, and reported condition.

**FR-MNT-02:** The system shall allow Maintenance Staff to schedule an inspection by recording the assigned staff member, date, and time.

**FR-MNT-03:** The system shall require Administrator approval before a maintenance record can enter the In Repair state.

**FR-MNT-04:** The system shall allow the assigned Maintenance Staff member to record each repair action, including its date, description, and cost in AED.

**FR-MNT-05:** The system shall allow a different authorised Maintenance Staff member or Asset Custodian to verify a completed repair and update the asset condition to Good, Fair, or Needs Repair.

**Error Handling:**
- Invalid asset IDs are rejected.
- Negative repair costs are not accepted.
- Assets undergoing repair cannot be transferred or reserved.
- Repairs cannot be marked as verified without a completed repair record.
- Assets that cannot be repaired remain unavailable until an authorised decision is made.

---

## 4.9 Life-Cycle History (FR-HST)

**Description:**  
The system maintains a complete history of every asset from registration until its final outcome.

**Priority:** Essential

**Stimulus and Response:**  
Whenever an asset-related event occurs, the system adds it to the asset's history. Authorised users can view the recorded events in chronological order.

### Functional Requirements

**FR-HST-01:** The system shall record acquisition, allocation, use-status changes, inspections, maintenance, repairs, transfers, refurbishment, donations, recycling, retirement, and disposal events.

**FR-HST-02:** The system shall display an asset's history in chronological order, including the event type, date, responsible user, and related record.

**FR-HST-03:** The system shall prevent users from editing or deleting existing history records. Corrections shall be saved as new entries linked to the original event.

**Error Handling:**
- Users without permission cannot view restricted asset histories.
- Failed operations cannot appear as completed events.
- Existing history records cannot be overwritten.

---

## 4.10 Donation, Recycling and Disposal (FR-DSP)

**Description:**  
The system supports the responsible handling of assets that are no longer needed. Reuse, transfer, and repair should be considered before disposal.

**Priority:** Essential

**Stimulus and Response:**  
An authorised user submits an end-of-life request with a reason. The system checks the required information and sends the request for approval before recording the final action.

### Functional Requirements

**FR-DSP-01:** The system shall require an asset ID, requested action (Donate, Recycle, or Dispose), and a reason of at least 10 characters when creating an end-of-life request.

**FR-DSP-02:** The system shall require a recorded assessment of reuse, transfer, repair, donation, and recycling alternatives before accepting a disposal request for approval.

**FR-DSP-03:** The system shall require Administrator approval for donation or recycling and approval from both the Administrator and Finance Officer for disposal.

**FR-DSP-04:** The system shall record the completed action date, authorised user, destination or recipient, and supporting document reference when available.

**FR-DSP-05:** The system shall update the asset status to Donated, Recycled, or Disposed only after the approved action is confirmed complete and shall remove the asset from available marketplace results.

**Error Handling:**
- Disposal requests without an alternatives assessment are rejected.
- Assets undergoing transfer or repair cannot complete an end-of-life action.
- Rejected requests do not change the asset's current status.

---

## 4.11 User and Access Management (FR-USR)

**Description:**  
The system manages user accounts, authentication, roles, and permissions to ensure that only authorised users access protected functions.

**Priority:** Essential

**Stimulus and Response:**  
A user registers or an administrator creates an account. The user logs in, and the system checks the assigned role before granting access.

### Functional Requirements

**FR-USR-01:** The system shall allow the System Administrator to create user accounts containing a unique email address, name, department, assigned role, and account status.

**FR-USR-02:** The system shall allow users to self-register only as Requesters, with their accounts remaining inactive until activated by the System Administrator.

**FR-USR-03:** The system shall require users to authenticate using a registered email address and password before accessing protected features.

**FR-USR-04:** The system shall reject passwords shorter than 12 characters or longer than 128 characters.

**FR-USR-05:** The system shall allow only the System Administrator to change user roles or deactivate accounts, and shall record these actions in the audit log.

**FR-USR-06:** The system shall verify the user's active status, role, and department permissions before executing each protected action.

**Error Handling:**
- Duplicate email addresses are rejected.
- Incorrect login credentials produce a general error message.
- Inactive accounts cannot log in.
- Unauthorised actions are blocked.
- The final active System Administrator account cannot deactivate itself.

---

## 4.12 Notifications (FR-NTF)

**Description:**  
The system informs users about important workflow updates, including approvals, transfers, maintenance, and overdue requests.

**Priority:** Essential for in-app notifications; Desirable for email notifications.

**Stimulus and Response:**  
When an important event occurs, the system identifies the relevant users and generates a notification.

### Functional Requirements

**FR-NTF-01:** The system shall generate in-app notifications for new approval assignments, approval decisions, overdue approvals, transfer arrangements, receipt discrepancies, inspection assignments, and completed repairs.

**FR-NTF-02:** The system shall send notifications only to users involved in the corresponding workflow, including requesters, approvers, custodians, and assigned maintenance staff.

**FR-NTF-03:** The system shall support optional email notifications for users who enable email delivery in their account settings.

**FR-NTF-04:** The system shall record the notification ID, recipient ID, event type, creation timestamp, and Read or Unread status, and shall allow users to mark their own notifications as read.

**Error Handling:**
- Failed email delivery does not cancel a completed workflow.
- In-app notifications remain accessible even if email delivery fails.
- Users cannot access other users' private notifications.

---

## 4.13 Operational Reports (FR-RPT)

**Description:**  
The system provides reports that help authorised users monitor assets, requests, transfers, maintenance, and approval activities.

**Priority:** Essential for standard reports; Desirable for additional export formats.

**Stimulus and Response:**  
An authorised user selects a report and applies filters. The system displays matching records and allows the results to be exported.

### Functional Requirements

**FR-RPT-01:** The system shall provide reports covering available assets, open requests, completed transfers, maintenance history, ownership changes, approval decisions, and current asset statuses.

**FR-RPT-02:** The system shall allow users to filter reports by date range, department, asset category, and workflow status when those fields are applicable.

**FR-RPT-03:** The system shall allow authorised users to export filtered report results as CSV files containing the report name and generation timestamp.

**FR-RPT-04:** The system shall restrict financial information to the Finance Officer, Administrator, and other roles explicitly authorised through the permission matrix.

**Error Handling:**
- Invalid date ranges are rejected.
- Empty reports display "No results found."
- Users cannot bypass reporting permissions through filters or exports.

---

## 4.14 Audit Logging (FR-AUD)

**Description:**  
The system records important user and system activities to maintain accountability and support future reviews.

**Priority:** Essential

**Stimulus and Response:**  
When a user performs a protected action or attempts an unauthorised action, the system generates an audit record. Authorised users can review these records.

### Functional Requirements

**FR-AUD-01:** The system shall log successful asset updates, approval decisions, transfers, maintenance updates, end-of-life actions, role changes, account deactivations, report exports, and denied permission attempts.

**FR-AUD-02:** The system shall store an audit ID, actor ID, action, affected record ID, timestamp, outcome, and old and new values for modified fields.

**FR-AUD-03:** The system shall prevent all application users, including System Administrators, from editing or deleting existing audit records through the application.

**FR-AUD-04:** The system shall allow only System Administrators and Administrators to view and filter audit records by user, action, affected record, and date range.

**Error Handling:**
- Unauthorised audit log access is denied.
- Failed actions are recorded as failed rather than successful.
- Passwords and authentication secrets are excluded from audit records.

---

## 6.2 State Models

This section defines the allowed state transitions for asset transfers and maintenance workflows.

### 6.2.1 Transfer State Model

| Current State | Next State | Trigger / Actor | Condition |
|---|---|---|---|
| Requested | Pending Approval | System | Transfer request submitted |
| Pending Approval | Approved | AD | Required approvals completed |
| Pending Approval | Rejected | AD | Rejection reason recorded |
| Requested / Pending Approval | Cancelled | RQ | No final approval |
| Approved | Scheduled | DR / AC | Handover date and location recorded |
| Approved / Scheduled | In Transit | AC | Asset handed over |
| Approved / Scheduled | Cancelled | AD | Cancellation before handover |
| In Transit | Received | RQ | Receipt confirmed without discrepancy |
| Received | Completed | System | Custody and location updated |

**Transfer Rules:**
- Only one active transfer may exist for the same asset.
- Rejected, Cancelled, and Completed are final states.
- Discrepancies prevent transfer completion until resolved.
- Ownership and custody information cannot change before receipt confirmation.
- Transfers already in transit require a separately recorded return or reversal.

### 6.2.2 Maintenance State Model

| Current State | Next State | Trigger / Actor | Condition |
|---|---|---|---|
| Reported | Inspected | MS | Inspection completed |
| Inspected | Repair Approved | AD | Repair authorised |
| Inspected | Not Repairable | MS | Repair is not feasible |
| Repair Approved | In Repair | MS | Repair begins |
| In Repair | Completed | MS | Repair work completed |
| In Repair | Not Repairable | MS | Repair unsuccessful |
| Completed | Verified | MS / AC | Repair result confirmed |
| Completed | In Repair | MS | Failed verification recorded |

**Maintenance Rules:**
- Assets undergoing maintenance cannot be transferred or reserved.
- Maintenance records must remain available in asset history.
- Verified repairs close the current maintenance record.
- New defects require new defect reports.
- Assets marked Not Repairable cannot automatically be disposed of; the disposal approval process must still be followed.

### 6.2.3 Cross-Workflow Rules

| Situation | System Behaviour |
|---|---|
| Asset undergoing repair | Block transfer and reservation |
| Asset reserved or in active transfer | Block duplicate reservation or transfer |
| Transfer awaiting approval | Do not update custody or location |
| Receipt discrepancy reported | Keep transfer open |
| Disposal assessment missing | Block disposal approval request |
| AI suggests transfer or disposal | Require human approval |
| Asset donated, recycled, or disposed | Remove from available marketplace results |

---

## Coordination Notes

The approval responsibilities in this section must match the final permission matrix created by Mohammed Alketbi.

The reservation and transfer rules must be consistent with Mohammed Al Ali's requirements.

AI recommendations developed by Abdulla must never bypass human approval requirements.

The proposed 48-hour overdue threshold, 10-character minimum rejection reason, and approval responsibilities should be checked against the team's final business rules before submission.

All requirements in this section are intended for the project prototype and use synthetic data.
