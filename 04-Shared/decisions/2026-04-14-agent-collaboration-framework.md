# Decision: Agent Collaboration Framework
**Date:** 2026-04-14 | **Decided by:** Cem + Athena | **Status:** Active

## Decision
Adopt a structured collaboration framework with:
1. Standard handoff protocol via `03-Agents/[Name]/handoffs/` folders
2. Shared workspace at `04-Shared/` for cross-agent work
3. No-overwrite rule — agents create separate files, Athena synthesises
4. Mandatory session bootstrap: check task sheet + handoffs every session
5. Navigation pointers coded into each agent's TOOLS.md

## Context
- Ava was already dropping handoff docs into Hermes's folder ad-hoc
- Hermes's SOUL referenced a stale `~/shared-agent-workspace/inbox/` path
- No standard way for agents to discover shared company knowledge
- YouTube reference showed other OpenClaw users using shared agent folders

## What Changed
- Created `~/Vault/00-Company/AGENT_COLLABORATION.md` (master reference)
- Created `~/Vault/04-Shared/` directory (active, handoffs, decisions)
- Updated Ava TOOLS.md, Harry TOOLS.md, Hermes SOUL.md with session bootstrap
- Updated Ava VAULT_GUIDE.md with 04-Shared reference
- Created handoffs/ folder in each agent directory

## Agents Affected
All: Ava, Harry, Hermes, Athena
