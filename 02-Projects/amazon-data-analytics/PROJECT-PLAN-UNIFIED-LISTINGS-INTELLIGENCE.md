# Project Plan: Unified Listings Intelligence Dashboard & Bulk Operations

**Date:** 2026-04-11 | **Owner:** Ava | **Status:** PLANNING | **Approved by:** Cem

---

## Reference Shape Document

**PROJECT-SHAPE-UNIFIED-LISTINGS-INTELLIGENCE.md** — Five unified gap dimensions with Stage 1-3 phasing.

**ADVISOR-REVIEW-UNIFIED-LISTINGS-INTELLIGENCE.md** — Architecture approved by Opus 4.6. Sequential phasing, single-table SQLite, boolean flags.

---

## Nine Core Deliverables (From Cem's Priority List)

Cem identified 9 distinct deliverable areas. This plan addresses each explicitly.

### 1️⃣ **Incorrect Shipping Templates**
- What's missing "Nationwide Prime" (UK) or "Reduced Shipping" (US)
- Dashboard view: Shipping Compliance Scorecard + heatmap (device × design)
- Automation: Codex cron for bulk SP-API updates
- **Priority:** CRITICAL (P0) — $37.5K/month revenue loss
- **Owner:** Codex (executor) + Forge (dashboard)

### 2️⃣ **Listing Gap Analysis for Champions**

**2a) Top Elbow Device Models from PULSE**
- Which champion designs are missing variants for top devices?
- Use PULSE elbow logic to identify priority devices per design
- Example: NARUTO elbows at iPhone 17, 16. Missing variants for those = gap.
- Dashboard: Device Coverage Heatmap
- **Owner:** Hermes (PULSE data) + Forge (visualization)

**2b) Listing Gap by Product Type**
- Best-selling HTPCR devices missing listings in HB401 or HLBWH
- Cross-product-type analysis: "iPhone 17PM sells 1,000 units/month in HTPCR. Missing in HB401 = $20K opportunity"
- Dashboard: Product Type Breakdown view
- **Owner:** Hermes (sales data) + Forge (viz)

**2c) Listing Gap by Champion Designs**
- Using PULSE elbow logic to define champion designs
- Which champions missing which devices/regions?
- Dashboard: Champion Design Gap Leaderboard (sorted by revenue impact)
- **Owner:** Hermes (PULSE) + Forge (dashboard)

### 3️⃣ **PH Listings Team EOD Comparison to Actual Listings**
- Daily: PH team reports "listed X items today"
- Actual: Query Active Listings Report for daily delta
- Compare: Did items actually go live? Any delays?
- Feedback loop: Alert PH if items not showing live after 6h
- Slack integration: Automated EOD comparison post to #eod-listings
- **Owner:** Codex (daily delta check) + Slack automation
- **Status:** Slack digest exists, expand to compare PH reported vs actual

### 4️⃣ **Listings with Blockers**
- Identify listings with issues that need fixing:
  - Suppressed (why? inventory issue? compliance issue?)
  - Missing images (from S3 CDN)
  - Pricing errors (below cost?)
  - Incorrect categories
  - Malformed data (SKU parsing fails)
- Dashboard view: Blockers Report (ranked by impact)
- Action: Output to task queue (Cem, PH team)
- **Owner:** Codex (detection) + Forge (dashboard)

### 5️⃣ **Cross-Regional Gaps & Market Behavior Differences**
- Which designs sell well in UK but not US (and vice versa)?
  - Example: Sports teams (#1 in UK, not top 100 in US)
  - Example: iPhone 17 top device in US, iPhone 16 top in EU
- Patterns: Why the differences? (licensing? pricing? shipping? regulatory?)
- Dashboard: Cross-Region Heatmap + analysis
- Action: List designs in new regions, adjust pricing, etc.
- **Owner:** Hermes (sales data by region) + Forge (viz)

### 6️⃣ **Sales Traffic Analysis Dashboard** (Two Branches)

**6a) FBA/Prime Conversion Opportunities**
- Which listings on FBM should move to FBA?
- FBA conversion lift: 2-4% on average, higher on certain devices
- Candidate filter: High velocity + feasible to move to FBA (size/weight/margin)
- Dashboard: FBA Migration Leaderboard
- **Owner:** Hermes (sales velocity) + Codex (eligibility check)
- **Blocker:** Harry's inventory module (FBA capability)
- **Fallback:** Use F-prefix (FSKU = FBA) as proxy

