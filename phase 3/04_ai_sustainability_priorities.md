## 4.17 Sustainable-Action Recommendation

### 4.17.1 Description

The system shall provide an AI-assisted sustainability recommendation function for assets that may no longer be suitable for their current use. The function shall analyse available asset information and recommend an appropriate next action.

Possible recommendations shall include retaining the asset, transferring it to another department, repairing it, refurbishing it, donating it, disassembling it, recycling it, or disposing of it as a last option.

The recommendation shall support the circular use of campus resources by considering the condition, maintenance information, potential reuse, and other available asset information.

The AI recommendation shall be presented to an authorised user for review. The system shall not automatically perform the recommended action.

### 4.17.2 Inputs and Outputs

| Type | Information |
|---|---|
| Input | Asset category |
| Input | Asset description |
| Input | Asset condition |
| Input | Maintenance and repair history |
| Input | Current availability or status |
| Input | Asset location |
| Input | Asset age or purchase date |
| Input | Estimated value |
| Input | Available reuse or transfer information |
| Output | Recommended sustainability action |
| Output | Explanation of the recommendation |
| Output | Confidence information |

### 4.17.3 Functional Requirements

| Requirement ID | Requirement |
|---|---|
| FR-AI-36 | The system shall use the available asset information when generating a sustainability-action recommendation. |
| FR-AI-37 | The system shall consider the asset condition when generating a sustainability-action recommendation. |
| FR-AI-38 | The system shall consider available maintenance and repair history when generating a sustainability-action recommendation. |
| FR-AI-39 | The system shall recommend retaining an asset when the available information indicates that continued use is suitable. |
| FR-AI-40 | The system shall recommend transferring an asset when available information indicates that another department may reuse it. |
| FR-AI-41 | The system shall recommend repair when the asset may be returned to service through repair. |
| FR-AI-42 | The system shall recommend refurbishment when refurbishment may extend the useful life of the asset. |
| FR-AI-43 | The system shall recommend donation when donation is an appropriate available option. |
| FR-AI-44 | The system shall recommend disassembly when component recovery is more suitable than continued use. |
| FR-AI-45 | The system shall recommend recycling when other reuse, repair, refurbishment, donation, or disassembly options are not suitable and recycling is appropriate. |
| FR-AI-46 | The system shall treat disposal as a last-option recommendation. |
| FR-AI-47 | The system shall provide a human-readable explanation for each sustainability recommendation. |
| FR-AI-48 | The system shall display the sustainability recommendation to an authorised user before any action is taken. |
| FR-AI-49 | The system shall not automatically dispose of, donate, recycle, transfer, or otherwise change the status of an asset based only on an AI recommendation. |

## 4.18 LLM-Powered Assistant

### 4.18.1 Description

The system shall provide an LLM-powered assistant that allows authorised users to interact with the system using natural language.

The assistant shall help users search for available resources, prepare resource requests, ask questions about asset history and status, obtain policy guidance available within the system, and navigate supported system services.

The assistant shall use information available in the system when answering asset-related questions. It shall not independently approve transfers, change asset ownership or custody, approve disposal, or perform other actions that require authorised human approval.

### 4.18.2 Supported User Tasks

| Task | Description |
|---|---|
| Resource Search | Help users find available resources using natural-language queries. |
| Request Submission | Help users prepare the information required to submit a resource request. |
| Asset History Questions | Answer questions about recorded asset history using available system records. |
| Asset Status | Provide information about the recorded status of an asset or request. |
| Policy Guidance | Provide guidance using approved policy information available to the assistant. |
| Navigation | Help users locate supported system functions and pages. |

### 4.18.3 Functional Requirements

| Requirement ID | Requirement |
|---|---|
| FR-AI-50 | The system shall accept natural-language questions from authorised users through the LLM assistant. |
| FR-AI-51 | The system shall allow users to search for available resources using natural-language queries through the assistant. |
| FR-AI-52 | The system shall assist users in preparing a resource request using information provided in natural language. |
| FR-AI-53 | The system shall provide asset-history information using records available in the system. |
| FR-AI-54 | The system shall provide recorded asset or request status information when requested by an authorised user. |
| FR-AI-55 | The system shall provide policy guidance using approved information available to the assistant. |
| FR-AI-56 | The system shall provide navigation guidance for supported system functions. |
| FR-AI-57 | The system shall indicate when requested information is not available in the system data. |
| FR-AI-58 | The system shall not allow the assistant to approve transfers, approve disposal, change ownership, or change custody. |
| FR-AI-59 | The system shall require the appropriate authorised user to complete any action that requires formal approval. |

