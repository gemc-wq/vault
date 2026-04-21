# Zero 2.0 Production Lane Automation — Build Spec

**Owner:** Jay Mark (Implementation)  
**Source:** Ava (CPSO) + Harry (COO)  
**Date:** 2026-04-01  
**Status:** Ready for Build

---

## Overview

Automated image generation pipeline for Zero production orders. Monitors BigQuery for new PO batches, checks if product images exist on S3, and triggers ListingForge when images are missing.

---

## Data Sources (BigQuery)

### 1. PO Header Table
**Dataset:** `instant-contact-479316-i4.elcell_co_uk_barcode`  
**Table:** `t_amalgamated_po`

| Field | Type | Description |
|-------|------|-------------|
| `f_HptId` | INT64 | HPT PO Number (= HPT_PO_Number in spreadsheet) |
| `f_POBatchNo` | INT64 | Batch number (= po_batch in URL) |
| `f_WarehouseName` | STRING | UK / FL / PH |
| `f_PhoneCode` | STRING | Device code (IPH13, IPH14, etc.) |
| `f_Status` | STRING | Live / Complete / etc. |
| `f_DateAdded` | DATETIME | PO creation timestamp |

### 2. PO Line Items Table
**Table:** `t_amalgamated_po_line`

| Field | Type | Description |
|-------|------|-------------|
| `f_HptId` | INT64 | FK to header |
| `f_CustomLabel` | STRING | **Full SKU** — image gen trigger (e.g., `HB401-IPH16PMAX-DRGBZCAS-SHE`) |
| `f_ProductCode` | STRING | Blank type (TP, LB, B4, B6, B7, BC, etc.) |
| `f_Quantity` | INT64 | Qty to produce |
| `f_QuantityReceived` | INT64 | Qty received (0 = not started) |
| `f_SageServer` | STRING | UK / US |
| `f_POType` | STRING | AMG_UK1 / AMG_US1 / etc. |
| `f_SageDocumentNumber` | STRING | Sage reference |
| `f_SageDateCreated` | DATETIME | Sage timestamp |

### 3. Production Tracker Tables
**Dataset:** `instant-contact-479316-i4.production_tracker`

| Table | Purpose |
|-------|---------|
| `t_scanned_records_v2` | Pick/scan activity (1.1M records, live) |
| `t_uk_stocks` / `t_fl_stocks` | Inventory levels |
| `t_pre_goods_in` | Goods-in tracking (stale since Jan 2026) |
| `t_print_out` | Print completion (stale since Oct 2025) |
| `t_uk_logs` / `t_fl_logs` | Audit logs (stale since 2018) |

---

## SKU Parsing Logic

Parse `f_CustomLabel` to extract:

```
Format: {PREFIX}-{DEVICE}-{DESIGN}-{VARIANT}
Example: HB401-IPH16PMAX-DRGBZCAS-SHE

- PREFIX: HB401, HC, HB6CR, etc. (brand/product line)
- DEVICE: IPH16PMAX, IPH13, IPADAIR20, etc.
- DESIGN: DRGBZCAS, FCBCKT8, ASSAWGRA, etc.
- VARIANT: SHE, AWY, YNA, BLK, etc. (color/finish)
```

---

## Image Check Endpoint

Check if image exists on S3:

```
https://elcellonline.com/atg/{DESIGN}/{VARIANT}/{PREFIX}-{DEVICE}-1.jpg
```

Example:
```
https://elcellonline.com/atg/DRGBZCAS/SHE/HB401-IPH16PMAX-1.jpg
```

**HTTP HEAD request** — check for 200 vs 404.

---

## Automation Pipeline (Agentic Flow)

```
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: POLL                                                   │
│  Query BQ every 5 minutes for new Live POs                      │
│  WHERE f_Status = 'Live' AND f_DateAdded > last_check           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: FETCH LINES                                            │
│  JOIN t_amalgamated_po_line on f_HptId                          │
│  Get all line items for the PO batch                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: PARSE SKU                                              │
│  Extract DESIGN, DEVICE, VARIANT, PREFIX from f_CustomLabel     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: CHECK S3                                               │
│  HEAD request to elcellonline.com/atg/{DESIGN}/{VARIANT}/...    │
│  If 200 → image exists, skip                                    │
│  If 404 → image missing, proceed                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ (404)
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: TRIGGER LISTINGFORGE                                   │
│  POST to ListingForge API with:                                 │
│  - design_code (from SKU)                                       │
│  - device_code (from SKU)                                       │
│  - blank_type (f_ProductCode)                                   │
│  - po_reference (f_HptId)                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 6: LOG & UPDATE                                           │
│  - Write to local tracking table (image_gen_queue)              │
│  - Update t_scanned_records_v2 when complete                    │
│  - Deduct from t_uk_stocks / t_fl_stocks as needed              │
│  - Log to t_uk_logs / t_fl_logs (if we fix the sync)            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Notes

### BigQuery Auth
- Use Application Default Credentials (gcloud auth)
- Project: `instant-contact-479316-i4`
- Query via `bq` CLI or Python BigQuery client

### Polling Strategy
- Poll every 5 minutes during business hours
- Track `last_checked_timestamp` in local state
- Query: `SELECT * FROM t_amalgamated_po WHERE f_Status = 'Live' AND f_DateAdded > @last_check`

### Error Handling
- Retry S3 checks 3x with backoff
- Log failures to local error queue
- Alert on >10 consecutive failures

### Rate Limiting
- Respect ListingForge API limits
- Batch image gen requests (max 10/min)
- Queue and process asynchronously

---

## Database Schema (Local Tracking)

```sql
CREATE TABLE image_gen_queue (
    id SERIAL PRIMARY KEY,
    hpt_id BIGINT NOT NULL,
    custom_label VARCHAR(255) NOT NULL,
    design_code VARCHAR(50),
    device_code VARCHAR(50),
    variant VARCHAR(50),
    prefix VARCHAR(50),
    s3_url VARCHAR(500),
    s3_status VARCHAR(20), -- 'exists', 'missing', 'error'
    listingforge_job_id VARCHAR(100),
    status VARCHAR(20), -- 'pending', 'processing', 'complete', 'failed'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## Success Criteria

1. ✅ Detect new PO batches within 5 minutes of creation
2. ✅ Parse 100% of SKUs correctly from f_CustomLabel
3. ✅ Check S3 image existence with <500ms latency
4. ✅ Trigger ListingForge for all missing images
5. ✅ Zero manual intervention for standard POs

---

## Open Questions

1. **ListingForge API endpoint** — confirm URL and auth method
2. **S3 bucket structure** — confirm elcellonline.com/atg/ path format
3. **Error alerting** — Slack? Email? Dashboard?
4. **Deployment target** — Cloud Run? VPS cron? Local daemon?

---

**Next Step:** Jay Mark to review and confirm open questions before implementation.
