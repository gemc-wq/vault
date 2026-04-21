# Project Shape: Priority Zero — Shipping Template Conversion Automation

**Date:** 2026-04-11 | **Owner:** Ava | **Status:** SHAPING COMPLETE (Cem Approved)

---

## Problem Statement

**Current state:** When new Amazon listings are created, they default to "Standard" shipping template (slow delivery, 5-7+ days). A Philippines fulfillment script is supposed to convert them to "Reduced Shipping" (US, 2-day) or "Prime" (UK, nationwide) — but the script times out and fails, leaving ~15% of listings orphaned on slow delivery templates.

**Impact:** Each listing on Standard template vs Reduced loses 2-4% conversion lift. Current gap: 502K SKUs × 2% missed conversion × ~$15 AOV = **$37.5K/month revenue loss** (or **$450K/year**).

**Why it matters:** Shipping delivery time directly correlates to conversion. Customers see 2-day vs 5-7 day and abandon cart.

---

## Scope

### IN SCOPE

1. **Automated daily cron** to identify and fix listings not on correct shipping templates
   - Query Active Listings Report
   - Match against rules engine (design tier, inventory, geography)
   - Call Amazon SP-API to update templates
   - Retry on failure with exponential backoff
   - Log results + alert on failures

2. **Opportunity Finder dashboard** to visualize conversion health
   - Scorecard: Overall compliance % (target 100%)
   - Opportunity pipeline: Which SKUs should be converted, ranked by revenue impact
   - Drill-down views: By product type, device, design, model combo
   - Conversion velocity tracking: Daily progress toward 100%

3. **Rules engine** to determine which SKUs are eligible for conversion
   - Design tier (top 500 designs US, top 300 UK = immediate priority)
   - Inventory status (FBA > FBM)
   - Fulfillment capability (can ship 2-day?)
   - Geography (US = Reduced, UK = Prime)
   - Conditional logic (FBM with 2-day capability = convert)

4. **Before/after metrics** to track revenue impact
   - Conversion rate by template type (Standard vs Reduced vs Prime)
   - Monthly revenue lift realized
   - Which designs benefited most from conversion

### OUT OF SCOPE

