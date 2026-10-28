# Phase 4 & 5 – Part 4: AI Layer and Sustainability

**Owner:** Abdulla

**Use cases:** UC-26 to UC-35

**Requirement groups:** FR-AI-01 to FR-AI-70, FR-AI-X-01 to FR-AI-X-17, FR-SUS-01 to FR-SUS-31

**Data stores:** D10 AI Output Log, D11 Sustainability Records

**Tables:** AI_OUTPUT, AI_OVERRIDE, AI_FEEDBACK, REUSE_EVENT, EMISSION_FACTOR

Shared architecture and common AI integration path:

**Service → AI Facade → Privacy Filter → AI Adapter → AI Service → Answer Checker → AI Output Log**

All AI use cases follow this common path unless a fallback or alternative flow is triggered.

# 1. Data Flow Diagrams, Level 1
## 1.1 Process 6.0 – Run AI Functions

```mermaid
flowchart LR

AC[Asset Custodian]
RQ[Requester]
SO[Sustainability Officer]
MS[Maintenance Staff]
AD[Administrator]
U[Any User]
AI[AI Service]

P61[6.1 Classify Asset]
P62[6.2 Match and Rank Assets]
P63[6.3 Recommend Sustainable Action]
P64[6.4 Answer Question]
P65[6.5 Draft AI Report]
P66[6.6 Detect Duplicate Listings]
P67[6.7 Predict Maintenance Need]
P68[6.8 Record Override and Feedback]

D2[D2 Assets]
D4[D4 Listings]
D5[D5 Requests and Reservations]
D8[D8 Maintenance Records]
D10[D10 AI Output Log]
D11[D11 Sustainability Records]
D12[D12 Reports]

P2[2.0 Manage Assets]
P3[3.0 Marketplace and Requests]

P2 -->|Classification request| P61
P61 -->|AI request| AI
AI -->|AI result and confidence| P61
P61 -->|Category suggestion| P2
P61 -->|AI output| D10

P3 -->|Match request| P62
D4 -->|Active listings| P62
P62 -->|AI request| AI
AI -->|AI result and confidence| P62
P62 -->|Ranked matches| P3
RQ -->|Match review| P62
P62 -->|AI output| D10

D2 -->|Asset condition and history| P63
D8 -->|Repair history| P63
P63 -->|AI request| AI
AI -->|AI result and confidence| P63
P63 -->|Recommendation| SO
SO -->|Recommendation review| P63
P63 -->|AI output| D10

U -->|Question| P64
D2 -->|Asset data| P64
D5 -->|Request data| P64
P64 -->|AI request| AI
AI -->|AI result and confidence| P64
P64 -->|Answer| U
P64 -->|AI output| D10

D11 -->|Sustainability figures| P65
D5 -->|Request summary| P65
D8 -->|Maintenance trends| P65
P65 -->|AI request| AI
AI -->|AI result and confidence| P65
P65 -->|Draft report| AD
AD -->|Report review| P65
P65 -->|Reviewed report| D12
P65 -->|AI output| D10

AC -->|New listing data| P66
D4 -->|Active listings| P66
P66 -->|AI request| AI
AI -->|AI result and confidence| P66
P66 -->|Duplicate warning| AC

D8 -->|Maintenance history| P67
D2 -->|Asset age and condition| P67
P67 -->|AI request| AI
AI -->|AI result and confidence| P67
P67 -->|Risk list| MS
P67 -->|AI output| D10

AC -->|Override and reason| P68
AD -->|Override and reason| P68
U -->|Feedback| P68
D10 -->|Previous AI output| P68
P68 -->|Override and feedback| D10
```
