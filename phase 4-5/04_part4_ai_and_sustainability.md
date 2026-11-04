# Phase 4 & 5 – Part 4: AI Layer and Sustainability

**Owner:** Abdulla

**Use cases:** UC-26 to UC-35

**Requirement groups:** FR-AI-01 to FR-AI-70, FR-AI-X-01 to FR-AI-X-17, FR-SUS-01 to FR-SUS-31

**Data stores:** D10 AI Output Log, D11 Sustainability Records

**Tables:** AI_OUTPUT, AI_OVERRIDE, AI_FEEDBACK, REUSE_EVENT, EMISSION_FACTOR

**Common AI Integration Path:**

Service → AI Facade → Privacy Filter → AI Adapter → AI Service → Answer Checker → AI Output Log


# 1. Sequence Diagrams

## 1.1 UC-26 – Classify Asset

**Primary actor:** Asset Custodian  
**Secondary actor:** AI Service

The sequence diagram shows how an Asset Custodian requests AI-assisted classification for an asset. The AI returns a suggested category, confidence score, and explanation. The user reviews the result and either accepts or changes the classification.

If the confidence is low, the system warns the user. If the AI service does not respond within the configured timeout, the user can classify the asset manually.

**Diagram:** UC-26 Classify Asset sequence diagram.


## 1.2 UC-27 – View, Accept or Override Match

**Primary actors:** Requester, Asset Custodian  
**Secondary actor:** AI Service

The sequence diagram shows how the system compares a request or listing with available assets. The AI returns ranked matches with compatibility scores, confidence information, and explanations.

The user can accept a suggested match or choose another option. If the AI service is unavailable, the system falls back to normal search.


## 1.3 UC-28 – Review Sustainability Recommendation

**Primary actor:** Sustainability Officer  
**Secondary actor:** AI Service

The sequence diagram shows how asset condition, maintenance history, value, and other information are used to generate a sustainability recommendation.

Possible recommendations include retaining, transferring, repairing, refurbishing, donating, recycling, or disposing of an asset.

The Sustainability Officer reviews the recommendation before any action is taken.


## 1.4 UC-29 – Ask the Assistant

**Primary actor:** All authorised users  
**Secondary actor:** AI Service

The assistant allows users to ask questions using natural language.

The system retrieves only information the user is authorised to access and sends the required information through the AI layer.

The assistant may help with resource search, request information, asset history, status, policy guidance, and system navigation.

The assistant cannot approve transfers, disposal, donation, or ownership changes.


## 1.5 UC-30 – Generate AI Report

**Primary actors:** Administrator, Sustainability Officer  
**Secondary actor:** AI Service

The system collects report data and asks the AI service to produce a written summary.

The generated report is treated as a draft. Important figures are checked against the system data, and an authorised user must review the report before formal use.


## 1.6 UC-31 – View Sustainability Dashboard

**Primary actors:** Sustainability Officer, Administrator

The dashboard displays sustainability indicators such as:

- Assets reused
- Avoided purchases
- Waste diversion
- Repair rate
- Reuse rate
- Estimated financial savings
- Estimated carbon reduction
- Asset-life extension

Estimated figures are clearly identified and their assumptions are available to the user.


## 1.7 UC-32 – Override an AI Output

**Primary actors:** Asset Custodian, Administrator, Sustainability Officer

An authorised user can reject or change an AI-generated output.

The system records:

- Original AI output
- Final user-selected value
- User who performed the override
- Reason for the override
- Date and time

The human decision becomes the final decision.


## 1.8 UC-33 – Detect Duplicate Listings

**Primary actor:** Asset Custodian  
**Secondary actor:** AI Service

When a new asset or listing is created, the system compares it with existing listings.

Possible duplicates are shown with a similarity score.

The system does not automatically merge or delete records. The Asset Custodian makes the final decision.


## 1.9 UC-34 – Predict Maintenance Need

**Primary actor:** Maintenance Staff  
**Secondary actor:** AI Service

The system uses asset age, condition, repair history, and inspection information to identify assets that may require maintenance.

The AI produces a risk ranking and explanation.

Maintenance Staff reviews the result and may schedule an inspection.


## 1.10 UC-35 – Submit AI Feedback

**Primary actor:** All authorised users

Users can rate an AI output as helpful or not helpful and may provide an optional comment.

The feedback is associated with the relevant AI output and can later be reviewed by administrators.


# 2. Class Diagrams

## 2.1 AI Module

The AI module contains the shared components used by the AI-enabled functions.

### Main Classes

