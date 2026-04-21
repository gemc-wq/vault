# Brain — Root Index
*Last updated: 2026-02-27*

This folder is the shared knowledge base for Harry (COO, Windows) and Ava (CPSO, iMac).
It is synced via rclone from both hosts.

---

## Navigation

| Document | Description |
|----------|-------------|
| `MEMORY_ARCHITECTURE.md` | **START HERE** — Full semantic memory architecture, Supabase setup, schemas, scripts, migration plan |
| `SOPs/AGENT_MEMORY_SOP.md` | Condensed memory rules for Harry + Ava (paste into SOUL/AGENTS files) |
| `SOPs/` | All standard operating procedures |
| `Projects/` | Per-project folders with docs, CSVs, reports |
| `Research/` | Research reports and competitor analysis |
| `Archive/` | Completed projects and old backups |

---

## Infrastructure Quick Reference

| Item | Value |
|------|-------|
| rclone remote | `gdrive:` |
| Brain root | `gdrive:Clawdbot Shared Folder/Brain/` |
| Local mirror (Windows/Harry) | `C:\Users\gemc\clawd\gdrive_shared\Brain\` |
| Local mirror (iMac/Ava) | `/Users/clawdbot/clawd/gdrive_shared/Brain/` |
| Supabase project | `nuvspkgplkdqochokhhi.supabase.co` |
| Semantic memory table | `agent_memory` (see MEMORY_ARCHITECTURE.md) |

---

## Active Projects (update here when status changes)

| Project ID | Description | Owner | Status |
|------------|-------------|-------|--------|
| `nbcu-po-automation` | NBCU PO → FedEx CSV pipeline | Harry | 🟡 Active |
| `sales-dashboard` | Cloud Run + BigQuery sales viz | Harry | 🟡 Active |
| `ecell-website` | B2B corporate site rebuild | Ava | 🆕 Scoping |
| `saas-spinoff` | Productize internal tools | Ava | 🆕 Concept |
| `catalog-health` | Nightly Supabase catalog health checks | Harry | 🟢 Running |
| `supabase-schema` | Catalog + orders schema build | Harry | 🟡 Active |
| `marketing-campaigns` | Social media + content calendar | Harry + Ava | 📋 Backlog |

---

## Sync Commands

```powershell
# Harry — pull Brain from Drive
rclone sync "gdrive:Clawdbot Shared Folder/Brain" "C:\Users\gemc\clawd\gdrive_shared\Brain" --log-level INFO

# Harry — push local changes to Drive
rclone sync "C:\Users\gemc\clawd\gdrive_shared\Brain" "gdrive:Clawdbot Shared Folder/Brain" --log-level INFO
```

```bash
# Ava — pull Brain from Drive
rclone sync "gdrive:Clawdbot Shared Folder/Brain" /Users/clawdbot/clawd/gdrive_shared/Brain --log-level INFO
```

---

*Brain maintained by Harry (COO) and Ava (CPSO). Architecture by Chief Memory Architect (CEO subagent), 2026-02-27.*
