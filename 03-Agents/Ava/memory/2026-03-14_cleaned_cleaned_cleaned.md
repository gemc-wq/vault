# Memory Log — March 14, 2026 (Saturday)

## Decisions
- **Shopify Product Architecture (Approved by Cem):** 1 design × 1 device. Use "Case Type" variants (Soft Gel, Hard Case, Leather Wallet, Clear MagSafe, Black MagSafe) and tags (`lineup`, `brand`, `device`, `device_brand`, `type`) for auto-collections. Ref: `research/cassetify-shopify-structure.md`.
- **Product Type & Pricing Restrictions (Cem Directive):** Only 5 types allowed for Shopify/Walmart: HTPCR ($17.95), HB401 ($19.95), HLBWH ($24.95), HB6 ($24.95), HB7 ($24.95).
- **Research Routing Rule (Cem Directive):** Simple research $\rightarrow$ Gemini 3.1 Flash; Complex research $\rightarrow$ Gemini 3.1 Pro.

## Deliverables
- **Sven Sub-agent Documentation:** Updated `TOOLS.md` with role, task backlog, dispatch method, and 8 council roles.
- **Shopify Import Files (via `scripts/generate_shopify_csv.py`):** 
  - `projects/sku-staging/output/shopify_test_10designs.csv` (10 designs)
  - `projects/sku-staging/output/shopify_import_top50.csv` (50 designs)
- **BC Coverage Report:** `projects/sku-