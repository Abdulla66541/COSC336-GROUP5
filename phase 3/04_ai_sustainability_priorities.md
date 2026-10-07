## 4.15 AI-Assisted Asset Classification

### 4.15.1 Description

The system shall provide an AI-assisted asset classification function for newly registered assets. The function shall analyse the information provided by the user and recommend an appropriate category, subcategory, tags, material type, and missing metadata.

The classification function shall support information from the asset title, description, technical specifications, and available images. The recommended classification shall be shown to the user for review before it becomes part of the official asset record.

The user shall be able to accept or correct the AI-generated classification. This ensures that AI assists the registration process while the final classification remains under human control.

### 4.15.2 Inputs and Outputs

| Type | Information |
|---|---|
| Input | Asset title or name |
| Input | Asset description |
| Input | Technical specifications |
| Input | Asset image, when available |
| Output | Recommended category |
| Output | Recommended subcategory |
| Output | Relevant tags |
| Output | Material type |
| Output | Missing metadata |
| Output | Classification confidence information |

### 4.15.3 Functional Requirements

| Requirement ID | Requirement |
|---|---|
| FR-AI-01 | The system shall accept an asset title or name as input to the AI classification function. |
| FR-AI-02 | The system shall accept an asset description as input to the AI classification function. |
| FR-AI-03 | The system shall use available technical specifications when generating an asset classification recommendation. |
| FR-AI-04 | The system shall accept an asset image as an optional input when an image is available. |
| FR-AI-05 | The system shall recommend an appropriate category for a newly registered asset using the available asset information. |
| FR-AI-06 | The system shall recommend an appropriate subcategory when a suitable subcategory exists in the configured classification list. |
| FR-AI-07 | The system shall recommend relevant tags for the asset to support searching and matching. |
| FR-AI-08 | The system shall recommend a material type when sufficient information is available. |
| FR-AI-09 | The system shall identify important asset metadata that is missing from the submitted information. |
| FR-AI-10 | The system shall display the AI-generated classification results to the authorised user before the results are saved as the final asset classification. |
| FR-AI-11 | The system shall allow an authorised user to accept the AI-generated classification suggestions. |
| FR-AI-12 | The system shall allow an authorised user to modify the AI-generated category, subcategory, tags, or material type before saving the final classification. |
| FR-AI-13 | The system shall record whether an AI classification recommendation was accepted or modified by the user. |
| FR-AI-14 | The system shall save the user-approved classification information in the asset record. |
| FR-AI-15 | The system shall not automatically save an AI-generated classification as the final classification without user review. |
## 4.16 Semantic Matching and Ranking

### 4.16.1 Description

The system shall provide an AI-based semantic matching function that compares departmental resource requests with available asset listings. The function shall identify assets that may satisfy the request even when the wording of the request and asset description is different.

The matching process shall consider the information available in both the request and the asset record. The system shall generate a compatibility score and rank the available assets according to their suitability for the request.

AI-generated matches shall be presented as recommendations. The system shall not automatically approve, reserve, or transfer an asset based only on the AI-generated result.

### 4.16.2 Matching Factors

The matching function shall consider the following factors when evaluating an asset against a resource request:

| Factor | Description |
|---|---|
| Category Compatibility | The similarity between the requested category and the asset category. |
| Purpose | How well the intended use of the asset matches the stated purpose of the request. |
| Technical Specifications | Compatibility between requested specifications and available asset specifications. |
| Quantity | Whether the available quantity is sufficient for the request. |
| Condition | How well the asset condition matches the requested condition. |
| Location | The suitability of the asset location in relation to the request location. |
| Urgency | The ability of the asset to satisfy the required timeframe. |
| Required Date | Whether the asset can be made available by the requested date. |
| Transfer Cost | The estimated cost associated with moving the asset, when available. |
| Repair Cost | The estimated cost required to make the asset suitable for reuse, when applicable. |

### 4.16.3 Ranking and Compatibility Score

The system shall assign each AI-generated asset match a compatibility score from 0 to 100.

A higher score shall indicate that the asset is considered more suitable for the request based on the available matching factors.

The system shall provide a human-readable explanation of the main factors that contributed to each recommended match. The explanation should help the user understand why an asset was ranked highly.

