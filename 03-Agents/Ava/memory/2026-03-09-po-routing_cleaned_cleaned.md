# 2026-03-09

**Decisions**
- **VCO Gap Analysis**: Cem approved scope covering the entire process through to fulfillment, including a document review phase.
- **PO Routing Logic**: Cem defined rules:
    - **Location**: Based on inventory/operational status; if a local printer is down, printing diverts to the Philippines.
    - **Carrier**: Fixed rules.
- **Handoff**: Gap analysis brief to be placed in the handoff folder; notify Harry.

**Deliverables**
- **VCO Gap Analysis Brief**: Prepared for Harry.

**Blockers**
- **Rclone Sync**: Harry failed to pull updates from Rclone.

**Knowledge**
- **PO Workflow & Prioritization**: 
    - **Priority 1**: Philippines stock (processed in PH morning) to allow for label and print file generation.
    - **Priority 2**: UK and US stock (afternoon waves) to meet 2 PM/3 PM local shipping cut-offs.
    - **Timezone Context**: PH is +8h UK and +12h US.
- **POSO Process**: Separate finance task for intercompany billing; currently out of scope for analysis.
- **Inventory Management**: Focus on site-specific accuracy to prevent wasted PO creation and stockouts.
- **Visual Verification**: Use AI image recognition (via Ecell Online domain) to verify printed products against intended images.
- **Technical Detail**: SKU parsing logic involves approximately 1,300 items.

**Carry-forwards**
- **Print Generation**: Harry to work on the print/card generation process.
- **Memory Fixes**: Recommend recently implemented memory fixes to Harry.