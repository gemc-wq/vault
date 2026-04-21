# Project Plan v2: Unified Listings Intelligence Dashboard & Bulk Operations
## (Incorporates All 9 Deliverables + 7 Integration Points)

**Date:** 2026-04-11 | **Owner:** Ava | **Status:** PLANNING | **Approved by:** Cem | **Version:** 2 (with SOP datapoints integrated)

---

## Reference Documents

**PROJECT-SHAPE-UNIFIED-LISTINGS-INTELLIGENCE.md** — Five unified gap dimensions with Stage 1-3 phasing.

**ADVISOR-REVIEW-UNIFIED-LISTINGS-INTELLIGENCE.md** — Architecture approved by Opus 4.6.

**MISSED-DATAPOINTS-ADDENDUM.md** — 7 additional datapoints from SOP audit + memory review.

---

## Nine Core Deliverables + Seven Integration Points

**9 from priority list + 7 from SOP audit = 16 total deliverables**

### 1️⃣ **Incorrect Shipping Templates** (Deliverable 1)
- Shipping Compliance Scorecard + heatmap
- Codex SP-API bulk updates
- **CRITICAL BLOCKER:** Confirm exact Amazon template names (US/UK/DE) with Cem
- Revenue: +$37.5K/month

### 2️⃣ **Champion Device Gaps** (Deliverable 2)
- 2a) Top elbow devices from PULSE
- 2b) Product type gaps (HTPCR vs HB401)
- 2c) Champion design gaps using PULSE logic
- Revenue: +$150-200K/month

### 3️⃣ **PH EOD Comparison** (Deliverable 3 — ENHANCED)
- Daily delta: PH reported vs actual listings
- **NEW:** Accuracy % per team member (leaderboard)
- **NEW:** Accuracy by product type + trend tracking
- Slack posts (8 AM & 4 PM)

### 4️⃣ **Listings Blockers** (Deliverable 4)
- Suppressed items, missing images, pricing errors
- Blockers Report dashboard

### 5️⃣ **Cross-Regional Gaps** (Deliverable 5)
- Market behavior differences (UK sports teams, device preferences by region)
- Cross-Region Heatmap

### 6️⃣ **Sales Traffic Analysis** (Deliverable 6 — TWO BRANCHES)
- 6a) FBA/Prime conversion opportunities (+$50-75K/month)
- 6b) Other platforms gap analysis

