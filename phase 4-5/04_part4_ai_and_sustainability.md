# Phase 4 & 5 - Part 4: AI Layer and Sustainability

**Owner:** Abdulla

**Use cases:** UC-26 Classify asset, UC-27 Review AI match, UC-28 Review sustainability recommendation, UC-29 Ask the assistant, UC-30 Generate AI report, UC-31 View sustainability dashboard, UC-32 Override an AI output, UC-33 Detect duplicate listings, UC-34 Predict maintenance need, UC-35 Submit AI feedback

**Requirement groups:** FR-AI-01 to FR-AI-70, FR-AI-X-01 to FR-AI-X-17, FR-SUS-01 to FR-SUS-31

**Data stores:** D10 AI Output Log, D11 Sustainability Records (reads D2, D4, D5, D8)

**Tables:** AI_OUTPUT, AI_OVERRIDE, AI_FEEDBACK, REUSE_EVENT, EMISSION_FACTOR

Shared diagrams (architecture, AI integration design, the one Level 0 DFD, ER diagram) are in `00_architecture_and_shared_design.md`. Read Section 2.4 there first. Every AI use case below uses the same path: service, AI Facade, privacy filter, AI Adapter, AI Service, answer checker, AI Output Log.


# 1. Sequence Diagrams

## 1.1 UC-26 Classify Asset

```mermaid
sequenceDiagram
    autonumber
    actor AC as Asset Custodian
    participant UI as Web Page
    participant AIController
    participant ClassificationService
    participant AIFacade
    participant Privacy as PrivacyFilter
    participant Adapter as AIAdapter
    participant AIService as AI Service
    participant Log as AIOutputLogger
    participant DB as Database

    AC->>UI: Click "Suggest category" on the form
    UI->>AIController: POST /ai/classify (title, description, specs, image)
    activate AIController
    AIController->>ClassificationService: classify(assetData)
    activate ClassificationService
    ClassificationService->>AIFacade: request("classification", data)
    activate AIFacade
    AIFacade->>Privacy: removePersonalData(data)
    Privacy-->>AIFacade: clean data
    AIFacade->>Adapter: send(clean data, promptVersion)
    Adapter->>AIService: classify

    alt answer within 15 seconds
        AIService-->>Adapter: category, subcategory, tags, material, confidence
        Adapter-->>AIFacade: result

        alt answer is not valid
            AIFacade-->>ClassificationService: ignore, ask user to choose by hand
        else confidence is below threshold
            AIFacade-->>ClassificationService: result with warning
        else answer is good
            AIFacade-->>ClassificationService: result
        end

    else no answer in 15 seconds
        Adapter-->>AIFacade: timeout
        AIFacade-->>ClassificationService: no suggestion, fallback used
    end

    deactivate AIFacade
    ClassificationService->>Log: save(modelId, modelVersion, promptVersion, confidence, result)
    Log->>DB: insert AI output
    ClassificationService-->>AIController: suggestion, confidence, warning or fallback notice
    deactivate ClassificationService
    AIController-->>UI: suggestion
    deactivate AIController
    UI-->>AC: Show category, tags, confidence
    AC->>UI: Accept or change

    Note over UI,DB: The suggestion is saved as the final classification only after the user accepts it (FR-AI-15). A change is saved as an override (UC-32).
```


## 1.2 UC-27 Review AI Match

