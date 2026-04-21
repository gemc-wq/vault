# Weekly Action Plan: Apr 14-18, 2026

**Owner:** Athena | **Status:** DRAFT — Awaiting Cem Approval
**Priority:** P0 — Revenue leakage is active. Every day on wrong template/price = lost money.

---

## Scorecard (Baseline — Apr 11 Snapshot)

| Metric | US | DE | Target |
|--------|----|----|--------|
| Total SKUs | 3,624,260 | 2,709,146 | — |
| Shipping compliance | **39.0%** | **32.1%** | 100% |
| SKUs on wrong template | 2,212,156 | 1,840,226 | 0 |
| Price integrity (FBA/FBM) | 97.7% (70 failures) | — | 100% |
| FBA SKUs (Prime-eligible) | 937 (0.03%) | — | TBD |
| Device coverage (Tier 1) | TBD (heatmap pending) | — | 100% |

---

## Monday Apr 14 — Shipping Template Fix (P0)

### Task 1: Confirm Shipping Template Names ⏱️ 10 min
**Owner:** Cem
**Action:** Open Seller Central → Settings → Shipping Settings → confirm:
- US correct template = "Reduced Shipping Template" (we see this in data)
- DE correct template = "Reduced Shipping Template" (same name, DE marketplace)
- Are there other valid templates besides "Nationwide Prime" (937 US SKUs)?
**Why:** We cannot run the fix without knowing which template is "right." Data shows 3 US templates: Default Amazon (61.1%), Reduced Shipping (38.9%), Nationwide Prime (0.03%).

### Task 2: Generate Shipping Template Fix File ⏱️ 30 min
**Owner:** Athena (CLI)
**Action:** From listings.db, export flat file of all 2,212,156 US SKUs currently on "Default Amazon Template" → generate SP-API compatible bulk update file
**Depends on:** Task 1 (template name confirmation)
**Output:** `output/shipping_fix_us_YYYYMMDD.tsv` — SKU + correct template name

### Task 3: Price Integrity Fix List ⏱️ 15 min
**Owner:** Athena (CLI)
**Action:** Export all 70 FBA pricing failures with correct target prices
**Output:** `output/price_fix_YYYYMMDD.tsv` — SKU, current FBA price, correct FBA price (FBM + $6)
**Approval:** 🔴 Cem must approve before any price change executes

---

## Tuesday Apr 15 — Execute Fixes + Build Delta

### Task 4: Execute Shipping Template Bulk Update
**Owner:** PH Team (via Jay Mark) OR Blueprint middleware
**Action:** Upload shipping fix file via Seller Central bulk upload or SP-API
**Volume:** 2,212,156 SKUs — may need batching across multiple uploads
**Approval:** 🟡 Athena generates, Cem approves execution method
**Note:** If SP-API route (Blueprint middleware), Jay Mark needs to confirm Product Listing scope is enabled

### Task 5: Execute Price Corrections
**Owner:** PH Team (manual) — 70 SKUs is manageable
**Action:** Update 70 FBA listings to correct prices
**Approval:** 🔴 Cem approves final price list

### Task 6: Build Weekly Delta Script ⏱️ 2 hrs
**Owner:** Athena (CLI)
**Action:** Create `delta_compare.py` — loads two snapshots of Active Listings into SQLite, compares:
- New listings (SKU exists in new, not old)
- Removed listings (SKU in old, not new)
- Price changes (same SKU, different price)
- Template changes (same SKU, different shipping template)
- Status changes
**Output:** Delta report (HTML + JSON) appended to dashboard

---

## Wednesday Apr 16 — Coverage Analysis

### Task 7: Device × Product Type Coverage Heatmap
**Owner:** Athena (CLI) + Hermes (PULSE data)
**Action:** For top 50 designs by velocity (from PULSE), generate matrix:
- Rows = designs
- Columns = Tier 1 devices × product types (HTPCR, HB401)
- Cells = ✅ listed / ❌ gap
**Depends on:** Hermes provides champion design list from PULSE
**Output:** Coverage heatmap added to dashboard

### Task 8: Delegate Champion List to Hermes
**Owner:** Athena → Hermes (via OpenClaw ACP)
**Action:** Request top 50 designs by 90-day revenue from BigQuery/PULSE
**Format:** Design code, revenue, units, conversion rate
**Deadline:** EOD Wednesday

