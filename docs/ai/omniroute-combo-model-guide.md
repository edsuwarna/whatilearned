---
title: Building OmniRoute Combos — Free & Budget Model Categorization
description: How to group free/cheap LLMs (DeepSeek, MiniMax, MiMo, Qwen) into OmniRoute auto/ combos — primary + fallback patterns, use-case fit, and 6 ready-made combo designs.
---

# Building OmniRoute Combos — Free & Budget Model Categorization

> **Last updated:** 2026-08-01
> **Source:** OmniRoute gateway catalog + capability research from this repo's AI articles

Guide to grouping free/cheap models into OmniRoute combos (`auto/*`). Combos are created via **dashboard → Combos → Create Combo** (the `/api/combos` API needs an admin key separate from the /v1 key).

## Table of Contents

- [🗂️ Model Categorization](#model-categorization)
- [🎯 Recommended Combos](#recommended-combos)
- [💡 Combo Design Strategy](#combo-design-strategy)

## 🗂️ Model Categorization

| Model | Category | Main Strength | Context | Modality |
|---|---|---|---|---|
| **DeepSeek V4 Flash** | ⚡ Fast/cheap workhorse | Low latency, cheap, general | 1M | Text |
| **DeepSeek V4 Pro** | 🧠 Strong reasoning | Deep reasoning, math, agentic | 1M | Text |
| **MiniMax M3** | 🖥️ Coding + multimodal | Frontier coding, 1M ctx, vision | 1M | Text + Image |
| **MiniMax M2.7-highspeed** | ⚡ Fast coding | Polyglot code, refactoring, low latency | 200K | Text |
| **MiMo V2.5** | 🎬 Omnimodal | Text+Image+Video+Audio, 1M ctx | 1M | Text+Img+Vid+Aud |
| **MiMo V2.5 Pro** | 🧠 Agentic giant | 1.02T params, agentic, software eng | 1M | Text |
| **Qwen3.7-Flash** | 🖼️ Multimodal agent | Vision-language, cheap, tool calling | 1M | Text+Img+Vid |

## 🎯 Recommended Combos

### 1. `auto/mimo-vision` — Omnimodal agent combo
- **MiMo V2.5** (primary) + fallback **Qwen3.7-Flash** + fallback **MiniMax M3**
- For: image/video/audio analysis, multimodal documents, agents needing visual+audio understanding
- Most unique — no other model handles audio+video in one model

### 2. `auto/cheap-coding` — Budget coding combo
- **DeepSeek V4 Flash** (primary) + **Qwen3.7-Flash** + fallback **MiMo V2.5 Pro**
- For: budget-friendly code generation/refactor without heavy reasoning
- Qwen3.7-Flash at $0.03/M input — cheapest for coding

### 3. `auto/pro-agent` — Agentic task combo
- **MiMo V2.5 Pro** (primary) + fallback **DeepSeek V4 Pro** + **MiniMax M2.7-highspeed**
- For: complex multi-step agents, software engineering, long-horizon tasks
- V2.5 Pro 1T params strongest agentic; V4 Pro reasoning; M2.7-highspeed fast responses

### 4. `auto/vision-fast` — Fast vision combo
- **Qwen3.7-Flash** (primary) + **MiniMax M3** (fallback)
- For: OCR, screenshot analysis, visual QA — fast & cheap
- Both vision-capable; Qwen cheaper, M3 stronger

### 5. `auto/balanced-multimodal` — All-rounder combo
- **MiniMax M3** (primary) + **MiMo V2.5** + **DeepSeek V4 Pro**
- For: daily driver — mix of coding, vision, reasoning

### 6. Improvements to existing combos
- **`auto/best-coding`** → add **MiniMax M3** + **MiMo V2.5 Pro** as candidates
- **`auto/best-vision`** → add **Qwen3.7-Flash** + **MiMo V2.5**
- **`auto/best-free`** → add **DeepSeek V4 Flash free** + **Qwen3.7-Flash**

## 💡 Combo Design Strategy

1. **One primary + 2-3 fallbacks** — if primary is down/expensive, auto-switch to equivalent
2. **Prefer the cheapest model fit for the task** — light coding uses V4 Flash/Qwen3.7-Flash, not V2.5 Pro
3. **Separate vision from text-only** — don't mix M2.7-highspeed (text) into a combo that needs images
4. **`noc/` prefix for free tier** — combos with zero total cost
