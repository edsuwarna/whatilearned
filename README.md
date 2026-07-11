# whatilearned

A personal documentation hub for various tools and technologies, especially in infrastructure, DevOps, and security.

🌐 **Live site**: [https://notes.edsuwarna.id](https://notes.edsuwarna.id)

```
whatilearned/
├── docs/
│   ├── index.html       # SPA documentation site
│   ├── terminal/         # Terminal tools & customization
│   ├── security/         # Security best practices
│   ├── cloudflare/       # Pages, Workers, DNS, deployments
│   ├── ai/               # AI agent frameworks & deep dives
│   ├── infrastructure/  # Deployment, Docker, infrastructure
│   └── images/           # Centralized images
└── README.md
```

Deployed on [Cloudflare Pages](https://pages.cloudflare.com) — auto-deploys on every push to `main`.

---

> 🤖 Some content in this repository is generated with the assistance of AI. All content is reviewed, edited, and curated manually to ensure accuracy and relevance.

### 🤖 AI
- **[docs/ai/9router-free-ai-router.md](docs/ai/9router-free-ai-router.md)** — Setup guide for 9Router: free AI gateway for OpenCode, Claude Code, and other CLI tools
- **[docs/ai/claw-framework-comparison.md](docs/ai/claw-framework-comparison.md)** — Side-by-side comparison of OpenClaw, Hermes Agent, Nanoclaw, and Picoclaw AI agent frameworks
- **[docs/ai/google-ai-studio-free-models.md](docs/ai/google-ai-studio-free-models.md)** — Google AI Studio free tier models, rate limits, and API access guide
- **[docs/ai/opencode-advanced-tips.md](docs/ai/opencode-advanced-tips.md)** — Advanced OpenCode workflows: live log tailing, SSH analysis, MCP servers, incident response, per-project commands, and SRE emergency kit
- **[docs/ai/opencode-agent-skills.md](docs/ai/opencode-agent-skills.md)** — OpenCode agent skills reference: open-source SKILL.md repositories, skill managers (skillkit, agnix), and cross-tool compatibility
- **[docs/ai/opencode-commands-by-role.md](docs/ai/opencode-commands-by-role.md)** — OpenCode custom commands organized by engineering role: Developer, DevOps, SRE, Cloud, and Infrastructure
- **[docs/ai/opencode-daily-use-cases.md](docs/ai/opencode-daily-use-cases.md)** — Real-world daily use cases for OpenCode: coding, debugging, refactoring, Docker, CI/CD, security, and devops workflows
- **[docs/ai/opencode-power-user.md](docs/ai/opencode-power-user.md)** — OpenCode power user guide: custom instructions, TUI shortcuts, token management, model strategy, git superpowers, tmux workflow, and session hygiene
- **[docs/ai/picoclaw-deep-dive.md](docs/ai/picoclaw-deep-dive.md)** — Comprehensive deep dive into Picoclaw (sipeed/picoclaw), the ultra-lightweight Go-based AI agent framework

### 📁 Career
- **[docs/career/upwork-profile.md](docs/career/upwork-profile.md)** — Upwork profile optimization guide: headline, overview, portfolio, specialized profiles, and pricing strategy

### ☁️ Cloudflare
- **[docs/cloudflare/deploy-littlelink-to-cloudflare-pages.md](docs/cloudflare/deploy-littlelink-to-cloudflare-pages.md)** — Step-by-step guide to deploy LittleLink on Cloudflare Pages

### 🛡️ Compliance
- **[docs/compliance/anjungan-compliance-scanner.md](docs/compliance/anjungan-compliance-scanner.md)** — Automated compliance scanning for internal tools using CIS benchmarks and Lynis
- **[docs/compliance/standards/01-governance-risk.md](docs/compliance/standards/01-governance-risk.md)** — Governance & risk management compliance standards
- **[docs/compliance/standards/02-server-infrastructure.md](docs/compliance/standards/02-server-infrastructure.md)** — Server infrastructure security standards
- **[docs/compliance/standards/03-cloud-saas.md](docs/compliance/standards/03-cloud-saas.md)** — Cloud & SaaS compliance standards
- **[docs/compliance/standards/04-finance-payment.md](docs/compliance/standards/04-finance-payment.md)** — Finance & payment industry compliance (PCI DSS, etc.)
- **[docs/compliance/standards/05-healthcare-privacy.md](docs/compliance/standards/05-healthcare-privacy.md)** — Healthcare & privacy compliance (HIPAA, GDPR, etc.)
- **[docs/compliance/standards/06-container-devops.md](docs/compliance/standards/06-container-devops.md)** — Container & DevOps compliance standards
- **[docs/compliance/standards/07-regional-standards.md](docs/compliance/standards/07-regional-standards.md)** — Regional compliance standards (Indonesia, EU, US)
- **[docs/compliance/standards/README.md](docs/compliance/standards/README.md)** — Overview of 30+ technology compliance standards mapped to ISO 27001 controls

### ⚙️ Infrastructure
- **[docs/infrastructure/act.md](docs/infrastructure/act.md)** — Run GitHub Actions workflows locally with nektos/act: installation, CLI reference, runner images, secrets, events, and practical examples
- **[docs/infrastructure/beszel.md](docs/infrastructure/beszel.md)** — Beszel — lightweight server monitoring with historical data, Docker stats, alerts, and OIDC/OAuth support
- **[docs/infrastructure/chisel.md](docs/infrastructure/chisel.md)** — Chisel: fast TCP/UDP tunnel over HTTP, alternative to frp and ngrok — client-server architecture
- **[docs/infrastructure/dagger.md](docs/infrastructure/dagger.md)** — Programmable CI/CD platform: SDKs in 8 languages, content-addressed caching, built-in tracing, Dagger Cloud
- **[docs/infrastructure/database-backup.md](docs/infrastructure/database-backup.md)** — Database backup guide for PostgreSQL, MySQL, and MariaDB: dedicated users, strategies, automation scripts, and test restore
- **[docs/infrastructure/database-backup-incremental.md](docs/infrastructure/database-backup-incremental.md)** — Incremental database backup guide: pgBackRest, WAL archiving, XtraBackup, binary logs, MariaDB Backup — with tool comparison and pitfalls
- **[docs/infrastructure/datasette-sqlite-tools.md](docs/infrastructure/datasette-sqlite-tools.md)** — Datasette, Turso/libSQL, SQLPage — open-source SQLite tools with web UI, auto APIs, and enhanced features for exploring and managing databases
- **[docs/infrastructure/dex-oidc.md](docs/infrastructure/dex-oidc.md)** — Dex OIDC — federated OpenID Connect identity provider for self-hosted apps (Zot, Forgejo, Beszel)
- **[docs/infrastructure/dokploy-basic-auth.md](docs/infrastructure/dokploy-basic-auth.md)** — Adding basic auth to Compose applications on Dokploy via Traefik middleware
- **[docs/infrastructure/dozzle.md](docs/infrastructure/dozzle.md)** — Dozzle — real-time Docker log viewer with forward-proxy OIDC auth via Dex and oauth2-proxy
- **[docs/infrastructure/forgejo-cicd-docker-compose.md](docs/infrastructure/forgejo-cicd-docker-compose.md)** — Self-hosted Forgejo with CI/CD (Forgejo Actions) using Docker Compose
- **[docs/infrastructure/forgejo-mirror-github.md](docs/infrastructure/forgejo-mirror-github.md)** — Mirror GitHub repositories to Forgejo via UI migration or CLI
- **[docs/infrastructure/forgejo-storage.md](docs/infrastructure/forgejo-storage.md)** — Forgejo storage architecture, backup, cleanup, and Docker build cache management
- **[docs/infrastructure/frp.md](docs/infrastructure/frp.md)** — 
- **[docs/infrastructure/glibc-vs-musl.md](docs/infrastructure/glibc-vs-musl.md)** — Comprehensive comparison: architecture, performance, static linking, Docker implications, DNS, threading, and when to choose which C library
- **[docs/infrastructure/kata-containers-vs-firecracker.md](docs/infrastructure/kata-containers-vs-firecracker.md)** — Comparison of Kata Containers and Firecracker for lightweight virtualization
- **[docs/infrastructure/kopia-backup.md](docs/infrastructure/kopia-backup.md)** — Kopia backup with Cloudflare R2: incremental, dedup, encrypted backup for VPS
- **[docs/infrastructure/netbird-selfhosted.md](docs/infrastructure/netbird-selfhosted.md)** — Self-hosted Netbird WireGuard mesh VPN with SSO, groups, policies, TURN relay, and routing peers
- **[docs/infrastructure/netmaker-selfhosted.md](docs/infrastructure/netmaker-selfhosted.md)** — Self-hosted Netmaker WireGuard mesh VPN platform: installation, ingress/egress gateways, ACL, and automation
- **[docs/infrastructure/object-storage-comparison.md](docs/infrastructure/object-storage-comparison.md)** — Comparison of S3-compatible object storage providers: R2, S3, GCS, Backblaze B2
- **[docs/infrastructure/taskfile.md](docs/infrastructure/taskfile.md)** — Modern YAML-based task runner: dependencies, caching, templates, includes, platform-specific commands
- **[docs/infrastructure/warpgate.md](docs/infrastructure/warpgate.md)** — 
- **[docs/infrastructure/wireguard.md](docs/infrastructure/wireguard.md)** — WireGuard VPN: installation, hub & spoke topology, site-to-site, NAT traversal, advanced config, security, and migration from OpenVPN
- **[docs/infrastructure/zot-registry.md](docs/infrastructure/zot-registry.md)** — Lightweight OCI-compliant container registry with Zot: deployment, auth, R2 storage, CVE scanning

### 🔒 Security
- **[docs/security/supply-chain-security.md](docs/security/supply-chain-security.md)** — Open source supply chain security prevention playbook

### 🖥️ Terminal
- **[docs/terminal/colorls.md](docs/terminal/colorls.md)** — Beautify your ls command with color and icons
- **[docs/terminal/customize-terminal.md](docs/terminal/customize-terminal.md)** — ZSH + oh-my-zsh installation guide
