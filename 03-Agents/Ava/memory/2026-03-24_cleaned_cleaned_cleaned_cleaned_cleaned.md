# 2026-03-24 — Daily Notes

## Decisions
- **Brand Identity & Strategy:** Established **Delegait** as a new AI automation SaaS/Consultancy targeting SMBs (E-commerce/Professional Services) via a tiered model (Platform, Advisory, and Starter Packs).
- **System Architecture:** Approved **Flash Triage Agent** for semantic search (QHD), intent classification, and delegation.
- **Sub-Agent Structure:** Sub-agents will utilize individual `AGENTS.md` and memory, managed via a centralized memory coordinator.

## Deliverables
- **SKU Standardization:** Created `projects/new-products/SKU_STRUCTURE.md` using format: `{PRODUCT_TYPE}-{COLOR}-{DESIGN}-{VARIANT}`.
- **Marketing Strategy:** Created `projects/marketing/NARUTO_UK_IPLAYER_OPPORTUNITY.md` regarding the BBC iPlayer Naruto launch.

## Blockers
- **HB401 Sprint (Critical):** Zero progress on 31 device×design combos (primary gap: iPhone 13).
- **NFL License:** Renewal decision pending (expires March 31).
- **Resolved:** `image_generate` tool (Gemini 3.1 Flash Image + OpenAI GPT-Image-1) is functional, supporting up to 5 reference images for product compositing.

## Knowledge
- **Process (Cem’s Pipeline):** Ideation $\rightarrow$ Auto-generation (Content/Images) $\rightarrow$ Marketing Image creation $\rightarrow$ Amazon Verification Loop.
- **Compliance:** 
    - **FC Barcelona:** New style guide and product approval/reporting process via Dependable Solutions.
    - **NBCU:** New POs (e.g., 3400798609) require vendor acknowledgment in the portal.
- **Technical Specs:** Models: GPT-5.4 nano/mini (classification/orchestration).