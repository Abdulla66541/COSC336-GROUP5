# Phase 4 & 5 – Part 4: AI Layer and Sustainability

**Owner:** Abdulla

**Use cases:** UC-26 to UC-35

**Requirement groups:** FR-AI-01 to FR-AI-70, FR-AI-X-01 to FR-AI-X-17, FR-SUS-01 to FR-SUS-31

**Data stores:** D10 AI Output Log, D11 Sustainability Records

**Tables:** AI_OUTPUT, AI_OVERRIDE, AI_FEEDBACK, REUSE_EVENT, EMISSION_FACTOR

**Common AI Integration Path:**

Service → AI Facade → Privacy Filter → AI Adapter → AI Service → Answer Checker → AI Output Log

All AI use cases use the common AI integration path unless a fallback or alternative flow is triggered.

# 1. Data Flow Diagrams, Level 1

## 1.1 Process 6.0 – Run AI Functions

**Diagram file:**

**Purpose:** Process 6.0 decomposes the AI layer into the eight AI-related processes used by the system.

### Processes

| Process | Description | Requirements |
|---|---|---|
| 6.1 Classify Asset | Suggests category, subcategory, tags, material type, and missing metadata for a newly registered or edited asset. | FR-AI-01 to FR-AI-15 |
| 6.2 Match and Rank Assets | Compares requests with active listings, generates compatibility scores, and ranks the most suitable matches. | FR-AI-16 to FR-AI-35 |
| 6.3 Recommend Sustainable Action | Recommends retain, transfer, repair, refurbish, donate, disassemble, or recycle, with disposal treated as a last option. | FR-AI-36 to FR-AI-49 |
| 6.4 Answer Question | Answers user questions using permitted system information and does not approve or modify controlled actions. | FR-AI-50 to FR-AI-59 |
| 6.5 Draft AI Report | Produces a draft report summary for human review. | FR-AI-60 to FR-AI-70 |
| 6.6 Detect Duplicate Listings | Compares new listings with existing listings and warns about possible duplicates. | UC-33 |
| 6.7 Predict Maintenance Need | Identifies assets with higher maintenance risk and provides supporting reasons. | UC-34 |
| 6.8 Record Override and Feedback | Records AI overrides, reasons, and user feedback. | FR-AI-X-03, FR-AI-X-04 |

### Data Stores Used

- **D2 Assets**
- **D4 Listings**
- **D5 Requests and Reservations**
- **D8 Maintenance Records**
- **D10 AI Output Log**
- **D11 Sustainability Records**
- **D12 Reports**

### Main Data Flows

The Level 1 DFD shows the following flows:

- Asset data is sent to 6.1 for AI classification.
- Requests and active listings are sent to 6.2 for semantic matching and ranking.
- Asset condition, asset history, and repair history are sent to 6.3 for sustainability recommendations.
- Permitted asset and request data is used by 6.4 to answer questions.
- Sustainability figures, request summaries, and maintenance trends are used by 6.5 to generate AI reports.
- New listings and existing listings are used by 6.6 for duplicate detection.
- Asset age, condition, and maintenance history are used by 6.7 for maintenance prediction.
- Overrides and feedback are handled by 6.8 and recorded in the AI output log.

AI requests are sent without unnecessary personal data. AI results are returned with confidence information where available and are recorded in D10 AI Output Log.

## 1.2 Process 7.0 – Calculate Sustainability Figures

**Diagram file:** 

Process 7.0 manages the calculation and display of sustainability indicators.

### Processes

| Process | Description | Requirements |
|---|---|---|
| 7.1 Record Reuse Event | Records a reuse or avoided-purchase event after a completed transfer. | FR-SUS-05, FR-SUS-09 |
| 7.2 Calculate Sustainability Figures | Calculates waste diversion, avoided purchases, life extension, reuse rate, repair rate, financial savings, and estimated CO2 reduction. | FR-SUS-01 to FR-SUS-31 |
| 7.3 Show Dashboard | Displays sustainability figures by reporting period or department. | FR-SUS-27 to FR-SUS-31 |

### Sustainability Data Flows

- Completed transfer events are passed to 7.1.
- Fulfilled requests can also create reuse events.
- Reuse events are stored in D11 Sustainability Records.
- D2 Assets provides asset values and categories.
- D8 Maintenance Records provides repair information.
- 7.2 calculates the sustainability indicators and stores the results in D11.
- 7.3 retrieves the calculated results and displays them to authorised users.

### Sustainability Formulas

**Reuse rate (%)**

`(Number of Assets Reused or Transferred / Number of Assets Considered for Reuse) × 100`

**Repair rate (%)**

