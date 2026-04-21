# SOP: Weekly Listings Intelligence Report
**Owner:** Ava | **Version:** 1.0 | **Date:** 2026-04-05
**Cadence:** Every Saturday night after Active Listings download

---

## Purpose
Measure week-over-week listing activity by marketplace and product type, using SKU parsing rules as the analytical lens. This is the listings equivalent of PULSE — not sales velocity, but catalog health.

---

## Known Issue (Apr 5 — fixed in v1)
Previous reports showed zero delta because `listings_current` and `listings_previous` in SQLite were overwritten with the same file. **Fix: always copy current → previous BEFORE loading new file.** The delta_log table captures correct numbers regardless — use that as ground truth.

---

## Data Sources

| Source | What it contains | Refresh |
|--------|-----------------|---------|
| `data/local_listings.db` → `listings_current` | US Active Listings (current week snapshot) | Weekly manual download |
| `data/local_listings.db` → `listings_previous` | US Active Listings (prior week snapshot) | Auto-rotated on each load |
| `data/local_listings.db` → `listings_uk_current` | UK Active Listings (current snapshot) | Weekly manual download |
| `data/local_listings.db` → `listings_uk_previous` | UK Active Listings (prior snapshot) | Auto-rotated on each load |
| `data/local_listings.db` → `delta_log` | Load history with accurate new/removed/changed counts | Written on each load |

**Key rule:** `open_date` in listings = creation date. Use `open_date >= [last Saturday]` as a proxy for new listings when snapshot delta is unavailable.

---

## Weekly Process

### Step 1: Download Active Listings (manual, ~5 min)
1. Log into Amazon Seller Central (US + UK)
2. Reports → Inventory → Active Listings Report
3. Download both US and UK files
4. Save as: `US Active+Listings+Report_MM-DD-YYYY.txt` and `UK Active+Listings+Report_MM-DD-YYYY.txt`
5. Do NOT rename or modify

### Step 2: Load into SQLite (automated script)
```bash
python3 scripts/refresh_listings.py --us "US Active+Listings+Report_MM-DD-YYYY.txt" --uk "UK Active+Listings+Report_MM-DD-YYYY.txt"
```
Script must:
- Copy `listings_current` → `listings_previous` BEFORE loading new data
- Copy `listings_uk_current` → `listings_uk_previous` BEFORE loading new data
- Load new file into `_current` tables
- Write delta to `delta_log`
- Delete source files after load (`--delete-after` flag)

### Step 3: Run weekly report
```bash
python3 scripts/weekly_listings_report.py --week "2026-04-05"
```
Outputs to `results/weekly_listings_YYYY-MM-DD.md`

### Step 4: Post to Slack
Post sanitised summary (no revenue figures) to `#eod-listings`

---

## Report Format (Agreed Template)

```markdown
# Weekly Listings Report — [Marketplace] — Week of [DATE]

## Executive Summary
- Total active listings: [US: X | UK: Y]
- Net change this week: [US: +X | UK: +Y]
- New SKUs added: [X]
- SKUs removed: [X]
- Price changes: [X]

## 1. Weekly Delta by Marketplace

| Marketplace | Prev Total | Current Total | New | Removed | Net |
|------------|-----------|--------------|-----|---------|-----|
| US         | X,XXX,XXX | X,XXX,XXX    | +XX,XXX | -XX,XXX | +XX,XXX |
| UK         | X,XXX,XXX | X,XXX,XXX    | +XX,XXX | -XX,XXX | +XX,XXX |

## 2. New Listings This Week — by Product Type (US)

| Type (Canonical) | New SKUs | % of New | Notes |
|-----------------|---------|----------|-------|
| HB1BK           | 164,656 | 86.1%    | New Android hard bumper rollout |
| HB401           | 13,427  | 7.0%     | Ongoing |
| HTPCR           | 5,959   | 3.1%     | Ongoing |

## 3. New Listings This Week — by Product Type (UK)

[Same table for UK]

## 4. Catalog Totals — US vs UK

| Type     | US Total   | US%   | UK Total   | UK%   | Gap Flag |
|----------|-----------|-------|-----------|-------|----------|
| HTPCR    | 1,294,099 | 35.8% | 1,945,138 | 37.0% |          |
| HLBWH    | 1,250,454 | 34.6% | 2,142,180 | 40.7% | UK>US    |
| HC       | 680,661   | 18.8% | 782,178   | 14.9% |          |
| HB401    | 96,593    | 2.7%  | 92,066    | 1.8%  |          |

## 5. FBA Penetration

| Type     | US FBA  | US FBM      | FBA%  | Priority |
|----------|---------|-------------|-------|----------|
| HTPCR    | 4,248   | 1,289,851   | 0.3%  | 🔴 LOW   |
| HB401    | 123     | 96,470      | 0.1%  | 🔴 LOW   |
| HDMWH    | 496     | 1,963       | 20%   | 🟢       |

## 6. Top 10 New Design Codes This Week

[Ranked by SKU count, with brand/license identified]

## 7. Flags & Actions

- [Flag any anomalies — e.g. >10K new of a single type in one day]
- [Flag new product types appearing for the first time]
- [Flag if UK-only or US-only designs > threshold]
```

---

## Parsing Rules Applied in Report

All analysis uses canonical SKU parsing per `wiki/SKU_PARSING_RULES.md`:

1. **Canonical product type** = strip `F` prefix (except FLAG, F1309, FRND, FKFLOR)
2. **Design code** = position [2] of seller_sku split by `-`
3. **Device code** = position [1]
4. **FBA flag** = `fulfillment_channel = 'AMAZON_NA'` OR product_type starts with `F` (excluding exceptions)
5. **New this week** = `open_date >= last Saturday` (most reliable) OR snapshot delta
6. **Region** = US from `listings_current`, UK from `listings_uk_current`

---

## What This Report Is NOT

- **Not sales data** — listing count ≠ sales volume. Use PULSE for sales velocity.
- **Not conversion data** — use Sales & Traffic report for CVR.
- **Not inventory** — use Supabase `blank_inventory` for stock levels.

The listings report answers: *"What did the team create/list this week, and is the catalog healthy?"*

---

## Automation Plan (Phase 2)
Once middleware BQ loader is fixed:
- Weekly Active Listings pull automated via Cloud Run cron (Sat 11 PM)
- Delta computed server-side, pushed to Supabase
- Report auto-generated by Pixel agent (Gemini Flash)
- No manual download required

Until then: manual download → run script → post to Slack.

---
*SOP v1.0 agreed: 2026-04-05 | Next review: 2026-05-05*
