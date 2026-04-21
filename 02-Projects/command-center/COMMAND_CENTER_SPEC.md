# Strategic Command Center — Project Spec

> **"A high-level brain that picks through the noise, keeps projects on track and on the RIGHT track, and suggests diversions."**

## The Problem

Information is everywhere:
- 20+ project folders in Brain/
- 3 agent workspaces with memory files
- Orbit PM tasks
- BigQuery sales data (2.8M orders)
- Supabase (orders, inventory, Walmart listings)
- Shopify stores (products, orders)
- Cron outputs (daily reports, momentum briefs)
- Git repos (code deployment status)
- Research docs, handoffs, SOPs

No single view answers:
- **Are we working on the right things?** (strategic alignment)
- **Are projects actually moving?** (velocity/stalls)
- **What should we stop, start, or accelerate?** (portfolio management)
- **How do today's tactics connect to the 12-month goal?** (strategy → execution mapping)

## The Solution: Strategic Command Center

A live dashboard + AI strategy layer that:

### Layer 1: Strategy Map (Top-Down View)
```
MISSION: 10x DTC units (2,609 → 26,000+), Amazon <60%
│
├── PILLAR 1: Microsite Factory
│   ├── Anime Site [🟢 Live] — 65 products, $555K addressable
│   ├── Sports Site [🟡 Prototype] — 50 products loaded, $4.6M addressable
│   ├── GoHeadCase Hub [🟡 Prototype] — needs Shopify store creation
│   ├── Entertainment [⚪ Not Started] — $757K addressable
│   └── Fantasy [⚪ Not Started] — $107K addressable
│
├── PILLAR 2: Marketplace Expansion
│   ├── Walmart Optimization [🟡 Gap Identified] — 895 best sellers missing
│   ├── OnBuy UK Launch [🟢 In Progress] — call completed, integration planned
│   ├── Target+ [🔴 Blocked] — needs Shopify store from Cem
│   └── Amazon ASIN Registry [🟡 Data Collected] — 6.4GB listings on Drive
│
├── PILLAR 3: Infrastructure
│   ├── Brain Memory Layer [🟢 Building] — 59/1286 docs indexed
│   ├── Sales Dashboard V2 [🔴 Blocked] — needs Cloud Run deploy
│   ├── Product Database [🟡 Specced] — SKU rules engine designed
│   ├── EAN Registry [🟡 Data Ready] — Walmart 95K GTINs available
│   └── Mac Studio Migration [🟢 Today] — arriving 12:30-2:30 PM
│
├── PILLAR 4: Operations
│   ├── NBCU PO Processor [🟢 Live] — deployed to Vercel
│   ├── Email Triage [❌ Cancelled] — replaced by Perplexity Max
│   └── Agent Architecture [🟡 Restructuring] — Harry parked, Ava absorbing COO role
│
└── PILLAR 5: Creative & Brand
    ├── Naruto Assets [🟢 Ready] — 20 PSDs, 6 hero banners composed
    ├── Sven Creative Agent [🔴 Crashing] — needs debugging on Mac Studio
    └── Ecell Studio (Image Maker) [⚪ Not Started] — specced, no code

Legend: 🟢 Active/Healthy  🟡 Needs Attention  🔴 Blocked  ⚪ Not Started  ❌ Killed
```

### Layer 2: Intelligence Engine (AI Strategy Advisor)

A weekly AI-generated strategic analysis that:

1. **Reads all project status** from Brain Memory Layer
2. **Pulls business metrics** from BigQuery (revenue trends, channel mix)
3. **Evaluates alignment**: Is each project actually moving the needle on 10x DTC?
4. **Flags misalignment**: "Sports frontend has $4.6M addressable revenue but only 50 products loaded — this should be priority over Entertainment"
5. **Suggests pivots**: "OnBuy UK has lower CAC than building Fantasy microsite — accelerate OnBuy, defer Fantasy"
6. **Identifies stalls**: "Sales Dashboard V2 has been blocked for 8 days — escalate or kill"
7. **Calculates opportunity cost**: "Every week without Walmart gap products listed = ~$15K missed revenue"

