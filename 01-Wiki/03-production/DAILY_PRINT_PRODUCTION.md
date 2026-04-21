# Daily Print Production & Workflow Deep-Dive
**Head Case Designs | Print-on-Demand Operations**

## Executive Summary
This document outlines the end-to-end production workflow for Head Case Designs, transforming multi-channel orders into physical products using a high-efficiency print-on-demand model. The workflow integrates AI-driven verification and automated inventory management to support ~270K annual orders across 7 global warehouses.

---

## 1. Order Ingestion & Production Queue
Orders flow from 29 platforms (21 API, 8 CSV) into a centralized production database (Supabase).

### Ingestion Logic
- **Deduplication:** Orders are unique by `PlatformID + OrderNumber`. API-fetched orders take precedence over CSV uploads to prevent duplicates.
- **Priority Sorting:**
  1. **Expedited/Marketplace SLAs:** Amazon Prime, Next Day Shipping.
  2. **Order Age:** FIFO (First In, First Out) within priority tiers.
  3. **Batch Efficiency:** Grouping to minimize printer/material changeovers.

### The "Golden Batch" Grouping
To maximize throughput, the system groups the daily queue into three nested layers:
1. **Product Type (Layer 1):** Group all HTPCR (Clear Case), HDMWH (Desk Mat), or HLBWH (Leather Wallet) together. Different materials require different printer settings/heat.
2. **Device Model (Layer 2):** Group by IPH16, S24, etc. (Within a product type, different models may share templates or jig layouts).
3. **Design Code (Layer 3):** Group identical designs (e.g., MAR - Marauder's Map) to minimize print file loading time and allow for batch quality inspection.

```text
[Daily Queue] 
   └── [HTPCR] 
       ├── [IPH16] 
       │   ├── [MAR x10] <-- Printed in one jig
       │   └── [HOP x5]
       └── [IPH15]
           └── [MAR x8]
```

---

## 2. Print File Generation & Retrieval
The bridge between the digital SKU and the physical product.

### SKU Decomposition
- **SKU:** `HTPCR-IPH16-HPOTDH37-HOP`
- **Physical Blank:** `HTPCR` (Type) + `IPH16` (Device)
- **Digital Source:** `HPOTDH37` (Design) + `HOP` (Variant)

### Retrieval & Pre-Processing
- **Storage:** PSD files (~128MB) stored in a tiered cloud structure (High-freq vs. Archive).
- **Template Mapping:** The system maintains a `Template_Map` table:
  - `ProductType + DeviceModel` -> `Production_Template_ID`.
  - Example: `HTPCR-IPH16` uses `Template_V2_Phone_Large`.
- **The "Flattening" Cache:**
  - High-volume designs (e.g., LFC Home Kit, HP Marauder's Map) are pre-rendered into production-ready PDFs/TIFFs for each Product Type.
  - Reduces per-order processing time from ~30s (PSD render) to <1s (Retrieval).

---

## 3. Print Production
Managed by the Philippines central hub (42 staff).

### Daily Schedule
- **Baseline:** ~600 - 700 units/day.
- **Peak (Dec):** ~1,600 units/day.
- **Shift Management:** 24/7 rotation during Q4 to handle surge volume.

### Workflow
1. **Pull Blanks:** Operators pull physical stock based on the "Blank Requirement List" (e.g., "Pull 50x HTPCR-IPH16").
2. **Jig Loading:** Products are placed into custom jigs (trays) matched to the printer bed.
3. **Printing:** Print server pushes the batched print files to the Mimaki/Roland UV printers.
4. **Post-Print QC:** Visual check for ink adhesion, color accuracy, and alignment.

---

## 4. Vision-Based SKU Verification (AI-Verify)
Using Gemini 2.5 Flash Vision to eliminate human error at the packing station.

### Mobile Web App Flow (The "Packer's Assistant")
1. **Scan:** Packer scans the barcode on the shipping label (Expected SKU: `HTPCR-IPH16-HPOTDH37-HOP`).
2. **Photo:** Packer places the finished case under a fixed tablet/phone mount and snaps a photo.
3. **Verify:**
   - Image + Expected SKU description sent to Gemini Vision.
   - **Gemini Query:** "Does this case show the 'Harry Potter Hogwarts Pattern' on a 'TPU Clear' case for an 'iPhone 16'?"
4. **Result:**
   - ✅ **MATCH:** Green screen, print shipping label, move to next.
   - ❌ **MISMATCH:** Red screen, "Expected: Harry Potter, Found: Liverpool FC". Flag for reprint/restock.

### Reference Database
- **Images:** High-res renders of every SKU (Design + Product Type) indexed in Supabase.
- **Metadata:** Design descriptions (brand, color, key features) for Gemini grounding.

---

## 5. Packing & Fulfillment

### Verification to Ship
- Once Gemini confirms the match, the system triggers the final label print.
- **Packing Material:** Matched to Product Type (e.g., bubble mailer for phone cases, tube for desk mats).
- **Consolidation:** If one order has 3 items, the system waits for all 3 "AI-Verify" passes before flagging the order as "Ready to Pack."

### Inventory Write-Off
- Fulfillment triggers an immediate decrement of physical stock:
  - `UPDATE stock SET quantity = quantity - 1 WHERE type = 'HTPCR' AND device = 'IPH16'`
- Order status is pushed back to the 29 platforms via API or CSV export.

---

## 6. Inventory Impact & Replenishment

### Tracking the "Blank"
Inventory is tracked at the **Blank SKU** level (`ProductType-DeviceModel`), not the finished design level.

- **Lead Time Tracking:** China suppliers (15-30 days).
- **Velocity Alerts:** System calculates 7-day and 30-day burn rates.
- **Thresholds:**
  - `Safety Stock = (Max Daily Use * Max Lead Time)`.
  - Example: If IPH16 cases sell 100/day and lead time is 20 days, trigger reorder at 2,000 units.

### Daily Production Report
Automated summary sent to management:
- **Throughput:** Units printed vs. Target.
- **Error Rate:** % Mismatches caught by AI-Verify.
- **Stock Outs:** Blanks that reached zero (preventing new orders).

---

## 7. Automation Opportunities & ROI

| Process Step | Manual Cost | AI/Automation Solution | Est. ROI |
| :--- | :--- | :--- | :--- |
| **Order Grouping** | High (Human error in batching) | N8N Orchestration | 15% throughput increase |
| **File Rendering** | Medium (Wait times for PSDs) | Auto-Flattening Service | 50% reduction in prep time |
| **Packing QC** | Very High (Returns/Resends) | Gemini Vision Verification | **95% reduction in wrong-item-sent** |
| **Reordering** | Low (Occasional stockouts) | Predictive Inventory AI | 20% reduction in tied-up capital |

### Implementation with N8N
- **Workflow 1:** [Order Arrives] -> [Decompose SKU] -> [Check Local Render Cache] -> [Trigger Render if Missing].
- **Workflow 2:** [Inventory < Threshold] -> [Check Supplier Lead Time] -> [Draft Purchase Order for Approval].

---

## Process Flow Diagram

```text
  [MARKETPLACES]
        │ (API/CSV)
  [CENTRAL DB (SUPABASE)] ───▶ [N8N BATCHING] ───▶ [PRINT QUEUE]
                                                      │
  [PHYSICAL BLANKS] ──────────▶ [UV PRINTING] ◀───────┘
                                     │
                               [QC & COOLING]
                                     │
  [SHIPPING LABEL] ──────────▶ [GEMINI VISION] ◀────── [FINISHED PRODUCT]
        │                            │
        │                            ├─── [MATCH] ───▶ [PACK & SHIP] ──▶ [INV -1]
        └────────────────────────────┘
                                     └─── [MISMATCH] ─▶ [REPRINT / RE-PULL]
```

*Document created by Clawdbot for Head Case Designs Production Team.*

## Related
- [[wiki/03-production/PRINT_FILE_PIPELINE|Print File Pipeline]] — TIFF/EPS automation target
- [[wiki/03-production/SOP_DAILY_PRINT_PRODUCTION|SOP: Daily Production]] — Standard operating procedure
- [[wiki/23-drew-handover/PATRICK_WORKFLOW_PICKLIST_TO_IMAGE|Patrick's Workflow]] — PO → Pick List → Image pipeline
- [[wiki/04-shipping/SHIPPING_CARRIER_RULES|Shipping Carrier Rules]] — Carrier selection feeds into production
- [[wiki/23-drew-handover/VEEQO_REPLACEMENT_ANALYSIS|Veeqo Replacement]] — New order management replacing Zero
- [[wiki/06-design-automation/DESIGN_SYSTEM|Design System]] — Design files used in production
