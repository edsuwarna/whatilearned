# Mem0 vs Honcho: External Memory Providers for Hermes Agent

Hermes Agent ships with a built-in memory system (`MEMORY.md` + `USER.md`) that injects persistent facts into every turn of conversation. But for agents that need richer recall — cross-session context, entity tracking, or long-term knowledge graphs — Hermes supports **8 external memory provider plugins**: Honcho, OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, and Supermemory.

This article compares the two most popular choices: **Mem0** and **Honcho**. Both are native Hermes plugins, both are open-source, and both solve the same fundamental problem — but their architectures, tradeoffs, and ideal use cases differ substantially.

---

## Quick Comparison

| Dimension | Mem0 | Honcho |
|---|---|---|
| **Approach** | Knowledge graph + vector embeddings | Conversation state + user identity |
| **Hosting** | Cloud (free tier) + self-host | Self-host only |
| **Cloud free tier** | Yes — 10k adds/mo, 1k searches/mo | N/A |
| **GitHub stars** | ~23k | ~6.3k |
| **Backend** | pgvector (PostgreSQL), Qdrant, or managed | PostgreSQL |
| **Hermes plugin** | Native (one of 8 bundled) | Native (one of 8 bundled) |
| **Python SDK** | Yes (`mem0ai`) | Yes (`honcho`) |
| **API style** | add/search/update/delete memories | create sessions, add messages, apply derivers |
| **Best for** | Fact extraction, knowledge retrieval | User state continuity, identity tracking |

---

## Mem0: The Knowledge Graph Approach

Mem0 treats memory as a **structured knowledge base**. When you add a memory, it doesn't just store raw text — it extracts entities, resolves relationships, and embeds everything into a vector database for semantic search.

### Architecture

```
User Message → Mem0 Client → Embedding Model (e.g., OpenAI)
                                   ↓
                            Vector Search (pgvector/Qdrant)
                                   ↓
                            Structured Memories (entities, facts, metadata)
```

- **Memory types**: Facts, preferences, entities, temporal context
- **Search**: Hybrid (semantic + keyword) for high recall
- **Entity extraction**: Automatically identifies people, tools, projects, and their relationships

### Hermes Integration

Enable Mem0 in Hermes with:

```bash
hermes config set memory.provider mem0
```