| Class | Responsibility |
|---|---|
| AIFacade | Provides a single controlled entry point to AI functionality. |
| PrivacyFilter | Removes unnecessary personal information before external AI processing. |
| AIAdapter | Defines a common interface for AI providers. |
| LlmAdapter | Connects the system to the selected LLM service. |
| FallbackService | Provides non-AI behaviour when the AI service is unavailable. |
| AnswerChecker | Checks AI results for validity and confidence. |
| AIOutputLogger | Stores AI outputs and related metadata. |
| AIResult | Represents the result returned by an AI function. |
| AIOutput | Represents a stored AI output. |
| AIOverride | Records a human override of an AI output. |
| AIFeedback | Stores user feedback about an AI output. |

### AI Design Rules

- AI outputs are recommendations.
- Human approval remains required for controlled decisions.
- Personal information should not be sent to external AI services unless required.
- AI outputs should be logged.
- Model and prompt versions should be recorded where available.
- AI functions should provide fallback behaviour where appropriate.
- Low-confidence outputs should be clearly indicated.


## 2.2 AI Functions and Sustainability

### Main Services

| Service | Responsibility |
|---|---|
| ClassificationService | Performs AI-assisted asset classification. |
| MatchingService | Matches requests with available assets. |
| RecommendationService | Generates sustainable-action recommendations. |
| AssistantService | Handles natural-language questions. |
| AIReportService | Generates AI-assisted reports. |
| DuplicateDetector | Detects possible duplicate listings. |
| MaintenancePredictor | Identifies possible maintenance needs. |
| OverrideService | Stores human overrides. |
| FeedbackService | Stores AI feedback. |
| SustainabilityService | Calculates sustainability indicators. |

### Sustainability Data Classes

| Class | Responsibility |
|---|---|
| ReuseEvent | Records reuse and avoided-purchase events. |
| EmissionFactor | Stores carbon-emission factors and sources. |
| Figures | Represents calculated sustainability figures and assumptions. |


# 3. User Interface Mockups

## 3.1 AI Match Review

The AI Match Review screen should display:

- Ranked matches
- Compatibility score
- Explanation
- Confidence information
- Low-confidence warning
- Accept match option
- Choose another asset option
- Feedback control


## 3.2 Sustainability Recommendation

The Sustainability Recommendation screen should display:

- Recommended action
- Confidence
- Explanation
- Alternative actions
- Accept option
- Change option
- Reject option
- Override reason field

The interface must clearly state that the AI recommendation does not automatically approve the action.


## 3.3 Assistant Interface

The assistant interface should provide:

- Natural-language input
- AI response
- Links to relevant assets or pages
- Clear refusal when the requested action requires formal approval
- Feedback controls


## 3.4 AI Report Review

The AI Report Review screen should provide:

- Report title
- Reporting period
- AI-generated label
- Generated summary
- Figure mismatch warnings
- Edit option
- Regenerate option
- Mark as reviewed option
- Export option after review


## 3.5 Sustainability Dashboard

The sustainability dashboard should display:

- Reuse count
- Avoided purchases
- Waste diversion
- Reuse rate
- Repair rate
- Financial savings
- Estimated carbon reduction
- Asset-life extension
- Assumptions
- Missing-data warnings


## 3.6 Duplicate Detection and Maintenance Forecast

The duplicate-listing screen should display:

- New listing
- Possible existing duplicate
- Similarity score
- Cancel option
- Continue option

The maintenance forecast should display:

- Asset
- Risk level
- Reason
- Insufficient-data indicator
- Schedule inspection option


# 4. Traceability

| Design Element | Use Case | Related Requirements |
|---|---|---|
| Sequence 1.1 | UC-26 Classify Asset | FR-AI-01 to FR-AI-15 |
| Sequence 1.2 | UC-27 AI Match | FR-AI-16 to FR-AI-35 |
| Sequence 1.3 | UC-28 Sustainability Recommendation | FR-AI-36 to FR-AI-49 |
| Sequence 1.4 | UC-29 Assistant | FR-AI-50 to FR-AI-59 |
| Sequence 1.5 | UC-30 AI Report | FR-AI-60 to FR-AI-70 |
| Sequence 1.6 | UC-31 Sustainability Dashboard | FR-SUS-01 to FR-SUS-31 |
| Sequence 1.7 | UC-32 AI Override | FR-AI-X-03 to FR-AI-X-04 |
| Sequence 1.8 | UC-33 Duplicate Detection | FR-AI requirements to be confirmed |
| Sequence 1.9 | UC-34 Maintenance Prediction | FR-AI requirements to be confirmed |
| Sequence 1.10 | UC-35 AI Feedback | FR-AI requirements to be confirmed |
| AI Module Class Diagram | All AI use cases | FR-AI-X-01 to FR-AI-X-17 |
| Sustainability Classes | UC-28, UC-31 | FR-SUS-01 to FR-SUS-31 |

