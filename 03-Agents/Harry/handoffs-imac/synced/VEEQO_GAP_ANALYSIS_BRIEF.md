# Veeqo Gap Analysis Brief — For Harry
*Created: 2026-03-09 by Ava | Approved by Cem*
*Priority: P0 — gate for entire shipping migration*

---

## Objective

Determine whether Veeqo can fully replace the Zero/PHP orchestration layer for order routing and label execution, or whether we need supplementary tools (ShipStation, custom automation, etc.).

**This analysis gates everything.** If Veeqo can't handle the requirements, we pivot. Don't build on assumptions.

---

## Context

Patrick currently runs two parallel lanes:
- **Lane 1 (Legacy):** Manual download from Amazon → upload to Zero → PHP PO filtering → picking list → multi-carrier labels → MFG PO email → HPT image gen
- **Lane 2 (Veeqo):** Auto-sync orders → Smart Order Routing → filtered tabs → bulk print labels → mark shipped → auto-update channels

Lane 2 is partially live (FL Premium, some non-Amazon) but still depends on Zero pre-processing for CSV imports. Goal: collapse everything into Lane 2, kill Lane 1.

**Key docs to review:**
- `wiki/23-drew-handover/DUAL_LANE_PROCESS_FLOW.md` — full visual + MD process flow
- `wiki/23-drew-handover/CARRIER_RULES_MATRIX.md` — carrier rules (draft)
- `wiki/23-drew-handover/CARRIER_RULES_UPDATE_NOTES.md` — Cem's updated requirements + PO wave sequencing
- `wiki/04-shipping/SHIPPING_CARRIER_RULES.md` — three-layer routing logic
- `wiki/23-drew-handover/PATRICK_WORKFLOW_PICKLIST_TO_IMAGE.md` — Patrick's current workflow

---

## Questions to Answer

### A. Routing & Queue Preparation

| # | Question | Why It Matters |
|---|----------|---------------|
| A1 | Can Veeqo's **Smart Order Routing** handle location-based allocation (FL vs UK vs PH) based on inventory availability? | Core routing requirement — Layer 2 of three-layer logic |
| A2 | Can routing rules be **dynamically overridden** (e.g., printer down at FL → divert to PH)? How quickly? UI toggle or API? | Operational flexibility — must be done ahead of time, not per-order |
| A3 | Can Veeqo enforce **hard product blocks** (HDMWH desk mats, H89/H90 skins, HSTWH stickers → NEVER route to PH)? | Equipment capability constraint — non-negotiable |
| A4 | Can Veeqo handle **PO wave sequencing** (PH first → UK second → US third → afternoon waves)? Or is this manual operator discipline? | Timezone-driven production flow — PH is +8 UK, +12 US |
| A5 | Does Veeqo support **SKU parsing** natively, or do we need to pre-process SKUs before Veeqo sees them? | SKU prefix determines product type, device, equipment routing |

### B. Label Execution

| # | Question | Why It Matters |
|---|----------|---------------|
| B1 | Can Veeqo **sort labels by SKU alphabetically** in the output PDF? | Operational requirement — print files are sorted by SKU, labels must match |
| B2 | Does Veeqo support **Amazon Buy Shipping** for ALL Amazon orders (US + UK)? | MANDATORY — late delivery protection |
| B3 | Can Veeqo handle **EVRI** as a carrier (UK international)? If not, what's the integration path? | New carrier replacing Deutsche Post — separate project if not native |
| B4 | Can Veeqo handle **Royal Mail International** alongside EVRI with country-based routing? | Need cost-split routing between RM and EVRI by destination country |
| B5 | For non-Amazon US orders: is Veeqo's native USPS integration sufficient, or is Stamps.com still needed? | Simplification — fewer integrations = better |
| B6 | Can ALL labels (Amazon + non-Amazon, US + UK) come from **one Veeqo PDF** sorted by SKU? Or will we always have multiple label sources? | Single stack vs multi-stack operator experience |
| B7 | What are Veeqo's **automation rules** capabilities? Can we set: IF channel=Amazon THEN carrier=Buy Amazon Shipping, IF product=HDMWH THEN block PH? | The crux — can Veeqo replace the PHP rule engine? |

### C. Production Handoff (Harry's Bridge)