**6b) Other Platforms & Microsites Gap Analysis**
- Which top-selling designs on Amazon missing from Shopify/Target/Walmart?
- Example: NARUTO sells 1K units/month on Amazon. Missing from Walmart = $50K/month opportunity
- Dashboard: Platform Coverage Matrix (design × platform)
- **Owner:** Hermes (sales data) + Loom (competitor research on other platforms)
- **Note:** Partially covered by PULSE Champions analysis

### 7️⃣ **Conversion/Sales Analytics to Identify Gaps**
- Revenue by design × device × region × fulfillment type
- Identify underperformers: "Why is NARUTO converting at 2% on iPhone 16 but 5% on iPhone 17?"
- **Already covered by:** Conversion Dashboard + PULSE
- **Integration:** Reference existing dashboards, don't duplicate
- **Owner:** Hermes (PULSE) — ensure Listings Intelligence feeds back to PULSE findings

### 8️⃣ **Automated Feedback Loop & PH Team Tracking**
- Slack integration: Daily EOD update (#eod-listings, #eod-creative-graphics)
- Assigned tasks: Track items assigned to PH team, follow up on progress
- Auto-escalation: If task unresolved after 5 days, flag to Cem
- Blueprint V3 integration: Actions from Listings Intelligence feed into Blueprint (strategy document)
- **Owner:** Codex (daily checks) + Slack automation
- **Status:** Slack digest already exists, expand it

### 9️⃣ **Self-Learning Loop (Hermes/Gemini 4) & New License/Design Gap Analysis**
- Hermes (Operations Librarian) or Gemini 4 self-manages listings based on feedback
- New license launches (e.g., One Piece, upcoming Football 2026, iPhone 18 rollout)
- New design/model gap reports: "One Piece launched, missing on 30 devices — create variants"
- Seasonal/event-driven: "Samsung S26 launches next month — prepare gap analysis"
- **Owner:** Hermes (trigger detection) + Codex (gap analysis generation)
- **Timeline:** Post-Stage 2. Requires self-improving skill loop.

### 1️⃣0️⃣ **Amazon Ads Plan (Bonus)**
- Once Listings Intelligence identifies gaps, Amazon Ads can:
  - Add/remove items from ad campaigns based on listing gaps
  - Identify search terms with high traffic but missing listings
  - Auto-pause ads for suppressed items
- **Blocker:** Amazon Ads API access (Drew/engineering)
- **Timeline:** Post-Stage 2, if Ads API available
- **Owner:** Atlas (ads analyst) + Codex (API integration)

---

## Task Breakdown: Three Stages

### STAGE 1: Unified BI Tool (Apr 15-May 5, 3 weeks)

#### Data Pipeline (Codex)

| Task | Owner | Duration | Dependencies | Status |
|------|-------|----------|--------------|--------|
| Build SQLite schema (listings_full) | Codex | 2 days | None | Ready |
| Load Active Listings Report (weekly) | Codex | 1 day | AWS S3 access | Ready |
| Load BQ orders (sales velocity by SKU) | Codex | 1 day | BQ credentials | Ready |
| Load PULSE leaderboard (champions + elbow) | Hermes | 2 days | PULSE data export | Ready |
| Compute all 5 gap dimensions | Codex | 3 days | Schema + data | Ready |
| Index queries (device, design, region) | Codex | 1 day | SQLite | Ready |
| **Total** | | **10 days** | | |

#### Dashboard Frontend (Forge)

| Task | Owner | Duration | Dependencies | Status |
|------|-------|----------|--------------|--------|
| Design dashboard layout (5 views) | Forge | 2 days | Wireframes (Ava) | Ready |
| Build View 1: Executive Summary | Forge | 2 days | Schema finalized | Ready |
| Build View 2: Gap Explorer | Forge | 3 days | Schema finalized | Ready |
| Build View 3: Pattern Heatmaps | Forge | 3 days | Recharts integration | Ready |
| Build View 4: Impact Dashboard | Forge | 2 days | Sales data | Ready |
| Build View 5: Execution Pipeline (stub) | Forge | 1 day | UI framework | Ready |
| Deployment + styling | Forge | 2 days | Next.js setup | Ready |
| **Total** | | **15 days** | | |

#### Integrations (Stage 1 Minimal)

| Task | Owner | Duration | Dependencies | Status |
|------|-------|----------|--------------|--------|
| Verify Active Listings data schema | Codex | 1 day | S3 access | Ready |
| Verify BQ orders schema | Hermes | 1 day | BQ query | Ready |
| Verify PULSE export format | Hermes | 1 day | PULSE | Ready |
| **Total** | | **3 days** | | |

#### Testing & QA (Stage 1)

| Task | Owner | Duration | Success Criteria | Status |
|------|-------|----------|------------------|--------|
| Dashboard loads <2s | Forge | 1 day | Load time <2s on 3.5M rows | Ready |
| Five dimensions visible + accurate | Ava | 2 days | Spot-check 10 designs manually | Ready |
| Patterns are clear (heatmaps legible) | Ava | 1 day | Cem can see patterns visually | Ready |
| Revenue calculations correct | Hermes | 1 day | Spot-check SKU → revenue mapping | Ready |
| Data freshness acceptable | Codex | 1 day | Weekly refresh sufficient | Ready |
| **Total** | | **6 days** | | |

**Stage 1 Timeline:** Apr 15 (Mon) → May 5 (Mon). 3 weeks.

**Stage 1 Deliverable:** 
- SQLite database with all 5 gap dimensions
- Dashboard with Views 1-4 (read-only, no execution)
- Weekly data refresh cron
- Shipping Compliance Scorecard live

---

### STAGE 2: Execution Engine & Integrations (May 5-25, 3 weeks)

#### Per-Dimension Executors

**2a) Shipping Template Updates (Codex)**

