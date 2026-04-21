# Fulfillment Portal — LLM Council Synthesis Report

> **Company:** Ecell Global — Licensed Tech Accessories  
> **Scale:** 200K+ SKUs | 500+ orders/day | $5M+ annual revenue  
> **Marketplaces:** Amazon, eBay, Walmart, Shopify, OnBuy  
> **Offices:** Philippines (PH), United Kingdom (UK), Florida (FL)  
> **Date:** March 28, 2026  
> **Council:** GPT-5.4 (Architecture) | Claude Sonnet 4.6 (Data/Security) | Gemini 3.1 Pro (Tech Stack)

---

## Executive Summary

Three LLM council members independently analyzed eight architectural questions for the Ecell Global Fulfillment Portal. This report synthesizes their findings into actionable decisions, risk assessments, and a phased implementation roadmap.

**All three models unanimously endorse** the proposed FastAPI + Next.js + Supabase stack, with important caveats on execution pattern, credential management, and the IREN replacement strategy.

---

## Council Decision Matrix

| Question | Council Verdict | Confidence | Key Caveat |
|----------|----------------|:----------:|------------|
| **Q1:** Portal Architecture | **YES** — FastAPI + Next.js + Supabase modular monolith | 3/3 | Must add Redis + durable job queue from day one. Not a simple CRUD app. |
| **Q2:** Amazon Buy Shipping | **DIRECT SP-API** — Not through aggregator | 3/3 | ShipStation OK as interim bridge. EasyPost/Shippo do NOT preserve seller protection. |
| **Q3:** Tracking Writeback | **DEDICATED TABLE** + SQS/Lambda relay | 3/3 | Never write to Zero's existing tables. Zero reads tracking via portal API. |
| **Q4:** IREN Replacement | **CLOUD PRINT SERVICE** — Pillow/libvips + PrinceXML | 3/3 | Puppeteer/Cairo insufficient for CMYK print. Need ICC profile support. |
| **Q5:** Credential Management | **GCP SECRET MANAGER** + per-office IAM | 3/3 | HashiCorp Vault is overkill for 3 offices / 12 secrets. Revisit at 10+ offices. |
| **Q6:** BQ→Supabase Sync | **15-MIN INCREMENTAL** watermark polling | 3/3 | Costs same as nightly with partition pruning. Event-driven when >5K orders/day. |
| **Q7:** Backend Runtime | **HYBRID** — FastAPI heavy + Next.js API routes light | 3/3 | Python mandatory for AI vision (Phase 3) and image processing. Node.js for CRUD. |
| **Q8:** Wave Scheduling | **BUILD CUSTOM** — ShipStation insufficient | 3/3 | Commercial tools provide batch mechanics only, not timezone-aware office routing. |

*3/3 = all three council members agree. Unanimous consensus across all questions.*

---

## Target Architecture

### Council-Endorsed Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | Next.js (Cloud Run or Vercel) | Server-rendered ops portal with RBAC. API routes handle light CRUD. |
| Core Backend | FastAPI modular monolith | Domain modules: orders, inventory, wave scheduler, carriers, print. Async jobs via Cloud Tasks. |
| Operational DB | Supabase (Managed Postgres) | ACID transactions, RLS for multi-office isolation, real-time subscriptions. Pro tier ($25/mo). |
| Job Queue | GCP Cloud Tasks + Pub/Sub | HTTP task dispatch to Cloud Run workers. Built-in retry, rate limiting, DLQ. No Celery overhead. |
| Cache | Redis (Memorystore) | SKU lookups, template cache, session state, rate-limit counters. |
| Analytics | BigQuery (existing) | Continues as analytics warehouse. CDC via Datastream. 15-min incremental sync to Supabase. |
| Secrets | Google Secret Manager | Per-office IAM bindings. Cloud Audit Logs. Auto-rotation via Cloud Functions. |
| Print Service | Pillow/libvips + PrinceXML | ICC-aware raster pipeline + PDF/X renderer. Separate Cloud Run service. |
| Carrier Layer | Dual-path: SP-API + direct APIs | Amazon Buy Shipping direct. Stamps.com, Royal Mail, Evri via direct APIs. Circuit breaker pattern. |
| Compute | GCP Cloud Run (all services) | Scale-to-zero. Estimated <$50/mo at current volume. No Kubernetes overhead. |

### Data Flow Architecture

```
Marketplaces (Amazon / eBay / Walmart / Shopify / OnBuy)
        │
        ▼
  PH MySQL (Zero PHP) ──► Aurora RDS ──► Datastream CDC (~2 min) ──► BigQuery
                               │                                        │
                        NEW: order_tracking                     15-min watermark
                        (portal writes only)                   sync (incremental)
                               │                                        │
                               ▼                                        ▼
                        Supabase Postgres  ◄────────────────────────────┘
                        (Operational DB)
                               │
                    ┌──────────┼──────────┬──────────┐
                    │          │          │          │
                 Orders     Carrier    Print      Wave
                 Queue      Service   Service   Scheduler
                    │          │          │          │
                    ▼          ▼          ▼          ▼
                 Next.js Operations Portal (RBAC per office)
                               │
                    Google Secret Manager (per-office IAM)

  Zero continues as-is (read-only from portal perspective)
```

