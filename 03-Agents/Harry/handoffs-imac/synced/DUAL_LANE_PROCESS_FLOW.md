# Patrick's Dual-Lane Operations — Process Flow

*Created: 2026-03-09 | Visual: [process-flow.html](process-flow.html) (open in browser)*

---

## Overview

Patrick currently operates **two parallel pipelines simultaneously** — the legacy Zero system and the new Veeqo system. The goal is to collapse everything into Lane 2 and kill Lane 1.

---

## 🔴 LANE 1: Legacy Zero Pipeline (Being Replaced)

```
┌─────────────────────────────────────────────────────────────┐
│  LANE 1: LEGACY ZERO                          🔴 RETIRING  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ① DOWNLOAD ORDERS (Manual)                                 │
│  Patrick manually downloads order CSV from Amazon           │
│  Seller Central at specific PO wave times.                  │
│  ⚠️ Manual trigger — no automation                          │
│          │                                                  │
│          ▼  CSV file → local machine                        │
│                                                             │
│  ② UPLOAD TO ZERO (Manual)                                  │
│  Orders imported into Zero on 192.168.20.57 (XAMPP/PHP)     │
│  ⚠️ Data re-entry point — errors cascade downstream         │
│          │                                                  │
│          ▼  Orders in Zero DB → 192.168.20.160              │
│                                                             │
│  ③ PO FILTERING (Hardcoded PHP)                             │
│  zero_POFiltering.php (1,300+ lines)                        │
│  Routes by:                                                 │
│    • Country: US / UK / EU / PH                             │
│    • Product type: skins (90), desk mats (DM,ST),           │
│      cases (A9, B6, B7)                                     │
│    • Day-of-week: Fri PM → Mon hold patterns                │
│    • Warehouse: UK vs FL unit availability                   │
│  ⚠️ Any rule change = edit PHP source. No admin UI.         │
│          │                                                  │
│          ▼  Filtered PO batches                             │
│                                                             │
│  ④ GENERATE PICKING LIST (Hardcoded PHP)                    │
│  sage_generate_picking_list_split.php                       │
│  Creates pick lists per warehouse/carrier                   │
│          │                                                  │
│          ▼  Pick list → carrier label generation            │
│                                                             │
│  ⑤ GENERATE SHIPPING LABELS (Multi-API)                     │
│  Calls 4+ carrier APIs separately:                          │
│    • Amazon Buy Shipping API                                │
│    • USPS / Stamps.com                                      │
│    • Royal Mail (UK)                                        │
│    • Veeqo labels (some channels)                           │
│  Labels combined into single PDF                            │
│  ⚠️ Patrick generates separate transaction reports for each │
│          │                                                  │
│          ▼  Combined label PDF + USPS scan form             │
│                                                             │
│  ⑥ CREATE MFG PURCHASE ORDER (PHP + Email)                  │
│  zero_generate_purchase_order_automated_phAMG1_wh.php       │
│  Automated email notification to production team            │
│          │                                                  │
│          ▼  Email trigger → production team                 │
│                                                             │
│  ⑦ HPT IMAGE RENDERING (Manual trigger)                     │
│  Staff open HPT (Head Case Production Tool)                 │
│  Renders print-ready images per order                       │
│  Images saved to QNAP NAS (Manufacturing Office)            │
│  ⚠️ Runs on Mfg Office VMs (likely IREN). Nobody fully     │
│    understands the code.                                    │
│          │                                                  │
│          ▼  Print images on NAS                             │
│                                                             │
│  ⑧ 1:1 RECONCILIATION & PRINT (Manual)                     │
│  100 labels = 100 print files. Must match exactly.          │
│  Physical print → pick → pack → ship                        │
│  ⚠️ Mismatch = wrong case shipped to customer               │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  📊 DAILY OUTPUT: ~8 emails by 4 AM                         │
│  • USPS Stamps Transaction Report                           │
│  • USPS Buy Shipping Transaction Report                     │
│  • Daily SO for Sage MFG                                    │
│  • USPS Scan Forms                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🟢 LANE 2: Veeqo Pipeline (Target State)

```
┌─────────────────────────────────────────────────────────────┐
│  LANE 2: VEEQO                               🟢 TARGET     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ① ORDERS AUTO-SYNC (Automatic)                             │
│  Orders flow in automatically from all channels:            │
│    • Amazon US, Amazon FBA, Walmart, eBay US                │
│    • GoHeadCase (Shopify), Etsy, Fanatics, TikTok          │
│  ✅ No manual download. Real-time across all channels.       │
│          │                                                  │
│          ▼  Auto-ingested orders                            │
│                                                             │
│  ② SMART ORDER ROUTING (Automatic)                          │
│  Veeqo auto-allocates to nearest warehouse with stock.      │
│  Location Priority fallback chain handles overflow.          │
│  Replaces 1,300 lines of PHP routing logic.                 │
│  ✅ Config-based rules. Changes via UI, not PHP.             │
│          │                                                  │
│          ▼  Routed orders in filtered tabs                  │
│                                                             │
│  ③ OPERATOR: FILTER → SORT → BULK SELECT                    │
│  Custom filtered tabs per operator:                         │
│    • FL Premium, FL Non-Premium                             │
│    • UK Orders, PH Consolidation                            │
│  Sort by SKU prefix → bulk select → print labels            │
│  ✅ Operators see only their orders.                         │
│          │                                                  │
│          ▼  Selected orders → label generation              │
│                                                             │
│  ④ PRINT LABELS — ONE CLICK (Auto-carrier)                  │
│  Bulk print — Veeqo auto-selects cheapest carrier.          │
│  Amazon Buy Shipping, USPS, RM — one interface.             │
│  5% cashback on Amazon shipping rates.                      │
│  ✅ One carrier integration, not 4+.                         │
│          │                                                  │
│          ▼  Labels printed → mark shipped                   │
│                                                             │
│  ⑤ MARK SHIPPED → AUTO-UPDATE ALL CHANNELS (Automatic)      │
│  One click: mark as shipped.                                │
│    • Auto-updates Amazon, Walmart, eBay, Etsy, Shopify     │
│    • Customer gets tracking email automatically             │
│    • Inventory decremented across all channels              │
│  ✅ No manual marketplace updates. Zero overselling risk.    │
│          │                                                  │
│          ▼  CSV export for production                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  🟡 BRIDGE TO PRODUCTION (THE GAP)                  │    │
│  │                                                     │    │
│  │  ⑥ CSV EXPORT → PRODUCTION PIPELINE                 │    │
│  │  Veeqo handles orders + shipping. But print file    │    │
│  │  generation still needs:                            │    │
│  │    • Shipped CSV export from Veeqo                  │    │
│  │    • Parse SKU → design code + device code          │    │
│  │    • Trigger image generation (HPT/IREN)            │    │
│  │    • 1:1 reconciliation with labels                 │    │
│  │                                                     │    │
│  │  ⚠️ The image gen trigger currently comes from      │    │
│  │  Zero's MFG PO email. Need Veeqo equivalent:       │    │
│  │  CSV webhook, Veeqo API, or manual export.          │    │
│  └─────────────────────────────────────────────────────┘    │
│          │                                                  │
│          ▼                                                  │
│                                                             │
│  ⑦ IMAGE GEN + PRINT (Same as Lane 1)                       │
│  HPT/IREN renders print images → QNAP NAS → print          │
│  This step is identical regardless of which lane feeds it.  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  📊 AUTOMATED REPORTS                                        │
│  • Veeqo dashboard = real-time metrics                      │
│  • Shipping reports auto-generated                          │
│  • No manual transaction report emails needed               │
│  Target: 3 operators (UK 1, FL 1, PH 1) replacing 10+      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 Critical Bridge: Where Lane 1 & Lane 2 Overlap

