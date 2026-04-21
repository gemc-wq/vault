# 2026-03-29 (Sunday)

## Decisions
- **Model Stack Migration**: Switched to Gemini 3.1 Pro + GPT-5.4 Codex to eliminate Anthropic costs.
- **Development Priority**: Set Zero 2.0 priority to Evri Portal (over XAMPP) for Jay Mark's onboarding.

## Deliverables
- **GCP Provisioning**: Created Service Account `jaymark-bq-reader` (`projects/fulfillment-portal/jaymark-bq-key.json`) with `bigquery.dataViewer` and `biglam.jobUser` roles.
- **Zero Documentation**: Completed 6 architectural files in `wiki/32-fulfillment-portal/zero-docs/` (covering PO routing, order import, inventory logic, and royalty calculations).
- **Agent Deployment**: Deployed **Iris** (Image Production Engineer) for PSD automation and batch processing.
- **Market Research**: Completed One Piece Market Research report (`projects/licensing/ONE_PIECE_MARKET_RESEARCH.md`).

## Knowledge
- **Memory Upgrade**: Upgraded system memory embeddings to `gemini-embedding-2-preview` (3072 dimensions) for improved search quality.