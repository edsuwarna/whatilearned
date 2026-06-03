# 07 — Regional Compliance Standards

Country-specific and regional security frameworks that apply to government, defense, and critical infrastructure.

---

## Essential Eight (Australia)

**Publisher:** Australian Signals Directorate (ASD)

### Overview
The ASD Essential Eight are a set of **mitigation strategies** designed to protect organizations against cyber threats. The most well-known Australian cybersecurity framework.

### Eight Strategies (in priority order)

| # | Strategy | Maturity Level 1 | Maturity Level 2 | Maturity Level 3 |
|---|---|---|---|---|
| 1 | **Application Control** | Block executables by user dir | Block all + MSI/ps | Allowlist only |
| 2 | **Patch Applications** | Patched within 2 months | Within 2 weeks | Within 48 hours |
| 3 | **Configure Microsoft Office Macro Settings** | Block all macros from internet | Block + warn on trusted | Block all Microsoft Office macros |
| 4 | **User Application Hardening** | Block browser plugins | Block web ads | Block Java in browser |
| 5 | **Restrict Administrative Privileges** | Separate admin account | MFA + PIM | Just-in-time access |
| 6 | **Patch OS** | Within 2 months | Within 2 weeks | Within 48 hours |
| 7 | **Multi-Factor Authentication** | MFA for internet-facing | MFA for all remote | MFA for all privileged |
| 8 | **Regular Backups** | Daily, retained 3 months | Offline + isolated | Immutable + tested |

### Maturity Levels
- **Level 1** — Partially aligned (basic)
- **Level 2** — Mostly aligned (good)
- **Level 3** — Fully aligned (strict)

### Relevance
- **Mandatory** for Australian government agencies (non-corporate entities)
- Highly recommended for Australian critical infrastructure
- Practical and action-oriented — unlike large control catalogs

---

## ISM / IRAP (Australia)

**Publisher:** ASD

### Overview
The **Information Security Manual (ISM)** is the comprehensive Australian government security framework. **IRAP** is the certification program that assesses compliance.

### Key Components
| Component | Description |
|---|---|
| **ISM** | 400+ controls across 39 control categories |
| **IRAP** | Assessor program — licensed assessors |
| **PROTECTED** | Security classification for AU gov data |

### IRAP Levels
| Level | Description |
|---|---|
| **Unclassified** | Basic compliance — most common for SaaS |
| **Protected** | Sensitive Australian government data |
| **Secret** | National security data |
| **Top Secret** | Intelligence, often cannot be cloud-hosted |

### Relevance
- Selling to Australian government? You need **IRAP assessment** (typically PROTECTED level)
- Expensive (~$200K+) and time-consuming
- ISM controls are publicly available and well-documented

---

## ISMAP (Japan)

**Publisher:** Government of Japan / IPA

### Overview
**ISMAP (Information System Security Management and Assessment Program)** is Japan's cloud security assessment program, modeled on FedRAMP.

### Requirements
| Area | Detail |
|---|---|
| **Control Baseline** | 271 controls (based on ISO 27001 + NIST SP 800-53) |
| **Assessment** | Third-party audit by registered assessor |
| **Registration** | Listed on ISMAP Cloud Service List |
| **Renewal** | Every 3 years |

### Relevance
- Required for cloud services used by Japanese government agencies
- Important for SaaS companies targeting Japanese enterprise customers
- Similar to FedRAMP in process and cost

---

## My Number Act (Japan)

**Publisher:** Government of Japan

### Overview
Japan's **social security and tax identification system (My Number card)** — equivalent to US SSN. Governs handling of personal identification numbers.

### Key Requirements
- Encryption at rest for My Number data
- Access logging and audit
- Separation from other systems
- Breach notification to authorities

### Relevance
- Companies handling Japanese user tax/social insurance data
- Administrative fines and criminal penalties for mishandling

---

## ANSSI / RGDP (France)

**Publisher:** French National Cybersecurity Agency (ANSSI)

### Overview
**RGDP (Règlement Général de Sécurité)** is France's security framework for critical infrastructure (vital operators).

### Key Documents
| Document | Focus |
|---|---|
| **RGDP** | Security requirements for operators of vital importance (OIV) |
| **ANSSI Guidelines** | Technical guides for specific technologies |
| **Passi** | Security certification for digital trust services |
| **SecNumCloud** | Cloud security qualification (similar to FedRAMP) |

### SecNumCloud
- French cloud certification for government data
- Requires **no extraterritorial jurisdiction** (no US CLOUD Act) — significant challenge for US cloud providers
- Increasingly important for European cloud sovereignty

### Relevance
- French government cloud procurement requires SecNumCloud
- RGDP is mandatory for French critical infrastructure operators

---

## TISAX (EU — Automotive)

**Publisher:** ENX Association (on behalf of VDA)

### Overview
**TISAX (Trusted Information Security Assessment Exchange)** is an automotive industry security standard. Developed by the German Association of the Automotive Industry.

### Assessment Levels

| Level | Assessment | Valid For |
|---|---|---|
| **AL1** | Self-assessment | 3 years |
| **AL2** | Remote audit | 3 years |
| **AL3** | On-site audit | 2 years (must reassess) |

### Key Areas
- Information security (ISO 27001 aligned)
- Prototype protection (unique to auto industry)
- Data protection
- Connections to third parties

### Relevance
- **Required** for suppliers to most European automakers (VW, BMW, Mercedes, Audi)
- Not limited to Europe — global supply chain requirement
- AL2 is typical for Tier 1 suppliers

---

## C5 (Germany)

**Publisher:** BSI (Federal Office for Information Security)

### Overview
**C5 (Cloud Computing Compliance Criteria Catalogue)** — Germany's standard for cloud security, aligned with ISO 27001 + CSA CCM.

### Key Features
| Aspect | Detail |
|---|---|
| **Controls** | ~140 controls in 17 domains |
| **Approach** | Based on ISO 27001 + CSA CCM |
| **Attestation** | Third-party audit report (similar to SOC 2) |
| **Recognition** | Increasingly accepted across EU |

### Relevance
- Required for German government cloud procurement
- Useful as a comprehensive cloud security baseline
- Easier than FedRAMP, comparable to SOC 2

---

## Regional Coverage Map

```
Asia-Pacific:
  🇦🇺 Australia     → Essential Eight + ISM/IRAP
  🇯🇵 Japan         → ISMAP + My Number Act
  🇸🇬 Singapore     → MAS TRM (finance), PDPA (privacy)
  🇮🇳 India         → DPDP Act (privacy), MeitY (cyber)
  🇮🇩 Indonesia     → PDPB / UU PDP (privacy), Kominfo regs

Europe:
  🇪🇺 EU-wide      → GDPR (privacy), NIS2 (cyber), DORA (finance)
  🇫🇷 France       → ANSSI, RGDP, SecNumCloud
  🇩🇪 Germany       → C5 (cloud), BAFIN (finance)
  🇬🇧 UK           → UK GDPR, Cyber Essentials

Americas:
  🇺🇸 US Federal   → FedRAMP (cloud), FISMA/NIST (gov)
  🇺🇸 US States     → CCPA (CA), CPA (CO), etc.
  🇧🇷 Brazil       → LGPD (privacy)

Middle East / Africa:
  🇦🇪 UAE          → NESA (critical infrastructure)
  🇸🇦 Saudi Arabia → NCA (cybersecurity)
  🇿🇦 South Africa → POPIA (privacy)
```

---

*Last updated: June 2026*