| # | Question | Why It Matters |
|---|----------|---------------|
| C1 | What does Veeqo's **shipped export** look like? CSV format? API webhook? What fields are included? | This becomes the print trigger replacing Zero's MFG PO email |
| C2 | Can Veeqo trigger a **webhook or API call** when orders are marked shipped? | Automation: shipped → trigger image gen without manual CSV export |
| C3 | Does the shipped export contain enough data to drive **SKU → design code + device code** parsing for image generation? | HPT/IREN needs this to render correct print files |
| C4 | Can we get a **real-time feed** of shipped items, or only batch exports? | Real-time = faster production pipeline |

### D. UK + US Evaluation (Separate)

| # | Question | Why It Matters |
|---|----------|---------------|
| D1 | Is Veeqo currently **live for UK** orders, or still in test/near-ready? | We heard "near-ready" in Feb — need current status |
| D2 | Does Veeqo's UK capability match US (same features, same carrier integrations)? | UK has different carriers (RM, EVRI) — may have gaps |
| D3 | If Veeqo falls short for UK, should we evaluate **ShipStation UK** separately? | Cem said UK and US should be evaluated independently |
| D4 | Two region-locked Veeqo instances (US/UK) — can we manage **one set of rules** across both, or must rules be configured separately? | Operational overhead of maintaining two rule sets |

---

## Deliverable

**A gap analysis document** with:
1. ✅ **CAN DO** — Veeqo handles this natively, here's how to configure it
2. ⚠️ **PARTIAL** — Veeqo handles part of it, needs workaround (describe)
3. ❌ **CANNOT** — Veeqo doesn't support this, here are alternatives
4. **Recommendation** per section: proceed with Veeqo / use supplementary tool / build custom

---

## Additional Phase: End-to-End Fulfillment Review

Once the Veeqo gap analysis is done, we need Harry to extend the spec through the **full fulfillment chain:**

### Phase 2: Print File Generation (Harry's bridge)
- Shipped export → SKU parsing → design code + device code → HPT/IREN image gen → NAS
- This is Harry's build task — the "C" layer

### Phase 3: Production Site Tools
- Each site needs tools to manage production queue and pack products
- Print → pick → pack → ship workflow per location

### Phase 4: AI Visual QC (Packing Verification)
- **Concept:** Camera/tablet at packing station
- Operator holds printed product → AI compares against product image from ecellonline.com
- **Match** → continue packing → ship
- **Mismatch** → flag blocker → operator skips to next order, comes back later
- Uses: Gemini Vision / similar image recognition model
- Product images already stored by design + linked to SKUs
- **Prior work:** Harry documented "internal packing app — visual product verification" on Feb 9
- Reference: `wiki/17-harry-workspace/daily/2026-02-09.md`

### Phase 5: Inventory Management
- Each site must have accurate stock counts
- Avoid: creating POs for out-of-stock items, missing distribution opportunities
- SKU parsing: sold SKU `HTPCR-IPH17-XXXX` → deduct 1 unit of blank `HTPCR-IPH17`
- Supplier order tracking + reorder level triggers
- **Separate workstream with Harry (Finance/Ops pillar)**

---

## Timeline Suggestion

| Phase | Owner | Target |
|-------|-------|--------|
| Veeqo Gap Analysis | Harry | 1 week |
| Carrier Rules Matrix (complete) | Ava | When PHP codebase arrives from Jay Mark |
| EVRI Cost Analysis | Ava + research agent | 2 weeks |
| Print File Bridge (Layer C) | Harry | After gap analysis |
| AI Visual QC POC | Harry | After print file bridge |
| Inventory Management | Harry | Ongoing (Finance pillar) |

---

## Related
- [[wiki/23-drew-handover/DUAL_LANE_PROCESS_FLOW|Dual Lane Process Flow]]
- [[wiki/23-drew-handover/CARRIER_RULES_MATRIX|Carrier Rules Matrix]]
- [[wiki/23-drew-handover/CARRIER_RULES_UPDATE_NOTES|Carrier Rules Update Notes]]
- [[wiki/23-drew-handover/HARRY_MIGRATION_SPEC_REVIEW|Harry's Migration Spec Review]]
- [[wiki/23-drew-handover/VEEQO_REPLACEMENT_ANALYSIS|Veeqo Replacement Analysis]]
- [[wiki/23-drew-handover/PATRICK_WORKFLOW_PICKLIST_TO_IMAGE|Patrick's Workflow]]
- [[wiki/04-shipping/SHIPPING_CARRIER_RULES|Shipping Carrier Rules]]
- [[wiki/03-production/PRINT_FILE_PIPELINE|Print File Pipeline]]
