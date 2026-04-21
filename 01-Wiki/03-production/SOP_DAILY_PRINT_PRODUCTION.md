# SOP: Daily Print Production
*Version: DRAFT 0.1 | Created: 2026-02-11 | Status: IN DEVELOPMENT*

---

## Purpose
Standard operating procedure for the daily print-on-demand production cycle across three sites.

---

## Sites & Capabilities

| Site | Role | Equipment | Staff |
|------|------|-----------|-------|
| Philippines | Central hub + overflow | UV printers (cases) | 35-40 total |
| UK | Local fulfillment | UV printers, skin printers (H89), laser cutter | 1 printer + 2 packers |
| US (Florida) | Local fulfillment | Skin printers (H89), sticker cutters | 1 printer + 2 packers |

---

## Daily Production Flow

### Step 1: Order Download & Sorting
- [ ] Veco pulls orders automatically (every 2 minutes)
- [ ] Orders sorted by product type → device → design
- [ ] Priority: Expedited/Prime first, then FIFO
- [ ] Site assignment based on 3-layer routing (capability → stock → overrides)

### Step 2: Shipping Label Generation
- [ ] Staff process labels in Veco
- [ ] Apply carrier rules (see `04_Shipping_Fulfillment/SHIPPING_CARRIER_RULES.md`)
- [ ] Click "Ship" → export shipped labels to Excel
- [ ] Excel = definitive print list

### Step 3: Print File Generation
- [ ] Take shipped label list (Excel)
- [ ] Decompose SKUs to identify design files
- [ ] Generate production-ready files:
  - **TIFF** for flatbed/jig printing (cases)
  - **EPS** for vinyl skins (nested per print job)
- [ ] Verify: labels = print files (1:1 match, no orphans)
- [ ] Check for camera hole obstruction on phone cases

### Step 4: Blank Stock Pull
- [ ] Generate "Blank Requirement List" from print queue
- [ ] Operators pull physical blanks (by product type + device)
- [ ] If blank out of stock → flag for rerouting or reorder

### Step 5: Printing
- [ ] Load blanks into jigs (trays) matched to printer bed
- [ ] Print server pushes batched files to UV printers
- [ ] Jig grouping: sorted alphabetically by device model

### Step 6: Post-Print QC
- [ ] Visual check: ink adhesion, color accuracy, alignment
- [ ] *Future: Gemini Vision AI verification*

### Step 7: Packing & Verification
- [ ] Packer scans shipping label barcode
- [ ] Matches printed product to correct label/order
- [ ] *Future: Gemini Vision confirms product matches SKU*
- [ ] Pack in correct packaging (bubble mailer / tube / box)
- [ ] Multi-item orders: wait for all items verified before packing

### Step 8: Shipping
- [ ] Combine packed items with Philippines overflow shipments (if applicable)
- [ ] Hand over to carrier (Royal Mail / USPS / FedEx / Amazon Shipping)
- [ ] Update order status → push tracking back to platforms

---

## Overflow Rules

### Holiday Override
When UK or US has upcoming holiday:
1. Philippines pre-prints and pre-packs affected orders
2. Ships consolidated carton via freight (UPS/international)
3. Local site opens carton on return, hands to final-mile courier

### Printer Downtime
- Manual trigger to reroute affected orders to Philippines
- No automated failover currently *(automation opportunity)*

### Peak Season (December)
- Philippines takes increased volume
- Manual load balancing between sites
- Shift to 24/7 rotation at Philippines during Q4

---

## Key Metrics
- Daily throughput (units printed vs target)
- Error rate (mismatches caught)
- Stock-outs (blanks reaching zero)
- Label-to-print-file reconciliation accuracy
- Time: order received → shipped

---

## Automation Opportunities

| Step | Current | Proposed | Impact |
|------|---------|----------|--------|
| Label generation | 2 staff manual | Veco automation | 2 staff freed |
| Print file generation | 3 staff manual | Script + AI hybrid | 3-4 staff freed |
| Packing verification | Visual (human eye) | Gemini Vision | 95% error reduction |
| Routing/failover | Manual trigger | Automated rules engine | Faster response |
| Inventory reorder | Manual check | Velocity-based alerts | Fewer stockouts |

---

*This SOP will be refined with input from floor staff and site managers. Cem to provide: EPS workflow docs, camera hole examples, site capability matrix.*
