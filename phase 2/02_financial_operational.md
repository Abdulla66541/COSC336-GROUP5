# 9. Legal, Ethical and Policy Constraints

The proposed system must consider legal, security, licensing, university-policy, safety, and ethical constraints. These constraints affect how the system should collect data, control access, use AI services, and support decisions. They do not prevent the development of the prototype, but they must be considered in its design.

## 9.1 Data Privacy

The system may process information relating to university users together with asset, request, transfer, inspection, and maintenance records. Some records could contain personal data such as names, university identifiers, contact information, departments, or records of actions performed by users.

The project must therefore consider the UAE Federal Decree-Law No. 45 of 2021 on the Protection of Personal Data. The law establishes requirements for protecting personal data and maintaining its confidentiality and privacy during processing.

During development and testing, the project will use synthetic data instead of real Khalifa University personal or operational data wherever possible. Synthetic data allows the team to test realistic asset records, requests, transfers, and AI functions without exposing information about real students or staff.

The system should also follow the principle of data minimisation. Only information needed for a particular function should be processed. Personal or confidential information should not be sent unnecessarily to an external AI service.

For example, an AI asset-matching request may require an asset category, description, quantity, condition, technical requirements, and location. It normally would not require the requester's real name, university ID, or contact information.

Khalifa University has a public website privacy policy that describes protection of personal information collected through its website. However, that policy states that it applies to information collected online and should not be treated as the complete internal data-handling policy for this project. A real deployment would therefore require review of the applicable Khalifa University internal privacy, security, and data-handling policies.

**Design response:** use synthetic data during development, minimise personal information, restrict access by role, and avoid sending unnecessary identifiable or confidential information to external AI services.

## 9.2 Security

The system will contain information about assets, users, requests, approvals, transfers, inspections, and maintenance activities. Unauthorized access or modification could result in incorrect records or unauthorized actions.

The system should therefore use role-based access control. Each user should only be able to perform actions that are appropriate for their assigned role. For example, a requester may submit an asset request, while approval of a transfer should be limited to an authorised role.

Important actions should also be recorded in an audit trail. The audit trail should record information such as the user responsible for an action, the action performed, the affected asset or request, and the time of the action.

Authentication information should be protected, passwords should not be stored as plain text, and user input should be validated before it is processed or stored.

**Design response:** implement authentication, role-based permissions, protected credentials, input validation, and audit logging for important system actions.

## 9.3 Intellectual Property and Licensing

The project may use external software libraries, frameworks, databases, AI models, and APIs. These components may have different licences and terms of use.

Before using a third-party component, the team should check its licence and follow any required conditions. The team should also maintain a record of the important external libraries and services used in the project.

The licence applied to the team's own source code does not automatically apply to third-party libraries, models, datasets, or APIs. Each external component remains subject to its own licence or terms.

If the team uses the MIT License for its own repository, the required copyright and licence notice must be retained. The final document should only state that the repository uses the MIT License after the team confirms that the appropriate licence file is actually present in the repository.

If an external AI API is selected, its terms of service, usage limits, permitted uses, and data-handling conditions should be reviewed before integration.

**Design response:** check third-party licences before use, document major dependencies, retain required licence notices, and review the terms of any external AI service used by the project.

## 9.4 Procurement and Asset Ownership Rules

The system should support university asset-management decisions rather than make authorised decisions automatically.

Actions that affect asset ownership, custody, transfer, donation, disposal, or procurement should only be completed by users who have the appropriate authority. An AI recommendation must not automatically cause an asset to be transferred or disposed of.

For example, the system may recommend transferring an unused computer to another department, but the actual transfer should require the appropriate human approval.

The system should also maintain the history of important asset changes, including previous custody, locations, transfers, and approvals. This will help preserve accountability when responsibility for an asset changes.

The exact approval rules used in a real Khalifa University deployment would need to be confirmed against the university's applicable procurement and asset-management policies.

**Design response:** enforce role-based approval permissions, maintain asset history, and require authorised human approval for important asset-management decisions.

## 9.5 Safety Constraints

Some university assets may require inspection or maintenance before they can safely be transferred or reused. This may be particularly important for laboratory equipment, electrical equipment, damaged assets, or equipment that requires calibration.

The system should not assume that an available asset is automatically safe or suitable for reuse. Asset condition, inspection status, maintenance history, and other relevant information should be considered.

Where necessary, the system should allow an asset to be marked as requiring inspection, maintenance, or approval before a transfer is completed.

An AI recommendation must not be treated as proof that physical equipment is safe to use. Safety-sensitive decisions should remain under the control of appropriately qualified personnel.

**Design response:** record condition and inspection information, support maintenance and inspection requirements, and keep safety approval under human control.

## 9.6 Ethical Use of AI

The project includes AI-based resource matching, AI-assisted asset classification, sustainability recommendations, an LLM-powered assistant, and generative AI reporting.

These functions may improve efficiency, but AI-generated results can be inaccurate, incomplete, biased, or difficult to explain. For example, an AI model may misunderstand a departmental request or recommend an asset that is not actually suitable.

AI outputs should therefore be presented as recommendations rather than guaranteed decisions. Where possible, the system should provide supporting information that helps a user understand a recommendation, such as category, condition, quantity, location, technical compatibility, or a similarity score.

Important decisions should remain under human control. AI should not independently approve asset transfers, change ownership or custody, authorise disposal, or make procurement decisions.

Generative reports should also be based on information available in the system. Important figures and conclusions should be traceable to the underlying records rather than being generated without supporting data.

If an AI service is unavailable or produces an unreliable result, essential system functions should continue to operate without depending entirely on AI.

**Design response:** use AI as decision support, maintain human oversight, show supporting information where possible, test AI outputs, and provide non-AI fallback behaviour for essential functions.

## 9.7 Course AI Policy

The development and documentation of the project must follow the AI-use rules stated in the COSC 336 Assessment Details and any additional instructions provided by the instructor or lab engineer.

This document does not assume that a particular use of AI for coursework is permitted or prohibited because the complete Assessment Details policy has not been reproduced here. The team must check the actual course policy and follow any restrictions or disclosure requirements that it contains.

Each team member remains responsible for reviewing, understanding, and being able to explain the work submitted under their name.

The project must also maintain meaningful individual GitHub commits so that each member's contribution and development progress can be identified.

**Design response:** follow the course Assessment Details and instructor instructions, comply with any required AI disclosure or restrictions, maintain clear individual authorship, and ensure that each team member understands their submitted work.
