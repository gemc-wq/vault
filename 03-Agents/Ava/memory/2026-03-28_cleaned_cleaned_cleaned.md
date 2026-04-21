# 2026-03-28 (Saturday) — HB401 Sprint Deadline Day

## Decisions
- **Architecture**: Fulfillment Portal will use FastAPI + Next.js + Supabase on Cloud Run.
- **Data Integrity**: Tracking writebacks must use a dedicated `order_tracking` table in Aurora (never write directly to Zero tables).
- **Logistics**: Mandatory use of Amazon Buy Shipping for protection.