# SOP: Weekly Amazon Reports Processing
*Owner: Ava | Created: 2026-04-04 | Status: Active*

---

## Overview
Every week, Amazon reports are downloaded and processed to maintain data freshness, audit the listings team, and generate intelligence for decision-making.

---

## Schedule
**Every Saturday morning (EST)**

---

## Step 1 — Download Reports from Seller Central

### Reports to download (all marketplaces)
| Report | Marketplace | Format | Approx Size |
|---|---|---|---|
| Active Listings Report | US | .txt (TSV) | ~6-7GB |
| Active Listings Report | UK | .txt (TSV) | ~9-10GB |
| Active Listings Report | DE | .txt (TSV) | ~4-5GB |
| Business Report (14-day) | US | .csv | ~7-8MB |
| Business Report (30-day) | US | .csv | ~7-8MB |
| Business Report (14-day) | UK | .csv | ~6-7MB |
| Business Report (30-day) | UK | .csv | ~7-8MB |
| Business Report (14-day) | DE | .csv | ~6MB |
| Business Report (30-day) | DE | .csv | ~9MB |
| Child ASIN Report (14-day) | US | .csv | varies |
| Child ASIN Report (30-day) | US | .csv | varies |

**Download destination:** `~/Downloads/`

**Storage rule:** Active Listings files are large — delete immediately after delta load. Business Reports are small — keep for 30 days then archive.

---

## Step 2 — Load Active Listings Delta

Run for each Active Listings file in order (US first, then UK, then DE):

```bash
python3 /Users/openclaw/.openclaw/workspace/scripts/refresh_listings.py \
  ~/Downloads/<filename>.txt --delete-after
```

**What this does:**
- Rotates current → previous
- Loads new file into `listings_current`
- Computes delta (new/removed/changed)
- Saves top 1000 new listings to `data/deltas/new_YYYY-MM-DD.json`
- **Deletes the raw file automatically**
- Logs run to `delta_log` table

**Note:** UK and DE tables are separate (`listings_uk_current`). Script needs to be run with region flag when UK/DE support is added.

---

## Step 3 — Run Weekly Intelligence Analysis

Dispatch to three agents simultaneously:

| Agent | Model | Output file |
|---|---|---|
| Prism | Gemma 4 26B (local) | `results/weekly_analysis_prism_YYYY-MM-DD.md` |
| Atlas | GPT-5.4 Codex | `results/weekly_analysis_atlas_YYYY-MM-DD.md` |
| Hermes | Kimi K2.5 | `results/weekly_analysis_hermes_YYYY-MM-DD.md` |

**Standard deliverables per agent:**
1. Delta summary (new/removed/changed vs last week)
2. Product type breakdown (canonical types, FBA+FBM combined)
3. Top 20 new listings
4. Price changes (>$2 movement)
5. FBA vs FBM split by product type
6. Device coverage gaps (HTPCR listed, HB401 missing)
7. UK vs US catalog comparison

**SKU parsing rules:** `wiki/SKU_PARSING_RULES.md` — mandatory reference for all analysis.

---

## Step 4 — Listings Team Audit

**Purpose:** Verify that what the PH listings team reports as listed is actually live on Amazon.

### Process
1. Pull this week's EOD reports from Slack `#eod-listings`
2. Extract SKUs the team claims to have listed this week
3. Query `listings_current` to verify each SKU exists:
   ```sql
   SELECT seller_sku, asin, open_date, fulfillment_channel
   FROM listings_current
   WHERE seller_sku IN (<team_reported_skus>)
   ```
4. Flag discrepancies:
   - **Missing:** Team reported listed but not found in Active Listings
   - **Wrong date:** Listed much earlier than team claims
   - **Wrong type:** Wrong fulfillment channel

### Output
Save to: `results/listings_audit_YYYY-MM-DD.md`

Include:
- Total SKUs team claimed listed
- Verified live count + %
- Missing/discrepancy list
- Pattern analysis (are specific team members or product types problematic?)

---

## Step 5 — Shipping Templates Review

**Purpose:** Ensure carrier rules, shipping templates, and rate configurations are current.

### Weekly checks
1. Review `wiki/04-shipping/SHIPPING_CARRIER_RULES.md` — any outdated rules?
2. Check Veeqo for any new carrier rate changes or service updates
3. Verify Amazon shipping templates match current carrier configurations
4. Check for any carrier surcharge updates (dimensional weight, fuel surcharges)
5. Flag any routes that have delivery time violations (Amazon SLA: 24hr)

### Output
Save to: `results/shipping_review_YYYY-MM-DD.md`

Flag: any changes needed → create task in TASKS.md

---

## Step 6 — Consolidate + Report to Cem

Ava consolidates all agent outputs into a single executive summary:

```
results/weekly_summary_YYYY-MM-DD.md
```

Includes:
- Key metrics (new listings, removed, changed)
- Top opportunities identified
- Listings team audit result
- Any shipping flags
- Recommended actions for coming week

Post summary to Slack `#eod-listings` and send to Cem via Telegram.

---

## Future: Google Cloud Run Amazon Reports API
- Amazon Reports API running on Cloud Run (confirmed 2026-04-04)
- **Planned:** Replace manual downloads with automated API pulls
- **When ready:** Steps 1 and 2 become fully automated via cron
- **Test needed:** Validate API output matches manual download format
- Cron will trigger Sat 6 AM EST once tested and confirmed

---

## SKU Parsing Reference (quick)
```
{PRODUCT_TYPE}-{DEVICE_CODE}-{DESIGN_CODE}-{VARIANT}
FBA prefix: F on product type = FBA (FHTPCR = FBA HTPCR)
F exceptions (NOT FBA): FLAG, F1309, FRND, FKFLOR
Always combine FBA+FBM for analytics
Full rules: wiki/SKU_PARSING_RULES.md
```

---

## Cron Schedule (target)
| Task | Schedule | Agent | Status |
|---|---|---|---|
| Download Active Listings (US/UK/DE) | Sat 6 AM EST | Pixel | ⏳ Pending Cloud Run test |
| Delta load + delete | Sat 6:30 AM EST | Pixel | ⏳ Pending download automation |
| Weekly intelligence analysis | Sat 7 AM EST | Prism + Atlas + Hermes | ⏳ To be wired |
| Listings team audit | Sat 7:30 AM EST | Pixel | ⏳ To be built |
| Shipping templates review | Sat 8 AM EST | Bolt | ⏳ To be built |
| Consolidated report to Cem | Sat 9 AM EST | Ava (main) | ⏳ To be wired |
