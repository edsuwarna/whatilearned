---
title: Picoclaw Deep Dive — Ultra-Lightweight AI Agent Framework
description: **Project:** `sipeed/picoclaw`
---

# Picoclaw Deep Dive — Ultra-Lightweight AI Agent Framework

**Project:** `sipeed/picoclaw`  
**Stars:** 29.2K ⭐  
**Language:** Go  
**Latest:** v0.2.8  
**Org:** Sipeed (hardware company — RISC-V boards, AI cameras)  
**License:** MIT  
**Website:** [picoclaw.io](https://picoclaw.io) | **Docs:** [docs.picoclaw.io](https://docs.picoclaw.io)  
**Created:** Feb 2026 (~4 months old)


## Table of Contents

- [📊 GitHub Statistics](#github-statistics)
- [🏗️ Architecture Overview](#architecture-overview)
  - [Package Structure (`pkg/` — 35+ packages)](#package-structure-pkg-35-packages)
  - [CLI Layer (`cmd/`)](#cli-layer-cmd)
  - [Web Layer (`web/`)](#web-layer-web)
- [🔄 Core Runtime: The Agent Loop](#core-runtime-the-agent-loop)
  - [Message Flow](#message-flow)
  - [Turn Lifecycle](#turn-lifecycle)
- [🔥 Key Features In Detail](#key-features-in-detail)
  - [1. 🪶 Ultra-Lightweight (<10 MB RAM)](#1-ultra-lightweight-10-mb-ram)
  - [2. 🤖 Native MCP Protocol Support](#2-native-mcp-protocol-support)
  - [3. 🧠 30+ LLM Providers via Protocol-Prefix Routing](#3-30-llm-providers-via-protocol-prefix-routing)
  - [4. 🔌 19+ Messaging Channels](#4-19-messaging-channels)
  - [5. 🔄 SubTurn Mechanism (Sub-Agent Coordination)](#5-subturn-mechanism-sub-agent-coordination)
  - [6. 🎯 Steering System (Mid-Turn Injection)](#6-steering-system-mid-turn-injection)
  - [7. 🔗 Hook System](#7-hook-system)
  - [8. 🧬 Agent Self-Evolution](#8-agent-self-evolution)
  - [9. 📱 Android Support](#9-android-support)
  - [10. ⏰ Cron/Scheduled Tasks](#10-cronscheduled-tasks)
  - [11. 🛠️ Built-in Tools](#11-built-in-tools)
- [📦 Installation](#installation)
  - [Binary Download (Recommended)](#binary-download-recommended)
  - [Build from Source](#build-from-source)
  - [Docker](#docker)
  - [Android APK](#android-apk)
- [⚙️ Configuration](#configuration)
- [🆚 Picoclaw vs Hermes Agent](#picoclaw-vs-hermes-agent)
  - [Picoclaw Strengths (vs Hermes)](#picoclaw-strengths-vs-hermes)
  - [Picoclaw Limitations (vs Hermes)](#picoclaw-limitations-vs-hermes)
- [🛑 Honest Limitations](#honest-limitations)
- [🗺️ Roadmap Highlights](#roadmap-highlights)
- [🏁 Summary](#summary)

---

## 📊 GitHub Statistics

| Metric | Value |
|--------|-------|
| **Stars** | 29,215 — hit 20K in 17 days |
| **Forks** | 4,189 |
| **Open Issues** | 83 |
| **Language** | Go (844 files), TypeScript (784KB), Makefile, Shell |
| **Total Files** | 1,556 |
| **Test Files** | 315 (37% of Go files) |
| **Markdown Docs** | 242 |
| **Top Contributors** | afjcjsbx (259), alexhoshina (208), lc6464 (88), lxowalle (80), wj-xiao (78) |

---

## 🏗️ Architecture Overview

Picoclaw is a **from-scratch Go reimplementation** inspired by NanoBot (Python, HKUDS). Built via **AI-bootstrapping** — 95% of core code was AI-generated, then human-refined.

### Package Structure (`pkg/` — 35+ packages)

```
pkg/
├── agent/          # Core agent loop, hooks, subturn mechanism, registry
├── audio/          # ASR (speech recognition) + TTS
├── auth/           # OAuth and authentication flows
├── bus/            # Message bus — inbound/outbound pub-sub with channels
├── channels/       # 19+ messaging platform integrations
├── commands/       # Built-in slash commands
├── config/         # Configuration loading, versioning, merging
├── cron/           # Cron/scheduled task service
├── devices/        # Device management
├── events/         # Runtime event bus
├── evolution/      # Agent self-evolution (learning from turns → skill improvements)
├── gateway/        # HTTP gateway server (service orchestrator)
├── hooks/          # Hook manager (observers, interceptors, tool approvers)
├── isolation/      # Sandbox/isolation for execution
├── mcp/            # Model Context Protocol support
├── memory/         # JSONL-based append-only memory store
├── providers/      # LLM provider implementations (12 provider packages)
├── routing/        # Smart model routing (light/heavy model dispatch)
├── session/        # Session management, scoping, canonical keys, aliases
├── skills/         # Skill system (load SKILL.md files, ClawHub registry)
├── tools/          # Built-in tool implementations (cron, delegate, web search)
└── updater/        # Self-update mechanism
```

### CLI Layer (`cmd/`)

- `cmd/picoclaw/` — Main binary with subcommands: `onboard`, `agent`, `gateway`, `auth`, `cron`, `mcp`, `skills`, `model`, `status`, `version`, `migrate`
- `cmd/membench/` — Memory benchmarking tool

### Web Layer (`web/`)

- `web/frontend/` — TypeScript/React UI (pnpm-based)
- `web/backend/` — Go-based launcher backend serving the Web UI
- `web/picoclaw-launcher.desktop` — Desktop entry file

---

## 🔄 Core Runtime: The Agent Loop

### Message Flow

```
InboundMessage → NormalizeInboundContext → RouteResolver.ResolveRoute()
  → session.AllocateRouteSession() → ensureSessionMetadata()
  → Router.SelectModel() → provider execution → tool execution → response
```

### Turn Lifecycle

1. **Worker spawn** — Agent spawns a goroutine per session (up to `max_parallel_turns`)
2. **Steering** — Messages from same session serialized via steering queue
3. **LLM call** — Provider-specific API call
4. **Tool execution** — Sequential tool execution with steering polling after each tool
5. **Turn end** — History persistence, event emission, evolution recording
6. **Continue** — Resume with steering messages if any

---

## 🔥 Key Features In Detail

### 1. 🪶 Ultra-Lightweight (<10 MB RAM)

| Metric | Picoclaw | OpenClaw | NanoBot |
|--------|----------|----------|---------|
| RAM | **<10-20 MB** | >1 GB | ~100 MB |
| Boot Time | **<1s** | >500s | ~30s |
| Binary | **~15 MB** (single Go binary) | Node.js + deps | Python + deps |

- **Single static Go binary** — zero runtime dependencies
- **Cross-platform**: x86_64, ARM64, ARMv6/v7, RISC-V, MIPS, LoongArch, s390x
- Runs on **$10 hardware** (LicheeRV-Nano RISC-V board)
- Supported OS: Linux, Windows, macOS, FreeBSD, NetBSD, Android

### 2. 🤖 Native MCP Protocol Support

Full Model Context Protocol integration via `pkg/mcp/`. Supports **stdio, SSE, and HTTP** transport.

```json
{
  "tools": {
    "mcp": {
      "enabled": true,
      "servers": {
        "filesystem": {
          "enabled": true,
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        }
      }
    }
  }
}
```

CLI: `picoclaw mcp add|list|test|edit|remove`

### 3. 🧠 30+ LLM Providers via Protocol-Prefix Routing

Unified routing using `protocol/model_name` format:

```json
{
  "model_name": "deepseek-chat",
  "model": "openai/deepseek-chat",
  "api_base": "https://api.deepseek.com/v1",
  "api_keys": ["sk-xxx"]
}
```

Supported providers: OpenAI, Anthropic, Google Gemini, DeepSeek, Qwen, Groq, Ollama, vLLM, Azure, AWS Bedrock, GitHub Copilot, and many more.

### 4. 🔌 19+ Messaging Channels

| Channel | Protocol | Channel | Protocol |
|---------|----------|---------|----------|
| Telegram | Long polling | Discord | WebSocket |
| WhatsApp | Native/Bridge | WeChat (Weixin) | iLink API |
| QQ | WebSocket | Slack | Socket Mode |
| Matrix | Sync API | DingTalk | Stream |
| Feishu/Lark | WebSocket/SDK | LINE | Webhook |
| WeCom | WebSocket | VK | Long Poll |
| IRC | IRC protocol | OneBot | OneBot v11 |
| MQTT | MQTT pub/sub | MaixCam | TCP socket |
| Pico (native) | Built-in | Pico Client | WebSocket |
| Teams Webhook | Webhook | | |

**This is the widest channel coverage of any AI agent framework**, including OpenClaw.

### 5. 🔄 SubTurn Mechanism (Sub-Agent Coordination)

Isolated nested agent loops with:
- **Context isolation** — ephemeral sessions that don't pollute parent history
- **Depth limit** — max 3 nested levels
- **Concurrency** — up to 5 concurrent sub-turns per parent
- **Async mode** — results delivered to parent's pending results channel
- **Error recovery** — auto-retry on context length exceeded
- **Critical flag** — sub-turns can survive parent completion

### 6. 🎯 Steering System (Mid-Turn Injection)

Messages can be injected mid-turn into the agent loop. Useful for:
- Interrupting the agent mid-thought
- Priority override of the current task
- External event handling (e.g., timeouts, user corrections)
- Priority injection for urgent requests

### 7. 🔗 Hook System

Four types of hooks — both **in-process** and **out-of-process** (JSON-RPC over stdio):

| Hook Type | Interface | Can Modify Data |
|-----------|-----------|-----------------|
| Observer | `RuntimeEventObserver` | No |
| LLM Interceptor | `LLMInterceptor` | Yes (before/after LLM) |
| Tool Interceptor | `ToolInterceptor` | Yes (before/after tool) |
| Tool Approver | `ToolApprover` | Allow/Deny only |

Hook actions: `continue`, `modify`, `respond`, `deny_tool`, `abort_turn`, `hard_abort`

### 8. 🧬 Agent Self-Evolution

Learns from completed turns and turns successful patterns into skill improvements:

| Mode | Behavior |
|------|----------|
| `observe` | Record learning data only |
| `draft` | Generate candidate skill drafts |
| `apply` | Auto-update workspace skills |

Trigger modes: `after_turn`, `scheduled`, `manual`

### 9. 📱 Android Support

- **Native APK** with full UI (main page, web page, log page, settings page)
- **Termux** support for resource-constrained environments
- No Termux required for APK install — turn old phones into AI assistants

### 10. ⏰ Cron/Scheduled Tasks

Full cron support:
- One-time reminders: "Remind me in 10 minutes"
- Recurring tasks: "Remind me every 2 hours"
- Cron expressions: "Remind me at 9am daily"
- CLI: `picoclaw cron list|add|disable|remove`

### 11. 🛠️ Built-in Tools

- **Web search**: DuckDuckGo (unlimited, free), Tavily, Brave, Perplexity, Baidu, SearXNG, GLM Search
- **Cron/Scheduling**: One-time and recurring
- **File operations**: Read/write within workspace
- **Code execution**: Sandboxed command execution
- **SubTurn spawning**: Nested agent loops for sub-tasks
- **MCP tools**: Dynamically loaded from MCP servers
- **Skills**: SKILL.md-based modular capabilities

---

## 📦 Installation

### Binary Download (Recommended)
```bash
curl -fsSL https://picoclaw.io | sh
```

### Build from Source
```bash
git clone https://github.com/sipeed/picoclaw.git
cd picoclaw
make deps
(cd web/frontend && pnpm install --frozen-lockfile)
make build            # Core binary
make build-launcher   # Web UI Launcher
```

Prerequisites: Go 1.25+, Node.js 22+, pnpm 10.33.0+

### Docker
```bash
docker compose -f docker/docker-compose.yml --profile launcher up
```

### Android APK
Download from picoclaw.io/download — no Termux needed.

**35+ build targets** available: Linux (x86_64, arm64, armv6, armv7, riscv64, loong64, mipsle, s390x), macOS (arm64, x86_64), Windows (x86_64, arm64), FreeBSD/NetBSD. Available as `.tar.gz`, `.deb`, `.rpm`, `.zip`.

---

## ⚙️ Configuration

Config lives in `~/.picoclaw/config.json` (JSON v3). API keys stored separately in `.security.yml`.

Key config sections:
- `agents.defaults` — Model, tokens, temperature, tool iterations, context window
- `agents.dispatch.rules` — Agent routing rules
- `model_list[]` — Model definitions with protocol prefix
- `channel_list{}` — Per-channel configuration
- `tools` — Web search, MCP, skills, cron
- `hooks` — Hook system configuration
- `events.logging` — Runtime event log filters
- `session` — Session dimensions, identity links
- `evolution` — Self-evolution settings

---

## 🆚 Picoclaw vs Hermes Agent

| Feature | Picoclaw | Hermes Agent |
|---------|----------|-------------|
| Language | Go | Python |
| RAM | <10-20 MB | ~100 MB+ |
| Boot Time | <1s | ~2-5s |
| Binary Size | ~15 MB (single binary) | Python + deps (~100 MB+) |
| Hardware | $10 RISC-V boards to Android | Requires Linux server/VPS |
| Message Channels | **19+** 🏆 | Telegram only |
| LLM Providers | **30+** 🏆 | Multiple (OpenAI, Anthropic, etc.) |
| MCP Support | Native Go MCP SDK | Via Python MCP |
| Skills System | SKILL.md-based + ClawHub | hermes-agent skill system |
| Tool System | Built-in + MCP + hooks | Function tools |
| Cron/Scheduling | Built-in cron service | Built-in cron |
| Memory/Persistence | JSONL session store | Database-backed |
| Hook System | ✅ In/out-process JSON-RPC | ❌ |
| Sub-Agent Coordination | ✅ SubTurn mechanism | ❌ |
| Vision Pipeline | ✅ Auto base64 encoding | ✅ Via tools |
| Steering (mid-turn injection) | ✅ Full steering system | ❌ |
| Agent Self-Evolution | ✅ Learning from turns | ❌ (not built-in) |
| Android Support | ✅ Native APK | ❌ |
| Web UI | ✅ Built-in launcher | ❌ (Telegram only) |
| System Tray | ✅ Windows & Linux | ❌ |
| Config Versioning | ✅ Auto-migration (v0→v3) | Manual |
| Documentation | 242 markdown files (sprawling) | Centralised docs |
| Maturity | Pre-v1.0 (rapid development) | More mature |
| Stars | 29.2K | 172K (Hermes Agent ecosystem) |

### Picoclaw Strengths (vs Hermes)
- Dramatically lower resource footprint (<10 MB vs ~100 MB+)
- Multi-channel support (19+ vs 1)
- Runs on embedded/RISC-V hardware
- Faster boot, single binary deployment
- More advanced agent mechanisms (SubTurn, Steering, Self-Evolution, Hooks)
- Android support

### Picoclaw Limitations (vs Hermes)
- Pre-v1.0 software; security not production-hardened
- Documentation spread across 242 markdown files
- Rapid changes may break configs between releases
- Go ecosystem smaller than Python for AI tooling
- Less mature skill/module ecosystem
- Partially Chinese-centric documentation

---

## 🛑 Honest Limitations

1. **Pre-1.0 software** — "do not deploy to production," security disclaimer active
2. **Memory creep** — originally <10 MB, recent PRs pushed to 10-20 MB; optimization deferred
3. **~80+ Go dependencies** — ironic for a "lightweight" project; includes full Anthropic/OpenAI SDKs
4. **Documentation sprawl** — 242 markdown files can be overwhelming
5. **Chinese-centric** — many docs in Chinese first; English translations may lag
6. **MCP dependency** — requires npx/Node.js for many MCP servers despite being a Go binary
7. **Velocity vs stability** — 29K stars in <4 months = rapid change outpacing polish
8. **Limited non-LLM tool ecosystem** — Python agents have pip; Go has fewer ready-made integrations

---

## 🗺️ Roadmap Highlights

1. **Core Optimization** — <20 MB on 64 MB RAM embedded boards, remove redundant deps
2. **Security Hardening** — prompt injection defense, tool abuse prevention, SSRF, filesystem sandbox
3. **Connectivity** — protocol-based provider architecture, browser automation (CDP), skill marketplace
4. **Advanced Capabilities** — multi-agent collaboration (basic + swarm mode), AIEOS (AI-Native OS)
5. **Developer Experience** — interactive CLI wizard, comprehensive platform guides
6. **Brand & Community** — Mantis Shrimp logo ("Small but Mighty, Lightning Fast")

---

## 🏁 Summary

Picoclaw is a **remarkably ambitious** project — a complete AI agent framework in pure Go that achieves extreme resource efficiency while supporting an unprecedented breadth of features: 19+ channels, 30+ providers, native MCP, sub-agents (SubTurn), hooks, self-evolution, cron, skills marketplace, Android APK, and system tray.

Its **<10 MB RAM** and **sub-second boot** on **$10 RISC-V hardware** are genuinely impressive engineering achievements. The AI-bootstrapped development approach is novel.

For **edge/IoT/embedded deployments** where resource constraints are critical, Picoclaw is uniquely positioned as the only viable option. However, for **production daily-driver use** on a capable server, more mature frameworks like Hermes Agent or OpenClaw still offer better stability, ecosystem, and documentation.

> **Bottom line:** Picoclaw is not a replacement for Hermes Agent today, but it's absolutely worth watching — especially once it hits v1.0 and security hardening is complete.