| Task | Duration | Dependencies | Status |
|------|----------|--------------|--------|
| Build execution queue table | 1 day | Schema | Ready |
| Implement SP-API batch update logic | 2 days | SP-API credentials | Ready |
| Retry logic (3x exponential backoff) | 1 day | Error handling | Ready |
| Rate limiting (100 items/batch, 5 req/sec) | 1 day | Batch logic | Ready |
| Execution log + monitoring | 1 day | Logging framework | Ready |
| Cron job (daily 11 PM) | 1 day | Scheduler | Ready |
| Test on 100-item batch (staging) | 1 day | SP-API sandbox | Ready |
| **Total** | **8 days** | | |

**2b) Device Coverage Gaps (Output to PULSE)**

| Task | Duration | Dependencies | Status |
|------|----------|--------------|--------|
| Identify missing variants (design × device) | 1 day | Gap detection logic | Ready |
| Calculate revenue opportunity per gap | 1 day | Sales velocity data | Ready |
| Priority ranking (elbow logic) | 1 day | PULSE elbow data | Ready |
| Output format (CSV for PULSE import) | 1 day | PULSE schema | Ready |
| Cron job (weekly, Friday night) | 1 day | Scheduler | Ready |
| Mock PULSE API (for now) | 1 day | CSV export | Ready |
| **Total** | **6 days** | | |

**2c) Cross-Region Gaps (Output to SKU Staging)**

