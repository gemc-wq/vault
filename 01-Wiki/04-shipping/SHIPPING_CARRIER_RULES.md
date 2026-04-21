# Shipping Carrier Rules — eCELL Global / Head Case Designs
*Documented: 2026-02-10 | Source: Cem walkthrough*

---

## Fulfillment Sites

| Site | Location | Fulfills For | Staff |
|------|----------|-------------|-------|
| **UK** | United Kingdom | UK + Europe + International | 1 printer, 2 packers |
| **US** | Florida, USA | US only | 1 printer, 2 packers |
| **Philippines** | Central Hub | UK + US (overflow/fallback) | 35-40 staff |

**Key Rules:**
- Philippines is the overflow hub — handles both UK and US fulfillment
- UK and US do NOT cross-fulfill for each other
- Philippines carrier rules = UK rules + US rules combined

---

## Carrier Matrix

### UK Domestic
| Service Level | Carrier | Notes |
|--------------|---------|-------|
| Standard | Royal Mail First Class | Single carrier for all UK |

### Europe (from UK site)
| Service Level | Carrier | Notes |
|--------------|---------|-------|
| Standard | Royal Mail OR Deutsche Post | Cost-dependent — pricing matrix, choose cheapest |

### US Domestic
| Service Level | Carrier | Notes |
|--------------|---------|-------|
| Standard | USPS | Default carrier |
| Premium (2-day) | FedEx | Negotiated flat rate |
| **Amazon Orders** | Amazon Shipping | **OVERRIDE** — Amazon dictates carrier based on zip code |

### Amazon Shipping Override (US)
- Amazon orders may force a specific carrier to meet "promised delivery time"
- Zip code / address driven — eCELL has no control
- Sometimes forces next-day service (~$30) vs normal average ($5-6)
- **Business decision:** Willing to accept 5% non-compliance rather than paying $30 per order
- Account health metrics must stay near 100% — suspensions are costly

### Philippines → UK/US (Consolidation Model)
- Philippines prints individual consumer shipping labels (final-mile labels)
- Items packed individually, ready for end customer
- 100-200 items consolidated into one large carton box
- Bulk carton shipped via freight (UPS or international freight company)
- On arrival at UK/US: open box, merge with local production, hand to final-mile courier

### International / Rest of World
- Handled from UK site
- **NOT yet configured in Veco** — still manual process
- Carriers: TBD (need details from Cem)

---

## Veco Transition

### What Veco Replaces
Currently 2 full-time staff in Philippines manage shipping labels manually:
1. Download sales order data from platforms
2. Filter in Excel (manual carrier/site rules)
3. Upload data to carrier system (API or manual entry)
4. Print shipping labels (often PDFs)
5. Combine/sort labels by product SKU (SKU = custom field on label)
6. Manually trigger shipment

**Veco automates this entire loop.**

### Veco Status
| Market | Status | Notes |
|--------|--------|-------|
| US | ✅ Ready | All carriers configured |
| UK (domestic) | ✅ Nearly ready | Close to completion |
| Europe | ❌ Not done | International carriers not configured |
| Rest of World | ❌ Not done | Manual process continues |

### Gap to Close
- European and international carrier configuration in Veco
- Once complete: 2 staff freed from manual label management

---

## Three-Layer Routing Logic

When an order comes in, routing follows this hierarchy:

### Layer 1 — Equipment Capability (Hard-coded)
Each site has specific printer/equipment capabilities. Some product types can ONLY be made at certain sites.

| Product Type | UK | US (Florida) | Philippines |
|-------------|-----|-------------|-------------|
| Skins (H89 codes) | ✅ | ✅ | ❌ |
| Stickers | ✅ | ✅ | ❌ |
| Laser-cut products | ✅ | ❌ | ❌ |
| UV-printed cases | ✅ | ❌ | ✅ |
| *Full mapping TBD — awaiting table from Cem* |

### Layer 2 — Stock Availability
- Cron job checks inventory database
- Flags items at zero stock
- Pre-defined table maps which blanks are stocked at which site
- Not every product/device combination stocked everywhere
- If local site out of stock → reroute to Philippines

### Layer 3 — Manual Overrides
- **Printer downtime:** Manual trigger to reroute to Philippines
- **Holidays:** If UK/US has upcoming holiday, Philippines pre-prints and pre-packs, ships boxed products via freight. Local site just opens and hands to courier.
- **Peak season (December):** Load balancing — Philippines takes more volume
- **Saturday:** Overflow rule in flowchart (manual trigger)

---

*Next steps: Get product type → site capability table from Cem. Configure remaining Veco carriers for Europe/International.*

## Related
- [[wiki/03-production/DAILY_PRINT_PRODUCTION|Daily Print Production]] — Production drives shipping
- [[wiki/23-drew-handover/ZERO_INFRASTRUCTURE|Zero Infrastructure]] — PO filtering hardcodes carrier rules
- [[wiki/23-drew-handover/VEEQO_REPLACEMENT_ANALYSIS|Veeqo Replacement]] — Veeqo replaces manual carrier routing
- [[wiki/23-drew-handover/PATRICK_WORKFLOW_PICKLIST_TO_IMAGE|Patrick's Workflow]] — Label generation step
- [[wiki/05-inventory/SOP_INVENTORY_TRACKING|Inventory Tracking]] — Stock availability drives routing
