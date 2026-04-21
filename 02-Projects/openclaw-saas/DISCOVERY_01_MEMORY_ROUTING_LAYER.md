# Discovery Doc #1: Memory, Embedding & Routing Layer Architecture

> **Purpose:** Cross-channel research document. Use in Perplexity, Claude, ChatGPT, or hand to any research agent.
> **Created:** 2026-03-24 | **Author:** Ava (for Cem)
> **Status:** DISCOVERY — open questions, not decisions

---

## The Problem We're Solving

OpenClaw runs multiple sessions (DM, group topics, sub-agents). Each session has its own context window. **There is no shared real-time context across sessions.** This causes:

- Repeated context ("we already discussed this in the other thread")
- Conflicting actions (agent acts on stale info from a different session)
- Lost decisions (key choices made in one topic don't carry to another)
- User frustration (having to re-explain the same thing)

## Proposed Architecture: Flash Triage + Semantic Memory Layer

### Layer 1 — Semantic Memory (Embedding + Retrieval)
- **What it does:** Indexes ALL session transcripts, memory files, wiki, and cross-session state into a searchable vector store
- **Current setup:** QMD (local) with Gemini Embedding 2.0 + BM25 hybrid search
- **Key question:** Is Gemini Embedding 2.0 the best retrieval model for this use case? Or should we test OpenAI's `text-embedding-3-large` or Cohere's Embed v4?

### Layer 2 — Flash Router (Triage Agent)
- **What it does:** Receives EVERY inbound message. Before responding:
  1. Runs semantic search across all memory/sessions
  2. Builds a context packet from top results
  3. Classifies intent (strategy, analysis, lookup, code, creative)
  4. Routes to the right specialist agent with context attached
  5. Returns the specialist's response to the user
- **Model candidates for router:**

| Model | Cost (OAuth) | Cost (API) | Context | TTFT | Throughput | Best For |
|-------|-------------|------------|---------|------|------------|----------|
| GPT-5.4 nano | FREE | $0.20/$1.25 per 1M | ~128K? | Fast | TBD | Classification, sub-agent support |
| Gemini 3.1 Flash Lite | FREE | $0.25/$1.50 per 1M | 1M | Fastest (2.5x) | 363 tok/s | High-throughput routing |
| Gemini 3 Flash | FREE | $0.50/$3.00 per 1M | 1M | Fast | 146 tok/s | Stronger reasoning when needed |
| Claude Haiku 4.5 | $1.00/$5.00 | Same | 200K | 597ms TTFT | 79 tok/s | Instruction following, agentic |
| GPT-5.4 mini | FREE | $0.75/$4.50 per 1M | 400K | Fast | TBD | Coding agents, tool use |

### Layer 3 — Specialist Agents (Vertical Experts)
- Each agent has its own model, workspace, memory, and AGENTS.md
- Receives pre-built context from the router — doesn't need to search itself
- Reports results back to router for delivery to user

## Open Research Questions

### On Embeddings
1. Which embedding model has the best recall for **business context retrieval** (not just code/academic)?
2. Does Gemini Embedding 2.0 work well with non-Gemini LLMs reading the results? Or is there a benefit to matching provider (OpenAI embeddings → OpenAI router)?
3. What's the optimal chunk size for session transcripts? Current QMD default vs custom?
4. Should we use **reranking** after initial retrieval? (Cohere Rerank, Jina Reranker)
5. How do we handle **temporal relevance**? (Today's decisions > last week's decisions)

### On Routing
1. **GPT-5.4 nano vs Gemini Flash Lite** — which classifies intent more accurately after reading retrieved context? Needs head-to-head test.
2. How many tokens of context should the router receive? (Top 5 results? Top 10? Full cross-session state file?)
3. Should the router have a **lightweight AGENTS.md** that describes all available specialists and their capabilities?
4. What's the latency budget? User sends message → sees first token. Target: <2 seconds total (retrieval + classification + specialist TTFT).
5. Can the router handle **multi-agent orchestration**? (e.g., "Get me sales data AND generate lifestyle images" → dispatch to Atlas AND Sven2 in parallel)

### On Memory Coordination
1. Should each sub-agent write to its own memory, then a **coordinator agent** synthesizes?
2. Or should all agents write to a **shared memory bus** that the router reads?
3. How often should cross-session state be refreshed? Real-time? Every N minutes? On-demand?
4. What's the storage/indexing cost at scale? (100 sessions × 30 days × avg 50KB each = ~150MB of transcripts to index)

## Test Plan
1. Set up GPT-5.4 nano and Gemini Flash Lite as two router candidates
2. Feed both the same 20 test messages with pre-retrieved context
3. Measure: classification accuracy, latency, token usage, quality of context selection
4. Pick winner → implement as default router

## References
- [Macaron: Flash Lite vs GPT-4o Mini vs Haiku comparison](https://macaron.im/blog/gemini-flash-lite-vs-gpt4o-mini-vs-claude-haiku)
- [LLM Latency Benchmarks 2026](https://www.kunalganglani.com/blog/llm-api-latency-benchmarks-2026)
- [GPT-5.4 mini vs Gemini 3 Flash](https://www.aifreeapi.com/en/posts/gpt-5-4-mini-vs-gemini-3-flash)
- OpenClaw changelog 2026.3.22-23 — per-agent model defaults, thinking/reasoning per agent
- OpenClaw config schema: `agents.list.*.model`, `agents.list.*.thinkingDefault`, `agents.list.*.skills`

---

*Use this doc to prompt Perplexity, Claude, or any research tool. Key query seeds:*
- "Best embedding model for business context retrieval 2026"
- "GPT-5.4 nano vs Gemini Flash Lite intent classification benchmark"
- "Multi-agent memory coordination patterns"
- "Semantic search reranking for conversational AI agents"
- "OpenClaw flash router architecture"
