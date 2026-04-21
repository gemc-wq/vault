# Apr 10

**Decisions**
- **Vault Architecture**: Per Cem's directive, Vault (`/Users/openclaw/Vault/`) is established as the Layer 3 canonical long-term reference for all agents.
- **Agent Model Update**: Hermes (Operations Librarian) now runs on Gemma 4.

**Deliverables**
- **Shopify Title Optimization**: 26 designs updated with SEO-optimized names.
- **SEO Content Project**: Created at `/projects/seo-content-creation/` (includes training materials).
- **Design Mappings**: Documented 26 designs and saved Claude Desktop approvals.

**Knowledge**
- **Memory Hierarchy**:
    - **Layer 1 (Local Bootstrap)**: `SOUL.md`, `MEMORY.md`, `AGENTS.md`, `TOOLS.md`, `TASKS.md` (Read-only).
    - **Layer 2 (Daily Logs)**: `memory/YYYY-MM-DD.md` (Transient session context).
    - **Layer 3 (Vault)**: `/Users/openclaw/Vault/` (Canonical, persistent, shared).
    - **Layer 4 (Wiki)**: Operational knowledge, SOPs, and reference docs.
- **Operational Protocol**: Start sessions by reading Vault `SOUL` + `MEMORY_BUSINESS_CONTEXT`; refer to Wiki for procedures; end sessions by syncing significant decisions back to Vault.
- **Ava's Vault Paths**:
    - **SOUL**: `/Users/openclaw/Vault/03-Agents/Ava/SOUL_V2_CREATIVE_DIRECTOR.md`
    - **Memory**: `/Users/openclaw/Vault/03-Agents/Ava/MEMORY_BUSINESS_CONTEXT.md`
    - **Daily Logs**: `/Users/openclaw/Vault/03-Agents/Ava/memory/`