Output: **Weekly Strategy Brief** (voice + text) delivered Monday mornings before the operational morning brief.

### Layer 3: Visualization Dashboard

**URL**: `ecell.app/apps/command-center`

#### Views:

**A. Strategy Map** (default view)
- Interactive tree/sunburst showing Mission → Pillars → Projects → Tasks
- Color-coded health status (green/yellow/red/grey)
- Click to drill into any project
- Revenue opportunity sizing on each node

**B. Velocity Board**
- Timeline showing when each project last had meaningful activity
- "Days since last update" counter
- Trend arrows (accelerating, stalling, stuck)
- Auto-populated from Brain Memory Layer + git commits + Orbit

**C. Resource Allocation**
- Where agent time is being spent (Ava, Harry, Sven, sub-agents)
- Cost per project (API tokens, compute)
- ROI estimate: effort invested vs revenue opportunity

**D. Decision Log**
- Every major decision with date, rationale, and outcome
- Pulled from MEMORY.md and Brain/
- Searchable, filterable by project
- "Decision audit": did past decisions prove correct?

**E. Blockers & Dependencies**
- Visual dependency graph
- What's blocking what
- Critical path to 10x goal
- Owner + age of each blocker

**F. Continuous Improvement**
- Weekly retrospective data
- What shipped, what slipped, what we learned
- Strategy drift detector: "You've spent 40% of time on infrastructure but only 15% on revenue-generating microsites"

## Data Architecture

```
┌─────────────────────────────────────────────────┐
│             COMMAND CENTER DASHBOARD              │
│  (Next.js on Vercel → ecell.app/apps/cc)        │
└──────────────┬──────────────────────┬────────────┘
               │                      │
    ┌──────────▼──────────┐  ┌───────▼────────────┐
    │   Supabase API      │  │   BigQuery API     │
    │                     │  │                     │
    │ brain_documents     │  │ zero_dataset.orders │
    │ brain_chunks        │  │ headcase.tblLineups │
    │ orders (304K)       │  │ headcase.tblDesigns │
    │ inventory (9.8K)    │  │                     │
    │ walmart_listings    │  │                     │
    │ cc_projects (NEW)   │  │                     │
    │ cc_decisions (NEW)  │  │                     │
    │ cc_metrics (NEW)    │  │                     │
    └─────────────────────┘  └─────────────────────┘
               ▲                      ▲
               │                      │
    ┌──────────┴──────────┐  ┌───────┴────────────┐
    │  Nightly Sync Cron  │  │  Weekly Strategy    │
    │  (5 AM)             │  │  Analysis Cron      │
    │                     │  │  (Sun 11 PM)        │
    │ - Brain/ folder     │  │                     │
    │ - Agent memories    │  │ - Reads all project │
    │ - Orbit tasks       │  │   status from DB    │
    │ - Git commit logs   │  │ - Pulls BigQuery    │
    │                     │  │   revenue metrics   │
    │                     │  │ - AI analysis       │
    │                     │  │ - Generates brief   │
    └─────────────────────┘  └─────────────────────┘
```

## New Supabase Tables

