---
title: 07 — Regional Compliance Standards
description: Country-specific and regional security frameworks that apply to government, defense, and critical infrastructure.
---

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

## European Union

### NIS2 Directive

**Publisher:** European Union

### Overview
The **Network and Information Security (NIS2) Directive** is the updated EU cybersecurity regulation, replacing the original NIS Directive (2016). EU member states must transpose NIS2 into national law by October 2024.

### Scope
NIS2 applies to **essential and important entities** in 15+ sectors:

| Category | Sectors |
|---|---|
| **Essential** | Energy, Transport, Banking, Health, Water, Digital Infrastructure |
| **Important** | Postal, Waste, Chemicals, Food, Manufacturing, Digital Providers |

### Key Requirements
| Requirement | Detail |
|---|---|
| **Cybersecurity Risk Management** | Risk assessments, incident response, business continuity |
| **Supply Chain Security** | Assess security of direct suppliers and service providers |
| **Incident Reporting** | Early warning (24h), notification (72h), final report (1 month) |
| **Crisis Management** | National CSIRTs, EU-CyCLONe for large-scale incidents |
| **Penalties** | Essential: up to €10M / 2% revenue; Important: up to €7M / 1.4% revenue |
| **Management Accountability** | Senior management can be held personally liable |
| **Audit & Enforcement** | Regular audits, binding instructions |

### Relevance
- **Mandatory** for organizations in covered sectors with 50+ employees
- Organizations under DORA (financial services) are exempt from NIS2
- Penalties include **personal liability for C-suite**
- Supply chain requirements mean even non-covered orgs may need to comply

---

### DORA (EU — Finance)

**Publisher:** European Union

### Overview
The **Digital Operational Resilience Act (DORA)** is an EU regulation for the financial sector. Effective January 2025. Requires financial entities and their **ICT third-party providers** (including cloud vendors) to demonstrate operational resilience.

### Key Requirements
| Requirement | Detail |
|---|---|
| **ICT Risk Management** | Framework, identification, protection, detection, response, recovery |
| **Incident Reporting** | Report major ICT incidents to competent authority |
| **Digital Operational Resilience Testing** | Threat-led penetration testing (TLPT) every 3 years |
| **ICT Third-Party Risk** | Register of all ICT providers, contractual clauses, exit strategy |
| **Information Sharing** | Threat intelligence sharing arrangements |

### Oversight Framework
DORA creates an **Oversight Framework** for critical ICT third-party providers (CTPPs) — including cloud providers like AWS, Azure, GCP. The European Supervisory Authorities (ESAs) can:
- Request access to premises and data
- Conduct audits and inspections
- Impose fines up to 1% of daily worldwide turnover

### Relevance
- **Mandatory** for EU financial institutions (banks, insurers, investment firms, payment processors)
- Also applies to their **cloud/SaaS vendors** designated as CTPPs
- Overlaps with **MAS TRM** (Singapore) — if you comply with one, you're close to the other
- Significant for any SaaS selling to EU financial sector

---

## United Kingdom

### UK GDPR

**Publisher:** UK Government (post-Brexit)

### Overview
Post-Brexit, the UK adopted its own version of GDPR — the **UK GDPR** (Data Protection Act 2018). Near-identical to EU GDPR with minor differences.

### Key Differences from EU GDPR
| Aspect | EU GDPR | UK GDPR |
|---|---|---|
| **Territorial scope** | EU/EEA | UK |
| **Lead DPA** | One-stop-shop (EU) | ICO (UK) |
| **Age of consent** | 16 (can be lower) | 13 |
| **Adequacy decision** | EU adequacy for UK | UK adequacy for EU (ongoing) |
| **International transfers** | SCCs + adequacy | UK SCCs + adequacy (International Data Transfer Agreement) |
| **Fines** | €20M / 4% | £17.5M / 4% |

