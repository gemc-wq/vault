# Amazon Multi-Marketplace Listings Data Pipeline

## PRD + SOP Addendum — Data Integrity, Staging & Delta Sync

**Version:** 1.1  
**Date:** April 2026  
**Owner:** Head Case Designs — CEO  
**Scope:** US (primary), UK (SFP), DE (monitored) — FR/IT/ES ad-hoc only  
**File sizes:** 6–10 GB per marketplace download  

---

## 1. Market Tier Model

Not all six marketplaces warrant the same investment in automation. This document applies a tiered structure:

| Tier | Marketplace | Revenue Weight | Fulfilment Model | Pipeline Treatment |
|---|---|---|---|---|
| **Tier 1 — Core** | 🇺🇸 United States | Primary | FBA + FBM | Fully structured. Biweekly automated pipeline. Scoring + restock + conversion decisions. |
| **Tier 1 — Core** | 🇬🇧 United Kingdom | ~50% of US | FBM + SFP (Nationwide Prime) | Fully structured. Biweekly automated pipeline. SFP eligibility decisions included. |
| **Tier 2 — Monitored** | 🇩🇪 Germany | Supplementary | FBM only | Structured staging, but scoring and decisions run ad-hoc (monthly or when flagged). No FBA. |
| **Tier 3 — Ad-hoc** | 🇫🇷 France | Low | FBM only | Manual pull when needed. No dedicated pipeline. No FBA. |
| **Tier 3 — Ad-hoc** | 🇮🇹 Italy | Low | FBM only | Manual pull when needed. No dedicated pipeline. No FBA. |
| **Tier 3 — Ad-hoc** | 🇪🇸 Spain | Low | FBM only | Manual pull when needed. No dedicated pipeline. No FBA. |

**What this means in practice:**
- All automation build effort focuses on US + UK first
- DE gets the same staging schema but is excluded from biweekly scoring runs until you choose to escalate it
- FR/IT/ES data can be pulled and staged on demand, using the same scripts, but are not part of any scheduled pipeline
- FBA logic (restock, conversion scoring, Prime badge opportunity) applies to **US only**
- SFP logic applies to **UK only** (Royal Mail 2-day tracked ~£4–6, significantly better unit economics than US SFP)

---

## 2. The Problem

The biweekly FBA/FBM optimisation system (PRD v1.0) assumes clean, marketplace-isolated data as input. In reality:

- **Raw listing files are 6–10 GB each** — no marketplace column exists; US and UK files have identical headers
- **Shipping templates are marketplace-specific** — US templates (`US_Standard_Shipping`) are meaningless in UK Seller Central
- **SFP eligibility is UK-specific** — Nationwide Prime badge rules differ from US Seller-Fulfilled Prime entirely
- **Amazon constantly mutates listings** — suppressions, IP takedowns, policy corrections, new uploads mid-cycle
- **Full reloads every cycle are wasteful** — 95%+ of listings don't change between biweekly runs

Without a staging strategy, you're one accidental file swap away from running UK SFP decisions against US shipping templates.

---

## 3. Data Sources — What You're Actually Downloading

### 3.1 Primary Listings Reports

| Report | reportType | Output | Size (est.) | Marketplace Constraint |
|---|---|---|---|---|
| All Listings Report | `GET_MERCHANT_LISTINGS_ALL_DATA` | Tab-delimited flat file | 6–10 GB per marketplace | **One marketplace per request** |
| Active Listings Report | `GET_MERCHANT_LISTINGS_DATA` | Tab-delimited flat file | 4–8 GB per marketplace | One marketplace per request |
| Inactive Listings Report | `GET_MERCHANT_LISTINGS_INACTIVE_DATA` | Tab-delimited flat file | 1–3 GB per marketplace | One marketplace per request |
| Suppressed Listings Report | `GET_MERCHANTS_LISTINGS_FYP_REPORT` | Tab-delimited flat file | 10–200 MB per marketplace | One marketplace per request |
| Cancelled Listings Report | `GET_MERCHANT_CANCELLED_LISTINGS_DATA` | Tab-delimited flat file | 50–500 MB per marketplace | One marketplace per request |

**Key columns in `GET_MERCHANT_LISTINGS_ALL_DATA`:**

```
item-name, item-description, listing-id, seller-sku, price, quantity,
open-date, image-url, item-is-marketplace, product-id-type, zshop-shipping-default,
item-note, item-condition, zshop-category1, zshop-browse-path, zshop-storefront-feature,
asin1, date-created, is-b2b, merchant-shipping-group, fulfillment-channel
```

> **Critical:** The `merchant-shipping-group` column is marketplace-specific. A shipping template called "US_Standard_Shipping" has no meaning in UK Seller Central. This is the #1 source of cross-marketplace data corruption.

### 3.2 SP-API Marketplace IDs

Every API call and every file must be tagged with the correct marketplace ID:

| Country | Marketplace ID | Region Endpoint | Currency | Pipeline Tier |
|---|---|---|---|---|
| United States | `ATVPDKIKX0DER` | `sellingpartnerapi-na.amazon.com` | USD | **Tier 1 — automated** |
| United Kingdom | `A1F83G8C2ARO7P` | `sellingpartnerapi-eu.amazon.com` | GBP | **Tier 1 — automated** |
| Germany | `A1PA6795UKMFR9` | `sellingpartnerapi-eu.amazon.com` | EUR | **Tier 2 — staged, ad-hoc scoring** |
| France | `A13V1IB3VIYZZH` | `sellingpartnerapi-eu.amazon.com` | EUR | Tier 3 — manual only |
| Italy | `APJ6JRA9NG5V4` | `sellingpartnerapi-eu.amazon.com` | EUR | Tier 3 — manual only |
| Spain | `A1RKKUPIHCS9HS` | `sellingpartnerapi-eu.amazon.com` | EUR | Tier 3 — manual only |

> **Rule:** Never combine marketplaces in a single report request. Even though the `createReport` API accepts multiple `marketplaceIds`, the `All Listings Report` only returns data for the first one. Always request one marketplace per call.

### 3.3 Manual Seller Central Fallback Paths

When SP-API roles aren't active yet (pending Patrick's approval):

| Marketplace | Seller Central URL | Navigation | Priority |
|---|---|---|---|
| US | `sellercentral.amazon.com` | Reports → Inventory Reports → Active Listings Report → Request | **Biweekly — must do** |
| UK | `sellercentral.amazon.co.uk` | Same path | **Biweekly — must do** |
| DE | `sellercentral.amazon.de` | Same path | Monthly or on-demand |
| FR | `sellercentral.amazon.fr` | Same path | Ad-hoc only |
| IT | `sellercentral.amazon.it` | Same path | Ad-hoc only |
| ES | `sellercentral.amazon.es` | Same path | Ad-hoc only |

