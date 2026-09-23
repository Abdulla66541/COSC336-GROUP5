# 9. Legal, Ethical and Policy Constraints

The proposed system must consider legal, security, licensing, university-policy, safety, and ethical constraints. These constraints affect how the system collects data, controls access, uses AI services, and supports asset-management decisions. They do not prevent development of the prototype, but they must be considered throughout the system design.

## 9.1 Data Privacy

The system may process information relating to university users together with asset, request, transfer, inspection, and maintenance records. Some records could contain personal information such as names, university identifiers, contact information, departments, or records of actions performed by users.

The project must consider the UAE Federal Decree-Law No. 45 of 2021 concerning the Protection of Personal Data when personal data is processed.

During development and testing, the project will use synthetic data instead of real Khalifa University personal or operational data wherever possible. Synthetic data allows the team to create realistic asset records, requests, transfers, maintenance records, and user accounts without using information belonging to real students or staff.

The system should also minimise the amount of personal information processed. Information that is not required for a particular function should not be sent to an external AI service.

For example, an AI asset-matching request may require an asset category, description, quantity, condition, technical requirements, and location. It would normally not require the requester's real name, university ID, or contact information.

Khalifa University has a public website privacy policy that describes measures for protecting personal information collected through its website. However, the policy states that it applies to information collected online through the website. Therefore, a real deployment of this project would require confirmation of the university's applicable internal privacy, security, and data-handling requirements.

**Design response:** use synthetic data during development, minimise personal information, restrict access by role, and avoid sending unnecessary identifiable or confidential information to external AI services.

## 9.2 Security

The system will contain information about assets, users, requests, approvals, transfers, inspections, and maintenance activities. Unauthorized access or modification could result in incorrect records, unauthorized transfers, or loss of accountability.

The system should therefore use role-based access control. Each user should only be able to perform actions that are appropriate for their assigned role. For example, a requester may submit an asset request, while approval of a transfer should only be available to an authorised role.

Important actions should also be recorded in an audit trail. The audit trail should record information such as the user responsible for an action, the action performed, the affected asset or request, and the time of the action.

Authentication information should be protected, passwords should not be stored as plain text, and user input should be validated before it is processed or stored.

**Design response:** implement authentication, role-based permissions, protected credentials, input validation, and audit logging for important system actions.

## 9.3 Intellectual Property and Licensing

The project may use external software libraries, frameworks, databases, AI models, and APIs. These components may have different licences and terms of use.

Before using a third-party component, the team should check its licence and comply with any required conditions. The team should also keep a record of the important external libraries and services used in the project.

The project repository uses the MIT License. The MIT License allows the software to be used, modified, and distributed, provided that the required copyright and licence notice is retained.

The MIT License applied to the team's own project does not replace the licences or terms of third-party libraries, AI models, APIs, or datasets. Each external component remains subject to its own licence or terms.

If an external AI API is selected, its terms of service, usage limits, permitted uses, and data-handling conditions should be reviewed before integration.

**Design response:** document major third-party components, check their licences before use, retain required licence notices, and review the terms of external AI services before integrating them.

## 9.4 Procurement and Asset Ownership Rules

The system should support asset-management decisions rather than automatically make decisions that require university authorization.

Actions that affect asset ownership, custody, transfer, donation, disposal, or procurement should only be completed by users who have the appropriate authority. An AI recommendation should not automatically cause an asset to be transferred, donated, or disposed of.

For example, the system may recommend transferring an unused computer to another department, but the actual transfer should require approval from the appropriate authorised user.

The system should also maintain the history of important asset changes, including previous custody, locations, transfers, and approvals. This helps maintain accountability when responsibility for an asset changes.

The exact approval rules for a real Khalifa University deployment would need to be confirmed against the university's applicable procurement and asset-management procedures.

**Design response:** enforce role-based approval permissions, preserve asset history, and require authorised human approval for transfers, disposal, donation, procurement, and other important asset-management decisions.

## 9.5 Safety Constraints

Some university assets may require inspection or maintenance before they can safely be transferred or reused. This may be particularly important for laboratory equipment, electrical equipment, damaged assets, or equipment that requires calibration.

The system should not assume that every available asset is automatically safe or suitable for reuse. Asset condition, inspection status, and maintenance history should be considered before an item is transferred.