`(Number of Assets Repaired / Number of Assets Requiring a Disposition Decision) × 100`

**Estimated carbon reduction**

`Activity Quantity × Applicable Emission Factor`

The emission factor and its source shall be shown when a carbon-reduction estimate is produced.

# 2. Sequence Diagrams

The detailed sequence diagrams are maintained as separate diagrams.net/draw.io diagrams.

## 2.1 UC-26 – Classify Asset

**Diagram file:** 

**Primary actor:** Asset Custodian

**Secondary actor:** AI Service

**Purpose:** Obtain an AI-generated asset classification and allow the user to review and approve or change the result.

**Main interactions:**

1. The Asset Custodian selects “Suggest category”.
2. The system requests classification.
3. The classification service sends the request through the AI layer.
4. The AI Service returns a category, confidence score, and short reason.
5. A low-confidence result produces a warning.
6. If the AI does not respond within 15 seconds, manual classification is used.
7. The AI output is logged.
8. The suggestion is displayed to the Asset Custodian.
9. The user accepts or changes the classification.
10. The final value and any override are recorded.

## 2.2 UC-27 – Review AI Match

**Diagram file:** `images/UC-27.png`

**Primary actors:** Requester, Asset Custodian, Department Representative, Administrator, or Procurement Officer

**Secondary actor:** AI Service

**Purpose:** Identify and rank assets that best fit a resource request.

**Main interactions:**

1. The user opens a request and requests AI matches.
2. The system reads the request and active listings.
3. The AI layer compares the request with available listings.
4. The AI returns ranked matches, scores, reasons, and confidence.
5. If the AI returns no suitable match, normal search is used.
6. If the AI times out, the system falls back to keyword search.
7. The result is logged.
8. The user reviews the ranked matches.
9. A low-confidence result is shown with a warning.
10. The user can accept a match or choose another asset.

## 2.3 UC-28 – Review Sustainability Recommendation

**Diagram file:** `images/UC-28.png`

**Primary actor:** Sustainability Officer

**Secondary actor:** AI Service

**Purpose:** Review an AI recommendation for the next sustainability action for an asset.

**Main interactions:**

1. The Sustainability Officer selects an asset.
2. The system reads asset condition, repair history, status, and value.
3. If insufficient information exists, the system displays “Not enough data”.
4. Otherwise, the system requests an AI recommendation.
5. The AI returns an action, reason, and confidence.
6. Disposal is considered only after other suitable options are ruled out.
7. The output is logged.
8. The officer reviews the recommendation.
9. The officer accepts, rejects, or changes the recommendation.
10. Any override is recorded.

## 2.4 UC-29 – Ask the Assistant

**Diagram file:** 

## 2.5 UC-30 – Generate AI Report

**Diagram file:** 

## 2.6 UC-31 – View Sustainability Dashboard

**Diagram file:**
## 2.7 UC-32 – Override an AI Output