| Task | Duration | Dependencies | Status |
|------|----------|--------------|--------|
| Identify designs in one region not others | 1 day | Cross-region data | Ready |
| Rank by revenue impact + sales velocity | 1 day | Sales data | Ready |
| Output format (CSV for staging team) | 1 day | SKU staging schema | Ready |
| Include licensing constraints | 1 day | License data | Ready |
| Cron job (weekly) | 1 day | Scheduler | Ready |
| Mock SKU staging API (for now) | 1 day | CSV export | Ready |
| **Total** | **6 days** | | |

**2d) FBA Migration Candidates (Output to Harry)**

| Task | Duration | Dependencies | Status |
|------|----------|--------------|--------|
| Identify FBM items with high conversion potential | 2 days | Sales data + FBM current state | Blocked on Harry |
| Filter by fulfillment capability (size/weight) | 1 day | Inventory data | Blocked on Harry |
| Calculate conversion uplift per item | 1 day | Sales data | Ready |
| Output format (CSV) | 1 day | Schema | Ready |
| Mock output (for now) | 1 day | CSV export | Ready |
| **Total** | **6 days** | | Blocked |

**2e) PRUNE Dead Listings (Codex)**

| Task | Duration | Dependencies | Status |
|------|----------|--------------|--------|
| Identify old listings (pre-2025-06-01) + 0 sales in 2025 | 1 day | BQ orders query | Ready |
| Calculate fee waste (50K × $0.06/month) | 1 day | Pricing data | Ready |
| SP-API suppress operation | 2 days | SP-API capability | Ready |
| Batch suppress (100 items/batch) | 1 day | Rate limiting | Ready |
| Execution log + safety gate (Cem approval) | 1 day | Queue UI | Ready |
| Cron job (weekly) | 1 day | Scheduler | Ready |
| **Total** | **7 days** | | |

#### Dashboard Enhancements (Forge)

| Task | Duration | Dependencies | Status |
|------|----------|--------------|--------|
| Build View 5: Execution Pipeline (full) | 2 days | Queue table | Ready |
| Add "Queue for conversion" buttons | 2 days | UI framework | Ready |
| Show execution status (queued/executing/success/failed) | 2 days | Real-time updates | Ready |
| Export queue as CSV (for manual review) | 1 day | CSV library | Ready |
| Slack notifications (cron status) | 1 day | Slack webhook | Ready |
| **Total** | **8 days** | | |

#### PH Team Feedback Loop (Codex + Slack)

| Task | Duration | Dependencies | Status |
|------|----------|--------------|--------|
| Daily delta check: PH reported vs actual listings | 1 day | BQ query | Ready |
| Auto-post to #eod-listings (Slack) | 1 day | Slack API | Ready |
| Flag discrepancies (items not live after 6h) | 1 day | Alert logic | Ready |
| Cron job (daily, 8 AM & 4 PM) | 1 day | Scheduler | Ready |
| **Total** | **4 days** | | |

#### Blockers Report (Codex + Forge)

| Task | Duration | Dependencies | Status |
|------|----------|--------------|--------|
| Detect suppressed listings + reason | 1 day | Active Listings schema | Ready |
| Detect missing images (S3 CDN check) | 1 day | S3 API | Ready |
| Detect pricing errors | 1 day | Pricing rules | Ready |
| Dashboard: Blockers Report view | 2 days | UI framework | Ready |
| Output to task queue (CSV) | 1 day | Export logic | Ready |
| **Total** | **6 days** | | |

**Stage 2 Timeline:** May 5 (Mon) → May 25 (Sun). 3 weeks.

**Stage 2 Deliverables:**
- Shipping template bulk update (SP-API)
- Device coverage gap output (CSV → PULSE)
- Cross-region gap output (CSV → SKU staging)
- FBA migration candidates (CSV → Harry)
- PRUNE suppression (SP-API)
- PH EOD feedback loop (Slack)
- Blockers detection + reporting
- Full execution pipeline UI

---

### STAGE 3: Automation & Self-Learning (May 25+, Ongoing)

#### Auto-Prioritization (Codex + Advisor Loop)

