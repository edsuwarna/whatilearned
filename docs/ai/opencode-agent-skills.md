# OpenCode Agent Skills — Open-Source Collections & Reference

> **Last updated:** 2026-06-06
> **Compatible with:** OpenCode, Claude Code, Codex CLI, Cursor, Gemini CLI, Antigravity, and any tool supporting the SKILL.md standard.

## Overview

OpenCode uses the **universal SKILL.md** format — the same standard supported by Claude Code, Codex, Cursor, Windsurf, Kiro, and 40+ other AI coding assistants. Skills are loaded from `.opencode/skills/<name>/SKILL.md` (project-level) or `~/.config/opencode/skills/<name>/SKILL.md` (global).

This document catalogs the best open-source SKILL.md collections on GitHub that are compatible with OpenCode.

---

## Top Open-Source Skill Repositories

### 🥇 cc-skills-golang — ⭐ 1,991
- **Repo:** [samber/cc-skills-golang](https://github.com/samber/cc-skills-golang)
- **42 skills** for production-ready Go development

| Skill | Category |
|-------|----------|
| `golang-testing` | Testing |
| `golang-concurrency` | Concurrency patterns |
| `golang-grpc` | gRPC development |
| `golang-performance` | Performance optimization |
| `golang-observability` | Observability (otel, prometheus) |
| `golang-database` | Database (SQL, NoSQL, migrations) |
| `golang-security` | Security hardening |
| `golang-cli` | CLI development (cobra, viper) |
| `golang-swagger` | API documentation |
| `golang-design-patterns` | Go design patterns |
| `golang-error-handling` | Error handling patterns |
| `golang-dependency-injection` | DI (uber-fx, google-wire) |
| `golang-project-layout` | Project structure |
| `golang-lint` | Linting & code quality |
| `golang-ci` | Continuous integration |

*Plus 28 more: context, data-structures, documentation, graphql, naming, modernize, popular-libraries, safety, stretchr/testify, spf13/cobra, spf13/viper, uber-dig, uber-fx, samber/{do,hot,lo,mo,oops,ro,slog}, and staying updated.*

**Install:**
```bash
npx skills add https://github.com/samber/cc-skills-golang --all
# Single skill:
npx skills add https://github.com/samber/cc-skills-golang --skill golang-performance
```

---

### 🥇 awesome-llm-skills — ⭐ 1,296
- **Repo:** [Prat011/awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills)
- **Curated list** of LLM/AI agent skills with ~30 ready-to-use skill directories

| Skill | Purpose |
|-------|---------|
| `skill-creator` | Bootstrap new SKILL.md files |
| `changelog-generator` | Auto-generate changelogs |
| `video-downloader` | Download video content |
| `meeting-insights-analyzer` | Analyze meeting transcripts |
| `notion-knowledge-capture` | Capture knowledge to Notion |
| `notion-meeting-intelligence` | Meeting notes to Notion |
| `notion-research-documentation` | Research docs in Notion |
| `notion-spec-to-implementation` | Spec → implementation workflow |
| `file-organizer` | Organize file structures |
| `canvas-design` | Design canvases/mockups |
| `theme-factory` | Create color themes |
| `webapp-testing` | Web app testing patterns |
| `image-enhancer` | Image optimization |
| `internal-comms` | Internal communications |
| `brand-guidelines` | Brand consistency check |
| `lead-research-assistant` | Lead/company research |
| `competitive-ads-extractor` | Ad analysis |
| `content-research-writer` | Content research & writing |
| `domain-name-brainstormer` | Domain name ideas |
| `mcp-builder` | MCP server scaffolding |
| `slack-gif-creator` | Slack GIF integration |
| `artifacts-builder` | Build artifacts |
| `raffle-winner-picker` | Raffle automation |
| `resemble-detect` | Visual similarity detection |
| `template-skill` | SKILL.md template |
| `algorithmic-art` | Generative art |
| `invoice-organizer` | Invoice management |
| `document-skills` | Document processing |

---

### 🥇 obsidian-skills (kepano) — ⭐ 34,575
- **Repo:** [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
- 5 skills by the Obsidian CEO for working with Obsidian vaults

| Skill | Description |
|-------|-------------|
| `obsidian-markdown` | Obsidian-flavored Markdown (wikilinks, embeds, callouts, properties, tags) |
| `obsidian-cli` | Obsidian CLI operations |
| `obsidian-bases` | Obsidian Bases (database-like views) |
| `json-canvas` | JSON Canvas format |
| `defuddle` | HTML-to-Markdown conversion |

---

### 🥇 ctf-skills — ⭐ 2,310
- **Repo:** [ljagiello/ctf-skills](https://github.com/ljagiello/ctf-skills)
- CTF challenge-solving skills

| Skill | Category |
|-------|----------|
| Web exploitation | Web vulnerabilities |
| Binary pwn | Binary exploitation |
| Crypto | Cryptography challenges |
| Reverse engineering | RE / decompilation |
| Forensics | Digital forensics |
| OSINT | Open-source intelligence |

---

### 🥇 Deep-Research-skills — ⭐ 994
- **Repo:** [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills)
- Structured deep research workflow with human-in-the-loop

| Skill | Language |
|-------|----------|
| `research-en` | English |
| `research-zh` | Chinese |
| `research-codex-en` | Codex-optimized (EN) |
| `research-codex-zh` | Codex-optimized (ZH) |

---

### 🥇 devops-sre-skills — ⭐ 12 (new)
- **Repo:** [bregman-arie/devops-sre-skills](https://github.com/bregman-arie/devops-sre-skills)
- DevOps / SRE runbooks as SKILL.md files with schema validation

| Skill | Description |
|-------|-------------|
| `kubernetes` | K8s operations |
| `terraform` | Terraform workflows |
| `aws` | AWS operations |
| `gcp` | GCP operations |
| `argocd` | ArgoCD management |
| `incident` | Incident response |
| `security` | Security runbooks |
| `observability` | Monitoring & observability |
| `cost` | Cost optimization |

---

### 🥇 context-engineering-kit — ⭐ 1,075
- **Repo:** [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit)
- Hand-crafted skills focused on improving agent results quality

---

## Skill Manager Tools

### Skillkit — ⭐ 1,189
- **Repo:** [rohitg00/skillkit](https://github.com/rohitg00/skillkit)
- Universal skill installer: install, translate & share skills across 40+ CLIs
- **Usage:**
  ```bash
  npx skills add <repo-url> --all
  npx skills add <repo-url> --skill <name>
  npx skills remove <skill-name>
  npx skills list
  ```
- Auto-detects your tool (OpenCode, Claude Code, Cursor, Codex, etc.) and installs to the correct directory
- Includes a marketplace at `skills.sh`

### Agnix — ⭐ 267
- **Repo:** [agent-sh/agnix](https://github.com/agent-sh/agnix)
- Linter + LSP for AI agent configs. Validates SKILL.md files (39 rules), opencode.json (45 rules), and cross-tool configs.
- **Usage:**
  ```bash
  agnix validate              # Validate all configs in current dir
  agnix validate skills       # Validate only SKILL.md files
  agnix fix                   # Auto-fix issues
  ```

### agentic-stack — ⭐ 2,074
- **Repo:** [codejunkie99/agentic-stack](https://github.com/codejunkie99/agentic-stack)
- Portable `.agent/` folder containing memory + skills + protocols that works across Claude Code, Cursor, Windsurf, OpenCode, OpenClaw, Hermes, and DIY Python

### oh-my-agent — ⭐ 1,062
- **Repo:** [first-fluke/oh-my-agent](https://github.com/first-fluke/oh-my-agent)
- Vendor-agnostic agent harness for project-specific skills, workflows, and agent teams aligned with your codebase

### agentsys — ⭐ 844
- **Repo:** [agent-sh/agentsys](https://github.com/agent-sh/agentsys)
- 44 skills + 49 agents for Claude Code, OpenCode, Codex, Cursor, Kiro

---

## How Skills Work in OpenCode

### Directory Structure

```bash
# Project-level (specific to a project)
.opencode/skills/<skill-name>/SKILL.md

# Global (available to all projects)
~/.config/opencode/skills/<skill-name>/SKILL.md

# Also compatible (cross-tool standards):
.claude/skills/<skill-name>/SKILL.md
.agents/skills/<skill-name>/SKILL.md
```

### SKILL.md Format

```yaml
---
name: my-skill
description: What this skill does (1-1024 chars)
license: MIT              # optional
compatibility: opencode   # optional
metadata:
  audience: developers    # optional
---

## What I Do

Detailed instructions for the agent here.
```

### Key Facts

- **Skills are NOT built-in** — OpenCode ships with zero pre-installed skills. Everything comes from the community or your own creation.
- **Skills are lazy-loaded** — the agent loads them only when relevant, so they don't bloat your context.
- **Permission control** — configure allow/deny/ask per skill pattern in `opencode.json`.
- **Cross-tool compatible** — SKILL.md format works identically across OpenCode, Claude Code, Codex, Cursor, Windsurf, Gemini CLI, Kiro, and 40+ other tools.

---

## Quick Reference: Most Valuable Picks

| What You Need | Best Pick |
|--------------|-----------|
| **Go development** | `samber/cc-skills-golang` — 42 Go-specific skills |
| **General LLM skills** | `Prat011/awesome-llm-skills` — ~30 curated skills |
| **Obsidian vault** | `kepano/obsidian-skills` — by Obsidian CEO |
| **CTF challenges** | `ljagiello/ctf-skills` — pentesting & CTF |
| **Deep research** | `Weizhena/Deep-Research-skills` — structured research |
| **DevOps/SRE runbooks** | `bregman-arie/devops-sre-skills` — ops workflows |
| **Universal installer** | `rohitg00/skillkit` — install any skill from CLI |
| **Skill validator** | `agent-sh/agnix` — lint & validate SKILL.md |

---

## Related

- [OpenCode Commands by Role](opencode-commands-by-role.md) — OpenCode custom commands organized by engineering role
- [OpenCode Power User Guide](opencode-power-user.md) — Custom instructions, TUI shortcuts, model strategy
- [OpenCode Advanced Tips](opencode-advanced-tips.md) — Advanced OpenCode workflows
