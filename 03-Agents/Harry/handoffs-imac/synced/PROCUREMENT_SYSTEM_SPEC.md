# Procurement System Spec v1

> **Owner:** Ava | **Builder:** Harry | **Date:** 2026-03-20
> **Status:** DRAFT — awaiting Cem review

---

## 1. Problem Statement

The current procurement process lives entirely in Zero (PHP, PH-hosted). PO creation, split logic, receiving, and supplier pricing are all manual or hardcoded. As we scale down PH printing and expand marketplaces, we need:

1. **Automated reorder triggers** based on real-time inventory velocity
2. **Intelligent location splits** (US/UK/PH) based on demand, not gut feel
3. **Separate POs per destination** so China can ship cleanly and invoicing reconciles
4. **Currency-aware COGS tracking** — suppliers bill in RMB, USD, or GBP
5. **Full cost modeling** — case cost is just one component; shipping, packaging, and royalties matter

---

## 2. Data Sources (all in BigQuery)

### 2.1 Inventory (LIVE view)
- **View:** `zero_dataset.inventory`
- **Underlying tables:** `elcell_co_uk_barcode.t_stock_item`, `t_warehouse_item`, `t_warehouse`
- **Freshness:** Real-time via Datastream (last PO date: 2026-03-20)
- **Key fields:** `Item_Code`, `Warehouse`, `Free_Stocks`, `Sales_Last_7_Days`, `Sales_Last_30_Days`, `Ave_Daily_Sales`, `Reorder_Level`, `On_Order`, `Average_PO_Price`, `Supplier`
- **Warehouses with sales data:** PH (2,938 items), UK (2,502), FL (1,194)
- **Stock-only warehouses:** DE (775), CN (12), Transit (40)

### 2.2 Purchase Orders
- **Header:** `elcell_co_uk_barcode.t_purchase_order_return` — `f_document_no`, `f_document_date`, `f_supplier_code`, `f_warehouse`
- **Lines:** `elcell_co_uk_barcode.t_purchase_order_return_line` — `f_item_code`, `f_quantity`, `f_receive_quantity`, `f_buying_price`
- **Volume:** ~20,750 POs in 2026 YTD (includes internal transfers)
- **External suppliers (last 9mo):** ECELLSZ (77 POs), XINTAI (41), YIZE (31), SHENG (30), JIZHAN (23), TOKO (19), QICAI (10)
- **⚠️ No currency field on PO lines** — must infer from supplier mapping

### 2.3 Supplier Reference
- **Table:** `elcell_co_uk_barcode.t_supplier` — has `f_currency_code` but mostly NULL
- **Confirmed currencies (Cem, 2026-03-20):**
  - **RMB:** ECELLSZ, XINTAI, YIZE, SHENG, JIZHAN, QICAI, BIQUANSHENG, DYNAMIC8, HUAXING, JIAXING, RUIBO, TIANLING, TWINSTAR, SKY STAR
  - **USD:** TOKO, SAIBORO, BAOLLY, SANXING, WONDERS
  - **GBP:** KOCH MEDIA, MAINLINE

### 2.4 Unit Cost — Source of Truth

> **⚠️ `t_mfg_supplier_price` is STALE — do not use.** (e.g., HTPCR listed at ¥1.80 but actual PO price is ¥4-5 RMB)

**Source of truth = most recent PO price per item** from `t_purchase_order_return` + `t_purchase_order_return_line`, combined with `supplier_currency_map` for currency.

**Confirmed costs (Cem, 2026-03-20):**

| Product | Supplier | Currency | Current Cost | Source |
|---------|----------|----------|-------------|--------|
| HTPCR | XINTAI | RMB | ¥3.50 | Cem confirmed (POs show ¥4-5 — may include newer devices at premium) |
| HB6 (Clear MagSafe) | TOKO | USD | $1.90 | Cem confirmed |
| HB7 (Black MagSafe) | TOKO | USD | $1.90 | Cem confirmed |
| HB401 | ECELLSZ | RMB | ¥6.50 | Cem confirmed |
| HLBWH (Phone) | JIZHAN/SHENG | RMB | ¥7 | Cem confirmed |
| HLBWH (Kindle, PPR3/PPR5) | JIZHAN | RMB | ¥14 | Cem confirmed |
| HLBWH (iPad) | JIZHAN | RMB | ¥15 | Cem confirmed |
| HDMWH 900×400 | TOKO | USD | $1.76 | Cem confirmed |
| HDMWH 600×300 | TOKO | USD | $0.86 | Cem confirmed |
| HDMWH 250×300 | ECELLSZ | RMB | ¥2.80 | Cem confirmed |
| H8939 (Gaming Skin) | Vinyl roll | USD | $0.75/ft² | Cem confirmed — printed in-house on vinyl |
| HSTWH (Sticker) | Vinyl roll | USD | $0.75/ft² | Cem confirmed — printed in-house on vinyl |

