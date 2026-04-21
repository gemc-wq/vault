# Listings Management System — Operational Spec

> **Owner:** Ava | **Created:** 2026-03-21 | **Status:** Draft for Cem review
> **Purpose:** Automate the direction, monitoring, and optimization of the PH listings team (~20 staff)
> **Impact:** $500K+ annual labor directed by data instead of guesswork

---

## Problem Statement

20 PH staff (listings + creative) create and manage product listings daily, but:
- ❌ No data-driven target list — they choose what to list themselves
- ❌ No feedback loop — listings go live but nobody checks if they convert
- ❌ No license ROI tracking — $200K MG licenses might be underperforming
- ❌ No gap visibility — champions may not be listed on all marketplaces
- ❌ EOD reports are filed but not systematically analyzed against targets

---

## Three Autonomous Loops

### LOOP 1: Weekly Listings Direction
*"What should the team list this week?"*

```
PULSE Champions (combined back case elbow)
    ↓ filter by marketplace (Amazon US/UK, Walmart, OnBuy)
    ↓ cross-reference against Active Listings (local SQLite)
    ↓ identify GAPS: champion designs NOT listed on each marketplace
    ↓ prioritize by revenue × conversion potential
    ↓
WEEKLY TARGET LIST
    ↓ posted to Slack #listings every Monday 8 AM
    ↓ format: "This week's priority listings — [X] items"
    ↓ each item: SKU, design, device, marketplace, expected revenue
```

**Data sources:**
- Champions: `combined_backcase_champions.json` (300 designs, updated weekly from BQ)
- Active Listings: local SQLite (3.4M US, 5.1M UK — refreshed weekly via AirDrop)
- Conversion data: Amazon Child ASIN reports (14-day + 30-day)

**Output: Slack message every Monday to #listings**
```
📋 *Weekly Listings Target — Week of Mar 24*

*Priority 1 — Walmart Gap Fill (HTPCR):*
1. DRGBSUSC-GOK × iPhone 17 Pro Max ($13.3K combined rev)
2. NARUICO-AKA × iPhone 17 ($10.4K)
3. PNUTBOA-XOX × Samsung S25 Ultra ($10.3K)
...

*Priority 2 — HB401 Image Creation:*
1. NARUICO-AKA × iPhone 17 Pro Max (image needed)
2. DRGBSUSC-GOK × iPhone SE 4 (image needed)
...

*Priority 3 — Amazon UK Coverage Gaps:*
1. LFCKIT25-AWY × iPhone 17 (selling in UK, not on UK Amazon)
...

Total items this week: 50
```

### LOOP 2: License Performance Monitor
*"Which licenses are making money and which are bleeding?"*

```
BQ Orders (90-day revenue by license)
    ↓ match against license terms (MG amounts, royalty %)
    ↓ calculate: actual revenue vs MG pace
    ↓ flag: at-risk licenses (below 50% of MG pace)
    ↓
WEEKLY LICENSE REPORT
    ↓ posted to Slack #marketing every Monday
    ↓ includes: action items per license
    ↓ "NBA needs 50 new listings + PPC campaign to hit MG"
```

**License health calculation:**
```
Annual MG = $100K
Monthly MG pace = $8,333/month
Actual monthly revenue = $4,000
Status: 🔴 AT RISK (48% of target)
Action: List top 20 NBA designs on Walmart + launch PPC on top 10 ASINs
```

**Key licenses to monitor:**
- NBA ($200K MG — currently underperforming)
- NFL ($25K MG — expires Mar 31, renewal decision made)
- Real Madrid ($50K MG — 15% pace, critical)
- Warner Bros (renewed, needs monitoring)

**Output: Weekly Slack + Telegram report**

### LOOP 3: Conversion Feedback (14-Day Attribution)
*"Did the listings we created 2 weeks ago actually work?"*

```
Week 0: PH team lists items (recorded in EOD + Active Listings)
    ↓ track listing creation date from Active Listings open_date
Week 2: Pull Amazon sessions + conversion for those specific ASINs
    ↓ compare against category average conversion (2.2%)
    ↓ classify:
        ✅ WINNER: above-avg conversion → scale (more devices, PPC)
        ⚠️ NEEDS WORK: high sessions, low conversion → fix images/copy
        🔴 UNDERPERFORMER: low sessions, low conversion → review or retire
    ↓
BI-WEEKLY PERFORMANCE REPORT
    ↓ posted to Slack #listings
    ↓ "Your listings from March 7 — here's how they performed"
```

