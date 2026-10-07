# 4. AI, Sustainability and Prioritisation

## 4.15 AI-Assisted Asset Classification

The system shall provide an AI-assisted classification function for newly registered assets. The function shall analyse available asset information and recommend a suitable category, subcategory, tags, material type, and missing metadata.

The classification function shall support the following inputs:

- Asset title or name
- Asset description
- Technical specifications
- Asset images, when available

The system shall use the available asset information to generate classification suggestions. The suggestions shall be presented to an authorised user for review before they are saved as the official asset classification.

### Functional Requirements

| Requirement ID | Requirement |
|---|---|
| FR-AI-01 | The system shall accept an asset title and description as input to the AI classification function. |
| FR-AI-02 | The system shall use available technical specifications when generating an asset classification recommendation. |
| FR-AI-03 | The system shall accept an asset image as an optional input when image-based classification is supported. |
| FR-AI-04 | The system shall recommend a category for a newly registered asset using the available asset information. |
| FR-AI-05 | The system shall recommend a subcategory when a suitable subcategory exists in the configured classification list. |
| FR-AI-06 | The system shall recommend relevant tags for the asset to improve future search and matching. |
| FR-AI-07 | The system shall identify important asset metadata that is missing from the submitted information. |
| FR-AI-08 | The system shall display the AI-generated classification recommendations before they are saved to the asset record. |
| FR-AI-09 | The system shall allow an authorised user to accept or modify the AI-generated category, subcategory, tags, and other suggested metadata. |
| FR-AI-10 | The system shall record whether an AI classification suggestion was accepted or changed by the user. |
| FR-AI-11 | The system shall store the final user-approved classification in the asset record. |
| FR-AI-12 | The system shall not automatically approve an AI classification as final without user review. |
### 4.15.1 Description

### 4.15.2 Inputs and Outputs

### 4.15.3 Functional Requirements

## 4.16 Semantic Matching and Ranking

### 4.16.1 Description

### 4.16.2 Matching Factors

### 4.16.3 Ranking and Compatibility Score

### 4.16.4 Functional Requirements

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
