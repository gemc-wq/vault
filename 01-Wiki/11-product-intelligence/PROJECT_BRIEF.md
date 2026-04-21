# Product Intelligence Engine — Project Brief
**Project Code:** PIE  
**Owner:** Harry (COO) — multi-model orchestration  
**Sponsor:** Cem (CEO)  
**Strategic Lead:** Ava (CPSO)  
**Created:** 2026-03-07  
**Priority:** P0 — Sales Driver & SKU Management  

---

## 1. Problem Statement

Ecell Global has **1.89M SKUs** in BigCommerce but needs to select **~200K** for the GoHeadCase Shopify storefront (which feeds Target+, Walmart, and DTC microsites). Currently there is no algorithmic method to determine which SKUs maximize revenue coverage while minimizing catalog bloat. The existing approach is manual and doesn't account for design-level performance, device family coverage, regional splits, or new license injection.

## 2. Vision

> "Essentially an LLM ecosystem trained on data" — Cem

A **multi-model product intelligence engine** that algorithmically scores and selects SKUs using design-level revenue ranking, device family coverage rules, and regional demand signals. Not a static matrix — a living system that reasons about what to sell, where, and why.

## 3. Core Concepts

### Design-First Approach
- **"We sell collections"** — a design is the parent asset
- SKUs = design × device × product type
- Rank best-selling DESIGNS first, then replicate across devices and product types (blanket coverage)
- Parent/child design hierarchy matters (e.g., a brand has multiple designs)

### Collection Completeness
Each selected design should be available across core product types:
- **HTPCR** (snap case) — £8.04M, 132K orders, #1 product type
- **HLBWH** (wallet case) — £7.28M, 60K orders, #2 (note: L prefix variant exists)
- **HC** (hard case) — £2.23M, 53K orders, #3
- **HB401** (soft gel case) — significant volume
- Additional types: H8939, HDMWH (desk mats), HHYBK, HA805, HB6CR

### Device Family Coverage
- If iPhone 16 is selected → must include 16/Plus/Pro/Pro Max
- Family-based selection, not individual device cherry-picking
- **704 unique devices** in catalog globally

