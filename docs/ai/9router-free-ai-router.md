---
title: 9Router — Free AI Router
description: **9Router** is a smart AI gateway that sits between your coding CLI tools (OpenCode, Claude Code, Cursor, Codex, Cline, etc.) and 60+ AI providers. It
---

# 9Router — Free AI Router

**9Router** is a smart AI gateway that sits between your coding CLI tools (OpenCode, Claude Code, Cursor, Codex, Cline, etc.) and 60+ AI providers. It provides a single OpenAI-compatible endpoint and handles routing, format translation, quota tracking, and auto-fallback.


## Table of Contents

- [How It Works](#how-it-works)
- [Free Providers](#free-providers)
- [Install](#install)
- [Usage](#usage)
  - [Docker (VPS/server)](#docker-vpsserver)
  - [Resources](#resources)
- [Setup: OpenCode CLI + 9Router (Free AI)](#setup-opencode-cli-9router-free-ai)
  - [Step 1: Install & run 9Router](#step-1-install-run-9router)
  - [Step 2: Connect a free provider](#step-2-connect-a-free-provider)
  - [Step 3: Config OpenCode](#step-3-config-opencode)
  - [Model naming](#model-naming)
- [Key Features](#key-features)
- [Supported CLI Tools](#supported-cli-tools)
- [Notes](#notes)

Project: [9router.com](https://9router.com) · GitHub: [decolua/9router](https://github.com/decolua/9router) (16k+ stars, MIT)

## How It Works

```
CLI Tool (OpenCode / Claude Code / dll)
    │  POST http://localhost:20128/v1/chat/completions
    ↓
┌─── 9Router ──────────────────────────────────────┐
│  • Detect request format (OpenAI/Claude/etc)      │
│  • RTK: compress tool_result (save 20-40% tokens) │
│  • Resolve model combo & credential                │
│  • Translate format (OpenAI ↔ Claude ↔ Gemini)    │
│  • Route to provider + SSE streaming               │
│  • Auto fallback if quota exhausted / error        │
│  • Track usage & cost                              │
└───┬───────────────────────────────────────────────┘
    │
    ├─→ Tier 1: SUBSCRIPTION (Claude Code, Codex, Copilot)
    ├─→ Tier 2: CHEAP (GLM $0.6/1M, MiniMax $0.2/1M)
    └─→ Tier 3: FREE (Kiro AI, OpenCode Free, Vertex $300 credits)
```

## Free Providers

| Provider | Models | How |
|----------|--------|-----|
| **Kiro AI** | Claude 4.5 + GLM-5 + MiniMax | Connect via dashboard, unlimited |
| **OpenCode Free** | Auto-fetch models | No auth, direct use |
| **Vertex AI** | Gemini 3 Pro + GLM-5 + DeepSeek | $300 free credits |

> Note: iFlow, Qwen, Gemini CLI free tiers were discontinued in 2026.

## Install

```bash
npm install -g 9router
```

## Usage

Run the dashboard + API server:

```bash
9router
```

Dashboard opens at `http://localhost:20128/dashboard`.

Options:
- `--port 8080` — custom port
- `--no-browser` — don't open browser automatically
- `--skip-update` — skip auto-update check

### Docker (VPS/server)

```bash
docker run -d --name 9router --restart unless-stopped \
  -p 20128:20128 \
  -v "$HOME/.9router:/app/data" -e DATA_DIR=/app/data \
  decolua/9router:latest
```

### Resources

- **Docker image:** ~834MB
- **npm size:** ~13MB download, ~47MB unpacked
- **RAM:** ~150-300MB
- **CPU:** Lightweight when idle

## Setup: OpenCode CLI + 9Router (Free AI)

### Step 1: Install & run 9Router

```bash
npm install -g 9router
9router
```

Keep this terminal open. Dashboard opens at `http://localhost:20128/dashboard`.

### Step 2: Connect a free provider

In the dashboard → **Providers** → Connect **Kiro AI** (no signup, Claude 4.5 free unlimited). Copy the API key from the dashboard.

### Step 3: Config OpenCode

In a **new terminal** (keep 9Router running):

**Test:**
```bash
LOCAL_ENDPOINT=http://localhost:20128/v1 opencode
```

**Permanent config** (`~/.opencode.json`):
```json
{
  "agents": {
    "coder": {
      "model": "local.kr/claude-sonnet-4.5"
    }
  }
}
```

Then run:
```bash
LOCAL_ENDPOINT=http://localhost:20128/v1 opencode
```

### Model naming

Models from 9Router use the `local.` prefix in OpenCode's agent config:
- `local.kr/claude-sonnet-4.5` — Claude 4.5 via Kiro AI (free)
- `local.glm-5` — GLM-5 via API key ($0.6/1M)

## Key Features

| Feature | Description |
|---------|-------------|
| **RTK Token Saver** | Auto-compress tool outputs, save 20-40% input tokens |
| **Caveman Mode** | Output compression — save up to 65% output tokens |
| **3-Tier Fallback** | Auto-route: Subscription → Cheap → Free, zero downtime |
| **Format Translation** | OpenAI ↔ Claude ↔ Gemini ↔ Cursor ↔ Kiro — works with any CLI |
| **Multi-Account** | Round-robin between multiple accounts per provider |
| **Quota Tracking** | Real-time token count + reset countdown |
| **Auto Token Refresh** | OAuth tokens refresh automatically |

## Supported CLI Tools

Claude Code · OpenClaw · Codex · **OpenCode** · Cursor · Antigravity · Cline · Continue · Droid · Roo · Copilot · Kilo Code · **Hermes Agent** · Gemini CLI · Qwen Code · iFlow · Aider

## Notes

- 9Router runs in the **foreground** — keep the terminal open while coding, Ctrl+C to stop
- OpenCode via `LOCAL_ENDPOINT` env var or configure in `~/.opencode.json`
- Resource usage is moderate (~150-300MB RAM), best for laptop or a VPS with spare memory

---

*Last updated: June 2026*