| Element | Status |
|---------|--------|
| **Image generation (HPT/IREN)** | SHARED — both lanes feed into same production system. Trigger mechanism differs (Zero email vs Veeqo CSV). |
| **Label reconciliation** | SHARED — both lanes must produce 1:1 label-to-print-file matching. Quality gate regardless of source. |
| **Patrick runs BOTH** | DUAL WORK — double effort during transition. Some channels on Zero, some on Veeqo. |
| **Split criteria** | ❓ UNKNOWN — What determines which orders go through which lane? Channel? Region? Product type? |
| **GDrive label distribution** | SHARED — Patrick saves labels to GDrive folders per location (UK/FL/PH). Each location pulls and prints locally. This step is the same in both lanes. |
| **PO Filtering → Smart Order Routing** | ⚠️ CRITICAL RISK — The 1,300-line PHP has been battle-tested for years. Edge cases (Fri night holds, DE address variants, skin-vs-case routing, weekend cutoffs) must ALL be replicated in Veeqo Shipping Rules before Lane 1 can be killed. |

---

## Data Flow Comparison

| Step | Lane 1 (Zero) | Lane 2 (Veeqo) | Automation Gain |
|------|---------------|-----------------|-----------------|
| Order ingestion | Manual CSV download | Auto-sync from 8+ channels | ✅ 100% automated |
| Order routing | 1,300-line PHP script | Smart Order Routing UI | ✅ Config, not code |
| Carrier selection | 4+ separate API calls | Single-click, auto-cheapest | ✅ Unified interface |
| Label generation | Multi-step, manual combine | Bulk print, one click | ✅ 80% faster |
| Marketplace update | Not automated (or separate) | Auto-update ALL channels | ✅ 100% automated |
| Customer tracking | Manual or delayed | Automatic on ship | ✅ 100% automated |
| Production trigger | MFG PO email from PHP | **🟡 TBD — CSV bridge needed** | ⚠️ Gap to solve |
| Image rendering | HPT on Mfg VMs | Same (unchanged) | ➡️ No change |
| Reconciliation | Manual count | Manual count (unchanged) | ➡️ No change |
| Daily reports | 8+ manual emails by 4 AM | Dashboard + auto-reports | ✅ Eliminated |

