---
title: Open-Source & Budget AI Models — NVIDIA NIM Catalog (2026)
description: Capability deep-dive of 7 models available on NVIDIA NIM — Gemma 4, Step-3.7-Flash, GPT-OSS, and Llama 3.x — architecture, context, modality, and use-case fit.
---

# Open-Source & Budget AI Models — NVIDIA NIM Catalog

> **Last updated:** 2026-08-01
> **Source:** NVIDIA NIM (integrate.api.nvidia.com) + Hugging Face model cards

Roundup of free/mit-licensed LLMs exposed via NVIDIA's NIM endpoint. All 7 verified present in the catalog (102 models total). Two surprises: **Gemma-4 and Step-3.7 are actually multimodal** (image-text-to-text), not text-only.

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

*Multimodal generasi terbaru Google — image + video*

- Input: teks + gambar + **video sebagai frame (hingga 60 detik @ 1fps)**
- 140+ bahasa, 256K context, reasoning mode (`enable_thinking`)
- **Visual token budget** configurable (70–1120): budget rendah → caption/video, tinggi → OCR/dokumen
- Hybrid attention: sliding window + global attention + p-RoPE → kuat long-context
- Use case: reasoning, agentic, coding, OCR, document parsing, video understanding
- ⚠️ `google/gemma-4-31B-it` di HF = `image-text-to-text` — **bukan text-only**

## ⚡ stepfun-ai/step-3.7-flash

*MoE vision-language dari StepFun — speed gila*

- 198B total tapi hanya ~11B aktif per token → speed kelas 11B, intelligence kelas 100B+
- **MTP-3** (3-way Multi-Token Prediction): 100–300 tok/s, peak 350 tok/s untuk coding
- Vision module 728×728 px — cocok baca screenshot/UI
- Use case: multimodal understanding, **GUI automation** (baca screenshot), coding/frontend generation, tool calling, agentic
- Positioning: "mini GPT-4o versi open-source"

## 🧠 openai/gpt-oss-120b

*Reasoning model open-weight OpenAI*

- Full chain-of-thought (CoT bisa dibaca untuk debugging), **reasoning effort configurable** (low/med/high)
- Tool use: function calling, web browsing, python execution, structured outputs
- 117B / 5.7B active → muat di **1× H100**, native MXFP4 quantization
- Benchmark (NVIDIA card, high reasoning): **2622 elo with tools** vs 2516 tanpa tools
- **Text-only**

## 🚀 openai/gpt-oss-20b

- Arsitektur & kemampuan reasoning identik dengan 120b, tapi 20B total / 4B active
- Latency rendah → cocok local/specialized deployment
- Kompatibel **OpenAI Responses API** + structured output

## 📚 meta/llama-3.1-70b-instruct

- Dense 70B, tool/function calling, JSON mode
- 8 bahasa utama (EN, DE, FR, IT, PT, HI, ES, TH)
- Solid untuk production RAG/agent, tapi generasi 2024

## 🐣 meta/llama-3.1-8b-instruct

- 8B dense, 128K context, function calling
- Untuk edge/local, latency kritis, atau baseline murah

## 👁️ meta/llama-3.2-11b-vision-instruct

- Text + image input, text output
- Use case: image captioning, document QA, OCR, visual reasoning
- License Llama 3.2 (komersial OK, syarat >700M MAU)

## 💡 Quick Recommendations

| Kebutuhan | Model |
|---|---|
| Vision + video + reasoning, GPU biasa | **gemma-4-31b-it** |
| Screenshot/UI agent + speed tinggi | **step-3.7-flash** |
| Reasoning/agent production text-only, 1 GPU | **gpt-oss-120b** |
| Latency rendah text reasoning | **gpt-oss-20b** |
| OCR/vision ringan | **llama-3.2-11b-vision** |
| RAG/chat stabil murah | **llama-3.1-8b** |

> **TL;DR:** Yang paling menarik: **gemma-4-31b-it** (multimodal + video + 256K, Apache 2.0) dan **step-3.7-flash** (MoE 198B speed gila). Dua-duanya gratis via API trial NVIDIA (integrate.api.nvidia.com) — tinggal bikin API key di build.nvidia.com.
