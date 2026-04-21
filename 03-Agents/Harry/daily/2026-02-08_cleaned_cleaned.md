# 2026-02-08

## Decisions
- **Cost Policy Update**: Sub-agents (spark-engineer, radar-scout, prism-analyst, pixel-merchant, nexus-integrator) migrated to Gemini Flash to achieve ~200x cost savings. Harry uses Opus 4.6; heavy coding tasks routed to Ava (via Claude Code/Codex); N8N bots utilize gpt-4o-mini.

## Deliverables
- **Image Gen Documentation**: Created Notion page (`3006887b-1dd7-80a7-bd8c-ff227bd8feb1`) and `projects/design-automation/PHONE_CASE_IMAGE_GEN_PROMPTS.md` (includes Python stitcher script and 8K photorealistic specs).
- **Agent Configuration**: Updated `AGENT_CONFIG.md` with new org chart; chart saved to `projects/design-automation/org-chart-feb2026.jpg`.
- **Skill Deployment**: Deployed Gamma skill (`SKILL.md` and `gamma.sh`) to `/Users/clawdbot/clawd/skills/gamma/` for Ava.

## Blockers
- **Resolved**: iMac node connection failure caused by an empty allowlist in `exec-approvals.json`. Fixed by Cem via manual file update and node restart.

## Knowledge
- **Node Configuration**: The command `clawdbot approvals allowlist add --node "X"` modifies the **Gateway**, not the node. Nodes read from `~/.clawdbot/exec-approvals.json`.