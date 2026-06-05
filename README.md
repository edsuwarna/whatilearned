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

### Infrastructure
- **[dokploy-basic-auth](docs/infrastructure/dokploy-basic-auth.md)** — Adding basic auth to Compose applications on Dokploy via Traefik middleware