```mermaid
sequenceDiagram
    autonumber
    actor U as RQ, AC, DR, AD or PO
    participant UI as Web Page
    participant AIController
    participant MatchingService
    participant AIFacade
    participant AIService as AI Service
    participant SearchService
    participant Log as AIOutputLogger
    participant OverrideService

    U->>UI: Open a request, click "Find matches"
    UI->>AIController: POST /ai/match (request id)
    activate AIController
    AIController->>MatchingService: findMatches(requestId)
    activate MatchingService
    MatchingService->>MatchingService: read request and active listings
    MatchingService->>AIFacade: request("matching", request, listings)
    activate AIFacade
    AIFacade->>AIService: embed and compare (no personal data)

    alt answer within 15 seconds
        AIService-->>AIFacade: ranked list, scores, reasons, confidence
        AIFacade-->>MatchingService: matches

        alt no matches
            MatchingService->>SearchService: normal search (UC-06)
            SearchService-->>MatchingService: results
        end

    else no answer in 15 seconds
        AIFacade-->>MatchingService: fallback
        MatchingService->>SearchService: keyword search (UC-06)
        SearchService-->>MatchingService: results
    end

    deactivate AIFacade
    MatchingService->>Log: save result and versions
    MatchingService-->>AIController: ranked matches (score 0 to 100, reasons)
    deactivate MatchingService
    AIController-->>UI: matches
    deactivate AIController
    UI-->>U: Show list with score and reasons

    alt confidence is low
        UI-->>U: Show warning "Please check this match"
    end

    alt user accepts a match
        U->>UI: Click "Reserve" (UC-07)
        Note over UI: The AI never reserves or approves by itself (FR-AI-35).
    else user rejects or chooses another asset
        U->>UI: Choose another asset
        UI->>OverrideService: saveOverride(output, finalValue)
    end
```


## 1.3 UC-28 Review Sustainability Recommendation

```mermaid
sequenceDiagram
    autonumber
    actor SO as Sustainability Officer
    participant UI as Web Page
    participant AIController
    participant RecommendationService
    participant AIFacade
    participant AIService as AI Service
    participant DB as Database
    participant Log as AIOutputLogger
    participant OverrideService

    SO->>UI: Open an asset, click "Recommend action"
    UI->>AIController: POST /ai/recommend (asset id)
    activate AIController
    AIController->>RecommendationService: recommend(assetId)
    activate RecommendationService
    RecommendationService->>DB: read condition, repair history, status, value
    DB-->>RecommendationService: asset data

    alt not enough data
        RecommendationService-->>AIController: "not enough data"
        AIController-->>UI: message
        UI-->>SO: Show "Not enough data"

    else enough data
        RecommendationService->>AIFacade: request("recommendation", data)
        AIFacade->>AIService: analyse (no personal data)

        alt valid answer
            AIService-->>AIFacade: action, reason, confidence
            AIFacade-->>RecommendationService: recommendation
            RecommendationService->>RecommendationService: disposal only if all other actions are not possible (BR-10)
            RecommendationService->>Log: save output and versions
            RecommendationService-->>AIController: recommendation with explanation
            deactivate RecommendationService
            AIController-->>UI: recommendation
            deactivate AIController
            UI-->>SO: Show action, reason, confidence

        else answer invalid or timeout
            AIFacade-->>RecommendationService: hidden, error logged
            RecommendationService-->>UI: no recommendation
        end

        alt Sustainability Officer accepts
            SO->>UI: Click "Accept"
            UI->>OverrideService: markReviewed(output)
            Note over UI,OverrideService: Accepting does not change the asset. A transfer, donation, recycling or disposal still needs the approval flow of Part 2 (FR-AI-49).

        else Sustainability Officer rejects or changes
            SO->>UI: Click "Reject" and enter a reason
            UI->>OverrideService: saveOverride(output, finalValue, reason)
            OverrideService->>Log: save override with user and time
        end
    end
```


## 1.4 UC-29 Ask the Assistant

```mermaid
sequenceDiagram
    autonumber
    actor U as User (any role except SA)
    participant UI as Web Page
    participant AIController
    participant Security
    participant AssistantService
    participant Privacy as PrivacyFilter
    participant AIFacade
    participant AIService as AI Service
    participant DB as Database
    participant Log as AIOutputLogger

    U->>UI: Type a question in the assistant box
    UI->>AIController: POST /ai/ask (question)
    activate AIController
    AIController->>Security: checkPermission(user, "assistant")
    Security-->>AIController: allowed with visible data scope
    AIController->>AssistantService: ask(question, userScope)
    activate AssistantService
    AssistantService->>Privacy: removePersonalData(question)
    Privacy-->>AssistantService: clean question
    AssistantService->>DB: read data the user may see (assets, requests, history, policy text)
    DB-->>AssistantService: data
    AssistantService->>AIFacade: request("assistant", question, data)
    AIFacade->>AIService: answer from this data

    alt answer is related and based on system data
        AIService-->>AIFacade: answer, confidence
        AIFacade-->>AssistantService: answer

    else answer is unrelated or no data
        AIFacade-->>AssistantService: standard "cannot answer"

    else no answer in 15 seconds
        AIFacade-->>AssistantService: fallback to normal search
    end

    AssistantService->>Log: save question type, answer and versions
    AssistantService-->>AIController: answer
    deactivate AssistantService
    AIController-->>UI: answer
    deactivate AIController
    UI-->>U: Show answer

    Note over UI,AssistantService: If the user asks it to approve a transfer or dispose of an asset, the assistant refuses and points to the approval page (FR-AI-58, FR-AI-59).
```