### 7️⃣ **Conversion/Sales Analytics** (Deliverable 7)
- Reference Conversion Dashboard + PULSE (don't duplicate)
- Listings Intelligence feeds findings back

### 8️⃣ **Automated Feedback Loop & PH Tracking** (Deliverable 8)
- Slack integration, task tracking, Blueprint V3 integration

### 9️⃣ **Self-Learning Loop** (Deliverable 9)
- Hermes auto-detects new licenses/designs/devices
- New license/design gap reports

---

## Seven Integration Points (From SOP Audit)

### A. **Business Reports Integration**
- **What:** 14d + 30d reports (already downloaded, not parsed)
- **Add to:** Stage 1 data pipeline
- **New table:** `business_metrics` (sessions, orders, conversion, units, revenue)
- **Use:** Weight gaps by traffic impact
- **Owner:** Hermes
- **Timeline:** Stage 1, Week 1-2
- **Revenue:** Enables smart prioritization

### B. **Traffic/Sessions Analysis Dashboard**
- **New View 6:** Traffic & Conversion Trends
- **Show:** Sessions 7d vs 30d momentum, conversion rate by device, funnel analysis
- **Owner:** Forge + Hermes
- **Timeline:** Stage 1-2
- **Revenue:** +2-3% conversion per insight

### C. **Buy Box Loss Root Cause**
- **New View 7:** Buy Box Analysis
- **Show:** Why did Buy Box disappear? Correlation with shipping templates
- **Owner:** Hermes + Codex
- **Timeline:** Stage 2
- **Revenue:** +2-5% if recovered

### D. **Keyword Gap Analysis** (Blocked on Ads API)
- **New View 8:** Keyword Opportunities
- **Show:** Search terms missing our SKUs, auto-suggest additions
- **Owner:** Atlas + Codex
- **Timeline:** Stage 2.5
- **Blocker:** Drew (Amazon Ads API)
- **Revenue:** +5-10% per keyword

### E. **PH Team Performance Audit (Detailed)**
- **Expand Deliverable 3** with accuracy leaderboard + product type breakdown
- **New scorecard:** Team member accuracy, product type accuracy, trends
- **Timeline:** Stage 1 (already in SOP Step 4)

### F. **Shipping Template Rules Confirmation** ⚠️ CRITICAL BLOCKER
- **Action:** Cem confirms exact Amazon template names (US/UK/DE)
- **Also:** Size/weight tier rules
- **Create:** `SHIPPING_TEMPLATE_RULES.md`
- **Timeline:** ASAP (blocks Stage 1)

### G. **Carrier Compliance Review** (From SOP Step 5)
- **Add to Stage 2:** Weekly Veeqo check (rate changes, surcharges, SLA violations)
- **New alert:** Carrier Issues in dashboard
- **Owner:** Codex + Bolt
- **Blocker:** Harry (Veeqo API creds)
- **Timeline:** Stage 2

---

## Three Stages: 11-Week Timeline (Revised with Integration Points)

### STAGE 1: Unified BI Tool + Integration Points (Apr 15-May 5, 3 weeks)

#### Data Pipeline (Codex + Hermes)

| Task | Owner | Duration | Dependencies | Status |
|------|-------|----------|--------------|--------|
| **BLOCKER:** Confirm shipping rules (US/UK/DE) | Cem | 0.5d | Cem review | 🔴 BLOCKED |
| Build SQLite schema (listings_full) | Codex | 2d | None | Ready |
| Load Active Listings Report (weekly) | Codex | 1d | S3 access | Ready |
| Load BQ orders (sales velocity) | Codex | 1d | BQ creds | Ready |
| **NEW:** Load Business Reports (14d+30d) | Hermes | 1d | CSV files | Ready |
| Load PULSE leaderboard | Hermes | 2d | PULSE export | Ready |
| **NEW:** Compute traffic analysis | Hermes | 1d | Business Reports | Ready |
| Compute all 5 gap dimensions | Codex | 3d | Schema + data | Ready |
| Index queries | Codex | 1d | SQLite | Ready |
| **Total** | | **12.5d** | | |

#### Dashboard (Forge)

| Task | Owner | Duration | Dependencies | Status |
|------|-------|----------|--------------|--------|
| View 1-5 (core) | Forge | 15d | Schema | Ready |
| **NEW:** View 6: Traffic & Conversion | Forge | 2d | Business Reports | Ready |
| Deployment + styling | Forge | 2d | Next.js | Ready |
| **Total** | | **19d** | | |

#### PH Team Audit (Codex + Ava)

| Task | Owner | Duration | Dependencies | Status |
|------|-------|----------|--------------|--------|
| Daily delta check + Slack posts | Codex | 1d | BQ query | Ready |
| **NEW:** Accuracy % by team member | Codex | 1d | EOD analysis | Ready |
| **NEW:** Product type breakdown + trend | Ava | 1d | Historical data | Ready |
| Cron (daily) | Codex | 1d | Scheduler | Ready |
| **Total** | | **4d** | | |

**Stage 1 Timeline:** Apr 15-May 5 (3 weeks)

**Stage 1 Deliverables:**
- SQLite database (all 5 gaps + Business Reports + traffic data)
- Dashboard Views 1-6 (read-only, no execution)
- PH Team Audit scorecard (accuracy leaderboard)
- Weekly data refresh cron

**Stage 1 Blockers:**
- 🔴 Shipping template rules (Cem must confirm names)
- ✅ Everything else ready

---

### STAGE 2: Execution Engine + Integration Points (May 5-25, 3 weeks)

#### Per-Dimension Executors (8 days each, parallel)

1. **Shipping template updates** (Codex) — SP-API
2. **Device coverage gaps** (Hermes) — CSV to PULSE
3. **Cross-region gaps** (Hermes) — CSV to SKU staging
4. **FBA migration** (Codex) — CSV to Harry
5. **PRUNE** (Codex) — SP-API suppress
6. **PH EOD + audit** (Codex) — Enhanced Slack + reporting
7. **Blockers** (Codex) — Detection + dashboard
8. **Carrier compliance** (Codex + Bolt) — Weekly Veeqo check ⏳ Blocked on Harry

#### Dashboard Enhancements (Forge)

| Task | Owner | Duration | Dependencies | Status |
|------|-------|----------|--------------|--------|
| View 5: Full execution pipeline | Forge | 2d | Queue table | Ready |
| **NEW:** View 7: Buy Box Analysis | Forge | 2d | Correlation data | Ready |
| **NEW:** View 8: Keyword Gap (stub) | Forge | 1d | Ads API (blocked) | 🔴 Blocked |
| Slack notifications | Forge | 1d | Webhook | Ready |
| **Total** | | **6d** | | |

**Stage 2 Timeline:** May 5-25 (3 weeks)

**Stage 2 Deliverables:**
- Shipping template bulk updates (SP-API)
- Device, cross-region, FBA, PRUNE outputs
- PH EOD + audit (enhanced)
- Blockers reporting
- Carrier compliance cron
- Views 5-7 (execution, Buy Box, keyword stub)

**Stage 2 Blockers:**
- 🔴 Keyword gaps View 8 (awaiting Drew - Ads API)
- 🔴 Carrier compliance (awaiting Harry - Veeqo creds)

---

### STAGE 3: Automation & Intelligence (May 25+, 5 weeks)

- Auto-prioritization by revenue impact
- Self-learning loop (Hermes detects new licenses/designs)
- Keyword gaps View 8 (once Ads API available)
- Amazon Ads integration

---

## Revenue Impact: 16 Deliverables

| Deliverable | Owner | Timeline | Revenue |
|-------------|-------|----------|---------|
| 1. Shipping templates | Codex | S1-S2 | +$37.5K/mo |
| 2. Champion device gaps | Hermes | S1-S2 | +$150-200K/mo |
| 3. PH EOD + audit | Codex | S1-S2 | Risk mitigation |
| 4. Blockers | Codex | S2 | Operational |
| 5. Cross-region | Hermes | S2 | +$80-100K/mo |
| 6a. FBA opportunities | Codex | S2 | +$50-75K/mo |
| 6b. Platform gaps | Loom | S2 | TBD |
| 7. Conversion analytics | Hermes | Ongoing | PULSE feed |
| 8. Feedback loop + Blueprint | Codex | S2-S3 | Operational |
| 9. Self-learning | Hermes | S3 | Ongoing |
| A. Business Reports | Hermes | S1 | Prioritization |
| B. Traffic/Sessions | Forge | S1-S2 | +$20-30K/mo |
| C. Buy Box | Hermes | S2 | +$30-50K/mo |
| D. Keyword gaps | Atlas | S2.5 | +$50-100K/mo (blocked) |
| E. PH Audit (detailed) | Codex | S1 | Risk mitigation |
| F. Shipping rules | Cem | ASAP | Critical input |
| G. Carrier compliance | Codex | S2 | SLA maintenance |
| **TOTAL** | | **S1-S3** | **$350-550K/year** |

---

## Team Assignments (Updated)

| Area | Owner | Backup | Status |
|------|-------|--------|--------|
| Data pipeline | Codex | Hermes | Ready |
| Business Reports ETL | Hermes | Codex | Ready |
| Dashboard (Views 1-8) | Forge | Spark | Ready |
| Traffic analysis | Forge | Spark | Ready |
| Buy Box analysis | Hermes | Codex | Ready |
| PULSE integration | Hermes | Ava | Ready |
| SP-API execution | Codex | Spark | Ready |
| PH audit (enhanced) | Codex | Harry | Ready |
| Carrier compliance | Codex | Bolt | 🔴 Blocked (Veeqo) |
| Ads integration | Atlas | Codex | 🔴 Blocked (API) |
| Shipping rules | Cem | Ava | 🔴 CRITICAL |

---

## Critical Blockers (Must Resolve Before Stage 1)

1. **🔴 SHIPPING RULES (Cem):** Confirm exact Amazon template names (US/UK/DE)
2. **🔴 VEEQO CREDS (Harry):** Needed for carrier compliance cron (Stage 2)
3. **🔴 ADS API (Drew):** Needed for keyword gaps View 8 (Stage 2.5)

---

## Success Criteria

**Stage 1 (May 5):** Dashboard + Views 1-6 live, shipping rules confirmed, PH audit enhanced

**Stage 2 (May 25):** Execution engine working, 1K+ shipping updates, Views 7 live, carrier cron running

**Stage 3 (Jun 30):** Auto-prioritization, self-learning, Ads integration (if API available)

---

## Next Steps (Cem Approval)

1. ✅ Approve revised 16-deliverable plan
2. ✅ **CRITICAL:** Confirm shipping template names (US/UK/DE) — BLOCKS Apr 15 start
3. ✅ Assign team (finalize backups)
4. ✅ Schedule weekly syncs
5. ✅ Ready to kick off: **Monday, Apr 15** (if shipping rules confirmed)

---

**Status:** PLANNING v2 COMPLETE ✅ | **Awaiting:** Shipping rules confirmation from Cem | **Ready to BUILD**

