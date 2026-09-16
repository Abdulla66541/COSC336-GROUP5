# 7. Success Criteria and Project Plan

## 7.1 Measurable Success Criteria
The success of the Circular Campus Asset Reuse and Management System will be evaluated using measurable criteria. These criteria cover system functionality, user acceptance, AI usefulness, financial savings, asset reuse, and sustainability impact.

| Area | Success Criterion | Measurement |
|---|---|---|
| Functional Performance | The system successfully implements the essential project requirements. | 100% of the Must-have functional requirements are implemented and pass testing. |
| User Acceptance | The system is understandable and useful for intended university users. | At least 80% positive feedback during User Acceptance Testing (UAT). |
| AI Match Usefulness | AI-generated asset matches are relevant to user requests. | At least 70% of AI-generated matches are rated as relevant or useful during testing. |
| Avoided Purchases | The system helps departments find reusable assets before purchasing new items. | Record the number and estimated value of purchases avoided through internal reuse. |
| Reuse and Repair | The system encourages assets to be reused, transferred, or repaired instead of discarded. | Track the percentage and number of registered assets that are reused, transferred, or repaired. |
| Sustainability Outcomes | The system contributes to reducing university waste and environmental impact. | Track assets diverted from disposal and provide an estimated amount of waste and CO2 emissions avoided where suitable data is available. |

## 7.2 Preliminary Timeline
The project is divided into eight phases according to the course project schedule. Each phase has a defined deliverable and contributes to the gradual development of the system.

| Phase | Submission Deadline | Duration | Main Deliverable | Weight |
|---|---|---|---|---|
| Phase 1 | In the labs of the week of Sep 14th, 2026 | 1 Week | Initial Plan and Requirement Gathering Document | 10% |
| Phase 2 | In the labs of the week of Sept 21st, 2026 | 1 Week | Feasibility Document | 10% |
| Phase 3 | In the labs of the week of Oct 5th, 2026 | 2 Weeks | Requirements Document | 10% |
| Phases 4 & 5 | In the labs of the week of Oct 26th, 2026 | 3 Weeks | Design Document (Architecture and Detailed Design) | 20% |
| Phase 6 | In the labs of the week of Nov 16th, 2026 | 3 Weeks | Draft Implementation with Major Features | 20% |
| Phase 7 | In the labs of the week of Nov 23rd, 2026 | 1 Week | Details of Test Cases | 10% |
| Phase 8 | In the labs of the week of Nov 23rd, 2026 | Not specified | Final Project, Presentation and Demonstration | 20% |

The timeline will be used to monitor progress and ensure that each major deliverable is completed before the required laboratory submission period.
## 7.3 Milestones and Deliverables
Each project phase represents a major milestone. The team will use these milestones to track progress and ensure that the required work is completed before moving to later stages.

| Phase | Milestone | Deliverable |
|---|---|---|
| Phase 1 | Project planning and initial requirements completed | Initial Plan and Requirement Gathering Document |
| Phase 2 | Project feasibility evaluated | Feasibility Document |
| Phase 3 | Detailed system requirements defined | Requirements Document |
| Phases 4 & 5 | System architecture and detailed design completed | Design Document (Architecture and Detailed Design) |
| Phase 6 | Major system functionality implemented | Draft Implementation with Major Features |
| Phase 7 | System testing prepared and documented | Details of Test Cases |
| Phase 8 | Final system completed and demonstrated | Final Project, Presentation and Demonstration |

The team will review the work completed at each milestone before continuing to the next stage. This will help identify missing requirements, design problems, implementation issues, and testing concerns early in the project.
## 7.4 Development Methodology
The team proposes to use an Agile-inspired development approach throughout the project. The project phases will be treated as development iterations in which the team plans the required work, produces the expected deliverables, reviews the results, and improves the system based on feedback.

This approach is suitable because the project is divided into several phases with separate deliverables. Instead of attempting to complete the entire system at once, the team can progressively develop the requirements, design, implementation, testing, and final system.

The weekly laboratory environment also supports an iterative approach because the team can receive feedback from the instructor and lab engineer and use that feedback to improve later work.

An iterative methodology is particularly useful for the AI-enhanced features of the project. AI-based resource matching, AI-assisted asset classification, sustainability optimization, the LLM-powered assistant, and generative AI reporting may require experimentation and refinement before satisfactory results are achieved.

The general development cycle will be:

**Plan → Develop → Test and Review → Receive Feedback → Improve → Continue to the Next Phase**

Although the project will use Agile principles, the team will continue to follow the official course phase deadlines and required deliverables.
## 7.5 Team Structure and Roles
The project team consists of four members. Each member has a primary responsibility while also contributing to reviews, development, testing, and documentation when required.

| Team Member | Proposed Primary Role | Phase 1 Responsibility | Preliminary Later Responsibility |
|---|---|---|---|
| Mohammed Alketbi | Project Coordinator | Introduction, problem statement, project overview, and final document assembly | Coordinate project integration, documentation, and selected core modules |
| Mohammed Al Ali | Design and AI Lead | Stakeholder analysis and current-process analysis | Support system/interface design and AI-related components |
| Mubarak | Requirements Lead | Requirements gathering and initial requirements specification | Maintain requirements and support requirements-based testing |
| Abdulla | Development and Testing Lead | Success criteria, timeline, methodology, roles, risks, resources, and AI reflection | Support implementation, integration, and system testing |

