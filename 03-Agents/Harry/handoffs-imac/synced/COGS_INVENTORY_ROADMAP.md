# COGS & Inventory Management Roadmap

> **Owner:** Ava (strategy) → Harry (build) | **Date:** 2026-03-20
> **Status:** DRAFT — Phase 1 ready for build

---

## 1. Vision

A unified cost and inventory system that answers three questions at any time:
1. **What does each product actually cost us?** (landed, not just blank price)
2. **What do we need to reorder, how much, and where should it go?**
3. **What's our real margin per SKU/product type/marketplace?**

---

## 2. Product Cost Reference (All confirmed by Cem, 2026-03-20)

### 2.1 Physical Blanks (ordered via PO pipeline)

| Product | Supplier | Currency | Unit Cost | Notes |
|---------|----------|----------|-----------|-------|
| HTPCR | XINTAI | RMB | ¥3.50 | Staple TPU case. POs show ¥4-5 for some devices — may vary by size |
| HB401 | ECELLSZ | RMB | ¥6.50 | Hard Case v2 |
| HB6 (Clear MagSafe) | TOKO | USD | $1.90 | |
| HB7 (Black MagSafe) | TOKO | USD | $1.90 | |
| HLBWH Phone | JIZHAN/SHENG | RMB | ¥7.00 | Device-size dependent ↓ |
| HLBWH Kindle/PPR3/PPR5 | JIZHAN | RMB | ¥14.00 | |
| HLBWH iPad | JIZHAN | RMB | ¥15.00 | |
| HDMWH 900×400 | TOKO | USD | $1.76 | |
| HDMWH 600×300 | TOKO | USD | $0.86 | |
| HDMWH 250×300 | ECELLSZ | RMB | ¥2.80 | |

### 2.2 Vinyl Products (NOT in PO pipeline — consumable roll restock)

**Raw material:** Vinyl roll @ **$0.75/ft²** (USD)

H8939 (Gaming Skins) and HSTWH (Stickers) are printed in-house on vinyl. No per-unit blanks to order — just restock rolls when low. But per-unit vinyl cost is critical for COGS.

**Per-unit cost = ft² consumed × $0.75**

| Product | Type | Sheets/unit | ft² per unit | Cost @ $0.75/ft² |
|---------|------|-------------|-------------|-------------------|
| H8939-DS4CT/DS5CT | Controller skin | 1 | ~0.41 | **$0.31** |
| H8939-SRSSCS | Xbox S console only | 1 | ~1.86 | **$1.40** |
| H8939-SRSSBD | Xbox S bundle (console+ctrl) | 2 | ~2.27 | **$1.71** |
| H8939-SWITCHBD | Switch bundle (console+JoyCons) | 2 | ~2.92 | **$2.19** |
| H8939-PS5BD | PS5 bundle (body+ctrl) | 2+ | ~3.42 | **$2.56** |
| H8939-A2141PRO | Laptop 16" | 1 | ~1.84 | **$1.38** |
| HSTWH-L | Sticker 2-pack | 2 | ~1.84 | **$1.38** |

**Key rules:**
- **BD suffix = Bundle** — console body + controller. 2+ print files = 1 product.
- **HSTWH = 2-pack** — 2 print files = 1 product.
- Cost calculation must sum ALL EPS files belonging to one SKU.
- Remaining device types: scan EPS templates on Google Drive for dimensions → auto-calculate ft² per device code.

### 2.3 Supplier Currency Map (confirmed by Cem)

| Currency | Suppliers |
|----------|-----------|
| **RMB** | ECELLSZ, XINTAI, YIZE, SHENG, JIZHAN, QICAI, BIQUANSHENG, DYNAMIC8, HUAXING, JIAXING, RUIBO, TIANLING, TWINSTAR, SKY STAR |
| **USD** | TOKO, SAIBORO, BAOLLY, SANXING, WONDERS |
| **GBP** | KOCH MEDIA, MAINLINE |

---

## 3. Full COGS Model (target state)

**Landed cost per unit = sum of all components:**

| # | Component | Source | Status |
|---|-----------|--------|--------|
| 1 | **Blank/material cost** | Last PO price (BQ) or vinyl ft² calc | ✅ Data available |
| 2 | **Shipping (CN → warehouse)** | Manual input per route | ❌ Need from Cem |
| 3 | **Packaging** (box, insert, poly bag, label) | Manual input per product type | ❌ Need from Cem |
| 4 | **Royalty** | 15% of net sales (standard), varies by license | ⚠️ Partial — need license-level rates |
| 5 | **Print/production labor** | Per unit at each location (PH/UK/FL) | ❌ Need from Cem |
| 6 | **Outbound shipping** (to customer) | Veeqo/carrier data | ⚠️ Extractable from Veeqo |

**Phase 1 covers component #1 only.** Components #2-6 are added progressively.

---

## 4. Inventory Management System

### 4.1 Current State (BQ — LIVE)
- **View:** `zero_dataset.inventory` (real-time via Datastream)
- **Warehouses with sales velocity:** PH (2,938 items), UK (2,502), FL (1,194)
- **Stock-only warehouses:** DE (775), CN (12), Transit (40)
- **Reorder logic in BQ:** `Reorder_Level = Sales_7d × 8` (8 days buffer)

