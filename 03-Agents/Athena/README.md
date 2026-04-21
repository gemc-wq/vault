# Athena -- Master Orchestrator

| Field | Value |
|-------|-------|
| Model | Claude Opus 4.6 |
| Platform | ZEUS bot |
| Machine | **Mac Studio** (user: openclaw) |
| SOUL | ~/zeus-agent/workspace/SOUL.md (V4) |
| Status | Live |

## Role
Master Orchestrator. Dispatches tasks, monitors 6 pillars, unblocks work, reports to Cem.

## Comms
- Receives: Telegram from Cem, ZEUS bot
- Dispatches to agents via: OpenClaw gateway (Ava, Harry) or Vault handoffs (Hermes)

## Key Files
- SOUL: ~/zeus-agent/workspace/SOUL.md
- Working context: ~/zeus-agent/data/working-context.md
- Daily logs: ~/zeus-agent/data/daily/
- Skills: ~/Vault/00-Company/skills/

## Handoff Protocol
- Deposit tasks in agent's handoffs/ folder using standard template
- Template: Vault/00-Company/skills/delegation/handoff-template.md
