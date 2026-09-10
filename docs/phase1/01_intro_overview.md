# Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System

## Phase 1 -Initial Plan and Requirement Gathering Document

**Khalifa University -Department of Computer Science**

**COSC 336-Introduction to Software Engineering-Fall2026**

**Prepared by:** Group 5 – Mohammed Alketbi, Abdulla, Mohammed Al Ali, Mubarak

**Prepared for:** Eng. Dina Atia, Lab Instructor

**Date:** September 2026



---

# 1. Introduction

## 1.1 Project Concept

Imagine a lab in one building throwing away twenty working monitors, while a department in the next building is filling out a purchase order for twenty new ones. Nobody did anything wrong; they simply had no way of knowing about each other. This happens across universities every year with furniture, computers, lab equipment, books and office supplies. The resources exist, but the connection between the people who have them and the people who need them does not.

Our project is that connection. We propose an internal web platform for Khalifa University that follows every campus asset through its whole life: from the day it is registered, through use, transfer, maintenance and repair, to the day it is finally donated, recycled or retired. The system is built in two layers.

The **classic layer** is the solid foundation: an asset register, a marketplace where departments publish surplus or unused items, a way for other departments to search, request and reserve them, approval and transfer workflows, maintenance and inspection records, and user accounts with clearly defined roles and permissions. This layer is rule-based, predictable and transparent.

The **AI layer** makes the foundation smart. It matches available assets to departmental requests by meaning rather than exact keywords, so a request for "laboratory seating" can find an item listed as "lab bench stool". It suggests categories and tags when a new asset is registered, recommends the most sustainable action for an asset (reuse, transfer, repair, donate, recycle or retire), lets users search and ask questions in plain language through an LLM assistant, and generates readable reports on savings, waste diverted and estimated carbon reductions.

The guiding idea is the circular economy: keep resources in use for as long as possible and recover their value at the end. In practice, before any department buys something new, the system should be able to answer one simple question: *does this already exist somewhere on campus?*

## 1.2 Purpose of this Document

This document is the Phase 1 deliverable of the COSC 336 running project: Planning and Requirement Gathering. Before we design or build anything, the team and the client need to agree on what problem we are solving, for whom, and what "done" looks like. This document records that agreement.

Specifically, it:

- defines the problem, scope, objectives, assumptions and expected benefits of the system;
- identifies all stakeholders and maps each one to the features they use, the data they need, their permissions, their responsibilities and the approval decisions they make;
- describes how surplus assets, requests, transfers, maintenance and disposal are handled today, without the system;
- explains how we gathered requirements, summarises and prioritises them, and presents an initial requirements specification;
- defines measurable success criteria so that we can judge the project objectively at the end; and
- presents a preliminary project plan covering the timeline, milestones, methodology, team roles, dependencies, risks and resources for the remaining seven phases.

The intended readers are the lab instructor and course instructor, who act as the client, and the four members of Group 5, who act as the development team. This document is the baseline for the Feasibility Study in Phase 2 and the detailed Requirements Analysis in Phase 3, and it will be updated as our understanding of the problem improves.
