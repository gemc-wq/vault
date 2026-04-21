# 2026-03-09

**Decisions**
- **VCO Gap Analysis Scope (Approved by Cem)**: Includes the entire process through fulfillment, including document review.
- **PO Routing Logic (Defined by Cem)**: Location-based routing (e.g., divert to PH if local printer is down) with fixed carrier rules.
- **Handoff Protocol**: Gap analysis briefs must be placed in the handoff folder with a notification sent to Harry.

**Deliverables**
- **VCO Gap Analysis Brief**: Prepared for Harry.

**Blockers**
- **Rclone Sync**: Harry is unable to pull updates from Rclone.

**Knowledge**
- **PO Workflow & Prioritization**: 
    - **Priority 1**: PH stock (morning) for label/print generation.
    - **Priority 2**: UK/US stock (afternoon) to meet 2 PM/3 PM local shipping cut-offs.
    - **Timezone Context**: PH is +8h UK and +12h US.
- **POSO Process**: Intercompany billing is a separate finance task and currently out of scope.
- **Inventory Management**: Focus on site-specific accuracy to prevent stockouts and redundant PO creation.
- **Visual Verification**: Use AI image recognition (via Ecell Online domain) to verify printed products against intended images.
- **Technical Detail**: SKU parsing logic involves ~1,300 items.

**Carry-forwards**
- **Print Generation**: Harry to develop the print/card generation process.
- **Memory Fixes**: Communicate recently implemented memory fixes to Harry.