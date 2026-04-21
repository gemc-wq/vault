# 2026-04-03

**Decisions**
- **Memory Architecture Update (Cem):** Transitioned the canonical model from a 3-layer to a 4-layer architecture.
- **Source of Truth:** The Wiki is the canonical business source-of-truth; the Obsidian Vault is designated for continuity and reference only.

**Deliverables**
- Created `VAULT_OPERATING_SYSTEM.md` to define the agent's operational workspace and reflect the updated architecture.

**Knowledge**
- **4-Layer Canonical Model:**
    1. **Built-in memory:** Compact facts and pointers.
    2. **Injected operating files:** Behavior and rule files (e.g., `AGENTS.md`, `SOUL.md`).
    3. **Obsidian Vault:** Durable continuity/reference layer (read during session start/compaction; written during checkpoints/tasks).
    4. **Session search:** Automatic archival recall and safety net.
- **Infrastructure Note (Cem):** `TOOLS.md` and `MEMORY.md` are part of the agent's primary workspace infrastructure and are **not** part of the Obsidian Vault (Layer 3).

**Carry-forwards**
- Complete the next stage of vault implementation and documentation before full rollout.