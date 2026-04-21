# PULSE — Product Uplift & Listing Signal Engine
**Scope v3.1**  
**Priority:** P0  
**Owner:** Ava (Strategy) + Atlas (Analysis)  
**Sponsor:** Cem (CEO)  
**Created:** 2026-03-07 | **Updated:** 2026-03-09 (v3.1 — council review + license obligation layer)

---

## 1. What PULSE Is

An opportunity identifier. It watches what's already selling, measures acceleration, and surfaces gaps we're leaving money on the table for — weighted by license obligations that determine which gaps cost us the most.

**Two questions drive everything:**

> **Q1: "What is live right now, generating views and sales, that is NOT listed on all channels?"**

> **Q2: "What design is winning in one form factor that we don't have in another high-velocity form factor?"**

Q1 finds distribution gaps. Q2 finds new product opportunities. Both are weighted by how urgently we need to hit minimum guarantees on each license.

PULSE is not a catalog ranker. It's a velocity-triggered, license-weighted alert system.

---

## 2. Velocity Engine

### Comparative Lookback

| Window | Period | Role |
|--------|--------|------|
| **Baseline** | 6 months | Establishes the normal monthly run rate for a design |
| **Velocity** | 1–2 months | What's happening right now |

**Signal = velocity_revenue ÷ baseline_monthly_avg**

| Ratio | Signal | What it means |
|-------|--------|---------------|
| > 2.0x | 🚀 Surging | This is on fire — expand everywhere NOW |
| 1.3–2.0x | 📈 Accelerating | Growing — prioritize for next push |
| 0.7–1.3x | ➡️ Steady | Normal — maintain, no urgency |
| 0.3–0.7x | 📉 Declining | Slowing down — don't invest more |
| < 0.3x | 💀 Dying | Reclaim the listing real estate |

### Device Lifecycle Normalization

iPhone case demand follows the device lifecycle — iPhone 16 cases surge at launch (Sep 2025) and decline when iPhone 17 launches (Sep 2026). PULSE must separate **design velocity** from **device lifecycle effects**.

Method: normalize each design's velocity against the aggregate velocity of ALL designs on that same device. If iPhone 16 Pro Max cases are declining 15% across the board, a design declining 10% is actually outperforming — not dying.

### Session Momentum (Amazon layer)

Revenue velocity can miss unmet demand. Amazon session data adds a second signal:

| Sessions | Conversion | Read | Action |
|----------|-----------|------|--------|
| High | Rising | Validated demand | Push everywhere |
| High | Low | Bad listing, not bad product | Fix content first |
| Low | High | Hidden gem | Boost visibility |
| Low | Low | No demand | Skip |

---

## 3. Six Alert Types

Council review (3 independent models) recommended expanding beyond LIST IT / BUILD IT. Six action types, each routing to a different team:

