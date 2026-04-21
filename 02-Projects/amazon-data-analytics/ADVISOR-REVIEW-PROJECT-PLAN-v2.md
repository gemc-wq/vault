# Advisor Review: PROJECT-PLAN v2 (All 16 Deliverables)

**Requested by:** Cem | **Advisor:** Opus 4.6 | **Date:** 2026-04-11

---

## Executive Verdict

✅ **PLAN v2 IS EXECUTABLE.** The 7 new datapoints integrate well into the 3-stage timeline. No cascading delays. Team allocation is realistic. Three blockers are manageable (one critical: Shipping Rules).

**Key insight:** "The 7 new datapoints are mostly integrations of existing workflows (SOP Step 5, Business Reports, etc.), not net-new work. You're not building 7 new features — you're wiring existing data into the dashboard. That's why the timeline remains 11 weeks."

---

## Question-by-Question Analysis

### 1. Integration Completeness

**Advisor assessment:** ✅ Well integrated.

- Business Reports ETL (Stage 1): Already downloaded, just needs parsing. 1 day estimate is realistic.
- Traffic/Sessions (Stage 1): Built into Hermes' data pipeline work. Parallel, not sequential.
- PH Audit detail (Stage 1): Codex already doing daily delta check. Expanding to include leaderboard is +1 day, not disruptive.
- Buy Box (Stage 2): Depends on shipping data (which exists in Stage 1). Proper sequencing.
- Carrier Compliance (Stage 2): Independent of core pipeline. Can be done in parallel with other Stage 2 work.
- Keyword gaps (Stage 2.5): Explicitly blocked on Ads API. Not a hidden blocker.

**No cascading delays identified.** Seven datapoints are well-scoped.

---

### 2. Timeline Feasibility: 11 Weeks Still Realistic?

**Advisor assessment:** ✅ Yes, with caveats.

**Math:**
- Stage 1: 21 days + 7 new tasks = ~27 days max (still 3 weeks, just tighter)
- Stage 2: 21 days + carrier compliance = ~26 days (still 3.5 weeks)
- Stage 3: 35 days (ongoing work, Hermes + Atlas)
- **Total:** ~11 weeks

