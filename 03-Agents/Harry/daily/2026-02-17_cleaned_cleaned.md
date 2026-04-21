# 2026-02-17

## Decisions
- **AI Sales Bot:** Project on hold (per Cem) pending discussion on AWS vs. BigCommerce CDN and potential GCP image migration.
- **SKU Standardization:** Cem approved adding `HC-` prefix to legacy inventory device codes to ensure direct matching (`product_type || '-' || device`).
- **Model Migration:** Switched primary model to `claude-sonnet-4-6` for cost efficiency ($3/$15 per 1M tokens).
- **Agent Org Chart Restructure:** New routing implemented:
    - **Harry (COO) & Content/Copy:** Sonnet 4.6.
    - **CEO Sub-agent:** Opus 4.6 (strategic/architecture).
    