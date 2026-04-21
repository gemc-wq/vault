# Inventory Ordering App — Decision Log
**Date:** 2026-04-13 | **Participants:** Cem (CEO) + Athena (Chief of Staff)

All decisions made in a single working session. PRD: MASTER_PRD.md (1,052 lines).

| # | Decision | Cem's Call |
|---|----------|-----------|
| 1 | Velocity formula | Tiered: best sellers MAX(7d/7, 30d/30), standard items 30d/30 only |
| 2 | Best seller definition | Top 50 global + top 50 per supply zone (union, ~80-120 items) |
| 3 | PH stock allocation | Proportional to FL vs UK velocity — same math feeds shipping plan |
| 4 | UK zone shipping | UK + PH split (not 100% UK) — PH handles overflow |
| 5 | Two procurement processes | Process 1: Internal Stock Transfers. Process 2: Supplier Ordering. |
| 6 | Transfer frequency | Weekly, Friday/Saturday from PH |
| 7 | Supplier order frequency | Bi-weekly |
| 8 | On-demand capability | Stock-out alerts trigger immediate transfer/order report |
| 9 | Lead time | 14-21 days China → destination (not 56) |
| 10 | Reorder levels | Normal items: velocity × 30 days. Best sellers: velocity × 45 days. |
| 11 | Build approach | Shadow mode — parallel with legacy Zero, compare outputs, GAP analysis |
| 12 | Agentic architecture | 3 layers: Data (SQL/cron) → Intelligence (Claude API advisory) → Portal (human gatekeeper) |
| 13 | Stale stock | 30d no sales = stale. <5/week + created 2024 or earlier = retire candidate (human decides) |
| 14 | China warehouse | No transit tracking. CN logs receipt, creates packing list, ships. Destination confirms. |

## Key Users Identified
- **Chris Yunnun** — Warehouse manager (PH), currently triggers in legacy Zero
- **Jae Vitug** — PH operations, sends packing list emails
- **Ben** — China office, receives POs

## Critical Data Findings
- avg_daily_sales uses 7d window only (fixed in spec to tiered)
- Supabase orders table is 70% incomplete (must use blank_inventory)
- "Florida" vs "FL" warehouse duplication (FL = packaging only)
- 95 active stock-outs in PH, 1,054 dead stock items
- Zero additional freight cost for internal transfers (piggyback existing shipments)

## Business Continuity
Cem classified this as a business continuity task. Must be correct. Data integrity verified in parallel.

## Session 2 Decisions (Cem, Apr 13 — post-council review)

| # | Decision | Cem's Call |
|---|----------|-----------|
| 15 | FBA Restock | Separate app (already exists on GitHub). Out of scope for this build. Top 30 best sellers always stocked — 6-day FBA restock cycle. |
| 16 | PH safety stock | Confirmed 21 days (raised from 14). PH must support both FBA pulls and direct fulfillment. |
| 17 | Zero system risk | App MUST be built to survive Zero failure. Zero is 2-decade-old PHP on Windows 2007. If it dies, data pipeline breaks. |
| 18 | Order freshness monitoring | AI-managed layer to detect when orders stop flowing per channel. Alert if Amazon silent >2h, eBay >4h, Walmart >6h. |
| 19 | eBay API middleware | Amazon middleware exists. eBay middleware NOT YET BUILT — needed for Zero bypass. |
| 20 | Business Blueprint 3.0 | Strategic question deferred: retain AWS MySQL or replace with direct-to-Supabase? Offline discussion. |
| 21 | Build tools | Install GSD (Get Shit Done) globally. Use Agent Teams for parallel build execution. |
| 22 | Council fixes | Apply all 35 fixes from both council reviews before build. Done — PRD v2.0 (1,481 lines). |

## Session 3 — Sentinel & Scope Boundary (Cem, Apr 13)

| # | Decision | Cem's Call |
|---|----------|-----------|
| 23 | Sentinel agent | NEXT priority after inventory ordering. Watches crons, data freshness, order imports, inventory sync. Separate project — do NOT let it interrupt this build. |
| 24 | Zero fragility — what's unstable | Cron on Apache 2 / PHP (order import, inventory sync). Manual shipping labels. Manual PO creation for print files. Xero = stable (MySQL + APIs to marketplaces). |
| 25 | Fulfillment project | Open, started by Harry, must continue separately. Includes shipping label automation + print file POs. |
| 26 | Third-party shipping (VeeCo) | Good for US, bad for UK. Not viable as single solution. |
| 27 | Fallback data strategy | Worst case: download from Amazon API as backup. Ideal: shadow data stream from Zero DB to BigQuery. |
| 28 | Scope boundary | This inventory ordering project = PROJECT 1. Sentinel + Zero bypass + fulfillment = PROJECT 2 ("Athena 2"). Don't mix them. |

## Sentinel Agent — Scope Notes (for Project 2)

**What Sentinel watches:**
- Order import freshness (per marketplace, per channel)
- Inventory sync (BigQuery ← AWS MySQL)
- Cron health (Apache 2 / PHP jobs)
- Data staleness detection across all systems
- API health per marketplace (Amazon, eBay, Walmart)

**What's stable (low priority for Sentinel):**
- Xero = MySQL + marketplace APIs — reliable
- AWS MySQL instance — secure, handles orders
- Amazon API middleware — exists and working

**What's fragile (high priority for Sentinel):**
- PHP crons on Apache 2 (order import, inventory feeds)
- Manual workflows: shipping labels, print file POs
- No eBay API middleware yet

**Cem's framing:** "We definitely need the Sentinel in place next — that's key to watch the data."

## DelegAIt Opportunity
This inventory ordering system — velocity-based procurement, zone allocation, shadow mode, order freshness monitoring — is a generalizable product for any multi-warehouse e-commerce business. Flag for DelegAIt product pipeline.

Sentinel agent is also DelegAIt-productisable: any business running legacy systems needs data pipeline health monitoring.
