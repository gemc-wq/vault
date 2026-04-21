# Advisor Review: Unified Listings Intelligence Dashboard Architecture

**Requested by:** Cem | **Advisor:** Opus 4.6 (via Anthropic Advisor Tool) | **Date:** 2026-04-11

---

## Executive Recommendation

✅ **Unified architecture is sound.** Five dimensions in single table is the right call for MVP. Sequential phasing (Stage 1 then Stage 2) lowers risk. Inventory module is soft blocker, not hard blocker.

**Key insight from Advisor:** "The unified table design trades normalization for simplicity, which is correct for a BI tool. You're optimizing for decision-making speed, not transactional consistency."

---

## Architecture Review

### Question 1: Single Table vs Normalized Design

**Advisor recommendation:** ✅ **Single unified table for Stage 1-2.**

**Rationale:**
- MVP BI tool optimizes for **query speed** (Cem opens dashboard, sees answer in <1 second)
- Normalized schema (separate dimension tables) would require complex joins
- Single table with denormalized flags is perfect for read-heavy BI use case
- Future: If you need transactional consistency (e.g., tracking dimension changes over time), normalize then. For now: YAGNI.

**Implementation:**
```
listings_full (
  sku, design, device, region, 
  device_gap_flag, cross_region_gap_flag, shipping_gap_flag, fba_gap_flag, prune_flag,
  sales_last_90d, revenue_last_90d
)
```

**Query efficiency:** Single table scan → apply filters → rank by revenue → result. One query, < 1 second on 3.5M rows.

---

### Question 2: Boolean Flags vs Ranked Scores

**Advisor recommendation:** ✅ **Boolean flags for MVP, add scores in Stage 3.**

**Rationale:**
- Boolean flags: Easy to understand, fast to compute, sufficient for Stage 1-2
- Ranked scores: Better for auto-prioritization, but adds complexity
- MVP should be: "Device gap exists: YES/NO" 
- Stage 3 (automation): "Device gap severity: 7/10 (high revenue, needed device, ready to create)"

**Progression:**
- Stage 1-2: Boolean flags (gap exists or not)
- Stage 3: Add severity scores (1-10) for intelligent auto-prioritization

---

### Question 3: Per-Dimension Executors vs Unified Executor

**Advisor recommendation:** ✅ **Start with per-dimension executors (separate crons), unify in Stage 3.**

**Rationale:**
- Each dimension has different execution model:
  - Device gaps → Output to PULSE (no immediate action)
  - Cross-region gaps → Output to SKU staging (no immediate action)
  - Shipping gaps → Call SP-API directly (immediate action)
  - FBA gaps → Call inventory module (immediate action)
  - PRUNE → Call SP-API directly (immediate action)
- Unified executor would need logic for 5 different integration points. Complex, hard to debug.
- Per-dimension executors: Simpler, specialized, can be deployed independently

**Stage 3 optimization:** Once each dimension is working independently, consider unified executor with strategy pattern.

---

### Question 4: Sequential vs Parallel Phasing

**Advisor recommendation:** ✅ **Sequential (Stage 1 then Stage 2) for Stage 1-2. Parallel for Stage 3 onward.**

**Rationale:**
- **Risk:** If data model wrong, you'll discover in Stage 1. Better to learn from BI queries before building executors.
- **Learning:** Stage 1 will reveal which dimensions need more sophisticated data (e.g., "Inventory data would help shipping template rules")
- **Timeline impact:** Only 2-3 week delay. Acceptable for risk reduction.

**Phasing:**
- **Weeks 1-3 (Apr 15-May 5):** Stage 1 only. Build BI tool. Validate data model.
- **Weeks 4-5 (May 5-20):** Stage 2 executors built in parallel. Different teams working on different dimensions.
- **Week 6+ (May 20+):** Stage 3 optimization + automation.

---

### Question 5: Revenue Weighting vs User Flexibility

**Advisor recommendation:** ✅ **Default to revenue ranking, allow manual sort.**

**Rationale:**
- Default to revenue: Forces focus on highest-impact work (good for strategy)
- Allow sort by gap_count, device, region, etc.: Operators can explore patterns (good for discovery)
- Best of both: "Default view sorted by revenue impact. [Sort options: count, complexity, date, device, region]"

