# Project Shape: Unified Listings Intelligence Dashboard & Bulk Operations

**Date:** 2026-04-11 | **Owner:** Ava | **Status:** SHAPING IN PROGRESS (Cem refining)

---

## Problem Statement (Comprehensive)

We have **five independent gap analyses** happening separately:

1. **Device Coverage Gaps** — Which designs are missing variants for top devices? (e.g., NARUTO on iPhone 17PM but missing iPhone 16)
2. **Cross-Region Gaps** — Which designs sell well in UK but aren't listed in US (or vice versa)?
3. **Shipping Template Gaps** — Which listings are on Standard instead of Reduced (US) or Prime (UK)? 
4. **Fulfillment Gaps** — FBA penetration low on certain designs/devices. FBM slow-ship items risk conversion loss.
5. **PRUNE Opportunities** — Old listings (9+ months, pre-2025-06-01) with zero sales in 2025. Waste to remove.

**Current state:** Each analysis is siloed. Cem can't see them together. Can't execute bulk fixes across multiple gap types. Can't prioritize which gap to fix first (revenue impact unclear).

**Impact:** $100K-500K/year in missed opportunities (device variants not created, regional gaps not filled, shipping templates not fixed, dead listings not pruned).

**The deeper insight you're raising:** We need a **unified Listings Intelligence Dashboard** that:
- Shows all five gap dimensions in one place
- Identifies **patterns** (which dimension has most impact?)
- Integrates with **sales data** (which gaps affect high-velocity designs?)
- Enables **bulk execution** (once identified, fix at scale via SP-API, SP-API, inventory module, etc.)

---

## Scope (Five Dimensions, Unified)

### Dimension 1: Device Coverage Gaps

**What it shows:**
- Which designs have incomplete device coverage?
- Example: NARUTO listed on iPhone 17PM, 17Pro, 17, but missing 16PM, 16Pro, 16
- Heatmap: design × device → green (listed) vs red (gap)
- Ranked by revenue opportunity: "Creating NARUTO-16PM would add $5K/month"

**Data sources:** Active Listings Report + SKU Parsing Rules + Sales velocity (BQ)

**Action:** "Create these missing variants" (outputs to PULSE backlog)

---

### Dimension 2: Cross-Region Gaps

**What it shows:**
- Which designs sell well in one region but aren't listed in another?
- Example: NARUTO sells $50K/month in UK. Not listed in US. Opportunity: +$80K/month if listed in US (extrapolation based on device cross-sell patterns)
- Matrix: design × region → listed/not listed
- Ranked by sales velocity in source region

**Data sources:** Active Listings Report (by region) + BQ orders (by buyer_country)

**Action:** "List these designs in [region]" (outputs SKU staging backlog)

---

### Dimension 3: Shipping Template Gaps

**What it shows:**
- Which listings are on Standard shipping instead of Reduced (US) / Prime (UK)?
- Patterns: by upload date, device, design, inventory status, FBA/FBM
- Heatmap: device × design → compliance %
- Breakdown: "87% of iPhone 16 from Jan 20 on Standard. Only 3% of iPhone 17PM missing."

**Data sources:** Active Listings Report + Inventory module (Harry)

**Action:** "Convert these X listings to Reduced/Prime" (queues SP-API batch update)

---

### Dimension 4: Fulfillment Gaps

**What it shows:**
- Which designs have low FBA penetration? (Should be FBA for faster shipping + higher conversion)
- Which FBM items can't actually ship in 2 days? (Listed as Reduced but can't deliver)
- Breakdown: design × fulfillment type → FBA %, conversion impact
- Opportunity: "Moving NARUTO to FBA would increase conversion +2% on 50K SKUs = $50K/month lift"

**Data sources:** Active Listings Report + Inventory module (Harry) + Conversion Dashboard (sales data)

**Action:** "Migrate these designs to FBA" (outputs to operations backlog)

---

### Dimension 5: PRUNE Opportunities

**What it shows:**
- Old listings (open_date before 2025-06-01, >9 months old) with zero sales in 2025
- Grouped by: design, license, product type, device
- Cost: "These 50K expired NFL listings cost $3K/month in marketplace fees. Revenue: $0."
- Patterns: "Entire design-license combos with zero sales. Kill them."

