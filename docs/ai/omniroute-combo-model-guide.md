---
title: Building OmniRoute Combos — Free & Budget Model Categorization
description: How to group free/cheap LLMs (DeepSeek, MiniMax, MiMo, Qwen) into OmniRoute auto/ combos — primary + fallback patterns, use-case fit, and 6 ready-made combo designs.
---

# Building OmniRoute Combos — Free & Budget Model Categorization

> **Last updated:** 2026-08-01
> **Source:** OmniRoute gateway catalog + capability research from this repo's AI articles

Panduan mengelompokkan model free/murah ke combo OmniRoute (`auto/*`). Combo dibuat via **dashboard → Combos → Create Combo** (API `/api/combos` butuh admin key terpisah dari /v1 key).

## Table of Contents

- [🗂️ Model Categorization](#model-categorization)
- [🎯 Recommended Combos](#recommended-combos)
- [💡 Combo Design Strategy](#combo-design-strategy)

## 🗂️ Model Categorization

| Model | Kategori | Kekuatan Utama | Context | Modalitas |
|---|---|---|---|---|
| **DeepSeek V4 Flash** | ⚡ Fast/cheap workhorse | Latensi rendah, murah, general | 1M | Text |
| **DeepSeek V4 Pro** | 🧠 Reasoning kuat | Penalaran dalam, math, agentic | 1M | Text |
| **MiniMax M3** | 🖥️ Coding + multimodal | Frontier coding, 1M ctx, vision | 1M | Text + Image |
| **MiniMax M2.7-highspeed** | ⚡ Coding cepat | Polyglot code, refactoring, low latency | 200K | Text |
| **MiMo V2.5** | 🎬 Omnimodal | Text+Image+Video+Audio, 1M ctx | 1M | Text+Img+Vid+Aud |
| **MiMo V2.5 Pro** | 🧠 Agentic raksasa | 1.02T params, agentic, software eng | 1M | Text |
| **Qwen3.7-Flash** | 🖼️ Multimodal agent | Vision-language, murah, tool calling | 1M | Text+Img+Vid |

## 🎯 Recommended Combos

### 1. `auto/mimo-vision` — Omnimodal agent combo
- **MiMo V2.5** (utama) + fallback **Qwen3.7-Flash** + fallback **MiniMax M3**
- Buat: analisis gambar/video/audio, dokumen multimodal, agent yang perlu paham dunia visual+audio
- Paling unik — tidak ada model lain yang bisa audio+video dalam satu model

### 2. `auto/cheap-coding` — Coding hemat combo
- **DeepSeek V4 Flash** (utama) + **Qwen3.7-Flash** + fallback **MiMo V2.5 Pro**
- Buat: coding generasi/refactor budget-friendly tanpa reasoning berat
- Qwen3.7-Flash cuma $0.03/M input — termurah buat coding

### 3. `auto/pro-agent` — Agentic task combo
- **MiMo V2.5 Pro** (utama) + fallback **DeepSeek V4 Pro** + **MiniMax M2.7-highspeed**
- Buat: agent complex multi-step, software engineering, long-horizon task
- V2.5 Pro 1T params paling kuat agentic; V4 Pro reasoning; M2.7-highspeed respons cepat

### 4. `auto/vision-fast` — Vision cepat combo
- **Qwen3.7-Flash** (utama) + **MiniMax M3** (fallback)
- Buat: OCR, screenshot analysis, visual QA — cepat & murah
- Dua-duanya vision-capable; Qwen lebih murah, M3 lebih kuat

### 5. `auto/balanced-multimodal` — Serba bisa combo
- **MiniMax M3** (utama) + **MiMo V2.5** + **DeepSeek V4 Pro**
- Buat: daily driver — campuran coding, vision, reasoning

### 6. Perbaikan combo existing
- **`auto/best-coding`** → tambah **MiniMax M3** + **MiMo V2.5 Pro** sebagai kandidat
- **`auto/best-vision`** → tambah **Qwen3.7-Flash** + **MiMo V2.5**
- **`auto/best-free`** → tambah **DeepSeek V4 Flash free** + **Qwen3.7-Flash**

## 💡 Combo Design Strategy

1. **Satu primary + 2-3 fallback** — kalau primary down/mahal, auto-switch ke setara
2. **Utamakan model paling murah untuk task itu** — coding ringan pakai V4 Flash/Qwen3.7-Flash, jangan V2.5 Pro
3. **Pisah vision vs text-only** — jangan campur M2.7-highspeed (text) ke combo yang butuh gambar
4. **Prefix `noc/` untuk free tier** — combo hemat biaya total
