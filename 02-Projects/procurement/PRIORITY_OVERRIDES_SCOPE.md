# Priority Overrides — Scope Document

> **Owner:** Cem | **Date:** 2026-04-15
> **Status:** DRAFT — awaiting review
> **Addresses:** LLM Council Review V2 Gap #5 (GPT-5.4 Business Logic)
> **Target Phase:** Phase 4 (after Phase 3 UI ships)
> **Related:** [[MASTER_PRD]], [[LLM_COUNCIL_REVIEW_V2_CEM]], [[LAYER0_COMPLIANCE_INTEGRATION]]

---

## 1. Problem Statement

The reorder engine currently applies `priority_multiplier` at the **product-group level** only (`product_group_config` table). HB401 gets 1.5x because the whole product group converts well. Every other group defaults to 1.0x.

This is too coarse. Real-world priority signals are **per-item**:

| Signal | Granularity | Example |
|--------|------------|--------|
| Amazon Prime promise at risk | Per SKU | HTPCR-IPH17 has 3 days cover on FL with Nationwide Prime template |
| Seasonal spike | Per item | HTPCR-S25U surging 4x normal velocity ahead of launch |
| Manual ops override | Per item | Cem flags HLBWH-IPD11 as critical for a retailer order |
| Best-seller momentum | Per item | Top 50 item accelerating — extend cover beyond 45d |

The product-group mechanism can't express any of these. The result: urgent items get the same cover-days as routine ones, leading to stock-outs on high-priority SKUs while low-priority items are over-ordered.

---

## 2. What We're Building

A **per-item priority override table** that any source (manual, automated, external) can write to. The reorder engine reads it during calculation and applies the multiplier to cover-days.

**One table. One lookup. Multiple writers.**

```
  [Manual Override]  ──┐
  [Amazon Compliance] ─┤──► priority_overrides ──► reorder engine
  [Best Seller Engine] ┘     (per item_code)        (cover_days × multiplier)
```

---

## 3. In Scope

- `priority_overrides` table in Supabase (same project as `blank_inventory`)
- Reorder engine integration: item-level override takes precedence over group-level
- Expiry mechanism (`expires_at`) — stale overrides auto-ignored
- Manual override UI (simple form on existing dashboard)
- Audit trail (who set what, when, why)
- API endpoint for external writers (authenticated)

## 4. Out of Scope

- Amazon listing compliance logic (owned by `amazon-unified-score` repo)
- Layer 0 template validation rules (listing-side concern, not procurement)
- Vinyl/consumable products (H8939, HSTWH) — managed by print floor, not PO pipeline
- Automatic override generation from velocity trends (future — Phase 5+)
- Changes to `product_group_config` table (stays as-is for group-level defaults)

## 5. Boundaries

| Boundary | Decision | Rationale |
|----------|----------|----------|
| Override stacking | **Highest wins** (not multiplicative) | Multiple overrides per item: take MAX(multiplier). Avoids runaway compounding |
| Override + group config | **Override wins** | Item-level is more specific than group-level. If override exists and is active, it replaces group config |
| Override range | **0.5x – 3.0x** | 0.5x = de-prioritise (e.g. known slow mover). 3.0x = maximum urgency (90 days cover for best sellers). Capped to prevent absurd orders |
| Expiry default | **7 days** | Most overrides are situational. If not refreshed, they expire. Permanent overrides set `expires_at = NULL` |
| Who can write | **ADMIN, MANAGER** (manual), **API key** (external) | China Ops and Warehouse roles cannot set priority overrides |

## 6. Success Criteria

1. Reorder engine uses item-level override when present, falls back to group config
2. Override expires after `expires_at` — no manual cleanup needed
3. External system (Amazon compliance) can POST overrides via authenticated API
4. Cem can manually set priority on any item from the dashboard
5. Audit log captures all override changes (who, when, old value, new value)
6. No regression in existing reorder math (all council fixes preserved)

## 7. Dependencies

| Dependency | Status | Blocking? |
|------------|--------|-----------|
| Phase 1-2 code (reorder engine) | Complete | No |
| Migrations 00001-00003 applied to Supabase | Pending | **Yes** — must run before adding new table |
| Phase 3 UI (dashboard) | In progress | No — override UI can be added to Phase 3 UI or as Phase 4 addon |
| Amazon unified-score Layer 0 | In progress (sibling repo) | No — external writer is optional; manual overrides work standalone |

---

*This scope document defines what we're building and why. See [[PRIORITY_OVERRIDES_PRD]] for technical specification and [[PRIORITY_OVERRIDES_SOP]] for operational procedures.*