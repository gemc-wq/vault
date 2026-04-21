# Daily Log — 2026-03-13 (Friday)

## Decisions
- **Repository Access:** Cem to grant Chad access to `github.com/gemc-wq/zero-php`.
- **EAN/UPC Strategy:** Use Amazon Active Listings or GS1 generation (BigCommerce lacks custom EAN fields).
- **Bug Fix:** Cem to refresh "US All Listings" file to resolve PULSE Region Gap Finder bug.

## Deliverables
- **RAG Pattern Cards:** Batch 11-30 uploaded to `Brain/Projects/goheadcase/rag/patterns/`.
- **Currency Normalization:** Completed Supabase `orders` table backfill (319K+ rows) via `projects/data-migrations/001_currency_normalization.sql`.
- **SKU Staging Pipeline:** Launched with 200 HTPCR champions; output: `projects/sku-staging/htpcr_champions.json`; documentation: `projects/sku-staging/SKU_STAGING_PLAN.md`.
- **BigCommerce API:** Connection established for store `otle45p56l` (1.87M SKUs); credentials in `TOOLS.md`.

## Blockers
- **Walmart Expansion:** 86.5% UPC/EAN data gap identified for HTPCR champions.
- **Agent Harry:** 4 tasks overdue (COGS, Chad file, BQ audit, Shopify connector); escalation required Monday.
- **Print Automation:** Awaiting EPS format documentation from creative team.
- **Order Fulfillment:** Items `HLBWH-IPDA1324` and `HHYBK-IPH16` require "discon" tagging.

## Knowledge
- **BigCommerce API Schema (Custom Fields):** `BrandCode`, `DeviceBrand`, `DeviceModel`, `ProdCat`, `Product Type`, `TeamCat`, `DesignName`, `ParentSKU`, `GenericKeywords`, `