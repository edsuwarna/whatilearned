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

**Sumber resmi:** platform.minimax.io (docs resmi MiniMax)

| Aspek | Detail |
|---|---|
| Positioning | **Varian "highspeed" dari M2.7** — performa sama, inference jauh lebih cepat, low latency |
| Arsitektur | MoE, 62 layer, hidden 3072, **256 local experts / 8 aktif per token**, full attention |
| Context | **200K tokens** (196K usable) |
| Keunggulan | 🧑💻 **Polyglot code mastery** + precision code refactoring + low latency |
| Capability M2.7 | "Recursive self-improvement", **agentic multi-agent**, top real-world engineering, office delivery, character-rich interaction |
| Tool use | ✅ Function calling (`minimax_m2` parser), reasoning, structured outputs, interleaved thinking |
| Ekstra | MTP (3 modules) akselerasi output, QK-norm |
| Harga (OpenRouter) | $0.25/M input, $1/M output |
| Deploy | Self-host: vLLM / SGLang (Linux GPU) / MLX (Mac Studio) — BF16 ~457GB VRAM |

**Kesimpulan:** fokus ke **coding, refactoring presisi, skenario butuh respons cepat** (agent, real-time). Text-only.

## ⚡ Qwen3.7-Flash

**Sumber resmi:** OpenRouter + Aliyun Model Studio (百炼) + platform.qianwenai.com

| Aspek | Detail |
|---|---|
| Positioning | **Vision-language reasoning model** Alibaba — "能看、能想、能动手" (bisa lihat, berpikir, bertindak) |
| Modality | 🖼️ **Text + Image + Video → Text** (multimodal!) |
| Context | **1M tokens**, max output 64K |
| Rilis | 28 Jul 2026 (slug `qwen3.7-flash-20260727`) |
| Use case resmi | **Multimodal agents, visual coding, search, computer interaction** — kuat di object recognition, spatial understanding, real-world visual perception |
| Capability dasar | Creative writing, math/logic, code development, info QA, text translation |
| Tool use | ✅ Tools, reasoning, response_format, seed, logprobs |
| Harga | Sangat murah: **$0.03/M input, $0.13/M output** (cache read $0.006/M) |
| Performa real | Latency 0.91s (P50), ~38 tps, uptime 99.99% (Alibaba Cloud) |

**Kesimpulan:** model **multimodal agent** — input gambar & video, reasoning, tool calling, context 1M, harga murah. Penerus Qwen3-VL lineage dengan kemampuan agentic.

## 🤖 Tencent Hy3

**Sumber resmi:** HF model card `tencent/Hy3` + OpenRouter

| Property | Nilai |
|---|---|
| Developer | **Tencent Hy Team** (腾讯混元) |
| Arsitektur | Sparse MoE |
| Total Params | **295B** |
| Active Params | **21B** (top-8 dari 192 experts) |
| MTP Layer | 3.8B (1 layer) |
| Layers | 80 (GQA, 64 heads, 8 KV heads, head dim 128) |
| Context | **256K** |
| License | **Apache 2.0** (open-source!) |
| Precision | BF16 (ada varian FP8) |

**Capability inti:**
- **Reasoning kuat** — configurable reasoning effort (disabled/low/high). 21B aktif tapi kompetitif dengan flagship 2-5x lebih besar
- **Agentic workflows** — keunggulan utama:
  - **Stability tool calls & output format** — production-grade, error recovery bagus, generalizes across scaffolding (CodeBuddy, Cline, KiloCode — SWE-Bench variance < 4%)
  - Dari feedback 50+ produk Tencent
- **Anti-hallucination**: hallucination rate turun **12.5% → 5.4%**, commonsense error **25.4% → 12.7%**
- **Long-context & multi-turn**: issue rate turun **17.4% → 7.9%**; kuat di long-dialogue (MRCR)
- **Productivity**: coding, office work, **financial modeling**, **frontend design**, **game development**
- **Benchmark**: blind eval 270 experts → **2.67/4** > GLM-5.1 (2.51/4)

**Harga (OpenRouter):** $0.132/M input, $0.528/M output, cache read $0.033/M

**Catatan:** text-only (bukan multimodal). Open-source Apache 2.0 → bisa self-host (vLLM/SGLang, ada guide finetuning & RL). Ada varian **hy3-preview** (April, lebih murah: $0.063/$0.21).

## 🆚 Comparison

| Model | Total/Active | Context | Fokus | Modalitas | Harga in/out per 1M |
|---|---|---|---|---|---|
| **M2.7-highspeed** | ~172B/? | 200K | Coding cepat & refactoring | Text | $0.25/$1 |
| **Qwen3.7-Flash** | ? | **1M** | Agent multimodal & visual | Text+Img+Vid | **$0.03/$0.13** |
| **Hy3** | 295B/21B | 256K | Agentic + reliability + anti-hallucination | Text | $0.132/$0.528 |