| Task | Owner | Duration | Dependencies | Status |
|------|--------|----------|--------------|--------|
| Add severity scores (1-10) to all 5 dimensions | Codex | 3 days | Stage 2 complete | Post-S2 |
| ML model: Predict conversion impact from gap | Codex | 5 days | Historical data | Post-S2 |
| Dashboard: "Recommended actions" section | Forge | 2 days | Scoring system | Post-S2 |
| **Total** | | **10 days** | | |

#### Self-Learning Loop (Hermes)

| Task | Owner | Duration | Dependencies | Status |
|------|--------|----------|--------------|--------|
| New license detection (One Piece, Football 2026, iPhone 18) | Hermes | 3 days | Automation trigger | Post-S2 |
| Auto-generate gap analysis for new licenses | Hermes | 2 days | Analysis template | Post-S2 |
| Feed results back to PULSE + dashboard | Hermes | 1 day | Integration | Post-S2 |
| Cron job (daily, trigger on new event) | Hermes | 1 day | Scheduler | Post-S2 |
| **Total** | | **7 days** | | |

#### Amazon Ads Integration (Codex + Atlas)

| Task | Owner | Duration | Dependencies | Status |
|------|--------|----------|--------------|--------|
| Get Amazon Ads API access | Drew | TBD | Approval | Blocked |
| Build Ads sync logic (listings ↔ campaigns) | Codex | 3 days | Ads API | Blocked |
| Add/remove items from campaigns based on gaps | Atlas | 2 days | Sync logic | Blocked |
| Identify search terms with missing listings | Atlas | 2 days | Ads data | Blocked |
| Dashboard: Ads opportunities view | Forge | 2 days | UI | Blocked |
| **Total** | | **11 days** | | Blocked on Drew |

**Stage 3 Timeline:** Starts May 25+. Ongoing refinement.

**Stage 3 Deliverables:**
- Auto-prioritization by revenue impact
- Self-learning loop for new licenses/designs/devices
- Amazon Ads integration (if API available)

---

## Standard Operating Procedure (SOP)

### Weekly Data Refresh (Every Saturday 1 AM)

```
1. Active Listings Report downloaded (S3 → local)
2. Parse + load into SQLite (listings_full table)
3. BQ orders query (last 7 days)
4. Compute all 5 gap dimensions
5. Publish to dashboard
6. Archive raw files (delete to save space)
```

### Daily Execution (11 PM Cron)

```
1. Check shipping template queue
2. Batch shipping updates (100 items/batch, 5 req/sec)
3. Log results (success/fail by SKU)
4. Alert if success rate < 95%
5. Email summary to Cem
```

### Daily PH Feedback (8 AM & 4 PM)

```
1. Query Active Listings for daily delta
2. Compare to PH team EOD report
3. Flag discrepancies
4. Post to #eod-listings (Slack)
5. Alert if items not live after 6h
```

---

## Risk Mitigation

| Risk | Severity | Mitigation | Owner |
|------|----------|------------|-------|
| SP-API rate limits on 502K items | Medium | Batch 100, 5 req/sec, spread over 100+ days | Codex |
| Inventory module not ready (Harry) | Low | Use F-prefix proxy, refine in Stage 2.5 | Codex |
| PULSE integration blocked | Low | Output CSV, PULSE team imports manually | Hermes |
| Shipping template data incomplete | Low | Use approximations (all items eligible initially) | Codex |
| Query performance on 3.5M rows | Low | Index on (device, design, region) | Forge |
| Dashboard crashes on high load | Low | Cache summaries, pre-compute heatmaps | Forge |

---

## Success Criteria by Milestone

### Stage 1 Complete (May 5)
- ✅ Dashboard loads <2 seconds
- ✅ Five dimensions visible + accurate
- ✅ Patterns clear (heatmaps readable)
- ✅ Revenue calculations validated
- ✅ Weekly refresh working
- ✅ Cem can see all gaps in one place