| Alert | Definition | Team | Priority |
|-------|-----------|------|----------|
| 📢 **LIST IT** | SKU exists internally, not live where it should be | Marketplace ops | Immediate |
| 🔗 **COMPLETE IT** | Same design/form factor missing device-family variants (e.g., iPhone 16 PM exists but 16/Plus/Pro don't) | Marketplace ops | High |
| 🆕 **BUILD IT** | New design × form factor combination justified by cross-matrix scoring | Design/merch team | High |
| 🔧 **FIX IT** | High sessions + low conversion = listing quality problem (images, copy, pricing) | Content/CRO team | Medium |
| 🚀 **BOOST IT** | High conversion + low sessions = hidden gem that needs visibility (PPC, placement) | Advertising team | Medium |
| 🗑️ **RETIRE IT** | Velocity < 0.3x for 90+ days, consuming listing real estate | Catalog ops | Low |

---

## 4. License Obligation Layer

### Why This Matters

Major licenses have minimum guarantee (MG) advances — money committed regardless of sales. If we're behind on an MG, every unsold unit is a loss against an advance we've already paid. PULSE must prioritize designs under licenses that are behind on their obligations.

### License Portfolio (as of March 2026)

| License | Currency | MG (Total) | MG (USD) | $/Year | Term | Months Left | Status |
|---------|----------|-----------|----------|--------|------|-------------|--------|
| Warner Bros | GBP | £350,000 | $444,500 | $152,400 | Jul 2022–Jun 2025 | Expired | 💀 Evaluate renewal |
| Liverpool FC | GBP | £265,000 | $336,550 | $115,389 | Jul 2024–Jun 2027 | 15 | ✅ Covered ($128K/90d) |
| NBA | USD | $200,000 | $200,000 | $104,348 | Jan 2026–Dec 2027 | 21 | 🔴 NOT in top 20 by 90d rev |
| Arsenal FC | GBP | £138,000 | $175,260 | $44,747 | Mar 2023–Feb 2027 | 11 | ✅ Covered ($89K/90d) |
| NFL | USD | $105,000 | $105,000 | $26,809 | Apr 2022–Mar 2026 | 0 | 💀 Expiring THIS MONTH |
| WWE | USD | $100,000 | $100,000 | $48,000 | Nov 2024–Dec 2026 | 9 | ✅ Covered ($68K/90d, surging) |
| Man City FC | GBP | £75,000 | $95,250 | $32,657 | Jan 2025–Dec 2027 | 21 | ✅ Covered ($58K/90d) |
| Chelsea FC | GBP | £81,000 | $102,870 | $35,270 | Jul 2024–Jun 2027 | 15 | ✅ Covered ($37K/90d) |
| AC Milan | EUR | €57,000 | $61,560 | $21,106 | Jul 2024–Jun 2027 | 15 | ⚠️ Needs audit |
| Peanuts | GBP | £50,000 | $63,500 | $33,130 | Jan 2025–Dec 2026 | 9 | ✅ #1 brand ($184K/90d) |
| FC Barcelona | EUR+USD | €45K+$30K | $78,600 | $26,949 | Jul 2024–Jun 2027 | 15 | ✅ Covered ($50K/90d) |
| Newcastle | GBP | £33,500 | $42,545 | $22,197 | Jul 2024–Jun 2026 | 3 | 🔴 Expiring Jun 2026 |
| Tottenham | GBP | £35,000 | $44,450 | $14,817 | Mar 2025–Mar 2028 | 24 | ✅ OK ($35K/90d) |
| Juventus | EUR | €35,000 | $37,800 | $19,722 | Jul 2025–Jun 2027 | 15 | ⚠️ Not started yet |
| West Ham | GBP | £24,000 | $30,480 | $10,450 | Apr 2023–Mar 2026 | 0 | 💀 Expiring THIS MONTH |
| Shelby | USD | $27,500 | $27,500 | $8,684 | Apr 2023–Jun 2026 | 3 | 🔴 Expiring Jun 2026 |
| Aston Villa | GBP | £20,000 | $25,400 | $8,709 | Jan 2025–Dec 2027 | 21 | ✅ OK ($19K/90d) |
| IMG College | USD | $11,350 | $11,350 | $12,382 | Jan 2026–Dec 2026 | 9 | ⚠️ Needs audit |
| Cobra Kai | USD | $10,000 | $10,000 | $5,217 | Jul 2024–Jun 2026 | 3 | 🔴 Expiring Jun 2026 |
| Naruto | USD | $8,991 | $8,991 | $3,720 | Jan 2025–Jun 2027 | 15 | ✅ Massive ROI ($87K/90d) |
| Dragon Ball | GBP | £5,000 | $6,350 | $3,313 | Apr 2024–Mar 2026 | 0 | 💀 Expiring THIS MONTH |

### License Urgency Score

```
license_urgency = mg_remaining / months_remaining
current_pace = trailing_90d_revenue × 4 (annualized)
gap_ratio = license_urgency / (current_pace / 12)

If gap_ratio > 1.5 → 🔴 BEHIND — boost ALL designs under this license
If gap_ratio 0.8–1.5 → ⚠️ WATCH — normal scoring with slight boost
If gap_ratio < 0.8 → ✅ AHEAD — normal scoring
```

**Impact on PULSE scoring:** The license urgency multiplier gets applied on top of the base opportunity score. An NBA design with a moderate velocity score still gets elevated to high priority because we're behind on a $200K advance.

---

## 5. Q1 — Channel Gaps (LIST IT + COMPLETE IT)

> "This SKU exists and is selling. Why isn't it on every channel?"

### 📢 LIST IT
SKU is live on Amazon, not on other channels. Pure distribution gap.

### 🔗 COMPLETE IT
Design exists in a form factor on one device but not across the full device family (e.g., iPhone 16 Pro Max but not 16/Plus/Pro).

**Output example:**
```
📢 LIST IT: HDMWH-WWE (Desk Mats)
VELOCITY: 🚀 2.1x | CONVERSION: 4.2% | LICENSE: WWE (✅ covered)
  ✅ Amazon US    ❌ Walmart    ❌ Target+    ❌ GoHeadCase
EST. GAP: $45,000–$65,000/quarter

🔗 COMPLETE IT: HB6CR-West Ham (Armour Gel)
VELOCITY: 🚀 3.2x | LICENSE: West Ham (💀 EXPIRING — maximize before Mar 31)
  ✅ iPhone 16 Pro Max    ❌ iPhone 16 Pro    ❌ iPhone 16    ❌ iPhone 16 Plus
EST. GAP: $12,000/quarter
```

---

## 6. Q2 — New Product Opportunity Engine (BUILD IT)

> "Given everything we know about what sells, what converts, and what gets traffic — what should we be building next?"

### 6.1 Three Leaderboards

**Leaderboard 1: Revenue** (BQ Orders — what's selling)
- Design × product type × device, ranked by revenue, velocity ratio, AOV

**Leaderboard 2: Conversion** (Amazon Sessions — what converts)
- Same dimensions, ranked by conversion rate, Buy Box %, conversion trend

**Leaderboard 3: Sessions/Demand** (Amazon Traffic — what gets eyeballs)
- Same dimensions, ranked by session volume, session trend

### 6.2 Weighted Opportunity Score

```
OPPORTUNITY_SCORE = (
    revenue_velocity   × 0.30  +
    conversion_rate    × 0.25  +
    session_volume     × 0.20  +
    aov                × 0.15  +
    trend_direction    × 0.10
) × license_urgency_multiplier
```

### 6.3 Cross-Leaderboard Matrix

Rows = designs (ranked by composite score). Columns = product types × devices.
Each cell = { revenue, velocity, conversion, sessions, EXISTS on Amazon? }

**Primary existence check: Amazon Active Listings (3.44M SKUs).**
- LIVE on Amazon → score with actual performance
- In BC catalog but NOT on Amazon → 📢 LIST IT
- Not in any system → 🆕 BUILD IT (score the gap)

### 6.4 Gap Cell Scoring

When a cell is empty (not live on Amazon), estimate opportunity:
1. **Design signal** — performance across all form factors it IS live in (40%)
2. **Form factor signal** — performance across all designs in this product type (30%)
3. **Analog match** — closest existing combination's actual performance (20%)
4. **Device applicability** — does this form factor apply to this device? (10%)

### 6.5 Drill-Down Reports

Each top opportunity gets a detailed report:
- Why this design (velocity, conversion, sessions evidence)
- Why this form factor (growth rate, AOV, category performance)
- Analog evidence (similar combos that worked)
- License obligation context (MG status, urgency)
- Proposed product list with device matrix and revenue estimates

---

## 7. Q3 — Optimization Alerts (FIX IT + BOOST IT)

### 🔧 FIX IT
High sessions + low conversion = listing quality problem.
- Sessions > 500/month AND conversion < 2% AND Buy Box > 80%
- Action: audit images, title, bullets, pricing. Don't expand until fixed.

### 🚀 BOOST IT
High conversion + low sessions = hidden gem.
- Conversion > 5% AND sessions < 200/month
- Action: increase PPC spend, improve placement, add to brand store.

### 🗑️ RETIRE IT
Velocity < 0.3x for 90+ days.
- Consuming listing real estate that could go to surging designs.
- Action: delist from secondary channels, keep on Amazon only if still generating any revenue.

---

## 8. Closed-Loop Tracking

Every PULSE alert that gets acted on enters the feedback loop:

| Field | Description |
|-------|------------|
| `alert_id` | Unique alert identifier |
| `alert_type` | LIST IT / COMPLETE IT / BUILD IT / FIX IT / BOOST IT / RETIRE IT |
| `design_code` | Design acted on |
| `predicted_quarterly_revenue` | PULSE's estimate at time of alert |
| `action_date` | When the listing/product was created |
| `actual_30d_revenue` | Actual revenue after 30 days |
| `actual_60d_revenue` | Actual revenue after 60 days |
| `actual_90d_revenue` | Actual revenue after 90 days |
| `hit_rate` | Actual ÷ predicted (>0.8 = hit, <0.5 = miss) |

Monthly calibration: update scoring weights based on actual hit rates across alert types. Win/loss reports: "Of 25 LIST IT alerts acted on, 18 beat prediction, 4 met, 3 missed."

---

## 9. Data Sources

Three inputs.

### Source 1: BigQuery Orders (Velocity Engine)
- **Location:** `instant-contact-479316-i4.zero_dataset.orders`
- **Records:** 2,802,015 orders (2019-12 → 2026-03-09, LIVE)
- **Key columns:** `custom_label` (parseable), `paid_date`, `total_sale`, `currency`, `net_sale_usd`, `marketplace`
- **Pre-parsed:** `design_code`, `device_code`, `product_type_code`, `design_variant`
- **Daily sync:** BQ → Supabase at 2:00 AM ET (21-day lookback)

### Source 2: Amazon Active Listings (Existence Matrix + ASIN→SKU Bridge)
- **File:** `Active+Listings+Report_03-05-2026.txt` (6.4GB, tab-delimited)
- **Records:** 3,441,323 active SKUs (ALL FBM)
- **Key columns:** `seller-sku`, `asin1`, `item-name`, `price`, `quantity`
- **SKU format:** Parseable — e.g., `HTPCR-IP16PM-HPOTDH37-MAT`
- **ASIN→SKU bridge:** Maps every ASIN to our internal SKU taxonomy
- **Status:** Downloaded to Mac Studio ✅. Not yet loaded to Supabase/BQ.

### Source 3: Amazon Business Report by Child ASIN (Behavioral Layer)
- **File:** `BusinessReportbychildAmazonUS_Jan1_Feb24 1.xlsx` (8MB)
- **Records:** 80,001 rows (Jan 1 – Feb 24, 2026)
- **Key columns:** Parent ASIN, Child ASIN, SKU, Sessions, Page Views, Buy Box %, Units Ordered, Conversion Rate, Revenue

### Source 4: License Obligations
- **File:** `Royalty_Advance_summary.xlsx`
- **Records:** 37 licenses with MG amounts, terms, currencies
- **Purpose:** License urgency multiplier for scoring

### How They Connect

```
BigQuery Orders (2.8M)          Amazon Child ASIN Report (80K)
  ├─ design_code                  ├─ SKU (parsed)
  ├─ product_type_code            ├─ sessions + conversion
  ├─ device_code                  ├─ Buy Box %
  ├─ revenue + velocity           └─ page views
  └─ AOV                    
          │                              │
          ▼                              ▼
     LEADERBOARD 1              LEADERBOARDS 2 + 3
     (Revenue)                  (Conversion + Sessions)
          │                              │
          └──────────┬───────────────────┘
                     ▼
          WEIGHTED OPPORTUNITY SCORE
                     │
                     ▼
        × LICENSE URGENCY MULTIPLIER
                     │
                     ▼
        Amazon Active Listings (3.44M)
        "Is this combination live?"
              │            │
           YES (LIVE)    NO (GAP)
              │            │
         Score actual    Score predicted
         performance     opportunity
              │            │
              ▼            ▼
     FIX IT / BOOST IT   LIST IT / BUILD IT / COMPLETE IT
```

---

## 10. Build Sequence — PULSE Dashboard (Codex)

### Tech Stack
- **Framework:** Next.js + React + TypeScript + Tailwind (same as Sales Dashboard V2)
- **Data:** Supabase (postgres) + BigQuery (read-only)
- **Deploy:** Vercel
- **Builder:** Codex CLI (GPT-5.3, FREE via ChatGPT OAuth)

### Dashboard Pages

**1. Velocity Overview** — All designs ranked by velocity ratio, color-coded by signal tier (surging/accelerating/steady/declining/dying). Filterable by license, product type, device.

**2. LIST IT Alerts** — Surging SKUs with channel gaps. Table: design, velocity, conversion, channels (checkmarks), license status, est. gap revenue. Sortable, filterable.

**3. COMPLETE IT Alerts** — Device family gaps for surging designs. Shows which family members are missing.

**4. BUILD IT Matrix** — The cross-leaderboard matrix. Rows = top designs, columns = product types. Cells show score + revenue/conversion/sessions. Gap cells highlighted with opportunity score. Click to drill down.

**5. BUILD IT Drill-Downs** — Individual opportunity reports with design evidence, form factor evidence, analog evidence, license context, proposed product list.

**6. FIX IT / BOOST IT** — Optimization alerts. High sessions + low conversion (FIX IT). High conversion + low sessions (BOOST IT).

**7. License Dashboard** — All licenses with MG, current run rate, gap ratio, months remaining. Color-coded urgency. Links to all alerts for that license.

**8. Tracking** — Closed-loop feedback. Actions taken, predicted vs actual revenue, hit rates, weight calibration history.

---

## 11. Success Metrics

| Metric | Target | When |
|--------|--------|------|
| Identify ≥10 surging designs with channel gaps | LIST IT alerts | Week 1 |
| Identify ≥10 new product opportunities | BUILD IT alerts | Week 1 |
| Revenue gap quantified per design | Est. quarterly $ | Week 1 |
| NBA 90d revenue audit | Determine gap vs $200K MG | Week 1 |
| Walmart SKU push list (ranked) | Top 100 | Week 2 |
| First new listings live from PULSE | Measurable | Week 3 |
| Closed-loop tracking operational | Actions logged | Week 3 |
| Revenue uplift from PULSE-driven actions | Tracked | Month 2 |

---

*v3.1 by Ava | 2026-03-09*  
*"PULSE tells you what's selling that you haven't listed everywhere, what you haven't built in every form factor, and which licenses are bleeding money while you wait. Everything else is noise."*