### Regional Device Splits (CRITICAL NUANCE)
- **US**: iPhone-heavy, iPads significant, desk mats (#11 at $62K!), Samsung S938U matters
- **UK**: Samsung A16 5G in top 10 (#8 at £98K — surprise finding), older iPhones persist (iPhone 13 = #1), console skins strong
- Device strategy MUST vary by marketplace/region

## 4. Data Sources

### Available Now
| Source | Records | Location | Status |
|--------|---------|----------|--------|
| Orders (Jan 2025–Feb 2026) | 304K | Supabase `orders` table | ✅ Active |
| Inventory | 9.8K | Supabase `inventory` table | ✅ Active |
| Walmart Listings | 95,640 | Supabase (partial — 10K of 95K loaded) | ⚠️ Pagination fix needed |
| Amazon Active Listings | 3.44M SKUs | CSV (6.8GB file) | ✅ Analyzed, not in DB |
| Target+ Items | 30,312 | Partner Portal (need export) | ⚠️ Pending Cem export |
| BigCommerce Catalog | 1.89M | BigCommerce API | 🔴 Not yet connected |

### Needed
| Source | Purpose | Status |
|--------|---------|--------|
| GA4 Session Data | Behavioral model (sessions, bounce, conversion by product) | 🔴 Not connected |
| Design-level revenue grouping | Group SKUs by design_code, rank within brands | 🔴 Query not yet run |
| Feedonomics mapping rules | Reverse-engineer BC→Target+ attribute transforms | 🔴 Need both exports to compare |

## 5. Key Analysis Results (from 304K order analysis)

### Revenue Distribution
- **$18.9M** total revenue across 704 unique devices
- **Top 50 devices = 86.5%** of revenue (global)
- **Top 100 = 95.4%**, Top 150 = 98.4%
- Elbow analysis confirms a Pareto-heavy distribution

### Top Devices by Region
**US (128K orders, $2.8M):**
- iPhone 16 #1, flatter curve (more device diversity)
- Desk mats (600x300) = #11 ($62K!) — missed in initial matrix
- Samsung S938U #16

**UK (99K orders, $1.96M):**
- iPhone 13 #1 (older phones persist longer)
- Samsung A165G #8 (£98K — must include)
- Console skins: DS5CT #22, DS5EGCT significant

### Product Type Revenue
1. HTPCR (snap case): £8.04M, 132K orders
2. HLBWH (wallet): £7.28M, 60K orders
3. HC (hard case): £2.23M, 53K orders

## 6. Architecture

### Multi-Model Approach (Cem's directive)
| Model | Role | Cost |
|-------|------|------|
| Gemini 3.1 Pro | Data analysis backbone (fast, cheap, good at numbers) | FREE (OAuth) |
| GPT-5.4 Codex | Behavioral/probabilistic analysis | FREE (ChatGPT Team) |
| Claude Opus 4.6 | Strategic synthesis, final recommendations | API (use sparingly) |

### Model Benchmark Results (Mar 6)
- **Gemini 3.1 Flash Lite**: 5.6s, 4K chars ✅ — fast, proposed WOS formula
- **Gemini 3.1 Pro**: 40s, 3.8K chars ✅ — deeper reasoning (surfaced "iPhone 7 = kids" insight)
- **Sonnet 4.6**: timed out (120s) ❌
- **Opus**: timed out (180s) ❌
- **Decision: Gemini for data analysis, Anthropic for strategic synthesis**

### Sub-Agents Created
- **Atlas** (Gemini 3.1 Pro) — data-first analyst, workspace: `~/.openclaw/workspaces/atlas/`
- **Prism** (GPT-5.4 Codex) — behavioral/probabilistic analyst, workspace: `~/.openclaw/workspaces/prism/`
- **Ensemble approach**: both analyze same data, Ava reconciles disagreements

### Scoring Engine Components
1. **Design-Level Revenue Ranking** — group by design_code within brands, rank by revenue
2. **Device Family Completeness** — ensure full family coverage per selected device
3. **Regional Split Optimizer** — different device mixes for US vs UK vs global
4. **Collection Completeness Checker** — verify each design × product type matrix
5. **New License Injector** — score unproven licenses against comparable brand velocity
6. **What-If Simulator** — SKU count vs revenue coverage trade-off curves

## 7. Target Output

### Product Matrix v1 (already drafted)
- 9 product types × 30 devices × 3 brand tiers (A/B/C)
- Tier A: Top 20 brands → all designs
- Tier B: Next 30 brands → top 10 designs each
- Tier C: Long tail → top 5 designs each
- **Estimated: ~201K SKUs**

### Pipeline
```
BigCommerce (1.89M) → PIE Scoring → Selected ~200K → Supabase → Shopify Import
                                                          ↓
                                              Target+ (via Marketplace Connect)
                                              Walmart (direct feed)
                                              DTC Microsites (themed stores)
```

## 8. Channel-Specific Rules

### Target+ License Restrictions (HARD RULE)
- ❌ **NO US Sports**: NFL, NBA, NHL, NCAA/Collegiate, MLS
- ✅ UK/EU football clubs fine on Target+
- ✅ US Sports allowed on Walmart + DTC microsites

### Amazon
- 3.44M SKUs, **ALL FBM** (zero FBA) — massive conversion opportunity if FBA enabled
- 144K currently out of stock

### Walmart
- 95,640 SKUs, 99.9% zero reviews
- Need review velocity strategy alongside SKU selection

## 9. Dependencies & Blockers

| Blocker | Owner | Status |
|---------|-------|--------|
| Design-level revenue query (Supabase) | Harry/Ava | 🔴 Not started |
| BigCommerce API connection | Harry | 🔴 Not started |
| GA4 session data pipeline | Harry | 🔴 Not started |
| Walmart pagination fix (10K of 95K) | Harry | ⚠️ Known bug |
| Target+ item export from Partner Portal | Cem | ⚠️ Pending |
| Feedonomics mapping reverse-engineering | Ava | 🔴 Needs both exports |
| GoHeadCase Shopify product catalogue load | Harry | 🔴 Blocked on PIE output |

## 10. Success Metrics

- **Revenue coverage**: Selected 200K SKUs should cover ≥95% of historical revenue potential
- **Collection completeness**: ≥90% of selected designs available across all 4 core product types
- **Device family coverage**: 100% family completeness for top 50 devices
- **Regional optimization**: US and UK device mixes differ by ≥15%
- **Time to first scored output**: 1 week from data pipeline completion

## 11. Immediate Next Steps

1. **Run design-level revenue query** against Supabase — group by design_code, rank within brands
2. **Run Atlas vs Prism dual-analyst benchmark** — validate ensemble approach works
3. **Fix Walmart pagination** — load remaining 85K of 95K listings
4. **Get GA4 session data** — behavioral layer for scoring
5. **Build BigCommerce → Supabase ingestion** — need full 1.89M catalog queryable
6. **Reverse-engineer Feedonomics mapping** — export Target items + BC items → compare

## 12. Sales Dashboard V2 Integration

The PIE outputs feed directly into Sales Dashboard V2:
- SKU selection status by brand/tier
- Revenue coverage visualization (actual vs projected)
- Device family completeness heatmap
- Regional split comparison (US vs UK)
- What-if simulator UI for Cem to adjust parameters

Dashboard: https://app-zeta-sable.vercel.app (needs Supabase backend for persistence)

---

*Created by Ava (CPSO) | 2026-03-07*  
*Source context: Mar 6 deep work session with Cem — product matrix, device analysis, model benchmarking, architecture decisions*

## Related
- [[wiki/02-sales-data/SCHEMA_DESIGN|Schema Design]] — Data foundation for PIE
- [[wiki/02-sales-data/SALES_ANALYSIS_2025|Sales Analysis 2025]] — Baseline metrics
- [[wiki/02-sales-data/SOP_SALES_ANALYTICS|SOP: Sales Analytics]] — Query methodology
- [[wiki/14-goheadcase/GOHEADCASE_PRODUCT_MATRIX|GoHeadCase Product Matrix]] — Product catalog for selection
- [[wiki/23-drew-handover/BIGQUERY_SETUP|BigQuery Setup]] — Data source
