# 2026-02-14

## Decisions
- **Token Usage Policy (Cem):** Use Opus for strategy and planning; utilize sub-agents (Kimi K2.5 or Gemini Flash) for coding builds to optimize costs.

## Deliverables
- **Model Upgrade:** Integrated `claude-opus-4-6` into `models.generated.js` and patched gateway configuration.
- **Project Sunrise (Mission Control) Launch:** Deployed at `projects/mission-control/` using Next.js 16, Tailwind, and Notion API.
- **GitHub Repository:** Created `github.com/gemc99-boop/ecell-ops` (125 files) with `gh` CLI auth and credential helper configured.
- **Task Compilation:** Compiled master To-Do list (34 items) from all memory files and Notion.

## Blockers
- **IT Handover:** Critical infrastructure ownership (cron jobs, API integrations, picking lists, CDN) is unverified due to the IT Manager's departure.
- **Supabase Connectivity:** Direct Postgres connections are failing with stored DB passwords.

## Knowledge
- Notion API Configuration (details pending)