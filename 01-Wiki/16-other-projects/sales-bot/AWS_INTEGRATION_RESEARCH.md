# AWS Integration Research: Event-Driven RAG Product Search System
## Head Case Designs — 1.89M Products, 8,000+ Designs

**Date:** 2026-02-17  
**Context:** Product images on AWS S3/CloudFront. Search/AI layer TBD (AWS vs GCP vs Hybrid).  
**CEO Requirement:** S3 image add/delete → automatic search index update. No crawling.

---

## Table of Contents
1. [Architecture Comparison Table](#1-architecture-comparison-table)
2. [Approach 1: Pure AWS (RECOMMENDED)](#2-approach-1-pure-aws-recommended)
3. [Approach 2: Google Vertex AI](#3-approach-2-google-vertex-ai)
4. [Approach 3: Hybrid AWS+GCP](#4-approach-3-hybrid-awsgcp)
5. [Event-Driven Pipeline Architecture](#5-event-driven-pipeline-architecture)
6. [Multimodal Image Understanding (Critical)](#6-multimodal-image-understanding-critical)
7. [Cost Comparison at Scale](#7-cost-comparison-at-scale)
8. [Recommended Approach & Justification](#8-recommended-approach--justification)
9. [Implementation Roadmap](#9-implementation-roadmap)

---

## 1. Architecture Comparison Table

| Criteria | Pure AWS | Google Vertex AI | Hybrid (AWS+GCP) |
|---|---|---|---|
| **Event-driven S3 sync** | ✅ Native (S3 → EventBridge → Lambda) | ⚠️ Requires cross-cloud bridge | ⚠️ AWS events → GCP pipeline |
| **Multimodal image search** | ✅ Nova MME + Bedrock KB | ✅ Vertex Multimodal Embeddings | ✅ Either embedding model |
| **Visual search ("show me hearts")** | ✅ Native with Nova MME | ✅ Native with multimodalembedding@001 | ✅ Depends on embedding provider |
| **RAG / Knowledge Base** | ✅ Bedrock Knowledge Bases | ✅ Vertex AI Search for Commerce | ⚠️ Complex glue |
| **Commerce-optimized search** | ⚠️ General-purpose (OpenSearch) | ✅ Purpose-built for retail | ⚠️ Mixed |
| **BigQuery integration** | ⚠️ Requires data export/sync | ✅ Native (existing data there) | ✅ Direct access |
| **BigCommerce integration** | ⚠️ Custom Lambda connectors | ⚠️ Custom Cloud Functions | ⚠️ Custom either way |
| **Vector storage cost (1.89M)** | ✅ S3 Vectors: ~$8-15/mo | ⚠️ Higher (Vertex Vector Search) | ⚠️ Depends |
| **Latency (S3 change → searchable)** | ✅ <60 seconds | ⚠️ 2-5 minutes (cross-cloud) | ⚠️ 1-3 minutes |
| **Implementation complexity** | ⭐⭐ Medium | ⭐⭐⭐ Medium-High | ⭐⭐⭐⭐⭐ Very High |
| **Operational complexity** | ⭐⭐ Low (single cloud) | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ High (two clouds) |
| **Vendor lock-in risk** | ⚠️ AWS-specific services | ⚠️ GCP-specific services | ⚠️ Both |
| **Monthly cost estimate** | **$500-1,500** | **$2,000-5,000** | **$3,000-6,000** |

---

## 2. Approach 1: Pure AWS (RECOMMENDED)

### Core Architecture

```
S3 (Product Images)
    ↓ EventBridge
    ↓
Lambda (Orchestrator)
    ├─→ Bedrock: Nova MME (generate embedding)
    ├─→ S3 Vectors / OpenSearch Serverless (store/update vector)
    └─→ DynamoDB (product metadata cache)
    
User Search Query
    ↓
Bedrock Agent
    ├─→ Knowledge Base (multimodal RAG)
    │     ├─ Nova MME (query embedding)
    │     └─ S3 Vectors / OpenSearch (vector similarity search)
    ├─→ BigCommerce API (live pricing/availability)
    └─→ Response to user
```

### Key AWS Services

#### Amazon Bedrock Knowledge Bases (Multimodal)
- **GA since Nov 2025** — native multimodal retrieval
- Connects directly to S3 as data source
- Supports **Amazon Nova Multimodal Embeddings** (released Oct 2025)
  - First unified embedding model: text + images + video + audio → single vector space
  - Dimensions: 3072 (default), 1024, 384, 256
  - Supports 200+ languages
- **Incremental sync**: Only processes added/modified/deleted objects since last sync
- **Critical limitation**: Sync is NOT automatic. Must call `StartIngestionJob` API
  - Solution: S3 event → Lambda → calls `StartIngestionJob` (debounced/batched)
  
#### Amazon Nova Multimodal Embeddings (Nova MME)
- **Model ID**: `amazon.nova-2-multimodal-embeddings-v1:0`
- **Image pricing**: ~$0.00006 per input image (Titan MME pricing; Nova likely similar or lower)
- **Text pricing**: ~$0.0002 per 1K input tokens
- **Initial embedding of 1.89M images**: ~$113 one-time cost
- **Batch pricing**: 50% discount → ~$57 for full catalog
- **Key capability**: Text query "valentine cases with hearts" → finds heart-pattern images without keyword matching
- Best for: Product catalogs, visual search (explicitly called out in AWS docs)

#### Vector Storage Options

**Option A: Amazon S3 Vectors (RECOMMENDED for cost)**
- GA since Dec 2025 — purpose-built for vector storage at scale
- **90% cheaper** than conventional vector databases
- Storage: $0.06/GB/month
- For 1.89M vectors @ 1024 dimensions: ~1.89M × 4KB = 7.6GB → **~$0.46/mo storage**
- Query: per-API charge + $/TB based on index size
- Sub-second query latency (100ms typical)
- Native integration with Bedrock Knowledge Bases
- **Trade-off**: Lower QPS than OpenSearch. Best for moderate traffic.

**Option B: Amazon OpenSearch Serverless (Vector Collection)**
- For high-QPS real-time search
- Minimum: 0.5 OCU indexing + 0.5 OCU search = **~$174/mo** (non-redundant)
- Production (redundant): **~$350/mo** minimum
- Each OCU: 1 vCPU, 6GB RAM, 120GB storage
- Vector graphs stored in RAM (2GB usable per OCU for vectors)
- 1.89M vectors @ 1024 dims ≈ needs ~3-4 OCUs for vectors → **~$700-1,050/mo**
- Millisecond query latency, high QPS

**Recommendation**: Start with S3 Vectors (dramatically cheaper), upgrade to OpenSearch Serverless only if query latency/throughput becomes a bottleneck.

#### Amazon Bedrock Agents
- Orchestrates the full search + chat experience
- Can combine: Knowledge Base retrieval + BigCommerce API calls + conversation
- Supports tool use for live inventory/pricing checks
- Cost: Per-token for the orchestrating LLM (Nova Pro: $0.0008/$0.0032 per 1K tokens)

### How Bedrock KB S3 Sync Works (Important Detail)

**Bedrock Knowledge Bases do NOT auto-sync.** Per AWS re:Post (confirmed May 2024):

> "Each time you add, modify, or remove files from the S3 bucket for a data source, you must sync the data source so that it is re-indexed to the knowledge base. Syncing is incremental, so Amazon Bedrock only processes the objects in your S3 bucket that have been added, modified, or deleted since the last sync."

**Solution — Event-Driven Sync Pattern:**
```
S3 Object Created/Deleted
    → EventBridge rule (filter: s3:ObjectCreated:*, s3:ObjectRemoved:*)
    → SQS Queue (batch + deduplicate, 5-min window)
    → Lambda (calls StartIngestionJob API)
    → Bedrock KB incrementally re-indexes only changes
```

This gives us **<10 minute latency** from S3 change → searchable, with no crawling.

---

## 3. Approach 2: Google Vertex AI

### Architecture

```
S3 (Product Images)
    ↓ EventBridge
    ↓
Lambda → Cross-Cloud Bridge → GCP
    ├─→ Copy image to GCS (or use S3 direct URL)
    ├─→ Pub/Sub topic
    └─→ Cloud Function
          ├─→ Vertex AI Multimodal Embeddings (generate embedding)
          ├─→ Vertex AI Search catalog update (streaming API)
          └─→ BigQuery product record update
          
User Search Query
    ↓
Vertex AI Search for Commerce
    ├─→ Product catalog search (Google Shopping-grade)
    ├─→ Conversational Commerce Agent
    └─→ BigQuery for analytics
```

### Vertex AI Search for Commerce
- **Purpose-built for retail** — leverages Google Shopping's understanding
- Search pricing: **$2.50 per 1,000 queries**
- Conversational queries: **$6.00 per 1,000 queries**
- **No charge** for catalog import or user event management
- Supports BigQuery import (we already have product data in BigQuery!)
- Streaming API for incremental product updates
- Product catalog management with real-time availability

### Vertex AI Multimodal Embeddings
- Model: `multimodalembedding@001`
- **$0.0001 per image** (or $0.80 per 1M text tokens)
- Full catalog: 1.89M × $0.0001 = **$189 one-time**
- Dimensions: 128, 256, 512, 1408
- Rate limit: **120 requests/minute** base quota (needs increase for bulk)

### Advantages
- Google Shopping-grade product understanding
- Native BigQuery integration (existing data)
- Conversational Commerce Agent built-in
- Better for pure e-commerce search relevance

### Disadvantages  
- **Cross-cloud complexity**: S3 events must bridge to GCP
- **Image transfer**: Either copy 1.89M images to GCS (~costs) or reference S3/CloudFront URLs
- **Latency**: Cross-cloud event pipeline adds 1-3 minutes
- **Cost at scale**: $2.50/1K queries × estimated 500K queries/mo = **$1,250/mo just for search**
- Vertex Search for Commerce requires Google Merchant Center-like data format
- Rate limits on multimodal embeddings (120 req/min = 8 hours for full catalog)

---

## 4. Approach 3: Hybrid AWS+GCP

### Architecture

```
AWS Side:                              GCP Side:
┌─────────────────────┐               ┌─────────────────────┐
│ S3 (Source of Truth) │               │ Vertex AI Search    │
│ CloudFront (CDN)     │               │ BigQuery (analytics)│
│ EventBridge          │ ──Pub/Sub──→  │ Cloud Functions     │
│ Lambda (event proc)  │               │ Vertex Embeddings   │
│ Bedrock (AI chat)    │               │                     │
└─────────────────────┘               └─────────────────────┘
```

### Glue Options
1. **EventBridge → API Gateway → Cloud Function**: Direct HTTP call
2. **EventBridge → Lambda → Pub/Sub**: Lambda publishes to GCP Pub/Sub
3. **EventBridge Partner Integration**: Some connectors exist
4. **AWS Lambda → GCP REST API**: Direct API calls from Lambda to Vertex

### Why This Is the Worst Option
- **Double infrastructure costs**: Pay for services on both clouds
- **Double failure modes**: Outage on either cloud breaks the pipeline
- **Cross-cloud auth complexity**: IAM + GCP service accounts, credential management
- **Data consistency**: Images on AWS, embeddings on GCP, metadata split
- **Debugging nightmare**: Tracing an issue across two cloud providers
- **No team expertise benefit**: Must maintain AWS AND GCP skills
- **Estimated cost**: $3,000-6,000/mo (sum of both approaches + transfer costs)

---

## 5. Event-Driven Pipeline Architecture

### Recommended: AWS-Native Pipeline

```
                    ┌──────────────────────────────────────────────────────┐
                    │                HEAD CASE S3 BUCKET                    │
                    │  s3://headcase-product-images/                        │
                    │                                                       │
                    │  Structure:                                           │
                    │  /designs/{design_id}/                                │
                    │    {design_id}_{device_sku}.jpg                       │
                    │    {design_id}_{device_sku}.metadata.json             │
                    │                                                       │
                    └───────────┬──────────────────────┬───────────────────┘
                                │ s3:ObjectCreated:*   │ s3:ObjectRemoved:*
                                ▼                      ▼
                    ┌──────────────────────────────────────────────────────┐
                    │              AMAZON EVENTBRIDGE                       │
                    │  Rule: Match image events (.jpg, .png, .webp)        │
                    │  Filter: prefix = "designs/"                         │
                    └───────────────────────┬──────────────────────────────┘
                                            │
                                            ▼
                    ┌──────────────────────────────────────────────────────┐
                    │              AMAZON SQS (Batch Queue)                │
                    │  • Batches events (5-min window via visibility)      │
                    │  • Deduplicates by object key                        │
                    │  • Dead-letter queue for failures                    │
                    └───────────────────────┬──────────────────────────────┘
                                            │
                                            ▼
                    ┌──────────────────────────────────────────────────────┐
                    │           LAMBDA: Image Event Processor              │
                    │                                                       │
                    │  ON CREATE:                                           │
                    │  1. Parse S3 key → extract design_id + device_sku    │
                    │  2. Read .metadata.json (product name, tags, price)  │
                    │  3. Call BigCommerce API → get full product details   │
                    │  4. Store metadata in DynamoDB                        │
                    │  5. Generate embedding (see below)                   │
                    │  6. Upsert vector in S3 Vectors / OpenSearch         │
                    │                                                       │
                    │  ON DELETE:                                           │
                    │  1. Parse S3 key → extract design_id + device_sku    │
                    │  2. Delete vector from S3 Vectors / OpenSearch       │
                    │  3. Mark product as inactive in DynamoDB             │
                    │                                                       │
                    └──────────┬───────────────────────┬───────────────────┘
                               │                       │
                    ┌──────────▼─────────┐  ┌─────────▼────────────────┐
                    │ BEDROCK: Nova MME   │  │ S3 VECTORS / OPENSEARCH  │
                    │ Generate embedding  │  │ Store/update/delete      │
                    │ from image + text   │  │ vector embeddings        │
                    └────────────────────┘  └──────────────────────────┘


                    ═══════════════════════════════════════════════════
                    
                    SEARCH / CHAT FLOW:
                    
                    ┌──────────────────────────────────────────────────────┐
                    │           WEBSITE (goheadcase.com)                    │
                    │  Search bar / Chat widget / "Find similar" button    │
                    └───────────────────────┬──────────────────────────────┘
                                            │ User query / image upload
                                            ▼
                    ┌──────────────────────────────────────────────────────┐
                    │              API GATEWAY + LAMBDA                     │
                    │  OR                                                   │
                    │              BEDROCK AGENT (Managed)                  │
                    └───────────────────────┬──────────────────────────────┘
                                            │
                          ┌─────────────────┼────────────────────┐
                          ▼                 ▼                    ▼
                    ┌───────────┐  ┌──────────────┐  ┌──────────────────┐
                    │ BEDROCK   │  │ VECTOR SEARCH │  │ BIGCOMMERCE API  │
                    │ KB (RAG)  │  │ (similarity)  │  │ (live price/     │
                    │           │  │               │  │  availability)   │
                    └───────────┘  └──────────────┘  └──────────────────┘
                          │                 │                    │
                          └─────────────────┼────────────────────┘
                                            ▼
                    ┌──────────────────────────────────────────────────────┐
                    │              LLM (Nova Pro / Claude)                  │
                    │  Synthesizes search results + product data            │
                    │  Returns: product cards, recommendations, chat        │
                    └──────────────────────────────────────────────────────┘
```

### S3 Key → Product Mapping Strategy

The S3 bucket naming convention is critical for mapping image changes back to products:

```
Option A: Design ID in path (RECOMMENDED)
  s3://headcase-images/designs/DES-12345/DES-12345_iphone16pro.jpg
  s3://headcase-images/designs/DES-12345/DES-12345_iphone16pro.metadata.json
  
  metadata.json contains:
  {
    "designId": "DES-12345",
    "designName": "Romantic Hearts Pattern",
    "categories": ["valentines", "hearts", "love", "romantic"],
    "colors": ["red", "pink", "white"],
    "bigcommerceProductIds": [48291, 48292, 48293, ...],
    "tags": ["trending", "seasonal", "valentines-day"]
  }

Option B: S3 Object Tags
  Set tags on the image object itself:
  design_id=DES-12345, product_id=48291
  
Option C: DynamoDB Lookup Table
  Key: S3 object key → Value: product details
  Populated during initial catalog sync from BigCommerce
```

**Recommendation**: Option A (path-based) + metadata.json sidecar files. The metadata.json approach is already supported natively by Bedrock Knowledge Bases for enriching embeddings.

### Latency Expectations

| Stage | Latency |
|---|---|
| S3 event → EventBridge | <1 second |
| EventBridge → SQS | <1 second |
| SQS batch window | 1-5 minutes (configurable) |
| Lambda processing | 2-10 seconds per image |
| Embedding generation (Nova MME) | 1-3 seconds per image |
| Vector store upsert | <1 second |
| **Total: S3 upload → searchable** | **~2-7 minutes** |

For **alternative direct path** (skip SQS batching):
- S3 → EventBridge → Lambda (direct) → embed → store
- **Total: ~5-15 seconds per image** (but higher Lambda invocation cost)

---

## 6. Multimodal Image Understanding (Critical)

### The Valentine → Hearts Problem

This is the core value proposition. Traditional text search fails:
- User searches: "valentine cases" 
- Product names might be: "Romantic Heart Pattern Case"
- Text search: might miss if no "valentine" keyword
- **Multimodal visual search**: Model SEES the heart patterns in the image, understands visual semantics

### How It Works with Nova MME

```
INDEX TIME:
  Image of red heart pattern case
    → Nova MME → [0.23, -0.45, 0.89, ...] (1024-dim vector)
  
  Text: "Romantic Hearts Pattern, red pink, valentines"  
    → Nova MME → [0.21, -0.42, 0.91, ...] (similar vector!)

QUERY TIME:
  User: "show me cases with hearts for valentines"
    → Nova MME → [0.22, -0.43, 0.90, ...] (query vector)
    → Cosine similarity search
    → Returns heart-pattern cases even if "valentine" isn't in product name!
    
  User uploads photo of a heart-themed case they saw elsewhere:
    → Nova MME → [0.24, -0.44, 0.88, ...] (image query vector)
    → Returns visually similar heart cases from YOUR catalog!
```

### AWS: Amazon Nova Multimodal Embeddings
- **Released**: October 2025, GA November 2025
- **Modalities**: Text, images, documents, video, audio → unified vector space
- **Dimensions**: 3072 (default), 1024, 384, 256
- **Max input**: 8,172 tokens (text), 25MB (image)
- **Image formats**: JPEG, PNG
- **Cross-modal**: Text query retrieves images, image query retrieves images
- **Pricing**: ~$0.00006 per image (Titan MME rate; Nova likely same or better)
- **Batch**: 50% discount for bulk embedding

### GCP: Vertex AI Multimodal Embeddings
- **Model**: `multimodalembedding@001`
- **Modalities**: Text, images, video
- **Dimensions**: 128, 256, 512, 1408
- **Pricing**: $0.0001 per image ($0.80/1M text tokens)
- **Rate limit**: 120 requests/minute (base) — needs quota increase
- **Key limitation**: At 120 req/min, full catalog takes ~11 days without quota bump

### Head-to-Head for Our Use Case

| Factor | Nova MME (AWS) | Vertex Multimodal (GCP) |
|---|---|---|
| Images already on S3 | ✅ Direct access | ❌ Must transfer or fetch via URL |
| Cost per image embedding | ~$0.00006 | $0.0001 |
| Full catalog (1.89M) | ~$113 | ~$189 |
| Batch discount | ✅ 50% → $57 | ❌ Not available |
| Default rate limits | Higher (Bedrock scaling) | 120 req/min (needs increase) |
| Time for full catalog | ~4-6 hours (batch) | ~11 days (base), ~6 hrs (increased) |
| Bedrock KB integration | ✅ Native | ❌ Custom pipeline needed |
| Visual search quality | State-of-the-art (per benchmarks) | Strong, well-established |

**Winner**: Nova MME for this use case. Images already on S3, cheaper, faster bulk processing, native Bedrock KB integration.

### Visual Search Scenarios

| User Action | How It Works |
|---|---|
| Text: "cases with hearts" | Text → Nova MME → vector → find similar image vectors |
| Text: "star wars phone case" | Text → Nova MME → vector → finds SW themed designs |
| Upload photo | Image → Nova MME → vector → reverse image search |
| "Similar to this" (clicks product) | Product image → Nova MME → vector → "more like this" |
| "Red floral pattern for iPhone 16" | Text → vector + metadata filter (device=iPhone 16) |

---

## 7. Cost Comparison at Scale

### Assumptions
- 1.89M products, 8,000+ unique designs
- ~500K search queries/month (estimated)
- ~5,000 image changes/month (new designs, retired products)
- ~50K AI chat interactions/month

### Pure AWS Approach

| Component | Monthly Cost | Notes |
|---|---|---|
| **S3 Vectors storage** | $0.50-2 | 1.89M vectors @ 1024 dims |
| **S3 Vectors queries** | $5-20 | 500K queries/mo |
| **Nova MME embeddings (incremental)** | $0.30 | 5K images × $0.00006 |
| **Lambda (event processing)** | $5-10 | 5K invocations + 500K search |
| **SQS** | $0.50 | Message processing |
| **EventBridge** | $0.50 | Event routing |
| **DynamoDB (metadata)** | $10-25 | 1.89M items, on-demand |
| **Bedrock Agent (AI chat)** | $200-500 | 50K conversations, Nova Pro |
| **Bedrock KB retrieval** | $0 | No additional charge |
| **API Gateway** | $15-20 | 550K requests |
| **S3 storage (images)** | (existing) | Already paying |
| **CloudFront** | (existing) | Already paying |
| **TOTAL** | **$240-600/mo** | |

**One-time**: Full catalog embedding via batch = ~$57

### If Using OpenSearch Serverless Instead of S3 Vectors

| Component | Monthly Cost | Notes |
|---|---|---|
| **OpenSearch Serverless** | $700-1,400 | 3-4 OCUs for 1.89M vectors |
| **Everything else** | $235-585 | Same as above minus S3 Vectors |
| **TOTAL** | **$935-1,985/mo** | |

### Vertex AI Search for Commerce (GCP)

| Component | Monthly Cost | Notes |
|---|---|---|
| **Search queries** | $1,250 | 500K × $2.50/1K |
| **Conversational queries** | $300 | 50K × $6.00/1K |
| **Vertex Multimodal Embeddings** | $0.50 | 5K incremental images |
| **BigQuery** | $50-100 | Analytics, existing |
| **Cloud Functions** | $10-20 | Event processing |
| **Pub/Sub** | $5 | Event routing |
| **Cross-cloud data transfer** | $50-100 | S3 → GCS sync |
| **Lambda (AWS side)** | $5-10 | Event forwarding |
| **TOTAL** | **$1,670-1,785/mo** | |

**One-time**: Full catalog embedding = ~$189 + GCS transfer costs

### Hybrid Approach

| Component | Monthly Cost | Notes |
|---|---|---|
| **AWS infrastructure** | $240-600 | Event pipeline, S3, Lambda |
| **GCP infrastructure** | $1,500-1,800 | Vertex Search + AI |
| **Cross-cloud networking** | $100-200 | Data transfer, VPN/API calls |
| **TOTAL** | **$1,840-2,600/mo** | |

### Cost Summary

| Approach | Monthly | Annual | One-Time Setup |
|---|---|---|---|
| **Pure AWS (S3 Vectors)** | **$240-600** | **$2,880-7,200** | ~$57 |
| **Pure AWS (OpenSearch)** | $935-1,985 | $11,220-23,820 | ~$57 |
| **Vertex AI (GCP)** | $1,670-1,785 | $20,040-21,420 | ~$300 |
| **Hybrid** | $1,840-2,600 | $22,080-31,200 | ~$400 |

---

## 8. Recommended Approach & Justification

### 🏆 RECOMMENDED: Pure AWS with S3 Vectors + Nova MME + Bedrock KB

#### Justification

1. **Images already on S3** — Zero data movement. This is the single biggest advantage. No cross-cloud syncing, no duplicating 1.89M images to GCS, no transfer costs, no sync failures.

2. **Event pipeline is native** — S3 → EventBridge → Lambda is a solved, battle-tested pattern. No cross-cloud glue needed.

3. **Nova MME is purpose-built for this** — AWS literally launched multimodal product search as the headline use case for Nova MME + Bedrock KB (see their e-commerce demo in launch blog post).

4. **Cost: 3-8x cheaper** than Vertex AI Search for Commerce at our query volume. $240-600/mo vs $1,670+/mo.

5. **S3 Vectors is a game-changer** — At $0.50/mo for vector storage of 1.89M products (vs $700+/mo for OpenSearch Serverless), this makes the pure AWS approach dramatically cheaper than it would have been 6 months ago.

6. **Simpler operations** — Single cloud provider, single billing, single IAM model, single monitoring stack. Team only needs AWS expertise.

7. **Bedrock Knowledge Bases handles the hard parts** — Parsing, chunking, embedding, indexing, retrieval — all managed. We just connect S3 and configure.

8. **BigCommerce integration** — Lambda can call BigCommerce API for real-time pricing/inventory regardless of which cloud hosts the search layer.

#### What We Give Up (Vs Vertex AI)
- Google Shopping-grade product understanding (mitigated by Nova MME quality)
- Native BigQuery integration for analytics (can export or use Athena on S3)
- Vertex's built-in Conversational Commerce Agent (build with Bedrock Agents instead)
- Google's retail-specific ML models (not critical for phone cases)

#### Mitigation for BigQuery Dependency
Our existing BigQuery data (product/order analytics) stays on GCP. The search system on AWS doesn't replace BigQuery — it complements it:
- **BigQuery**: Historical analytics, order data, business intelligence
- **AWS**: Real-time product search, AI assistant, image-driven discovery
- **Sync point**: Nightly BigQuery → S3 export for any analytics-derived product attributes (popularity scores, trending tags) that should influence search ranking

---

## 9. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-3)
- [ ] Audit S3 bucket structure and naming conventions
- [ ] Design metadata.json schema for design-to-product mapping
- [ ] Create Bedrock Knowledge Base with S3 data source (multimodal)
- [ ] Select embedding model: Nova MME @ 1024 dimensions
- [ ] Create S3 Vectors bucket/index OR OpenSearch Serverless collection
- [ ] Run initial full catalog embedding (batch job, ~$57, ~4-6 hours)

### Phase 2: Event Pipeline (Weeks 3-5)
- [ ] Enable EventBridge notifications on S3 bucket
- [ ] Build Lambda: S3 event → parse key → generate embedding → upsert vector
- [ ] Set up SQS for batching/deduplication
- [ ] Build DLQ and error handling
- [ ] Test: upload image → verify searchable within 5 minutes

### Phase 3: Search API (Weeks 5-7)
- [ ] Build search API (API Gateway + Lambda or Bedrock Agent)
- [ ] Implement: text search, visual search (image upload), "more like this"
- [ ] Connect BigCommerce API for live product data
- [ ] Add metadata filters (device, color, category, price range)
- [ ] Build response formatting (product cards with CloudFront image URLs)

### Phase 4: AI Sales Assistant (Weeks 7-10)
- [ ] Configure Bedrock Agent with tools:
  - Knowledge Base retrieval (multimodal)
  - BigCommerce product lookup
  - Cart/checkout actions
- [ ] Build conversational UI (chat widget on goheadcase.com)
- [ ] Implement conversation memory (session-based)
- [ ] Add proactive suggestions ("You might also like...")

### Phase 5: Optimization (Weeks 10-12)
- [ ] A/B test search relevance
- [ ] Monitor S3 Vectors query latency; upgrade to OpenSearch if needed
- [ ] Add analytics: search terms, click-through rates, conversion
- [ ] Implement search ranking boost (bestsellers, new arrivals, seasonal)
- [ ] Connect BigQuery trending data for popularity signals

---

## Appendix A: Alternative Considered — Bedrock KB Auto-Sync via Direct S3

Instead of building a custom event pipeline, we could use Bedrock KB's native S3 connector with scheduled syncs:

```
Option: Scheduled Sync (simpler but slower)
  CloudWatch Events (every 15 min)
    → Lambda
    → calls StartIngestionJob()
    → Bedrock KB re-indexes changed files
```

**Pros**: Simpler, fewer moving parts  
**Cons**: 15-minute latency, unnecessary syncs when nothing changed, less control  
**Verdict**: Good for Phase 1 (MVP), upgrade to event-driven in Phase 2

## Appendix B: S3 Vectors vs OpenSearch Serverless Decision Matrix

| Factor | S3 Vectors | OpenSearch Serverless |
|---|---|---|
| Cost at 1.89M vectors | ~$2/mo | ~$700-1,400/mo |
| Query latency | ~100ms | ~10-50ms |
| Max QPS | Lower (TBD) | High (scales with OCUs) |
| Hybrid search (text + vector) | ❌ Vector only | ✅ Text + vector |
| Filtering | ✅ Metadata filters | ✅ Rich filtering |
| Managed by | S3 team | OpenSearch team |
| Maturity | New (GA Dec 2025) | Established |
| Bedrock KB integration | ✅ Native | ✅ Native |

**Recommendation**: Start S3 Vectors. Budget $350/mo OpenSearch Serverless upgrade fund if S3 Vectors proves insufficient for production QPS.

## Appendix C: Key AWS Service Configurations

```yaml
# Bedrock Knowledge Base
knowledge_base:
  name: headcase-product-search
  embedding_model: amazon.nova-2-multimodal-embeddings-v1:0
  embedding_dimensions: 1024
  data_source: 
    type: S3
    bucket: headcase-product-images
    inclusion_prefixes: ["designs/"]
  vector_store:
    type: S3_VECTORS  # or OPENSEARCH_SERVERLESS
    
# EventBridge Rule
event_rule:
  name: headcase-s3-image-events
  event_pattern:
    source: ["aws.s3"]
    detail-type: ["Object Created", "Object Deleted"]
    detail:
      bucket:
        name: ["headcase-product-images"]
      object:
        key:
          - prefix: "designs/"
          - suffix: [".jpg", ".png", ".webp"]

# Lambda Function
lambda:
  name: headcase-image-processor
  runtime: python3.12
  memory: 512
  timeout: 30
  environment:
    KNOWLEDGE_BASE_ID: "kb-xxxxxxxx"
    DATA_SOURCE_ID: "ds-xxxxxxxx"
    VECTOR_BUCKET: "headcase-vectors"
    BIGCOMMERCE_STORE_HASH: "otle45p56l"

# S3 Vectors Index
vector_index:
  name: headcase-products
  dimensions: 1024
  distance_metric: cosine
  metadata_schema:
    design_id: string
    device_sku: string
    product_name: string
    categories: string[]
    colors: string[]
    price_range: string
```

---

## References

- [Amazon Bedrock Knowledge Bases - Multimodal Retrieval (GA Nov 2025)](https://aws.amazon.com/blogs/machine-learning/introducing-multimodal-retrieval-for-amazon-bedrock-knowledge-bases/)
- [Amazon Nova Multimodal Embeddings (Oct 2025)](https://aws.amazon.com/blogs/aws/amazon-nova-multimodal-embeddings-now-available-in-amazon-bedrock/)
- [Amazon S3 Vectors (GA Dec 2025)](https://aws.amazon.com/s3/features/vectors/)
- [Bedrock KB S3 Data Source Connector](https://docs.aws.amazon.com/bedrock/latest/userguide/s3-data-source-connector.html)
- [Bedrock KB Sync (Incremental)](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-data-source-sync-ingest.html)
- [OpenSearch Serverless Half-OCU Pricing](https://aws.amazon.com/blogs/big-data/amazon-opensearch-serverless-cost-effective-search-capabilities-at-any-scale/)
- [Vertex AI Search for Commerce Pricing](https://cloud.google.com/retail/pricing)
- [Vertex AI Multimodal Embeddings](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings)
- [S3 Event Notifications with EventBridge](https://aws.amazon.com/blogs/aws/new-use-amazon-s3-event-notifications-with-amazon-eventbridge/)
