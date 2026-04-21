# Harry's Migration Spec — Ava Strategic Review
*Received: 2026-03-09 | Source: Harry's ORDER_MANAGEMENT_FULFILLMENT_MIGRATION_SPEC.md*

## Harry's Three-Layer Model (AGREED ✅)

| Layer | What | Current Owner | Veeqo Replaces? |
|-------|------|---------------|-----------------|
| A. Routing & Queue Prep | Country/product/timing rules, SO/PO generation, batch prep | Zero PHP + Patrick | ❌ NOT fully — this is the orchestration brain |
| B. Label Execution | Views, package edits, carrier selection, bulk buy+print, PDF output | Veeqo (partially live) | ✅ YES — this is what Veeqo does well |
| C. Production Handoff | Shipped export → pick list → HPT image gen → NAS → 1:1 reconciliation | Zero email trigger + HPT | ❌ NO — needs bridge built |

## Key New Intel from Harry

### Veeqo FL Premium Workflow (confirmed from Patrick's docs)
- Real "Ready to Ship" view exists with filter: Dispatch Date = This Week, Delivery Method = SecondDay
- Bulk package edit → FedEx 2Day One Rate → Buy + Print → combined PDF
- This is LIVE and working for FL Premium

### Veeqo Manual Import Bridge (CRITICAL finding)
- Non-native orders still require CSV pre-processing from PHP tools
- Flow: generate CSV internally → import to Veeqo → bulk set packages → bulk set USPS Ground Advantage → sort by SKU → buy labels
- **Veeqo is partly live but STILL depends on Zero pre-processing**

### SO/PO Warehouse Movement (NOT replaced by Veeqo)
- Separate internal flow: shipment email → pivot item code/qty → free-stock check → convert price → generate SO/PO → create PO in destination warehouse → create SO in PH → dispatch SO → email outputs
- This is inventory/warehouse management, not shipping — Veeqo doesn't touch it

## Ava's Assessment

### Where Harry is RIGHT
1. **Three-layer model is correct.** "Replace Zero with Veeqo" is an oversimplification. The real work is separating orchestration from execution.
2. **Veeqo is the label workstation, not the brain.** The routing logic, SO/PO generation, and warehouse movement flows are separate concerns.
3. **The manual import bridge confirms partial dependency.** Veeqo can't fully replace Zero until the CSV pre-processing step is eliminated or automated.
4. **His 5 questions are the right ones to answer next.**

### Where I'd push back / add nuance
1. **The "routing brain" doesn't need to be rebuilt — it needs to be SIMPLIFIED.** The 1,300 lines of PHP encode rules that can be expressed in ~20 Veeqo Shipping Rules + Smart Order Routing config. The complexity is artificial (accumulated cruft over 17 years).
2. **The SO/PO layer may not need 1:1 replacement.** If Veeqo handles order management and we build the production bridge (shipped CSV → image gen trigger), the internal SO/PO generation becomes redundant for the shipping flow. It only matters for inventory/finance — which is Harry's separate project.
3. **The Veeqo gap analysis (Cem's directive) should answer Harry's questions 1-5.** Rather than speculating, Harry should investigate Veeqo's Shipping Rules, Smart Order Routing, and API capabilities directly.

## Answers to Harry's 5 Questions (from today's intel)

### Q1: Where does the real routing brain live?
**Primarily in PHP** — `zero_POFiltering.php` is the routing engine. Patrick/team have operational knowledge but can't articulate the rules (confirmed in meeting). Some routing has migrated to Veeqo views (FL Premium filters), but the bulk is still PHP.

### Q2: Is Veeqo live for UK?
**Partially.** UK was "near-ready" as of Feb. Patrick's current workflow shows UK labels still going through Royal Mail Click & Drop (not Veeqo). Need Patrick to confirm current UK Veeqo status.

### Q3: What is the definitive print trigger?
**Multiple triggers coexist:**
- Lane 1 (Zero): MFG PO email from PHP → staff open HPT
- Lane 2 (Veeqo): Shipped export → (bridge TBD) → HPT
- The "definitive" trigger depends on which lane the order went through

### Q4: Where is 1:1 reconciliation?
**At the print station.** 100 labels printed = 100 print files generated. Physical count. Patrick/operators check. No automated reconciliation exists.

### Q5: What hurts most today?
**Queue/routing prep + the dual-lane overhead.** Patrick running both systems simultaneously is the biggest pain. The label buying itself works (Veeqo for some, carriers for others). The SO/PO generation is rote but functional.

## Recommended Next Steps

1. **Harry: Veeqo gap analysis** — investigate Shipping Rules, Smart Order Routing, API, CSV export capabilities. Can Veeqo handle: SKU-based routing? Label sorting by SKU? EVRI integration? Automation rules?
2. **Ava: Complete carrier rules matrix** — when Jay Mark delivers PHP codebase, decode all rules into the matrix
3. **Joint: Three-part operating spec** per Harry's A/B/C model
4. **Cem decision needed:** Single provider (all labels from Veeqo) vs multi-provider (Veeqo + ShipStation + others)?