## 4.19 Generative AI Reporting

### 4.19.1 Description

The system shall provide a generative AI reporting function that produces summaries based on recorded system data.

The reporting function shall support management and sustainability review by summarising resource-exchange activity, sustainability outcomes, maintenance trends, and other relevant information.

Generated reports shall be based on available system records and shall be reviewed by an authorised human before they are used for formal reporting or decision-making.

### 4.19.2 Report Types

| Report Type | Main Information |
|---|---|
| Monthly Activity Summary | Resource requests, listings, reservations, and completed transfers during the reporting period. |
| Sustainability Update | Reuse, repair, waste diversion, avoided purchases, and estimated environmental impact. |
| High-Demand Categories | Categories with a high number of requests during the reporting period. |
| Maintenance Insights | Maintenance activity, repair trends, and recurring maintenance issues. |
| Recommended Actions | AI-generated summary of potential actions based on recorded system information. |

### 4.19.3 Functional Requirements

| Requirement ID | Requirement |
|---|---|
| FR-AI-60 | The system shall generate a monthly summary of recorded resource-exchange activities. |
| FR-AI-61 | The system shall summarise recorded resource requests, listings, and completed transfers for the selected reporting period. |
| FR-AI-62 | The system shall generate a sustainability summary using recorded sustainability indicators. |
| FR-AI-63 | The system shall summarise avoided purchases when supporting records are available. |
| FR-AI-64 | The system shall summarise waste-diversion information when supporting records are available. |
| FR-AI-65 | The system shall summarise estimated carbon-emission reductions when supporting estimates are available. |
| FR-AI-66 | The system shall identify high-demand asset categories from recorded request data. |
| FR-AI-67 | The system shall summarise maintenance trends from recorded maintenance and repair data. |
| FR-AI-68 | The system shall generate recommended actions based on available system information. |
| FR-AI-69 | The system shall identify the reporting period covered by each generated report. |
| FR-AI-70 | The system shall allow an authorised user to review a generated report before it is used as an official report. |

### 4.19.4 Human Review

Generated reports shall be treated as draft outputs until reviewed by an authorised user.

The reviewer shall check important figures and statements against the underlying system data before using the report for formal communication or decision-making.

The system shall not treat an AI-generated report as an authoritative record if its contents have not been reviewed.

## 4.20 Cross-Cutting AI Requirements

### 4.20.1 Confidence Information

| Requirement ID | Requirement |
|---|---|
| FR-AI-X-01 | The system shall provide confidence information for each AI-generated classification, match, recommendation, assistant response, or generated report when confidence information is available. |
| FR-AI-X-02 | The system shall indicate when the confidence of an AI output is below the configured confidence threshold. |

### 4.20.2 User Override

| Requirement ID | Requirement |
|---|---|
| FR-AI-X-03 | The system shall allow an authorised user to override an AI-generated output when the user has the required permission. |
| FR-AI-X-04 | The system shall record the user override and the final value selected by the user. |

### 4.20.3 Model and Prompt Version Tracking

| Requirement ID | Requirement |
|---|---|
| FR-AI-X-05 | The system shall record the model identifier and model version used to generate an AI output when that information is provided by the AI service. |
| FR-AI-X-06 | The system shall record the prompt version used to generate an AI output. |
| FR-AI-X-07 | The system shall associate recorded model and prompt version information with the corresponding AI output. |

### 4.20.4 AI Fallback Behaviour

| Requirement ID | Requirement |
|---|---|
| FR-AI-X-08 | The system shall provide a fallback method for essential search or matching functionality when the AI service is unavailable. |
| FR-AI-X-09 | The system shall use a configured non-AI fallback when an AI output has confidence below the required threshold and a suitable fallback is available. |
| FR-AI-X-10 | The system shall inform the user when an AI-generated function is unavailable and a fallback method is being used. |

