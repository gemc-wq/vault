# Handoff: Veeqo Gap Analysis — From Ava
*Date: 2026-03-09 | Priority: P0*

## Harry — Action Required

Cem has approved the Veeqo Gap Analysis as the next priority. This gates the entire shipping migration.

### Your deliverable:
A gap analysis document answering 20 specific questions across 4 sections (see `VEEQO_GAP_ANALYSIS_BRIEF.md`).

Format: For each question, classify as:
- ✅ **CAN DO** — Veeqo handles natively, here's how
- ⚠️ **PARTIAL** — needs workaround (describe it)  
- ❌ **CANNOT** — not supported, here are alternatives

### Files in this handoff:
1. **VEEQO_GAP_ANALYSIS_BRIEF.md** — The main brief with all 20 questions + context
2. **DUAL_LANE_PROCESS_FLOW.md** — Patrick's current dual-lane operation (visual + MD)
3. **CARRIER_RULES_MATRIX.md** — Draft carrier rules (needs PHP codebase to complete)
4. **CARRIER_RULES_UPDATE_NOTES.md** — Cem's latest requirements (EVRI, PO wave sequencing, SKU sorting)
5. **HARRY_MIGRATION_SPEC_REVIEW.md** — My review of your migration spec
6. **PATRICK_WORKFLOW_PICKLIST_TO_IMAGE.md** — Patrick's workflow documentation

### Key context from Cem today:
- Amazon Buy Shipping is MANDATORY (late delivery protection)
- EVRI replacing Deutsche Post for UK international — separate project
- Labels MUST be sorted by SKU alphabetically (operational requirement)
- PO wave sequencing: PH first → UK second → US third (timezone-driven)
- SO/PO process is separate (finance) — don't conflate with shipping
- Non-Amazon labels: not tied to Veeqo — could use ShipStation or others
- UK and US must be evaluated SEPARATELY

### Target: 1 week