**Data sources:** Active Listings Report + BQ orders (by sku, 2025 only)

**Action:** "Suppress these X listings" (removes marketplace clutter + saves fees)

---

## Architecture: Unified Data Model

### Core Tables (SQLite)

```sql
-- Active listings with all dimensions
CREATE TABLE listings_full (
  sku TEXT PRIMARY KEY,
  asin TEXT,
  design TEXT,
  device TEXT,
  product_type TEXT,
  region TEXT,  -- US, UK, DE
  upload_date DATE,
  listing_status TEXT,  -- ACTIVE, SUPPRESSED, etc.
  price REAL,
  quantity INTEGER,
  
  -- Dimension 1: Device Coverage
  design_available_devices TEXT,  -- "IPH17PM,IPH17PRO,IPH17" (what's listed)
  device_gap_flag BOOLEAN,        -- is this design missing this device elsewhere?
  
  -- Dimension 2: Cross-Region
  design_in_other_regions TEXT,   -- "UK,DE" (where else this design lives)
  cross_region_gap_flag BOOLEAN,  -- is this design missing from this region?
  
  -- Dimension 3: Shipping Template
  shipping_template TEXT,         -- STANDARD, REDUCED, PRIME
  target_shipping_template TEXT,  -- what it SHOULD be
  shipping_gap_flag BOOLEAN,
  
  -- Dimension 4: Fulfillment
  fulfillment_type TEXT,          -- FBA, FBM
  can_ship_2day BOOLEAN,
  fba_penetration_by_design REAL, -- % of this design in FBA
  
  -- Dimension 5: PRUNE
  days_since_sale INTEGER,        -- 0 if sold in 2025, else days since last sale
  prune_flag BOOLEAN,             -- old + no sales?
  
  -- Metadata
  sales_last_90d INTEGER,
  revenue_last_90d REAL,
  created_at TIMESTAMP
);

-- Gap summary (for dashboard)
CREATE TABLE gap_summary (
  date DATE,
  dimension TEXT,  -- "device_coverage", "cross_region", "shipping", "fulfillment", "prune"
  dimension_value TEXT,  -- "NARUTO", "US", etc.
  total_items INTEGER,
  gap_items INTEGER,
  gap_pct REAL,
  revenue_opportunity REAL,
  priority TEXT  -- HIGH, MEDIUM, LOW (based on impact)
);

-- Execution queue (for bulk fixes)
CREATE TABLE execution_queue (
  action_id TEXT PRIMARY KEY,
  action_type TEXT,  -- "CREATE_VARIANT", "LIST_REGION", "UPDATE_SHIPPING", "MIGRATE_FBA", "SUPPRESS"
  sku TEXT,
  design TEXT,
  target_value TEXT,  -- new device, new region, new template, FBA, etc.
  priority TEXT,
  queued_at TIMESTAMP,
  status TEXT,  -- QUEUED, EXECUTING, SUCCESS, FAILED
  result TEXT
);
```

---

## Dashboard: Five Unified Views

### View 1: Executive Summary (Top of Page)

**Scorecard showing all 5 dimensions:**

```
┌────────────────────────────────────────────────────────────┐
│  📊 LISTINGS INTELLIGENCE SUMMARY                          │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣  Device Coverage Gaps                                 │
│      120 designs missing variants on top devices           │
│      Revenue opportunity: $150K-200K/month                 │
│      Top gap: NARUTO missing iPhone 16 (5 variants)       │
│      [Action: Create variants]                             │
│                                                             │
│  2️⃣  Cross-Region Gaps                                    │
│      45 designs selling well in UK but not US              │
│      Revenue opportunity: $80K-100K/month                  │
│      Top gap: NARUTO in UK ($50K/mo), not in US           │
│      [Action: List in US]                                  │
│                                                             │
│  3️⃣  Shipping Template Gaps                               │
│      502K listings on Standard (should be Reduced/Prime)   │
│      Revenue opportunity: $37.5K/month                     │
│      Compliance: 85% (target 100%)                         │
│      [Action: Convert to Reduced/Prime]                    │
│                                                             │
│  4️⃣  Fulfillment Gaps                                     │
│      FBA penetration: 42% (target 60% for top designs)     │
│      Revenue opportunity: $50K-75K/month                   │
│      Top gap: NARUTO 15% FBA, 85% FBM (slow)              │
│      [Action: Migrate to FBA]                              │
│                                                             │
│  5️⃣  PRUNE Opportunities                                  │
│      50K expired NFL listings (zero 2025 sales)            │
│      Annual fee waste: $36K                                │
│      [Action: Suppress dead listings]                      │
│                                                             │
│  TOTAL OPPORTUNITY: $350K-500K/year                        │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

### View 2: Gap Explorer (Drill-Down by Dimension)

**User selects dimension, sees ranked list:**

```
DIMENSION: Device Coverage Gaps
SORTED BY: Revenue Opportunity (descending)