### 4.20.5 AI Output Logging

| Requirement ID | Requirement |
|---|---|
| FR-AI-X-11 | The system shall record each AI output generated for a supported system function. |
| FR-AI-X-12 | The system shall record the date and time associated with each logged AI output. |
| FR-AI-X-13 | The system shall associate a logged AI output with the relevant asset, request, report, or user interaction when applicable. |

### 4.20.6 Human Approval Boundary

| Requirement ID | Requirement |
|---|---|
| FR-AI-X-14 | The system shall treat AI outputs as recommendations and shall not allow an AI function to independently approve an asset transfer. |
| FR-AI-X-15 | The system shall not allow an AI function to independently approve asset disposal or donation. |
| FR-AI-X-16 | The system shall not allow an AI function to independently change asset ownership or custody. |
| FR-AI-X-17 | The system shall require an authorised human user to complete actions that require formal approval. |

## 4.21 Sustainability Requirements

The system shall provide measurable sustainability indicators to evaluate the effect of resource reuse and asset life-cycle management.

All sustainability figures produced by the system shall be treated as estimates unless they are directly derived from confirmed recorded values. The system shall store or display the assumptions used for estimated calculations.

### 4.21.1 Waste Diversion

Waste diversion measures the amount of assets or material kept out of disposal through reuse, repair, refurbishment, donation, recycling, or other approved actions.

| Requirement ID | Requirement |
|---|---|
| FR-SUS-01 | The system shall calculate the quantity of assets diverted from disposal during a selected reporting period. |
| FR-SUS-02 | The system shall calculate waste diversion using the recorded quantity and applicable asset or material data. |
| FR-SUS-03 | The system shall display waste diversion using an appropriate unit such as item count or estimated kilograms. |
| FR-SUS-04 | The system shall identify the reporting period for each waste-diversion result. |

### 4.21.2 Avoided Purchases

Avoided purchases represent purchases that may have been unnecessary because an existing campus asset was reused.

| Requirement ID | Requirement |
|---|---|
| FR-SUS-05 | The system shall record a reuse event that results in an estimated avoided purchase. |
| FR-SUS-06 | The system shall calculate the number of avoided purchases during a selected reporting period. |
| FR-SUS-07 | The system shall calculate the estimated value of avoided purchases using the recorded or estimated replacement value. |
| FR-SUS-08 | The system shall identify the assumptions used when calculating estimated avoided-purchase value. |

### 4.21.3 Asset-Life Extension

Asset-life extension measures additional useful time obtained by repairing, refurbishing, transferring, or otherwise continuing to use an asset.

| Requirement ID | Requirement |
|---|---|
| FR-SUS-09 | The system shall record an action that extends an asset's useful life when such an action is completed. |
| FR-SUS-10 | The system shall calculate estimated asset-life extension using recorded dates and available life-cycle information. |
| FR-SUS-11 | The system shall display asset-life extension using an appropriate unit such as months or years. |
| FR-SUS-12 | The system shall identify the assumptions used when an asset-life extension is estimated. |

### 4.21.4 Reuse Rate

The reuse rate measures the proportion of relevant assets that are reused or transferred rather than disposed of.

**Reuse Rate (%) = (Number of Assets Reused or Transferred / Number of Assets Considered for Reuse) × 100**

| Requirement ID | Requirement |
|---|---|
| FR-SUS-13 | The system shall calculate reuse rate using the defined reuse-rate formula. |
| FR-SUS-14 | The system shall display reuse rate as a percentage. |
| FR-SUS-15 | The system shall identify the numerator and denominator values used in each reuse-rate calculation. |

### 4.21.5 Repair Rate

The repair rate measures the proportion of applicable assets that receive repair action rather than being immediately retired or disposed of.

**Repair Rate (%) = (Number of Assets Repaired / Number of Assets Requiring a Disposition Decision) × 100**