### 4.2 Supabase Mirror (exists, needs refresh)
- **Table:** `blank_inventory` — last snapshot script: `scripts/snapshot_inventory.py`
- **View:** `v_inventory_alerts_v2` — alert levels: GREEN/YELLOW/RED/BLACK
- **Last snapshot:** ~Mar 12 — needs re-run to be current

### 4.3 Reorder Trigger Logic
```
FOR each item WHERE:
  Free_Stocks < Reorder_Level
  AND On_Order = 0
  AND Product_Group NOT IN ('PACKG', 'PROD-CON', 'PROD-SUPPLIES')
  AND Warehouse IN ('PH', 'UK', 'Florida')
DO:
  Calculate split ratios from 7-day velocity by Buyer_Country
  Generate separate PO per supplier × destination
  Include: item_code, qty, last_po_price, currency
```

### 4.4 Split Algorithm
| Region | Fulfillment | Countries |
|--------|-------------|-----------|
| US | Florida | US, CA, MX |
| UK/ROW | UK | GB, EU, AU, NZ, etc. |
| JP | PH | JP |
| Overflow | PH | Holiday spillover (toggle) |

- Use `Buyer_Country` from orders, NOT `PO_Location`
- PH has a configurable capacity cap (scaling toward 0 as printing winds down)
- Split at PO creation → separate POs per destination → China ships per PO

### 4.5 PO Volume
- ~1 run/week across 3-4 suppliers = 12-16 POs/month
- External suppliers (by volume): ECELLSZ, XINTAI, YIZE, SHENG, JIZHAN, TOKO, QICAI

---

## 5. Data Sources in BigQuery

| Table/View | What | Key Fields |
|-----------|------|------------|
| `zero_dataset.inventory` | Live inventory + velocity | Item_Code, Warehouse, Free_Stocks, Sales_7d/30d, Avg_Daily_Sales, Reorder_Level, On_Order, Avg_PO_Price, Supplier |
| `zero_dataset.orders` | Sales with buyer location | Custom_Label, Buyer_Country, Paid_Date |
| `elcell_co_uk_barcode.t_purchase_order_return` | PO headers | f_document_no, f_document_date, f_supplier_code, f_warehouse |
| `elcell_co_uk_barcode.t_purchase_order_return_line` | PO line items | f_item_code, f_quantity, f_receive_quantity, f_buying_price |
| `elcell_co_uk_barcode.t_supplier` | Supplier master | f_supplier_name, f_currency_code (mostly NULL — use our map) |

**⚠️ DO NOT USE `t_mfg_supplier_price`** — stale data (shows HTPCR at ¥1.80, actual is ¥3.50-5).

**Source of truth for unit cost = most recent f_buying_price from t_purchase_order_return_line per item.**

---

## 6. Build Phases

### Phase 1: Cost & Inventory Foundation (Week 1) — UNBLOCKED
- [ ] Create `supplier_currency_map` table in Supabase (pre-populated above)
- [ ] Build function: get latest PO price per item_code from BQ
- [ ] Re-run `snapshot_inventory.py` to refresh Supabase inventory mirror
- [ ] Build velocity calculator: 7-day rolling sales by region by item_code
- [ ] Build reorder trigger: flag items below reorder level with no orders pending

### Phase 2: PO Generator (Week 2)
- [ ] Split algorithm (velocity ratios + PH capacity cap)
- [ ] PO document generator (JSON + printable PDF)
- [ ] Group by supplier × destination (separate POs)
- [ ] Cem approval interface before POs go out

### Phase 3: China Receiving UI (Week 3)
- [ ] Outstanding PO list (Supabase-backed Next.js page)
- [ ] Receive goods action → update quantities
- [ ] Ship-to-destination action → capture tracking
- [ ] Replaces Zero PO receiving screen at 192.168.20.57

### Phase 4: COGS Dashboard (Week 4+)
- [ ] Add shipping cost per route (Cem to provide averages)
- [ ] Add packaging cost per product type
- [ ] Vinyl cost automation: scan EPS files on GDrive → extract dimensions → calculate ft² per device → multiply by $0.75
- [ ] Royalty rates per license
- [ ] Full margin analysis: revenue - landed COGS - royalty = gross margin per SKU type
- [ ] FX rate table for currency conversion (RMB/GBP → USD at report time)

---

## 7. Remaining Data Gaps

| Gap | Owner | Blocking |
|-----|-------|----------|
| Shipping cost per unit (CN→US, CN→UK) | Cem | Phase 4 |
| Packaging cost per product type | Cem | Phase 4 |
| Production labor cost per location | Cem | Phase 4 |
| Royalty rates by license | Cem | Phase 4 |
| PH wind-down timeline | Cem | Phase 2 (split cap) |
| EPS file dimensions for all skin devices | Auto-scan GDrive | Phase 4 |
| Vinyl cost for remaining H8939 device types | Derived from EPS scan | Phase 4 |

**Nothing blocks Phase 1-3.** Phase 4 gaps are filled progressively.

---

*Ava owns strategy, cost model design, and Phase 4 spec. Harry builds Phases 1-3. Cem provides cost inputs for Phase 4 when ready.*