**File naming convention on download:**
```
{marketplace}_{report_type}_{YYYY-MM-DD}.txt
```
Example: `US_ALL_LISTINGS_2026-04-15.txt`, `UK_ALL_LISTINGS_2026-04-15.txt`

> **Never rename after download.** The marketplace prefix is your chain-of-custody tag. If a file doesn't have a marketplace prefix, reject it.

---

## 4. Recommended Architecture — Three-Tier Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        TIER 1: LOCAL STAGING                           │
│                     (MySQL 8.x on local machine)                       │
│                                                                        │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│   │  US_RAW   │  │  UK_RAW   │  │  DE_RAW   │  │  FR/IT/ES — ad-hoc  │  │
│   │ listings  │  │ listings  │  │ listings  │  │  pull only, no auto  │  │
│   │(biweekly) │  │(biweekly) │  │ (monthly) │  │  pipeline           │  │
│   └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └──────────────────────┘  │
│         │              │              │            │       │       │    │
│         └──────────────┴──────────────┴────────────┴───────┴───────┘    │
│                                    │                                    │
│                        ┌───────────▼───────────┐                       │
│                        │   VALIDATION LAYER     │                       │
│                        │  - Schema checks       │                       │
│                        │  - Marketplace tagging  │                       │
│                        │  - Row hash generation  │                       │
│                        │  - Dedup + clean        │                       │
│                        └───────────┬───────────┘                       │
│                                    │                                    │
│                        ┌───────────▼───────────┐                       │
│                        │   UNIFIED_LISTINGS     │                       │
│                        │  (marketplace-tagged,   │                       │
│                        │   deduplicated, hashed) │                       │
│                        └───────────┬───────────┘                       │
└────────────────────────────────────┼────────────────────────────────────┘
                                     │
                                     │  Delta export (changed rows only)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    TIER 2: CLOUD WAREHOUSE                              │
│                       (Google BigQuery)                                 │
│                                                                        │
│   Project: instant-contact-479316-i4                                   │
│   Dataset: amazon_listings                                             │
│                                                                        │
│   ┌─────────────────────────────────────────┐                          │
│   │  listings_master (partitioned by         │                          │
│   │    marketplace, clustered by sku+asin)   │                          │
│   ├─────────────────────────────────────────┤                          │
│   │  listings_history (append-only, SCD2)    │                          │
│   ├─────────────────────────────────────────┤                          │
│   │  listings_suppressed (current snapshot)  │                          │
│   ├─────────────────────────────────────────┤                          │
│   │  listings_delta_log (change audit trail) │                          │
│   └─────────────────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │  Materialised views / exports
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    TIER 3: OPERATIONAL LAYER                            │
│                        (Supabase Postgres)                              │
│                                                                        │
│   ┌──────────────────────────────────────┐                             │
│   │  active_listings (lightweight,        │                             │
│   │    biweekly scoring input)            │                             │
│   ├──────────────────────────────────────┤                             │
│   │  restock_queue (output of scoring)    │                             │
│   ├──────────────────────────────────────┤                             │
│   │  conversion_candidates (FBM→FBA)      │                             │
│   ├──────────────────────────────────────┤                             │
│   │  blank_inventory (warehouse stock)    │                             │
│   └──────────────────────────────────────┘                             │
│                                                                        │
│   → Feeds dashboards, OpenClaw, biweekly SOP queries                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Why Three Tiers?

| Tier | Tool | Purpose | Why This Tool |
|---|---|---|---|
| **Tier 1 — Local Staging** | MySQL 8.x (local) | Ingest raw files, validate, hash, produce delta | You already have MySQL expertise (Aurora RDS). `LOAD DATA INFILE` handles 10 GB files in ~3–5 minutes. No cloud egress costs. Full control over validation before anything goes upstream. |
| **Tier 2 — Cloud Warehouse** | BigQuery (`instant-contact-479316-i4`) | Historical record, cross-marketplace analytics, heavy queries | You already have BigQuery with DataStream from Aurora. Columnar storage makes 24M-row analytical queries sub-second. Partitioning by marketplace + date eliminates cross-contamination at the storage layer. First 1 TB/month of queries free. |
| **Tier 3 — Operational** | Supabase (Postgres) | Live operational tables for the biweekly SOP, dashboards, OpenClaw | Row-level security, real-time subscriptions, REST API for dashboards. Lightweight — only holds active/actionable rows, not the full 24M catalogue. |

### 4.2 Why NOT Just One Tool?

| Single-tool approach | Problem |
|---|---|
| **MySQL only** | No analytical horsepower for 24M rows × 6 marketplaces. Local machine can't serve dashboards or OpenClaw remotely. No historical partitioning. |
| **BigQuery only** | Pay-per-query gets expensive if OpenClaw or dashboards poll frequently. No `LOAD DATA INFILE` equivalent — must stage files in GCS first. Can't do transactional writes (restock queue updates). |
| **Supabase only** | Postgres on Supabase chokes on 24M+ row bulk loads. Supabase COPY ingests 5 GB in ~160 seconds (benchmarked), but index maintenance during load kills performance. Storage limits on lower tiers. |

### 4.3 What About Local LLM (Gemma 4)?

Gemma 4 (26B-A4B MoE or 31B Dense) is useful but **not for bulk data processing**. Here's where it fits:

| Use Case | Gemma 4 Role | Better Alternative |
|---|---|---|
| **Bulk CSV loading/hashing** | No — too slow, wrong tool | MySQL `LOAD DATA INFILE` |
| **Listing quality audit** | Yes — review flagged listings for title/bullet quality | Batch 50–100 listings at a time through Gemma 4 with structured JSON output |
| **Suppression root cause analysis** | Yes — parse suppression reasons, suggest fixes | Feed `GET_MERCHANTS_LISTINGS_FYP_REPORT` rows through Gemma 4 |
| **IP flag triage** | Yes — classify IP notices, suggest response templates | Local LLM keeps sensitive IP data off cloud APIs |
| **Anomaly narration** | Yes — explain why a listing's metrics changed | After delta detection, have Gemma 4 narrate the top 50 changes |

**Recommended setup:** Run Gemma 4 26B-A4B via Ollama on a local machine with 16+ GB RAM. Feed it structured prompts post-staging, not raw CSV. It's a quality layer, not an ETL layer.

