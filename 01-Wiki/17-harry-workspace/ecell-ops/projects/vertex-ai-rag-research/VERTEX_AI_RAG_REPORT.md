# Vertex AI RAG Research Report — Head Case Designs

**Prepared:** February 2026  
**Context:** E-commerce phone case company, 12,000+ licensed designs, existing Google Cloud account  
**Use Cases:** Customer chatbot (geo-aware), packing verification (vision), sales data analysis

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Vertex AI RAG Engine — What It Is & How It Works](#2-vertex-ai-rag-engine)
3. [Vertex AI Search — The Higher-Level Option](#3-vertex-ai-search)
4. [Vertex AI Agent Builder — Chatbot Platform](#4-vertex-ai-agent-builder)
5. [Gemini Integration — Text RAG & Vision](#5-gemini-integration)
6. [Grounding: Google Search vs Custom Data](#6-grounding-options)
7. [Alternatives Comparison](#7-alternatives-comparison)
8. [Recommended Architecture for Head Case Designs](#8-recommended-architecture)
9. [Cost Estimates](#9-cost-estimates)
10. [Final Recommendation](#10-final-recommendation)

---

## 1. Executive Summary

**Bottom line: Use a hybrid approach.** Vertex AI is powerful but expensive for a fully-managed RAG setup. For Head Case Designs' scale (~12,000 products, moderate traffic), the recommended approach is:

- **Chatbot:** Gemini 2.5 Flash + Grounding with your data (via Vertex AI Search or RAG Engine) — managed, low-maintenance
- **Packing Verification:** Direct Gemini Vision API calls (no RAG needed — just multimodal prompting)
- **Sales Analysis:** Gemini with structured data access (BigQuery or direct database queries)

**Estimated monthly cost: $150–$600/month** depending on traffic volume and architecture choices, vs **$25–$75/month** for a self-hosted Supabase pgvector approach (but with significantly more development/maintenance effort).

---

## 2. Vertex AI RAG Engine

### What It Is
Vertex AI RAG Engine is a **fully managed RAG service** (GA as of early 2025). It handles the entire RAG pipeline:

1. **Data ingestion** — Upload files from local storage, Cloud Storage, or Google Drive
2. **Data transformation** — Parsing (free default parser, or LLM/Document AI parsers) and chunking (fixed-size, free)
3. **Embedding generation** — Uses your chosen embedding model (e.g., `text-embedding-004`)
4. **Indexing & retrieval** — Vector search via Spanner backend or bring-your-own vector DB
5. **Generation** — Retrieved context is fed to Gemini for grounded responses

### How It Works
- You create a **RAG corpus** (an indexed knowledge base)
- Ingest your product catalog (JSON, CSV, PDF, etc.)
- The engine chunks, embeds, and indexes automatically
- At query time: embed the query → retrieve relevant chunks → feed to Gemini → get grounded response

### Pricing Components
| Component | Cost |
|-----------|------|
| Data ingestion | Free (data source transfer costs may apply) |
| Default parsing | Free |
| LLM parsing | LLM model costs (e.g., Gemini Flash token costs) |
| Chunking | Free |
| Embedding generation | ~$0.10/1M tokens (text-embedding-004) |
| **Vector storage (Spanner)** | **$0.90/hr per node (Basic tier = 100 PU ≈ $65/month)** |
| Retrieval | Included with Spanner costs |
| LLM reranking (optional) | LLM model costs |
| Ranking API reranking | $1.00/1,000 queries |

### Key Concern: Spanner Costs
The RAG-managed database uses **Cloud Spanner** as its backend:
- **Basic tier:** 100 processing units → ~**$65/month minimum** (always-on)
- **Scaled tier:** Starting at 1 node (1,000 PU) → ~**$650/month**, autoscales to 10 nodes

For 12,000 products, the Basic tier is more than sufficient. But this is a fixed floor cost even with zero queries.

### Supported Regions
GA in `europe-west3` (Frankfurt) and `europe-west4` (Netherlands). US regions (`us-central1`, `us-east4`) are on allowlist — you'd need to contact Google or use other regions.

### Documentation
- [RAG Engine Overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview)
- [RAG Engine Billing](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-engine-billing)
- [RAG Quickstart](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-quickstart)

---

## 3. Vertex AI Search

### What It Is
Vertex AI Search is a **higher-level managed search engine** (part of Agent Builder). It's designed for website search, product catalogs, and structured/unstructured data retrieval with built-in generative answers.

### Key Features for E-Commerce
- **Structured data search** — Index your product catalog with attributes (design name, license, device, price, etc.)
- **Semantic understanding** — Natural language queries like "Marvel phone case for iPhone 16"
- **Faceting & filtering** — Dynamic filters (by license, device, price range)
- **Generative answers** — AI-generated summaries from search results
- **Natural language query understanding** — Parses structured queries from natural language

### Pricing (General Model — Pay-per-query)
| SKU | Price |
|-----|-------|
| Search Standard Edition | $1.50/1,000 queries |
| Search Enterprise Edition (with AI answers) | $4.00/1,000 queries |
| Advanced Generative Answers add-on | +$4.00/1,000 queries |
| Index storage | $5.00/GB/month (first 10GB free) |
| Free trial | 10,000 queries/month free |

### For Head Case Designs
- 12,000 products at ~1KB each ≈ 12MB → well within free storage tier
- At 5,000 chatbot queries/month: ~$7.50/month (Standard) or ~$20/month (Enterprise with AI answers)
- At 50,000 queries/month: ~$75/month (Standard) or ~$200/month (Enterprise)

### Documentation
- [Vertex AI Search Pricing](https://cloud.google.com/generative-ai-app-builder/pricing)
- [Vertex AI Search Introduction](https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction)

---

## 4. Vertex AI Agent Builder

### What It Is
A full suite for building, scaling, and governing AI agents:

- **Agent Development Kit (ADK)** — Open-source Python/Java framework for multi-agent systems
- **Agent Engine** — Fully managed runtime for deploying agents
- **Agent Designer** — Low-code visual interface (preview)
- **Agent Garden** — Pre-built agent templates and tools

### Key Features for the Chatbot Use Case
- **Built-in tool integration:** Grounding with Google Search, Vertex AI Search, RAG Engine, Code Execution
- **Sessions & Memory Bank** — Conversational memory across turns
- **MCP (Model Context Protocol)** — Connect to databases, APIs, external tools
- **Multi-agent orchestration** — E.g., a routing agent that delegates to product search, order status, etc.
- **Identity & security** — IAM-based access control

### Agent Engine Pricing
| Component | Price |
|-----------|-------|
| Runtime (vCPU) | $0.0864/vCPU-hour |
| Memory | $0.0090/GB-hour |
| Code Execution | Same vCPU/memory rates |

### Worth It for Head Case?
**Yes, if you want a production-grade chatbot fast.** Agent Builder with ADK gives you:
- Managed infrastructure (no server management)
- Built-in conversation memory
- Easy integration with Vertex AI Search for product catalog
- Geo-location routing (can be implemented as agent logic)

**Alternative:** A simpler Cloud Run + Gemini API approach would be cheaper but requires more custom code.

### Documentation
- [Agent Builder Overview](https://docs.cloud.google.com/agent-builder/overview)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Agent Engine Quickstart](https://docs.cloud.google.com/agent-builder/agent-engine/quickstart)

---

## 5. Gemini Integration — Text RAG & Vision

### Text RAG with Gemini
Gemini models integrate directly with both RAG Engine and Vertex AI Search:

| Model | Input (text/image) | Output | Best For |
|-------|-------------------|--------|----------|
| Gemini 2.5 Flash | $0.30/1M tokens | $2.50/1M tokens | **Chatbot (best cost/quality)** |
| Gemini 2.5 Flash Lite | $0.10/1M tokens | $0.40/1M tokens | Simple queries, high volume |
| Gemini 2.0 Flash | $0.15/1M tokens | $0.60/1M tokens | Budget option |
| Gemini 2.5 Pro | $1.25/1M tokens | $10.00/1M tokens | Complex reasoning (overkill for chatbot) |

**Recommendation:** Use **Gemini 2.5 Flash** for the chatbot — excellent quality-to-cost ratio.

### Vision / Image Matching for Packing Verification

This is where Gemini shines. You have two approaches:

#### Approach A: Direct Gemini Vision (Recommended)
Send a photo of the product + a text prompt describing what it should be → Gemini confirms match/mismatch.

```
Prompt: "This should be product SKU HCD-12345: 'Marvel Spider-Man Red iPhone 16 Pro Case'. 
Does this photo match? Check: design, color, device model, packaging."
[Attach photo]
```

**Cost:** ~$0.0002 per image verification (Gemini 2.5 Flash: 1 image ≈ 1,290 tokens input + ~200 tokens output)

#### Approach B: Multimodal Embeddings + Vector Search
- Generate embeddings for all 12,000 product images using `multimodalembedding@001`
- Store in Vector Search
- At packing time: embed the photo → find nearest match → verify

**Cost:** Higher setup ($0.0001/image for embedding, plus Vector Search infrastructure), but enables "identify unknown product from photo" capability.

**Recommendation for packing verification:** **Approach A** (direct Gemini Vision) — simpler, cheaper, more accurate for "verify this is X" tasks. You already know what the product *should* be from the order.

### Multimodal Embeddings Pricing
| Model | Price |
|-------|-------|
| multimodalembedding@001 (image input) | $0.0001/image |
| multimodalembedding@001 (text input) | $0.80/1M tokens |
| text-embedding-004 | $0.10/1M tokens |

### Documentation
- [Gemini Vision / Image Understanding](https://ai.google.dev/gemini-api/docs/vision)
- [Multimodal Embeddings](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings)
- [Vision API Product Search](https://cloud.google.com/vision/product-search/docs) (legacy but relevant)

---

## 6. Grounding Options

### Grounding with Google Search
Uses live Google Search results to ground Gemini responses.

| Gemini Version | Free Tier | Paid Rate |
|----------------|-----------|-----------|
| Gemini 3 models | 5,000 queries/month | $14/1,000 queries |
| Gemini 2.5 Flash | 1,500/day (~45K/month) | $35/1,000 prompts |
| Gemini 2.5 Pro | 10,000/day | $35/1,000 prompts |

**Use case for Head Case:** Could supplement product search with live Google results (e.g., "trending phone cases 2026"), but probably not needed for the core chatbot.

### Grounding with Your Data
Uses Vertex AI Search or RAG Engine to ground responses in your own data.

| Feature | Price |
|---------|-------|
| Grounding with your data | **$2.50/1,000 requests** |

This is **on top of** the Gemini model costs and the underlying search/RAG costs.

### Recommendation
**Grounding with your data** is the right choice for the product recommendation chatbot. Google Search grounding is useful as an optional enhancement for trending products but adds significant per-query cost.

### Documentation
- [Grounding Overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview)

---

## 7. Alternatives Comparison

### Vertex AI RAG Engine vs Supabase pgvector vs Pinecone

| Factor | Vertex AI RAG Engine | Vertex AI Search | Supabase pgvector | Pinecone |
|--------|---------------------|------------------|-------------------|----------|
| **Setup effort** | Low (managed) | Very low (no-code console) | Medium (self-managed) | Low (SaaS) |
| **Maintenance** | None | None | You manage it | None |
| **Min monthly cost** | ~$65 (Spanner) | ~$0 (pay per query) | $25 (Pro plan) | $50/month min |
| **Cost at 10K queries** | ~$70 | ~$15–$40 | ~$25 + embedding costs | ~$50 + embedding costs |
| **Cost at 100K queries** | ~$90 | ~$150–$400 | ~$30 + embedding costs | ~$70 + embedding costs |
| **Max dataset size** | Virtually unlimited | Virtually unlimited | 8GB (Pro), 500GB+ available | Unlimited (serverless) |
| **Multimodal support** | Text only (for now) | Text + structured data | Text + images (manual) | Text only |
| **Built-in Gemini integration** | ✅ Native | ✅ Native | ❌ Manual | ❌ Manual |
| **Geo-location features** | Via agent logic | ✅ Faceting/filtering | Via SQL queries | Via metadata filtering |
| **Image search** | Via Vector Search add-on | Limited | Via pgvector | Via embeddings |
| **Production readiness** | High | Very high | Medium (DIY) | High |
| **Vendor lock-in** | High (Google) | High (Google) | Low (Postgres) | Medium (API) |

### Self-Hosted RAG on Supabase — Pros & Cons

**Pros:**
- **Cheapest option** — $25/month Supabase Pro includes Postgres with pgvector
- **Full control** — Custom ranking, filtering, hybrid search
- **No vendor lock-in** — Standard Postgres, can migrate anywhere
- **Unified database** — Products, orders, users, AND vectors in one DB
- **Already familiar** — You already use Supabase (per your current stack)

**Cons:**
- **You build everything** — Ingestion pipeline, chunking, embedding, retrieval, reranking
- **No managed Gemini integration** — Manual API calls for embeddings and generation
- **Scaling challenges** — pgvector performance degrades past ~1M vectors (not a concern at 12K)
- **No built-in generative answers** — Must implement prompt engineering yourself
- **Maintenance burden** — Index management, embedding updates, monitoring

### Verdict
For **12,000 products with moderate traffic**, Supabase pgvector is cost-effective but requires more engineering. **Vertex AI Search** hits the sweet spot for the chatbot — low setup, pay-per-query, native Gemini integration. For the vision use case, the Gemini API is the clear winner regardless of vector store choice.

---

## 8. Recommended Architecture for Head Case Designs

### Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                 CUSTOMER CHATBOT                 │
│                                                  │
│  User Query → Agent (ADK on Cloud Run)           │
│     ├─ Detect geo-location (IP/browser)          │
│     ├─ Query Vertex AI Search (product catalog)  │
│     │   └─ Faceted by region (US/UK bestsellers) │
│     ├─ Gemini 2.5 Flash generates response       │
│     │   └─ Grounded in search results            │
│     └─ Return product recommendations            │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│            PACKING VERIFICATION APP              │
│                                                  │
│  Photo Upload → Cloud Function / Cloud Run       │
│     ├─ Lookup order → get expected SKU/product   │
│     ├─ Send photo + product details to Gemini    │
│     │   └─ Gemini 2.5 Flash (vision)             │
│     ├─ Gemini returns: MATCH / MISMATCH + reason │
│     └─ Log result, alert if mismatch             │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│              SALES DATA ANALYSIS                 │
│                                                  │
│  Internal Dashboard → Agent or scheduled job     │
│     ├─ Query BigQuery / Supabase (sales data)    │
│     ├─ Gemini 2.5 Flash analyzes trends          │
│     │   └─ "What's trending?" "Compare US vs UK" │
│     └─ Generate insights report                  │
└─────────────────────────────────────────────────┘
```

### Data Setup

1. **Product Catalog → Vertex AI Search Data Store**
   - Export product catalog as structured JSON (JSONL)
   - Fields: SKU, name, design_name, license, device, price_us, price_uk, categories, image_url, sales_rank_us, sales_rank_uk
   - Index into Vertex AI Search via Agent Builder console
   - Enable semantic search + faceting on key attributes

2. **Sales Data → BigQuery (or existing Supabase)**
   - Daily/weekly sales aggregation
   - Gemini queries this via SQL or MCP Toolbox for Databases

3. **Product Images → Cloud Storage**
   - Already likely there; referenced by URL in catalog
   - Used directly by Gemini Vision for packing verification (no pre-processing needed)

### Geo-Location Implementation
- Detect user location via IP geolocation (MaxMind GeoIP, or Cloudflare headers)
- Pass as context to the agent: `"User is in UK. Show UK top sellers and GBP prices."`
- Vertex AI Search filters on `region=UK` facet to prioritize UK-relevant results

---

## 9. Cost Estimates

### Scenario: Moderate Traffic
- **Chatbot:** 20,000 queries/month
- **Packing verification:** 5,000 scans/month
- **Sales analysis:** 500 queries/month

### Option A: Vertex AI Search + Gemini (Recommended)

| Component | Monthly Cost |
|-----------|-------------|
| Vertex AI Search Standard (20K queries) | $30.00 |
| Grounding with your data (20K requests) | $50.00 |
| Gemini 2.5 Flash — chatbot (~2M input + 500K output tokens) | $1.85 |
| Gemini 2.5 Flash — packing verification (5K images) | $2.50 |
| Gemini 2.5 Flash — sales analysis (500 queries, ~1M tokens) | $1.00 |
| Cloud Storage (images, ~50GB) | $1.00 |
| Cloud Run (agent hosting) | $5–$20 |
| **TOTAL** | **~$90–$105/month** |

### Option B: Vertex AI RAG Engine + Gemini

| Component | Monthly Cost |
|-----------|-------------|
| Spanner (Basic tier, 100 PU) | $65.00 |
| Embedding generation (one-time, then incremental) | $0.50 |
| Gemini 2.5 Flash (all use cases) | $5.35 |
| Cloud Run | $5–$20 |
| **TOTAL** | **~$75–$90/month** |

Note: RAG Engine has a higher minimum but doesn't have per-query grounding costs.

### Option C: Supabase pgvector (Self-Hosted RAG)

| Component | Monthly Cost |
|-----------|-------------|
| Supabase Pro plan | $25.00 |
| Gemini API calls (via Vertex AI or AI Studio) | $5.35 |
| Embedding generation (text-embedding-004) | $0.50 |
| Cloud Run or Supabase Edge Functions | $0–$10 |
| **TOTAL** | **~$30–$40/month** |

**But:** Add 40–100+ hours of engineering time to build the RAG pipeline, embeddings management, retrieval logic, prompt engineering, and maintenance.

### Option D: Full Agent Builder (Enterprise)

| Component | Monthly Cost |
|-----------|-------------|
| Agent Engine runtime | $20–$50 |
| Vertex AI Search Enterprise (20K queries) | $80.00 |
| Grounding + Gemini costs | $55.00 |
| **TOTAL** | **~$155–$185/month** |

Most polished but most expensive.

---

## 10. Final Recommendation

### 🏆 Recommended: Option A — Vertex AI Search + Gemini 2.5 Flash

**Why:**
1. **Best ROI for your scale** — Pay-per-query means no wasted spend; ~$100/month for a fully grounded chatbot
2. **Fastest to production** — Vertex AI Search has a no-code console; index your catalog in hours
3. **Native Gemini integration** — Seamless grounding, no custom RAG pipeline to build
4. **Faceting for geo-location** — Built-in structured filtering for US vs UK results
5. **Scales smoothly** — From 1,000 to 1,000,000 queries without infrastructure changes
6. **Already on Google Cloud** — No new vendor relationships needed

**For packing verification:** Use Gemini 2.5 Flash Vision directly — simple, cheap, no special infrastructure. Send the photo + expected product details → get a match/mismatch response.

**For sales analysis:** Use Gemini with structured data access (BigQuery or direct SQL via MCP Toolbox). No RAG needed — this is more of an analytics agent.

### When to Consider Alternatives

| Scenario | Go With |
|----------|---------|
| Budget is extremely tight (<$50/month) | Supabase pgvector + Gemini API |
| Need multimodal product search (search by photo) | Add Vertex AI Vector Search with multimodal embeddings |
| Chatbot needs complex multi-turn workflows | Vertex AI Agent Builder (full) |
| Want full control & no vendor lock-in | Supabase pgvector + open-source embeddings |
| Traffic exceeds 500K queries/month | Vertex AI Search Configurable pricing |

### Migration Path
Start with **Vertex AI Search Standard** for the chatbot. If needs grow:
1. Add Agent Builder for multi-turn conversations + memory
2. Add Vertex AI Vector Search for image-based product discovery
3. Migrate to Configurable pricing if volume exceeds 15M queries/month

### Key Links
| Resource | URL |
|----------|-----|
| Vertex AI RAG Engine Overview | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview |
| Vertex AI RAG Billing | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-engine-billing |
| Vertex AI Search Pricing | https://cloud.google.com/generative-ai-app-builder/pricing |
| Vertex AI Generative AI Pricing | https://cloud.google.com/vertex-ai/generative-ai/pricing |
| Agent Builder Overview | https://docs.cloud.google.com/agent-builder/overview |
| Multimodal Embeddings | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings |
| Grounding Overview | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview |
| Multimodal Search Architecture | https://cloud.google.com/blog/products/ai-machine-learning/combine-text-image-power-with-vertex-ai |
| Spanner Pricing | https://cloud.google.com/spanner/pricing |

---

*Report compiled from Google Cloud documentation, pricing pages, and community resources as of February 2026. Prices are subject to change — always verify against the official pricing pages before committing.*