| Requirement ID | Requirement |
|---|---|
| FR-SUS-16 | The system shall calculate repair rate using the defined repair-rate formula. |
| FR-SUS-17 | The system shall display repair rate as a percentage. |
| FR-SUS-18 | The system shall identify the numerator and denominator values used in each repair-rate calculation. |

### 4.21.6 Financial Savings

Financial savings represent the estimated financial benefit obtained through reuse, repair, refurbishment, and avoided purchases.

**Estimated Financial Savings = Estimated Avoided Purchase Value + Other Recorded Savings - Relevant Additional Costs**

| Requirement ID | Requirement |
|---|---|
| FR-SUS-19 | The system shall calculate estimated financial savings for a selected reporting period when the required input values are available. |
| FR-SUS-20 | The system shall identify the input values used to calculate estimated financial savings. |
| FR-SUS-21 | The system shall display financial savings using a monetary unit. |
| FR-SUS-22 | The system shall indicate when financial savings are estimated rather than confirmed. |

### 4.21.7 Estimated Carbon Reduction

Estimated carbon reduction represents the potential emissions avoided by reusing, repairing, or otherwise extending the life of assets instead of purchasing replacement items or disposing of them.

**Estimated CO2 Reduction = Activity Quantity × Applicable Emission Factor**

The applicable emission factor shall depend on the relevant asset category or activity and shall be recorded as an assumption where it is not obtained from a confirmed source.

| Requirement ID | Requirement |
|---|---|
| FR-SUS-23 | The system shall calculate estimated carbon reduction when the required activity quantity and emission factor are available. |
| FR-SUS-24 | The system shall display estimated carbon reduction using a unit such as kg CO2e. |
| FR-SUS-25 | The system shall identify the emission factor used in an estimated carbon-reduction calculation. |
| FR-SUS-26 | The system shall identify the assumptions used when an emission factor is estimated or selected for prototype testing. |

### 4.21.8 Sustainability Uncertainty and Assumptions

| Requirement ID | Requirement |
|---|---|
| FR-SUS-27 | The system shall identify sustainability values that are estimates rather than directly measured values. |
| FR-SUS-28 | The system shall display the main assumptions used to produce an estimated sustainability value. |
| FR-SUS-29 | The system shall identify the data source or input values used in each sustainability calculation when available. |
| FR-SUS-30 | The system shall indicate when insufficient data is available to produce a sustainability estimate. |
| FR-SUS-31 | The system shall avoid presenting estimated sustainability values as exact measured values. |

# 8. Requirements Prioritisation

## 8.1 Prioritisation Criteria

Requirements are prioritised according to their importance to the core purpose of the system, their contribution to the project objectives, their implementation difficulty, and their value to users.

The three priority levels are:

- **Essential:** The requirement is necessary for the prototype because it supports a core workflow or a major project objective.
- **Desirable:** The requirement provides useful additional functionality but can be simplified or postponed if time or resources become limited.
- **Future:** The requirement is suitable for later development after the core prototype has been completed.

The prioritisation protects the core functionality of the system. If schedule or technical constraints occur, Future requirements should be postponed before Essential requirements are removed.

## 8.2 Functional Requirements Prioritisation

| Requirement Group | Priority | Reason |
|---|---|---|
| FR-AST – Asset Registration and Inventory | Essential | Asset records are the foundation of the system and are required by the other workflows. |
| FR-MKT – Resource Publication / Marketplace | Essential | Reusable and surplus resources must be visible to potential users. |
| FR-REQ – Resource Request Submission | Essential | Requests are necessary to represent departmental demand for resources. |
| FR-SRC – Search and Filtering | Essential | Users need a basic method to discover available resources. |
| FR-RSV – Reservation and Request Management | Essential | Reservation and request tracking support the resource-exchange process. |
| FR-APR – Approval Workflows | Essential | Approvals are required to maintain control over transfers and disposal-related actions. |
| FR-TRF – Transfer Management | Essential | Transfer management is a core purpose of the resource-exchange system. |
| FR-MNT – Inspection, Maintenance and Repair | Essential | Maintenance and repair support asset life-cycle management. |
| FR-HST – Life-Cycle History | Essential | Asset history preserves accountability when an asset changes location or custody. |
| FR-DSP – Donation, Recycling and Disposal | Essential | These functions complete the asset life-cycle process. |
| FR-USR – User and Access Management | Essential | Authentication and role-based access are necessary for secure operation. |
| FR-NTF – Notifications | Desirable | Notifications improve workflow awareness but are not required for the basic exchange workflow. |
| FR-RPT – Operational Reports | Desirable | Operational reports provide useful monitoring but are not required for the minimum core workflow. |
| FR-AUD – Audit Logging | Essential | Auditability is important for tracking sensitive actions and maintaining accountability. |