Where necessary, the system should allow an asset to be marked as requiring inspection, maintenance, or approval before the transfer is completed.

An AI recommendation should not be treated as proof that physical equipment is safe to use. Safety-sensitive decisions should remain under the control of appropriately qualified personnel.

**Design response:** record condition, inspection, and maintenance information, allow assets to be marked as requiring inspection, and keep safety-related approval under human control.

## 9.6 Ethical Use of AI

The project includes AI-based resource matching, AI-assisted asset classification, sustainability recommendations, an LLM-powered assistant, and generative AI reporting.

These functions may improve efficiency, but AI-generated results can be inaccurate, incomplete, biased, or difficult to explain. For example, an AI model may misunderstand a departmental request or recommend an asset that is not actually suitable.

AI outputs should therefore be presented as recommendations rather than guaranteed decisions. Where possible, the system should provide supporting information that helps the user understand a recommendation, such as category, condition, quantity, location, technical compatibility, or similarity score.

Important decisions should remain under human control. AI should not independently approve asset transfers, change ownership or custody, authorise disposal, or make procurement decisions.

Generative reports should be based on information available in the system. Important figures and conclusions should be supported by the underlying records rather than generated without evidence.

The team should also consider possible bias in AI recommendations. Testing should include different asset categories and request types so that the team can identify situations where the AI performs poorly.

If an AI service is unavailable or produces an unreliable result, essential system functions should still be usable without depending completely on AI.

**Design response:** use AI as decision support, maintain human oversight, provide supporting information where possible, test AI outputs, and provide non-AI fallback behaviour for essential functions.

## 9.7 Course AI Policy

AI functionality is a required part of the project. The system is expected to include AI-based resource matching, AI-assisted asset classification, sustainability recommendations, an LLM-powered assistant, and generative AI reporting.

The use of AI tools during the preparation of coursework and documentation is a separate issue and must follow the COSC 336 Assessment Details and any instructions provided by the instructor or lab engineer.

Each team member remains responsible for understanding and being able to explain the work submitted under their name.

**Design response:** implement the required AI functionality as part of the system while following the course rules concerning the use of AI tools during development and documentation.

## 9.8 Feasibility Conclusion

The identified legal, ethical, policy, security, licensing, and safety constraints do not prevent development of the proposed prototype.

The project is considered feasible provided that synthetic data is used during development where possible, personal information is minimised, external AI services are used carefully, third-party licences and terms are respected, role-based permissions are enforced, and important asset-management decisions remain under authorised human control.

A future deployment using real Khalifa University systems or operational data would require additional review of the university's applicable internal privacy, security, procurement, asset-management, and safety requirements.

# 10. Risk Assessment

The Phase 1 risk assessment identified several technical, schedule, data, and team-related risks. During the feasibility study, these risks are reviewed in more detail to determine how they could affect successful development of the system.

The table below includes both preventive mitigation actions and contingency plans. Mitigation describes what the team will do to reduce the chance or impact of a risk, while the contingency plan describes what the team will do if the risk actually occurs.