---

## 5. Schema Design — Marketplace Isolation

### 5.1 Local MySQL Staging Schema

```sql
-- Database per marketplace (hard isolation)
-- Tier 1 (automated, biweekly): amazon_us, amazon_uk
-- Tier 2 (structured, ad-hoc): amazon_de
-- Tier 3 (ad-hoc pull only, same schema): amazon_fr, amazon_it, amazon_es
CREATE DATABASE amazon_us;
CREATE DATABASE amazon_uk;
CREATE DATABASE amazon_de;
CREATE DATABASE amazon_fr;   -- ad-hoc only
CREATE DATABASE amazon_it;   -- ad-hoc only
CREATE DATABASE amazon_es;   -- ad-hoc only

-- Identical table structure in each database
-- Example for amazon_us:
USE amazon_us;

CREATE TABLE raw_listings (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    load_batch_id       VARCHAR(20) NOT NULL,        -- e.g. '2026-04-15'
    seller_sku          VARCHAR(100) NOT NULL,
    asin                VARCHAR(20),
    item_name           TEXT,
    price               DECIMAL(10,2),
    quantity            INT,
    fulfillment_channel VARCHAR(20),                  -- AMAZON_NA / DEFAULT
    merchant_shipping_group VARCHAR(200),
    item_condition      VARCHAR(50),
    listing_id          VARCHAR(50),
    open_date           VARCHAR(50),
    image_url           TEXT,
    status              VARCHAR(20) DEFAULT 'ACTIVE', -- ACTIVE/INACTIVE/SUPPRESSED
    row_hash            CHAR(64),                     -- SHA-256 of key fields
    loaded_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_sku (seller_sku),
    INDEX idx_asin (asin),
    INDEX idx_hash (row_hash),
    INDEX idx_batch (load_batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Unified view across all marketplaces (read-only, for delta export)
-- Created in a separate 'amazon_unified' database
CREATE DATABASE amazon_unified;
USE amazon_unified;

CREATE TABLE listings_master (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    marketplace         CHAR(2) NOT NULL,             -- US/UK/DE/FR/IT/ES
    marketplace_id      VARCHAR(20) NOT NULL,          -- ATVPDKIKX0DER etc.
    seller_sku          VARCHAR(100) NOT NULL,
    asin                VARCHAR(20),
    item_name           TEXT,
    price               DECIMAL(10,2),
    currency            CHAR(3),                       -- USD/GBP/EUR
    quantity            INT,
    fulfillment_channel VARCHAR(20),
    merchant_shipping_group VARCHAR(200),
    status              VARCHAR(20),
    row_hash            CHAR(64),
    first_seen_date     DATE,
    last_seen_date      DATE,
    last_changed_date   DATE,
    change_type         VARCHAR(20),                   -- NEW/UPDATED/UNCHANGED/REMOVED
    cycle_id            VARCHAR(20),                   -- '2026-W16'
    
    UNIQUE KEY uk_marketplace_sku (marketplace, seller_sku),
    INDEX idx_asin (asin),
    INDEX idx_hash (row_hash),
    INDEX idx_change (change_type),
    INDEX idx_status (status),
    INDEX idx_cycle (cycle_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 5.2 Why Separate Databases, Not Just a Marketplace Column?

1. **Physical isolation** — A botched US load can't corrupt UK data. You can drop and reload `amazon_us.raw_listings` without touching any other marketplace.
2. **Independent load timing** — UK file arrives at 9:00 AM, US at 9:45 AM. Load them independently without blocking.
3. **Shipping template safety** — `merchant_shipping_group` values are only meaningful within their marketplace database. No accidental cross-joins possible.
4. **Parallel `LOAD DATA INFILE`** — MySQL can load 6 files simultaneously into 6 databases without lock contention.
5. **Easy purge** — After merging into `amazon_unified.listings_master`, truncate the raw tables to reclaim disk space.

### 5.3 BigQuery Schema

```sql
-- Partitioned by marketplace, clustered by seller_sku
CREATE TABLE `instant-contact-479316-i4.amazon_listings.listings_master` (
    marketplace         STRING NOT NULL,
    marketplace_id      STRING NOT NULL,
    seller_sku          STRING NOT NULL,
    asin                STRING,
    item_name           STRING,
    price               FLOAT64,
    currency            STRING,
    quantity            INT64,
    fulfillment_channel STRING,
    merchant_shipping_group STRING,
    status              STRING,
    row_hash            STRING,
    first_seen_date     DATE,
    last_seen_date      DATE,
    last_changed_date   DATE,
    change_type         STRING,
    cycle_id            STRING,
    loaded_at           TIMESTAMP
)
PARTITION BY marketplace
CLUSTER BY seller_sku, asin;

-- History table (SCD Type 2 — append-only)
CREATE TABLE `instant-contact-479316-i4.amazon_listings.listings_history` (
    marketplace         STRING NOT NULL,
    seller_sku          STRING NOT NULL,
    asin                STRING,
    field_changed       STRING,       -- e.g. 'price', 'quantity', 'status'
    old_value           STRING,
    new_value           STRING,
    changed_at          TIMESTAMP,
    cycle_id            STRING
)
PARTITION BY DATE(changed_at)
CLUSTER BY marketplace, seller_sku;
```

### 5.4 Supabase Operational Schema

> Only US and UK data flows into Supabase operational tables on a biweekly cadence. DE can be queried directly from BigQuery when needed. FR/IT/ES never touch Supabase in the automated pipeline.

```sql
-- Only US + UK active, actionable listings (subset of BigQuery master)
-- DE/FR/IT/ES are NOT in this table in the automated pipeline
CREATE TABLE active_listings (
    marketplace         CHAR(2) NOT NULL,
    seller_sku          VARCHAR(100) NOT NULL,
    asin                VARCHAR(20),
    item_name           TEXT,
    price               DECIMAL(10,2),
    currency            CHAR(3),
    quantity            INT,
    fulfillment_channel VARCHAR(20),
    merchant_shipping_group VARCHAR(200),
    status              VARCHAR(20),
    last_changed_date   DATE,
    
    PRIMARY KEY (marketplace, seller_sku)
);

-- Enable Row Level Security for marketplace isolation in dashboards
ALTER TABLE active_listings ENABLE ROW LEVEL SECURITY;

CREATE POLICY marketplace_isolation ON active_listings
    USING (marketplace = current_setting('app.current_marketplace')::text);

