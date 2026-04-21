# Priority Overrides — Product Requirements Document

> **Owner:** Cem | **Date:** 2026-04-15
> **Status:** DRAFT — awaiting review
> **Version:** 1.0
> **Addresses:** LLM Council Review V2 Gap #5 (GPT-5.4 Business Logic)
> **Target Phase:** Phase 4
> **Prerequisite:** Migrations 00001-00003 applied to Supabase

---

## 1. Overview

Add per-item priority overrides to the procurement reorder engine. Currently, `priority_multiplier` is group-level only (from `product_group_config`). This PRD adds an item-level table that any authenticated source can write to, consumed by the reorder engine during calculation.

**Integration point:** `lib/inventory/reorder.ts:getReorderQty()` and `lib/inventory/allocation.ts:calculateAllocation()` both use `priority_multiplier` to scale `coverDays`. Currently sourced from `product_group_config`. After this change: check `priority_overrides` first, fall back to `product_group_config`.

---

## 2. Data Model

### 2.1 New Table: `priority_overrides`

```sql
CREATE TABLE priority_overrides (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  item_code       TEXT NOT NULL,
  multiplier      NUMERIC(4,2) NOT NULL DEFAULT 1.0,
  source          TEXT NOT NULL,
  reason          TEXT,
  severity        TEXT DEFAULT 'MEDIUM',
  created_by      UUID REFERENCES users(id),
  expires_at      TIMESTAMPTZ,
  is_active       BOOLEAN NOT NULL DEFAULT true,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT chk_multiplier_range CHECK (multiplier >= 0.5 AND multiplier <= 3.0),
  CONSTRAINT chk_severity CHECK (severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
  CONSTRAINT uk_item_source UNIQUE (item_code, source)
);
```

**Design decisions:**

| Decision | Choice | Rationale |
|----------|--------|-----------|
| One row per (item_code, source) | UNIQUE constraint | Each source gets exactly one active override per item |
| Multiplier range 0.5–3.0 | CHECK constraint | Prevents runaway orders |
| Expiry via `expires_at` | Nullable TIMESTAMPTZ | NULL = permanent. Non-null = auto-ignored. No cleanup cron needed |
| Source as TEXT not ENUM | Extensibility | New sources added without migration |
| `is_active` boolean | Soft-delete | Deactivate without losing audit trail |

### 2.2 RLS Policies

- ADMIN: full access
- MANAGER: read all, write/update manual source only
- CHINA_OPS / WAREHOUSE: read-only

### 2.3 Audit Integration

All changes captured in existing `audit_log` table via trigger (`trg_audit_priority_overrides`).

---

## 3. Reorder Engine Changes

### 3.1 Override Resolution Logic

New `resolveMultiplier()` function in `lib/inventory/reorder.ts`:
1. Check `priority_overrides` for active, non-expired overrides on this item
2. If found: use highest multiplier (multiple sources → MAX wins)
3. If not: fall back to `product_group_config.priority_multiplier`
4. If no group config: default 1.0

### 3.2 Data Loading

Both `app/api/reorder/generate/route.ts` and `app/api/cron/reorder-calc/route.ts` load overrides after loading product group configs.

### 3.3 ZoneItem Construction Change

Currently:
```typescript
priority_multiplier: configs.get(data.product_group)?.priority_multiplier ?? 1.0
```

Changes to:
```typescript
priority_multiplier: resolveMultiplier(itemCode, overrideMap, configs.get(data.product_group))
```

### 3.4 No Other Engine Changes Required

All council fixes preserved. This is a data-source change, not a math change.

---

## 4. API Specification

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/priority-overrides` | GET | Any role | List overrides (filter by item_code, active_only) |
| `/api/priority-overrides` | POST | ADMIN, MANAGER | Create/update manual override (UPSERT on item_code+source) |
| `/api/priority-overrides/external` | POST | API key | External writer endpoint (batch support, rate limited) |
| `/api/priority-overrides/:id` | DELETE | ADMIN, MANAGER, API key | Soft-deactivate (sets is_active=false) |

---

## 5. Dashboard UI

- **Override badges** on reorder queue (red/amber/blue/grey by severity)
- **Override management page** (`app/priority-overrides/page.tsx`) with filters
- **Quick override** from inventory page (Set Priority button → modal)

---

## 6. Effect on Reorder Math

| Scenario | Multiplier | Cover Days (standard) | Cover Days (best seller) |
|----------|-----------|----------------------|-------------------------|
| Default | 1.0x | 30 | 45 |
| Group (HB401) | 1.5x | 45 | 68 |
| Item HIGH | 2.0x | 60 | 90 |
| Item CRITICAL | 3.0x | 90 | 135 |
| De-prioritised | 0.5x | 15 | 23 |

---

## 7. Rollback Plan

1. **Immediate:** Set `is_active = false` on all rows → engine falls back to group config
2. **Code revert:** One-line change in each route file
3. **Nuclear:** Drop table, remove migration

Default state = identical to current behavior.

---

## 8. Migration File

Full SQL in `supabase/migrations/00004_priority_overrides.sql` (see local repo for complete DDL including indexes, RLS, and audit trigger).

---

*See [[PRIORITY_OVERRIDES_SCOPE]] for boundaries and [[PRIORITY_OVERRIDES_SOP]] for operational procedures.*