---

## Q1: Portal Architecture — Modular Monolith

### Council Consensus

All three council members endorse FastAPI + Next.js + Supabase as the right stack, but emphasize this must be built as a **modular monolith with domain boundaries**, not a simple CRUD application. The real complexity is in integrations, state transitions, retries, and warehouse/print workflows. ([FastAPI docs](https://fastapi.tiangolo.com/deployment/concepts/), [AWS monolith vs microservices](https://aws.amazon.com/compare/the-difference-between-monolithic-and-microservices-architecture/))

### Rejected Alternatives

| Alternative | Why Rejected |
|-------------|-------------|
| Serverless-first (Lambda) | Fulfillment needs long-lived transactional control, predictable queues, and locking. Fragments business logic too early. |
| Full microservices day-1 | Higher deploy/debug/observability overhead. Too much upfront tax for 500 orders/day. Extract services later as needed. |
| Node.js monolith | No fundamental advantage. CPU-heavy print/image work and AI vision are less natural in Node.js. |
| Extend Zero (PHP) | Zero is a 10yr PHP monolith behind a firewall with no API surface. Modification risks breaking production. |

### Domain Modules

| Module | Responsibilities | Notes |
|--------|-----------------|-------|
| Order Ingestion | Marketplace intake, normalization, idempotency, status updates | Evented ingestion with dead-letter handling ([AWS event-driven](https://aws.amazon.com/what-is/eda/)) |
| Inventory & Allocation | Available-to-promise, reservations, warehouse selection, split logic | Strongly transactional in Postgres |
| Wave Scheduler | Office ownership, timezone cutoffs, release windows, batch queueing | Custom build required — commercial tools insufficient |
| Print Composition | Template placement, ICC transforms, PDF/X output, asset versioning | Separate Cloud Run service |
| Carrier Service | Rate shopping, Buy Shipping, label purchase, manifest, tracking | Circuit breaker per carrier |
| Reconciliation | Shipment confirmations, retries, inventory mismatch, audit logs | Publishes events to BQ + alerts |
| Admin Portal | Exception queues, search, dashboards, reruns, overrides | Next.js with RBAC |

### Multi-Office Design (PH / UK / FL)

Model the three offices as **operational control zones**, not just physical warehouses. The stated problem is time-based wave ownership as much as stock location. ([ShipStation Mobile Picking](https://help.shipstation.com/hc/en-us/articles/38623190668443-Mobile-Picking))

Use a **canonical UTC event timeline** in the database, but store each office's local operating calendar, shift schedule, holiday calendar, and release windows so wave logic is deterministic and auditable.

**Routing sequence:**
1. Marketplace order arrives → order normalized
2. Candidate ship-from/production sites resolved
3. Wave owner assigned based on office calendar and SLA
4. Batch released to pick/print queue at that office's local release time
5. Exceptions routed to global exception queue if missed or blocked

### Concrete Recommendation

1. Use FastAPI + Next.js + Supabase, but deploy as containers on managed compute with **Redis + durable job queue from day one**
2. Keep BigQuery as analytics/reconciliation and continue CDC into it
3. Put all marketplace and carrier interactions behind adapter modules and publish internal domain events
4. Make wave scheduling a first-class domain service with office calendars and local cutoffs
5. Split out print composition as its own execution service early

---

## Q2: Amazon Buy Shipping — Direct SP-API Integration

### Council Verdict

Unanimous: use Amazon Buy Shipping **directly via SP-API Shipping API v2** for all Amazon FBM orders. This is the only path that guarantees OTDR seller protection. ([Amazon Merchant Fulfillment API](https://developer-docs.amazon.com/sp-api/docs/merchant-fulfillment-api), [Amazon Shipping API v1 Reference](https://developer-docs.amazon.com/sp-api/docs/shipping-api-v1-reference))

### Carrier Approach Comparison

| Approach | Seller Protection | Limitations | Verdict |
|----------|------------------|-------------|---------|
| Direct SP-API | Full OTDR protection | Higher implementation effort; restricted API roles required | **BEST** — use for production |
| ShipStation proxy | Documented OTDR (US/UK only) ([ShipStation docs](https://help.shipstation.com/hc/en-us/articles/360025855992-Amazon-Buy-Shipping-API-United-States)) | Single account, no multi-package, split order issues, throttling | OK as interim bridge |
| EasyPost / Shippo | No documented protection | Not designed for Amazon Buy Shipping semantics | **DO NOT** use for Amazon |

### Recommended: Dual-Path Carrier Architecture

- **Path 1 — Amazon FBM:** Direct SP-API Shipping API v2 integration. Maintains seller protection, provides rate comparison within Amazon's carrier network.
- **Path 2 — Non-Amazon:** Direct carrier APIs (Stamps.com, Royal Mail, Evri) or EasyPost aggregator for USPS/UPS/DHL/FedEx.
- **Circuit Breaker:** Each carrier wrapped in a circuit breaker (`pybreaker`). If carrier API fails 3x in 60 seconds, circuit opens. Auto-retry via Cloud Tasks with exponential backoff.

### Key Finding: ShipStation Limitations

ShipStation can proxy Amazon Buy Shipping but with meaningful constraints: only US/UK accounts, single Amazon account limit, no multi-package shipments, split-order issues, and throttling. It should not define the portal's long-term domain model. ([ShipStation Amazon Marketplace](https://help.shipstation.com/hc/en-us/articles/360026140891-Amazon-Marketplace))

---

## Q3: Tracking Writeback — Dedicated Table Strategy

### The Problem

```
Current Flow (READ-ONLY from portal perspective):
┌─────────────────┐    replication    ┌──────────────┐    Datastream    ┌──────────────┐
│  PH MySQL       │ ────────────────► │ Aurora RDS   │ ──────────────► │  BigQuery    │
│  192.168.20.160 │    binlog         │  us-east-1   │    CDC ~2min    │              │
│  "Zero" PHP app │                   │              │                  │              │
└─────────────────┘                   └──────────────┘                  └──────────────┘

New Requirement: Portal must inject tracking numbers back into the chain
without disrupting Zero's order processing.
```

### Approach Comparison

| Approach | Schema Risk | Lock Risk | Replication Safety | Verdict |
|----------|:-----------:|:---------:|:------------------:|---------|
| Direct writes to Zero's tables | HIGH | HIGH | MEDIUM | **AVOID** |
| Dedicated `order_tracking` table | LOW | NONE | HIGH | **PRIMARY** |
| SQS/Lambda relay (add-on) | LOW | NONE | HIGH | **ADD** for resilience |
| CDC reverse sync (bidirectional) | MEDIUM | NONE | LOW | **AVOID** (anti-pattern) |

### Recommended: Dedicated Table + SQS Relay

**Why this works:**
- Zero's existing tables are **never touched**
- Zero can JOIN to `order_tracking` by SRN when needed (read-only join, no write risk)
- Datastream CDC already watches Aurora — new tables added via configuration, no pipeline changes
- Schema is owned by the portal team; no coordination required with Zero's PHP code

**DDL for Aurora:**
```sql
CREATE TABLE order_tracking (
  id           BIGINT UNSIGNED AUTO_INCREMENT,
  srn          VARCHAR(50) NOT NULL,
  carrier      VARCHAR(50) NOT NULL,
  tracking_no  VARCHAR(100),
  label_url    TEXT,
  office       ENUM('PH','UK','FL') NOT NULL,
  shipped_at   DATETIME,
  created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY  (id),
  UNIQUE KEY   uq_srn_office (srn, office),
  INDEX        idx_srn (srn),
  INDEX        idx_updated (updated_at)
) ENGINE=InnoDB CHARACTER SET utf8mb4;
```

### Critical Implementation Notes

- **Dedicated DB user:** `portal_tracking_writer` with INSERT/UPDATE on `order_tracking` only. No access to Zero's tables.
- **Aurora writes do NOT propagate back to PH MySQL.** Zero must read tracking data via a portal REST API — not via the database.
- **Datastream CDC** picks up the new table automatically. Flows to BigQuery within ~2 minutes.
- **SQS dead-letter queue** ensures no tracking numbers are lost during transient Aurora connectivity issues.

### End-to-End Latency

```
Portal writes tracking_no (t=0)
     ├──► Aurora order_tracking: committed ≤ 100ms
     ├──► Datastream CDC: ~2 min
     ├──► BigQuery order_tracking: ~2-3 min
     └──► Supabase (next 15-min sync): 2–17 min

Acceptable: tracking numbers are communicated to customers asynchronously.
```

---

## Q4: IREN Replacement — Cloud Print Composition

### The Problem

IREN is a **single-point-of-failure** Java app on ONE PC in the Philippines. If that PC dies, print file generation stops. No documentation, no API, no source code access.

### Technology Assessment

| Technology | CMYK Support | ICC Profiles | PDF/X Output | Verdict |
|-----------|:------------:|:------------:|:------------:|---------|
| Pillow / ImageCms | YES (via LittleCMS) | YES | NO (raster only) | **USE** for preprocessing ([Pillow docs](https://pillow.readthedocs.io/en/stable/reference/ImageCms.html)) |
| libvips | YES (via LittleCMS) | YES (N-color) | NO (raster only) | **USE** for fast raster ops ([libvips](https://www.libvips.org/2022/12/22/What's-new-in-8.14.html)) |
| PrinceXML | YES (native) | YES (output intent) | YES (PDF/X-1,3,4) | **USE** for final PDF ([Prince docs](https://www.princexml.com/doc/13/graphics/)) |
| Puppeteer/Chrome | NO (modifies colors) | NO | NO | Previews only ([Puppeteer docs](https://pptr.dev/api/puppeteer.page.pdf)) |
| Cairo/WeasyPrint | NO (TODO in roadmap) | NO | NO | **AVOID** for print ([Cairo TODO](https://www.cairographics.org/todo/)) |

### Recommended Print Pipeline

```
Stage 1: Template Resolver
  SKU → device family → template version → print surface geometry

Stage 2: Asset Normalizer
  Validate artwork DPI, transparency, ICC profile; convert via Pillow/libvips

Stage 3: Composition Engine
  Place artwork into safe area, bleed, trim, camera holes, wrap rules

Stage 4: PDF/X Renderer
  Emit final print-ready PDF with fixed printer profile (PrinceXML)

Stage 5: Validation Layer
  Check profile, page size, trim/bleed box, DPI thresholds

Stage 6: Preview Renderer
  Generate RGB JPEG previews for portal UI (separate from print output)
```

### Output Separation

| Output Type | Purpose | Engine |
|------------|---------|--------|
| Customer/ops preview | Fast UI preview, proofs, internal review | Puppeteer or RGB image pipeline |
| Production print file | Print-ready PDF/X with CMYK/output intent | PrinceXML or dedicated PDF/X renderer |
| Intermediate artwork | Masking, scaling, ICC conversion, flattening | Pillow/ImageCms or libvips |

### Pre-requisite

Obtain sample input/output pairs from Chad — **10 real POs with their IREN print file outputs** — for golden-master testing against the new cloud service.

---

## Q5: Credential Management — GCP Secret Manager

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: Google Secret Manager (Source of Truth)               │
│  • All carrier API credentials stored here                      │
│  • Per-office IAM bindings (PH SA cannot read UK secrets)      │
│  • Cloud Audit Logs: every secret access logged                │
│  • Automatic versioning + rotation via Cloud Functions          │
└───────────────────────────┬─────────────────────────────────────┘
                            │  Secret accessed at request time
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 2: Portal API (Supabase Edge Functions / Cloud Run)      │
│  • JWT claim: user.office = 'PH' | 'UK' | 'FL'                │
│  • RBAC check: user may only request credentials for own office │
│  • Credentials used in-memory, never logged                    │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 3: Carrier APIs                                          │
│  Amazon Buy Shipping / Stamps.com / Royal Mail / Evri           │
└─────────────────────────────────────────────────────────────────┘
```

### Options Comparison

| Option | Cost | Multi-Tenant | Rotation | Verdict |
|--------|------|:------------:|----------|---------|
| Google Secret Manager ([docs](https://cloud.google.com/secret-manager/docs/overview)) | <$5/mo for 12 secrets | Per-office IAM bindings | Cloud Functions auto-rotation | **PRIMARY** |
| HashiCorp Vault (HCP) ([docs](https://developer.hashicorp.com/vault/tutorials/manage-hcp-vault-dedicated/vault-manage-namespaces)) | ~$22/mo minimum | Full namespace isolation | Dynamic secret generation | Future (10+ offices) |
| Supabase Vault ([docs](https://supabase.com/docs/guides/database/vault)) | $0 (included) | No native RLS for secrets | Manual | Runtime secrets only |

### Secret Naming Convention

```
ecell-carrier-creds-{office}-{carrier}-{credential-type}

Examples:
  ecell-carrier-creds-ph-amazon-buy-shipping
  ecell-carrier-creds-uk-royal-mail-api-key
  ecell-carrier-creds-fl-stamps-api-key
```

### IAM Policy per Office

```yaml
# Philippines office service account — can ONLY read PH secrets
resource: projects/ecell-global/secrets/ecell-carrier-creds-ph-*
members:
  - serviceAccount:portal-worker-ph@ecell-global.iam.gserviceaccount.com
roles:
  - roles/secretmanager.secretAccessor   # read-only
```

### RBAC Model

| Role | Read Own Office | Write Tracking | Read Other Office | Rotate Credentials | View Audit Logs |
|------|:-:|:-:|:-:|:-:|:-:|
| Worker (PH/UK/FL) | YES | YES (own SRNs) | NO | NO | NO |
| Manager (PH/UK/FL) | YES | YES | NO | NO | Own office only |
| System Admin | YES (all) | YES (all) | YES | YES | YES (all) |

### Key Rotation Cadence

| Credential Type | Rotation Frequency | Method |
|----------------|:------------------:|--------|
| Amazon Buy Shipping API key | 90 days | Manual via portal + Secret Manager update |
| Stamps.com API user/pass | 60 days | Semi-automated Cloud Function |
| Royal Mail API cert | At expiry (1-2 years) | Manual + calendar reminder |
| ShipStation API key | 90 days | Manual |
| Aurora portal_tracking_writer password | 90 days | AWS Secrets Manager automatic rotation |

---

## Q6: BQ → Supabase Sync — 15-Minute Incremental

### Current vs. Proposed

| Metric | Current (Nightly) | Proposed (15-min) | Improvement |
|--------|:-:|:-:|:-:|
| Data staleness | Up to 24 hours | Up to 17 minutes | **85x faster** |
| End-to-end latency | 2 min + 24 hr | 2 min + 15 min | 2-17 min total |
| BQ monthly cost | ~$0.09 | ~$0.09-0.36 | Same (free tier) |
| Failure impact | 1 large batch to retry | Small incremental batch | Self-healing |
| Supabase connections | 1 connection, 1x/day | 1 connection, 96x/day | Negligible impact |

### Strategy: Incremental Watermark Pattern

The correct approach is **incremental sync with a high-watermark timestamp** — not a full table scan every 15 minutes.

**Key principles:**
- Use parameterized query with `updated_at >= @watermark` and static `DATE BETWEEN` bounds for [BQ partition pruning](https://cloud.google.com/blog/products/data-analytics/optimizing-your-bigquery-incremental-data-ingestion-pipelines)
- 20-minute lookback window (slightly wider than 15-min interval) ensures no orders missed at sync boundaries
- Upserts are idempotent by `order_id` — safe to re-process the same row
- If a sync run fails, watermark was not updated, so next run re-processes from same point

**Watermark table (Supabase):**
```sql
CREATE TABLE sync_watermarks (
  table_name    TEXT PRIMARY KEY,
  last_synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  rows_synced   INTEGER DEFAULT 0,
  sync_duration_ms INTEGER,
  error_message  TEXT,
  updated_at    TIMESTAMPTZ DEFAULT NOW()
);
```

### Cost Analysis ([BigQuery pricing](https://cloud.google.com/bigquery/pricing))

| Sync Strategy | Data Scanned per Query | Queries/Month | Monthly BQ Cost |
|--------------|:----------------------:|:-------------:|:---------------:|
| Nightly full sync (current) | ~500 MB | 30 | ~$0.09 |
| 15-min full sync (naive) | ~500 MB each | 2,880 | ~$9.00 |
| **15-min incremental + partition filter** | **~5-20 MB** | **2,880** | **~$0.09-0.36** |

With partition pruning, the 15-min sync costs virtually the same as nightly — well within the 1 TiB/month free tier.

### Supabase Connection Budget

```
Sync job:          1 connection × 2–5 sec every 15 min  →  negligible
Portal workers:    ~50-200 concurrent (via Supavisor)   →  200 pooler slots on Small
Tracking writeback: 1 connection per write (fast)       →  negligible
Admin queries:     5-10 occasional connections          →  negligible

Total peak: ~210 pooler connections → requires Small tier minimum ($25/mo)
```

### Upgrade Path

When volume exceeds 5,000 orders/day, switch to **event-driven** (Datastream → Pub/Sub → Cloud Run → Supabase) for sub-2-minute latency.

---

## Q7: Backend Runtime — Hybrid Python/Node.js

### The Verdict

All council members recommend a **hybrid approach**: Next.js API routes for lightweight CRUD, FastAPI for computationally heavy operations. ([Squareboat comparison](https://www.squareboat.com/blog/nextjs-vs-nodejs-which-one-should-you-choose-in-2026), [Slincom comparison](https://www.slincom.com/blog/programming/fastapi-vs-express-backend-comparison-2025))

| Layer | Runtime | Handles |
|-------|---------|---------|
| Next.js API Routes | Node.js / TypeScript | Authentication, simple CRUD, dashboard data fetching, real-time subscriptions |
| FastAPI Workers | Python | Label generation, carrier API calls, print file composition, order routing, AI vision QC, BQ sync |

**Why Python is mandatory:** Phase 3 requires Gemini Vision API for QC and image processing (Pillow, libvips, ICC profiles). These libraries and the AI ecosystem are fundamentally Python-native.

### Deployment Architecture

- **FastAPI:** Cloud Run with min 1 instance (always warm for carrier calls). Estimated <$50/mo at 500 orders/day. ([Cloud Run vs GKE](https://hivelogue.com/labs/cloudfunctions-vs-cloudrun-vs-gke))
- **Next.js:** Cloud Run or Vercel. Scale-to-zero is fine for the portal UI.
- **Supabase:** Managed Pro tier ($25/mo). 90 direct + 400 pooler connections via [Supavisor](https://supabase.com/blog/supavisor-1-million).

### Job Queue: GCP Cloud Tasks (Not Celery)

Cloud Tasks is the right choice for FastAPI on Cloud Run. Celery requires managing a separate worker infrastructure and message broker — unnecessary overhead for this workload. ([Cloud Tasks vs Pub/Sub](https://oneuptime.com/blog/post/2026-02-17-how-to-choose-between-pub-sub-and-cloud-tasks-for-asynchronous-processing-on-gcp/view))

- Cloud Tasks creates HTTP POST to dedicated FastAPI worker endpoints on Cloud Run
- Native retry with configurable rate limiting (crucial for fragile carrier APIs)
- Built-in dead-letter queues — no infrastructure management

### Circuit Breaker Pattern for Carrier APIs

```python
import pybreaker
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Fail after 3 errors, reset after 60 seconds
carrier_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=60)

@carrier_breaker
def call_carrier_api(order_data):
    # External carrier call
    ...

@app.post("/generate-label")
def generate_label(order_data: dict):
    try:
        return call_carrier_api(order_data)
    except pybreaker.CircuitBreakerError:
        raise HTTPException(503, "Carrier API unavailable. Retrying via Cloud Tasks.")
```

**Fallback strategies:**
1. **Queue for retry:** Push failed label generation back to Cloud Tasks with exponential backoff
2. **Alternative carrier:** If rules permit, failover to secondary carrier (e.g., USPS if FedEx API is down)

---

## Q8: Wave Scheduling — Custom Build Required

### What Commercial Tools Actually Do

| Capability | ShipStation/ShipBob | What Ecell Needs |
|-----------|-------------------|-----------------|
| Multi-location inventory | Supported via warehouses ([ShipStation](https://help.shipstation.com/hc/en-us/articles/360026158531-Set-Up-Manage-ShipStation-Internal-Inventory)) | Office ownership abstraction (not just physical stock) |
| Picking waves | Batches / Ready-to-Pick states ([ShipStation](https://help.shipstation.com/hc/en-us/articles/38623190668443-Mobile-Picking)) | Timezone-aware automatic release logic |
| Routing rules | Tags / automation rules ([ShipStation](https://help.shipstation.com/hc/en-us/articles/360047475631-Advanced-Automation-Rules)) | SLA-aware, cross-office, multi-factor routing engine |
| Network optimization | ShipBob: demand-based placement ([ShipBob](https://www.shipbob.com/product/inventory-placement/)) | Print capability + Amazon pathing + office staffing |
| Exception handling | Manual queue management | Auto-escalation to next office on missed cutoff |

Commercial tools handle "when do I release a batch?" through batches and rules, but they **assume the user already decided which warehouse owns the order**. Ecell needs timezone-governed cross-office orchestration — that belongs in your own service.

### Recommended Wave Model

| Office | Wave | Typical Responsibility |
|--------|------|----------------------|
| Philippines (PH) | Morning (Wave 1) | Overnight backlog, Asia/EU crossover orders |
| United Kingdom (UK) | Afternoon (Wave 2) | Midday reallocation, EU/UK carrier cutoffs |
| Florida (FL) | Afternoon (Wave 3) | Final North America same-day release, US carrier handoff |

### Wave Routing Sequence

```
1. ORDER ALLOCATION   → choose physical production/ship-from based on stock,
                        print capability, geography, channel constraints

2. OFFICE OWNERSHIP   → assign operational owner based on local office window,
                        order SLA, and backlog

3. WAVE RELEASE       → place order into wave bucket:
                        PH_MORNING_1, UK_AFTERNOON_1, US_AFTERNOON_2

4. PICK/PRINT RELEASE → convert wave to Ready-to-Pick / print / label jobs

5. EXCEPTION HANDOFF  → if wave misses cutoff or blocking condition exists,
                        reassign to next office or global exception queue
```

---

## Implementation Roadmap

### Phase 1: Foundation + Quick Wins (Weeks 1-4)

**Goal:** Unified order queue + Evri/Royal Mail label generation + daily tracking monitor

| # | Deliverable | Pain Point | Owner | Priority |
|:-:|-------------|-----------|-------|:--------:|
| 1 | Unified Order Queue (web portal) | P2.8 No dashboard | Jay Mark | HIGH |
| 2 | Picking List Generator (with product images from S3) | P2.5 No self-service | Jay Mark | HIGH |
| 3 | Evri CSV Auto-Generator | P2.2 Manual labels | Jay Mark | HIGH |
| 4 | 15-min BQ → Supabase incremental sync | Data foundation | Jay Mark + Ava | HIGH |
| 5 | Daily Tracking Monitor (flag no-scan after 24h) | P1.1 Lost shipments | Ava (cron) | **CRITICAL** |
| 6 | SRN Reconciliation (daily BQ integrity check) | Data quality | Ava | HIGH |
| 7 | Configurable Routing Rules table + UI | P1.4 Hardcoded PHP | Jay Mark + Ava | HIGH |

### Phase 2: Carrier Integration + Writeback (Weeks 5-8)

**Goal:** Automated label purchase across all carriers + tracking writeback

| # | Deliverable | Pain Point | Owner | Priority |
|:-:|-------------|-----------|-------|:--------:|
| 8 | Amazon Buy Shipping API (direct SP-API v2) | P2.2, P1.1 | Jay Mark | **CRITICAL** |
| 9 | Stamps.com API (USPS/UPS/DHL labels) | P2.2 | Jay Mark | HIGH |
| 10 | Royal Mail API (replaces Click & Drop) | P2.2 | Jay Mark | HIGH |
| 11 | Evri API via ShipStation | P2.2 | Jay Mark | HIGH |
| 12 | Marketplace Tracking Push (eBay, Walmart, Shopify) | P2.7 | Jay Mark | **CRITICAL** |
| 13 | Aurora tracking writeback (dedicated table + SQS) | P2.7 | Jay Mark | HIGH |
| 14 | Multi-Office RBAC (PH/UK/FL isolation) | P2.5 | Harry | MEDIUM |
| 15 | Rules Engine UI (CRUD + test mode) | P1.4 | Jay Mark + Ava | HIGH |

### Phase 3: Print Files + Vision QC (Weeks 9-12)

**Goal:** Replace IREN with cloud service + add packing verification

| # | Deliverable | Pain Point | Owner | Priority |
|:-:|-------------|-----------|-------|:--------:|
| 16 | Cloud Print Composition Service (IREN replacement) | P1.3 | Jay Mark + Chad | **CRITICAL** |
| 17 | "Send to Print" portal workflow | P1.3 | Jay Mark | HIGH |
| 18 | Vision QC Microservice (Gemini Vision) | P2.6 | Ava | MEDIUM |
| 19 | Packing Audit Trail (every QC check logged) | P2.6 | Ava | MEDIUM |
| 20 | Packaging Profiles (weight/dimensions per product type) | P2.10 | Jay Mark | MEDIUM |

### Phase 4: Optimization + Intelligence (Weeks 13+)

**Goal:** Carrier rate optimization + predictive analytics

| # | Deliverable | Pain Point | Owner | Priority |
|:-:|-------------|-----------|-------|:--------:|
| 21 | Carrier Rate Shopping (compare rates per shipment) | P2.9 | Future | MEDIUM |
| 22 | Predictive Dispatch (forecast volumes, optimize waves) | P2.5 | Future | MEDIUM |
| 23 | Cost Analytics (per-order shipping cost, margin impact) | P2.9 | Future | MEDIUM |

---

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|:------:|:----------:|------------|
| IREN PC failure before cloud replacement | CRITICAL | MEDIUM | Prioritize Chad's I/O spec (Section 6 of scope). Begin cloud print as parallel effort in Phase 1. |
| Amazon SP-API restricted role rejection | HIGH | LOW | Apply early (Week 0). ShipStation as interim bridge if delayed. |
| Zero schema change breaks portal sync | HIGH | LOW | Portal reads from BQ (downstream). Dedicated tracking table isolates writes. |
| Carrier API outage during peak season | HIGH | MEDIUM | Circuit breaker + Cloud Tasks retry + alternative carrier fallback. |
| Supabase connection exhaustion | MEDIUM | LOW | Supavisor pooler (400 connections on Small tier). Monitor via `pg_stat`. |
| BQ partition pruning not applied | LOW | MEDIUM | Use static `DATE BETWEEN` bounds in all sync queries. Monitor scan bytes in BQ console. |
| Print quality regression vs IREN | HIGH | MEDIUM | Golden-master testing with 100 top-selling SKUs before cutover. |
| Shadow mode reveals routing differences | LOW | HIGH | Expected. Use comparison reports to tune rules. Budget extra 1-2 weeks. |

---

## Shadow Mode Cutover Strategy

The portal must run in **shadow mode parallel to Zero for 1-2 weeks** before any production cutover. This is the council's strongest risk-mitigation recommendation given $5M+ annual revenue flowing through this system. ([Shadow Deployment Strategy — Codefresh](https://codefresh.io/learn/software-deployment/shadow-deployments-benefits-process-and-4-tips-for-success/))

| Phase | Duration | What Happens | Success Criteria |
|-------|:--------:|-------------|-----------------|
| Shadow Read | Week 1 | Portal reads same orders as Zero from BQ. Displays unified queue. No writes. | 100% SRN match with Zero. UI validated by PH/UK/FL teams. |
| Shadow Compute | Week 2 | Portal generates labels and routing decisions in parallel. Suppresses writes. | Label data matches Zero output for 95%+ orders. |
| Shadow Write | Week 3 | Portal writes tracking to dedicated Aurora table. Zero unaffected. | Tracking data accurate. No impact on Zero. |
| Controlled Cutover | Week 4 | Migrate one channel (e.g., Shopify) to portal-only. Zero handles rest. | 48 hours clean operation on migrated channel. |
| Full Cutover | Week 5+ | All channels through portal. Zero becomes read-only reference. | 1 week stable. Exception rate < 2%. |

### Testing Strategy

- **Carrier API Mocking:** Build a FastAPI mocking layer returning static JSON fixtures. Carrier sandboxes are unreliable — use them for integration testing only, not unit tests.
- **Shadow Comparator:** Automated script compares portal output vs Zero output per order: routing decision, carrier, rate, label data. Differences logged to BQ for analysis.
- **Error Handling:** Circuit breaker pattern (`pybreaker`) wraps each carrier. Fail-fast at 3 failures in 60 seconds. Cloud Tasks provides retry with exponential backoff.

---

## Monthly Cost Estimate

Estimated infrastructure costs at 500 orders/day. Does not include carrier label costs or developer time.

| Service | Tier | Est. Monthly Cost |
|---------|------|------------------:|
| Supabase (Postgres + Auth + RLS) | Pro | $25 |
| GCP Cloud Run (FastAPI + Next.js) | Serverless | $30-50 |
| GCP Cloud Tasks | Serverless | $5-10 |
| GCP Secret Manager (12 secrets) | Pay-per-use | <$5 |
| Redis / Memorystore | Basic 1GB | $30-40 |
| BigQuery (1 TiB free tier) | On-demand | $0-5 |
| Cloud Storage (print files) | Standard | $10-20 |
| PrinceXML license (server) | Server | $3,800/year (~$317/mo) |
| | | |
| **TOTAL (without PrinceXML)** | | **$105-135/mo** |
| **TOTAL (with PrinceXML)** | | **$420-450/mo** |

> **Note:** PrinceXML has a one-time server license. Alternative: open-source PDF/X pipeline with Pillow + reportlab (lower fidelity, $0 cost). Evaluate against IREN output quality before committing.

---

## Immediate Next Steps (Week 0)

| # | Action | Owner | Deadline | Blocker? |
|:-:|--------|-------|:--------:|:--------:|
| 1 | Send IREN I/O specification request to Chad (Section 6 of scope) | Cem | Week 0 | **YES** — blocks Phase 3 |
| 2 | Apply for Amazon SP-API Direct to Consumer Shipping restricted role | Cem / Jay Mark | Week 0 | **YES** — blocks Phase 2 |
| 3 | Provision Supabase Pro project + create `sync_watermarks` table | Jay Mark | Day 1 | No |
| 4 | Set up GCP Secret Manager with per-office naming convention | Jay Mark | Day 1 | No |
| 5 | Upgrade `sync_bq_orders.py` to 15-min incremental watermark pattern | Jay Mark / Ava | Day 2 | No |
| 6 | Create `order_tracking` table DDL in Aurora (dedicated DB user) | Jay Mark | Day 2 | No |
| 7 | Set up Cloud Run project + CI/CD pipeline (GitHub Actions) | Jay Mark | Day 3 | No |
| 8 | Register `order_tracking` in Datastream for automatic CDC to BQ | Jay Mark | Day 3 | No |
| 9 | Share this council report with Harry and Jay Mark for review | Cem | Day 1 | No |

---

## Sources

1. [Amazon Merchant Fulfillment API](https://developer-docs.amazon.com/sp-api/docs/merchant-fulfillment-api)
2. [Amazon Shipping API v1 Reference](https://developer-docs.amazon.com/sp-api/docs/shipping-api-v1-reference)
3. [ShipStation Amazon Buy Shipping (US)](https://help.shipstation.com/hc/en-us/articles/360025855992)
4. [ShipStation Amazon Marketplace](https://help.shipstation.com/hc/en-us/articles/360026140891-Amazon-Marketplace)
5. [FastAPI Deployment Concepts](https://fastapi.tiangolo.com/deployment/concepts/)
6. [Supabase Connecting to Postgres](https://supabase.com/docs/guides/database/connecting-to-postgres)
7. [Supavisor: Scaling Postgres to 1M Connections](https://supabase.com/blog/supavisor-1-million)
8. [Next.js Self-Hosting Guide](https://nextjs.org/docs/app/guides/self-hosting)
9. [AWS Event-Driven Architecture](https://aws.amazon.com/what-is/eda/)
10. [AWS Monolith vs Microservices](https://aws.amazon.com/compare/the-difference-between-monolithic-and-microservices-architecture/)
11. [AWS Supply Chain Lens](https://docs.aws.amazon.com/wellarchitected/latest/supply-chain-lens/welcome.html)
12. [Google Secret Manager](https://cloud.google.com/secret-manager/docs/overview)
13. [GCP Secret Manager vs HashiCorp Vault](https://infisical.com/blog/gcp-secret-manager-vs-hashicorp-vault)
14. [BigQuery Incremental Ingestion Optimization](https://cloud.google.com/blog/products/data-analytics/optimizing-your-bigquery-incremental-data-ingestion-pipelines)
15. [BigQuery Pricing](https://cloud.google.com/bigquery/pricing)
16. [PrinceXML Graphics Documentation](https://www.princexml.com/doc/13/graphics/)
17. [Pillow ImageCms Module](https://pillow.readthedocs.io/en/stable/reference/ImageCms.html)
18. [libvips 8.14 Release Notes](https://www.libvips.org/2022/12/22/What's-new-in-8.14.html)
19. [Supabase Vault](https://supabase.com/docs/guides/database/vault)
20. [Supabase Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
21. [Supabase Connection Limits](https://supabase.com/docs/guides/troubleshooting/how-to-change-max-database-connections-_BQ8P5)
22. [AWS Aurora MySQL Replication Best Practices](https://aws.amazon.com/blogs/database/overview-and-best-practices-of-multithreaded-replication-in-amazon-rds-for-mysql-amazon-rds-for-mariadb-and-amazon-aurora-mysql/)
23. [Shadow Deployment Strategy (Codefresh)](https://codefresh.io/learn/software-deployment/shadow-deployments-benefits-process-and-4-tips-for-success/)
24. [ShipStation Mobile Picking](https://help.shipstation.com/hc/en-us/articles/38623190668443-Mobile-Picking)
25. [ShipStation Advanced Automation Rules](https://help.shipstation.com/hc/en-us/articles/360047475631-Advanced-Automation-Rules)
26. [ShipBob Warehouse Mapping](https://www.shipbob.com/uk/blog/warehouse-mapping/)
27. [ShipBob Inventory Placement](https://www.shipbob.com/product/inventory-placement/)
28. [Shippo Batch Label Creation](https://docs.goshippo.com/docs/shipments/batchlabelcreation)
29. [EasyPost Home](https://www.easypost.com/home/)
30. [Cloud Run vs GKE](https://hivelogue.com/labs/cloudfunctions-vs-cloudrun-vs-gke)

---

*Cross-reference: PROJECT_SCOPE.md (original scope), BUILD_SOP.md (detailed implementation), Harry's SPEC.md (GDrive)*  
*Council run date: March 28, 2026 | Models: GPT-5.4, Claude Sonnet 4.6, Gemini 3.1 Pro*