The exact ownership of implementation modules may be adjusted during the design phase depending on workload, technical difficulty, and each member's experience.

Although each member has a primary role, the project will not depend entirely on one person for any major component. Team members will review each other's work and share enough information so that progress can continue if one member is temporarily unavailable.

All members are also responsible for maintaining clear GitHub commit history so that their individual contributions can be identified.
## 7.6 Dependencies, Risks and Resource Allocation
### 7.6.1 Project Dependencies

Several project activities depend on the successful completion of earlier work.

- Requirements must be understood before detailed system design can be completed.
- The system design should define the main structure before major implementation begins.
- Implementation must reach a usable stage before complete system testing can be performed.
- AI-based functions depend on having suitable asset and request data for testing and evaluation.
- Some AI functions may depend on access to an external AI model or API.
- Sustainability calculations depend on having enough information to estimate avoided purchases, waste diversion, and environmental impact.
- Final integration depends on team members completing their assigned work on time.

These dependencies will be reviewed during each project phase so that delays can be identified and handled early.

### 7.6.2 Project Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| AI API becomes unavailable, limited, or expensive | Medium | High | Use free-tier or alternative services where possible and keep non-AI fallback functionality for essential processes. |
| Lack of realistic university asset data | High | Medium | Create representative sample datasets containing realistic asset categories, quantities, conditions, locations, and requests. |
| Team member becomes temporarily unavailable | Medium | Medium | Keep work documented on GitHub, commit regularly, and make sure other members understand the main project components. |
| Project scope becomes too large | Medium | High | Prioritise Must-have requirements first and postpone lower-priority enhancements if necessary. |
| AI produces inaccurate or irrelevant recommendations | Medium | High | Test AI results using multiple examples and require human review for important decisions. |
| AI recommendations are difficult to explain | Medium | Medium | Present AI results as suggestions and provide supporting information where possible. |
| Sensitive university information is sent to an external AI service | Medium | High | Avoid sending unnecessary personal or confidential information and use controlled test data during development. |
| GitHub conflicts or lost work | Low | Medium | Commit frequently, use meaningful commit messages, and review changes before merging. |
| Insufficient time for testing | Medium | High | Begin testing individual functions during development instead of waiting until the final project phase. |

### 7.6.3 Resource Allocation

The team will use available software and university resources to minimise project cost.

Expected resources include:

- **GitHub:** version control, documentation, collaboration, and tracking individual contributions.
- **Visual Studio Code:** software development environment.
- **Python and/or JavaScript:** implementation of application functionality where appropriate.
- **Database technology:** storage of assets, requests, users, transfers, inspections, and life-cycle information.
- **AI/LLM service:** experimentation and implementation of AI-enhanced functionality.
- **draw.io:** preparation of system diagrams and design models.
- **University laboratory facilities:** development, testing, demonstrations, and instructor feedback.
- **Sample datasets:** testing both classic and AI-enhanced system functions.

Resources will be allocated according to the needs of each project phase. Team members will also share responsibility for reviewing and testing integrated components.
## 7.7 Classic vs AI-Enhanced Approach Reflection
The proposed system combines traditional software functions with AI-enhanced functionality. Both approaches are useful, but they should be used for different types of tasks.

Traditional or deterministic software is more suitable when the system must follow clear and predictable rules. Examples include user permissions, asset quantities, reservation status, transfer approvals, ownership records, custody information, and audit history. These functions require consistent and reliable behaviour. For example, the system should use fixed rules to determine whether a user has permission to approve a transfer instead of allowing an AI model to make that decision.

AI is more suitable for tasks that involve interpretation, recommendations, classification, or natural-language interaction. In this project, AI can help match available assets with departmental requests, recommend categories and tags for assets, suggest sustainability actions, support users through an LLM-powered assistant, and generate summaries and reports.

AI-based resource matching can be useful because a request and an asset listing may describe the same need using different words. AI can compare factors such as meaning, technical compatibility, condition, quantity, location, and urgency to suggest potentially suitable resources.

AI-assisted classification can recommend categories, tags, and standardised descriptions for newly registered assets. Sustainability optimisation can also recommend whether an asset should be reused, transferred, repaired, refurbished, donated, recycled, or retired.

However, AI should support human users rather than replace them in important decisions. Actions such as approving transfers, changing asset custody, approving purchases, or disposing of university property should remain under human control.

A suitable process is:

**AI Suggests → Human Reviews → Human Approves or Rejects**

There are also risks when using AI. AI-generated results may be inaccurate, irrelevant, biased, or difficult to explain. An AI model may misunderstand a request or recommend an unsuitable asset. Users should therefore be able to review recommendations before acting on them.

Privacy is another important concern. Asset records and user requests may contain internal university information. The system should avoid sending unnecessary personal, confidential, or sensitive information to external AI services.

For this reason, a hybrid approach is suitable for the project. Traditional software rules should control functions that require accuracy, security, permissions, and accountability. AI should be used for functions that benefit from flexible interpretation, recommendations, natural-language interaction, and generated summaries.

The purpose of the AI components is to assist users and improve efficiency while keeping important decisions under human control.