- Manual template editing (cron does it automatically)
- Building the inventory module (Harry's responsibility)
- Rewriting the Philippines fulfillment script (we're replacing it)
- Regional expansion beyond US/UK (DE handled separately)
- Real-time template updates (daily cron is sufficient)

---

## Edge Cases Identified

### 1. **Inventory-Dependent Conversions**
**Edge case:** Can't mark item as Reduced Shipping if it's out of stock (no inventory to ship).

**How we handle it:**
- Rules engine checks inventory status before conversion
- Skip out-of-stock items, retry in 24h when restocked
- Once Harry delivers inventory module, refine this logic

**Current limitation:** Until inventory data available, use design tier as proxy (if top-500 design, assume stock)

---

### 2. **FBM with Mixed Fulfillment Capability**
**Edge case:** FBM (seller-fulfilled) item can ONLY go to Reduced Shipping if seller can actually ship 2-day. Some of our FBM items are slow (7-10 days).

**How we handle it:**
- Rule: IF inventory_type = FBM AND can_2day_ship = FALSE THEN skip (leave on Standard)
- This requires fulfillment capability data (Harry's inventory module)
- Fallback: Only convert FBA items until inventory module ready

**Timeline:** Phase 1 (Apr 11-20) → FBA only. Phase 2 (Apr 25+) → Add FBM conditionals.

---

### 3. **License-Specific Rules**
**Edge case:** Some designs have license restrictions that affect shipping eligibility.

**Example:**
- NFL (expired Mar 31): Should NOT be on Reduced (license ending, don't over-invest)
- NBA: CAN be on Reduced (active license, high revenue)
- Shelby (AC): CAN be on Reduced (active, niche market)

**How we handle it:**
- Rules engine checks license status first
- Skip items for expired licenses (put on Standard)
- Prioritize items for active licenses

**Timeline:** Build into Phase 1 rules.

---

### 4. **Bulk Conversion Timeouts (SP-API Rate Limits)**
**Edge case:** If we try to convert 502K SKUs at once, Amazon SP-API will rate-limit or timeout.

**How we handle it:**
- Batch size: 100 items per API call
- Rate limit: 5 calls per second (respect Amazon's limits)
- Retry logic: 3x exponential backoff on 429/5xx errors
- Spread conversions over time: Daily cron converts ~1-5% of gap, eventually reaching 100%

**Timeline:** Phase 1 (Apr 11-20) → Set up rate limiting. Monitor success rate daily. Adjust batch size if needed.

---

### 5. **Listing Already on Correct Template**
**Edge case:** Some listings may already be on Reduced/Prime template. Cron shouldn't re-update them (wastes API quota).

**How we handle it:**
- Query Active Listings Report includes current template status
- Filter: Only update items where template != target_template
- Reduces API load and prevents unnecessary updates

---

### 6. **SP-API Authentication Token Expiry**
**Edge case:** Amazon refresh token could expire mid-batch.

**How we handle it:**
- Cron checks token validity at start of job
- If expired, refresh using client credentials
- Log token refresh events for monitoring

**Timeline:** Implement in Phase 1.

---

### 7. **New Listings Arriving Faster Than We Can Convert**
**Edge case:** New listings created daily. If conversion rate < new listing rate, gap grows.

**How we handle it:**
- Monitor daily: New listings created vs converted
- If gap is growing, escalate frequency (cron twice daily instead of once)
- Target: 100% of new listings hit Reduced within 24 hours of creation

**Timeline:** Phase 1 (daily cron). Phase 2 (if needed, 2x daily).

---

### 8. **Dashboard Showing Stale Data**
**Edge case:** Active Listings Report is weekly. Dashboard could show outdated conversion status.

**How we handle it:**
- Dashboard shows "Last Updated: [DATE]" clearly
- Cron also pushes daily delta updates to dashboard API (don't wait for full weekly report)
- Update Opportunity Pipeline in real-time (X items converted today)

---

## High-Level Architecture

### Layer 1: Rules Engine (YAML Configuration)

```yaml
regions:
  US:
    reduced_shipping:
      design_tiers:
        top_500: "IMMEDIATE"  # convert ASAP
        top_501_1000: "THIS_WEEK"
        others: "NEXT_WEEK"
      inventory_types:
        FBA: "eligible"
        FBM: "conditional" # only if can_2day_ship = true
      licenses:
        active: "eligible"
        expired: "skip"

  UK:
    prime_nationwide:
      design_tiers:
        top_300: "IMMEDIATE"
        others: "THIS_WEEK"
      inventory_types:
        FBA: "eligible"
        FBM: "conditional"
```

---

### Layer 2: Automated Conversion Cron (Codex)

```
Daily at 11 PM (after inventory sync):
  1. Query Active Listings Report (weekly, or manual if Cloud Run not ready)
  2. For each SKU not on target template:
     a. Check rules engine (design tier, inventory, license)
     b. If eligible → queue for conversion
  3. Call Amazon SP-API in batches (100 items, 5 req/sec)
  4. Retry failed conversions (3x exponential backoff)
  5. Log results (converted, failed, retried)
  6. Push daily delta to dashboard API
  7. Alert if success rate < 90%
```

---

### Layer 3: Opportunity Finder Dashboard (Forge)

```
Views:
  1. Compliance Scorecard
     - % on Reduced/Prime (target 100%)
     - % on Standard (target 0%)
     - Items converted today/week
     - Revenue impact

  2. Opportunity Pipeline
     - Ranked by design (which designs need work)
     - Ranked by revenue impact
     - By priority tier (IMMEDIATE, THIS_WEEK, NEXT_WEEK)

  3. Conversion Velocity
     - Daily conversions trending toward 100%
     - Failed conversions (needs retry)
     - Why items couldn't convert (inventory, license, etc.)

  4. Before/After Revenue
     - Conversion rate by template
     - Monthly revenue uplift from conversions
     - Which designs benefited most
```

---

### Layer 4: Monitoring & Alerts

```
Daily checks:
  - Cron success rate (should be >90%)
  - API errors (429s, 5xxs, timeouts)
  - Compliance trend (should be rising toward 100%)

Alerts (via Slack):
  - If success rate drops below 90%
  - If new listings arriving faster than we convert
  - If license changes affect conversion eligibility
```

---

## Success Metrics

| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| **Compliance Rate** | 85% | 100% | By end of Apr 2026 |
| **Conversions/Day** | 0 (broken script) | ~2K SKUs | First week of cron |
| **Cron Success Rate** | N/A | >95% | Consistent after Phase 1 |
| **Days to Full Compliance** | N/A | <30 days | By May 11 |
| **Revenue Lift** | $37.5K/mo loss | +$50-100K/mo gain | By May 2026 |
| **Dashboard Adoption** | No visibility | Weekly review by Cem | By Apr 25 |

---

## Dependencies / Blockers

### Blocker 1: Inventory Module (Harry)
**What:** Rules engine needs `inventory_status`, `fulfillment_capable`, `days_to_stock` columns.

**Impact:** Phase 1 uses approximations (design tier only). Phase 2 uses real inventory data.

**Timeline:** 
- Phase 1 (Apr 11-20): Build without inventory, works for FBA
- Phase 2 (Apr 25+): Integrate inventory, enable conditional FBM conversions

**Mitigation:** Start now with FBA-only rules. Expand when inventory ready. No hard blocker.

---

### Blocker 2: Cloud Run Amazon Reports API (Drew / Engineering)
**What:** Cloud Run service doesn't have Amazon SP-API integrated yet.

**Impact:** Currently, Active Listings Report downloaded manually Friday. If Cloud Run ready, could auto-download weekly.

**Timeline:**
- Phase 1 (Apr 11-20): Use manual downloads (Cem downloads Friday 5 PM)
- Phase 2 (May): Build Cloud Run integration (3-5 days) if needed

**Mitigation:** Manual downloads work fine for weekly cron. No blocker.

---

### Blocker 3: Amazon SP-API Marketplace Credentials (Drew / Merchant Token)
**What:** SP-API needs tokens for US, UK, DE marketplaces.

**Current status:** US token confirmed. UK/DE tokens need verification.

**Impact:** Phase 1 = US only. Phase 2 = Add UK, DE.

**Timeline:**
- Phase 1 (Apr 11-20): US only
- Phase 2 (May): UK + DE once tokens verified

**Mitigation:** Start with US (biggest revenue). Expand soon.

---

## Notes & Open Questions

### Q1: How fast can we convert?
**Rate limit:** Amazon SP-API allows ~5 requests/second. With 100 items per batch = 500 items/second theoretically. Realistic: 1-2K items/hour (accounting for retries, network latency).

**Gap to close:** 502K SKUs. At 1K/hour × 24 hours = 24K/day. So 502K / 24K = ~21 days to full compliance.

**Timeline is realistic.** Could be faster if we run cron 2x/day or increase batch size.

### Q2: What if SP-API fails mid-batch?
**Answer:** Retry logic handles it. Exponential backoff (2s, 4s, 8s). If still fails after 3 retries, log and move on. Next day's cron will retry.

### Q3: Do we need Shipping Compliance Center as Phase 0 or Phase 1?
**Answer:** Phase 0. Shipping is P0 because it's $37.5K/month loss. Get cron + dashboard running ASAP (Apr 15-20). Other dashboard views (device coverage, FBA opportunities) can follow (Apr 20+).

### Q4: Should cron run once daily or 2x/day?
**Answer:** Start with once daily (11 PM). Monitor completion rate. If < 95%, increase to 2x/day (11 PM + 2 AM). Adjust based on results.

### Q5: How do we handle regional differences in shipping templates?
**Answer:** Rules engine has separate config per region (US = Reduced, UK = Prime, DE = different rules). Cron queries Active Listings by region, applies regional rules.

---

## Shaping Sign-Off

- [x] **Cem reviewed and approved** (Apr 11, 7:40 AM EDT)
- [x] **Ava incorporated edge case feedback** (this document)
- [x] **Architecture reviewed by Advisor tool** (Opus 4.6)
- [x] **Ready to move to planning phase**

---

**Status:** SHAPING COMPLETE ✅ | **Next Phase:** PLANNING (move to `PROJECT-PLAN-SHIPPING-TEMPLATE.md`)

