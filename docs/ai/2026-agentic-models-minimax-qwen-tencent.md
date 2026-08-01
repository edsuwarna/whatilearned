---
title: MiniMax M2.7-highspeed, Qwen3.7-Flash & Tencent Hy3 — 2026 Agentic Contenders
description: Capability deep-dive of three 2026 agentic models — MiniMax M2.7-highspeed (fast coding), Qwen3.7-Flash (multimodal agent, 1M ctx, cheap), Tencent Hy3 (295B MoE reliability-first).
---

# MiniMax M2.7-highspeed, Qwen3.7-Flash & Tencent Hy3

> **Last updated:** 2026-08-01
> **Source:** MiniMax API Docs, OpenRouter, Aliyun Model Studio, Tencent HF card

Three 2026 models from MiniMax, Alibaba, and Tencent — all strong agentic contenders with different strengths.

## Table of Contents

- [🚀 MiniMax-M2.7-highspeed](#minimax-m27-highspeed)
- [⚡ Qwen3.7-Flash](#qwen37-flash)
- [🤖 Tencent Hy3](#tencent-hy3)
- [🆚 Comparison](#comparison)

## 🚀 MiniMax-M2.7-highspeed

**Official source:** platform.minimax.io (MiniMax docs)

| Aspect | Detail |
|---|---|
| Positioning | **"highspeed" variant of M2.7** — same performance, much faster inference, low latency |
| Architecture | MoE, 62 layers, hidden 3072, **256 local experts / 8 active per token**, full attention |
| Context | **200K tokens** (196K usable) |
| Strengths | 🧑💻 **Polyglot code mastery** + precision code refactoring + low latency |
| M2.7 base capabilities | "Recursive self-improvement", **agentic multi-agent**, top real-world engineering, office delivery, character-rich interaction |
| Tool use | ✅ Function calling (`minimax_m2` parser), reasoning, structured outputs, interleaved thinking |
| Extras | MTP (3 modules) output acceleration, QK-norm |
| Price (OpenRouter) | $0.25/M input, $1/M output |
| Deploy | Self-host: vLLM / SGLang (Linux GPU) / MLX (Mac Studio) — BF16 ~457GB VRAM |

**Takeaway:** focused on **coding, precise refactoring, and fast-response scenarios** (agents, real-time). Text-only.

## ⚡ Qwen3.7-Flash

**Official source:** OpenRouter + Aliyun Model Studio (百炼) + platform.qianwenai.com

| Aspect | Detail |
|---|---|
| Positioning | Alibaba's **vision-language reasoning model** — "能看、能想、能动手" (sees, thinks, acts) |
| Modality | 🖼️ **Text + Image + Video → Text** (multimodal!) |
| Context | **1M tokens**, max output 64K |
| Released | Jul 28, 2026 (slug `qwen3.7-flash-20260727`) |
| Official use cases | **Multimodal agents, visual coding, search, computer interaction** — strong at object recognition, spatial understanding, real-world visual perception |
| Base capabilities | Creative writing, math/logic, code development, info QA, text translation |
| Tool use | ✅ Tools, reasoning, response_format, seed, logprobs |
| Price | Very cheap: **$0.03/M input, $0.13/M output** (cache read $0.006/M) |
| Real performance | Latency 0.91s (P50), ~38 tps, uptime 99.99% (Alibaba Cloud) |

**Takeaway:** a **multimodal agent model** — image & video input, reasoning, tool calling, 1M context, dirt cheap. Successor to the Qwen3-VL lineage with agentic capabilities.

## 🤖 Tencent Hy3

**Official source:** HF model card `tencent/Hy3` + OpenRouter

| Property | Value |
|---|---|
| Developer | **Tencent Hy Team** (腾讯混元) |
| Architecture | Sparse MoE |
| Total Params | **295B** |
| Active Params | **21B** (top-8 of 192 experts) |
| MTP Layer | 3.8B (1 layer) |
| Layers | 80 (GQA, 64 heads, 8 KV heads, head dim 128) |
| Context | **256K** |
| License | **Apache 2.0** (open-source!) |
| Precision | BF16 (FP8 variant available) |

**Core capabilities:**
- **Strong reasoning** — configurable reasoning effort (disabled/low/high). 21B active yet competitive with flagships 2-5× larger
- **Agentic workflows** — main strength:
  - **Stable tool calls & output formats** — production-grade, error recovery, generalizes across scaffoldings (CodeBuddy, Cline, KiloCode — SWE-Bench variance < 4%)
  - Built from feedback across 50+ Tencent products
- **Anti-hallucination**: hallucination rate down **12.5% → 5.4%**, commonsense errors **25.4% → 12.7%**
- **Long-context & multi-turn**: issue rate down **17.4% → 7.9%**; strong on long-dialogue evals (MRCR)
- **Productivity**: coding, office work, **financial modeling**, **frontend design**, **game development**
- **Benchmark**: blind eval of 270 experts → **2.67/4** > GLM-5.1 (2.51/4)

**Price (OpenRouter):** $0.132/M input, $0.528/M output, $0.033/M cache read

**Notes:** text-only (not multimodal). Open-source Apache 2.0 → self-hostable (vLLM/SGLang, finetuning & RL guides included). **hy3-preview** variant available (April, cheaper: $0.063/$0.21).

## 🆚 Comparison

| Model | Total/Active | Context | Focus | Modality | Price in/out per 1M |
|---|---|---|---|---|---|
| **M2.7-highspeed** | ~172B/? | 200K | Fast coding & refactoring | Text | $0.25/$1 |
| **Qwen3.7-Flash** | ? | **1M** | Multimodal & visual agent | Text+Img+Vid | **$0.03/$0.13** |
| **Hy3** | 295B/21B | 256K | Agentic + reliability + anti-hallucination | Text | $0.132/$0.528 |
