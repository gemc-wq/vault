# 04-Shared — Cross-Agent Workspace

This directory enables agents to collaborate without overwriting each other's files.

## Structure

| Folder | Purpose | Who Writes |
|--------|---------|-----------|
| `active/` | In-progress shared work (one subfolder per task) | Any assigned agent |
| `handoffs/` | Completed work awaiting pickup by another agent | Any agent (deposit only) |
| `decisions/` | Cross-agent decisions that affect multiple agents | Athena only |

## Rules

1. **Never edit** another agent's file — create your own alongside it
2. **Name your files** with your agent name prefix: `ava-analysis.md`, `harry-spec.md`
3. **Athena synthesises** shared work into final deliverables
4. **Move completed work** to the relevant `02-Projects/` folder when done

## Full Framework

See `~/Vault/00-Company/AGENT_COLLABORATION.md` for the complete collaboration protocol.
