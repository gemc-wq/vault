# 2026-04-03

**Decisions**
- **Memory Architecture (Cem):** Transitioned from a 3-layer to a 4-layer architecture.
- **Source of Truth:** Defined the Wiki as the business source-of-truth; the Obsidian Vault is strictly for continuity and reference.

**Deliverables**
- Created `VAULT_OPERATING_SYSTEM.md` to define the agent's operational workspace and reflect the updated architecture.

**Knowledge**
- **4-Layer Canonical Model:** 
    1. **Built-in memory:** Compact facts and pointers.
    2. **Injected operating files:** Behavior/rule files (e.g., `AGENTS.md`, `SOUL.md`).
    3. **Obsidian Vault:** Durable continuity/reference layer.
    4. **Session search:** Automatic archival recall and safety net.
- **Infrastructure (Cem):** `TOOLS.md` and `MEMORY.md` are part of the primary workspace infrastructure and are **not** part of the Obsidian Vault (Layer 3).

**Carry-forwards**
- Complete the next stage of vault implementation and documentation before full rollout.