Design        | Missing Devices | Revenue Op | Priority | Action
──────────────────────────────────────────────────────────────────
NARUTO        | 5 devices       | $12K/mo    | HIGH     | [Create]
ONE PIECE     | 3 devices       | $8K/mo     | HIGH     | [Create]
PEANUTS       | 2 devices       | $4K/mo     | MEDIUM   | [Create]
HARRY POTTER  | 1 device        | $2K/mo     | LOW      | [Create]
```

---

### View 3: Pattern Heatmaps (Visual Analysis)

**Device × Design heatmap (Shipping Templates):**
```
Design       | IPH17PM | IPH17Pro | IPH17 | IPH16PM | IPH16Pro | IPH16
─────────────────────────────────────────────────────────────────────
NARUTO       | 95% ✅  | 94% ✅   | 60%❌ | 85% ✅  | 85% ✅   | 40%❌
ONE PIECE    | 92% ✅  | 92% ✅   | 58%❌ | 82% ✅  | 82% ✅   | 38%❌
PEANUTS      | 98% ✅  | 98% ✅   | 95% ✅| 95% ✅  | 95% ✅   | 92% ✅
```

**Insight:** iPhone 17 and iPhone 16 consistently have lower compliance. Script issue with older devices?

---

### View 4: Impact Dashboard (Sales × Gaps)

**Which gaps matter most (revenue impact)?**

```
Dimension          | Gap Count | Affected Sales | Monthly Impact | Priority
──────────────────────────────────────────────────────────────────────────
Shipping Template  | 502K SKUs | $1.2M revenue  | $37.5K loss    | 🔴 CRITICAL
FBA Penetration    | 150K SKUs | $800K revenue  | $50K-75K loss  | 🔴 CRITICAL
Device Coverage    | 500 gaps  | $600K revenue  | $150K-200K opp | 🔴 CRITICAL
Cross-Region       | 45 designs| $500K revenue  | $80K-100K opp  | 🟠 HIGH
PRUNE              | 50K SKUs  | $0 revenue     | $3K/mo fees    | 🟡 MEDIUM
```

---

### View 5: Execution Pipeline (What's Queued?)

**Once you identify gaps, queue bulk fixes:**

```
Action Type         | Queued | In Progress | Success | Failed | Est. Revenue
────────────────────────────────────────────────────────────────────────────
Create Variants     | 0      | 0           | 0       | 0      | $150K-200K/mo
List in Region      | 0      | 0           | 0       | 0      | $80K-100K/mo
Update Shipping     | 0      | 0           | 0       | 0      | $37.5K/mo
Migrate to FBA      | 0      | 0           | 0       | 0      | $50K-75K/mo
Suppress Dead List  | 0      | 0           | 0       | 0      | $36K/year
```

---

## Implementation: Three Stages (Unified)

### Stage 1: Unified Listings BI Tool (Apr 15-May 5)

**Build:**
- SQLite schema (listings_full table with all 5 dimensions)
- Data pipeline: Load Active Listings + BQ orders + Inventory (when ready)
- Dashboard: Views 1-4 (summary, explorer, heatmaps, impact)
- Pattern detection: Upload date, device, design, region, FBA/FBM

**Timeline:** 2-3 weeks

**Output:** Read-only visibility into all 5 gap dimensions

---

### Stage 2: Execution Engine (May 5-25)

**Build:**
- View 5: Execution Pipeline
- Queue system: Users mark gaps for action
- Codex cron for automated fixes:
  - **Device gaps:** Output to PULSE backlog (design/product team creates variants)
  - **Cross-region gaps:** Output to SKU staging backlog (listings team uploads to new region)
  - **Shipping gaps:** Call Amazon SP-API to update templates
  - **FBA gaps:** Inventory module (Harry) handles FBA migration
  - **PRUNE:** Call Amazon SP-API to suppress listings

**Timeline:** 2 weeks

**Output:** Bulk execution across all 5 gap types

---

### Stage 3: Automation & Intelligence (May 25+)

**Enhancements:**
- Auto-prioritize (revenue impact weighting)
- Predictive recommendations ("We recommend fixing shipping first, then FBA")
- Weekly automated report to Cem ("This week: 187 shipping fixes, 45 variants created, 1K dead listings pruned")
- Slack alerts for emerging gaps

**Timeline:** Ongoing

---

## Data Dependencies

### Hard Blockers: None
Stage 1 works with Active Listings Report + BQ orders. Both available now.

### Soft Blockers (Enhance Later Stages)

1. **Inventory Module (Harry)** — Needed for:
   - FBA penetration analysis (dimension 4)
   - Shipping template rules (dimension 3: can ship 2-day?)
   - FBA migration execution (dimension 4)
   
   **Fallback:** Use SKU naming convention (F prefix = FBA) as proxy

2. **PULSE Backlog Integration** — Needed for:
   - Device coverage action: "Create NARUTO-16PM variant"
   - Outputs to PULSE task queue
   
   **Fallback:** Manual output (CSV export, Cem reviews)

3. **SKU Staging Integration** — Needed for:
   - Cross-region action: "List NARUTO in US"
   - Outputs to SKU staging backlog
   
   **Fallback:** Manual output

---

## Edge Cases (Per Dimension)

### Device Coverage
- **Don't create variants for designs nearing EOL** (license expiring soon)
- **Prioritize top 50 devices** (tail devices not worth the effort)
- **Check inventory before creating** (don't create variants we can't fulfill)

### Cross-Region
- **Respect regional licensing** (some designs not licensed in all regions)
- **Account for regulatory differences** (device certifications vary)
- **Check shipping rules** (some devices can't ship to certain regions)

### Shipping Template
- **Don't convert out-of-stock items** (can't deliver 2-day if no inventory)
- **Respect FBM capability** (FBM can only be Reduced if seller can ship 2-day)
- **Batch by region** (US = Reduced, UK = Prime, different rules)

### Fulfillment
- **Don't force FBA for low-volume designs** (not economical)
- **Account for size/weight** (some items too large/heavy for FBA)
- **Respect seller preference** (some designs intentionally FBM)

### PRUNE
- **Don't suppress recent failures** (give new listings 90 days to sell)
- **Check license status** (expired licenses = safe to prune, active = investigate why no sales)
- **Respect strategic inventory** (some SKUs kept for assortment even if low-sales)

---

## Success Metrics

| Dimension | Current | Target | Timeline | Impact |
|-----------|---------|--------|----------|--------|
| **Device Coverage** | 500 gaps | 50 gaps | 6 weeks | +$150-200K/mo |
| **Cross-Region** | 45 gaps | 5 gaps | 8 weeks | +$80-100K/mo |
| **Shipping Template** | 85% compliance | 100% | 4 weeks | +$37.5K/mo |
| **FBA Penetration** | 42% | 60% (top designs) | 6 weeks | +$50-75K/mo |
| **PRUNE** | 50K dead SKUs | <5K | 2 weeks | $36K/year savings |
| **Dashboard Adoption** | None | Weekly review | Week 1 | Decision velocity |

**Total Impact:** $300-450K/year in new revenue + $36K/year in fee savings

---

## Shaping Sign-Off (Pending)

- [ ] Cem reviewed unified five-dimension architecture
- [ ] Cem approved Stage 1 scope (unified BI tool with all 5 dimensions)
- [ ] Cem approved execution capability (bulk fixes across all 5 types)
- [ ] Cem approved timeline (Stage 1 by May 5, Stage 2 by May 25)
- [ ] Cem approved data dependencies (inventory module soft blocker, not hard)
- [ ] **Ready to move to planning?**

---

**Status:** SHAPING IN PROGRESS (awaiting Cem approval) | **Next:** PLANNING phase once approved