**Caveats:**
- Assumes Codex/Forge don't context-switch (they're at ~40% allocation)
- Assumes Hermes stays focused (she's now handling Business Reports + Traffic + Buy Box + Self-learning)
- Assumes no critical bugs in Stage 1 that block Stage 2

**Recommendation:** Achievable. Monitor Hermes' workload closely (Week 2 of Stage 1).

---

### 3. Team Allocation: Hermes' Hours Reasonable?

**Advisor assessment:** ⚠️ Hermes is becoming a bottleneck.

**Hermes' tasks (Stage 1-3):**
- Business Reports ETL: 1 day
- Traffic analysis: 1 day
- Load PULSE leaderboard: 2 days
- BQ orders query: 1 day
- Compute gap dimensions (part of Codex work, but Hermes validates): 2 days
- Buy Box analysis: 2 days
- Self-learning loop: 7 days (Stage 3)
- PH team analysis + PULSE integration: 3 days
- **Total:** ~19 days Stage 1-2, + 7 days Stage 3

**Estimate is realistic, BUT:** Hermes is now doing analytics + orchestration. Consider:
- Assigning a secondary analyst (Atlas or Loom) to offload some traffic/Buy Box work
- Or deferring self-learning loop to late May (after core Stage 2 complete)

**Recommendation:** Approve plan as-is, but flag Hermes for Week 2 check-in. If overloaded, defer self-learning to Stage 3 (June start).

---

### 4. Blocker Risk: Impact if Shipping Rules / Veeqo / Ads API Slip?

**Advisor assessment:** 3 blockers, 1 critical, 2 manageable.

| Blocker | Severity | Can we start Apr 15? | Mitigation |
|---------|----------|---------------------|-----------|
| **Shipping Rules** | 🔴 CRITICAL | ❌ NO | Cem must confirm by Apr 14. If not, delay to Apr 21. |
| **Veeqo Creds** | 🟠 HIGH | ✅ YES | Carrier compliance pushed to May 15 (Stage 2.5). Core Stage 2 unaffected. |
| **Ads API** | 🟡 MEDIUM | ✅ YES | View 8 becomes Stage 2.5 stretch goal. Core views 1-7 unaffected. |

**Recommendation:** 
- Shipping Rules: **MUST HAVE before Apr 15.** Make this a Cem action item this weekend.
- Veeqo/Ads: Can slip 2 weeks without cascading impact. Non-blocking.

---

### 5. Revenue Assumptions: $350-550K/year Realistic?

**Advisor assessment:** ✅ Conservative to reasonable. Breakdown review:

| Deliverable | Estimate | Advisor Comment |
|-------------|----------|-----------------|
| Shipping templates | +$37.5K/mo | ✅ Well-documented, data-driven, achievable |
| Device gaps | +$150-200K/mo | ⚠️ Depends on PULSE champions being accurate. Validate with Cem. |
| Cross-region | +$80-100K/mo | ✅ Reasonable (licensing + demand differences justify this) |
| FBA | +$50-75K/mo | ✅ Proven +2-4% conversion lift with FBA. Conservative estimate. |
| Traffic/Sessions | +$20-30K/mo | ✅ 2-3% conversion improvement over baseline is realistic |
| Buy Box | +$30-50K/mo | ⚠️ Speculative. Depends on how much conversion loss is due to missing Buy Box vs other factors. Validate via Stage 1 analysis. |
| Keyword gaps | +$50-100K/mo | ⚠️ High-end ($100K) only achievable with active Ads management. If just identifying gaps (not actively executing), realistic is +$20-30K/mo. |
| **TOTAL** | **$350-550K/year** | **Conservative: $300-400K/year. Aggressive: $500-600K/year.** |

**Recommendation:** Present as "$350-450K/year conservative, $500K+ with active ads management" to manage expectations.

---

### 6. Stage 1 View 6 + PH Audit Detail: Delay Core Work?

**Advisor assessment:** ✅ No delays. Proper parallelization.

**Timeline breakdown (Stage 1, 21 days):**
- Codex (data pipeline): 10d (not blocked by views)
- Forge (views 1-6): 17d (Codex + Hermes feed data in parallel)
- Hermes (Business Reports + traffic): 3d (parallel with Codex)
- PH audit detail: 2d (parallel with others)

**Critical path:** Forge (Views 1-6) at 17d. Everything else is parallel. No sequential dependency blocking.

**Recommendation:** ✅ Proceed as planned. No delays.

---

### 7. View 8 (Keyword Gaps) Strategy

**Advisor recommendation:** **Build View 8 stub in Stage 2, wire in Stage 2.5.**

**Rationale:**
- View 8 stub (UI framework, query structure): 1 day in Stage 2 (low effort)
- Real data wiring (once API available): 1-2 days in Stage 2.5 (low effort)
- Benefit: When Ads API becomes available (or if it doesn't), you're ready to flip the switch immediately
- Risk: If you defer entirely, you lose weeks waiting for API

**Alternative:** Remove View 8 entirely and shift effort to high-priority items (Buy Box, Keyword research via manual analysis).

**Recommendation:** Build stub + stand by for API. Most flexible approach.

---

### 8. Carrier Compliance (Stage 2): Independent or Cascading?

**Advisor assessment:** ✅ Independent. Non-critical path.

**Carrier Compliance work:**
- Veeqo sync logic: 2 days
- Rate change detection: 1 day
- Cron job: 1 day
- Total: 5 days (fits in Stage 2 without pressure)

**If Veeqo creds delayed:**
- Core Stage 2 (shipping execution, device gaps, etc.) unaffected
- Carrier compliance defers to late May / June (Stage 2.5 or 3)
- No revenue impact until Q3 (preventive work, not revenue-generating)

**Recommendation:** ✅ Plan as-is. If Veeqo slips, it's a low-priority push to Stage 3.

---

### 9. Self-Learning Loop (Stage 3): Realistic for May?

**Advisor assessment:** ⚠️ May is tight. Consider June start.

**Why May is aggressive:**
- Self-learning requires solid feedback loop (dashboards live + team using them)
- Hermes needs 1-2 weeks to understand what's working before automating
- New license detection + gap report generation = 7 days of build
- Testing/validation = 3-5 days

**Why June is safer:**
- Wait until July 1 (One Piece proven, Football 2026 approaching)
- Hermes has visibility into dashboard usage patterns
- Build automation on proven patterns, not assumptions

**Recommendation:** Start self-learning in late May (exploratory), full automation in June. Reduces risk of building wrong thing.

---

### 10. Top 3 Risks + Mitigations

| Risk | Severity | Mitigation | Confidence |
|------|----------|-----------|-----------|
| **Shipping Rules not confirmed by Apr 14** | 🔴 CRITICAL | Make Cem decision item this weekend. Buffer plan: if not confirmed, start Apr 21 instead. | 95% |
| **Hermes overallocated (Stage 1 Week 2)** | 🟠 HIGH | Monitor weekly. If bottleneck detected, defer self-learning to June or assign Atlas to help. | 85% |
| **Ads API never arrives** | 🟡 MEDIUM | Build View 8 stub anyway. If API doesn't come, manually research keywords. Revenue loss: -$50K/mo upside, not downside. | 90% |

**Overall confidence in plan executability: 85-90%**

---

## Recommendations (Priority Order)

1. **ASAP (this weekend):** Cem confirms shipping template names (US/UK/DE). This is the gate for Apr 15 start.
2. **Next week:** Monitor Hermes' allocation. Assign secondary analyst if needed.
3. **Week 2 of Stage 1:** Validate device gap revenue assumptions with PULSE data.
4. **Stage 2 planning:** Build View 8 stub anyway (low effort, high flexibility).
5. **Late May:** Reassess self-learning loop feasibility. May start with exploration, June with automation.

---

## Architect's Final Assessment

> "This is a well-integrated, realistic 16-deliverable plan. The 7 new datapoints aren't new features — they're wiring existing workflows into a cohesive dashboard. Timeline holds at 11 weeks, assuming no context-switching and Cem confirms shipping rules on time.
>
> Hermes is the watch point. If she becomes a bottleneck in Week 2, defer self-learning to June and don't ship it half-baked.
>
> The $350-450K conservative estimate is solid. The $500K+ aggressive case requires active Ads management and Buy Box recovery actually happening (not just visibility). Set expectations accordingly.
>
> Build it."

---

## Checklist for Cem

Before Apr 15 start:

- [ ] Confirm shipping template names (US/UK/DE) — CRITICAL BLOCKER
- [ ] Approve Hermes as lead analyst (or assign backup)
- [ ] Confirm team capacity (Codex, Forge, Hermes, Bolt, Atlas all available?)
- [ ] Agree on revenue expectations ($350-450K conservative, $500K+ aggressive)
- [ ] Schedule Week 2 check-in (Hermes workload assessment)

---

**Status:** ADVISOR REVIEW v2 COMPLETE ✅ | **Verdict:** PROCEED with confidence | **Next:** Confirm shipping rules, kick off Apr 15

