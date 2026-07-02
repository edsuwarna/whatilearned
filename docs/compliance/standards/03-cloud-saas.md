---
title: 03 — Cloud & SaaS Compliance Standards
description: Security assurance frameworks for cloud service providers, SaaS vendors, and cloud infrastructure.
---

# 03 — Cloud & SaaS Compliance Standards

Security assurance frameworks for cloud service providers, SaaS vendors, and cloud infrastructure.

---

## SOC 2

**Publisher:** AICPA (American Institute of CPAs)

### Overview
SOC 2 (System and Organization Controls) is a **reporting framework** for service organizations handling customer data. It's the most common compliance ask for SaaS companies.

### Trust Service Criteria

| Criterion | What It Covers |
|---|---|
| **Security** | Protected against unauthorized access (firewalls, IDS, access control) |
| **Availability** | System available for operation and use (monitoring, redundancy, DR) |
| **Processing Integrity** | Processing is complete, accurate, timely, and authorized |
| **Confidentiality** | Information designated as confidential is protected (encryption) |
| **Privacy** | Personal info is collected, used, retained, disclosed in accordance with commitments |

Most orgs report on **Security alone** (Type II). Full criteria are common for B2B SaaS.

### Type I vs Type II

| Type | What It Tests | Duration |
|---|---|---|
| **Type I** | Design of controls at a point in time | Snapshot |
| **Type II** | Operating effectiveness over time | 6–12 months |

### Certification
- Not a "certification" — it's an **audit report** issued by a licensed CPA firm
- Report is valid for 12 months
- Customer receives the report (NDA-bound) — not publicly listed

### Relevance
- **Standard requirement** for B2B SaaS (customers will ask)
- Pairs well with ISO 27001 (ISMS) — SOC 2 covers what ISO 27001 doesn't (availability, processing integrity)
- For startups: start with Security-only Type II

---

## FedRAMP

**Publisher:** US General Services Administration (GSA), Joint Authorization Board

### Overview
A US government program that provides a **standardized approach** to security assessment, authorization, and continuous monitoring for cloud services used by federal agencies.

### Impact Levels

| Level | Data Types | Examples | Requirements |
|---|---|---|---|
| **Low** | Public, non-critical | Govt websites | 125 controls (baseline) |
| **Moderate** | Sensitive but not classified | Financial, legal | 325 controls |
| **High** | Mission-critical | Emergency services, law enforcement | 421 controls |

### Authorization Process

```
Readiness Assessment (RAR) ──→ Provisional Authorization (P-ATO)
     ↘                                              ↘
   Agency-specific Auth (Leveraged)             Full FedRAMP
```

### Key Requirements
- **Continuous Monitoring** — monthly scans, annual assessments
- **Third-Party Assessment Organization (3PAO)** — licensed auditor
- **Plan of Action & Milestones (POA&M)** — remediation tracking
- **Incident Response** — report to US-CERT within 1 hour

### Relevance
- **Mandatory** for selling cloud services to US federal agencies
- Expensive ($500K–$2M+ for Moderate) and time-consuming (12–18 months)
- FedRAMP-equivalent programs exist in other countries

---

## CSA STAR

**Publisher:** Cloud Security Alliance

### Overview
The **Security, Trust, Assurance, and Risk (STAR)** program provides three levels of cloud assurance:

| Level | Type | Description |
|---|---|---|
| **Level 1** | Self-assessment | Free, based on CSA Cloud Controls Matrix (CCM) |
| **Level 2** | Third-party audit | Based on CSA CCM + ISO 27001 |
| **Level 3** | Continuous monitoring | Automated, real-time assurance |

### Cloud Controls Matrix (CCM)
A meta-framework mapping **cloud controls** across 17 domains (application security, encryption, IAM, incident response, etc.) mapped to ISO 27001, PCI DSS, NIST, HIPAA, and others.

### Relevance
- Level 1 is free — good starting point for cloud security posture
- Level 2 builds on ISO 27001 audit (cost-effective)
- CCM is useful as a **cross-reference** — see how your controls map to multiple frameworks

---

## CIS Cloud Benchmarks

**Publisher:** Center for Internet Security (CIS)

### Supported Platforms
AWS, Microsoft Azure, Google Cloud Platform (GCP), Oracle Cloud (OCI), Alibaba Cloud.

### Key Areas Checked
| Domain | AWS Example | Azure Example | GCP Example |
|---|---|---|---|
| Identity & Access | IAM users, roles, policies | RBAC, MFA, service principals | IAM, service accounts |
| Storage | S3 public access, encryption | Blob storage, key vault | Cloud Storage, KMS |
| Networking | Security groups, VPC flow | NSG, network watcher | VPC, firewall rules |
| Logging | CloudTrail, Config | Azure Monitor, Sentinel | Cloud Logging |
| Database | RDS encryption, backup | SQL auditing, TDE | Cloud SQL, Spanner |
| Compute | EC2 IMDS, AMI | VM disk encryption | GCE, shielded VMs |

### Relevance
- **Most practical** for day-to-day cloud configuration auditing
- Tools like Prowler, ScoutSuite, and custom scanners implement these
- Freely available and regularly updated

---

## Comparison

| Framework | Cost | Difficulty | Best For |
|---|---|---|---|
| **SOC 2** | $50K–$150K | Medium | B2B SaaS companies |
| **FedRAMP** | $500K–$2M+ | Very High | US federal cloud providers |
| **CSA STAR** | Free–$50K | Low–Medium | Cloud assurance, cross-framework mapping |
| **CIS Cloud** | Free | Low | DevOps/platform engineering teams |

---

*Last updated: June 2026*