-- UK-specific: SFP eligibility table
CREATE TABLE uk_sfp_candidates (
    seller_sku          VARCHAR(100) PRIMARY KEY,
    asin                VARCHAR(20),
    item_name           TEXT,
    price               DECIMAL(10,2),    -- GBP
    sessions_30d        INT,
    cvr_30d             DECIMAL(5,2),
    unified_score       DECIMAL(4,2),
    sfp_break_even_asp  DECIMAL(10,2),    -- Category minimum (Cases £18, Mats £24)
    sfp_eligible        BOOLEAN,          -- price >= break_even_asp
    royal_mail_cost_est DECIMAL(10,2),    -- ~£4.00–6.00 for 2-day tracked
    sfp_margin_est      DECIMAL(10,2),
    last_scored_date    DATE
);

-- US-specific: FBA restock + conversion queue
CREATE TABLE us_fba_action_queue (
    seller_sku          VARCHAR(100) PRIMARY KEY,
    asin                VARCHAR(20),
    action_type         VARCHAR(20),      -- RESTOCK / CONVERT / SFP_TRIAL / SUPPRESS
    tier                VARCHAR(5),       -- T1/T2/T3/T4
    unified_score       DECIMAL(4,2),
    suggested_qty       INT,
    ship_by_date        DATE,
    days_of_supply      INT,
    last_scored_date    DATE
);
```

---

## 6. Data Integrity Rules — The Non-Negotiable Checklist

### 6.1 Ingest-Time Validation (Before Loading)

| Check | Rule | Action on Failure |
|---|---|---|
| **File naming** | Must match `{MP}_*.txt` where MP ∈ {US, UK, DE, FR, IT, ES} | Reject file. Do not load. |
| **Header validation** | First row must contain expected column headers | Reject file. Column schema may have changed. |
| **Encoding** | Must be UTF-8 or Latin-1. Detect with `chardet`. | Convert to UTF-8 before load. |
| **Row count sanity** | Compare row count to previous cycle. Flag if delta > ±20%. | Warn operator. Possible partial download or Amazon API issue. |
| **Currency cross-check** | If marketplace = UK, prices must be in GBP range (not USD range). | Flag for manual review. Likely wrong file loaded into wrong database. |
| **SFP template check (UK)** | UK `merchant_shipping_group` must reference valid UK shipping templates (e.g. Nationwide Prime templates). US SFP templates in UK data = cross-contamination. | Reject rows. Alert operator. |
| **Shipping template cross-check** | `merchant_shipping_group` values must exist in the marketplace's known template list | Flag rows with unknown templates. Possible cross-marketplace contamination. |
| **BOM stripping** | Strip `\uFEFF` from first column header and any leading/trailing whitespace | Auto-fix before load. |

### 6.2 Row-Level Hashing for Change Detection

Generate a SHA-256 hash of the mutable fields that matter for your optimisation decisions:

```python
import hashlib

def compute_row_hash(row):
    """Hash the fields that, if changed, require re-scoring."""
    hashable = '|'.join([
        str(row.get('seller_sku', '')),
        str(row.get('price', '')),
        str(row.get('quantity', '')),
        str(row.get('fulfillment_channel', '')),
        str(row.get('merchant_shipping_group', '')),
        str(row.get('item_condition', '')),
        str(row.get('status', '')),
    ])
    return hashlib.sha256(hashable.encode('utf-8')).hexdigest()
```

Or in MySQL directly during load:

```sql
UPDATE raw_listings 
SET row_hash = SHA2(
    CONCAT_WS('|', 
        seller_sku, 
        COALESCE(price, ''), 
        COALESCE(quantity, ''), 
        COALESCE(fulfillment_channel, ''), 
        COALESCE(merchant_shipping_group, ''),
        COALESCE(item_condition, ''),
        COALESCE(status, '')
    ), 256
)
WHERE load_batch_id = '2026-04-15';
```

### 6.3 Cross-Marketplace Integrity Constraints

| Rule | Implementation |
|---|---|
| **Never JOIN across raw marketplace databases** | Only join through `amazon_unified.listings_master` where the marketplace column is explicit |
| **FBA twin lookup** | ASIN is the bridge. Same ASIN can exist in US and UK with different SKUs. Always filter by marketplace first: `WHERE marketplace = 'US' AND asin = 'B0...'` |
| **SKU prefix convention** | FBA SKUs start with 'F'. FBM twin = remove first character. This convention is marketplace-independent — the same SKU may exist in all 6 marketplaces. Always include marketplace in the lookup key. |
| **Price comparisons** | Never compare prices across marketplaces without currency conversion. USD ≠ GBP ≠ EUR. |

---

## 7. Delta Sync Strategy — Biweekly Updates

### 7.1 The Problem with Full Reloads

| Metric | Full Reload | Delta Only |
|---|---|---|
| Data volume | ~36–60 GB (all 6 marketplaces) | ~1–3 GB (changed rows only) |
| MySQL load time | ~30–45 minutes | ~3–5 minutes |
| BigQuery upload cost | ~$0.30 (60 GB × $5/TB) | ~$0.015 |
| BigQuery query cost | Full table scan if not partitioned | Touch only changed partitions |
| Risk of corruption | Higher (more data = more failure points) | Lower (smaller surface area) |

### 7.2 Delta Detection Algorithm

```
EVERY BIWEEKLY CYCLE:

1. Download fresh All Listings Report for each marketplace
   (this is always a full snapshot — Amazon doesn't offer delta reports)

2. Load into per-marketplace raw_listings table (TRUNCATE + LOAD DATA INFILE)

3. Compute row_hash for every row in raw_listings

4. Compare against listings_master:

   DELTA CLASSIFICATION:
   ┌─────────────────────────────────┬──────────────────────────────────┐
   │  In raw_listings, NOT in master │  → change_type = 'NEW'          │
   ├─────────────────────────────────┼──────────────────────────────────┤
   │  In both, hash MATCHES          │  → change_type = 'UNCHANGED'    │
   ├─────────────────────────────────┼──────────────────────────────────┤
   │  In both, hash DIFFERS          │  → change_type = 'UPDATED'      │
   ├─────────────────────────────────┼──────────────────────────────────┤
   │  In master, NOT in raw_listings │  → change_type = 'REMOVED'      │
   └─────────────────────────────────┴──────────────────────────────────┘

5. Export ONLY rows where change_type ∈ ('NEW', 'UPDATED', 'REMOVED')
   to BigQuery and Supabase

6. For 'UPDATED' rows, log the specific field changes to listings_history
```

### 7.3 SQL Implementation — Delta Detection

```sql
-- Run this in amazon_unified after loading all raw marketplace databases

-- Step 1: Mark NEW listings
INSERT INTO listings_master (marketplace, marketplace_id, seller_sku, asin, 
    item_name, price, currency, quantity, fulfillment_channel, 
    merchant_shipping_group, status, row_hash, first_seen_date, 
    last_seen_date, last_changed_date, change_type, cycle_id)
SELECT 
    'US', 'ATVPDKIKX0DER', r.seller_sku, r.asin,
    r.item_name, r.price, 'USD', r.quantity, r.fulfillment_channel,
    r.merchant_shipping_group, r.status, r.row_hash,
    CURDATE(), CURDATE(), CURDATE(), 'NEW', '2026-W16'
FROM amazon_us.raw_listings r
LEFT JOIN listings_master m 
    ON m.marketplace = 'US' AND m.seller_sku = r.seller_sku
WHERE m.seller_sku IS NULL;

-- Step 2: Mark UPDATED listings (hash mismatch)
UPDATE listings_master m
INNER JOIN amazon_us.raw_listings r 
    ON m.marketplace = 'US' AND m.seller_sku = r.seller_sku
SET 
    m.item_name = r.item_name,
    m.price = r.price,
    m.quantity = r.quantity,
    m.fulfillment_channel = r.fulfillment_channel,
    m.merchant_shipping_group = r.merchant_shipping_group,
    m.status = r.status,
    m.row_hash = r.row_hash,
    m.last_seen_date = CURDATE(),
    m.last_changed_date = CURDATE(),
    m.change_type = 'UPDATED',
    m.cycle_id = '2026-W16'
WHERE m.row_hash != r.row_hash;

-- Step 3: Mark UNCHANGED (hash matches — just bump last_seen_date)
UPDATE listings_master m
INNER JOIN amazon_us.raw_listings r 
    ON m.marketplace = 'US' AND m.seller_sku = r.seller_sku
SET 
    m.last_seen_date = CURDATE(),
    m.change_type = 'UNCHANGED',
    m.cycle_id = '2026-W16'
WHERE m.row_hash = r.row_hash;

-- Step 4: Mark REMOVED (in master but not in raw)
UPDATE listings_master m
LEFT JOIN amazon_us.raw_listings r 
    ON m.marketplace = 'US' AND m.seller_sku = r.seller_sku
SET 
    m.change_type = 'REMOVED',
    m.status = 'REMOVED',
    m.last_changed_date = CURDATE(),
    m.cycle_id = '2026-W16'
WHERE m.marketplace = 'US' 
    AND r.seller_sku IS NULL 
    AND m.change_type != 'REMOVED';

-- Repeat Steps 1-4 for UK, DE, FR, IT, ES
-- (parameterise marketplace, marketplace_id, currency, source database)
```

### 7.4 Delta Export to BigQuery

```python
# Export only changed rows to BigQuery
# Using the google-cloud-bigquery library (already in your stack)
# Note: BigQuery receives delta from ALL staged marketplaces (US, UK, DE)
# Supabase receives US + UK only

from google.cloud import bigquery
import pandas as pd
import pymysql

# Connect to local MySQL
conn = pymysql.connect(host='127.0.0.1', user='root', db='amazon_unified')

# Extract delta only — all staged marketplaces
delta_df = pd.read_sql("""
    SELECT * FROM listings_master 
    WHERE change_type IN ('NEW', 'UPDATED', 'REMOVED')
    AND cycle_id = '2026-W16'
""", conn)

print(f"Delta rows: {len(delta_df):,} out of ~4M total")

# Upload to BigQuery
client = bigquery.Client(project='instant-contact-479316-i4')
job_config = bigquery.LoadJobConfig(
    write_disposition='WRITE_APPEND',  # Append to history
    schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION],
)

# Upsert into listings_master using MERGE
# First load delta to a staging table
staging_table = 'instant-contact-479316-i4.amazon_listings.listings_staging'
job = client.load_table_from_dataframe(delta_df, staging_table, job_config=job_config)
job.result()

# Then MERGE into master
merge_query = """
MERGE `instant-contact-479316-i4.amazon_listings.listings_master` T
USING `instant-contact-479316-i4.amazon_listings.listings_staging` S
ON T.marketplace = S.marketplace AND T.seller_sku = S.seller_sku
WHEN MATCHED THEN
    UPDATE SET 
        T.item_name = S.item_name,
        T.price = S.price,
        T.currency = S.currency,
        T.quantity = S.quantity,
        T.fulfillment_channel = S.fulfillment_channel,
        T.merchant_shipping_group = S.merchant_shipping_group,
        T.status = S.status,
        T.row_hash = S.row_hash,
        T.last_seen_date = S.last_seen_date,
        T.last_changed_date = S.last_changed_date,
        T.change_type = S.change_type,
        T.cycle_id = S.cycle_id,
        T.loaded_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
    INSERT ROW;
"""
client.query(merge_query).result()
```

### 7.5 Delta Export to Supabase (US + UK Only)

```python
# Push only US + UK active, actionable listings to Supabase
# Supabase = lightweight operational layer, not the full catalogue
# DE/FR/IT/ES go to BigQuery only — query direct from BQ when needed

from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# US: active FBA + FBM listings
us_active_df = pd.read_sql("""
    SELECT marketplace, seller_sku, asin, item_name, price, currency,
           quantity, fulfillment_channel, merchant_shipping_group, 
           status, last_changed_date
    FROM listings_master 
    WHERE status = 'ACTIVE'
    AND marketplace = 'US'
    AND (fulfillment_channel = 'AMAZON_NA' OR quantity > 0)
""", conn)

# UK: active FBM + SFP listings
uk_active_df = pd.read_sql("""
    SELECT marketplace, seller_sku, asin, item_name, price, currency,
           quantity, fulfillment_channel, merchant_shipping_group, 
           status, last_changed_date
    FROM listings_master 
    WHERE status = 'ACTIVE'
    AND marketplace = 'UK'
    AND quantity > 0
""", conn)

import pandas as pd
active_df = pd.concat([us_active_df, uk_active_df])

# Upsert in batches of 1000
for i in range(0, len(active_df), 1000):
    batch = active_df.iloc[i:i+1000].to_dict('records')
    supabase.table('active_listings').upsert(batch).execute()

