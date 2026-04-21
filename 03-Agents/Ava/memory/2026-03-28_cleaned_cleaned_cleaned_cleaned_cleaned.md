# 2026-03-28 (Saturday) — HB401 Sprint Deadline Day

## Decisions
- **Fulfillment Portal Architecture**: Use FastAPI + Next.js + Supabase on Cloud Run.
- **Logistics**: Mandatory use of Amazon Buy Shipping for protection.

## Knowledge
- **Data Integrity**: Tracking writebacks must use a dedicated `order_tracking` table in Aurora; direct writes to Zero tables are prohibited.