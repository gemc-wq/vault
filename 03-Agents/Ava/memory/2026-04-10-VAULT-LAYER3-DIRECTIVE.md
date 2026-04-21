# Apr 10, 2:43 PM — Vault Layer 3 Memory Directive

## Cem's Clarification on Memory Architecture

Vault (`/Users/openclaw/Vault/`) is **Layer 3 Memory** — the canonical long-term reference for all agents.

### Memory Hierarchy
1. **Layer 1** — Local workspace bootstrap (SOUL.md, MEMORY.md, AGENTS.md, TOOLS.md, TASKS.md) — read-only, don't edit
2. **Layer 2** — Daily logs (memory/YYYY-MM-DD.md) — transient session context
3. **Layer 3** — **Vault** — canonical, persistent, shared across all agents
4. **Layer 4** — **Wiki** — operational knowledge (SOPs, procedures, reference docs)

### What This Means
- Start each session by reading Vault SOUL + MEMORY_BUSINESS_CONTEXT first
- Refer to Wiki for operational procedures
- End session: sync significant decisions back to Vault
- Never edit local bootstrap files (they're read-only references)
- Vault is the source of truth for anything that needs to persist

### Vault Locations (Ava)
- **SOUL:** `/Users/openclaw/Vault/03-Agents/Ava/SOUL_V2_CREATIVE_DIRECTOR.md`
- **Memory:** `/Users/openclaw/Vault/03-Agents/Ava/MEMORY_BUSINESS_CONTEXT.md` (53KB)
- **Daily logs:** `/Users/openclaw/Vault/03-Agents/Ava/memory/` (116 files as of Apr 10)

### Agent Model Update
- **Hermes** (Operations Librarian) runs on **Gemma 4** (not Gemini Flash)

---

## Actions Taken This Session

✅ **Shopify Title Optimization** — All 26 designs updated with SEO names
✅ **SEO Content Project Created** — `/projects/seo-content-creation/` with training materials
✅ **Design Mappings Documented** — All 26 designs + Claude Desktop approvals saved
✅ **Vault Memory Architecture Clarified** — Per Cem's directive

---

## To Do Before Next Session
- [ ] Read Vault SOUL + MEMORY_BUSINESS_CONTEXT to prime context
- [ ] Sync this session's learnings to Vault (Agent folder + Wiki)
- [ ] Update local MEMORY.md to reference Vault as Layer 3