```sql
-- Projects registry (source of truth for all projects)
CREATE TABLE cc_projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  pillar TEXT NOT NULL,  -- 'microsites', 'marketplace', 'infrastructure', 'operations', 'creative'
  status TEXT NOT NULL DEFAULT 'not_started',  -- active, blocked, stalled, completed, killed, not_started
  health TEXT DEFAULT 'grey',  -- green, yellow, red, grey
  owner TEXT,  -- 'ava', 'harry', 'sven', 'cem', 'codex'
  revenue_opportunity NUMERIC,  -- estimated $ addressable
  last_activity TIMESTAMPTZ,
  days_stalled INT DEFAULT 0,
  blockers JSONB DEFAULT '[]',
  brain_paths JSONB DEFAULT '[]',  -- paths in Brain/ related to this project
  orbit_task_ids JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Decision log
CREATE TABLE cc_decisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES cc_projects(id),
  decision TEXT NOT NULL,
  rationale TEXT,
  decided_by TEXT DEFAULT 'cem',
  outcome TEXT,  -- filled in retrospectively
  decided_at TIMESTAMPTZ DEFAULT NOW()
);

-- Weekly metrics snapshots
CREATE TABLE cc_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  week_start DATE NOT NULL,
  total_dtc_units INT,
  amazon_pct NUMERIC,
  walmart_units INT,
  target_units INT,
  onbuy_units INT,
  microsite_units INT,
  total_revenue NUMERIC,
  active_projects INT,
  blocked_projects INT,
  agent_cost_usd NUMERIC,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Implementation Plan

### Phase 1: Foundation (Day 1-2) — Ava + Codex
- [ ] Create Supabase tables (cc_projects, cc_decisions, cc_metrics)
- [ ] Seed cc_projects with all 20+ known projects from MEMORY.md
- [ ] Build basic Next.js dashboard with Strategy Map view
- [ ] Deploy to ecell.app/apps/command-center

### Phase 2: Auto-Population (Day 3-4) — Ava
- [ ] Cron job: sync project status from Brain Memory Layer nightly
- [ ] Cron job: pull BigQuery revenue metrics weekly
- [ ] Cron job: detect stalls (no brain_documents update in 7 days → yellow)
- [ ] Wire to Orbit PM for task-level status

### Phase 3: Intelligence (Day 5-7) — Ava
- [ ] Weekly Strategy Analysis cron (Sunday 11 PM)
- [ ] AI reads all project status + metrics + decisions
- [ ] Generates "Strategic Alignment Report":
  - Are we on track for 10x?
  - What to accelerate, what to defer
  - Opportunity cost of blockers
  - Recommended priority restack
- [ ] Delivers as Monday morning voice brief + text

### Phase 4: Full Visualization (Week 2) — Codex
- [ ] Velocity Board view
- [ ] Resource Allocation view
- [ ] Decision Log view (searchable)
- [ ] Blockers & Dependencies graph
- [ ] Continuous Improvement retrospectives

### Phase 5: Self-Improving (Week 3+) — Ava
- [ ] Strategy drift detection: alert when effort allocation doesn't match stated priorities
- [ ] Prediction: "At current velocity, Anime microsite reaches 500 units by [date]"
- [ ] Auto-suggest task reordering based on ROI
- [ ] Decision audit: review past decisions and flag ones that need revisiting

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Frontend | Next.js + Tailwind + Recharts | Matches Sales Dashboard V2 |
| Backend | Supabase REST + Edge Functions | Already have it |
| AI Engine | Gemini Flash (cron analysis) | Cheap, fast, good at synthesis |
| Visualization | Recharts + D3 (strategy map) | React-native, interactive |
| Hosting | Vercel → ecell.app | Consistent with other apps |

## Cost

| Item | Monthly |
|------|---------|
| Supabase (existing) | $0 |
| Gemini Flash (weekly analysis) | ~$0.50 |
| BigQuery queries | ~$0.10 |
| Vercel hosting | $0 (free tier) |
| **Total** | **~$0.60/month** |

## Success Criteria

1. Cem can see the full strategic picture in <30 seconds
2. Stalled projects are auto-detected within 48 hours
3. Weekly strategy brief identifies at least one actionable pivot per week
4. Decision log captures every major decision with rationale
5. 10x DTC goal progress is tracked and visible at all times
6. No project goes "forgotten" — everything is visible, everything has an owner

## Key Insight

This isn't just a dashboard. It's the **strategic operating system** for Ecell Global's AI-first operations. The agents do the work; the Command Center ensures they're doing the RIGHT work. It's the difference between busy and productive.

---

*Scoped by Ava, 2026-03-05*
*Estimated build: Phase 1-3 in first week, Phase 4-5 in weeks 2-3*
*Cost: ~$0.60/month*
