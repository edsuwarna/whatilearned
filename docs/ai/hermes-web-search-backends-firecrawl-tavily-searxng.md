# Web Search & Extract Backends for Hermes Agent: Firecrawl, Tavily, and SearXNG + Crawl4AI

Hermes Agent has two model-callable web tools — `web_search` (ranked results from the internet) and `web_extract` (readable content from URLs). These tools are what let an agent research, verify facts, pull documentation, and stay current beyond its training cutoff. Without a backend configured, both tools return: *"No web search provider configured."*

Hermes ships with **8 backend plugins**: Firecrawl, Tavily, SearXNG, Exa, Brave, DDGS, Parallel, and xAI (Grok). This article focuses on the three approaches that make sense for real-world setups:

1. **Firecrawl** — premium all-in-one (search + extract), Hermes default
2. **Tavily** — balanced all-in-one, AI-native search
3. **SearXNG + Crawl4AI** — fully self-hosted, zero cost stack

---

## Provider Capability Matrix

| Provider | Search | Extract | Free Tier | Self-Hostable |
|---|---|---|---|---|
| **Firecrawl** | ✔ | ✔ | 500 credits/mo | Yes (OSS) |
| **Tavily** | ✔ | ✔ | 1,000 calls/mo | No |
| Exa | ✔ | ✔ | 1,000 searches/mo | No |
| Parallel | ✔ | ✔ | Paid only | No |
| **SearXNG** | ✔ | — | Free (self-hosted) | Yes |
| Brave | ✔ | — | 2,000 queries/mo | No |
| DDGS | ✔ | — | Free (no key) | No |
| xAI (Grok) | ✔ | — | Paid | No |

Search-only providers (SearXNG, Brave, DDGS, xAI) **must be paired** with an extract provider (Firecrawl/Tavily/Exa/Parallel) for full search + extract functionality. Hermes allows per-capability splitting — you can set a different backend for search vs extract.

---

## Approach 1: Firecrawl — The Premium All-in-One

Firecrawl is Hermes' **default** backend and the most full-featured option. It handles both search and extract with a single API key, and the underlying engine is open-source (159k+ GitHub stars).

### What It Does

- **Search**: Web search with customizable depth, country/language filtering, and domain allow/block
- **Extract**: Full page extraction into clean markdown, handles JavaScript rendering, bypasses anti-bot protections
- **Scrape**: Structured extraction via LLM-guided schemas — pull specific data points from any page
- **Map**: Crawl entire websites and return all URLs (site discovery)
- **Crawl**: Deep multi-page crawls with automatic retry and rate limiting

### Pricing

| Tier | Price | Credits | Best For |
|---|---|---|---|
| Free | $0 | 500/mo | Testing, one-off research |
| Hobby | $19/mo | 3,000/mo | Personal agents, light use |
| Standard | $99/mo | 30,000/mo | Production agents |
| Growth | $249/mo | 100,000/mo | Teams, heavy research |
| Enterprise | Custom | Custom | Organization-wide |

One credit ≈ one search or one page scrape. The free tier's 500 credits is ~16 searches per day — fine for testing but tight for a daily driver agent.

### Hermes Setup

```bash
# 1. Get API key from https://firecrawl.dev → sign up → API Keys
export FIRECRAWL_API_KEY="fc-your-key-here"

# 2. Firecrawl is the default, but you can explicitly set it:
hermes config set web.firecrawl_api_key "$FIRECRAWL_API_KEY"

# 3. Verify
hermes tools  # → Web Search & Extract → should show Firecrawl as active
```

Or use `hermes tools` to select Firecrawl interactively.

### Pros

- **Hermes default**: Zero-config integration, best-tested path
- **All-in-one**: Search + extract with one provider, no pairing needed
- **JavaScript rendering**: Handles SPA/React sites that other extractors miss
- **Anti-bot bypass**: Smart about rotating IPs and respecting rate limits
- **Open-source core**: Self-host if you outgrow the cloud API
- **Structured extraction**: LLM-guided schema extraction (`/extract`) for pulling specific data

### Cons

