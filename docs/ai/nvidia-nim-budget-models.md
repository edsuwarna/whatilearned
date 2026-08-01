---
title: Open-Source & Budget AI Models — NVIDIA NIM Catalog (2026)
description: Capability deep-dive of 7 models available on NVIDIA NIM — Gemma 4, Step-3.7-Flash, GPT-OSS, and Llama 3.x — architecture, context, modality, and use-case fit.
---

# Open-Source & Budget AI Models — NVIDIA NIM Catalog

> **Last updated:** 2026-08-01
> **Source:** NVIDIA NIM (integrate.api.nvidia.com) + Hugging Face model cards

Roundup of free/open-licensed LLMs exposed via NVIDIA's NIM endpoint. All 7 verified present in the catalog (102 models total). Two surprises: **Gemma-4 and Step-3.7 are actually multimodal** (image-text-to-text), not text-only.

## Table of Contents

- [📊 Comparison Table](#comparison-table)
- [🤖 google/gemma-4-31b-it](#googlegemma-4-31b-it)
- [⚡ stepfun-ai/step-3.7-flash](#stepfun-aistep-37-flash)
- [🧠 openai/gpt-oss-120b](#openaigpt-oss-120b)
- [🚀 openai/gpt-oss-20b](#openaigpt-oss-20b)
- [📚 meta/llama-3.1-70b-instruct](#metallama-31-70b-instruct)
- [🐣 meta/llama-3.1-8b-instruct](#metallama-31-8b-instruct)
- [👁️ meta/llama-3.2-11b-vision-instruct](#metallama-32-11b-vision-instruct)
- [💡 Quick Recommendations](#quick-recommendations)

## 📊 Comparison Table

| Model | Architecture | Total / Active Params | Context | Modality | License |
|---|---|---|---|---|---|
| **gemma-4-31b-it** | Dense + hybrid attention | ~31B | **256K** | 🖼️ Text + **Image + Video** | Apache 2.0 |
| **step-3.7-flash** | Sparse MoE | 198B / ~11B active | **256K** | 🖼️ Text + **Image** | Apache 2.0 |
| **gpt-oss-120b** | MoE (K=4) | 117B / ~5.7B active | 128K | 💬 Text only | Apache 2.0 |
| **gpt-oss-20b** | MoE (K=4) | 20B / ~4B active | 128K | 💬 Text only | Apache 2.0 |
| **llama-3.1-70b-instruct** | Dense | 70.5B | 128K | 💬 Text only | Llama 3.1 |
| **llama-3.1-8b-instruct** | Dense | 8B | 128K | 💬 Text only | Llama 3.1 |
| **llama-3.2-11b-vision** | Dense (MLLaMA) | 10.7B | 128K | 🖼️ Text + **Image** | Llama 3.2 |

## 🤖 google/gemma-4-31b-it

*Google's newest multimodal generation — image + video*

- Input: text + image + **video as frames (up to 60 seconds @ 1fps)**
- 140+ languages, 256K context, reasoning mode (`enable_thinking`)
- **Configurable visual token budget** (70–1120): low budget → caption/video, high budget → OCR/documents
- Hybrid attention: sliding window + global attention + p-RoPE → strong long-context
- Use cases: reasoning, agentic, coding, OCR, document parsing, video understanding
- ⚠️ `google/gemma-4-31B-it` on HF = `image-text-to-text` — **not text-only**

## ⚡ stepfun-ai/step-3.7-flash

*StepFun's vision-language MoE — insane speed*

- 198B total but only ~11B active per token → 11B-class speed, 100B+ intelligence
- **MTP-3** (3-way Multi-Token Prediction): 100–300 tok/s, peak 350 tok/s for coding
- Vision module 728×728 px — great for reading screenshots/UI
- Use cases: multimodal understanding, **GUI automation** (reading screenshots), coding/frontend generation, tool calling, agentic
- Positioning: "open-source mini GPT-4o"

## 🧠 openai/gpt-oss-120b

*OpenAI's open-weight reasoning model*

- Full chain-of-thought (CoT readable for debugging), **configurable reasoning effort** (low/med/high)
- Tool use: function calling, web browsing, python execution, structured outputs
- 117B / 5.7B active → fits in **1× H100**, native MXFP4 quantization
- Benchmark (NVIDIA card, high reasoning): **2622 elo with tools** vs 2516 without
- **Text-only**

## 🚀 openai/gpt-oss-20b

- Same architecture & reasoning capabilities as the 120b, but 20B total / 4B active
- Low latency → good for local/specialized deployment
- Compatible with **OpenAI Responses API** + structured output

## 📚 meta/llama-3.1-70b-instruct

- Dense 70B, tool/function calling, JSON mode
- 8 major languages (EN, DE, FR, IT, PT, HI, ES, TH)
- Solid for production RAG/agents, but a 2024 generation

## 🐣 meta/llama-3.1-8b-instruct

- 8B dense, 128K context, function calling
- For edge/local, latency-critical, or cheap baseline workloads

## 👁️ meta/llama-3.2-11b-vision-instruct

- Text + image input, text output
- Use cases: image captioning, document QA, OCR, visual reasoning
- Llama 3.2 license (commercial OK, >700M MAU clause)

## 💡 Quick Recommendations

| Need | Model |
|---|---|
| Vision + video + reasoning on consumer GPU | **gemma-4-31b-it** |
| Screenshot/UI agent + high speed | **step-3.7-flash** |
| Text-only reasoning/agent production, 1 GPU | **gpt-oss-120b** |
| Low-latency text reasoning | **gpt-oss-20b** |
| Lightweight OCR/vision | **llama-3.2-11b-vision** |
| Stable cheap RAG/chat | **llama-3.1-8b** |

> **TL;DR:** Most interesting: **gemma-4-31b-it** (multimodal + video + 256K, Apache 2.0) and **step-3.7-flash** (198B MoE with insane speed). Both free via NVIDIA's trial API (integrate.api.nvidia.com) — just create an API key at build.nvidia.com.
