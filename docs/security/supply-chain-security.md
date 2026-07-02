---
title: Open Source Supply Chain Security — Prevention Playbook
description: - [1. 🔐 GitHub / Repository Security](#1-github-repository-security)
---

# Open Source Supply Chain Security — Prevention Playbook

> Lessons learned from the Trivy supply chain attack (GHSA-69fq-xp46-6x23, March 2026)
> and general best practices for securing open source projects.


## Table of Contents

- [1. 🔐 GitHub / Repository Security](#1-github-repository-security)
- [2. 🔄 CI/CD Security](#2-cicd-security)
- [3. 📦 Dependency Management](#3-dependency-management)
- [4. 📤 Release Security](#4-release-security)
- [5. 👥 Access Control](#5-access-control)
- [6. 🕵️ Pre-commit & Secret Detection](#6-pre-commit-secret-detection)
- [7. 📋 Open Source Project Checklist](#7-open-source-project-checklist)

## 1. 🔐 GitHub / Repository Security

**Branch protection** — protect your `main` branch:
- No force push allowed
- Require pull request reviews before merging
- Require status checks to pass before merging

**Signed commits** — enable GPG or SSH signing:
- Git supports commit signing via GPG or SSH keys
- GitHub marks verified commits with a ✅ badge
- Prevents impersonation — no one can push a commit pretending to be you

```bash
# Configure GPG signing
git config --global commit.gpgsign true
git config --global user.signingkey <KEY_ID>
```

**CODEOWNERS** — enforce code review for critical files:
```github
# .github/CODEOWNERS
Dockerfile          @edsuwarna
.github/workflows/* @edsuwarna
requirements.txt    @edsuwarna
```

**2FA WAJIB** — mandatory two-factor authentication for all maintainers:
- The Trivy incident was caused by compromised credentials without 2FA
- GitHub enforces 2FA for all users publishing to GitHub Packages / releases

## 2. 🔄 CI/CD Security

**Pin all GitHub Actions by commit SHA** — never use version tags:

```yaml
# ❌ DANGEROUS — tags can be force-pushed!
uses: aquasecurity/trivy-action@v0.35.0

# ✅ SAFE — pinned by SHA
uses: aquasecurity/trivy-action@8a3177a...

# ✅ SAFE with Dependabot auto-updates
uses: aquasecurity/trivy-action@8a3177a...  # Dependabot will update SHA
```

**Rules:**
- Never use `@latest` or `@main` in production workflows
- Use Dependabot to automatically update action SHAs
- Store secrets in **GitHub Secrets** or use **OIDC** — never in workflow YAML
- Validate artifact checksums before use

## 3. 📦 Dependency Management

**Lock dependencies** with hashes to prevent tampering:

```bash
# Python — pip-tools with hashes
pip-compile --generate-hashes requirements.in -o requirements.txt
```

**Automated dependency scanning:**
- **Dependabot** — auto PR for known vulnerable dependencies
- **Renovate** — more configurable alternative
- **pip-audit** — scan Python dependencies against PyPI advisory DB

**Software Bill of Materials (SBOM):**
- Generate SBOM for every release using Syft or Trivy
- Attach SPDX/CycloneDX JSON to GitHub releases
- Consumers can verify no unexpected dependencies were added

```bash
# Generate SBOM with Syft
syft packages your-image:latest -o spdx-json > sbom.spdx.json
```

## 4. 📤 Release Security

**Immutable releases:**
- GitHub Releases are immutable by default — enabled March 2026
- Prevents overwriting release assets after publication
- Verify this is enabled in your repo settings

**Signing release artifacts:**
```bash
# GPG sign release assets
gpg --armor --detach-sign my-release.tar.gz

# Cosign (container signing)
cosign sign --key cosign.key ghcr.io/username/image:tag
```

**SLSA framework:**
- Target at least **SLSA Level 1** — build provenance
- Generate non-forgeable attestation that artifacts came from your CI build
- SLSA Level 3+ provides dependency integrity guarantees

**Never reuse version tags:**
- Trivy attacker force-pushed 76/77 version tags in trivy-action
- If you must use tags, make them immutable via GitHub settings
- Production pipelines should use **release IDs** or **content hashes**, not tags

## 5. 👥 Access Control

The Trivy incident started with **compromised maintainer credentials**.

**Best practices:**
```
✅ Minimal maintainers — 1-2 admins, everyone else as contributor
✅ Fine-grained Personal Access Tokens (not classic tokens)
✅ Token scoping — grant minimum required permissions
✅ Token rotation — expire and renew periodically
✅ No shared credentials — each maintainer uses their own account
✅ Audit active tokens monthly
```

**GitHub-specific:**
- Use **GitHub Apps** instead of PATs for automation
- Fine-grained PATs can be scoped to specific repos and permissions
- Classic tokens have broad access — avoid them

## 6. 🕵️ Pre-commit & Secret Detection

Prevent sensitive data from ever reaching the repository:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
```

**Tools to run periodically:**
- **TruffleHog** — scan git history for exposed secrets
- **gitleaks** — lightweight secret scanning alternative
- **git secret** — encrypt sensitive files in the repo

```bash
# Scan entire git history
trufflehog filesystem --directory=. .
```

## 7. 📋 Open Source Project Checklist

Use this when starting a new open source project:

- [ ] **Branch protection** on `main` (no force push, require reviews)
- [ ] **GPG/SSH signing** for all commits
- [ ] **GitHub Actions pinned by SHA** (not tags)
- [ ] **Dependabot / Renovate** enabled for dependency updates
- [ ] **SBOM** generated for each release
- [ ] **2FA** enabled for all maintainers
- [ ] **Pre-commit hooks** for secret detection
- [ ] **CODEOWNERS** file for sensitive paths
- [ ] **Fine-grained PATs** (no classic tokens)
- [ ] **Dependency scanning** in CI (pip-audit, Trivy, or Grype)
- [ ] **Immutable releases** confirmed in repo settings
- [ ] **Documented** security policy (`SECURITY.md`) for vulnerability reporting

---

*Last updated: May 2026*
*Inspired by the Trivy ecosystem supply chain incident (GHSA-69fq-xp46-6x23)*