## 1.5 UC-30 Generate AI Report

```mermaid
sequenceDiagram
    autonumber
    actor U as AD, SO, FO or PO
    participant UI as Web Page
    participant AIController
    participant AIReportService
    participant SustainabilityService
    participant AIFacade
    participant AIService as AI Service
    participant DB as Database
    participant Log as AIOutputLogger

    U->>UI: Choose report type and period, click "Generate"
    UI->>AIController: POST /ai/reports
    activate AIController
    AIController->>AIReportService: generate(type, period, user)
    activate AIReportService
    AIReportService->>SustainabilityService: getFigures(period)
    SustainabilityService-->>AIReportService: figures and assumptions
    AIReportService->>DB: read summaries (requests, listings, transfers, maintenance)
    DB-->>AIReportService: summary data

    alt data set is too large
        AIReportService->>AIReportService: shorten the data and tell the user
    end

    AIReportService->>AIFacade: request("report", summary data)
    AIFacade->>AIService: write the summary text
    AIService-->>AIFacade: draft text
    AIFacade-->>AIReportService: draft
    AIReportService->>AIReportService: check every figure in the text against the data

    alt a figure does not match
        AIReportService->>AIReportService: flag the text for the reviewer
    end

    AIReportService->>Log: save draft and versions
    AIReportService->>DB: save report as "aiGenerated, not reviewed"
    AIReportService-->>AIController: draft report with period
    deactivate AIReportService
    AIController-->>UI: draft
    deactivate AIController
    UI-->>U: Show draft with banner "AI generated, please review"
    U->>UI: Edit if needed, click "Mark as reviewed"
    UI->>AIReportService: markReviewed(reportId, userId)
    AIReportService->>DB: set reviewed

    Note over UI,DB: A report cannot be shared before it is reviewed (FR-AI-70).
```


## 1.6 UC-31 View Sustainability Dashboard

```mermaid
sequenceDiagram
    autonumber
    actor U as SO, AD, FO or PO
    participant UI as Web Page
    participant DashboardController
    participant Security
    participant SustainabilityService
    participant DB as Database

    U->>UI: Open "Sustainability"
    UI->>DashboardController: GET /sustainability?period=...&dept=...
    activate DashboardController
    DashboardController->>Security: checkPermission(user, "dashboard")
    Security-->>DashboardController: allowed with scope
    DashboardController->>SustainabilityService: getFigures(period, scope)
    activate SustainabilityService
    SustainabilityService->>DB: read reuse events, repair records, asset values, emission factors

    alt data source is down
        DB-->>SustainabilityService: error
        SustainabilityService-->>DashboardController: last saved figures with date

    else data is read
        DB-->>SustainabilityService: rows
        SustainabilityService->>SustainabilityService: waste diversion, avoided purchases, life extension, reuse rate, repair rate, savings

        alt emission factor is missing
            SustainabilityService->>SustainabilityService: set CO2e to "not enough data" (FR-SUS-30)
        else emission factor exists
            SustainabilityService->>SustainabilityService: CO2e = quantity x emission factor
        end

        SustainabilityService->>SustainabilityService: mark estimates and list assumptions
        SustainabilityService-->>DashboardController: figures with assumptions
    end

    deactivate SustainabilityService
    DashboardController-->>UI: figures
    deactivate DashboardController
    UI-->>U: Show charts, estimates marked, assumptions on request

    opt user exports the view
        U->>UI: Click "Export"
        UI-->>U: CSV file
    end
```


## 1.7 UC-32 Override an AI Output

