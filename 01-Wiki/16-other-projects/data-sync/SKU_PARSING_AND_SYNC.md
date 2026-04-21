# SKU Parsing Rules & BigQuery → Supabase Sync

## SKU / Custom Label Format

```
HC-IPH16-HPOTDH37-HOP
│   │      │       │
│   │      │       └── Design variant (digital file)
│   │      └────────── Design/Lineup code (digital file)
│   └───────────────── Device model (stockable unit)
└───────────────────── Product type (physical product)
```

### Segments

| Segment | Meaning | Examples |
|---------|---------|---------|
| **Product Type** (1st) | Physical product stocked | HC, HTPCR, HLBWH, HDMWH, HHYBK, HA805, HB401 |
| **Device** (2nd) | The stockable unit | IPH16, IPH16PMAX, IPHSE4, G780F, S918X, DS5CT |
| **Design Code** (3rd) | Digital print file — irrelevant for inventory | HPOTDH37, PNUTHAL, etc. |
| **Design Variant** (4th+) | Design variant — irrelevant for inventory | HOP, CSW, etc. |

### Key Rule: Inventory = Product Type + Device ONLY
- Designs are digital files applied at print time
- Inventory tracks **blank physical products** (product type + device)
- Replenishment from China for blank stock

---

## Inventory Mapping Rules

### Inventory Standardised to Modern HC Format (2026-02-17)
**Legacy inventory had bare device codes** (e.g., `IPH16` instead of `HC-IPH16`).
**We added `HC-` prefix to all bare device codes** so inventory matches the modern SKU format.

Now ALL matching is **direct** — `product_type_code || '-' || device_code` = `item_code`:

| Orders SKU | Inventory item_code | Match |
|---|---|---|
| `HC-IPH16-HPOTDH37-HOP` | `HC-IPH16` | ✅ Direct |
| `HC-G780F-DESIGN-VAR` | `HC-G780F` | ✅ Direct |
| `HTPCR-IPHSE4-DESIGN-VAR` | `HTPCR-IPHSE4` | ✅ Direct |
| `HLBWH-IPH16-DESIGN-VAR` | `HLBWH-IPH16` | ✅ Direct |

### Mapping Function (Supabase)
```sql
-- Simple direct match — no prefix stripping needed
inventory_key_for_order(product_type_code, device_code)
-- Always returns: product_type_code || '-' || device_code
```

### Future Products
Always use the standard format: `ProductType-Device-Design-Variant`
This ensures consistent matching between orders and inventory.

---

## Excluded Items

| Prefix | Description | Action |
|--------|-------------|--------|
| `Z%` | Legacy items no longer managed | Excluded from inventory |
| `H8%` | PS5 skins (H8939, H8940) — legacy stock | Excluded from inventory |

---

## BigQuery Source

### Connection
- **Project:** `instant-contact-479316-i4`
- **Dataset:** `zero_dataset`
- **Auth:** gcloud CLI → `gcloud auth print-access-token`
- **API:** `POST https://bigquery.googleapis.com/bigquery/v2/projects/{project}/queries`

### Tables

**orders** (2.79M rows, Nov 2019 → present)
| Column | Type | Notes |
|--------|------|-------|
| Sales_Record_Number | STRING | Unique ID |
| Paid_Date | DATE | |
| Dispatch_Date | DATE | |
| Custom_Label | STRING | **The SKU — parse this** |
| Quantity | STRING | Cast to INTEGER |
| Buyer_Country | STRING | |
| Status | STRING | |
| Is_Refunded | STRING | Cast to BOOLEAN |
| Currency | STRING | |
| Net_Sale | STRING | Cast to NUMERIC |
| GBP_Price | STRING | Cast to NUMERIC |
| GBP_Exchange_Rate | STRING | Cast to NUMERIC |
| Marketplace | STRING | eBay UK, Amazon US, etc. |
| TransactionID | STRING | |
| PO_Date | DATE | |
| PO_Location | STRING | |
| Brand | STRING | |
| Product | STRING | |
| Unit | STRING | |

**inventory** (78K rows)
| Column | Type | Notes |
|--------|------|-------|
| Warehouse | STRING | UK, Florida, PH, DE, CN, Amazon, Transit |
| Product_Unit | STRING | |
| Item_Code | STRING | **The inventory key** |
| Description | STRING | |
| Product_Group | STRING | |
| Free_Stocks | INT64 | Current available stock |
| Supplier | STRING | |
| Date_Created | DATE | |
| Last_PO_Date | DATE | Key filter: 2024+ = active |
| Last_PO_Qty | INT64 | |
| POs_Not_Received | STRING | |
| Average_PO_Price | NUMERIC | |
| On_Order | INT64 | |
| Sales_Last_30_Days | INT64 | |
| Sales_Last_7_Days | INT64 | |
| Ave_Daily_Sales_or_Sales_divided_7 | FLOAT64 | → avg_daily_sales |
| Reorder_Level_or_Sales_times_8 | FLOAT64 | → reorder_level |

---

## Supabase Target

### Project: auzjmawughepxbtpwuhe (Orders & Inventory)
- See `Brain/Credentials/supabase.md` for connection details

### Sync Rules
1. **Orders:** Sync from 2025-01-01 onwards only
2. **Inventory:** Only active items:
   - Items with Last PO Date >= 2024-01-01
   - PLUS items matching any SKU that sold in 2025+
   - EXCLUDE Z% and H8% prefixes
3. **Type conversions:** BigQuery stores most fields as STRING → cast to proper types
4. **is_refunded:** 'Yes'/'True'/'1' → true, else false
5. **ON CONFLICT:** orders use DO NOTHING (skip dupes), inventory uses DO UPDATE (upsert)

### Auto-Parse Trigger
When an order is inserted with `custom_label`, the trigger automatically populates:
- `product_type_code` — first segment
- `device_code` — second segment
- `design_code` — third segment
- `design_variant` — fourth+ segments

### Views Available
| View | Purpose |
|------|---------|
| `v_orders_with_inventory` | Orders matched to inventory via HC-aware mapping |
| `v_stock_consumption` | Units sold per item vs current stock + days remaining |
| `v_sales_by_product_type` | Revenue/units by product type (HC, HTPCR, etc.) |
| `v_sales_by_device` | Revenue/units by device with inventory key |
| `v_inventory_alerts` | Low stock / out of stock / reorder alerts |
| `v_unmatched_skus` | Orders with no matching inventory record |

### Functions Available
| Function | Purpose |
|----------|---------|
| `parse_sku(sku TEXT)` | Splits SKU into product_type, device, design, variant |
| `inventory_key_for_order(product_type, device)` | Returns correct inventory item_code (HC-aware) |
| `get_inventory_for_sku(sku TEXT)` | Full inventory lookup for any SKU |

---

## Sync Script
Location: `C:\Users\gemc\clawd\scripts\bq_to_supabase_sync.ps1`
- PowerShell script, runs in batches of 5000 from BigQuery
- Inserts via Supabase Management API in chunks of 200-500
- Handles type conversions, NULL values, quote escaping
- Idempotent (safe to re-run)

### Current State (2026-02-17)
- **Orders synced:** 304,778 (Jan 2025 → Feb 2026)
- **Inventory synced:** 9,805 rows (active items only)
- **SKU parsing:** Working, auto-triggers on insert

---

*Updated: 2026-02-17 by Harry*
