# 2026-02-08

## Decisions
- **Cost Policy Update**: Migrated sub-agents (spark-engine, radar-scout, prism-analyst, pixel-merchant, nexus-integrator) to Gemini Flash to achieve ~200x cost savings.
- **Agent Routing**: Harry uses Opus 4.6; heavy coding tasks routed to Ava (via Claude Code/Codox); N8N bots utilize gpt-4o-mini.

## Deliverables
- **Image Gen Documentation**: Created Notion page (`3006887b-1dd7-80a7-bd8c-ff227bd8feb1`) and `projects/design-automation/PHONE_CASE_IMAGE_GEN_PROMPTS.md` (includes Python stitcher script and 8K photorealistic specs).
- **Agent Configuration**: Updated `AGENT_CONFIG.md` with new org chart (`projects/design-automation/org-chart-feb2026.jpg`).
- **Skill Deployment**: Deployed Gamma skill (`SKILL.md` and `gamma.sh`) to `/Users/clawdbot/clawd/skills/gamma/` for Ava.

## Blockers
- **Resolved**: iMac node connection failure (caused by empty allowlist in `exec-approvals.json`) fixed by Cem via manual file update and node restart.

## Knowledge
- **Node Configuration**: The command `clawdbot approvals allowlist add --node "X"` modifies the **Gateway**, not the node. Nodes read from `~/.clawdbot/exec-approvals.json`.