The system shall support ranking matches according to the following considerations:

- Overall suitability
- Request urgency
- Transfer cost
- Potential waste-diversion benefit
- Estimated CO2 reduction

The ranking shall be presented to the user as a recommendation. The user shall remain responsible for reviewing the available matches and deciding which asset to pursue.

### 4.16.4 Functional Requirements

| Requirement ID | Requirement |
|---|---|
| FR-AI-16 | The system shall compare a resource request with available asset listings using the information contained in the request and asset records. |
| FR-AI-17 | The system shall consider category compatibility when evaluating a potential asset match. |
| FR-AI-18 | The system shall consider the stated purpose of the request when evaluating a potential asset match. |
| FR-AI-19 | The system shall consider technical specification compatibility when evaluating a potential asset match. |
| FR-AI-20 | The system shall consider the requested quantity and available asset quantity when evaluating a potential asset match. |
| FR-AI-21 | The system shall consider asset condition when evaluating a potential asset match. |
| FR-AI-22 | The system shall consider asset location and request location when evaluating a potential asset match. |
| FR-AI-23 | The system shall consider request urgency when evaluating a potential asset match. |
| FR-AI-24 | The system shall consider the required date when evaluating whether an asset can satisfy a request. |
| FR-AI-25 | The system shall consider estimated transfer cost when sufficient cost information is available. |
| FR-AI-26 | The system shall consider estimated repair cost when the asset requires repair and sufficient cost information is available. |
| FR-AI-27 | The system shall assign a compatibility score between 0 and 100 to each generated asset match. |
| FR-AI-28 | The system shall rank generated asset matches according to their calculated suitability for the request. |
| FR-AI-29 | The system shall provide a human-readable explanation of the main factors contributing to a recommended asset match. |
| FR-AI-30 | The system shall consider request urgency when ranking otherwise suitable asset matches. |
| FR-AI-31 | The system shall consider transfer cost when ranking otherwise suitable asset matches. |
| FR-AI-32 | The system shall consider potential waste-diversion benefit when ranking asset matches. |
| FR-AI-33 | The system shall consider estimated CO2 reduction when ranking asset matches where an estimate is available. |
| FR-AI-34 | The system shall display the ranked matches to the user before any reservation or transfer decision is made. |
| FR-AI-35 | The system shall not automatically approve, reserve, or transfer an asset solely because it received a high AI compatibility score. |

## 4.17 Sustainable-Action Recommendation

### 4.17.1 Description

### 4.17.2 Inputs and Outputs

### 4.17.3 Functional Requirements

## 4.18 LLM-Powered Assistant

### 4.18.1 Description

### 4.18.2 Supported User Tasks

### 4.18.3 Functional Requirements

## 4.19 Generative AI Reporting

### 4.19.1 Description

### 4.19.2 Report Types

### 4.19.3 Functional Requirements

## 4.19.4 Human Review

## 4.20 Cross-Cutting AI Requirements

### 4.20.1 Confidence Information

### 4.20.2 User Override

### 4.20.3 Model and Prompt Version Tracking

### 4.20.4 AI Fallback Behaviour

### 4.20.5 AI Output Logging

### 4.20.6 Human Approval Boundary

## 4.21 Sustainability Requirements

### 4.21.1 Waste Diversion

### 4.21.2 Avoided Purchases

### 4.21.3 Asset-Life Extension

### 4.21.4 Reuse Rate

### 4.21.5 Repair Rate

### 4.21.6 Financial Savings

### 4.21.7 Estimated Carbon Reduction

### 4.21.8 Sustainability Uncertainty and Assumptions

## 4.22 Use Cases

### UC-26 Classify Asset

### UC-27 View AI Match

### UC-28 Accept or Override AI Match

### UC-29 Review Sustainability Recommendation

### UC-30 Ask the LLM Assistant

### UC-31 Generate AI Report

### UC-32 View Sustainability Dashboard

### UC-33 Override an AI Output

### UC-34 View AI Explanation and Confidence

### UC-35 View AI Output History

# 8. Requirements Prioritisation

## 8.1 Prioritisation Criteria

## 8.2 Functional Requirements Prioritisation

## 8.3 AI Requirements Prioritisation

## 8.4 Sustainability Requirements Prioritisation