**Vinyl cost is per-area, not per-unit.** Per-unit cost varies hugely by device:
- Controller skin (DS4CT/DS5CT): ~0.41 ft² → **$0.31**
- Laptop 16" (A2141PRO): ~1.84 ft² → **$1.38**
- PS5 Body (PS5BD): ~3.42 ft² → **$2.56**
- AirPods: ~0.15 ft² → **$0.11**

**Automation approach (Phase 4):** Scan EPS/PNG templates on Google Drive (`gdrive:`), extract image dimensions from metadata (pixels + DPI → mm → ft²), apply nesting waste factor (~1.3-1.5x), calculate per-unit cost per device code. No manual table needed.

**Logic:** For each item, pull the most recent `f_buying_price` from `t_purchase_order_return_line` joined to `t_purchase_order_return`. Pair with `supplier_currency_map` for currency code.

### 2.5 Orders (for velocity/split calculation)
- **View:** `zero_dataset.orders` — has `Buyer_Country`, `Custom_Label`, `PO_Location`, sales dates
- **Use `Buyer_Country` not `PO_Location`** for determining which location SHOULD fulfill (per SKU Parsing Rules)

---

## 3. Architecture

### 3.1 Split Algorithm

**Inputs:**
- Rolling 7-day sales velocity per item, per fulfillment region
- Current inventory levels per warehouse
- PH capacity cap (configurable — scales toward 0 as PH printing winds down)

**Region Mapping (from Buyer_Country):**
| Region | Fulfillment Location | Countries |
|--------|---------------------|-----------|
| US | Florida | US, CA, MX |
| UK/ROW | UK | GB, EU, AU, NZ, etc. |
| JP | PH | JP |
| Overflow | PH | Spillover when US/UK backlogged (holiday toggle) |

**Split Calculation:**
```
For each item needing reorder:
  1. Get 7-day velocity by region: vel_US, vel_UK, vel_PH
  2. Apply PH capacity cap (e.g., max 30% → decreasing to 0%)
  3. Calculate split ratios: ratio_US = vel_US / total_vel
  4. Multiply reorder qty × ratio = qty per destination
  5. Round up to nearest pack size (if applicable)
  6. Generate separate PO per destination
```