- **Tight free tier**: 500 credits/month runs out fast
- **Closed-source cloud**: Managed API is proprietary; self-hosted is possible but heavier
- **Price jumps sharply**: $19 → $99 between Hobby and Standard
- **Overkill for simple searches**: If you just need a few text search results, you're paying for JS rendering you don't use

---

## Approach 2: Tavily — The AI-Native Search

Tavily is built from the ground up for AI agent consumption. Unlike general-purpose search APIs, Tavily's results are optimized for LLM context windows — concise, relevant, and structured.

### What It Does

- **Search**: AI-optimized web search returning clean results with content snippets, relevance scores, and raw content extraction in a single call
- **Extract**: Built into search results — `include_raw_content=true` returns the full extracted text alongside search snippets
- **Context building**: Designed to minimize tokens while maximizing relevance — no ads, no SEO spam, no junk
- **Depth control**: `basic` (fast, 1 credit) vs `advanced` (deeper, 2 credits) search depth

### Pricing

| Tier | Price | API Calls | Credit System |
|---|---|---|---|
| Free | $0 | 1,000/mo | 1 call = 1 credit (basic), 2 credits (advanced) |
| Researcher | $20/mo | 5,000/mo | 1 call = 1 credit |
| Researcher Pro | $80/mo | 25,000/mo | 1 call = 1 credit |
| Enterprise | Custom | Custom | Custom |

The free tier's 1,000 calls/month is generous — ~33 searches per day, more than double Firecrawl's free tier.

### Hermes Setup

```bash
# 1. Get API key from https://tavily.com → sign up → dashboard
export TAVILY_API_KEY="tvly-your-key-here"

# 2. Set Tavily as the search backend
hermes config set web.tavily_api_key "$TAVILY_API_KEY"

# 3. Select Tavily via hermes tools
hermes tools  # → Web Search & Extract → choose Tavily
```

With Tavily handling both search and extract, no pairing is needed. But if you want Tavily search + Firecrawl extract as a hybrid:

```bash
export TAVILY_API_KEY="tvly-..."
export FIRECRAWL_API_KEY="fc-..."
# In hermes tools → set search=Tavily, extract=Firecrawl
```

### Pros

- **AI-native**: Results are designed for LLM consumption, not human browsing — cleaner, more relevant
- **Single-call extract**: `include_raw_content` pulls full page text alongside search results
- **Generous free tier**: 1,000 calls/mo is practical for daily use
- **Built for agents**: Domain filtering, result count control, score filtering — knobs agents actually need
- **Low latency**: Optimized API, fast responses ideal for agent loops

### Cons

- **No self-host option**: Cloud-only, your data goes through Tavily's servers
- **No JS rendering**: Cannot extract from JavaScript-heavy SPA sites
- **Black-box relevance**: You can't tune the search ranking algorithm
- **Less powerful extract**: Raw content extraction is basic — no structured schemas, no LLM-guided parsing like Firecrawl
- **Newer entrant**: Smaller ecosystem than Firecrawl, fewer integrations beyond the core AI agent space

---

## Approach 3: SearXNG + Crawl4AI — The Self-Hosted Zero-Cost Stack

For users who want full data sovereignty and zero recurring API costs, pairing **SearXNG** (metasearch engine) with **Crawl4AI** (LLM-friendly web scraper) creates a completely free, self-hosted pipeline. The tradeoff: you run the infrastructure.

### Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Hermes     │────▶│   SearXNG    │────▶│  70+ Search  │
│  web_search  │     │  (Docker)    │     │   Engines    │
└──────┬───────┘     └──────────────┘     └──────────────┘
       │
       │ web_extract
       ▼
┌──────────────┐     ┌──────────────┐
│   Hermes     │────▶│  Crawl4AI    │
│  web_extract │     │  (Python)    │
└──────────────┘     └──────────────┘
```

### SearXNG — The Search Half

SearXNG is a privacy-respecting metasearch engine that aggregates results from 274+ search engines. It exposes a JSON API that Hermes can consume directly.

**Key facts:**
- Aggregates Google, Bing, DuckDuckGo, Brave, and 270+ others simultaneously
- Self-hosted via Docker — one `docker compose up`
- JSON API must be enabled (`search.formats` includes `json`)
- Zero API keys, zero rate limits, zero costs
- Built-in caching reduces upstream calls

**Docker Compose snippet:**

```yaml
services:
  searxng:
    image: searxng/searxng:latest
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng
    environment:
      - SEARXNG_BASE_URL=https://search.yourdomain.com