### Relevance
- **Separate registration** required with ICO (Information Commissioner's Office)
- EU adequacy decision currently in place — may change
- If you comply with EU GDPR, you're ~95% compliant with UK GDPR

---

### Cyber Essentials

**Publisher:** UK National Cyber Security Centre (NCSC)

### Overview
A **government-backed certification** scheme that helps organizations defend against common cyber attacks. Two tiers: **Cyber Essentials** (self-assessment) and **Cyber Essentials Plus** (verified audit).

### 5 Controls
| Control | Requirements |
|---|---|
| **Firewalls** | Boundary firewalls, secure configuration |
| **Secure Configuration** | Remove unnecessary software, change default passwords |
| **User Access Control** | Least privilege, separate admin accounts |
| **Malware Protection** | Anti-malware, whitelisting, sandboxing |
| **Patch Management** | Automatic updates, 14-day patch window for critical |

### Certification
| Tier | Cost | Process | Valid For |
|---|---|---|---|
| **Basic** | ~£300 | Self-assessment questionnaire | 12 months |
| **Plus** | ~£1,500 | External vulnerability scan | 12 months |

### Relevance
- **Mandatory** for UK central government suppliers
- Highly recommended for UK SMEs and public sector
- Basic is cheap and achievable for any organization
- Plus requires a qualified assessor to verify

---

## Singapore

### PDPA (Personal Data Protection Act)

**Publisher:** Personal Data Protection Commission (PDPC), Singapore

### Overview
Singapore's comprehensive data protection law. Applies to any organization collecting personal data in Singapore.

### Key Requirements
| Requirement | Detail |
|---|---|
| **Consent** | Must obtain consent before collection, use, or disclosure |
| **Purpose Limitation** | Collect only what's necessary |
| **Notification** | Inform individuals of purpose |
| **Access & Correction** | Provide access and correct data on request |
| **Accuracy** | Reasonable efforts to keep data accurate |
| **Protection** | Make security arrangements |
| **Retention** | Stop retaining when purpose ends |
| **Transfer** | Disclosure rules apply to cross-border transfers |
| **Breach Notification** | Notify PDPC + affected individuals (if significant harm) |
| **Data Protection Officer (DPO)** | Must appoint and register a DPO |

### Enforcement
- **Financial penalty**: Up to $1M SGD
- **Directions**: Stop collection, delete data, appoint auditor
- **Criminal liability**: For knowingly mishandling data

### Relevance
- **Mandatory** for any organization operating in Singapore
- DPO appointment is mandatory — must be registered publicly
- MAS TRM (below) adds additional requirements for financial institutions

---

### MAS TRM (Technology Risk Management)

Already covered in **04 — Finance & Payment**. Key additional Singapore context:
- **ABS Guidelines** — Association of Banks in Singapore provides implementation guidance
- **Notice 658** — MAS notice on cyber hygiene (6 controls: patching, anti-malware, MFA, account mgmt, endpoint security, logging)

---

## India

### DPDP Act (Digital Personal Data Protection Act)

**Publisher:** Government of India

### Overview
India's first comprehensive data protection law, enacted in 2023. Applies to processing of **digital personal data** within India, or outside India if related to offering goods/services to data principals in India.

### Key Requirements
| Requirement | Detail |
|---|---|
| **Consent** | Consent must be free, specific, informed, unconditional, and unambiguous |
| **Notice** | Privacy notice in clear language (English + any 22 scheduled languages) |
| **Data Principal Rights** | Right to access, correction, erasure, grievance redressal |
| **Data Fiduciary** | Obligations include purpose limitation, data minimization, security safeguards |
| **Data Processor** | Contractual obligations with Data Fiduciary |
| **Cross-Border Transfer** | Central government will notify restricted countries (blacklist approach) |
| **Data Protection Officer** | Required for significant Data Fiduciaries |
| **Breach Notification** | Notify Data Protection Board (DPBI) + affected individuals |
| **Data Retention** | Cease retention when purpose is served |

### Enforcement
- **Up to ₹250 crore (~$30M)** for material breaches
- **Up to ₹500 crore (~$60M)** for failure to implement security safeguards
- Criminal penalties for re-identification of anonymized data

### Key Differences from GDPR
| Aspect | GDPR | DPDP Act |
|---|---|---|
| **Data subject rights** | 8 rights | 5 rights (no objection, portability, automated decision-making) |
| **Cross-border mechanism** | Adequacy + SCCs | Blacklist approach (restricted countries) |
| **Consent** | Must be explicit | Notice-based consent + consent manager |
| **DPO** | Some orgs | Significant Data Fiduciaries only |
| **Right to be forgotten** | Yes | Yes (erasure) |
| **Data portability** | Yes | Not explicitly |
| **Children's data** | 16 (can be lower) | 18 + verifiable parental consent |

### Relevance
- **Mandatory** for any organization processing Indian citizen data
- Applicable to foreign entities targeting Indian users
- Still awaiting full implementation rules from DPBI

---

### MeitY Cyber Security Framework

**Publisher:** Ministry of Electronics & Information Technology (MeitY), India

### Overview
MeitY publishes guidelines and frameworks for **cybersecurity in the Indian government and critical sectors**.

### Key Frameworks
| Framework | Focus |
|---|---|
| **National Cyber Security Policy (NCSP) 2013** | Overall cybersecurity strategy |
| **Cyber Crisis Management Plan (CCMP)** | Incident response coordination |
| **CERT-In** | National CERT — mandatory incident reporting (6 hours) |
| **Guidelines for Information Security Practices** | For government agencies |
| **IT Act 2000 (amended 2008)** | Legal framework for cybercrime and digital signatures |

### CERT-In Mandatory Reporting
Since 2022, CERT-In requires **mandatory reporting of cybersecurity incidents within 6 hours** — one of the fastest globally. Incidents include:
- Data breaches
- Denial of service attacks
- Malware outbreaks
- Unauthorized access
- Ransomware
- ATM/POS intrusions

### Relevance
- CERT-In reporting is **mandatory** for all service providers, intermediaries, data centers, VPN providers, cloud providers
- Non-compliance: up to 1 year imprisonment + fine
- Pairs with DPDP Act for comprehensive Indian compliance

---

## Indonesia

### PDPB (UU PDP) — Privacy

Already detailed in **05 — Healthcare & Privacy**.

---

### PSE (Penyelenggara Sistem Elektronik) / Kominfo Regulations

**Publisher:** Ministry of Communication and Informatics (Kominfo), Indonesia

### Overview
**PSE (Electronic System Operator)** registration is a requirement for any organization providing electronic systems or digital services to Indonesian users. Mandatory since 2022.

### Who Must Register
- **Public PSE**: Government electronic systems
- **Private PSE**: Private sector electronic systems
  - Domestic: Indonesian companies
  - **Foreign**: Non-Indonesian companies serving Indonesian users

### Key Requirements
| Requirement | Detail |
|---|---|
| **Registration** | Register via OSS (Online Single Submission) or PSE portal |
| **Data Centre** | Must locate data centre in Indonesia (for public service PSE) |
| **Data Protection** | Must comply with UU PDP |
| **Content Moderation** | Must have content monitoring and takedown mechanism |
| **Access** | Must provide access to Kominfo for lawful interception |
| **Reporting** | Annual report on system operations |
| **Certification** | Some sectors require additional certification (e.g., fintech) |

### Enforcement
- **Administrative sanctions**: Written warning, fines, suspension, revocation
- **Blocking**: Non-registered PSE can be blocked by Kominfo (enforced since 2022)
- Examples of blocked services: PayPal, Yahoo, Steam, Epic Games (temporarily, 2022)

### Relevance
- **Mandatory** for any company with Indonesian users
- Foreign companies must also register (B2C SaaS, games, social media)
- Registration is relatively simple — no certification needed for most private PSEs

---

### UU ITE (Undang-Undang Informasi dan Transaksi Elektronik)

**Publisher:** Government of Indonesia

### Overview
The **Electronic Information and Transactions Law (UU No. 11/2008, amended 2016, 2024)** is Indonesia's primary cybercrime and e-commerce law.

### Key Provisions
| Provision | Detail |
|---|---|
| **Article 27** | Prohibits distribution of obscene content, gambling, defamation, extortion |
| **Article 28** | Prohibits hate speech and false news |
| **Article 30** | Prohibits unauthorized access to computer systems |
| **Article 31** | Prohibits unlawful interception |
| **Article 32** | Prohibits damaging/altering electronic information |
| **Article 35** | Prohibits identity fraud |
| **Article 36** | Prohibits causing losses through electronic systems |

### Relevance
- Basis for **cybercrime enforcement** in Indonesia
- Controversial for "rubber article" enforcement (particularly Article 27 on defamation)
- 2024 revision removed some vague provisions and reduced criminal penalties

---

## Brazil

### LGPD (Lei Geral de Proteção de Dados)

**Publisher:** Autoridade Nacional de Proteção de Dados (ANPD), Brazil

### Overview
Brazil's comprehensive data protection law (Law 13,709/2018), effective 2020, modeled closely on the GDPR. Applies to any processing of personal data of individuals in Brazil.

### Key Requirements
| Requirement | Detail |
|---|---|
| **Legal Bases** | 10 legal bases (consent, contract, legal obligation, legitimate interest, etc.) |
| **Consent** | Specific, unambiguous, revocable |
| **Data Subject Rights** | 9 rights — access, correction, anonymization, blocking, portability, deletion, information, opposition, review |
| **DPO** | Must appoint a DPO (encarregado) |
| **Breach Notification** | Notify ANPD + affected individuals within reasonable time |
| **International Transfer** | Adequacy determination or contractual safeguards |
| **Privacy Notice** | Must be clear, free, and accessible |

### Key Differences from GDPR
| Aspect | GDPR | LGPD |
|---|---|---|
| **Legal bases** | 6 | 10 |
| **Fines** | €20M / 4% revenue | 2% revenue (max R$50M ~$10M) |
| **DPO** | Required for some | Required for all (can be outsourced) |
| **Enforcement** | Active (multiple €100M+ fines) | Gradually ramping up (first fines in 2023) |
| **Criminal penalties** | No | No |

### Enforcement
- First LGPD fines issued by ANPD in 2023 (Telefônica Brasil: R$2.8M)
- Max penalty: 2% of revenue in Brazil, capped at R$50M (~$10M)
- Partial suspension of data processing activities is possible

### Relevance
- **Mandatory** for any organization processing Brazilian personal data
- Similar to GDPR — if you comply with GDPR, you're ~80% compliant with LGPD
- Growing enforcement — ANPD is becoming more active

---

## UAE

### NESA / IA Standard (Information Assurance)

**Publisher:** National Electronic Security Authority (NESA), UAE

### Overview
The **UAE Information Assurance (IA) Standard** is the national cybersecurity framework for UAE government entities and critical infrastructure providers.

### Key Components
| Component | Description |
|---|---|
| **IA Standard** | 60+ security controls across 10 domains |
| **ISR (Information Security Regulations)** | Mandatory for federal government |
| **NESA Compliance** | Required for Critical Infrastructure (CNI) |
| **UAE Cyber Security Strategy** | National cybersecurity strategy (2019+) |

### 10 Control Domains
| Domain | Examples |
|---|---|
| **Security Governance** | Policies, roles, risk management, compliance |
| **HR Security** | Screening, training, disciplinary |
| **Physical Security** | Secure areas, access control |
| **Communications Security** | Encryption, TLS, VPN |
| **Access Control** | MFA, least privilege, privilege mgmt |
| **System Acquisition** | Secure SDLC, third-party assessment |
| **Cryptography** | Key management, PKI |
| **Operations Security** | Patch mgmt, anti-malware, backup |
| **Business Continuity** | BCP, DRP testing |
| **Incident Response** | SOC, reporting, forensic readiness |

### Relevance
- **Mandatory** for UAE government entities and critical infrastructure
- Critical Infrastructure sectors: energy, water, telecom, finance, healthcare, transportation, food
- Increasingly referenced by UAE-based enterprises (not just gov/CNI)

---

## Saudi Arabia

### NCA / ECC (Essential Cybersecurity Controls)

**Publisher:** National Cybersecurity Authority (NCA), Saudi Arabia

### Overview
The **NCA Essential Cybersecurity Controls (ECC)** is the primary cybersecurity framework for Saudi government entities and Critical National Infrastructure (CNI).

### ECC v2 — 5 Domains

| Domain | Controls |
|---|---|
| **Governance & Management** | 7 controls — policies, risk mgmt, compliance, performance |
| **Defense** | 15 controls — access control, network security, application security |
| **Resilience** | 6 controls — business continuity, DR, incident response |
| **Third-Party** | 2 controls — supplier security, managed services |
| **Cloud** | 1 control — cloud security requirements |

### Additional NCA Frameworks
| Framework | Applied To |
|---|---|
| **ECC (Essential)** | All government entities + CNI |
| **CCC (Critical)** | Critical infrastructure (stricter than ECC) |
| **CSCC (Cloud)** | Cloud service providers serving government |
| **OT-ECC** | Operational Technology / Industrial Control Systems |
| **NCF (National Cybersecurity Framework)** | Comprehensive strategic framework |

### Compliance Levels
| Level | Requirements |
|---|---|
| **Basic** | Foundational controls implemented |
| **Intermediate** | Most controls implemented, evidence available |
| **Advanced** | Full compliance, continuous monitoring |

### Relevance
- **Mandatory** for government entities and critical infrastructure in Saudi Arabia
- Extremely strict — fines and penalties for non-compliance
- Cloud providers must additionally comply with CSCC
- NCA conducts audits and publishes compliance results publicly

---

## South Africa

### POPIA (Protection of Personal Information Act)

**Publisher:** Information Regulator, South Africa

### Overview
South Africa's comprehensive data protection law (Act 4 of 2013), fully effective since July 2021. Applies to processing of personal information in South Africa.

### Key Conditions (8)

| # | Condition | Requirements |
|---|---|---|
| 1 | **Accountability** | Comply with all conditions, designate an Information Officer |
| 2 | **Processing Limitation** | Lawful processing, minimal collection, consent |
| 3 | **Purpose Specification** | Collect for specific, defined purpose |
| 4 | **Further Processing Limitation** | Compatible with original purpose |
| 5 | **Information Quality** | Reasonable steps to ensure accuracy |
| 6 | **Openness** | Documentation, notification of data subjects |
| 7 | **Security Safeguards** | Technical and organizational measures, breach notification |
| 8 | **Data Subject Participation** | Access, correction, deletion |

### Key Requirements
| Requirement | Detail |
|---|---|
| **Information Officer** | Must register with Information Regulator |
| **Consent** | Voluntary, specific, informed |
| **Direct Marketing** | Opt-in consent (unless existing customer relationship) |
| **Cross-Border Transfer** | Only if recipient country has adequate protection + contract |
| **Breach Notification** | Notify Regulator + data subjects (serious breaches) |
| **Retention** | No longer than necessary for purpose |
| **Prior Authorization** | Some processing requires prior Regulator approval |

### Enforcement
- **Fines**: Up to R10M (~$550K) per violation
- **Imprisonment**: Up to 10 years for serious offenses (obstruction, breach of confidentiality)
- **Civil liability**: Class actions possible
- **Enforcement notice**: Regulator can order cessation of processing

### Relevance
- **Mandatory** for any organization processing South African personal information
- Applies to foreign entities (if using automated processing in SA)
- Information Officer must be registered — penalty for non-registration
- Growing enforcement — Regulator is increasingly active

---

## United States

### FISMA / NIST (US Federal)

**Publisher:** NIST, Office of Management and Budget (OMB), US Congress

### Overview
The **Federal Information Security Modernization Act (FISMA)** requires US federal agencies to implement information security programs. NIST develops the standards and guidelines that implement FISMA.

### Key Documents
| Document | Purpose |
|---|---|
| **NIST SP 800-53** | Control catalog (1,000+ controls) |
| **NIST SP 800-37** | Risk Management Framework (RMF) — 6-step process |
| **FIPS 199** | Security categorization (low, moderate, high) |
| **FIPS 200** | Minimum security requirements |
| **NIST CSF** | Cybersecurity Framework — broader, non-regulatory |

### FISMA Compliance Process
1. **Categorize** information system (FIPS 199)
2. **Select** controls (SP 800-53)
3. **Implement** controls
4. **Assess** control effectiveness
5. **Authorize** system (AO signs ATO)
6. **Monitor** continuously

### Security Categorization Levels
| Level | Impact | Examples |
|---|---|---|
| **Low** | Limited damage | Public websites |
| **Moderate** | Serious damage | Financial systems, healthcare |
| **High** | Severe damage | National security systems |

### Relevance
- **Mandatory** for US federal agencies and their contractors
- FedRAMP (see 03 — Cloud) is built on FISMA/NIST
- SP 800-53 is the largest control catalog available — used as reference by many non-US frameworks

---

### US State Privacy Laws

#### CCPA / CPRA (California)

Covered in detail in **05 — Healthcare & Privacy**.

#### Other US State Privacy Laws

**Publisher:** Individual state legislatures

As of 2026, 15+ US states have enacted comprehensive privacy laws. This is a rapidly growing landscape due to the absence of a federal US privacy law.

| State | Law | Effective | Key Features |
|---|---|---|---|
| 🇺🇸 **California** | CCPA / CPRA | 2020 / 2023 | Right to know, delete, opt-out, opt-in for minors, private right of action |
| 🇺🇸 **Virginia** | VCDPA | 2023 | Right to access, correct, delete, portability, opt-out |
| 🇺🇸 **Colorado** | CPA | 2023 | Universal opt-out, sensitive data consent |
| 🇺🇸 **Connecticut** | CTDPA | 2023 | Similar to Virginia, broad controller obligations |
| 🇺🇸 **Utah** | UCPA | 2023 | Opt-out for targeted advertising, no private right of action |
| 🇺🇸 **Texas** | TDPSA | 2024 | Covers entities of any size (no revenue threshold) |
| 🇺🇸 **Oregon** | OCPA | 2024 | Sensitive data includes biometric, genetic, geolocation |
| 🇺🇸 **Montana** | MCDPA | 2024 | Covers non-profits (unlike most others) |
| 🇺🇸 **Iowa** | ICDPA | 2025 | Lighter than Virginia, no private right of action |
| 🇺🇸 **Tennessee** | TIPA | 2025 | Safe harbor for NIST CSF-compliant orgs |
| 🇺🇸 **Indiana** | INDPA | 2026 | Broad controller obligations |
| 🇺🇸 **Delaware** | DDPA | 2025 | Covers non-profits, broad definition of consumer |
| 🇺🇸 **Nebraska** | NDPA | 2025 | Opt-out for targeted advertising |
| 🇺🇸 **New Hampshire** | NHPA | 2025 | Sensitive data processing requires opt-in |
| 🇺🇸 **New Jersey** | NJDPA | 2025 | Broad controller obligations |

### Common Rights Across State Laws
| Right | CA | VA | CO | CT | UT |
|---|---|---|---|---|---|
| **Access** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Correction** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Deletion** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Portability** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Opt-out of sale** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Opt-out of profiling** | ✅ | ❌ | ✅ | ✅ | ❌ |
| **Private right of action** | ✅ | ❌ | ❌ | ❌ | ❌ |

### Relevance
- If you have US customers, you likely need to comply with **multiple state laws**
- Most laws only apply above certain thresholds (revenue, data volume, data sale)
- No federal preemption — each state is separate
- Consent management platforms (CMPs) are essentially mandatory for websites serving US visitors

---

## Regional Coverage Map

```
Asia-Pacific:
  🇦🇺 Australia     → Essential Eight + ISM/IRAP
  🇯🇵 Japan         → ISMAP + My Number Act
  🇸🇬 Singapore     → PDPA + MAS TRM
  🇮🇳 India         → DPDP Act + MeitY / CERT-In
  🇮🇩 Indonesia     → PDPB (UU PDP) + PSE / Kominfo
  🇨🇳 China         → PIPL + CSL + DSL (triple data law)
  🇰🇷 South Korea   → PIPA + Network Act
  🇹🇭 Thailand      → PDPA (Thailand)
  🇻🇳 Vietnam       → Law on Cybersecurity + DPDP (draft)
  🇵🇭 Philippines   → Data Privacy Act (DPA)

Europe:
  🇪🇺 EU-wide      → GDPR + NIS2 + DORA + AI Act
  🇫🇷 France       → ANSSI, RGDP, SecNumCloud
  🇩🇪 Germany       → C5 (cloud), BAFIN (finance)
  🇬🇧 UK           → UK GDPR + Cyber Essentials + NIS Regulations
  🇳🇱 Netherlands  → BIO (gov baseline)
  🇳🇴 Norway       → NSM cybersecurity principles
  🇸🇪 Sweden       → MSB framework
  🇨🇭 Switzerland  → nFADP + FINMA (finance)

Americas:
  🇺🇸 US Federal   → FISMA (gov) + FedRAMP (cloud)
  🇺🇸 US States     → CCPA (CA), VCDPA (VA), CPA (CO), TDPSA (TX), +12 more
  🇨🇦 Canada       → PIPEDA + CPPA (replacing PIPEDA)
  🇧🇷 Brazil       → LGPD
  🇲🇽 Mexico       → LFPDPPP
  🇦🇷 Argentina    → PDPA (highly protective — EU adequacy)
  🇨🇱 Chile        → Law 19.628 (new framework pending)

Middle East / Africa:
  🇦🇪 UAE          → NESA / IA Standard
  🇸🇦 Saudi Arabia → NCA / ECC + CCC + CSCC
  🇶🇦 Qatar        → NCSA + Data Privacy Law
  🇴🇲 Oman         → Cyber Law + PDPL
  🇧🇭 Bahrain      → NCA framework
  🇿🇦 South Africa → POPIA
  🇰🇪 Kenya        → Data Protection Act 2019
  🇳🇬 Nigeria      → NDPR + Data Protection Act 2023
  🇬🇭 Ghana        → Data Protection Act (Act 843)


---

*Last updated: June 2026*