### Stage 2 Complete (May 25)
- ✅ 1,000+ shipping template conversions executed (>95% success)
- ✅ Device coverage gaps output to PULSE
- ✅ Cross-region gaps output to SKU staging
- ✅ PH EOD feedback loop working
- ✅ Blockers detection + reporting live
- ✅ Cem approves queue → cron executes

### Stage 3 Complete (June 30)
- ✅ Auto-prioritization by revenue impact
- ✅ Self-learning loop for new licenses
- ✅ Amazon Ads integration (if API available)
- ✅ Weekly automated reports to Cem
- ✅ Hermes self-manages most of listings intelligence

---

## Integration Points (With Existing Systems)

### PULSE Integration
- Gap Explorer references PULSE elbow logic (champion designs)
- Device coverage gaps feed into PULSE backlog
- Output: "Create these 50 variants (sorted by PULSE sales velocity)"

### Conversion Dashboard Integration
- Reference existing conversion analytics
- Don't duplicate. Link to Conversion Dashboard for detailed analysis.

### Slack Integration
- EOD updates to #eod-listings, #eod-creative-graphics
- Daily PH comparison reports
- Cron job status alerts

### BigQuery Integration
- Sales velocity data (BQ orders table)
- Orders by sku, device, region, date
- Buyer_country for cross-region analysis

### Blueprint V3 Integration
- Actions from Listings Intelligence feed into Blueprint (strategic roadmap)
- "Create 50 variants" → task in Blueprint
- "List 45 designs in US" → task in Blueprint

---

## Team Assignments

| Area | Owner | Backup | Status |
|------|-------|--------|--------|
| **Data Pipeline** | Codex | Hermes | Ready |
| **Dashboard Frontend** | Forge | Spark | Ready |
| **PULSE Integration** | Hermes | Ava | Ready |
| **SP-API Execution** | Codex | Spark | Ready |
| **PH Feedback Loop** | Codex | Harry | Ready |
| **Slack Automation** | Codex | Harry | Ready |
| **Ads Integration** | Atlas | Codex | Blocked on Drew |
| **Self-Learning Loop** | Hermes | Atlas | Post-S3 |

---

## Timeline Summary

| Phase | Start | End | Duration | Status |
|-------|-------|-----|----------|--------|
| **Stage 1: BI Tool** | Apr 15 | May 5 | 3 weeks | Ready |
| **Stage 2: Execution** | May 5 | May 25 | 3 weeks | Ready |
| **Stage 3: Automation** | May 25 | Jun 30 | 5 weeks | Ready |
| **TOTAL** | Apr 15 | Jun 30 | 11 weeks | Ready |

---

## Budget & Resources

| Resource | Allocation | Cost Impact | Status |
|----------|-----------|-------------|--------|
| Codex (engineer) | 40% for 11 weeks | ~160 hours | Approved |
| Forge (engineer) | 40% for 6 weeks (S1-S2) | ~80 hours | Approved |
| Hermes (analyst) | 30% for 11 weeks | ~120 hours | Approved |
| Atlas (ads) | 20% for 5 weeks (S3) | ~20 hours | Blocked |
| Spark (engineer, backup) | 10% on-call | ~10 hours | Ready |
| **Total engineering** | | ~390 hours | Approved |

---

## Success = Revenue Impact

Once complete:

- **Shipping templates:** +$37.5K/month
- **Device coverage:** +$150-200K/month
- **Cross-region:** +$80-100K/month
- **FBA migration:** +$50-75K/month
- **PRUNE:** +$36K/year ($3K/month savings)
- **TOTAL:** **$300-450K/year**

---

## Next Steps (Cem Approval)

1. ✅ Approve task breakdown + timeline
2. ✅ Approve team assignments
3. ✅ Approve Stage 1 start date (Apr 15)
4. ✅ Assign backup owners (if anyone unavailable)
5. ✅ Schedule weekly syncs (Cem + team leads)
6. Ready to kick off: **Codex starts data pipeline Monday, Apr 15**

---

**Status:** PLANNING COMPLETE ✅ | **Ready to BUILD** | **Awaiting Cem approval**