print(f"US: {len(us_active_df):,} rows | UK: {len(uk_active_df):,} rows pushed to Supabase")
```

---

## 8. Handling Amazon's Dynamic Listing Changes

### 8.1 Types of Mid-Cycle Changes

| Change Type | Detection Method | Response |
|---|---|---|
| **New listing uploaded** | `change_type = 'NEW'` in delta | Auto-score in next biweekly cycle. If acceleration flag is present, escalate to Trend Ride queue immediately. |
| **Listing suppressed** | Appears in `GET_MERCHANTS_LISTINGS_FYP_REPORT` + disappears from Active Listings | Mark `status = 'SUPPRESSED'` in master. Do NOT restock suppressed FBA listings. Log suppression reason. |
| **IP takedown** | Listing removed from All Listings Report entirely | Mark `change_type = 'REMOVED'`. Flag for manual IP review. Do NOT auto-relist. Queue for legal/compliance review. |
| **Price change (by Amazon/competitor)** | `price` field hash mismatch | Log old vs new price. Recalculate margin. If margin drops below threshold, flag for Buy Box strategy review. |
| **Quantity zeroed (OOS)** | `quantity` drops to 0 | If FBA: Amazon ran out. Check restock recommendations. If FBM: You ran out. Check warehouse stock in Supabase. |
| **Category/browse node change** | `item_name` or browse fields change | Log for reference. Category median CVR may need recalculating if the item moved categories. |
| **Listing corrected by Amazon** | Fields change without seller action | Log all field changes. This often means Amazon applied a catalogue update or merged/split ASINs. |

### 8.2 Suppressed Listings Pipeline

```
EVERY BIWEEKLY CYCLE (Phase 1.5 — after data collection):

1. Request GET_MERCHANTS_LISTINGS_FYP_REPORT for each marketplace
   (this report CAN be scheduled — set up weekly auto-generation)

2. Load into suppressed_listings table (per-marketplace staging)

3. Cross-reference against listings_master:
   - If in master + in suppressed → mark SUPPRESSED
   - If was SUPPRESSED last cycle + NOT suppressed now → mark RESTORED
   - If new suppression → alert operator

4. Feed suppression reasons through Gemma 4 for:
   - Classification (missing image / missing attribute / policy violation / IP)
   - Suggested fix (specific attribute to add, image requirement, etc.)
   - Priority ranking (suppress + high sessions = high priority fix)

5. Output: suppression_action_list.csv with columns:
   marketplace | sku | asin | suppression_reason | suggested_fix | priority
```

### 8.3 IP & Compliance Flag Handling

```
DO NOT AUTOMATE IP RESPONSES. EVER.

When change_type = 'REMOVED' and the listing was previously ACTIVE:

1. Check if the ASIN still exists on Amazon (catalog API or manual search)
   - If ASIN exists but you're removed → likely IP complaint or policy takedown
   - If ASIN doesn't exist → Amazon removed the product entirely

2. Log to ip_flag_queue table with:
   - marketplace, sku, asin, last_known_status, removal_date
   - Linked to any recent Amazon emails (Health → Account Health Dashboard)

3. Gemma 4 can CLASSIFY the issue but CANNOT respond
   Feed it the Amazon notification text → get structured output:
   {
     "type": "ip_complaint" | "policy_violation" | "authenticity_challenge",
     "severity": "high" | "medium" | "low",
     "suggested_response_template": "...",
     "requires_legal_review": true/false
   }

4. Human reviews and acts. Period.
```

---

## 9. Biweekly SOP — Data Pipeline Steps (Phase 0)

This phase runs BEFORE Phase 1 (Data Collection) from the main PRD v1.0.

> **Scope:** Steps 0.1–0.11 apply to US + UK every cycle. DE is included in steps 0.3–0.8 when pulled (monthly/ad-hoc). FR/IT/ES are excluded from all automated steps.

### Phase 0 — Data Pipeline (45–60 minutes, US + UK only)

| Step | Action | Time | Marketplaces | Tool |
|---|---|---|---|---|
| **0.1** | Download All Listings Report. Name: `{MP}_ALL_LISTINGS_{YYYY-MM-DD}.txt` | 5–8 min | **US + UK** (DE monthly) | Seller Central × 2, or SP-API `createReport` |
| **0.2** | Download Suppressed Listings Report | 2–3 min | **US + UK** | Seller Central or SP-API `GET_MERCHANTS_LISTINGS_FYP_REPORT` |
| **0.3** | Validate file naming, headers, encoding, row counts. Reject any failure. | 3 min | **US + UK** | Python validation script |
| **0.4** | `TRUNCATE` each marketplace `raw_listings` table | 1 min | **US + UK** | MySQL |
| **0.5** | `LOAD DATA INFILE` both files in parallel | 6–10 min | **US + UK** | MySQL (2 parallel processes) |
| **0.6** | Compute `row_hash` for all raw rows | 3–5 min | **US + UK** | MySQL `UPDATE ... SET row_hash = SHA2(...)` |
| **0.7** | Run delta detection (NEW / UPDATED / UNCHANGED / REMOVED) | 5–8 min | **US + UK** | MySQL stored procedure or Python |
| **0.8** | Export delta to BigQuery + MERGE into `listings_master` | 5–8 min | **US + UK** | Python + `google-cloud-bigquery` |
| **0.9** | Upsert US (FBA/FBM) + UK (FBM/SFP) active listings to Supabase | 3–5 min | **US + UK only** | Python + Supabase client |
| **0.10** | Run US + UK suppressed listings through Gemma 4 (top 50 each by sessions) | 8–10 min | **US + UK** | Ollama / Gemma 4 26B-A4B |
| **0.11** | Generate pipeline report: rows loaded, delta counts, anomalies | 2 min | **US + UK** | Python summary script |

**Total Phase 0:** 43–60 minutes (runs Monday morning before the biweekly SOP Phase 1)

### Phase 0 (DE) — Ad-hoc / Monthly Pull

Run this only when you want to review DE performance or take listing action:

| Step | Action | Tool |
|---|---|---|
| **DE-1** | Download `DE_ALL_LISTINGS_{date}.txt` from sellercentral.amazon.de | Seller Central |
| **DE-2** | Validate + `LOAD DATA INFILE` into `amazon_de.raw_listings` | MySQL |
| **DE-3** | Run delta detection against `listings_master WHERE marketplace = 'DE'` | MySQL |
| **DE-4** | Export DE delta to BigQuery only (not Supabase) | Python |
| **DE-5** | Query BigQuery directly for DE performance review | BigQuery UI / OpenClaw |

> DE does not touch Supabase. All DE analysis runs via BigQuery SQL or OpenClaw.

### Phase 0 Output Files

| File | Contents | Destination |
|---|---|---|
| `pipeline_report_{cycle_id}.txt` | Row counts per marketplace (US + UK), delta summary, anomalies | Local + email to operator |
| `delta_export_{cycle_id}.csv` | All NEW + UPDATED + REMOVED rows (US + UK; DE if pulled) | BigQuery staging |
| `suppression_action_list_{cycle_id}.csv` | US + UK suppressed listings with Gemma 4 classifications | Supabase + operator review |
| `ip_flag_queue_{cycle_id}.csv` | Removed listings suspected IP/policy (US + UK) | Manual review queue |
| `uk_sfp_candidates_{cycle_id}.csv` | UK listings eligible for Nationwide Prime trial | Operator review → SFP enablement |

---

## 10. MySQL Local Setup Guide

### 10.1 Hardware Requirements

| Component | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB+ |
| Disk | 100 GB SSD | 250 GB NVMe |
| CPU | 4 cores | 8 cores |
| MySQL version | 8.0+ | 8.0.36+ |

### 10.2 MySQL Configuration for Bulk Loading

Add to `my.cnf` / `my.ini`:

```ini
[mysqld]
# Buffer pool — set to 50-70% of available RAM
innodb_buffer_pool_size = 8G

