# 05 — Healthcare & Privacy Compliance Standards

Frameworks for protecting personal data — health information, consumer privacy, and cross-border data transfers.

---

## HIPAA

**Publisher:** US Department of Health and Human Services (HHS)

### Overview
The **Health Insurance Portability and Accountability Act (HIPAA)** of 1996. Protects Protected Health Information (PHI) — any individually identifiable health data.

### Who Must Comply
- **Covered Entities**: Healthcare providers, health plans, healthcare clearinghouses
- **Business Associates**: Anyone handling PHI on behalf of a covered entity (cloud hosting, billing, analytics)

### Three Rules

| Rule | What It Requires |
|---|---|
| **Privacy Rule** | Use/disclosure limits, patient rights (access, amendment, accounting), minimum necessary |
| **Security Rule** | Administrative, physical, and technical safeguards for ePHI |
| **Breach Notification Rule** | Notify affected individuals + HHS (60 days), media if 500+ |

### Security Rule Safeguards

| Category | Examples |
|---|---|
| **Administrative** (9 standards) | Risk analysis, workforce training, contingency plan, incident response |
| **Physical** (4 standards) | Facility access, workstation security, device/media control |
| **Technical** (5 standards) | Access control (unique IDs, auto-logoff, encryption), audit controls, integrity, transmission security |

### Enforcement
- HHS Office for Civil Rights (OCR)
- Penalties: $100–$50K+ per violation, up to $1.5M/year per category
- **Criminal penalties** for knowingly obtaining/disclosing PHI

### Relevance
- **Mandatory** for US healthcare organizations and their vendors
- HIPAA-only audits are rare — most organizations use HITRUST to simplify

---

## HITRUST CSF

**Publisher:** HITRUST Alliance

### Overview
A **certifiable framework** that integrates HIPAA, ISO 27001, NIST, PCI, and other standards into a single assessment. Very common in US healthcare.

### Why HITRUST Instead of Plain HIPAA

| Aspect | Raw HIPAA | HITRUST CSF |
|---|---|---|
| **Specificity** | Vague ("encryption addressable") | Explicit control requirements |
| **Audit** | Self-assessment typical | Third-party validated |
| **Scope** | Just HIPAA | HIPAA + ISO + NIST + PCI |
| **Certification** | None | r2 (Validated Assessment) |
| **Accepted by** | HHS | Multiple healthcare orgs |

### Assessment Types
| Assessment | Depth | Use Case |
|---|---|---|
| **e1** | 100+ controls | Basic self-assessment |
| **r2** | 200+ controls | Third-party validated — most common |
| **CSF** | 400+ controls | Full certification |

### Relevance
- **Gold standard** for healthcare security in the US
- Alternative to ISO 27001 for healthcare orgs (combines both)
- Expensive ($50K–$100K+) but reduces audit fatigue

---

## GDPR

**Publisher:** European Union

### Overview
The **General Data Protection Regulation (GDPR)** is an EU regulation governing the processing of personal data of individuals in the EU/EEA. Applies to **any organization** worldwide that processes EU citizen data.

### Key Principles

| Principle | Meaning |
|---|---|
| **Lawfulness, Fairness, Transparency** | Clear privacy notices, consent where needed |
| **Purpose Limitation** | Collect data only for specified, explicit purposes |
| **Data Minimization** | Collect only what's necessary |
| **Accuracy** | Keep data accurate and up to date |
| **Storage Limitation** | Delete when no longer needed |
| **Integrity & Confidentiality** | Security measures (Article 32) |
| **Accountability** | Demonstrate compliance (records, DPO, DPIAs) |

### Key Rights (for Data Subjects)

| Right | Description |
|---|---|
| **Right to be Informed** | Privacy notice at collection |
| **Right of Access** | Get copy of all personal data (30 days) |
| **Right to Rectification** | Correct inaccurate data |
| **Right to Erasure** ("Right to be Forgotten") | Delete data on request |
| **Right to Restrict Processing** | Temporarily stop processing |
| **Right to Data Portability** | Download data in machine-readable format |
| **Right to Object** | Opt out of marketing, profiling |
| **Automated Decision-Making** | Right to human review |

### Fines
- **Up to €20M or 4% of global annual turnover** (whichever is higher)
- Two-tier system: standard violations (€10M/2%) vs serious (€20M/4%)

### DPO Requirement
- Organizations with **large-scale systematic monitoring** or **special categories of data** must appoint a Data Protection Officer

### Relevance
- **Mandatory** if you have EU users — no threshold (even 1 user counts)
- Privacy notices, cookie consent, data processing records are table stakes
- Non-compliance is expensive — but enforcement is complaint-driven

---

## CCPA / CPRA

**Publisher:** State of California, USA

### Overview
The **California Consumer Privacy Act** (2018) + **California Privacy Rights Act** (2023 amendment). Often called the "California GDPR."

### Key Similarities to GDPR
- Right to know, delete, opt out
- Data minimization
- Contractual requirements with service providers

### Key Differences from GDPR

| Aspect | GDPR | CCPA/CPRA |
|---|---|---|
| **Threshold** | Any EU resident data | California residents + $25M revenue / 100K records / 50% revenue from data sale |
| **Opt-in vs Opt-out** | Opt-in consent required | Opt-out of data **sale** (Do Not Sell) |
| **Enforcement** | DPA | California Privacy Protection Agency (CPPA) |
| **Private right of action** | No (except processors) | Yes — data breach only ($100–$750 per incident) |

### Relevance
- If you do business in California, you likely need a CCPA-compliant privacy policy
- Influenced privacy laws in other US states (Virginia, Colorado, Connecticut, Utah, Texas)

---

## PDPB (UU PDP Indonesia)

**Publisher:** Government of Indonesia

### Overview
The **Personal Data Protection Act (UU No. 27/2022)** — Indonesia's first comprehensive data protection law. Came into full effect October 2024.

### Key Requirements

| Requirement | Detail |
|---|---|
| **Consent** | Explicit, specific, freely given |
| **Purpose Limitation** | Must specify purpose at collection |
| **Data Subject Rights** | Access, correction, deletion, portability, objection |
| **DPO Appointment** | Required for large-scale processing |
| **Cross-Border Transfer** | Adequacy assessment or contractual safeguards |
| **Breach Notification** | Max 3 days (72 hours) — strictest globally |
| **Data Retention** | Deletion when purpose ends |
| **PIA (DPIA)** | Required for high-risk processing |

### Fines
- **Up to 6% of annual revenue** (higher than GDPR's 4%)
- Criminal penalties for intentional violations

### Key Differences from GDPR

| Aspect | GDPR | PDPB |
|---|---|---|
| **Breach notification** | 72 hours | 3 × **24** hours (same: 72h) |
| **Max fine** | 4% revenue / €20M | 6% revenue |
| **Criminal penalty** | No | Yes (intentional data misuse) |
| **Cross-border** | Adequacy + SCCs | Adequacy or contracts |
| **DPO** | Some orgs | Broad criteria |

### Relevance
- **Mandatory** for any organization processing Indonesian citizen data
- Applies to foreign entities targeting Indonesian users
- Enforcement agency (PDPB) still being fully operationalized

---

## Global Privacy Landscape

```
GDPR (EU) ────────→ EDPB guidelines ──────→ Influences LGPD (Brazil)
     │                                        └── Influences PDPB (Indonesia)
     │                                        └── Influences DPDP (India)
     ├──→ UK GDPR (post-Brexit, near-identical)
     └──→ CCPA/CPRA (California) ───→ Other US states (VA, CO, CT, UT, TX)
```

---

*Last updated: June 2026*
