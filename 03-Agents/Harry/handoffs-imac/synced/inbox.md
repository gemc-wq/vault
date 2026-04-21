# Brain/Handoffs/inbox.md
## Shared Handoff Queue — New Tasks

*Format: one task per entry. Agent picks up, moves to doing.md, completes to done.md.*

---

<!-- Template:
### [TASK-001] Task title
- **owner:** harry | ava | shared
- **priority:** high | medium | low
- **from:** harry | ava | cem
- **created:** YYYY-MM-DD
- **definition of done:** ...
- **links:** ...
---
-->

*(empty — no pending handoffs)*
# Handoff: Ava → Harry
- **Date:** 2026-02-28 12:18
- **From:** Ava (CPSO)
- **To:** Harry (COO)
- **Status:** pending

## Task
Test handoff

## Detail
This is a test handoff from Ava to Harry via Shared Drive. System working.

---
# Handoff: Ava → Harry
- **Date:** 2026-02-28 12:19
- **From:** Ava (CPSO)
- **To:** Harry (COO)
- **Status:** pending

## Task
Handoff received

## Detail
Ava confirms: Harry-to-Ava SSH working. Ava-to-Harry rclone working. System fully operational.

---
# Handoff: Ava → Harry
- **Date:** 2026-02-28 12:24
- **From:** Ava (CPSO)
- **To:** Harry (COO)
- **Status:** pending

## Task
Sales Dashboard V2 — BigQuery Live Feed + Momentum

## Detail

## Summary
Build Sales Dashboard V2 with direct BigQuery feed (replacing CSV uploads) and momentum scoring algorithm.

## Architecture
- **Data source:** BigQuery `zero_dataset.orders` (project: instant-contact-479316-i4)
- **Auth:** gemc@ecellglobal.com (gcloud already configured)
- **Deploy:** Cloud Run (same as V1 pattern)
- **Frontend:** React dashboard (existing sales-dashboard repo)

## What's New in V2

### 1. Live BigQuery Feed
Replace CSV upload with direct queries to `zero_dataset.orders`:
- Schema: Brand, Custom_Label (SKU), Currency, Net_Sale, Quantity, PO_Date, Is_Refunded, Marketplace, Buyer_Country, Product, Unit
- Apply FX conversion: GBP*1.27, EUR*1.08, USD*1.0, CAD*0.71, AUD*0.64, JPY*0.0067

### 2. Momentum Algorithm (built + tested by Ava)
Three time windows: 6-month, 3-month, 1-month
- monthly_rate_6m = rev_6m / 6
- monthly_rate_3m = rev_3m / 3
- monthly_rate_1m = rev_1m (latest month)
- momentum_score = (monthly_rate_1m * 0.5) + (monthly_rate_3m * 0.3) + (monthly_rate_6m * 0.2)
- Trend flags: 🚀 Accelerating | 📈 Growing | ➡️ Stable | 📉 Declining

### 3. Views Required
- Revenue by Brand (ranked by momentum score)
- Trend Direction column with emoji flags
- Marketplace Breakdown (Amazon US/UK, Rakuten, eBay, etc.)
- Device Brand split (Apple, Samsung, etc.)
- Product Type split (case types)
- Opportunities tab (already built in commit 58dbc15 — merge this in)

### 4. Cloud Run Requirements
- BigQuery client library (Node.js: @google-cloud/bigquery)
- Service account with BigQuery Data Viewer role on project instant-contact-479316-i4
- CORS configured for ecell.app embedding

## Reference Files
- Momentum analysis: Brain/Projects/goheadcase/MOMENTUM_ANALYSIS.md
- Momentum raw data: Ava workspace projects/goheadcase-shopify/data/momentum_raw.csv
- Python script: Ava workspace projects/goheadcase-shopify/scripts/momentum_analysis.py
- V1 repo: gemc-wq/sales-dashboard (or gemc99-boop fork)

## Priority
HIGH — Cem approved 2026-02-28


---
# Handoff: Ava → Harry
- **Date:** 2026-02-28 15:05
- **From:** Ava (CPSO)
- **To:** Harry (COO)
- **Status:** pending

## Task
Calendar API Access + Cron Visibility

## Detail

## Request
1. Give Ava API write access to the ecell.app Calendar — either direct API endpoint or a shared webhook where I can push events.
2. Alternatively, add a /cron-dashboard page to ecell.app that reads from a shared JSON file on Drive listing all agent cron jobs.

## Context
- Cem wants centralized visibility of all scheduled tasks across agents (Ava, Sven, Harry)
- Ava's current crons: Nightly mission (2AM), Weekly Amazon review (Sat 8AM), Heartbeat (~30min)
- Sven: No crons yet but will need benchmark capture schedules
- Harry: Daily trend scraping, marketing content pipeline

## Proposed Format (Brain/Schedules/cron_registry.json)
{
  "jobs": [
    {"agent": "ava", "name": "Nightly Mission", "schedule": "0 2 * * *", "model": "gemini-flash"},
    {"agent": "ava", "name": "Amazon Review", "schedule": "0 8 * * 6", "model": "gemini-flash"},
    {"agent": "sven", "name": "Benchmark Capture", "schedule": "TBD", "model": "gemini-3.1"}
  ]
}

## Priority: MEDIUM (not blocking microsites, but Cem wants it)


---
# Handoff: Ava → Harry
- **Date:** 2026-02-28 17:33
- **From:** Ava (CPSO)
- **To:** Harry (COO)
- **Status:** pending

## Task
Orbit PM — Deploy POST endpoint + Add missing projects

## Detail

## What I did
Added a POST endpoint to /api/tasks/route.ts in the orbit-pm project that supports upsert (create or update tasks).
Code is at: /Users/clawdbot/.openclaw/workspace/projects/orbit-pm/app/api/tasks/route.ts

## What's needed
1. Deploy the updated Orbit PM to Vercel/Cloud Run
2. Once POST works, I'll bulk-create these missing project tasks:

NEW TASKS TO ADD:
- goheadcase-anime-microsite | Ava | URGENT | GoHeadCase Anime Microsite — Phase 1
- goheadcase-shopify-migration | Ava+Harry | HIGH | GoHeadCase Shopify Migration (100-200K SKUs)
- sales-dashboard-v2 | Harry | HIGH | Sales Dashboard V2 — BigQuery Live Feed
- sven-rag-corpus | Sven | HIGH | RAG Benchmark Corpus — Pattern Cards + Templates
- ecell-studio-pipeline | Sven | HIGH | Ecell Studio — Gemini Image Pipeline
- supabase-shopify-sync | Harry | HIGH | Supabase → Shopify Sync Pipeline
- fulfillment-orchestrator | Harry | MEDIUM | Fulfillment Orchestrator (ShipStation replacement)
- target-plus-integration | Ava | MEDIUM | Target+ / Walmart via Shopify Connect
- calendar-cron-visibility | Harry | MEDIUM | Calendar API + Cron Dashboard
- vector-memory-phase2 | Harry | LOW | Semantic Memory (Supabase pgvector) — Phase 2

## Priority: HIGH — Cem wants all projects tracked in Orbit


---
