# 2026-03-09

**Decisions**
- **VCO Gap Analysis**: Cem approved proceeding with the gap analysis for VCO. The scope must cover the entire process through to fulfillment and include a review of relevant documents as an extra phase.
- **PO Routing Logic**: Cem defined the rules for Purchase Orders:
    - **Location Rules**: Based on inventory location and operational status. If a printer is down at a specific location, printing must be dynamically diverted to the Philippines.
    - **Carrier Rules**: These are fixed and straightforward.
- **Handoff**: The gap analysis brief is to be placed in the handoff folder and Harry is to be notified.

**Deliverables**
- **VCO Gap Analysis Brief**: Prepared for Harry.

**Blockers**
- **Rclone Sync**: Harry failed to pull updates from Rclone (noted/reminded).

**Knowledge**
- **PO Workflow & Prioritization**: 
    - **Priority 1**: Philippines stock items (Wave 1). This is processed first thing in the Philippines morning to allow them to prioritize printing labels and generating print files.
    - **Priority 2**: UK and US stock (Afternoon waves). These are smaller POs processed to meet local same-day shipping cut-offs (2 PM/3 PM).
    - **Timezone Context**: Philippines is 8 hours ahead of the UK and 12 hours ahead of the US.
- **POSO Process**: This is a separate finance task for intercompany billing and is out of scope for the current analysis.
- **Inventory Management**: The primary goal is ensuring site-specific accuracy to prevent wasted PO creation and avoid stockouts.
- **Visual Verification**: Operational staff should use AI image recognition (utilizing images from the Ecell Online domain) to verify that printed products match the intended product images.
- **Technical Detail**: The parsing logic for SKUs involves approximately 1,300 items.

**Carry-forwards**
- **Print Generation**: Harry is tasked with working on the print/card generation process.
- **Memory Fixes**: Recommend the recently implemented memory fixes to Harry.