```mermaid
sequenceDiagram
    autonumber
    actor U as AC, DR, AD or SO
    participant UI as Web Page
    participant AIController
    participant Security
    participant OverrideService
    participant DB as Database
    participant Audit as History and Audit

    U->>UI: Click "Change" on an AI suggestion
    UI-->>U: Show override form
    U->>UI: Choose final value and enter a reason
    UI->>AIController: POST /ai/outputs/{id}/override
    activate AIController
    AIController->>Security: checkPermission(user, "override AI")

    alt user has no permission
        Security-->>AIController: denied
        AIController->>Audit: record denied attempt
        AIController-->>UI: access denied
        UI-->>U: Show "No permission"

    else user has permission
        Security-->>AIController: allowed
        AIController->>OverrideService: saveOverride(outputId, finalValue, reason, userId)
        activate OverrideService
        OverrideService->>DB: save override with user, time, final value and reason

        alt reason cannot be saved
            DB-->>OverrideService: error
            OverrideService-->>AIController: override not applied
            AIController-->>UI: error
            UI-->>U: Show "Try again"

        else saved
            DB-->>OverrideService: saved
            OverrideService->>Audit: record override
            OverrideService-->>AIController: done
            deactivate OverrideService
            AIController-->>UI: success
            deactivate AIController
            UI-->>U: Show the final value
        end
    end
```


## 1.8 UC-33 Detect Duplicate Listings

```mermaid
sequenceDiagram
    autonumber
    actor AC as Asset Custodian
    participant UI as Web Page
    participant MarketplaceService
    participant DuplicateDetector
    participant AIFacade
    participant AIService as AI Service
    participant Log as AIOutputLogger

    AC->>UI: Click "Publish" on an asset
    UI->>MarketplaceService: publish(assetId)
    MarketplaceService->>DuplicateDetector: checkDuplicates(asset)
    DuplicateDetector->>AIFacade: request("duplicate check", asset, active listings)

    alt AI Service available
        AIFacade->>AIService: compare similarity
        AIService-->>AIFacade: similar listings with scores
        AIFacade-->>DuplicateDetector: result
        DuplicateDetector->>Log: save output and versions

        alt a similar listing is found
            DuplicateDetector-->>UI: warning with the existing listing
            UI-->>AC: Show both listings, ask to cancel or continue

        else score is borderline
            DuplicateDetector-->>UI: show both listings, ask the user to decide

        else no duplicate
            DuplicateDetector-->>MarketplaceService: no duplicate
            MarketplaceService-->>UI: listing created
        end

    else AI Service not available
        AIFacade-->>DuplicateDetector: skipped
        DuplicateDetector-->>UI: continue, tell the user the check was skipped
    end
```


## 1.9 UC-34 Predict Maintenance Need

```mermaid
sequenceDiagram
    autonumber
    actor MS as Maintenance Staff
    participant UI as Web Page
    participant AIController
    participant MaintenancePredictor
    participant DB as Database
    participant AIFacade
    participant AIService as AI Service
    participant Log as AIOutputLogger

    MS->>UI: Open "Maintenance forecast"
    UI->>AIController: GET /ai/maintenance-forecast
    AIController->>MaintenancePredictor: predict()
    MaintenancePredictor->>DB: read assets, age, condition, repair history
    DB-->>MaintenancePredictor: asset data
    MaintenancePredictor->>AIFacade: request("forecast", data)

    alt valid answer within 15 seconds
        AIFacade->>AIService: rank assets by risk
        AIService-->>AIFacade: ranked list with reasons
        AIFacade-->>MaintenancePredictor: result
        MaintenancePredictor->>Log: save output and versions
        MaintenancePredictor-->>UI: list
        UI-->>MS: Show assets with risk and reason
        MS->>UI: Open an asset and click "Schedule inspection" (UC-24)

    else not enough data for an asset
        MaintenancePredictor-->>UI: list with "not enough data" for that asset

    else no answer or invalid answer
        AIFacade-->>MaintenancePredictor: fallback
        MaintenancePredictor-->>UI: plain inspection schedule instead
    end
```


## 1.10 UC-35 Submit AI Feedback

