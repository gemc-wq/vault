# Inventory Ordering App — Build State
**Last updated:** 2026-04-13 | **Builder:** Athena via Claude Code Agent Teams

## Build Progress

| Phase | Status | Lines | Key Files |
|-------|--------|-------|-----------|
| **1: Schema + Types + Math** | DONE | 1,701 | supabase/migrations/00001*.sql, lib/types/database.ts, lib/inventory/*.ts |
| **2: Data Pipeline + API** | DONE | ~1,200 | app/api/cron/*, app/api/transfers/*, app/api/health/* |
| **3: Portal UI** | NEXT | — | Transfers page, enhanced dashboard, zone stock view |
| **4: China Portal** | PENDING | — | Mandarin UI, PO download, packing list, invoice upload |
| **5: Shadow Mode** | PENDING | — | Comparison engine vs Zero output |

## Phase 3 Scope (Portal UI)

1. **Internal Transfers page** — /app/transfers/page.tsx
   - List suggested transfers with approve/reject
   - Tracking number input on confirmation
   - Status badges (SUGGESTED/CONFIRMED/SHIPPED/RECEIVED)
   - Filter by status, destination, priority

2. **Enhanced Dashboard** — Update /app/page.tsx
   - Zone stock summary cards (Zone US / Zone UK)
   - Data freshness indicator (green/red based on /api/health)
   - PH stock-out alert banner
   - Best sellers widget

3. **Zone Stock View** — /app/inventory/zones/page.tsx
   - Zone US stock (FL + PH share) vs Zone UK stock (UK + PH share)
   - Proportional PH allocation visualization
   - Days of cover per zone with alert colors

4. **Reorder Queue Enhancement** — Update /app/reorder/page.tsx
   - Add downtrend warning badges
   - Show approval tier per PO
   - Zone-aware quantities

## What Already Works
- Dashboard (basic summary cards)
- Inventory table (warehouse/alert filters)
- Reorder queue (generate/approve/reject/batch)
- PO batches (grouped view)
- All Phase 1 math engine functions
- All Phase 2 API routes

## Supabase Migration
Migration SQL at supabase/migrations/00001_inventory_ordering_v2.sql has NOT been run yet.
Must be applied to Supabase before Phase 3 UI can connect to new tables.

## Run Migration
```sql
-- Copy contents of supabase/migrations/00001_inventory_ordering_v2.sql
-- Paste into Supabase SQL Editor and execute
-- Verify: SELECT count(*) FROM warehouses; (should return 6)
```
