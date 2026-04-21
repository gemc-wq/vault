# Athena Review: Amazon Data Analytics Project (15 Documents)

**Reviewer:** Athena | **Date:** 2026-04-11 | **Requested by:** Cem
**Docs reviewed:** 15 files (~247KB) in `/02-Projects/amazon-data-analytics/`
**Cross-referenced against:** Wiki SOPs, SKU parsing rules, PULSE specs, shipping rules, TASK_SHEET

---

## Executive Verdict

**The work is thorough and well-structured.** Ava + Advisor Tool produced a comprehensive, implementable plan. However, there are **6 issues that need fixing** before kickoff and **4 gaps** the docs don't address.

**Confidence in plan:** 80% (vs Advisor's 85-90%). I'm more conservative because of agent roster mismatches and infrastructure assumptions.

---

## 1. What's Good (No Changes Needed)

| Strength | Detail |
|----------|--------|
| **Five-dimension unification** | Correct call. Shipping, device, cross-region, FBA, PRUNE in one dashboard eliminates silos. |
| **Single-table SQLite for MVP** | Advisor is right — denormalized flags beat normalized joins for BI reads on 3.5M rows. |
| **Sequential phasing** | Stage 1 (BI) → Stage 2 (execution) → Stage 3 (automation) is sound risk management. |
| **Revenue estimates grounded** | $37.5K/mo shipping loss is data-backed. Device gap estimates tie to PULSE. Conservative range is honest. |
| **Edge cases documented** | PROJECT-SHAPE docs cover rate limits, token expiry, inventory dependencies, license-specific rules. Good engineering. |
| **Manual approval for bulk execution** | Correct. Don't auto-convert 500K listings on day one. Safety gate is essential. |
| **SOP integration** | MISSED-DATAPOINTS-ADDENDUM correctly identified 7 gaps from SOP cross-reference. Shows rigour. |

---

## 2. Issues to Fix (6)

### Issue 1: 🔴 Agent Roster Mismatch
**Severity:** HIGH — plan won't execute as written

The docs reference agents that don't match SOUL V4's actual roster:

| Doc Reference | Actual Status | Fix |
|---------------|---------------|-----|
| **Forge** (dashboard builder) | Not in SOUL V4 roster. No "Forge" agent exists in OpenClaw. | Assign to Jay Mark (human, PH) or build via Claude Code CLI |
| **Spark** (backup for Forge) | Not in roster. | Remove or assign backup to Bolt |
| **Loom** (competitor research) | Not in roster. | Assign to Hermes or Atlas |
| **Codex** (data pipeline) | Exists in OpenClaw but role undefined in SOUL V4. Not the adversary subagent. | Clarify: is this OpenClaw's codex agent or a new pipeline agent? |
| **Atlas** (ads analyst) | Exists in OpenClaw. Role matches. | ✅ OK |
| **Bolt** (carrier compliance) | Exists in OpenClaw. Role matches. | ✅ OK |
| **Harry** | Docs say "infrastructure + inventory module". SOUL V4 says "Finance spec-only". | Reconcile — Harry can spec the inventory module but Jay Mark builds it |

**Recommendation:** Create an AGENT-ASSIGNMENT.md that maps each deliverable to a real agent/human from SOUL V4's roster. Without this, nobody knows who's actually building the dashboard.

---

### Issue 2: 🔴 Shipping Template Names Still Unconfirmed
**Severity:** CRITICAL — blocks Apr 15 start

Every doc flags this. The Advisor review says "Cem must confirm by Apr 14." It's now Apr 11. This is the single biggest risk.

**What's needed from Cem:**
- US template: Is it "Reduced Shipping", "Two-Day Shipping", or something else?
- UK template: Is it "Nationwide Prime", "Prime", or something else?
- DE template: What's the German equivalent?
- Which column in Active Listings Report contains the template? (`merchant-shipping-group`?)

**Recommendation:** This is a 10-minute Seller Central lookup. Cem should do it today.

---

### Issue 3: 🟠 Cron Engine Assumption Wrong
**Severity:** MEDIUM — docs assume Gemini Flash, reality is Gemma 4

Multiple docs (PROJECT-BRIEF-2026-04-10.md, DASHBOARD-DESIGN-SPEC.md) reference "Gemini Flash" for Saturday crons. We already switched all 4 weekly crons to **Gemma 4 (ollama/gemma4:26b)** on Apr 10.

**Impact:** Gemma 4 is local ($0) but slower and less capable for complex analysis. The docs' assumption of cloud-hosted LLM with larger context window affects:
- Analysis depth per cron run
- Timeout requirements (currently 600s)
- Complex multi-step reasoning (Gemma 4 struggles with 10+ metric calculations)

**Recommendation:** Update all docs to reference Gemma 4. For complex analytics (Search Term analysis, Buy Box correlation), consider using Claude SDK (Sonnet) via subagent instead of Gemma 4.

---

### Issue 4: 🟠 SKU Parsing Not Referenced
**Severity:** MEDIUM — data pipeline will break without it

The wiki has a **definitive SKU parsing rules document** (`/01-Wiki/SKU_PARSING_RULES.md`) that defines:
- Format: `{PRODUCT_TYPE}-{DEVICE_CODE}-{DESIGN_CODE}-{VARIANT}`
- Critical FBA prefix stripping rules (strip F except FLAG, F1309, FRND, FKFLOR)
- Product type reference table
- Device code mappings

**None of the 15 project docs reference this.** The data pipeline (Stage 1) must use these parsing rules to extract design, device, and product_type from SKUs. Without it, the `listings_full` table's `design`, `device`, and `product_type` columns will be empty or wrong.

The wiki SOP (`SOP_LISTINGS_DB_MANAGEMENT.md`) explicitly states SKU parsing is mandatory for all listings analysis.

**Recommendation:** Add explicit dependency on SKU_PARSING_RULES.md in PROJECT-PLAN-v2. Stage 1 data pipeline task "Build SQLite schema" must include SKU parsing integration.

---

### Issue 5: 🟡 Document Overlap and Redundancy
**Severity:** LOW — confusing but not blocking

There are **two versions of several documents** that overlap significantly:

| Document Pair | Overlap |
|---------------|---------|
| PROJECT-PLAN-UNIFIED-LISTINGS-INTELLIGENCE.md (v1) vs v2 | v2 supersedes v1. v1 should be archived. |
| PROJECT-BRIEF-2026-04-10.md vs PROJECT-BRIEF-DATA-EXTRACTION.md | ~60% overlap on data extraction topics |
| ADVISOR-REVIEW-UNIFIED-LISTINGS-INTELLIGENCE.md vs ADVISOR-REVIEW-PROJECT-PLAN-v2.md | First reviews architecture, second reviews full plan. Both valid but confusing naming. |
| PROJECT-SHAPE-SHIPPING-TEMPLATE.md vs SHIPPING-TEMPLATE-DASHBOARD-ADDENDUM.md vs ADVISOR-SHIPPING-STRATEGY.md | Three docs covering shipping templates from different angles |

15 files is too many for one project. After Cem approves, consolidate to:
1. **PROJECT-PLAN-v2.md** (the plan — keep)
2. **ADVISOR-REVIEW-v2.md** (the review — keep)
3. **SHIPPING-RULES.md** (merge 3 shipping docs — create)
4. **DATA-GUIDE.md** (merge 2 data extraction docs — create)
5. **SOP-WEEKLY-CRON-RUN.md** (the SOP — keep)
6. Archive the rest to `/archive/`

---

### Issue 6: 🟡 Revenue Double-Counting Risk
**Severity:** LOW — affects expectations, not execution

The revenue estimates across documents don't add up consistently:

| Source | Estimate |
|--------|----------|
| PROJECT-PLAN-v2 summary table | $350-550K/year |
| Advisor review (conservative) | $300-400K/year |
| Advisor review (aggressive) | $500-600K/year |
| PROJECT-SHAPE (5 dimensions) | $300-450K/year + $36K savings |
| SHIPPING-TEMPLATE-DASHBOARD-ADDENDUM | $100-200K/year (shipping alone) |

The shipping template revenue is counted as both "$37.5K/mo" AND part of the overall device gap / FBA estimates. Some of these improvements are overlapping (fixing shipping AND moving to FBA on the same SKU doesn't double the lift).

**Recommendation:** Present to Cem as **"$300-400K/year net new, with $500K+ upside if all dimensions execute perfectly."** Don't stack estimates additively.

---

## 3. Gaps Not Addressed (4)

### Gap 1: No Connection to Existing PULSE Dashboard
PULSE V4 already tracks champion designs, device elbow points, and conversion attribution. The project plan references "PULSE data" but doesn't specify:
- How Listings Intelligence **feeds back** to PULSE
- Whether they share the same database or sync
- Who resolves conflicts when PULSE says "champion" but Listings Intelligence says "gap"

**Recommendation:** Add a PULSE Integration section to PROJECT-PLAN-v2 specifying data flow direction and conflict resolution.

### Gap 2: No Mention of Athena's KPI Dashboard Scope
I already created `LISTINGS_KPI_DASHBOARD_SCOPE.md` (in `/02-Projects/listings-intelligence/`) with 7 KPI categories and a 4-phase build plan. This overlaps significantly with the project plan's dashboard.

**Recommendation:** Merge or reconcile. My scope doc adds the **shipping-to-conversion-to-revenue chain** that Ava's docs don't have. The project plan adds the execution engine I didn't scope.

### Gap 3: Active Listings Report File Size
The docs mention 6-7GB TSV files. The actual files in `~/Downloads/` are:
- US Active Listings: 6.8GB (Apr 10)
- DE Active Listings: 4.8GB (Apr 4)

**Gemma 4 cannot process these.** SQLite can handle them but loading 6.8GB into SQLite requires a dedicated parsing script (not an LLM task). The SOP (`SOP_LISTINGS_DB_MANAGEMENT.md`) has the SQLite load process documented, but the project plan doesn't reference it.

**Recommendation:** Stage 1 data pipeline must include a dedicated Python script for TSV→SQLite loading. This is not an agent task — it's a script that runs on Mac Studio.

### Gap 4: No Rollback Plan
If the Codex cron converts 10,000 shipping templates and it turns out the template name was wrong, there's no documented way to revert. SP-API updates are not easily reversible at scale.

**Recommendation:** Add rollback section: before bulk conversion, snapshot current template assignments. If conversion causes problems, re-apply old templates from snapshot.

---

## 4. Wiki Alignment Check

| Wiki Document | Project Plan Alignment | Status |
|---------------|----------------------|--------|
| `SKU_PARSING_RULES.md` | ❌ Not referenced | Must add |
| `SOP_LISTINGS_DB_MANAGEMENT.md` | ✅ Compatible (SQLite approach matches) | OK |
| `SOP_WEEKLY_REPORTS.md` | ✅ MISSED-DATAPOINTS addendum correctly cross-referenced | OK |
| `SOP_WEEKLY_LISTINGS_REPORT.md` | ✅ Delta calculation approach matches | OK |
| `SHIPPING_CARRIER_RULES.md` | ⚠️ Partially aligned — wiki has 3-layer routing logic not in project plan | Add reference |
| `SOP_SHIPPING_LABELS.md` | ⚠️ Veeqo/Veco transition status not reflected | Minor |
| `PULSE_SPEC_V4.md` | ⚠️ Referenced but no integration spec | Add integration section |

---

## 5. Implementation Readiness Assessment

| Component | Ready? | Blocker |
|-----------|--------|---------|
| Active Listings data (US/UK/DE) | ✅ Files exist in ~/Downloads/ | None |
| BigQuery orders data | ✅ BQ access confirmed | None |
| SQLite infrastructure | ✅ Mac Studio has SQLite | None |
| SKU parsing rules | ✅ Wiki doc exists | Must wire into pipeline |
| Dashboard hosting | ❌ No decision on Next.js vs extend existing | Cem decision needed |
| SP-API for shipping updates | ⚠️ US token confirmed, UK/DE unverified | Drew to verify |
| Shipping template names | ❌ Unconfirmed | **Cem must confirm TODAY** |
| Agent assignments | ❌ Roster doesn't match plan | Reassignment needed |
| Business Reports CSVs | ✅ Already downloaded weekly | None |
| PULSE export data | ⚠️ Export format not specified | Hermes to confirm |
| Veeqo API creds | ❌ Not available | Harry (Stage 2, non-blocking) |
| Amazon Ads API | ❌ Not available | Drew (Stage 2.5, non-blocking) |

---

## 6. Recommended Next Steps (Priority Order)

1. **TODAY (Apr 11):** Cem confirms shipping template names (US/UK/DE) — 10 min in Seller Central
2. **TODAY:** Create AGENT-ASSIGNMENT.md mapping deliverables to actual agents/humans
3. **This weekend:** Build TSV→SQLite loading script for Active Listings (6.8GB file)
4. **Apr 14:** Archive redundant docs, consolidate to 5-6 key files
5. **Apr 15:** Stage 1 kickoff (if shipping rules confirmed)
6. **Apr 15:** Wire SKU parsing rules into data pipeline
7. **Week 2:** Monitor Hermes workload (bottleneck risk per Advisor)

---

## 7. DelegAIt Opportunity Flag

This entire project is a **DelegAIt product candidate**. The pattern:
- Ingest marketplace data (any platform, not just Amazon)
- Parse SKUs into design × device × region dimensions
- Identify gaps across 5+ dimensions
- Prioritize by revenue impact
- Execute bulk fixes via API

**Generic version:** "Marketplace Intelligence Dashboard" — any e-commerce company with 1K+ SKUs across multiple platforms could use this. $499-999/mo tier.

---

---

## 8. Blueprint V3 Overlap Analysis (Added Apr 11, per Cem's request)

**Source:** `Vault/00-Company/OPERATIONAL_BLUEPRINT_V3.md`

### Key Finding: Stage 2 Execution Engine Should NOT Build Its Own SP-API Layer

Blueprint V3 Stage 6 already has an Amazon middleware on Cloud Run with SP-API access (`POST /api/v1/reports/request-and-wait`, JSON_LISTINGS_FEED). The Listings Intelligence project's Stage 2 plans to build a **separate** Codex cron for SP-API shipping template edits. This is duplication.

### Recommended Architecture

```
LISTINGS INTELLIGENCE (analysis)          BLUEPRINT V3 (execution)
────────────────────────────────          ────────────────────────
Stage 1: BI Dashboard (5 gaps)     →     Stage 6: Middleware edits via SP-API
Stage 2: Execution QUEUE (not API) →     Stage 6: Middleware reads queue, executes
Stage 3: Auto-prioritization       →     Stage 10: PULSE feedback loop
```

### Overlap Map

| Function | Blueprint V3 | Listings Intelligence | Resolution |
|----------|-------------|----------------------|------------|
| SP-API listing edits | Stage 6 middleware (Cloud Run) | Stage 2 Codex cron | **Use Blueprint middleware only** |
| Gap identification | Stage 10 (PULSE + Hermes) | Stage 1 (5-dimension dashboard) | **Complementary — LI is deeper** |
| New listing creation | Stages 3-5 (SKU → Image → Content → Upload) | Out of scope | No conflict |
| Inventory data | Stage 7B (`blank_inventory`, 5,193 SKUs) | "Harry's inventory module" blocker | **Same thing — Blueprint owns it** |
| Shipping compliance | Stage 8 (carrier routing) | Shipping template cron | **Different aspects — compatible** |

### Impact on Project Plan

1. **Stage 1** — no changes needed
2. **Stage 2** — redesign: output an execution queue (Supabase table or JSON), not a direct SP-API caller. Blueprint middleware consumes the queue.
3. **Stage 3** — no changes needed
4. **Blocker alignment** — "Product Listing scope" is one shared blocker, not two separate ones

### Blueprint Components Already Built

| Component | Status | Relevance |
|-----------|--------|-----------|
| Amazon middleware API (Cloud Run) | ✅ Live | SP-API execution layer exists |
| PULSE Dashboard | ✅ Live | Gap identification partially exists |
| Supabase `blank_inventory` | ✅ Built (5,193 SKUs) | Inventory dependency partially met |
| EAN assignment engine | ✅ Built (44K pool) | New SKU creation supported |
| ListingForge (Lane 1 POC) | 🟡 Built, testing | Image generation for new variants |
| Echo content generation | ✅ Framework ready | Content for new listings |

### What Blueprint Still Needs (Shared Blockers)

- Amazon "Product Listing scope" for JSON_LISTINGS_FEED — same as project plan's SP-API blocker
- Xero OAuth (UK + US) — finance, not directly related
- Jay Mark's Supabase schema updates — shared dependency

### Council Question

Should Listings Intelligence Stage 2 execution be **absorbed into Blueprint V3 Stage 6** rather than built as a separate system? This would mean:
- One SP-API layer (Blueprint middleware)
- One execution queue (Supabase)
- Listings Intelligence = pure analytics + gap identification + queue generation
- Blueprint = execution engine for all listing changes

This is cleaner and avoids two teams building two API integrations for the same Amazon endpoints.

---

**Status:** REVIEW COMPLETE ✅ | **Verdict:** PROCEED with 6 fixes + Blueprint integration | **Critical path:** Shipping template names (Cem, today)
