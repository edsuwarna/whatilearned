# 04 — Finance & Payment Compliance Standards

Security requirements for organizations handling financial transactions, cardholder data, and banking infrastructure.

---

## PCI DSS v4.0

**Publisher:** PCI Security Standards Council (Visa, Mastercard, Amex, Discover, JCB)

### Overview
The **Payment Card Industry Data Security Standard (PCI DSS)** protects cardholder data. Version 4.0 (effective March 2024, Dated March 2025) is the current version. **Any organization that stores, processes, or transmits cardholder data** must comply.

### Merchant Levels (by transaction volume)

| Level | Volume | Requirements |
|---|---|---|
| **1** | > 6M transactions/year | Full QSA audit annually |
| **2** | 1M–6M | Self-assessment (SAQ D) or QSA |
| **3** | 20K–1M e-commerce | SAQ annually |
| **4** | < 20K e-commerce | SAQ annually |

### 12 Requirements (6 Goals)

| Goal | Req # | Requirement |
|---|---|---|
| **Build & Maintain Security** | 1 | Install firewalls |
| | 2 | Change vendor defaults |
| **Protect Cardholder Data** | 3 | Protect stored data (encryption, truncation, hashing) |
| | 4 | Encrypt transmission (TLS 1.2+) |
| **Manage Vulnerabilities** | 5 | Anti-malware |
| | 6 | Secure apps (SDLC, patching) |
| **Access Control** | 7 | Least privilege |
| | 8 | Unique IDs + MFA |
| | 9 | Physical security of card data |
| **Monitor & Test** | 10 | Logging & audit trails |
| | 11 | Vulnerability scans + penetration tests |
| **Policy** | 12 | Info security policy for all personnel |

### PCI v4.0 Changes
- **Customized Approach** — implement custom controls instead of defined ones (with validation)
- **More frequent assessments** — quarterly some controls were annual
- **Scripting security** — form page scripts need integrity verification
- **Multi-factor authentication** — now required for all administrative access (not just remote)

### Relevance
- **Mandatory** if you accept credit cards
- Penalties: $5K–$100K/month + potential loss of card acceptance rights
- Applies to **any server** in the cardholder data environment (CDE)

---

## PCI PIN Security

**Publisher:** PCI SSC

### Overview
Extends PCI DSS for **PIN processing environments** — ATMs, POS terminals, payment HSMs (Hardware Security Modules). Replaces the older PCI PED (PIN Entry Device) standard.

### Key Requirements
| Requirement | Detail |
|---|---|
| HSM Key Management | Dual control, split knowledge, tamper protection |
| Key Derivation | Unique keys per transaction |
| PIN Encryption | Triple-DES or AES — never plaintext |
| Terminal Security | Tamper-responsive, certified hardware |
| Remote Key Loading | Secure channel, authenticated |

### Relevance
- **Only if you handle PINs directly** (merchant processing, ATM deployer, payment processor)
- Most SaaS companies never touch this — gateway handles it (Stripe, Midtrans, etc.)

---

## SWIFT CSP

**Publisher:** SWIFT

### Overview
The **SWIFT Customer Security Programme (CSP)** is a mandatory set of security controls for all SWIFT-connected financial institutions. Released after the 2016 Bangladesh Bank heist ($81M theft).

### Control Framework (3 Pillars)

| Pillar | Category | Example Controls |
|---|---|---|
| **1 — Secure Environment** | 8 controls | Restrict internet access, dedicated endpoint, MFA, hardened OS |
| **2 — Prevent Compromise** | 7 controls | Anti-malware, password policy, patch mgmt, vulnerability scans |
| **3 — Detect & Respond** | 6 controls | Anomaly detection, incident response, reporting to SWIFT |

### Attestation
- **Self-attestation** annually
- **Independent assessment** every 2–3 years (larger institutions)
- Results can be shared with counterparties

### Relevance
- **Mandatory** for any SWIFT member (banks, brokerages, clearing houses)
- Directly responsible for preventing payment fraud
- Non-compliance = potential disconnection from SWIFT network

---

## MAS TRM (Technology Risk Management)

**Publisher:** Monetary Authority of Singapore

### Overview
Guidelines for technology risk management of **Financial Institutions in Singapore** — very influential across APAC.

### Key Requirements
| Domain | Requirements |
|---|---|
| **IT Governance** | Board-level oversight, risk appetite, escalation |
| **Cybersecurity** | SOC, threat intelligence, red teaming, BCP testing |
| **Cloud** | Outsourcing notification, data residency, shared responsibility |
| **AI/ML** | Governance, transparency, explainability |
| **Outsourcing** | Vendor risk management, audit rights, exit plan |

### Relevance
- **Banks and Fintech** operating in Singapore must comply
- MAS guidelines are often used as reference by Bank Indonesia and OJK

---

## Other Notable Financial Standards

| Standard | Region | Focus |
|---|---|---|
| **P2PE** (PCI) | Global | Point-to-point encryption for POS |
| **3DS 2.x** (EMVCo) | Global | Authentication — e-commerce card-not-present |
| **PSD2 / PSD3** | EU | Open banking, SCA (Strong Customer Authentication) |
| **BAFIN** | Germany | MaRisk (IT for banking) — very detailed |
| **FFIEC** | US | Federal Financial Institutions Examination Council |
| **BCBS 239** | Global | Basel Committee — risk data aggregation |

---

*Last updated: June 2026*
