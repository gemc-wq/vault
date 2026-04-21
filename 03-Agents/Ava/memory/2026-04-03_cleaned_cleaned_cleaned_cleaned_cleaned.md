# 2026-04-03

**Decisions**
- **Memory Architecture (Cem):** Transitioned from a 3-layer to a 4-layer architecture.
- **Source of Truth:** Defined the Wiki as the business source-of-truth; the Obsidian Vault is strictly for continuity and reference.

**Deliverables**
- Created `VAULT_OPERATING_SYSTEM.md` to define the agent's operational workspace and reflect the updated architecture.

**Knowledge**
- **4-Layer Canonical Model:** 1. Built-in memory (facts/pointers); 2. Injected operating files (e.g., `AGENTS.md`, `SOUL.md`); 3. Obsidian Vault (continuity/reference); 4. Session search (archival recall).
- **Infrastructure (Cem):** `TOOLS.md` and `MEMORY.md` are part of the primary workspace infrastructure and are **not** part of the Obsidian Vault (Layer 3).

**Carry-forwards**
- Complete the next stage of vault implementation and documentation before full rollout.