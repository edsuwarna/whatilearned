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

### Terminal
- **[colorls](docs/terminal/colorls.md)** — Beautify your ls command with color and icons
- **[customize-terminal](docs/terminal/customize-terminal.md)** — ZSH + oh-my-zsh installation guide

### Security
- **[supply-chain-security](docs/security/supply-chain-security.md)** — Open source supply chain security prevention playbook

### Cloudflare
- **[deploy-littlelink-to-cloudflare-pages](docs/cloudflare/deploy-littlelink-to-cloudflare-pages.md)** — Step-by-step guide to deploy LittleLink on Cloudflare Pages

### AI
- **[9router-free-ai-router](docs/ai/9router-free-ai-router.md)** — Setup guide for 9Router: free AI gateway for OpenCode, Claude Code, and other CLI tools
- **[opencode-daily-use-cases](docs/ai/opencode-daily-use-cases.md)** — Real-world daily use cases for OpenCode: coding, debugging, refactoring, Docker, CI/CD, security, and devops workflows
- **[picoclaw-deep-dive](docs/ai/picoclaw-deep-dive.md)** — Comprehensive deep dive into Picoclaw (sipeed/picoclaw), the ultra-lightweight Go-based AI agent framework
- **[claw-framework-comparison](docs/ai/claw-framework-comparison.md)** — Side-by-side comparison of OpenClaw, Hermes Agent, Nanoclaw, and Picoclaw AI agent frameworks
- **[opencode-commands-by-role](docs/ai/opencode-commands-by-role.md)** — OpenCode custom commands organized by engineering role: Developer, DevOps, SRE, Cloud, and Infrastructure
- **[opencode-advanced-tips](docs/ai/opencode-advanced-tips.md)** — Advanced OpenCode workflows: live log tailing, SSH analysis, MCP servers, incident response, per-project commands, and SRE emergency kit
- **[opencode-power-user](docs/ai/opencode-power-user.md)** — OpenCode power user guide: custom instructions, TUI shortcuts, token management, model strategy, git superpowers, tmux workflow, and session hygiene
- **[opencode-agent-skills](docs/ai/opencode-agent-skills.md)** — OpenCode agent skills reference: open-source SKILL.md repositories, skill managers (skillkit, agnix), and cross-tool compatibility

### Infrastructure
- **[act](docs/infrastructure/act.md)** — Run GitHub Actions workflows locally with nektos/act: installation, CLI reference, runner images, secrets, events, and practical examples
- **[dagger](docs/infrastructure/dagger.md)** — Programmable CI/CD platform: SDKs in 8 languages, content-addressed caching, built-in tracing, Dagger Cloud
- **[dokploy-basic-auth](docs/infrastructure/dokploy-basic-auth.md)** — Adding basic auth to Compose applications on Dokploy via Traefik middleware
- **[forgejo-cicd-docker-compose](docs/infrastructure/forgejo-cicd-docker-compose.md)** — Self-hosted Forgejo with CI/CD (Forgejo Actions) using Docker Compose
- **[glibc-vs-musl](docs/infrastructure/glibc-vs-musl.md)** — Comprehensive comparison: architecture, performance, static linking, Docker implications, DNS, threading, and when to choose which C library
- **[taskfile](docs/infrastructure/taskfile.md)** — Modern YAML-based task runner: dependencies, caching, templates, includes, platform-specific commands
