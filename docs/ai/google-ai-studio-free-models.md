---
title: Google AI Studio — Free Tier Models & Limits
description: **Google AI Studio** (ai.google.dev) provides free access to Gemini models through the Gemini API. No credit card required — just a Google account.
---

# Google AI Studio — Free Tier Models & Limits

**Google AI Studio** (ai.google.dev) provides free access to Gemini models through the Gemini API. No credit card required — just a Google account.

> **Note**: Free tier has rate limits (RPD = Requests Per Day). These reset daily. If you exhaust your quota, you can either wait for reset or enable billing for pay-as-you-go.


## Table of Contents

- [📋 Free Models (June 2026)](#free-models-june-2026)
  - [Text & Multimodal Models](#text-multimodal-models)
  - [Specialized Models](#specialized-models)
  - [Deep Research (Free Preview)](#deep-research-free-preview)
- [⚡ Rate Limits & Quotas](#rate-limits-quotas)
- [🔌 API Access](#api-access)
  - [Get an API Key](#get-an-api-key)
  - [Using with OpenCode](#using-with-opencode)
  - [Using with 9Router](#using-with-9router)
- [🆚 Free Tier Comparison](#free-tier-comparison)
- [💡 Tips](#tips)
- [🔗 Related](#related)

---

## 📋 Free Models (June 2026)

### Text & Multimodal Models

| Model | Free Rate Limit | Notes |
|-------|----------------|-------|
| **Gemini 3.5 Flash** | ~1,500 RPD | Latest Flash — best speed/quality ratio |
| **Gemini 3.1 Flash** | ~1,500 RPD * | Shared quota with Flash-Lite |
| **Gemini 3.1 Flash-Lite** | ~1,500 RPD * | Cheapest tier, fastest |
| **Gemini 3 Flash Preview** | ~1,500 RPD | Preview model |
| **Gemini 2.5 Flash** | ~1,500 RPD | Stable, well-tested |
| **Gemini 2.5 Flash-Lite** | ~1,500 RPD | Lightweight variant |
| **Gemini 2.5 Pro** | **10,000 RPD** | Most generous — best for complex reasoning |
| **Gemini 2.0 Flash** | ~1,500 RPD | Legacy (being sunset) |
| **Gemini 2.0 Flash-Lite** | ~1,500 RPD | Legacy (being sunset) |

*\* Flash and Flash-Lite share a combined 1,500 RPD pool.*

### Specialized Models

| Model | Free Limit | Use Case |
|-------|-----------|----------|
| **Imagen** | Included | Image generation |
| **Gemini Embedding 001 / 2** | Included | Embeddings / vector search |
| **Veo 2.0 Generate 001** | Limited free | Video generation |
| **Veo 3.1 Lite Preview** | Limited free | Video generation (newer) |
| **Gemini 3.1 Flash TTS Preview** | ~1,500 RPD | Text-to-speech |
| **Gemini 2.5 Flash TTS Preview** | ~1,500 RPD | Text-to-speech |

### Deep Research (Free Preview)

| Model | Free Limit |
|-------|-----------|
| **Deep Research Preview 04-2026** | Limited free |
| **Deep Research Max Preview 04-2026** | Limited free |
| **Deep Research Pro Preview 12-2025** | Limited free |

---

## ⚡ Rate Limits & Quotas

Key limits to be aware of:

- **Flash series**: ~1,500 requests/day (shared across all Flash variants)
- **Gemini 2.5 Pro**: 10,000 requests/day — highest free quota
- **Grounding / Google Search**: 5,000 prompts/month free (shared across Gemini 3 models)
- **Rate limits** are more restrictive on preview models

When you hit a limit, the API returns a `429 RESOURCE_EXHAUSTED` error.

---

## 🔌 API Access

### Get an API Key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **Get API Key** in the left sidebar
3. Create a new key (or use existing)
4. Use it with any OpenAI-compatible client by pointing to:

```
https://generativelanguage.googleapis.com/v1beta/openai/
```

### Using with OpenCode

Configure in your OpenCode provider config:

```yaml
provider: openai
api_base: https://generativelanguage.googleapis.com/v1beta/openai/
api_key: YOUR_API_KEY
```

### Using with 9Router

Add as a provider in 9Router dashboard → Providers → Google AI Studio → paste API key.

---

## 🆚 Free Tier Comparison

| Aspect | Google AI Studio | OpenCode Free | Kiro AI |
|--------|-----------------|---------------|---------|
| **Models** | Gemini 2.5 Pro, Flash series | Auto-fetched | Claude 4.5, GLM-5, MiniMax |
| **Rate Limit** | 1,500–10,000 RPD | Varies | Unlimited |
| **Credit Card** | No | No | No |
| **Best For** | Reasoning (Pro) & speed (Flash) | Quick coding | Premium Claude access |

---

## 💡 Tips

- **Use Gemini 2.5 Pro** (10k RPD) for deep reasoning, code analysis, and complex debugging
- **Use Gemini 3.5 Flash** (1.5k RPD) for quick Q&A, summarization, and everyday tasks
- **API key is free** — you only pay if you enable billing and exceed free tier
- **Context window**: Flash models support up to 1M tokens; Pro models up to 2M tokens
- **Grounding**: Free search grounding up to 5,000 prompts/month across all Gemini 3 models

---

## 🔗 Related

- [9Router — Free AI Router](9router-free-ai-router.md)
- [OpenCode Daily Use Cases](opencode-daily-use-cases.md)
- [Google AI Studio Docs](https://ai.google.dev/gemini-api/docs)