**14-Day Attribution Timeline:**
```
Day 0:   PH team creates listing (captured in EOD)
Day 1-2: Amazon indexes listing
Day 3-7: Initial sessions data available (unreliable)
Day 14:  Full attribution window — reliable conversion data
Day 16:  System pulls sessions report, matches to creation date
Day 17:  Performance report generated + posted to Slack
```

**Matching logic:**
```python
# Find SKUs listed in the last 14-21 days
new_listings = listings_current WHERE open_date BETWEEN (today - 21 days) AND (today - 14 days)

# Match against sessions report by ASIN
for listing in new_listings:
    asin = asin_bridge[listing.sku]
    sessions = sessions_report[asin]
    conversion = sessions.units / sessions.sessions
    
    if conversion > avg_conversion * 1.2:
        status = "WINNER"
    elif sessions.sessions > 50 and conversion < avg_conversion * 0.5:
        status = "NEEDS_WORK"  # high traffic, low conversion = listing issue
    else:
        status = "MONITORING"
```

---

## Data Architecture

### What we have:
| Data | Location | Freshness |
|------|----------|-----------|
| Order velocity | BQ → Supabase | Nightly 3 AM sync |
| Active Listings (US) | Local SQLite | Weekly AirDrop refresh |
| Active Listings (UK) | Local SQLite | Weekly AirDrop refresh |
| Amazon Sessions (14d/30d) | Local CSV | Weekly AirDrop |
| EAN database | Local SQLite | 480K mappings |
| Champion designs | JSON file | Updated from BQ weekly |
| EOD reports | Slack channels | Daily (PH team posts) |

### What we need to build:
| Data | Purpose | Location |
|------|---------|----------|
| `listings_targets` table | Weekly target list tracking | Supabase |
| `listings_performance` table | 14-day attribution results | Supabase |
| `license_obligations` table | MG terms, deadlines, status | Supabase |
| `weekly_task_queue` | Auto-generated from PULSE gaps | Supabase |

### Supabase Schema (new tables):

```sql
-- Weekly target tracking
CREATE TABLE listings_targets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    week_start DATE NOT NULL,
    sku TEXT NOT NULL,
    design_code TEXT,
    device_code TEXT,
    marketplace TEXT, -- 'amazon_us', 'amazon_uk', 'walmart', 'onbuy'
    priority INTEGER, -- 1=highest
    revenue_potential DECIMAL,
    status TEXT DEFAULT 'pending', -- pending, assigned, completed, verified
    assigned_to TEXT, -- PH team member
    completed_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 14-day attribution tracking
CREATE TABLE listings_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku TEXT NOT NULL,
    asin TEXT,
    listed_date DATE NOT NULL,
    review_date DATE, -- listed_date + 14-16 days
    sessions_14d INTEGER,
    units_14d INTEGER,
    conversion_rate DECIMAL,
    category_avg_conversion DECIMAL,
    performance_status TEXT, -- WINNER, NEEDS_WORK, UNDERPERFORMER, MONITORING
    action_taken TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- License obligation tracking
CREATE TABLE license_obligations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    license_name TEXT NOT NULL,
    brand_code TEXT,
    mg_amount_annual DECIMAL,
    royalty_percentage DECIMAL,
    contract_start DATE,
    contract_end DATE,
    renewal_deadline DATE,
    actual_revenue_ytd DECIMAL,
    mg_pace_percentage DECIMAL, -- actual vs target
    status TEXT, -- ON_TRACK, AT_RISK, CRITICAL, EXPIRED
    action_items TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Cron Schedule

| Time | Job | Output |
|------|-----|--------|
| Mon 7 AM | Generate weekly target list from PULSE gaps | Slack #listings + #creative |
| Mon 7 AM | License performance report | Slack #marketing + Telegram to Cem |
| Daily 8 AM | Slack EOD digest + review summary | Slack channels + Telegram |
| Daily 8 AM | Cross-reference EODs against weekly targets | Track completion rate |
| Wed 7 AM | Mid-week progress check on targets | Slack #listings |
| Fri 5 PM | Remind Cem to download Amazon reports | Telegram |
| Sat 7 AM | 14-day attribution review (for items listed 2 weeks ago) | Slack #listings + Telegram |

---

## Implementation Phases

### Phase 1 (Week 1): Weekly Target Generation
- [ ] Build gap finder: champions × marketplaces → missing listings
- [ ] Auto-post to Slack #listings every Monday
- [ ] Track completion via EOD cross-reference

### Phase 2 (Week 2): License Monitor
- [ ] Load license terms into Supabase
- [ ] Calculate revenue pace vs MG
- [ ] Weekly report to #marketing

### Phase 3 (Week 3): 14-Day Attribution
- [ ] Match new listings (by open_date) to sessions data
- [ ] Classify performance (winner/needs work/underperformer)
- [ ] Bi-weekly performance report

### Phase 4 (Week 4): Closed Loop
- [ ] EOD analysis: parse team member names + tasks from Slack messages
- [ ] Match completed work against target list
- [ ] Auto-update completion status
- [ ] Generate individual performance metrics per team member

---

## Success Metrics

| Metric | Current | Target (90 days) |
|--------|---------|-------------------|
| Listings with clear targets | ~0% | 100% |
| Champion gap fill rate | Unknown | >80% of top 300 listed on Walmart |
| License at-risk alerts | Manual/none | Automated weekly |
| 14-day conversion feedback | None | Weekly reports |
| Team utilization on champions | Unknown | >70% of listings are champion designs |
| Time from design to live listing | 2-4 weeks | <1 week |

---

*This spec connects to: Master Architecture (MEMORY.md), Champion Selection Methodology, PULSE Dashboard, HB401 Gap Tracker, Marketplace Expansion Plan*

---

## Season Launch Playbook

> **Purpose:** Coordinated product launch across all marketplaces for seasonal kit releases
> **Frequency:** Twice yearly — mid-season (January) and new season (August)
> **Added:** 2026-03-23

### Timeline: 2026 Calendar

```
NOW (Mar) ──→ May: World Cup HB401 sprint (91 gaps across 15 football clubs)
June-July:     World Cup 2026 (US/Canada/Mexico) — club merch sales surge
August:        New 2026/27 season kits launch (EPL, La Liga, Serie A)
September:     Monitor new kit velocity, expand to all devices
```

### Season Launch Process

```
Week -8:  New kit designs received from licensors
    ↓
