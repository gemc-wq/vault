# Veeqo: Order Management Automation — Staff Reduction Analysis
*Strategic analysis by Ava | 2026-03-08*
*Objective: Determine if Veeqo (or ShipStation) can absorb Patrick's team functions*

---

## Executive Summary

**Verdict: Yes — Veeqo can replace 3-4 of the 5 IT/Production-Operations staff functions.**

Veeqo is Amazon's own free multichannel shipping software. It directly replaces the manual processes that Zero currently handles through Patrick's team: picking list generation, shipping label creation, order status updates, carrier selection, and PO wave timing. The routing rules currently hardcoded in Zero can be replicated through Veeqo's automation rules engine.

**Estimated headcount impact: 5 → 1-2 staff**

---

## Current State — What Patrick's Team Does

### Daily Order Flow (from Drew's docs + wiki)
1. **Order intake** — Zero pulls orders from Amazon, eBay, BigCommerce, etc.
2. **PO creation** — Patrick/Jeric create Purchase Orders in Zero, route to PH or FL
3. **Picking list generation** — Zero generates picking lists per location per wave (AMG1 = daily batch)
4. **Shipping label creation** — Staff download carrier label files (RM, USPS, FedEx, DHL, etc.)
5. **Wave management** — Timed PO waves throughout the day:
   - UK: 9:00 AM, 8:50 PM, 10:50 PM, 11:40 PM
   - FL: 9:40 AM, 10:00 AM, 11:50 PM, 2:50 AM
   - Saturdays: UK 9:00 AM, 7:15 PM
6. **Status updates** — Mark orders as shipped, update tracking numbers across channels
7. **Exception handling** — Late orders, stock errors, manual interventions

### Current Staff Involved
- **Patrick Gaña** — Zero operations lead (crons, scripts, queries, day-to-day)
- **Jeric Tyron Padilla** — PO uploads, FBA shipment prep
- **Mechelle Ann Gaña** — RM label files, international tracked labels
- **Chris Yunun** — Warehouse/production coordination
- **Additional IT support** — Dickel Pineda leads remaining IT team

### Three-Layer Routing Logic (currently in Zero)

**Layer 1 — Equipment Capability (Hard Rule)**
| Product Type | UK | FL | PH |
|---|---|---|---|
| Skins (H89) | ✅ | ✅ | ❌ |
| Stickers | ✅ | ✅ | ❌ |
| Laser-cut | ✅ | ❌ | ❌ |
| UV-printed cases | ✅ | ❌ | ✅ |

**Layer 2 — Geography-Based Routing**
| Customer Location | Primary Site | Overflow |
|---|---|---|
| UK/Europe | UK | PH |
| US | FL | PH |
| International | UK | PH |

**Layer 3 — Carrier Selection**
| Market | Standard | Premium | Amazon Override |
|---|---|---|---|
| UK Domestic | Royal Mail 1st Class | — | — |
| Europe | RM or Deutsche Post (cheapest) | — | — |
| US Domestic | USPS | FedEx 2-day | Amazon dictates by zip code |

---

## What Veeqo Replaces — Function by Function

| Current Manual Process | Veeqo Capability | Automation Level |
|---|---|---|
| Order intake from multiple channels | ✅ Auto-sync from Amazon, eBay, Shopify, Walmart, BigCommerce | **Fully automated** |
| PO creation & routing to PH/FL/UK | ✅ Smart order routing by warehouse + automation rules | **Fully automated** — rules engine can encode Layer 1-3 logic |
| Picking list generation (AMG1 daily) | ✅ Digital picking with barcode scanning, batch picking | **Fully automated** — morning batch generation |
| Shipping label creation | ✅ Bulk print 100+ labels in one click, 21+ carrier integrations | **Fully automated** — RM, USPS, FedEx, DHL, UPS all supported |
| Wave management (timed PO releases) | ⚠️ Partial — can schedule batches but may need custom automation for 4-wave daily pattern | **Semi-automated** — may need n8n/cron to trigger waves |
| Order status updates | ✅ Auto-updates across all channels when label printed | **Fully automated** |
| Tracking number management | ✅ Auto-generated + synced to channels + customer emails | **Fully automated** |
| Returns processing | ✅ Return label generation, stock adjustment, refund processing | **Fully automated** |
| PH→UK/US consolidation shipping | ⚠️ Partial — bulk shipment creation exists but consolidation model is custom | **Needs config** — Veeqo supports multi-warehouse but PH→UK freight consolidation is unique |
| Exception handling (late orders, stock errors) | ✅ Order tagging, automation rules, flagging | **Mostly automated** — human review for edge cases |