---

## Migration Impact

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Manual steps | 8 | 3 | -63% |
| IT team cost | ₱117K/mo (5 staff) | ₱25-50K/mo (1-2 staff) | -57-79% |
| Operators | 10+ | 3 (UK 1, FL 1, PH 1) | -70% |
| Carrier integrations | 4+ separate | 1 unified | -75% |
| Marketplace updates | Manual per channel | Automatic all channels | -100% |

---

## PO Wave Schedule (Both Lanes)

| Wave | Time | Region |
|------|------|--------|
| UK Prime/Non-Prime Wave 1 | 9:00 AM GMT | UK |
| UK Prime Wave 1.5 | 8:50 PM GMT | UK |
| UK Prime Wave 2 | 10:50 PM GMT | UK |
| UK Prime Wave 3 | 11:40 PM GMT | UK |
| FL Prime Wave 1 | 9:40 AM EST | US |
| FL Non-Prime Wave 1 | 10:00 AM EST | US |
| FL Prime Wave 1.5 | 11:50 PM EST | US |
| FL Prime Wave 2 | 2:50 AM EST | US |
| Saturday UK | 9:00 AM, 7:15 PM GMT | UK |

---

## Related
- [[wiki/23-drew-handover/PATRICK_WORKFLOW_PICKLIST_TO_IMAGE|Patrick's Original Workflow]] — Detailed email documentation
- [[wiki/23-drew-handover/PATRICK_IT_TEAM_PROFILE|Patrick IT Team Profile]] — Team roles and costs
- [[wiki/23-drew-handover/ZERO_INFRASTRUCTURE|Zero Infrastructure]] — Legacy system architecture
- [[wiki/23-drew-handover/ZERO_INFRASTRUCTURE_MAP|Zero Infrastructure Map]] — Network and DB topology
- [[wiki/23-drew-handover/VEEQO_REPLACEMENT_ANALYSIS|Veeqo Replacement Analysis]] — Why Veeqo was selected
- [[wiki/23-drew-handover/MEETING_CEM_BEA_PATRICK_2026-03-09|Meeting Notes Mar 9]] — Zero knowledge gaps confirmed
- [[wiki/03-production/DAILY_PRINT_PRODUCTION|Daily Print Production]] — Full production cycle
- [[wiki/04-shipping/SHIPPING_CARRIER_RULES|Shipping Carrier Rules]] — Carrier routing logic
- [[wiki/12-org/PH_STAFF_ROSTER|PH Staff Roster]] — Full staff and salary data