# Larger log file for bulk inserts
innodb_log_file_size = 1G

# Reduce disk flushes during bulk load
innodb_flush_log_at_trx_commit = 2

# Direct I/O to avoid double buffering
innodb_flush_method = O_DIRECT

# Allow large LOAD DATA INFILE
max_allowed_packet = 256M

# Allow local file loading
local_infile = ON

# Increase sort buffer for large JOINs during delta detection
sort_buffer_size = 4M
join_buffer_size = 4M
```

### 10.3 Load Script Template

```bash
#!/bin/bash
# load_marketplace.sh — Load one marketplace file into MySQL
# Usage: ./load_marketplace.sh US /path/to/US_ALL_LISTINGS_2026-04-15.txt
# Supports: US, UK (biweekly), DE (ad-hoc), FR/IT/ES (manual as needed)

MARKETPLACE=$1
FILE=$2
BATCH_DATE=$(date +%Y-%m-%d)
DB="amazon_$(echo $MARKETPLACE | tr '[:upper:]' '[:lower:]')"

echo "[$MARKETPLACE] Loading $FILE into $DB.raw_listings..."

mysql -u root $DB --local-infile=1 -e "
SET GLOBAL local_infile = 1;
SET foreign_key_checks = 0;
SET unique_checks = 0;
SET autocommit = 0;

TRUNCATE TABLE raw_listings;

LOAD DATA LOCAL INFILE '$FILE'
INTO TABLE raw_listings
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(seller_sku, @dummy, @dummy, item_name, @dummy, @dummy, @dummy, 
 listing_id, price, quantity, open_date, @dummy, @dummy, 
 @dummy, @dummy, image_url, item_condition, @dummy, @dummy, 
 asin, @dummy, @dummy, merchant_shipping_group, @dummy, 
 @dummy, fulfillment_channel, @dummy, @dummy, @dummy, @dummy)
SET load_batch_id = '$BATCH_DATE';

COMMIT;
SET unique_checks = 1;
SET foreign_key_checks = 1;
"

echo "[$MARKETPLACE] Computing row hashes..."
mysql -u root $DB -e "
UPDATE raw_listings 
SET row_hash = SHA2(
    CONCAT_WS('|', seller_sku, COALESCE(price,''), COALESCE(quantity,''),
    COALESCE(fulfillment_channel,''), COALESCE(merchant_shipping_group,''),
    COALESCE(item_condition,''), COALESCE(status,'')), 256
)
WHERE load_batch_id = '$BATCH_DATE';
"

ROW_COUNT=$(mysql -u root $DB -sN -e "SELECT COUNT(*) FROM raw_listings WHERE load_batch_id='$BATCH_DATE'")
echo "[$MARKETPLACE] Loaded $ROW_COUNT rows."
```

Biweekly run — US + UK in parallel:

```bash
#!/bin/bash
# load_core_marketplaces.sh — Biweekly. US + UK only.
DATE=$(date +%Y-%m-%d)
DIR="/data/amazon/downloads/$DATE"

./load_marketplace.sh US "$DIR/US_ALL_LISTINGS_$DATE.txt" &
./load_marketplace.sh UK "$DIR/UK_ALL_LISTINGS_$DATE.txt" &

wait
echo "Core marketplaces loaded. Running delta detection..."
python run_delta.py --marketplaces US UK --cycle "$(date +%Y-W%V)"
```

Ad-hoc DE pull (run manually when needed):

```bash
#!/bin/bash
# load_de_adhoc.sh — Manual, monthly or as needed
DATE=$(date +%Y-%m-%d)
DIR="/data/amazon/downloads/adhoc"