```

In `settings.yml`, enable JSON:

```yaml
search:
  formats:
    - html
    - json
```

**Hermes config:**

```bash
export SEARXNG_URL="http://localhost:8080"
hermes config set web.searxng_url "$SEARXNG_URL"
# In hermes tools → set search=SearXNG
```

### Crawl4AI — The Extract Half

Crawl4AI (75.8k GitHub stars) is an open-source Python library purpose-built for LLM-friendly web scraping. It's not just another HTTP client — it renders JavaScript, extracts clean markdown, and structures content for AI consumption.

**Key facts:**
- Full browser rendering via Playwright — handles SPAs, lazy-loaded content, auth walls
- Output formats: raw HTML, clean markdown, structured JSON, screenshot
- LLM-friendly extraction strategies: CSS selectors, XPath, LLM-guided extraction, cosine similarity
- Fits > 95% of LLM use cases without extra parsing
- Python API — can be wrapped into an HTTP endpoint for Hermes

**Hermes integration note:** Crawl4AI is **not** a native Hermes backend plugin. The integration path is:

1. Deploy Crawl4AI as a microservice exposing a REST endpoint
2. Write a 50-line adapter script that translates Hermes `web_extract` calls to Crawl4AI
3. Register the adapter as a custom extract backend

Alternatively, pair SearXNG search with **Tavily's free extract-only** tier (or use Firecrawl's free tier for extract while SearXNG handles search) to avoid building the adapter.

**Quick Crawl4AI usage:**

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def extract(url: str) -> str:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown  # Clean, LLM-ready output

# Wrap as HTTP API for Hermes to call
```

### Pros

- **Zero cost forever**: No API keys, no credits, no monthly bills
- **Full data sovereignty**: Every query, every crawl, every result stays on your server
- **No rate limits**: You control the throttle; search as much as you want
- **SearXNG breadth**: 274+ search engines aggregated means no single-source bias
- **Crawl4AI depth**: Full browser rendering beats any API-only extractor for JS-heavy sites
- **Privacy-respecting**: SearXNG strips tracking, no query logging

### Cons

- **Infrastructure burden**: Two Docker services to maintain, monitor, and update
- **No native Hermes extract plugin for Crawl4AI**: Requires a custom adapter script or hybrid pairing
- **Latency**: SearXNG aggregates multiple engines (slower than a single-API call), Crawl4AI renders full pages (slower than lightweight HTTP extract)
- **SearXNG result quality varies**: Depends on which engines are enabled and their current health
- **Google/Cloudflare may block**: Self-hosted scrapers without residential IPs can get captcha'd on aggressive sites
- **Maintenance**: Search engines change their HTML — SearXNG needs regular updates; Crawl4AI's Playwright browser needs occasional restarts

---

## Hybrid Setups: Mix and Match

Hermes supports **per-capability backend selection** — different providers for search vs extract. This unlocks cost-optimized combinations:

### Budget Hybrid: SearXNG Search + Tavily Free Extract

```bash
# Free search via SearXNG
export SEARXNG_URL="http://localhost:8080"

# Free extract via Tavily (1,000 calls/mo)
export TAVILY_API_KEY="tvly-..."

# In hermes tools: search=SearXNG, extract=Tavily
```

