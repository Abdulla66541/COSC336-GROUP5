# Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System

## Phase 2 – Feasibility Document

**Khalifa University – Department of Computer Science**

**COSC 336 – Introduction to Software Engineering – Fall 2026**

**Prepared by:** Group 5 – Mohammed Alketbi (100067035), Abdulla, Mohammed Al Ali, Mubarak

**Prepared for:** Eng. Dina Atia, Lab Instructor

**Date:** September 2026

**Version:** 0.1 (Draft)

---

# 1. Introduction

## 1.1 Purpose of this Study

Phase 1 defined what we want to build. This document asks a different question: can we actually build it, with four students, one semester, no budget and no access to real university data — and is it worth building at all?

A feasibility study exists to support a go/no-go decision before serious design and development effort is committed. It examines the project from several angles — market, technical, financial, operational, schedule, data and AI, and legal — and for each one asks whether the project is achievable and under what conditions. The output is a recommendation, not a description.

## 1.2 Project Recap

The proposed system is an internal web platform for Khalifa University that registers campus assets, publishes surplus items to an internal marketplace, lets departments request and reserve them, manages approvals and transfers, records the full life cycle of each asset, and adds an AI layer for semantic matching, classification, sustainability recommendations, a natural-language assistant and generated reports. The full scope, stakeholders and initial requirements are in the Phase 1 document (`docs/phase1/Phase1_Final.md`) and are not repeated here.

## 1.3 How this Document is Organised

Sections 2 and 3 set the context (stakeholders and existing solutions). Sections 4 to 9 assess feasibility dimension by dimension: technical, financial, operational, schedule, data and AI, and legal/policy. Section 10 consolidates the risks, and Section 11 gives the recommendation and the action plan for Phase 3.

# 2. Stakeholder Summary

Phase 1 identified eleven stakeholder groups and mapped them to features, data and permissions. For the feasibility study, what matters is each group's main interest and the condition under which the system is feasible *for them*.

| Stakeholder | Main interest | Feasibility condition |
|---|---|---|
| Department representatives | Get needed equipment quickly without a purchase request | Search and request must be faster than emailing procurement |
| Asset custodians | Keep records accurate with minimal extra work | Registration must be quick; AI classification must reduce typing, not add review burden |
| Requesters | Find items that fit their need | Matching must return relevant results, not noise |
| Administrators | Clear, auditable approvals | Approval rules must be explicit and enforced by the system, not by AI |
| Procurement officers | Avoid unnecessary purchases | Surplus must be visible at the moment a purchase is considered |
| Finance officers | Trustworthy savings figures | Every estimate must show its assumption |
| Maintenance staff | One place for repair history | History must follow the asset across transfers |
| Sustainability officers | Reportable indicators | Waste-diversion and CO₂ estimates must be explainable and labelled as estimates |
| System administrators | Security and low maintenance | Standard stack, role-based access, audit log |
| Instructors (client) | Evidence of process and learning | Regular commits, documented decisions, honest limitations |
| Group 5 (developers) | Deliverable within the semester | Scope limited to Must requirements; free tools only |

The common thread is that feasibility depends less on technology and more on keeping the workflow simpler than the current informal process. If using the system takes longer than sending an email, nobody will use it.
