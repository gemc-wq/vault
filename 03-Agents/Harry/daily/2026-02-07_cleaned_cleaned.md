# 2026-02-07

## Decisions
- **Agent Team Structure**: Cem (CEO), Harry (Lead Automator), and Ava (Lead Strategist).
- **Cost Optimization**: Assigned heavy coding to **Ava** (utilizing free CLI subscriptions) to minimize API costs; sub-agents default to **Gemini Flash**; **Opus 4.6** reserved for complex architecture; N8N bots use **GPT-4o-mini**.
- **Infrastructure**: Disabled 30-minute iMac node health check cron to reduce token consumption.

## Deliverables
- **Agent Org Chart**: Documented 14 agents across 6 models.
- **Amazon SP-API Documentation**: Created `projects/amazon-sp-api/SP-API-GUIDE.md` and `projects/amazon-sp-api/APPLICATION-CHECKLIST.md`.
- **Creative Pipeline Architecture**: Documented flow in `projects/design-automation/CREATIVE_PIPELINE_ARCHITECTURE.md`.
- **Design Assets**: Saved 4 product shot automation references to Drive.

## Blockers
- **Amazon SP-API**: Awaiting API key from Cem.
- **Ecell Command Centre**: Pending final website design.
- **Avatar Project**: Awaiting video files from Cem for cloning.

## Knowledge
- **Technical Specs**:
    - **N8N**: v2.6.4, port 5678, API key at `~/.config/n8n/api_key`.
    - **CS Chat Agent**: `POST /webhook/headcase-chat` (GPT-4o-mini via OpenRouter).
    - **Integrations**: GitHub and Vercel connected to `gemc99-boop`.
    - **Amazon SP-API Reports**: `GET_SALES_AND_TRAFFIC_REPORT`, `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA`, and `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2`.
- **Process Insights**:
    - **Gemini Gems**: Can generate API tokens