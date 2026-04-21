# 2026-03-28 (Saturday) — HB401 Sprint Deadline Day

## Decisions
- **Architecture & Data**: Fulfillment Portal will use FastAPI + Next.js + Supabase on Cloud Run. Tracking writebacks must use a dedicated `order_tracking` table in Aurora (never write directly to Zero tables).
- **Logistics**: Mandatory Amazon Buy Shipping for protection;