---

## Thursday Apr 17 — PH Delegation + Monitoring

### Task 9: Generate Next Week's Listing Queue
**Owner:** Athena (CLI)
**Action:** From coverage gaps (Task 7), generate PH work queue:
- Priority 1: Missing Tier 1 device listings for champion designs
- Priority 2: Missing HB401 variants for designs that only have HTPCR
- Priority 3: Missing FBA variants for top 20 designs
**Output:** `output/ph_listing_queue_week16.tsv`

### Task 10: Brief PH Team
**Owner:** Athena → Jay Mark (email brief)
**Action:** Send structured brief with:
- Week's listing priorities (from Task 9)
- Shipping template compliance requirement (ALL new listings on "Reduced Shipping Template")
- Price rules (FBM: $19.95 HTPCR, $21.95 HB401; FBA: +$6.00)
**Approval:** 🟡 Send then notify Cem

---

## Friday Apr 18 — Review + Cron Setup

### Task 11: Download Fresh Active Listings Report
**Owner:** Cem (Seller Central) or automated if SP-API scope allows
**Action:** Download US + DE Active Listings Reports for Apr 18
**Purpose:** Delta comparison vs Apr 10/11 baseline

### Task 12: Run First Delta + Measure Impact
**Owner:** Athena (CLI)
**Action:** Load new reports, run delta script, measure:
- How many of the 2.2M shipping template fixes were applied?
- Were all 70 price corrections made?
- Any new compliance issues introduced?
**Output:** Delta report added to dashboard

### Task 13: Set Up Weekly Cron
**Owner:** Athena (Green Zone)
**Action:** Create cron job (Gemma 4, Saturday morning):
1. Load latest Active Listings TSV → SQLite
2. Run delta comparison
3. Run shipping compliance check
4. Run price integrity audit
5. Generate updated dashboard
6. Alert Athena if any metric degrades
**Runtime:** ~10 min for full pipeline (600s timeout)

---

## Delegation Summary

| Agent | Tasks | Priority |
|-------|-------|----------|
| **Cem** | Task 1 (template names), Task 3 approval, Task 5 approval | P0 — 15 min total |
| **Athena (CLI)** | Tasks 2, 3, 6, 7, 9, 12, 13 | P0-P1 — bulk of work |
| **Jay Mark** | Task 4 (bulk upload), Task 10 recipient | P0 — needs capacity check |
| **Hermes** | Task 8 (champion list from PULSE/BQ) | P1 — data dependency |
| **PH Team** | Task 5 (70 price fixes), Task 9 queue | P0-P1 |
| **Gemma 4** | Task 13 (weekly cron) | P2 — automation |

---

## Revenue Impact (If Executed This Week)

| Fix | SKUs Affected | Est. Monthly Impact | Confidence |
|-----|---------------|-------------------|------------|
| Shipping template 39%→100% | 2,212,156 | **+$50-75K/mo** | HIGH |
| Price integrity (70 failures) | 70 | +$3-5K/mo | HIGH |
| Device coverage gaps | TBD (Task 7) | +$150-200K/mo | MEDIUM |
| **Total potential** | — | **+$200-280K/mo** | — |

*Shipping impact revised upward from $37.5K — the gap is 61% of listings, not 15%.*

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Bulk template update fails or causes listing suppression | Test on 1,000 SKUs first, verify no suppression, then batch remainder |
| SP-API Product Listing scope not enabled | Fallback: Seller Central flat file upload (slower but works) |
| Jay Mark unavailable for bulk upload | Escalate to Cem for alternative executor |
| PULSE data stale or unavailable | Use Active Listings data to rank designs by SKU count as proxy for popularity |
| Price corrections rejected by Amazon | Review rejected SKUs individually, may need content update alongside price |

---

## Success Criteria (End of Week)

- [ ] Shipping compliance US: 39% → 80%+ (stretch: 95%)
- [ ] Price integrity: 70 failures → 0
- [ ] Dashboard live with delta tracking
- [ ] Weekly cron operational
- [ ] PH team has structured queue for Week 17
- [ ] Coverage heatmap identifies top 20 gaps by revenue potential

---

**Next review:** Friday Apr 18, 17:00 ET — Athena generates weekly delta report
**Escalation:** If Task 1 (template confirmation) not done by Monday 12:00 → P0 blocker alert to Cem