**Diagram file:** `


## 2.8 UC-33 – Detect Duplicate Listings

**Diagram file:** 
## 2.9 UC-34 – Predict Maintenance Need

**Diagram file:** 


## 2.10 UC-35 – Submit AI Feedback

**Diagram file:** 

# 3. Class Diagram

## 3.1 AI Module

**Diagram file:** 

The AI module contains the main classes responsible for controlled interaction with AI services.

### Main Classes

| Class | Main responsibility |
|---|---|
| AIFacade | Provides a single entry point to the AI layer and coordinates privacy filtering, adapters, validation, fallback, and logging. |
| PrivacyFilter | Removes unnecessary personal data before AI processing. |
| AIAdapter | Common interface for AI providers. |
| LlmAdapter | Adapter for the selected LLM provider. |
| FallbackService | Provides non-AI fallback behavior. |
| AnswerChecker | Checks validity and confidence of AI results. |
| AIOutputLogger | Stores AI outputs and associated metadata. |
| AIResult | Represents the result returned from an AI function. |
| AIOutput | Represents a stored AI result. |
| AIOverride | Stores a user override of an AI result. |
| AIFeedback | Stores user feedback about an AI result. |

### AI Design Rules

| Class | Rule |
|---|---|
| AIFacade | AI requests use one controlled path. |
| PrivacyFilter | Names, emails, and personal identifiers are removed when not required. |
| AIAdapter / LlmAdapter | A provider can be changed without changing higher-level services. |
| FallbackService | Essential behavior has a fallback when AI is unavailable. |
| AnswerChecker | Invalid and low-confidence results are handled safely. |
| AIOutputLogger | Model, version, prompt version, confidence, and result are traceable. |
| AIOverride | User overrides are recorded with the final value and reason. |

## 3.2 AI Functions and Sustainability

**Diagram file:** 

The main application services are:

- ClassificationService
- MatchingService
- RecommendationService
- AssistantService
- AIReportService
- DuplicateDetector
- MaintenancePredictor
- OverrideService
- FeedbackService
- SustainabilityService
- ReuseEvent
- EmissionFactor
- Figures
- AIController
- DashboardController

### Service Responsibilities

| Service | Responsibility |
|---|---|
| ClassificationService | Runs AI-assisted asset classification. |
| MatchingService | Finds and ranks matching assets. |
| RecommendationService | Generates sustainability recommendations. |
| AssistantService | Processes natural-language user questions. |
| AIReportService | Generates and reviews AI report drafts. |
| DuplicateDetector | Detects possible duplicate listings. |
| MaintenancePredictor | Produces maintenance-risk predictions. |
| OverrideService | Stores user overrides and review actions. |
| FeedbackService | Stores AI feedback. |
| SustainabilityService | Calculates sustainability indicators. |
| ReuseEvent | Stores reuse activity and avoided-purchase information. |
| EmissionFactor | Stores emission-factor information. |
| Figures | Represents calculated sustainability figures and assumptions. |
| AIController | Exposes AI functions to the application. |
| DashboardController | Provides sustainability dashboard information. |

# 4. User Interface Mockups

## 4.1 AI Match Review

**Diagram/image file:** 
The AI match-review page shall show:

- ranked assets
- compatibility score
- explanation/reason
- confidence information
- warning when confidence is low
- option to accept a match
- option to choose another asset
- AI feedback control

## 4.2 Sustainability Recommendation

**Diagram/image file:** 
The screen shall show:

- recommended action
- confidence
- explanation
- alternative actions
- accept/change/reject controls
- override reason field
- clear statement that approval is still required

## 4.3 Assistant

**Diagram/image file:** 
The assistant interface shall show:

- user question
- AI response
- links to relevant assets or pages
- refusal when an action requires formal approval
- feedback option

## 4.4 AI Report Review

**Diagram/image file:** 

The report screen shall show:

- report title
- reporting period
- AI-generated status
- generated summary
- flagged figure mismatches
- edit control
- regenerate control
- mark as reviewed control
- export disabled until review

## 4.5 Sustainability Dashboard

**Diagram/image file:** 
The dashboard shall show:

- assets reused
- avoided purchases
- estimated financial savings
- estimated CO2 reduction
- reuse rate
- repair rate
- waste diversion
- asset-life extension
- assumptions for estimates
- missing-data warnings
- export option

## 4.6 Duplicate Warning and Maintenance Forecast

**Diagram/image file:** 

The interface shall show:

- possible duplicate listing
- similarity score
- existing matching listing
- cancel or publish-anyway option
- maintenance risk ranking
- reason for risk
- “not enough data” status
- schedule inspection option

# 5. Traceability

| Diagram | Use Case | Requirements |
|---|---|---|
| DFD 6.1, Sequence 2.1 | UC-26 Classify Asset | FR-AI-01 to FR-AI-15, FR-AI-X-01, FR-AI-X-02 |
| DFD 6.2, Sequence 2.2 | UC-27 Review AI Match | FR-AI-16 to FR-AI-35 |
| DFD 6.3, Sequence 2.3 | UC-28 Review Sustainability Recommendation | FR-AI-36 to FR-AI-49, FR-SUS-27 to FR-SUS-31 |
| DFD 6.4, Sequence 2.4 | UC-29 Ask the Assistant | FR-AI-50 to FR-AI-59 |
| DFD 6.5, Sequence 2.5 | UC-30 Generate AI Report | FR-AI-60 to FR-AI-70 |
| DFD 7.1 to 7.3, Sequence 2.6 | UC-31 View Sustainability Dashboard | FR-SUS-01 to FR-SUS-31 |
| DFD 6.8, Sequence 2.7 | UC-32 Override an AI Output | FR-AI-X-03, FR-AI-X-04 |
| DFD 6.6, Sequence 2.8 | UC-33 Detect Duplicate Listings | FR-AI requirements to be confirmed |
| DFD 6.7, Sequence 2.9 | UC-34 Predict Maintenance Need | FR-AI requirements to be confirmed |
| DFD 6.8, Sequence 2.10 | UC-35 Submit AI Feedback | FR-AI requirements to be confirmed |
| AI Module Class Diagram | All AI Use Cases | FR-AI-X-05 to FR-AI-X-17 |
| AI Module Class Diagram | Privacy and performance constraints | NFR-04, NFR-14 |