**Safety buffer:** 8 days of stock (matching Zero's current `Reorder_Level = Sales_7d × 8`)

### 3.2 PO Generation

**Frequency:** Weekly (matching current cadence — ~4 POs/week across 3-4 suppliers)

**Output per run:**
- 1 PO per supplier × per destination = e.g., ECELLSZ-US, ECELLSZ-UK
- Each PO includes: item codes, quantities, last unit price, currency, estimated total
- Format: Printable PDF + JSON for system ingestion

**Supplier grouping:** Items are grouped by their primary supplier from `t_mfg_supplier_price` or most recent PO supplier.

### 3.3 COGS Model

> "Cost of case is just a small part of costs" — Cem

**Full landed cost per unit:**

| Component | Source | Currency | Notes |
|-----------|--------|----------|-------|
| **Blank case cost** | `t_mfg_supplier_price` or last PO price | RMB/USD | Per product type, from supplier |
| **Shipping (CN→destination)** | TBD — manual input or table | USD | Per kg or per unit, varies by destination |
| **Packaging** | TBD — manual input | USD/RMB | Box, insert, poly bag, label |
| **Royalty** | 15% of net sales (standard) | USD/GBP | Per license, varies. Some fixed. |
| **Print/production** | Internal (PH/UK/FL labor) | USD/GBP/PHP | Per unit production cost at each location |
| **Freight (local last mile)** | Veeqo/carrier data | USD/GBP | Outbound shipping to customer |

**Phase 1:** Track blank cost + currency per PO line. Build supplier→currency mapping table.
**Phase 2:** Add shipping and packaging per-unit estimates (Cem to provide averages).
**Phase 3:** Full COGS model with royalty rates per license and production costs per location.

### 3.4 Currency Handling

**Approach:** Store all prices in source currency + currency code. Convert to USD at report time using a daily FX rate table.

**New table needed:** `supplier_currency_map`
```sql
CREATE TABLE supplier_currency_map (
  supplier_code TEXT PRIMARY KEY,
  default_currency TEXT NOT NULL,  -- 'RMB', 'USD', 'GBP'
  confirmed BOOLEAN DEFAULT FALSE,
  notes TEXT
);
```

**Immediate action:** Pre-populate from `t_supplier.f_currency_code` where available. Cem to confirm the ~10 NULL suppliers (likely all RMB for SZ-based ones).

---

## 4. China Office View

**What they need:** A simple web page showing:
1. Outstanding POs (not yet fully received) — grouped by destination
2. For each PO: supplier, items, quantities ordered vs received, destination warehouse
3. Action: Mark items as received → updates receive quantities
4. Action: Mark PO as shipped → captures ship date + tracking

**Tech:** Lightweight Next.js page reading from Supabase (or direct BQ if latency is okay). No auth needed initially (internal tool).

**This replaces:** The Zero PO receiving screen at `192.168.20.57`.

---

## 5. Implementation Plan

### Phase 1: Foundation (Week 1)
- [ ] Build `supplier_currency_map` in Supabase — pre-populate from BQ
- [ ] Cem confirms currencies for NULL suppliers (ECELLSZ, XINTAI, YIZE, SHENG, JIZHAN, SAIBORO, QICAI, BAOLLY)
- [ ] Cem provides missing COGS for: HB401, HB6, HB7, H8939, HDMWH, HSTWH
- [ ] Build velocity calculator: 7-day rolling sales by region by item_code (BQ query + Supabase cache)
- [ ] Build reorder trigger: items where `Free_Stocks < Reorder_Level` AND `On_Order = 0`

### Phase 2: PO Generator (Week 2)
- [ ] Split algorithm implementation (velocity ratios + PH cap)
- [ ] PO document generator (JSON + PDF)
- [ ] Group by supplier × destination
- [ ] Include last PO price + currency on each line
- [ ] Review interface: Cem approves POs before they go out

### Phase 3: China Receiving UI (Week 3)
- [ ] Outstanding PO list view (Supabase-backed)
- [ ] Receive goods action (update quantities)
- [ ] Ship-to-destination action (capture tracking)
- [ ] Basic dashboard: POs in transit, received, shipped

### Phase 4: COGS Dashboard (Week 4)
- [ ] Shipping cost input (per-route averages from Cem)
- [ ] Packaging cost input
- [ ] Full landed cost per product type per destination
- [ ] Margin analysis: revenue - landed COGS - royalty = gross margin per SKU type

---

## 6. Open Questions for Cem

1. ~~**Supplier currencies:**~~ ✅ CONFIRMED — RMB: ECELLSZ, XINTAI, YIZE, SHENG, JIZHAN, QICAI. USD: SAIBORO, BAOLLY, TOKO, SANXING.
2. **Missing COGS:** What's the blank cost for HB401, HB6 (Clear MagSafe), HB7 (Black MagSafe), H8939 (Gaming Skin), HDMWH (Desk Mat), HSTWH (Sticker)?
3. **Shipping costs:** Rough per-unit averages for CN→US, CN→UK? (We can refine later)
4. **Packaging costs:** Standard poly bag + insert per case — what's the unit cost?
5. **PH wind-down timeline:** When does PH printing go to zero? Gradual over 3mo? 6mo?
6. **Pack sizes:** Do suppliers require minimum order quantities or pack sizes (e.g., multiples of 50)?
7. **PO approval flow:** Do you want to approve every PO, or just review a weekly summary?

---

## 7. Key Data Gaps

| Gap | Impact | Resolution |
|-----|--------|------------|
| No currency on PO lines | Can't track actual cost per order | Build supplier→currency map + backfill |
| `t_mfg_supplier_price` incomplete | Missing 6 product types | Cem to provide |
| DE warehouse has no sales data | Can't calculate velocity for EU | Use orders view `Buyer_Country` instead |
| Amazon FBA locations not in inventory | FBA stock managed by Amazon | Exclude from procurement — separate system |
| Shipping/packaging costs not in BQ | Can't calculate true landed cost | Manual input table (Phase 4) |

---

*This spec covers the data layer and logic. Harry builds the tooling. Ava owns the split algorithm design and COGS model. Cem approves POs and provides missing cost inputs.*