```mermaid
sequenceDiagram
    autonumber
    actor U as Any user
    participant UI as Web Page
    participant AIController
    participant FeedbackService
    participant DB as Database

    U->>UI: Click "Was this helpful?" under an AI result
    UI-->>U: Show rating and comment box
    U->>UI: Choose rating, write comment, click "Send"
    UI->>AIController: POST /ai/outputs/{id}/feedback
    AIController->>FeedbackService: save(outputId, userId, rating, comment)
    FeedbackService->>DB: check for same feedback from the same user

    alt same feedback was already sent
        FeedbackService-->>UI: kept one entry
        UI-->>U: Show "Thank you"

    else feedback is new
        FeedbackService->>DB: save feedback

        alt save fails
            DB-->>FeedbackService: error
            FeedbackService-->>UI: error, keep the comment
            UI-->>U: Show "Try again"

        else saved
            DB-->>FeedbackService: saved
            FeedbackService-->>UI: success
            UI-->>U: Show "Thank you"
        end
    end
```


# 2. Class Diagram

## 2.1 AI Module (design pattern: Facade + Adapter)

```mermaid
classDiagram
    class AIFacade {
        +request(function, data) AIResult
        -applyFallback(function, data) AIResult
        -checkConfidence(result) boolean
    }

    class PrivacyFilter {
        +removePersonalData(data) Data
    }

    class AIAdapter {
        <<interface>>
        +send(data, promptVersion) AIResult
    }

    class LlmAdapter {
        -String modelId
        -String modelVersion
        -int timeoutSeconds
        +send(data, promptVersion) AIResult
    }

    class FallbackService {
        +keywordSearch(request) List
        +fixedRules(asset) Recommendation
        +plainSchedule() List
    }

    class AnswerChecker {
        +isValid(result) boolean
        +isLowConfidence(result) boolean
    }

    class AIOutputLogger {
        +save(function, data, result) AIOutput
    }

    class AIResult {
        +String content
        +Decimal confidence
        +String explanation
        +String modelId
        +String modelVersion
        +String promptVersion
    }

    class AIOutput {
        +int aiOutputId
        +String functionName
        +int assetId
        +int requestId
        +String modelId
        +String modelVersion
        +String promptVersion
        +Decimal confidence
        +String content
        +DateTime createdAt
    }

    class AIOverride {
        +int overrideId
        +int aiOutputId
        +int userId
        +String finalValue
        +String reason
        +DateTime createdAt
    }

    class AIFeedback {
        +int feedbackId
        +int aiOutputId
        +int userId
        +int rating
        +String comment
    }

    AIFacade --> PrivacyFilter
    AIFacade --> AIAdapter
    AIFacade --> FallbackService
    AIFacade --> AnswerChecker
    AIFacade --> AIOutputLogger
    AIAdapter <|.. LlmAdapter
    AIAdapter ..> AIResult
    AIOutputLogger ..> AIOutput
    AIOutput "1" --> "0..*" AIOverride : is changed by
    AIOutput "1" --> "0..*" AIFeedback : gets
```


## 2.2 AI Functions and Sustainability

```mermaid
classDiagram
    class ClassificationService {
        +classify(assetData) Suggestion
    }

    class MatchingService {
        +findMatches(requestId) List
        -score(request, listing) int
    }

    class RecommendationService {
        +recommend(assetId) Recommendation
        -disposalOnlyLast(options) Recommendation
    }

    class AssistantService {
        +ask(question, userScope) Answer
        -refuseAction(question) boolean
    }

    class AIReportService {
        +generate(type, period, user) Report
        +markReviewed(reportId, userId) void
        -checkFigures(text, data) boolean
    }

    class DuplicateDetector {
        +checkDuplicates(asset) List
    }

    class MaintenancePredictor {
        +predict() List
    }

    class OverrideService {
        +saveOverride(outputId, finalValue, reason, userId) AIOverride
        +markReviewed(outputId) void
    }

    class FeedbackService {
        +save(outputId, userId, rating, comment) AIFeedback
    }

    class SustainabilityService {
        +recordReuseEvent(assetId, requestId) ReuseEvent
        +getFigures(period, scope) Figures
        +wasteDiversion(period) Decimal
        +avoidedPurchases(period) int
        +lifeExtension(assetId) int
        +reuseRate(period) Decimal
        +repairRate(period) Decimal
        +financialSavings(period) Decimal
        +carbonReduction(period) Decimal
    }

    class ReuseEvent {
        +int reuseId
        +int assetId
        +int requestId
        +String eventType
        +Decimal avoidedValueAed
        +DateTime eventTime
    }

    class EmissionFactor {
        +int factorId
        +int categoryId
        +Decimal kgCo2ePerUnit
        +String source
    }

    class Figures {
        +Decimal value
        +boolean isEstimate
        +String assumptions
        +String numerator
        +String denominator
    }

    class AIController {
        +postClassify() Response
        +postMatch() Response
        +postRecommend() Response
        +postAsk() Response
        +postReport() Response
        +postOverride() Response
        +postFeedback() Response
        +getForecast() Response
    }

    class DashboardController {
        +getFigures() Response
    }

    AIController ..> ClassificationService
    AIController ..> MatchingService
    AIController ..> RecommendationService
    AIController ..> AssistantService
    AIController ..> AIReportService
    AIController ..> OverrideService
    AIController ..> FeedbackService
    AIController ..> MaintenancePredictor
    DashboardController ..> SustainabilityService
    AIReportService ..> SustainabilityService
    SustainabilityService ..> ReuseEvent
    SustainabilityService ..> EmissionFactor
    SustainabilityService ..> Figures
    ClassificationService ..> AIFacade
    MatchingService ..> AIFacade
    RecommendationService ..> AIFacade
    AssistantService ..> AIFacade
    AIReportService ..> AIFacade
    DuplicateDetector ..> AIFacade
    MaintenancePredictor ..> AIFacade
```

