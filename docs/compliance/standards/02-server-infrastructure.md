---
title: 02 — Server & Infrastructure Security Standards
description: Hardening guidelines and security controls for operating systems, servers, and network devices.
---

# 02 — Server & Infrastructure Security Standards

Hardening guidelines and security controls for operating systems, servers, and network devices.

---

## CIS Benchmarks

**Publisher:** Center for Internet Security (CIS)

### Overview
CIS Benchmarks are **prescriptive configuration guidelines** for hardening systems. They cover 100+ technologies: OS (Linux, Windows, macOS), cloud (AWS, Azure, GCP), containers (Docker, K8s), databases (MySQL, PostgreSQL, MongoDB), and network devices (Cisco, Palo Alto).

### Key Concepts

| Term | Meaning |
|---|---|
| **Level 1 (L1)** | Essential security — easy to implement, minimal disruption |
| **Level 2 (L2)** | Defense-in-depth — may impact operations, requires planning |
| **CIS Controls v8** | 18 overarching controls (not a benchmark — a program) |
| **CIS-CAT** | Tool to assess compliance against benchmarks |

### Scoring
Each check = PASS or FAIL. Score is percentage passing. Many tools (CIS-CAT, Prowler, custom scanners) implement this.

### Relevance
- **Most practical framework** for day-to-day server hardening
- L1 = immediate wins with no breakage
- The compliance scanner in Anjungan uses CIS Benchmarks as its primary reference

---

## NIST SP 800-53

**Publisher:** National Institute of Standards and Technology (US)

### Overview
A catalog of **1,000+ security and privacy controls** for US federal information systems. The gold standard for comprehensive control coverage.

### Control Families (20)

| ID | Family | Example |
|---|---|---|
| AC | Access Control | Least privilege, separation of duties |
| AT | Awareness & Training | Security training |
| AU | Audit & Accountability | Log generation, audit review |
| CM | Configuration Management | Baseline config, change control |
| IA | Identification & Authentication | MFA, password policy |
| IR | Incident Response | Training, testing, monitoring |
| MA | Maintenance | Remote maintenance |
| MP | Media Protection | Encryption at rest |
| PE | Physical & Environmental | Facility controls |
| PL | Planning | System security plan |
| PS | Personnel Security | Background checks |
| RA | Risk Assessment | Vulnerability scanning |
| SA | System & Services Acquisition | Supply chain risk |
| SC | System & Communications Protection | Encryption, boundary protection |
| SI | System & Information Integrity | Malware protection, system monitoring |
| RA, CA, CP, PM, SA, SR | (additional families) | |

### Relationship to Other Frameworks

```
CIS Benchmarks → cover ~20% of SP 800-53 (config-focused)
ISO 27001     → maps to ~60% of SP 800-53 (ISMS-focused)
NIST CSF      → high-level version of SP 800-53
```
SP 800-53 is the **implementation** detail behind NIST CSF.

### Relevance
- **Mandatory** for US federal contractors (FISMA)
- Overkill for most commercial orgs — pick relevant control families
- Best used as a **control library** to map your existing controls against

---

## STIG (Security Technical Implementation Guide)

**Publisher:** DISA (Defense Information Systems Agency), US DoD

### Overview
Military-grade hardening guides for specific software/OS versions (e.g., "RHEL 9 STIG", "Windows Server 2022 STIG"). More strict than CIS Benchmarks.

### Key Differences from CIS

| Aspect | CIS L1 | CIS L2 | STIG |
|---|---|---|---|
| **Strictness** | Moderate | High | Very High |
| **Operational Impact** | None | Some | Significant |
| **Audience** | General | Security-conscious | Military/Government |
| **PKI/Auth** | Optional CA | Recommends | **Requires** CAC/PKI |
| **Logging** | Basic | Good | Comprehensive |

### Example: SSH Differences

| Setting | CIS Level 1 | STIG |
|---|---|---|
| `PermitRootLogin` | No | No + audit |
| `Ciphers` | Any strong | FIPS 140-2 validated only |
| `MACs` | Any strong | FIPS-only |
| `ClientAliveInterval` | 300 (5 min) | 600 (suggested) |

### Relevance
- **If you contract with US DoD**, STIG is mandatory
- Otherwise, CIS is usually sufficient
- STIG can break things — test in staging first

---

## NSA Hardening Guides

**Publisher:** National Security Agency (US)

### Overview
NSA publishes hardening guides for common systems. They are shorter and more focused than STIG or CIS.

### Notable Guides
- **NSA Kubernetes Hardening** — 5 steps (images, RBAC, network policies, secrets, audit)
- **NSA Android / iOS** — mobile device hardening
- **NSA DNS Security** — preventing DNS hijacking and tunneling

### Relevance
- NSA K8s guide is excellent — practical and concise
- Good supplement to CIS K8s Benchmark
- NSA guides are free and easy to digest

---

## Comparison: Choosing a Hardening Standard

| Your Situation | Use |
|---|---|
| Standard Linux server | CIS Level 1 + Level 2 (selectively) |
| Public-facing web server | CIS Level 2 |
| PCI-DSS compliant | CIS Level 1 + PCI-specific controls |
| US Federal contractor | NIST SP 800-53 + STIG |
| DoD/Military | STIG + NIST SP 800-53 |
| Kubernetes | CIS K8s Benchmark + NSA K8s |
| Quick wins, small team | CIS Level 1 (most impactful per effort) |

---

*Last updated: June 2026*