Week -6:  Creative team produces images for ALL devices × case types
    ↓ Sven/image pipeline generates mockups in parallel
Week -4:  Content generated from SKU templates (titles, descriptions, bullets)
    ↓ Echo refines per marketplace
Week -3:  EANs assigned from unassigned pool
    ↓ Auto-assignment engine
Week -2:  Staged in Supabase product master
    ↓ QA gate: images + content reviewed
Week -1:  Pre-uploaded to all marketplaces as DRAFT
    ↓ Shopify, Walmart, OnBuy, Kaufland
Day 0:    PUBLISH simultaneously across all channels
    ↓ PPC campaigns launched on top champions
Week +2:  First conversion data available (14-day attribution)
    ↓ AutoPricer baseline established
Week +4:  Full velocity data — identify new champions
    ↓ PULSE updates elbow, gap analysis refreshes
```

### Old Kit Retirement

| Action | Timing | Method |
|--------|--------|--------|
| Stop PPC on old kits | Day 0 of new season | Pause campaigns |
| Mark old kits as "Previous Season" | Week +2 | Add tag in Shopify/Amazon |
| Reduce price by 20% | Week +4 | AutoPricer clearance experiment |
| Retire from new marketplaces | Week +12 | Remove from Walmart/OnBuy if zero sales |
| Keep on Amazon | Indefinitely | Some collectors buy previous season |

### Football Club Licenses (Active as of Mar 23, 2026)

| League | Clubs |
|--------|-------|
| EPL | Arsenal, Liverpool, Chelsea, Tottenham, Man City, Aston Villa, Wolves, Newcastle, Crystal Palace |
| La Liga | Real Madrid, FC Barcelona |
| Serie A | AC Milan, Inter (renewal pending), Juventus |
| Bundesliga | Bayer Leverkusen |
| Scottish | Scottish FA |
| **EXPIRED** | ~~AS Roma~~ (expired, flagged for PRUNE) |

### World Cup 2026 HB401 Sprint (Mar-May)

**91 missing HB401 device×club combos** across top 20 US devices.

Common missing devices (all clubs):
- iPhone 13, Galaxy S25 Ultra, Galaxy S25
- iPhone SE 4 (top clubs only)

**Depends on:** Huaqing blank order arriving (Samsung S26 + iPhone gaps)

**Post to Slack:** Weekly progress via #eod-listings + #creative

### New Product Lines (August 2026)

Cem confirmed new product lines launching with 2026/27 season:
- New kit designs for all licensed clubs
- Potentially new product types (TBD)
- Must hit all marketplaces simultaneously
- Pipeline must be ready: design → image → content → EAN → push

---

*This playbook connects to: Master Architecture, Champion Selection Methodology, HB401 Gap Tracker, World Cup Readiness Check*
