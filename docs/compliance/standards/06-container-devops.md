---
title: 06 — Container, Kubernetes & DevOps Security Standards
description: Security frameworks for containerized workloads, Kubernetes, CI/CD pipelines, and software supply chains.
---

# 06 — Container, Kubernetes & DevOps Security Standards

Security frameworks for containerized workloads, Kubernetes, CI/CD pipelines, and software supply chains.

---

## CIS Docker Benchmark

**Publisher:** Center for Internet Security (CIS)

### Overview
Hardening guidelines for Docker environments — covering the host, daemon, images, containers, and runtime.

### 5 Sections (100+ Checks)

| Section | Focus | Example |
|---|---|---|
| **1 — Host Configuration** | Linux host that runs Docker | Separate partition for `/var/lib/docker`, firewalld |
| **2 — Docker Daemon** | dockerd configuration | TLS auth, no privileged ports, log driver |
| **3 — Docker Daemon Files** | Permissions on config files | `/etc/docker` permissions, CA certs |
| **4 — Images & Build** | Dockerfiles, image scanning | No latest tag, no secrets in env, USER directive |
| **5 — Container Runtime** | Running containers | No privileged mode, read-only root FS, resource limits |
| **6 — Security Operations** | Docker Swarm | Auto-lock manager keys, rotate CA certs |

### Top 5 Critical Checks

| Check | Risk |
|---|---|
| `--privileged` flag | Full host access — sandbox escape |
| Host network mode (`--network host`) | Breaks container network isolation |
| Mounting Docker socket | Full control over host Docker daemon |
| Containers running as root | If compromised, full host access |
| `SYS_ADMIN` capability | Many kernel exploit vectors |

### Relevance
- **Core reference** for Docker security in production
- Many of these checks are implemented in Anjungan's compliance scanner

---

## CIS Kubernetes Benchmark

**Publisher:** CIS

### Overview
Hardening guidelines for Kubernetes clusters — covering control plane, worker nodes, RBAC, pod security, and policies.

### 7 Sections (240+ Checks)

| Section | Focus |
|---|---|
| **1 — Control Plane Node** | API server, scheduler, controller manager, etcd |
| **2 — etcd** | TLS, authentication, encryption at rest |
| **3 — Control Plane Configuration** | Kubelet on CP, admission controllers, pod security |
| **4 — Worker Nodes** | Kubelet configuration, node authentication |
| **5 — Policies** | RBAC, service accounts, network policies, secrets |
| **6 — CNI / Plugins** | Third-party plugin security |
| **7 — Managed Services** | EKS, AKS, GKE specific checks |

### Key Hardening Areas

| Component | Key Controls |
|---|---|
| **API Server** | `--anonymous-auth=false`, `--authorization-mode=Node,RBAC`, `--enable-admission-plugins=PodSecurityPolicy,NodeRestriction` |
| **etcd** | `--cert-file`, `--peer-cert-file`, `--auto-compaction-retention` |
| **Kubelet** | `--read-only-port=0`, `--authentication-anonymous=false`, `--protect-kernel-defaults=true` |
| **RBAC** | Cluster-admin to admins only, service accounts without cluster roles |
| **Pod Security** | Pod Security Standards (Privileged, Baseline, Restricted) |
| **Secrets** | Encryption at rest, no secrets in env vars |

### Relevance
- **Essential** for any production Kubernetes cluster
- Managed K8s (EKS, AKS, GKE) handle many control plane checks automatically
- Use tools like `kube-bench` (Aqua Security) to automate assessment

---

## NSA Kubernetes Hardening Guide

**Publisher:** National Security Agency (US) / CISA

### Overview
A practical 5-step guide published in 2021, updated 2025. Shorter and more actionable than CIS K8s Benchmark.

### 5 Steps

| Step | What to Do |
|---|---|
| **1 — Scan container images** | Use image scanners (Trivy, Grype) — only run verified images |
| **2 — Apply least privilege** | Pod Security Standards (Restricted), no privileged, drop ALL caps |
| **3 — Network segmentation** | Default deny network policies, encrypt traffic (mTLS) |
| **4 — Secrets protection** | Encryption at rest, avoid secrets in env/configmaps, use external secrets store |
| **5 — Audit logging** | Enable K8s audit logs, monitor for anomalies |

### Relevance
- Excellent **starting point** for K8s security — covers 80% of common risks in 5 steps
- Pairs with CIS K8s for deeper coverage

---

## SLSA (Supply-chain Levels for Software Artifacts)

**Publisher:** OpenSSF (Open Source Security Foundation)

### Overview
A framework for **software supply chain integrity** — ensuring that artifacts (binaries, containers, packages) are built securely and traceably.

### SLSA Levels

| Level | Requirements | Achieving |
|---|---|---|
| **L1** | Provenance exists (build process documented) | Tag builds, store SBOM |
| **L2** | Provenance hosted + tamper-resistant | Host provenance with build logs |
| **L3** | Hardened builds + strong provenance | Reproducible builds, ephemeral env |
| **L4** | Two-party review + hermetic builds | Independent verification |

### Key Concepts
| Term | Meaning |
|---|---|
| **Provenance** | Who built what, from what source, using what process |
| **Attestation** | Cryptographically signed provenance (e.g., in-toto) |
| **SBOM** | Software Bill of Materials — list of all components |
| **Hermetic Build** | No network access during build — deterministic |

### Relevance
- **Growing importance** after SolarWinds, Log4j, xz utils attacks
- SLSA L3 is becoming common for critical infrastructure
- GitHub Actions + Sigstore make SLSA L2 achievable for small teams

---

## OWASP CI/CD Top 10

**Publisher:** OWASP Foundation

### Overview
A risk list specific to **CI/CD pipeline security** — threats that traditional web app security doesn't cover.

### Top 10 Risks (2023)

| Rank | Risk |
|---|---|
| **CICD-01** | Insufficient Flow Control Mechanisms |
| **CICD-02** | Inadequate Identity & Access Management |
| **CICD-03** | Dependency Chain Abuse |
| **CICD-04** | Poisoned Pipeline Execution (PPE) |
| **CICD-05** | Insufficient PBAC (Pipeline-Based Access Control) |
| **CICD-06** | Insufficient Credential Hygiene |
| **CICD-07** | Insecure System Configuration |
| **CICD-08** | Ungoverned Usage of 3rd-Party Services |
| **CICD-09** | Improper Artifact Integrity Validation |
| **CICD-10** | Insufficient Logging & Visibility |

### Relevance
- **Critical** if you run CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins)
- Many risks are ignored in standard security audits
- PPE (Poisoned Pipeline Execution) was exploited in the SolarWinds attack

---

## How These Fit Together

```
CONTAINER SECURITY STACK

            ┌──────────────────┐
            │  NSA K8s Guide   │ ← Starting point (5 steps)
            └────────┬─────────┘
                     │ maps to
            ┌────────▼─────────┐
            │ CIS K8s Benchmark│ ← Deep K8s hardening
            └────────┬─────────┘
                     │ covers
            ┌────────▼─────────┐
            │ CIS Docker Bmk   │ ← Container runtime
            └────────┬─────────┘
                     │
            ┌────────▼─────────┐
            │  SLSA (supply    │ ← Pipeline integrity
            │  chain security) │
            └──────────────────┘
```

---

*Last updated: June 2026*