| Class | Role | Rule it enforces |
|---|---|---|
| AIFacade | Single door to the AI layer. Applies the privacy filter, adapter, checker, fallback and logger in the same order every time | BR-11, NFR-04, NFR-14 |
| PrivacyFilter | Removes names, emails and IDs of people | NFR-14 |
| AIAdapter / LlmAdapter | One interface. A new provider only needs a new adapter class | Design goal "easy to change" |
| FallbackService | Keyword search, fixed rules, plain schedule | FR-AI-X-08 to 10 |
| AIOutputLogger | Saves model, version, prompt version, confidence and result | FR-AI-X-05 to 07, FR-AI-X-11 to 13 |
| OverrideService | Saves override, final value and reason | FR-AI-X-03, FR-AI-X-04, BR-12 |
| SustainabilityService | The formulas and the "estimate" marks | FR-SUS-01 to 31 |


## 2.3 Sustainability Formulas

From Phase 3, Section 4.21:

**Reuse rate (%)** = (assets reused or transferred / assets considered for reuse) x 100

**Repair rate (%)** = (assets repaired / assets needing a disposition decision) x 100

**Estimated carbon reduction (kg CO2e)** = activity quantity x emission factor, with the emission factor and its source shown on screen


# 3. User Interface Mockups

## 3.1 AI Match Review (UC-27)

```text
+----------------------------------------------------------------------+
|  Matches for request R-0042: "laboratory seating x10"                |
|                                                                      |
|  Rank  Asset                 Score  Why                              |
|  1     Lab bench stool x20   91     Same purpose, stock is enough,   |
|                                     Good condition, same campus      |
|  2     Office chair x6       64     Not enough quantity, Fair        |
|                                                                      |
|  Confidence: High            AI suggestions need your decision.      |
|  [ Reserve #1 ]  [ Choose another asset ]  [ Was this helpful? ]     |
+----------------------------------------------------------------------+
|  Low confidence example:                                             |
|  ! The AI is not sure about this match. Please check it.             |
+----------------------------------------------------------------------+
```


## 3.2 Sustainability Recommendation (UC-28, UC-32)

```text
+----------------------------------------------------------------------+
|  Recommended action for A-2045 Projector                             |
|                                                                      |
|  Suggested: REPAIR              Confidence: 74 %                     |
|  Why: Repair cost is low and the asset is 3 years old.               |
|  Other options: Transfer, Refurbish, Recycle                         |
|  Disposal is the last option.                                        |
|                                                                      |
|  [ Accept ]   [ Change ]   [ Reject ]                                |
|                                                                      |
|  Change or reject:                                                   |
|  Final value [ Transfer v ]   Reason * [____________________]        |
|                                                [ Save override ]     |
|                                                                      |
|  Accepting does not change the asset. Approvals are still needed.    |
+----------------------------------------------------------------------+
```


## 3.3 Assistant (UC-29)