| Risk | Likelihood | Impact | Mitigation | Contingency Plan | Owner |
|---|---|---|---|---|---|
| Free-tier AI API quota is exhausted or the service becomes unavailable | Medium | High | Monitor API usage, minimise unnecessary calls, cache results where possible, and keep essential functions independent of AI. | Switch to another available free service or temporarily use rule-based/manual functionality so core system features continue working. | AI/Development Lead |
| Synthetic data is not realistic enough to evaluate the system properly | Medium | High | Create a dataset containing different asset categories, conditions, departments, requests, transfers, and maintenance records based on the Phase 1 requirements. | Expand or revise the synthetic dataset and add missing edge cases before final testing. | Requirements Lead |
| Team lacks enough experience with AI integration | Medium | High | Start AI experiments early, use simple approaches first, divide research between team members, and document successful examples. | Reduce AI complexity and implement a simpler solution such as basic embeddings, fixed prompts, or deterministic fallback rules. | AI/Development Lead |
| AI produces inaccurate or irrelevant recommendations | Medium | High | Test the AI using different asset and request examples, display supporting information, and keep humans responsible for final decisions. | Disable or limit the unreliable AI feature and use manual search, filters, or rule-based recommendations until it can be improved. | AI/Development Lead |
| Project scope becomes too large for the available time | Medium | High | Prioritise the Must-have requirements defined during requirements gathering and avoid adding unnecessary features. | Remove or postpone Should-have and Could-have features and concentrate development effort on the core system. | Project Coordinator |
| Phases 7 and 8 have deadlines in the same week | High | High | Begin testing before Phase 7, prepare test cases during implementation, and avoid leaving final integration until the last week. | Freeze new features, focus only on fixing critical defects, and divide testing, documentation, and presentation work between team members. | Project Coordinator / All Members |
| Phase 6 implementation takes longer than expected | Medium | High | Develop core functions incrementally during earlier phases and test individual components as they are completed. | Reduce lower-priority functionality and focus on completing a stable version of the Must-have features. | Development/Testing Lead |
| A team member becomes temporarily unavailable | Medium | Medium | Maintain documentation, use regular GitHub commits, and ensure more than one member understands important project components. | Reassign urgent tasks between available members and adjust lower-priority work if necessary. | Project Coordinator |
| GitHub conflicts, accidental deletion, or integration problems occur | Low | Medium | Commit frequently with meaningful messages, review changes before merging, and avoid editing the same section simultaneously. | Restore a previous Git version, resolve conflicts manually, and use commit history to recover lost work. | All Members |
| External software, library, or AI-service terms change | Low | Medium | Check licences and service terms before depending on an external tool and avoid unnecessary vendor-specific dependencies. | Replace the affected component with an alternative library, model, or service that meets the project requirements. | Development Lead |
| Sensitive information is accidentally included in AI requests | Low | High | Use synthetic data, minimise data sent to external services, and avoid including names, university IDs, or confidential information in prompts. | Stop sending affected data, remove it from test inputs where possible, review the integration, and change the application so only necessary non-sensitive fields are sent. | Development Lead |
| Insufficient time remains for complete testing | Medium | High | Begin unit and functional testing during development and prepare test cases before Phase 7. | Prioritise testing of Must-have functions and high-risk workflows such as authentication, approvals, transfers, and AI recommendations. | Development/Testing Lead |

## 10.1 Overall Risk Evaluation

The project contains several risks, but none of the identified risks currently make the proposed system infeasible.

The most important risks are the limited project schedule, dependence on free AI services, the quality of synthetic test data, AI accuracy, and the possibility that the planned scope becomes too large.

These risks can be controlled by keeping the Must-have requirements as the main development priority, testing AI functions early, maintaining non-AI fallback options, preparing realistic synthetic data, and beginning testing before the final project phases.

The team should review the risk table during each phase and update the likelihood, impact, mitigation, and contingency plans if project conditions change.

# 11. Recommendation and Action Plan

## 11.1 Overall Recommendation

Based on the feasibility analysis, the recommendation is to **proceed with the project, with conditions**.

The proposed Circular Campus Resource Exchange and Asset Life Cycle Management System is feasible as a student software-engineering project as long as the team keeps the scope controlled, prioritises the Must-have requirements, uses realistic synthetic data for development and testing, and avoids making the core system completely dependent on external AI services.

The classic asset-management functions should form the reliable foundation of the system. AI functionality should then be added where it provides clear value, such as resource matching, classification, sustainability recommendations, natural-language interaction, and report generation.

Important decisions such as transfer approval, disposal, changes in asset custody, and procurement-related actions should remain under authorised human control.

The team should therefore continue to Phase 3 while resolving the main technical, data, scope, and AI decisions identified in this feasibility study.

## 11.2 Feasibility Summary

| Dimension | Verdict | Key Condition |
|---|---|---|
| Technical Feasibility | Feasible | Use a manageable technology stack and keep the system architecture suitable for the team's available skills and project duration. |
| Financial Feasibility | Feasible | Use free or low-cost development tools, hosting, databases, and AI services during the prototype stage. |
| Operational Feasibility | Feasible with conditions | Workflows must be easy to understand, role responsibilities must be clear, and unnecessary data entry should be reduced. |
| Schedule Feasibility | Feasible with conditions | Must-have requirements must be prioritised and development and testing must begin early enough to avoid pressure during the final phases. |
| Data Feasibility | Feasible for the prototype | A realistic synthetic dataset must be created because real Khalifa University operational data is not currently available to the team. |
| AI Feasibility | Feasible with limitations | AI functions should be tested on synthetic data, important outputs should be reviewed by users, and fallback behaviour should be available if an AI service fails. |
| Legal, Ethical and Policy Feasibility | Feasible with conditions | Personal data should be minimised, licences and service terms must be respected, and important decisions must remain under authorised human control. |
| Risk Feasibility | Manageable | Major risks must be reviewed regularly and contingency plans should be used if schedule, API, data, or scope problems occur. |