## 8.3 AI Requirements Prioritisation

| Requirement Group | Priority | Reason |
|---|---|---|
| FR-AI-01 to FR-AI-15 – AI Asset Classification | Essential | AI-assisted classification is one of the required AI capabilities and can reduce manual classification effort. |
| FR-AI-16 to FR-AI-35 – Semantic Matching and Ranking | Essential | AI matching is central to connecting available assets with departmental demand. |
| FR-AI-36 to FR-AI-49 – Sustainable-Action Recommendation | Essential | Sustainability recommendations directly support the circular-campus objective. |
| FR-AI-50 to FR-AI-59 – LLM-Powered Assistant | Desirable | The assistant provides useful natural-language interaction but the core system can operate without advanced assistant functionality. |
| FR-AI-60 to FR-AI-70 – Generative AI Reporting | Desirable | Generated reports provide additional management value but are less critical than the core exchange workflow. |
| FR-AI-X-01 to FR-AI-X-02 – Confidence Information | Essential | Users need confidence information to evaluate AI outputs appropriately. |
| FR-AI-X-03 to FR-AI-X-04 – User Override | Essential | Human override is necessary to keep AI-assisted decisions under user control. |
| FR-AI-X-05 to FR-AI-X-07 – Model and Prompt Version Tracking | Essential | Version tracking supports AI output traceability and evaluation. |
| FR-AI-X-08 to FR-AI-X-10 – AI Fallback Behaviour | Essential | Essential functions should remain usable when AI services are unavailable or unreliable. |
| FR-AI-X-11 to FR-AI-X-13 – AI Output Logging | Essential | Logging supports traceability and review of AI-generated outputs. |
| FR-AI-X-14 to FR-AI-X-17 – Human Approval Boundary | Essential | AI must not independently approve important asset-management decisions. |

## 8.4 Sustainability Requirements Prioritisation

| Requirement Group | Priority | Reason |
|---|---|---|
| FR-SUS-01 to FR-SUS-04 – Waste Diversion | Essential | Waste diversion is a central sustainability outcome of the project. |
| FR-SUS-05 to FR-SUS-08 – Avoided Purchases | Essential | Avoided purchases demonstrate the financial and reuse benefits of using existing campus resources. |
| FR-SUS-09 to FR-SUS-12 – Asset-Life Extension | Essential | Extending useful asset life directly supports the circular-campus objective. |
| FR-SUS-13 to FR-SUS-15 – Reuse Rate | Essential | Reuse rate provides a direct measure of resource reuse. |
| FR-SUS-16 to FR-SUS-18 – Repair Rate | Essential | Repair rate measures how effectively assets are kept in service. |
| FR-SUS-19 to FR-SUS-22 – Financial Savings | Desirable | Financial savings provide useful evidence of project value but depend on available cost data. |
| FR-SUS-23 to FR-SUS-26 – Estimated Carbon Reduction | Desirable | Carbon reduction provides useful sustainability information but depends on suitable emission factors and assumptions. |
| FR-SUS-27 to FR-SUS-31 – Sustainability Uncertainty and Assumptions | Essential | Estimated sustainability values must be clearly identified and supported by their assumptions. |

## 8.5 Priority Summary

The prioritisation gives highest importance to the core asset-exchange workflow, security and accountability, essential AI capabilities, human oversight, and the main sustainability indicators.

Desirable requirements such as advanced LLM assistant functionality, generative reporting, financial-savings analysis, and carbon-reduction analysis can be simplified if development time becomes limited.

Future functionality identified during later project planning, such as advanced forecasting and external system integrations, should be implemented only after the Essential requirements are stable and tested.
