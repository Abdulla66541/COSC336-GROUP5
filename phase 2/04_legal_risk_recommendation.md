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

The development and documentation of the project must follow the AI-use rules stated in the COSC 336 Assessment Details and any additional instructions provided by the instructor or lab engineer.

The team will follow any permissions, restrictions, or disclosure requirements stated in the course policy when using AI tools for project development or documentation.

Each team member remains responsible for reviewing, understanding, and being able to explain the work submitted under their name.

**Design response:** follow the COSC 336 Assessment Details and instructor instructions, comply with any required AI-use restrictions or disclosure requirements, and ensure that each team member understands their submitted contribution.

## 9.8 Feasibility Conclusion

The identified legal, ethical, policy, security, licensing, and safety constraints do not prevent development of the proposed prototype.

The project is considered feasible provided that synthetic data is used during development where possible, personal information is minimised, external AI services are used carefully, third-party licences and terms are respected, role-based permissions are enforced, and important asset-management decisions remain under authorised human control.

A future deployment using real Khalifa University systems or operational data would require additional review of the university's applicable internal privacy, security, procurement, asset-management, and safety requirements.