Overall, no feasibility dimension currently requires the project to be stopped. However, several dimensions depend on controlling the project scope and validating important technical decisions early.

## 11.3 Phase 3 Action Plan

The main objective before and during Phase 3 is to convert the current feasibility decisions into clear and testable system requirements.

The following actions should be completed:

| Action | Proposed Owner | Expected Result |
|---|---|---|
| Confirm the final technology stack | Design/AI Lead and Development/Testing Lead | Agreed backend, frontend, database, and AI technologies |
| Finalise the synthetic dataset design | Requirements Lead | Defined asset, request, user, transfer, inspection, maintenance, and related test-data fields |
| Review and lock the Must-have requirements | Requirements Lead with all team members | Agreed set of essential functional requirements for implementation |
| Review AI requirements for the five AI functions | Design/AI Lead | Clear and realistic AI requirements that can be tested during later phases |
| Define fallback behaviour for AI-dependent functions | Development/Testing Lead | Core workflows remain usable when an AI API is unavailable or unreliable |
| Confirm user roles and approval boundaries | Requirements Lead and Project Coordinator | Clear permissions and responsibilities for each stakeholder role |
| Review security and privacy requirements | Development/Testing Lead | Requirements for authentication, role-based access, audit logging, and data minimisation |
| Check third-party licences and selected AI-service terms | Development/Testing Lead | Record of important external dependencies and their usage conditions |
| Review workload and assign later modules | Project Coordinator with all team members | Clear responsibility for design, implementation, testing, and documentation tasks |
| Review Phase 3 work before submission | All team members | Consistent Requirements Document with no missing or conflicting requirements |

The proposed ownership can be mapped to the team's existing roles:

- **Mohammed Alketbi:** Project Coordinator
- **Mohammed Al Ali:** Design and AI Lead
- **Mubarak:** Requirements Lead
- **Abdulla:** Development and Testing Lead

These assignments may be adjusted by the team if responsibilities change during Phase 3.

## 11.4 Scope Reduction Triggers

The team should reduce project scope if continuing with all planned features would put the Must-have requirements or final submission at risk.

Scope reduction should be considered if one or more of the following situations occurs:

- Core Must-have requirements are still unclear after the Phase 3 requirements work.
- The selected AI service cannot be integrated reliably within the available development time.
- Free-tier AI limits prevent sufficient development or testing.
- The synthetic dataset requires significantly more work than expected.
- The team falls behind during the design or implementation phases.
- Major system functions remain unstable close to the testing phase.
- A team member becomes unavailable for an extended period.
- Too much development time is being spent on optional features instead of the core workflows.

If scope reduction becomes necessary, the team should take the following actions in order:

1. Protect all Must-have requirements.
2. Postpone Could-have requirements.
3. Postpone lower-priority Should-have requirements if necessary.
4. Simplify AI functions rather than removing the core classic functionality.
5. Use simpler interfaces or workflows where they still satisfy the required functionality.
6. Focus development and testing on the most important end-to-end workflows.
7. Freeze new features when necessary so that remaining time can be used for integration, testing, documentation, and demonstration.

The project should only continue adding optional functionality when the core system is stable and the Must-have requirements are on schedule.

## 11.5 Final Feasibility Decision

The final recommendation of this feasibility study is **GO, with conditions**.

The project should proceed to Phase 3 because the proposed system can be developed using the available team, tools, project schedule, and prototype resources.

The main conditions are that the team must control the project scope, prioritise Must-have requirements, use suitable synthetic data, validate AI functions early, maintain non-AI fallback options for essential workflows, and keep important decisions under human control.

If these conditions are followed, the project remains suitable for continued development through the remaining software-engineering phases.
