# Code Review — Phase 1+2 Build
**Date:** 2026-04-13 | **Reviewer:** feature-dev:code-reviewer agent

## Critical Issues (9)

| # | Issue | File | Impact |
|---|-------|------|--------|
| 1 | Downtrend check is dead code — reconstructed sales always ratio 1.0 | lib/inventory/reorder.ts | Downtrend flag never fires |
| 2 | Concurrent lock not atomic (SELECT then UPSERT) | app/api/cron/reorder-calc/route.ts | Duplicate runs possible |
| 3 | Stock mutations not atomic (read-then-write) | app/api/transfers/[id]/route.ts | Double deduction possible |
| 4 | Partial delivery stock imbalance (received_qty vs transfer.qty) | app/api/transfers/[id]/route.ts | Units vanish on damage |
| 5 | No auth on any routes | All API routes | Public access to all operations |
| 6 | Zone aggregation warehouse label bug | app/api/cron/best-sellers/route.ts | UNIQUE constraint conflicts |
| 7 | Stale exclusion bypassed with hardcoded nulls | lib/inventory/reorder.ts | Stale items get reordered |
| 8 | Transfer number collision under concurrency | app/api/transfers/generate/route.ts | UNIQUE constraint failures |
| 9 | DELIVERED_PENDING state missing from transfer state machine | app/api/transfers/[id]/route.ts | Council Fix #10 not implemented |

## Important Issues (3)

| # | Issue | File |
|---|-------|------|
| 10 | best_sellers_daily FK blocks zone-level rows | migration SQL |
| 11 | Partial index CURRENT_DATE evaluated once at creation | migration SQL |
| 12 | Lock release runs even if never acquired | reorder-calc route |

## Clean Files (no issues)
- lib/inventory/velocity.ts
- lib/inventory/allocation.ts
- lib/inventory/transfers.ts
- lib/types/database.ts
- app/api/health/route.ts
