# 4. Functional Requirements – Assets, Marketplace, Requests and Search

This section defines the functional requirements for asset registration,
marketplace publication, resource requests, search and filtering, and
reservation management.

Each functional requirement uses the word "shall" and is written so that
it can be tested during later development and testing phases.


# 4.1 Asset Registration and Inventory

**Priority:** Essential

## 4.1.1 Description

The Asset Registration and Inventory feature allows authorized users to
create and maintain asset records. Each asset record stores the information
required to identify, locate, value and manage an asset throughout its
life cycle.

## 4.1.2 Stimulus and Response

| Stimulus | System Response |
|---|---|
| Authorized user selects Register Asset | System displays the asset registration form |
| User submits valid asset information | System creates the record and assigns a unique asset ID |
| User submits invalid information | System rejects the submission and identifies the invalid fields |
| Authorized user edits an asset | System validates and saves the changes |
| Authorized user deactivates an asset | System marks the asset as inactive |
