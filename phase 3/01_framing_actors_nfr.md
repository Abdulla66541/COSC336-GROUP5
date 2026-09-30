# Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System

## Phase 3 – Requirements Document

**Khalifa University – Department of Computer Science**

**COSC 336 – Introduction to Software Engineering – Fall 2026**

**Prepared by:** Group 5 – Mohammed Alketbi (100067035), Abdulla, Mohammed Al Ali, Mubarak

**Prepared for:** Eng. Dina Atia, Lab Instructor

**Date:** October 2026


---

# 1. Introduction

## 1.1 Purpose

Phase 1 described the problem and Phase 2 showed that solving it is feasible. This document says exactly what the system shall do. It turns the ideas from the earlier phases into numbered, testable requirements that the design team can build against (Phases 4–5), the developers can implement (Phase 6) and the testers can verify (Phase 7). If a feature is not written here, it is not promised. If it is written here, it can be checked.

The document covers the whole prototype: the classic asset-management layer and the AI-enhanced layer.

## 1.2 Document Conventions

- **Identifiers.** Every item has a unique ID: `FR-<AREA>-nn` for functional requirements (for example `FR-AST-03` is the third asset-registration requirement), `NFR-nn` for non-functional requirements, `BR-nn` for business rules and `UC-nn` for use cases.
- **Wording.** "Shall" marks a mandatory requirement, "should" a desirable one and "may" an option.
- **Priority.** Every requirement is rated Essential (must be included in the prototype), Desirable (to be implemented if time permits) or Future (listed but not implemented). All priorities are described in Section 8.
- **Testable**: Each requirement describes exactly one testable thing. If a limit is relevant, it is stated numerically and not verbally (e.g., quickly).
- **Roles**: Roles are abbreviated in the permission matrix (Section 2.4). Definitions are provided in Appendix A.
