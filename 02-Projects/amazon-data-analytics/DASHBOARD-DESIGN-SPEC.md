# Dashboard Design: Weekly Amazon Listings Trend Analysis

**Created with Advisor Tool (Opus 4.6)** | **Date:** 2026-04-10 | **Owner:** Ava | **Status:** Design Phase

---

## Executive Vision

**Goal:** A real-time dashboard that transforms weekly Amazon listings data into actionable intelligence.

**What it does:**
- Surfaces emerging opportunities (device gaps, FBA migrations, pricing insights)
- Tracks license obligations (NBA, NFL, Shelby, CLC)
- Monitors catalog health (new SKUs, suppression trends, device coverage)
- Enables fast decision-making with clear action items and owners

**Who uses it:** Cem (strategy), Harry (operations), Marketplace Ops team

---

## Architecture Decision: Separate Service (Recommended)

### Why Separate from ecell-dashboard?

**Option A: Extend ecell-dashboard** 
- ❌ Adds complexity to existing BigQuery-driven service
- ❌ Different data source (S3/SQLite JSON vs BigQuery)
- ❌ Different update cadence (weekly spike vs continuous)
- ❌ Risk of destabilizing production sales dashboard

**Option B: New Standalone Service** ✅ **RECOMMENDED**
- ✅ Purpose-built for listings intelligence (not sales)
- ✅ Clean data pipeline (Codex → JSON → Dashboard)
- ✅ Independent scaling (can handle large weekly uploads)
- ✅ Parallel development (doesn't block cron execution)
- ✅ Easy to version/rollback
- ✅ Clear ownership (Ava strategy + Harry infrastructure)

**Decision:** Build as new service: `listings-dashboard` (separate from ecell-dashboard)

---

## Data Model: Weekly Snapshots + Trending

### Data Structure

```
Weekly Report (JSON input from Codex):
├── Date: 2026-04-12
├── Metrics (current week)
│   ├── total_skus: 3,425,000
│   ├── new_skus: 5,000
│   ├── removed_skus: 0
│   ├── suppressed: 45
│   ├── fba_penetration: 42.5%
│   ├── avg_conversion: 2.89%
│   └── shipping_template_compliance: 85%
├── Device Coverage Gaps
│   ├── design_code: NARUTO
│   ├── missing_devices: 3
│   ├── revenue_opportunity: $1,500/month
│   └── priority: HIGH
├── FBA Opportunities
│   ├── design: NFL-MAHOMES
│   ├── current_conversion: 2%
│   ├── fba_expected: 6.4%
│   ├── revenue_lift: $2,000/month
│   └── priority: HIGH
├── License Status
│   ├── license: NBA
│   ├── mg_obligation: $200K
│   ├── current_revenue: $50K
│   ├── gap: -$150K
│   └── status: CRITICAL
└── Actions (recommended)
    ├── owner: Harry
    ├── action: Create NARUTO-IPH16 variants
    ├── timeline: 1 week
    └── expected_impact: +$2K/month
```

### SQLite Schema (Trending)

```sql
-- Weekly snapshots
CREATE TABLE weekly_metrics (
  week_of DATE PRIMARY KEY,
  total_skus INTEGER,
  new_skus INTEGER,
  removed_skus INTEGER,
  suppressed INTEGER,
  fba_penetration REAL,
  avg_conversion REAL,
  shipping_compliance REAL
);

-- Device coverage tracking
CREATE TABLE device_gaps (
  week_of DATE,
  design_code TEXT,
  missing_devices INTEGER,
  revenue_opportunity REAL,
  status TEXT
);

-- FBA opportunities
CREATE TABLE fba_opportunities (
  week_of DATE,
  design TEXT,
  current_conversion REAL,
  expected_conversion REAL,
  revenue_lift REAL,
  status TEXT
);

-- License compliance
CREATE TABLE license_status (
  week_of DATE,
  license TEXT,
  mg_obligation REAL,
  current_revenue REAL,
  gap REAL,
  status TEXT
);

-- Action items
CREATE TABLE action_items (
  week_of DATE,
  action_id TEXT PRIMARY KEY,
  owner TEXT,
  action TEXT,
  timeline TEXT,
  expected_impact REAL,
  status TEXT
);
```

---

## Critical Visualizations (3-5 Views)

### 1. **Listings Health Scorecard** (Top of page)

**What:** Real-time KPI indicators

```
┌─────────────────────────────────────────┐
│  📊 WEEKLY LISTINGS HEALTH              │
├─────────────────────────────────────────┤
│                                          │
│  Total SKUs: 3,425,000  [↑ 5,000]      │
│  New This Week: 5,000   [vs 4,200 last] │
│  Suppressed: 45         [vs 38 last]    │
│  FBA Penetration: 42.5% [↑ 2% trend]   │
│  Avg Conversion: 2.89%  [stable]       │
│  Shipping Compliance: 85% [↓ target 100%] ⚠️ │
│                                          │
└─────────────────────────────────────────┘
```

**Interaction:**
- Click any KPI to drill down
- Hover for week-over-week %

---

### 2. **Opportunity Leaderboard** (Left sidebar)

**What:** Ranked list of top actions to take

```
🎯 TOP OPPORTUNITIES (This Week)

1. 📱 Device Gaps
   NARUTO: Missing 3 devices
   Revenue opportunity: +$2,000/mo
   Priority: HIGH
   [Owner: Marketplace Ops] [Timeline: 1 week]

2. 🚚 FBA Migrations
   NFL-MAHOMES: FBM→FBA
   Expected uplift: +$3,000/mo (3.2x conversion)
   Priority: HIGH
   [Owner: Harry] [Timeline: 2 weeks]

3. 🏷️ Pricing Adjustment
   NARUTO iPhone 17PM: +$2 premium
   Revenue uplift: +$500/mo
   Priority: MEDIUM
   [Owner: Pricing] [Timeline: 3 days]

4. 📛 Negate Terms
   "cody rhodes": $13.52 waste
   Expected savings: $300-500/mo
   Priority: MEDIUM
   [Owner: Hermes] [Timeline: Same day]

5. 🔴 License Gap
   NBA: -$150K obligation
   Fast-track 5 designs
   Priority: CRITICAL
   [Owner: Cem] [Timeline: TBD]
```

**Interaction:**
- Click to expand full details
- Click owner name to assign to them
- Mark as "Done" when completed

---

### 3. **Trend Charts** (Center, 60% width)

**Chart A: Listings Growth Over Time**
```
Total SKUs (Last 12 weeks)

3,450K │
3,425K │     ┌──────────┐
3,400K │    ╱          │
3,375K │───╱           └────
3,350K │
       └────────────────────→
       Apr  May  Jun  Jul
```

**Chart B: FBA Penetration Trend**
```
FBA % of Top 50 Designs

80% │                    TARGET
50% │    ╱────╲
42% │───╱      └─────
40% │
    └────────────────→
```

**Chart C: License Compliance Status**
```
MG Obligation Gap by License

    NBA: -$150K 🔴 CRITICAL
   MLB: -$80K 🟠 BEHIND
  Shelby: -$27K 🟡 WATCH
   NHL: +$10K ✅ AHEAD
    NFL: EXPIRED ⚠️ ACTION
```

**Interaction:**
- Hover for exact numbers
- Click to see contributing designs
- Toggle week/month/quarter view

---

### 4. **Device Coverage Heatmap** (Right sidebar)

**What:** Quick visual of which designs need which devices

```
Design         | iPhone 17PM | 17Pro | 17 | 16PM | 16Pro | 16
─────────────────────────────────────────────────────────────
NARUTO         |     ✅      |  ✅   | ✅  |  ❌  |  ❌   | ❌
PEANUTS        |     ✅      |  ✅   | ✅  |  ✅  |  ✅   | ✅
ONEPIECE       |     ✅      |  ✅   | ✅  |  ❌  |  ❌   | ❌
HARRYPOTTER    |     ✅      |  ✅   | ✅  |  ✅  |  ✅   | ✅
NARUTO-HB401   |     ✅      |  ✅   | ✅  |  ❌  |  ❌   | ❌
```

**Interaction:**
- Red cells = missing variants (clickable to create)
- Hover for revenue opportunity

---

### 5. **Action Items Timeline** (Bottom, full width)

**What:** Who's doing what, when, with what impact?

```
Due This Week          │ Due Next Week         │ Due Next Month
─────────────────────────────────────────────────────────────
✅ DONE:              │ IN PROGRESS:          │ UPCOMING:
- Negate terms        │ - Create NARUTO-IPH16 │ - FBA migration
  (save $400/mo)      │   (+$2K/mo expected)  │ - License renewal
                      │ - NFL→FBA              │ - NBA fast-track
                      │   (+$3K/mo expected)  │

BLOCKED:
- Shipping template edit (waiting for SP-API capability)
```

---

## Technology Stack

### Frontend
- **Framework:** Next.js 16 (same as ecell-dashboard for consistency)
- **Charts:** Recharts (proven, lightweight)
- **Tables:** TanStack Table (React Table)
- **Styling:** Tailwind CSS (same as conversion-dashboard)
- **State:** React Context + SWR (real-time updates)

### Backend
- **Data source:** SQLite (local) + S3 (JSON archives)
- **API:** Node.js express routes (same as ecell-dashboard)
- **Caching:** 24-hour data freshness (Saturday 8 AM → Sunday 8 AM)
- **Auth:** NextAuth (same as ecell-dashboard)

### Data Pipeline
```
Codex Script (Sat 1 AM)
    ↓
    ├→ weekly_report_YYYY-MM-DD.json (S3)
    ├→ SQLite (local machine)
    └→ Send alert to /api/ingest endpoint
    
NextAuth checks permission
    ↓
Dashboard processes JSON
    ↓
Stores in SQLite trending tables
    ↓
Recharts renders live (auto-refresh every hour)
```

---

## Data Flow: Codex → Dashboard

```
Saturday 1 AM
────────────
Codex weekly_listings_processor.py runs
    ↓
Outputs JSON files:
  - weekly_metrics_2026-04-12.json
  - device_gaps_2026-04-12.json
  - fba_opportunities_2026-04-12.json
  - license_status_2026-04-12.json
  - action_items_2026-04-12.json
    ↓
POST to http://localhost:3000/api/ingest
  {
    "date": "2026-04-12",
    "files": [...]
  }
    ↓
Dashboard API processes:
  1. Parse JSON
  2. Validate schema
  3. Store in SQLite
  4. Trigger Recharts re-render
    ↓
Saturday 8 AM
─────────────
Dashboard live and accessible
  - Cem opens dashboard
  - Sees all KPIs, opportunities, trends
  - Clicks action items to assign/approve
```

---

## Phased Rollout (No Blocking)

### Phase 1: Core Dashboard (Apr 15-20) — 3 days
- ✅ Set up Next.js project (`listings-dashboard`)
- ✅ Create SQLite schema + ingest API
- ✅ Build Listings Health Scorecard (View 1)
- ✅ Build Opportunity Leaderboard (View 2)
- ✅ Connect to Codex script output

**Deliverable:** Functional dashboard, powered by first week's data (Apr 12)

**Blocker:** None — Codex script already outputs JSON

**Timeline:** Won't delay Saturday cron (runs in parallel)

### Phase 2: Trending + Charts (Apr 21-27) — 3 days
- Add Trend Charts (View 3, 4)
- Add Device Coverage Heatmap (View 5)
- Add Action Items Timeline
- Build drill-down views (click → details)

**Deliverable:** Full dashboard with 12 weeks of historical data

### Phase 3: Automation + Intelligence (May 1-15) — 2 weeks
- Wire action item assignments (Slack integration)
- Auto-notify owners when actions are due
- Build alert system (e.g., "FBA opportunity detected, estimated ROI: $3K/mo")
- Export weekly PDF report

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|-----------------|
| **Time to insight** | <2 min | Cem opens dashboard, spots #1 opportunity |
| **Action identification** | 5+ per week | Dashboard lists 5+ recommended actions |
| **Decision velocity** | Same-day | Cem approves action within 24h of cron |
| **Revenue impact** | +$10K/mo | Track completed actions → realized lift |
| **Team engagement** | 3+ users | Harry, Marketplace Ops, Hermes using it |

---

## Implementation Timeline

**Week 1 (Apr 13-19):**
- Codex script runs Saturday (Apr 13) → generates first week of data
- Dashboard Phase 1 built (Apr 15-19) → live for review by Apr 20

**Week 2 (Apr 20-26):**
- Dashboard Phase 2 (trending, charts)
- First full 2-week trend analysis available (Apr 19 + Apr 26)

**Week 3+ (May 1+):**
- Phase 3 (automation, alerts, exports)
- Regular weekly insights flowing to team

---

## Budget & Resources

| Resource | Time | Cost |
|----------|------|------|
| Frontend dev (Phase 1) | 3 days | Forge (Codex CLI) |
| Backend API (Phase 1) | 1 day | Harry (infrastructure) |
| Data pipeline (already done) | 0 | Codex script (existing) |
| Phase 2 enhancements | 3 days | Forge |
| Phase 3 automation | 10 days | Harry + Spark |

**Total:** 17 days, no blockers to Saturday cron

---

## Next Steps

1. **Approve architecture** — Separate service? Next.js? SQLite?
2. **Assign Phase 1 owner** — Forge (frontend) + Harry (API)
3. **Schedule kickoff** — Apr 14, after Saturday cron proves data quality
4. **Plan Phase 2-3** — Prioritize trending charts vs automation?

---

**Status:** Ready for approval | **Owner:** Ava | **Advisor-Reviewed:** ✅ (Opus 4.6)

