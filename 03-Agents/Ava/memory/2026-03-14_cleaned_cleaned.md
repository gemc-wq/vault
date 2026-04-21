# Memory Log — March 14, 2026 (Saturday)

## Decisions
- **Shopify Product Architecture (Approved by Cem):** 
  - Structure: 1 design × 1 device.
  - Variants: Use "Case Type" (Soft Gel, Hard Case, Leather Wallet, Clear MagSafe, Black MagSafe) with 1–5 variants per product.
  - Organization: Use tags (lineup, brand, device, device_brand, type) for auto-collections.
  - Reference: `research/cassetify-shopify-structure.md`
- **Product Type & Pricing Restrictions (Cem Directive):** Only 5 types allowed for Shopify/Walmart:
  - HTPCR (Soft Gel): $17.95
  - HB401 (Hard Case): $19.95
  - HLBWH (Leather Wallet): $24.95
  - HB6 (Clear MagSafe): $24.95
  - HB7 (Black MagSafe): $24.95
- **Research Routing Rule (Cem Directive):** 
  - Simple research $\rightarrow$ Gemini 3.1 Flash (Bolt agent).
  - Complex research $\rightarrow$ Gemini 3.1 Pro.

## Deliverables
- **Sven Sub-agent Documentation:** Added role, task backlog, dispatch method, and 8 council roles to `TOOLS.md`.
- **Shopify Import Files (Generated via `scripts/generate_shopify_csv.py`):** 
  - Test (10 designs): `projects/sku-staging/output/shopify_test_10designs.csv`
  - Full (50 designs): `projects/sku-staging/output/shopify_import_top50.csv`
- **BC Coverage Report:** `projects/sku-staging/BC_COVERAGE_REPORT.md` (identifies 7 missing champions).

## Blockers
- **Shopify Automation:** Missing Shopify Admin API token for automated uploads.
- **Fulfillment:** 28 items from Friday FL W1 batch remain unprinted/unshipped.

## Knowledge
- **BigCommerce API:** 
  - Store hash: `otle45p56l`. 
  - Credentials: Stored in `TOOLS.md`. 
  - Custom fields: `BrandCode`, `DeviceBrand`, `DeviceModel`.