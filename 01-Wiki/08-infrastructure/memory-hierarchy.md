# Memory Hierarchy
*Auto-created by vault compiler on 2026-04-13 | Consolidated*

## 4-Layer Architecture
- **Layer 1 (Local Bootstrap)**: `SOUL.md`, `MEMORY.md`, `AGENTS.md`, `TOOLS.md`, `TASKS.md` (Read-only)
- **Layer 2 (Daily Logs)**: `memory/YYYY-MM-DD.md` (Transient session context)
- **Layer 3 (Vault)**: `/Users/openclaw/Vault/` (Canonical, persistent, shared long-term reference for all agents)
- **Layer 4 (Wiki)**: Operational knowledge, SOPs, and reference docs

## Implementation
- Vector store: SQLite database at `memory/main.sqlite`
- `MEMORY.md` file maintained in each agent workspace for curated memory
- Automated sync to Vault occurs nightly at 11 PM

See also: [[data-architecture]], [[agent_vault_paths]]