**Cost: $0/month** (staying within Tavily's free tier). SearXNG handles all searches for free; Tavily handles extracts that fit within 1,000 calls/month.

### Premium Hybrid: Tavily Search + Firecrawl Extract

```bash
# Fast AI-native search via Tavily
export TAVILY_API_KEY="tvly-..."

# Deep JS-aware extract via Firecrawl
export FIRECRAWL_API_KEY="fc-..."

# In hermes tools: search=Tavily, extract=Firecrawl
```

**Cost: $0-$39/month** (depending on free tier usage). Gets the best of both: Tavily's AI-optimized search speed + Firecrawl's deep extraction with JS rendering.

### Privacy Hybrid: SearXNG Search + Firecrawl Extract

```bash
export SEARXNG_URL="http://localhost:8080"
export FIRECRAWL_API_KEY="fc-..."

# In hermes tools: search=SearXNG, extract=Firecrawl
```

**Cost: $0-$19/month**. SearXNG keeps search queries private; Firecrawl handles the heavy lifting on extraction with its anti-bot capabilities.

---

## Decision Guide: Which Approach Fits You?

### Choose Firecrawl if:
- You want **zero config** — it's the Hermes default, just set one env var
- You need **JavaScript rendering** for SPAs and modern sites
- You want **structured extraction** (LLM-guided schemas, not just raw text)
- You can afford **$19-$99/month** for production use
- You occasionally need **deep crawling** of entire websites

### Choose Tavily if:
- You want **AI-optimized results** — clean, relevant, no SEO spam
- You value **speed** — Tavily's API is the fastest of the three
- **Free tier is enough** — 1,000 calls/month covers moderate daily usage
- You're building an **agent that makes many quick searches** (not deep crawls)
- You want the simplest possible all-in-one: one API key, no pairing

### Choose SearXNG + Crawl4AI if:
- **Privacy is non-negotiable** — all queries and crawls stay on your metal
- You want **zero recurring cost** — pay once for the server, run forever
- You need **unlimited usage** — no credit counters, no rate limits
- You're comfortable **running Docker services** and writing a small adapter
- You need **274+ search engine coverage** — no single-provider blind spots

### Choose a Hybrid if:
- You want to **optimize cost vs capability** — free search, paid extract (or vice versa)
- Your **search and extract needs are asymmetric** — many searches, few extracts
- You want **defense in depth** — if one provider is down, swap to the other

---

## Practical: Bare-Minimum Setup for Each

### Firecrawl (30 seconds)

```bash
export FIRECRAWL_API_KEY="fc-..."
hermes run "search the web for latest Hermes Agent release notes"
```

### Tavily (30 seconds)

```bash
export TAVILY_API_KEY="tvly-..."
hermes tools  # → pick Tavily
hermes run "what's new in Python 3.13?"
```

### SearXNG + Firecrawl extract (5 minutes)

```bash
# Terminal 1: Start SearXNG
docker run -d -p 8080:8080 \
  -e SEARXNG_BASE_URL=http://localhost:8080 \
  searxng/searxng:latest
# Then enable JSON in http://localhost:8080 → settings → search.formats

# Terminal 2: Configure Hermes
export SEARXNG_URL="http://localhost:8080"
export FIRECRAWL_API_KEY="fc-..."
hermes tools  # → search=SearXNG, extract=Firecrawl
hermes run "find me recent articles about Rust async programming"
```

---

## Important: No Runtime Fallback

One critical detail from the Hermes docs: **there is no runtime cross-provider fallback**. If you set Tavily as your search backend and it returns 0 results, errors with 403, or times out — Hermes does NOT silently retry with SearXNG or Firecrawl. It returns the failure to the agent.

Fallback only happens at **config-resolution time**: if `web.search_provider` is unset, Hermes scans for the first provider with a valid API key. Set it explicitly, and you get exactly that provider — successes and failures alike.

This means hybrid setups with per-capability splitting are your only "fallback" strategy: SearXNG + Tavily means if SearXNG is slow, you can manually switch search to Tavily. But automatic failover requires external tooling (a load balancer or health-check proxy in front of your providers).

---

## The Bottom Line

Hermes gives you genuine choice in how your agent accesses the web. Firecrawl is the premium default — powerful but meter-aware. Tavily is the pragmatic sweet spot — AI-native, generous free tier, single-key simplicity. SearXNG + Crawl4AI is the self-hosting ideal — unlimited, private, and free, at the cost of infrastructure.

For most Hermes users starting out: **Tavily's free tier** (1,000 calls/month) + **Firecrawl free tier** (500 credits/month) as a hybrid gives you 1,500 monthly operations at $0 — enough to search and extract daily without hitting a single limit. From there, scale the one you hit first.
