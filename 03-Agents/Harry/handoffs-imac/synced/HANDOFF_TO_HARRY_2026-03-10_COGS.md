# HANDOFF TO HARRY — COGS per Product Group
*Date: 2026-03-10 | From: Ava | Priority: HIGH — blocks PULSE Phase 3 profit scoring*

## What You're Building
A `product_group_cogs` table in Supabase with cost-of-goods-sold per product group. This feeds PULSE's profit-weighted opportunity scoring.

## Product Groups
Group products by manufacturing similarity, NOT by individual SKU:

| Group | Product Type Codes | Why Grouped |
|---|---|---|
| Phone Back Cases | HTPCR, HC, HB6CR, H7805 | Same print process, similar materials |
| Leather Wallets | HLBWH | Different material, higher cost |
| Desk Mats | HDMWH | Large format, different print |
| Vinyl Skins | H8939, HST | Cut vinyl, different process |
| Console Cases | (console codes) | Larger form factor |
| Laptop Cases/Skins | (laptop codes) | Mixed |

## Table Schema
```sql
CREATE TABLE product_group_cogs (
    id SERIAL PRIMARY KEY,
    group_name TEXT UNIQUE NOT NULL,
    product_type_codes TEXT[] NOT NULL,  -- Array of codes in this group
    material_cost NUMERIC(10,2),         -- Per unit
    print_cost NUMERIC(10,2),            -- Per unit
    packaging_cost NUMERIC(10,2),        -- Per unit
    total_cogs NUMERIC(10,2) NOT NULL,   -- Sum of above
    marketplace_fee_pct NUMERIC(5,2),    -- Average marketplace take rate
    shipping_cost_avg NUMERIC(10,2),     -- Average shipping per unit
    notes TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## What Ava Needs Back
- The table populated with real numbers from Cem/finance
- If exact numbers aren't available, get ranges (min/max) and we'll use midpoints
- This directly feeds the profit-weighted scoring formula:
  `Expected Profit = Units × (Sell Price - COGS - Marketplace Fee - Shipping)`

## Supabase Connection
- Host: db.auzjmawughepxbtpwuhe.supabase.co:5432
- DB: postgres
- User: postgres
- Password: [REDACTED_DB_PASSWORD]
- SSL: require

## Deadline
**March 11, 2026 (TOMORROW)** — Cem wants this tight. One day.

— Ava