./load_marketplace.sh DE "$DIR/DE_ALL_LISTINGS_$DATE.txt"
echo "DE loaded. Exporting to BigQuery only (not Supabase)."
python run_delta.py --marketplaces DE --cycle "adhoc-$DATE" --no-supabase
```

---

## 11. Automation Roadmap

### Phase A — Manual (Now → Week 4)
**US + UK only. DE pulled manually if needed.**
- Download US + UK All Listings Reports manually from Seller Central (biweekly, Monday)
- Run `load_core_marketplaces.sh` manually
- Delta detection via SQL scripts
- Gemma 4 suppression classification via Ollama CLI
- UK SFP candidates reviewed manually in spreadsheet

### Phase B — Semi-Automated (Week 4 → Week 12)
**SP-API roles approved by Patrick. US + UK automated. DE structured but still manual.**
- Scheduled SP-API `createReport` calls for US + UK (biweekly cron, Sunday evening so reports are ready Monday)
- Auto-download via `getReportDocument` when report status = `DONE`
- Python pipeline orchestrates: download → validate → stage → delta → BigQuery → Supabase
- Gemma 4 integrated via Ollama API (no manual CLI step)
- UK SFP candidates pushed to Supabase `uk_sfp_candidates` table
- US FBA action queue populated in Supabase `us_fba_action_queue`
- DE: still manual pull via Seller Central, ad-hoc

### Phase C — Fully Automated (Week 12+)
**US + UK fully hands-off. DE escalated to monthly scheduled pull if DE revenue warrants it.**
- End-to-end pipeline runs automatically every other Sunday night (results ready Monday 9am)
- Anomaly alerts via Slack (using existing Slack connector in your stack)
- Dashboard in Supabase: pipeline health, delta metrics, suppression queue, US restock + UK SFP queues
- OpenClaw queries BigQuery for cross-marketplace analytics and surface DE insights on demand
- FR/IT/ES: remain ad-hoc — no scheduled pipeline unless revenue justifies escalation

---

## 12. Key Risk Mitigations

| Risk | Mitigation |
|---|---|
| **Wrong file loaded into wrong marketplace database** | File naming convention enforced by validation script. Currency spot-check on load. |
| **Amazon changes column schema** | Header validation step rejects files with unexpected columns. Alerts operator. |
| **Partial download (network timeout)** | Row count comparison to previous cycle. Flag >20% drop. |
| **MySQL disk space exhaustion** | Truncate raw tables after delta merge. Keep only current + previous cycle. Alert at 80% disk usage. |
| **BigQuery cost overrun** | Partition by marketplace. Cluster by SKU. Use delta-only uploads. Monitor query costs via BigQuery audit log. |
| **Supabase connection limits** | Batch upserts in groups of 1000. Use connection pooling. Only push active listings, not full catalogue. |
| **Gemma 4 hallucination on suppression reasons** | Always include the raw Amazon suppression text alongside Gemma's classification. Human reviews the pair. |
| **ASIN collision across marketplaces** | ASINs are globally unique, but the same ASIN can have different sellers, prices, and status per marketplace. Always include marketplace in every query predicate. |

---

## 13. Quick Reference — SP-API Report Types for This Pipeline

| Report | reportType | One Per Marketplace? | Schedulable? |
|---|---|---|---|
| All Listings | `GET_MERCHANT_LISTINGS_ALL_DATA` | Yes (only first marketplaceId used) | Request only |
| Active Listings | `GET_MERCHANT_LISTINGS_DATA` | Yes | Request only |
| Inactive Listings | `GET_MERCHANT_LISTINGS_INACTIVE_DATA` | Yes | Request only |
| Suppressed Listings | `GET_MERCHANTS_LISTINGS_FYP_REPORT` | Yes | Request or scheduled |
| Cancelled Listings | `GET_MERCHANT_CANCELLED_LISTINGS_DATA` | Yes | Request only |
| FBA Inventory Health | `GET_FBA_INVENTORY_PLANNING_DATA` | No (multi-marketplace) | Request only |
| FBA Restock | `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT` | No | Request only |
| Sales & Traffic | `GET_SALES_AND_TRAFFIC_REPORT` | No | Request only |

**SP-API Documentation:**
- Inventory Reports: https://developer-docs.amazon.com/sp-api/docs/report-type-values-inventory
- Analytics Reports: https://developer-docs.amazon.com/sp-api/docs/report-type-values-analytics
- Marketplace IDs: https://developer-docs.amazon.com/sp-api/docs/marketplace-ids
- Listings Items API: https://developer-docs.amazon.com/sp-api/docs/listings-items-api
- Report Request Flow: https://developer-docs.amazon.com/sp-api/docs/request-a-report

---

## Appendix A — Amazon Marketplace ID Quick Reference

```
── TIER 1 — Automated, biweekly pipeline ──
US  → ATVPDKIKX0DER      (sellingpartnerapi-na.amazon.com)   [FBA + FBM]
UK  → A1F83G8C2ARO7P      (sellingpartnerapi-eu.amazon.com)   [FBM + SFP]

── TIER 2 — Structured, ad-hoc pull ──
DE  → A1PA6795UKMFR9      (sellingpartnerapi-eu.amazon.com)   [FBM only]

── TIER 3 — Manual only, no automated pipeline ──
FR  → A13V1IB3VIYZZH      (sellingpartnerapi-eu.amazon.com)   [FBM only]
IT  → APJ6JRA9NG5V4       (sellingpartnerapi-eu.amazon.com)   [FBM only]
ES  → A1RKKUPIHCS9HS      (sellingpartnerapi-eu.amazon.com)   [FBM only]
```

## Appendix B — File Naming Convention

```
{MARKETPLACE}_{REPORT_TYPE}_{YYYY-MM-DD}.txt

Examples:
US_ALL_LISTINGS_2026-04-15.txt
UK_SUPPRESSED_2026-04-15.txt
DE_INACTIVE_2026-04-15.txt
FR_ALL_LISTINGS_2026-04-15.txt
IT_ALL_LISTINGS_2026-04-15.txt
ES_CANCELLED_2026-04-15.txt
```

## Appendix C — Delta Summary Report Template

```
=== PIPELINE REPORT — Cycle 2026-W16 ===
Date: 2026-04-15
Operator: [name]
Marketplaces processed: US (Tier 1) + UK (Tier 1)

LOAD SUMMARY:
  US: 823,412 rows loaded (prev: 819,887 → +0.4%)   [FBA + FBM]
  UK: 654,201 rows loaded (prev: 651,033 → +0.5%)   [FBM + SFP]
  DE: NOT PULLED THIS CYCLE (ad-hoc — last pulled 2026-04-01)
  TOTAL THIS CYCLE: 1,477,613 rows

DELTA SUMMARY (US + UK):
  NEW:          8,412 (0.57%)
  UPDATED:     41,803 (2.83%)
  UNCHANGED: 1,422,941 (96.30%)
  REMOVED:      4,457 (0.30%)
  
  → 54,672 rows exported to BigQuery (3.70% of total)
  → 1,394,886 active rows synced to Supabase (US + UK only)

ANOMALIES:
  ⚠ UK row count dropped 2.1% — within tolerance but monitor
  ⚠ 23 US listings have GBP-range prices — flagged for review
  ✓ No encoding issues detected
  ✓ All headers validated
  ✓ No US shipping templates found in UK file
  
SUPPRESSION REPORT (US + UK):
  New suppressions US: 143 | UK: 91
  Restored US: 34 | UK: 55
  Total suppressed: 1,847
  → Top 50 US + Top 50 UK classified by Gemma 4
    (see suppression_action_list_2026-W16.csv)

UK SFP CANDIDATES:
  Newly eligible: 28 listings (price ≥ £18 break-even, CVR ≥ median)
  → (see uk_sfp_candidates_2026-W16.csv)

IP/REMOVAL FLAGS (US + UK):
  Removed listings (suspected IP): 7 US | 5 UK
  → Queued for manual review (see ip_flag_queue_2026-W16.csv)
```

---

*This document is an addendum to the Amazon FBA/FBM Biweekly Optimisation System PRD v1.0. It should be read in conjunction with that document, which covers the scoring model, biweekly SOP phases 1–4, and the channel economics framework.*