For the managed cloud free tier, sign up at [app.mem0.ai](https://app.mem0.ai) and set your API key:

```bash
export MEM0_API_KEY="your-key"
```

For self-hosted, a Docker Compose stack ships with the Mem0 OSS repo — PostgreSQL with pgvector, REST API on port 8888, and an optional web dashboard on port 3000.

### Pricing (Managed Cloud)

| Tier | Price | Memory Adds | Searches | Projects |
|---|---|---|---|---|
| Hobby | Free | 10,000/mo | 1,000/mo | 1 |
| Pro | $99/mo | 100,000/mo | 10,000/mo | Unlimited |
| Team | Custom | Custom | Custom | Unlimited |

Hobby tier is generous enough for a single Hermes agent doing moderate daily usage (~333 adds and ~33 searches per day).

### Pros

- **Zero-infra option**: Free cloud tier means you can have external memory without running any server
- **Smart extraction**: Automatically pulls out entities and facts, not just raw text
- **Hybrid search**: Semantic + keyword gives higher accuracy than vector-only search
- **Large community**: 23k GitHub stars, active development, frequent releases
- **Hermes native**: First-class plugin, no adapter code needed

### Cons

- **Cloud dependency (free tier)**: If Mem0's cloud is down, so is your agent's memory. Self-host escapes this but adds infra burden
- **Embedding costs**: Every memory add and search consumes embedding API calls — if you use OpenAI embeddings, that's an extra cost on top of Mem0 itself
- **Less conversation-aware**: Designed for facts, not dialog flow. It knows *what* you said but loses the *narrative arc* of conversations
- **Agent-mode lock-in**: Mem0 CLI's `mem0 init --agent` creates email-less orphan accounts with no dashboard access. You need `mem0 init --email` to claim them

---

## Honcho: The Conversation-Centric Approach

Honcho views memory through the lens of **conversations and user identity**. Rather than extracting facts into a graph, it stores raw dialog sessions and applies *derivers* — transformation pipelines that process conversation history into structured memory representations.

### Architecture

```
User Message → Honcho Client → Session Storage (PostgreSQL)
                                      ↓
                               Derivers (identity, summary, memory)
                                      ↓
                               Structured State (user profile, session context)
```

- **Core concepts**: Users, Sessions, Messages, Metamessages, Derivers
- **Derivers**: Python classes that process dialog — built-in ones handle identity extraction, conversation summarization, and memory consolidation
- **State management**: Each user has persistent state across sessions — the agent remembers who you are across days, not just facts

### Hermes Integration

Enable Honcho in Hermes with:

```bash
hermes config set memory.provider honcho
```

Honcho requires a running PostgreSQL instance and its own API server. Set the connection:

```bash
export HONCHO_BASE_URL="http://localhost:8000"
```

Since it's self-hosted only, you need to run the server yourself. The [Honcho repo](https://github.com/plastic-labs/honcho) includes Docker Compose setups.

### Pros

- **Conversation-native**: Models context as flowing dialog, not static facts — better for agents that need to understand narrative
- **User identity**: Persistent user profiles across sessions — the agent remembers *who* you are, not just disconnected preferences
- **Deriver system**: Extensible pipeline for transforming raw conversation into useful representations
- **Self-hosted privacy**: All your conversation data stays on your infrastructure
- **Hermes native**: Also a first-class plugin, same integration quality as Mem0

### Cons

- **No free cloud tier**: You must self-host — PostgreSQL + Honcho server + maintenance
- **Smaller community**: ~6.3k GitHub stars vs Mem0's 23k — fewer third-party integrations, slower ecosystem growth
- **Higher setup cost**: Requires running and maintaining a PostgreSQL database plus the Honcho API server
- **No built-in vector search**: Facts are stored in relational tables — semantic search requires additional tooling
- **Less entity-aware**: Won't automatically connect "Endang" the user with "Hermes" the agent and "SumoPod" the provider into a graph

---

## Token Economics: Built-in vs External Memory

A key consideration: Hermes' built-in `MEMORY.md`/`USER.md` is injected into *every single turn's* system prompt. At ~4 characters per token, the default limits (2,200 chars memory + 1,375 chars user) cost roughly **900 input tokens per turn**, every turn, forever.

External providers like Mem0 and Honcho change the economics: instead of injecting everything every turn, they query on-demand and inject only *relevant* memories. For sessions with thousands of accumulated facts, this is dramatically cheaper.

| Approach | Cost per turn | Latency | Infra needed |
|---|---|---|---|
| Built-in (MEMORY.md) | ~900 tokens (constant) | 0ms | None |
| Mem0 (cloud free) | ~100-500 tokens (grows with recall) | 50-200ms | None |
| Mem0 (self-host) | ~100-500 tokens + embedding cost | 10-50ms | Docker Compose + pgvector |
| Honcho (self-host) | ~100-500 tokens | 10-50ms | PostgreSQL + Honcho server |

---

## Which One Should You Choose?

### Choose Mem0 if:

- You want **zero infrastructure** — sign up, set an API key, done
- Your agent needs **factual recall** — "what model did I use last time?" or "what's the SumoPod pricing?"
- You value **entity relationships** — automatically connecting users, tools, and projects
- You're okay with a **cloud dependency** (for the free tier) or comfortable self-hosting with pgvector

### Choose Honcho if:

- You need **conversation continuity** — the agent should remember the flow of a multi-day debugging session, not just isolated facts
- **Privacy is critical** — all data stays on your server, period
- You want **user identity tracking** — distinct profiles for different team members using the same agent
- You're willing to **run and maintain** PostgreSQL + Honcho server

### Choose Neither (stick with built-in MEMORY.md) if:

- Your memory fits comfortably under the default 2,200 character limit
- You don't need cross-session recall beyond what files can store
- You want zero latency and zero external dependencies
- Your agent runs simple cron jobs, not long-running interactive sessions

---

## Practical Example: Hermes + Mem0 Setup

Here's a minimal setup to get Mem0 running with Hermes in under 5 minutes:

```bash
# 1. Sign up and get an API key
#    Go to https://app.mem0.ai → create project → copy API key

# 2. Set the key
export MEM0_API_KEY="m0-your-key-here"

# 3. Tell Hermes to use Mem0
hermes config set memory.provider mem0

# 4. Test it
hermes run "remember that my server runs on Ubuntu 24.04 and my name is Endang"
```

From that point on, Hermes injects relevant Mem0 memories alongside your built-in MEMORY.md every turn. You can browse stored memories at [app.mem0.ai/dashboard](https://app.mem0.ai).

---

## Practical Example: Hermes + Honcho Setup

Setting up Honcho takes more work but gives full data sovereignty:

```bash
# 1. Clone and start Honcho
git clone https://github.com/plastic-labs/honcho.git
cd honcho
docker compose up -d

# 2. Set the base URL
export HONCHO_BASE_URL="http://localhost:8000"

# 3. Tell Hermes to use Honcho
hermes config set memory.provider honcho

# 4. Test it
hermes run "create a session for user 'endang' and remember that I prefer short answers"
```

Honcho will track user identity across sessions — so even if you start a fresh Hermes session tomorrow, it knows you're the same "endang" who prefers concise responses.

---

## The Bottom Line

Both Mem0 and Honcho are solid, production-grade memory layers with native Hermes integration. The choice comes down to a single question: **do you want your agent to remember facts, or remember people?**

Mem0 for facts. Honcho for identity. And if you only need a few hundred characters of persistent context, built-in MEMORY.md remains the simplest, fastest option — no extra infrastructure, no API keys, no moving parts.
