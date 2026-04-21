# Request: Implementation Plan — Shipping Template Dashboard
**From:** Ava | **To:** Hermes | **Date:** 2026-04-14 | **Priority:** HIGH

---

## What I need from you

A detailed implementation plan for the Shipping Template Gap Dashboard + Bulk Fix Engine. Please structure it as a PROJECT-PLAN.md with task breakdown, timelines, owners, and dependencies.

## Context (read these first)

1. **Project Shape:** `Vault/02-Projects/` or workspace `projects/shipping-template-dashboard/PROJECT-SHAPE.md`
2. **Business Rules:** `workspace/projects/shipping-template-dashboard/BUSINESS_RULES.md`
3. **Source CSVs:** Already in `Vault/04-Shared/active/` (fbm_wrong_template + iphone17 files)
4. **Middleware docs:** `Vault/02-Projects/amazon-report-middleware/HANDOFF.md`

## Key decisions from Cem (confirmed today)

1. **Data validity first** — Before any build, confirm data source is correct, recent, and properly filtered through staging table
2. **Staging table required** — Raw report → BQ staging → filtered curated table → dashboard reads from curated only
3. **Two action types:**
   - Standard → Reduced Shipping Template: NO price change
   - Standard → Prime (SFP): +$11 price increase to cover shipping cost
4. **Test SKU:** `HSTWH-L-WWE2JCEN-ICO` (ASIN: B0F213JBXT) — manually test in Seller Central first

## What your plan should cover

1. **Phase 1: Data Validation**
   - How do we confirm the Active Listings data is fresh and has `merchant-shipping-group`?
   - What does the staging table schema look like?
   - How do we apply the inclusion/exclusion filters (from BUSINESS_RULES.md)?
   - How do we cross-reference FL stock?

2. **Phase 2: Dashboard Build**
   - Tech stack recommendation (extend middleware? standalone?)
   - Key views: by product type, by device, by revenue impact
   - Action buttons: Convert to Reduced, Convert to Prime+$11, Export CSV, Preview

3. **Phase 3: SP-API Bulk Update**
   - How does the PATCH work for template change?
   - How does the PATCH work for price change?
   - Rate limiting strategy
   - Rollback mechanism

4. **Phase 4: Monitoring Cron**
   - Weekly delta check for new wrong-template listings
   - Alert threshold and channel

## Format requested

```markdown
# Project Plan: Shipping Template Dashboard
## Phase 1: Data Validation — [timeline]
### Tasks:
| Task | Owner | Duration | Depends on | Status |
...
## Phase 2: Dashboard — [timeline]
...
```

Include your estimate of total build time and the critical path.

**Reply with PROJECT-PLAN.md content. I will then run it through Advisor (Opus) for final scope review.**

— Ava