**Example:**
```
View: Gap Explorer
Default sort: Revenue Opportunity (descending)
[↑ ↓ buttons for manual sort]
  ├─ Revenue Opportunity
  ├─ Gap Count
  ├─ Design
  ├─ Device
  └─ Region
```

---

### Question 6: Inventory Module Sequencing

**Advisor recommendation:** ✅ **Build Stage 1-2 with approximations, integrate real data in Stage 2.5.**

**Rationale:**
- Shipping template gaps can be calculated WITHOUT inventory (just flag items not on Reduced/Prime)
- FBA penetration gaps can use SKU naming (F prefix = FBA) as proxy for now
- Once Harry delivers inventory module:
  - Refine shipping template rules (don't convert if out of stock)
  - Improve FBA gap priority (use actual fulfillment capability, not just prefix)
  - Enable FBA migration execution

**Timeline:**
- Stage 1-2: Use approximations
- Stage 2.5 (May 20): Integrate inventory data, refine all 5 dimensions
- No hard blocker. Inventory is force multiplier, not prerequisite.

---

### Question 7: Execution Permissions

**Advisor recommendation:** ✅ **Manual approval (Cem reviews queue, clicks "convert").**

**Rationale:**
- Bulk operations touch sensitive data (3.5M listings)
- Manual approval provides safety gate
- Cem sees queue of 1,000 items queued for shipping template update → can review before executing
- Risk: Automatic execution could have unintended consequences (rate limits, SP-API failures, data quality issues)

**Implementation:**
```
1. Dashboard shows "Queued for conversion: 1,247 items"
2. Cem clicks "Review queue" → sees items
3. Cem can filter, exclude items, then clicks "Convert selected"
4. Cron executes overnight, logs results
5. Next morning: Dashboard shows "Converted: 1,187. Failed: 60 (out of stock)."
```

**Escalation to automatic:** Stage 3, after 1 month of successful manual executions. Then: "Auto-convert LOW-priority items, manual approve HIGH-priority items."

---

### Question 8: Integration Points & Mocking

**Advisor recommendation:** ✅ **Build Stage 1 with real data, mock outputs in Stage 2, integrate real integrations in Stage 2.5.**

**Rationale:**
- Stage 1 (BI): Use real Active Listings Report + BQ orders. Real data feeds.
- Stage 2 (Execution): Mock outputs for non-critical dimensions:
  - Device gaps → Output to CSV (mock PULSE API)
  - Cross-region gaps → Output to CSV (mock SKU staging API)
  - Shipping gaps → Call real SP-API (critical path, don't mock)
  - FBA gaps → Output to CSV (mock inventory API)
  - PRUNE → Call real SP-API (critical path, don't mock)
- Stage 2.5 (Integration): Integrate real APIs once mocking validated

**Why mock non-critical dimensions?**
- SP-API is low-risk (well-tested, Cem has experience)
- PULSE + SKU staging are internal systems, can integrate later
- Shipping + PRUNE are customer-facing, integrate when stable

---

## Data Quality Concerns

### Challenge 1: Active Listings Report Freshness
- Report is weekly (generated Saturdays)
- By next Saturday, 7 days of new listings not in snapshot
- **Solution:** Calculate delta daily. "New listings since last full report: X". Refresh full snapshot weekly.

### Challenge 2: BQ Orders Lag
- BQ syncs nightly, not real-time
- Shipping template sales impact data is ~24h old
- **Solution:** Acceptable for weekly analysis. Refresh nightly.

### Challenge 3: Cross-Region Consistency
- US listings reported in ATVPDKIKX0DER format
- UK listings reported in A1F83G7Y2K0TJSG format
- Mapping via SKU (design + device) not ASIN (region-specific)
- **Solution:** Use SKU as join key, not ASIN. SKU parsing rules handle this correctly.

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Data model wrong | Medium | Stage 1 BI queries validate before Stage 2 |
| Active Listings Report changes schema | Low | Monitor schema weekly, update parser if needed |
| SP-API rate limits on bulk updates | Medium | Batch 100 items/request, 5 req/sec, respect 429s |
| Inventory data not ready | Low | Use approximations (F prefix) for now, integrate later |
| PULSE/SKU staging APIs unavailable | Low | Mock outputs, integrate later |
| Dashboard performance on 3.5M rows | Low | Index on (design, device, region), query should be <1s |

**Overall risk:** Low-Medium. Sequential phasing reduces risk.

---

## Performance Considerations

### Query Optimization
```sql
-- Critical queries should use indexes:
CREATE INDEX idx_device_gap ON listings_full(device_gap_flag, revenue_last_90d DESC);
CREATE INDEX idx_shipping_gap ON listings_full(shipping_gap_flag, region, sales_last_90d DESC);
CREATE INDEX idx_design ON listings_full(design);
```

### Data Volume
- 3.5M listings in SQLite = ~500MB (moderate)
- Queries should complete in <1 second
- Dashboard refresh (full BI tool) = ~5 seconds weekly
- Real-time dashboard views = <1 second (pre-computed summaries)

### Caching Strategy
- Summary scorecard: Recompute weekly
- Explorer drill-downs: Recompute on demand (<5s acceptable)
- Pattern heatmaps: Recompute weekly (static visual)

---

## Stage 1 Success Criteria

**You'll know Stage 1 is successful when:**

1. ✅ Dashboard loads in <2 seconds
2. ✅ Five dimensions visible in executive summary
3. ✅ Patterns are clear (e.g., "iPhone 16 has 40% shipping compliance, iPhone 17 has 95%")
4. ✅ Cem can drill into a design and see all gaps (device, region, shipping, FBA, prune status)
5. ✅ Revenue opportunity calculations are accurate (spot-check 10 designs manually)
6. ✅ Data freshness is acceptable (weekly refresh is sufficient)

**If any of these fail, reshape before moving to Stage 2.**

---

## Stage 2 Success Criteria

**You'll know Stage 2 is successful when:**

1. ✅ Execution queue interface works (can queue items for conversion)
2. ✅ SP-API batch updates execute without errors (95%+ success rate)
3. ✅ Execution log shows clear pass/fail (transparent)
4. ✅ Cem can bulk-convert 1,000 shipping templates overnight with confidence
5. ✅ Device gap output goes to PULSE (or mocked CSV for now)
6. ✅ PRUNE suppression works (old listings marked suppressed, confirmed on Amazon)

---

## Architect's Notes

**Advisor perspective on this project:**

> "This is well-scoped. Five dimensions unified into one BI dashboard is the right call. The sequential phasing (Stage 1 BI, then Stage 2 execution) is smart risk management. You're not over-engineering the data model (single table is correct for BI). You're allowing for softblocking on dependencies (inventory, integrations) without hard-blocking delivery.
>
> One thing to watch: Make sure Stage 1 BI queries are fast enough (< 1 second) on 3.5M rows. If not, you'll need to pre-compute summaries or partition the data. But that's a Stage 1 concern, not an architectural one.
>
> The five dimensions are real, the revenue opportunity is substantial, and the execution risk is manageable. Build this."

---

## Recommendations (Priority Order)

1. **Proceed with unified single-table design.** Boolean flags, revenue ranking.
2. **Start Stage 1 (BI) now.** Sequential phasing is lower risk.
3. **Plan Stage 2 parallel development.** Different teams working on different dimensions.
4. **Inventory integration in Stage 2.5.** Non-blocking, but refines rules significantly.
5. **SP-API execution first, other integrations later.** Shipping + PRUNE are customer-facing. Device + cross-region can be CSV exports for now.
6. **Manual approval for bulk execution.** Safety gate. Auto-conversion can come later in Stage 3.

---

## Questions for Planning Phase

1. **Who owns each dimension in Stage 2?**
   - Device coverage → Marketplace Ops?
   - Cross-region → SKU staging?
   - Shipping template → Codex cron?
   - FBA migration → Harry?
   - PRUNE → Codex cron?

2. **What's the integration order for Stage 2.5?**
   - Which API comes first?
   - Which can wait?

3. **Dashboard host?**
   - New Next.js service (like Conversion Dashboard)?
   - Or extend ecell-dashboard?

4. **Cron executor?**
   - Codex for shipping/prune?
   - Separate agents for other dimensions?

---

**Status:** ADVISOR REVIEW COMPLETE ✅ | **Recommendation:** PROCEED with confidence | **Next:** PLANNING phase