### What Veeqo CANNOT Do
1. **Print file generation** — Veeqo manages orders, not product manufacturing. The actual design-to-print pipeline stays separate
2. **Zero's custom cron jobs** — Some of Drew's legacy scripts do specialized things (eBay transaction sync, B2B invoice generation). These need migration to n8n or direct API integration
3. **PH consolidation freight model** — Veeqo handles warehouse-to-customer, not the batch-100-items-into-one-box-ship-via-freight model. This requires either a custom workflow or keeping 1 person on freight coordination

---

## Proposed Target State

### Veeqo Configuration
1. **3 warehouses:** UK, FL (Florida), PH (Philippines)
2. **Automation rules (encoding current Zero logic):**
   - IF product_type = H89/Skins AND customer = US → route to FL
   - IF product_type = H89/Skins AND customer = UK/EU → route to UK
   - IF product_type = UV_case AND customer = US → route to PH → consolidation
   - IF product_type = UV_case AND customer = UK/EU → route to UK (primary) or PH (overflow)
   - IF product_type = Laser-cut → route to UK only
3. **Carrier rules:**
   - UK domestic → Royal Mail 1st Class
   - Europe → cheapest of RM vs Deutsche Post
   - US standard → USPS
   - US premium/2-day → FedEx
   - Amazon orders → honor Amazon carrier override
4. **Wave scheduling:** Use Veeqo's batch processing + n8n cron triggers to replicate 4-wave daily pattern
5. **Real-time inventory sync** across Amazon, eBay, BigCommerce, Shopify

### Remaining Manual Roles (1-2 people)
1. **Operations Coordinator (1 person)** — Handles exceptions, PH consolidation freight, FBA shipment prep, quality review
2. **Warehouse Supervisor (1 person, optional)** — Physical oversight of PH printing/packing. Could be existing production staff (Jae Vitug)

### Staff Reduction Impact
| Current | Role | Replaced By | Status |
|---|---|---|---|
| Drew Ramos | IT Manager/Zero dev | Already gone | ✅ Eliminated |
| Patrick Gaña | Zero operations | Veeqo automation rules | 🔄 Transition to Ops Coordinator or redeploy |
| Jeric Padilla | PO uploads, FBA prep | Veeqo + automation | 🔄 Redundant if FBA prep automated |
| Mechelle Gaña | Label file generation | Veeqo label printing | 🔄 Redundant |
| Chris Yunun | Warehouse coordination | Veeqo digital picking | 🔄 Stays as warehouse supervisor |
| Dickel Pineda | IT infrastructure | Minimal IT needed post-Veeqo | 🔄 Reduced scope |

**Net result: 5 IT/Operations staff → 1-2 staff (Patrick as Ops Coordinator + Chris as warehouse)**

---

## Cost Analysis

| Item | Current | With Veeqo |
|---|---|---|
| Staff cost (5 IT/Ops) | ~₱350K/mo (~$6K/mo) | ~₱140K/mo (~$2.4K/mo) for 2 staff |
| Software | Zero (custom, no license fee) | Veeqo: **FREE** (Amazon-owned) + $19/mo for inventory management |
| Shipping rates | Current carrier rates | Veeqo: pre-negotiated UPS/USPS/FedEx/DHL rates + 5% cashback |
| **Monthly savings** | | **~$3,600/mo staff + potential shipping savings** |
| **Annual savings** | | **~$43K+ per year** |