```text
+----------------------------------------------------------------------+
|  Assistant                                                           |
|                                                                      |
|  You:        Which projectors are available in Engineering?          |
|  Assistant:  2 projectors are published by Engineering:              |
|              A-2045 (Good) and A-2051 (Fair).  [Open A-2045]         |
|                                                                      |
|  You:        Approve the transfer of A-2045 for me.                  |
|  Assistant:  I cannot approve transfers. An administrator must       |
|              approve it on the Approvals page.                       |
|                                                                      |
|  [ Type your question here ______________________ ] [ Send ]          |
|  [ Was this helpful? ]                                               |
+----------------------------------------------------------------------+
```


## 3.4 AI Report Review (UC-30)

```text
+----------------------------------------------------------------------+
|  AI report: Monthly summary, September 2026                          |
|  ! AI generated. Please review before sharing.                       |
|                                                                      |
|  Period: 2026-09-01 to 2026-09-30                                   |
|  Summary: 14 assets were reused. 6 purchases were avoided with an    |
|  estimated value of AED 21,000 (estimate).                           |
|  Flagged: "AED 25,000" does not match the data (AED 21,000).         |
|                                                                      |
|  [ Edit text ]   [ Regenerate ]   [ Mark as reviewed ]               |
|  Status: Not reviewed             [ Export ] (disabled until reviewed)|
+----------------------------------------------------------------------+
```


## 3.5 Sustainability Dashboard (UC-31)

```text
+----------------------------------------------------------------------+
|  Sustainability                  Period [ Sep 2026 v ] Dept [ All v ]|
|                                                                      |
|  Assets reused    Avoided purchases   Savings (est.)   CO2e (est.)   |
|  14               6                   AED 21,000       380 kg        |
|                                                                      |
|  Reuse rate  70 %  (14 of 20)         Repair rate 50 % (5 of 10)     |
|  Waste diverted  38 items             Life extension 26 months (est.)|
|                                                                      |
|  [bar chart: reuse by month]          [pie: actions taken]           |
|                                                                      |
|  Values marked "est." are estimates. [Show assumptions] [Export]     |
|  Missing emission factor: "Not enough data"                          |
+----------------------------------------------------------------------+
```


## 3.6 Duplicate Warning (UC-33) and Maintenance Forecast (UC-34)

```text
+----------------------------------------------+   +--------------------------------------+
|  Possible duplicate listing                  |   |  Maintenance forecast                |
|                                              |   |                                      |
|  New: Lab bench stool x20 (CS)               |   |  Asset      Risk     Reason          |
|  Existing: Lab bench stool x20 (CS) L-0044   |   |  A-2045     High     5 repairs, 6 y  |
|  Similarity: 93 %                            |   |  A-2102     Medium   Age 4 y         |
|  [ Cancel ]   [ Publish anyway ]             |   |  A-2201     -        Not enough data |
+----------------------------------------------+   |  [Schedule inspection]               |
                                                   +--------------------------------------+
```


# 4. Traceability

| Diagram | Use case | Requirements |
|---|---|---|
| Sequence 1.1 | UC-26 Classify asset | FR-AI-01 to 15, FR-AI-X-01, FR-AI-X-02 |
| Sequence 1.2 | UC-27 Review AI match | FR-AI-16 to 35 |
| Sequence 1.3 | UC-28 Review sustainability recommendation | FR-AI-36 to 49, FR-SUS-27 to 31 |
| Sequence 1.4 | UC-29 Ask the assistant | FR-AI-50 to 59 |
| Sequence 1.5 | UC-30 Generate AI report | FR-AI-60 to 70 |
| Sequence 1.6 | UC-31 View sustainability dashboard | FR-SUS-01 to 31 |
| Sequence 1.7 | UC-32 Override an AI output | FR-AI-X-03, FR-AI-X-04, BR-12 |
| Sequence 1.8 | UC-33 Detect duplicate listings | No functional requirement in Phase 3 yet |
| Sequence 1.9 | UC-34 Predict maintenance need | No functional requirement in Phase 3 yet |
| Sequence 1.10 | UC-35 Submit AI feedback | No functional requirement in Phase 3 yet |
| AI module class diagram | All AI use cases | FR-AI-X-05 to 17, NFR-04, NFR-14 |
