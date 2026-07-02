---
title: 01 — Governance & Risk Frameworks
description: IT governance, risk management, and audit standards for managing technology at the organizational level.
---

# 01 — Governance & Risk Frameworks

IT governance, risk management, and audit standards for managing technology at the organizational level.

---

## ISO 27001

**Publisher:** International Organization for Standardization (ISO)

### Overview
The most widely recognized **Information Security Management System (ISMS)** standard. Specifies requirements to establish, implement, maintain, and continually improve an ISMS.

### Scope
Entire organization — not just IT. Covers people, process, technology, physical security, and third parties.

### Key Components (Annex A — 93 Controls, 4 Domains)

| Domain | Controls | Examples |
|---|---|---|
| **Organizational** | A.5 (37) | Policy, roles, supplier security, threat intel |
| **People** | A.6 (8) | Screening, training, confidentiality |
| **Physical** | A.7 (14) | Secure areas, equipment, clear desk |
| **Technological** | A.8 (34) | Access control, cryptography, logging, network |

### Certification
- Third-party audit by accredited certification body (BSI, DNV, etc.)
- Surveillance audits annually
- Recertification every 3 years
- Most orgs spend 6–12 months preparing

### Relevance
- **Essential** if you need formal security certification
- Often required for B2B contracts, government tenders
- Provides a strong ISMS backbone that other frameworks (PCI, SOC 2) can sit on top of

---

## ISO 27002

**Publisher:** ISO

### Overview
A **reference document** containing detailed implementation guidance for the 93 controls listed in ISO 27001 Annex A. Not certifiable on its own — used alongside ISO 27001.

### Key Difference
- ISO 27001: *What* you must do (requirements + certifiable)
- ISO 27002: *How* to do it (guidelines)

---

## COBIT 2019

**Publisher:** ISACA

### Overview
A governance framework for **enterprise IT**. Bridges the gap between business goals and IT capabilities through a set of 40 management and governance objectives.

### Key Concepts

| Component | Description |
|---|---|
| **Governance Objectives** | Evaluate, Direct, Monitor (EDM) |
| **Management Objectives** | Align, Plan, Organize (APO) — Build, Acquire, Implement (BAI) — Deliver, Service, Support (DSS) — Monitor, Evaluate, Assess (MEA) |
| **Design Factors** | Strategy, enterprise size, risk profile, technology adoption |
| **Capability Levels** | 0 (Incomplete) to 5 (Optimizing) |

### Relevance
- Useful for **organizations with complex IT governance needs**
- Complements ISO 27001 for the governance layer
- Provides KPIs and maturity metrics that ISO 27001 doesn't

---

## ITIL

**Publisher:** Axelos

### Overview
ITIL (Information Technology Infrastructure Library) is a set of **IT Service Management (ITSM)** best practices. The current version is ITIL 4, organized around the **Service Value System (SVS)**.

### Key Components (ITIL 4)

| Component | Description |
|---|---|
| **Service Value Chain** | Plan → Improve → Engage → Design & Transition → Obtain/Build → Deliver & Support |
| **34 Practices** | Incident mgmt, problem mgmt, change mgmt, service desk, etc. |
| **4 Dimensions** | Organizations & people, info & tech, partners & suppliers, value streams & processes |

### Relevance
- **Not a security framework** — focuses on service delivery and operations
- Complements compliance by ensuring **operational discipline** (incident response, change management, problem management)
- Often used alongside ISO 20000 (service management certification)

---

## SOX (Sarbanes-Oxley Act)

**Publisher:** US Securities and Exchange Commission (SEC)

### Overview
US federal law enacted in 2002 in response to Enron/WorldCom. Requires **financial reporting controls**, including IT General Controls (ITGC).

### ITGC Controls That Matter

| Domain | What SOX Checks |
|---|---|
| **Access Management** | User provisioning, termination, privileged access, segregation of duties |
| **Change Management** | Code promotion, change approval, emergency change process |
| **Computer Operations** | Batch job monitoring, backup/restore, incident handling |
| **Program Development** | SDLC controls, testing, QA sign-off |

### Relevance
- **Mandatory** for any US publicly traded company
- Private companies preparing for IPO should adopt early
- ITGC controls overlap heavily with ISO 27001/CIS — implementing those first simplifies SOX readiness

---

## Framework Relationships

```
┌─────────────────────────────────────────────────┐
│                 COBIT 2019                       │
│           (Governance — WHY)                     │
├─────────────────────────────────────────────────┤
│            ISO 27001 (ISMS)                      │
│         (Management — WHAT)                      │
├──────────────────┬──────────────────────────────┤
│   ITIL (ITSM)    │   SOX (Financial)            │
│   (Operations)   │   (Accountability)            │
└──────────────────┴──────────────────────────────┘
```

---

*Last updated: June 2026*