---

## Veeqo vs ShipStation

| | Veeqo | ShipStation |
|---|---|---|
| **Price** | FREE (Amazon-owned) | $9.99-$229/mo |
| **Amazon integration** | Native (Amazon owns it) | Third-party |
| **Amazon Buy Shipping** | ✅ Integrated + A-to-Z protection | ❌ Not integrated |
| **Multi-warehouse** | ✅ | ✅ |
| **Digital picking** | ✅ + barcode scanner | Limited |
| **Carrier rates** | Pre-negotiated discounts + 5% cashback | Discounted USPS only |
| **Inventory sync** | ✅ Real-time across channels | Basic |

**Recommendation: Veeqo wins.** Free, Amazon-native, better shipping rates, and deeper Amazon integration. ShipStation only makes sense if Veeqo can't handle the PH consolidation model — and even then, neither handles it natively.

---

## Implementation Plan

### Phase 1 — Setup (Week 1-2)
- Create Veeqo account (free)
- Connect sales channels: Amazon (US+UK), eBay, Shopify (GoHeadCase), BigCommerce
- Configure 3 warehouses: UK, FL, PH
- Set up carrier accounts: RM, USPS, FedEx, DHL, UPS, Deutsche Post

### Phase 2 — Rule Encoding (Week 2-3)
- Encode Layer 1-3 routing logic as Veeqo automation rules
- Set up wave scheduling via n8n cron triggers
- Configure label templates (thermal 4x6 for FBA, standard for others)
- Test with small batch of real orders (parallel run with Zero)

### Phase 3 — Parallel Run (Week 3-6, 4 weeks minimum per Cem's rule)
- Run Veeqo alongside Zero for all order processing
- Patrick validates accuracy daily
- Track error rate — must be <5% for 4+ consecutive weeks

### Phase 4 — Cutover + Staff Transition (Week 7+)
- Migrate fully to Veeqo
- Patrick transitions to Ops Coordinator (or exits)
- Mechelle + Jeric transition to other roles or exit
- Decommission Zero order management functions (keep BQ sync for analytics)

---

## Risks

1. **PH consolidation model** — Veeqo doesn't natively support the "100 items → 1 freight box → UK/US → distribute" model. Needs custom workflow or 1 person managing this
2. **Zero as data source** — BQ sync relies on Zero database. If we decommission Zero order processing, we need an alternative data pipeline (Veeqo → BQ via API)
3. **Patrick as single point of knowledge** — Patrick knows all Zero operations. If he leaves before transition, we lose institutional knowledge. **Must document everything first** (we've started this with the Drew email extraction)
4. **Amazon carrier overrides** — Veeqo handles this natively (Amazon Buy Shipping), but the 5% non-compliance business decision needs to be configured as an exception rule

---

*Next: Cem to confirm Veeqo account setup → Harry builds the carrier rule engine → Ava reviews transition timeline against staff reduction plan*

## Related
- [[wiki/23-drew-handover/ZERO_INFRASTRUCTURE|Zero Infrastructure]] — The legacy system being replaced
- [[wiki/23-drew-handover/PATRICK_WORKFLOW_PICKLIST_TO_IMAGE|Patrick's Workflow]] — Current manual process Veeqo replaces
- [[wiki/04-shipping/SHIPPING_CARRIER_RULES|Shipping Carrier Rules]] — Carrier routing logic to migrate
- [[wiki/03-production/DAILY_PRINT_PRODUCTION|Daily Print Production]] — Production workflow connected to order management
- [[wiki/23-drew-handover/MEETING_CEM_BEA_PATRICK_2026-03-09|Meeting Notes Mar 9]] — Discussion confirming Zero knowledge gaps
