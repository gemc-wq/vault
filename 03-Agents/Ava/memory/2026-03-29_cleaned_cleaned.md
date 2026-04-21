# 2026-03-29 (Sunday)

## Decisions
- **Model Stack Migration**: Moved agent team to free OAuth models (Gemini 3.1 Pro + GPT-5.4 Codex) to eliminate Anthropic costs.
- **Memory Upgrade**: Upgraded system memory embeddings to `gemini-embedding-2-preview` (3072 dimensions) for improved search quality.
- **Development Priority**: Confirmed Zero 2.0 priority is Evri Portal (not XAMPP) for Jay Mark's onboarding.

## Deliverables
- **GCP Provisioning**: Created Service Account `jaymark-bq-reader` (`projects/fulfillment-portal/jaymark-bq-key.json`) with `bigquery.dataViewer` and `biglam.jobUser` roles.
- **Zero Documentation**: Completed 6 architectural files in `wiki/32-fulfillment-portal/zero-docs/` (PO routing, order import, inventory logic, and royalty calculations).
- **Agent Deployment**: Created **Iris** (Image Production Engineer) for PSD automation and batch processing.
- **Market Research**: Completed One Piece Market Research report (`projects/licensing/ONE_PIECE_MARKET_RESEARCH.md`).
