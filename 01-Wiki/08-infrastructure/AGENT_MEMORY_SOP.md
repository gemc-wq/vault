# AGENT MEMORY SOP
*Version 1.0 | 2026-02-27 | Applies to: Harry + Ava*
*Full architecture: gdrive:Clawdbot Shared Folder/Brain/MEMORY_ARCHITECTURE.md*

---

## Where Memory Lives

| Store | What's in it | When to use |
|-------|-------------|-------------|
| **Supabase `agent_memory`** | Live semantic memory, shared Harry↔Ava | Primary: decisions, project state, SOPs, insights |
| **MEMORY.md** (workspace) | Cold-start bootstrap (<150 lines) | Session start; offline fallback |
| **memory/YYYY-MM-DD.md** | Daily raw session log | Always write throughout session |
| **gdrive:Brain/** | Human-readable docs, reports, assets | Reports, PDFs, design files, SOPs |

---

## Session Start Routine (non-negotiable)

```
1. Read MEMORY.md
2. Read memory/YYYY-MM-DD.md (today)
3. If working on a project: search Supabase for current state
   → .\scripts\memory_ops.ps1 -op search -query "<project> current state and blockers" -project <project-id>
4. Check for cross-agent handoffs:
   → .\scripts\memory_ops.ps1 -op search -query "pending handoffs and tasks for me" -matchCount 5
```

---

## When to Store to Supabase

**DO store when:**
- ✅ Significant decision made (what / why / what was rejected)
- ✅ Project milestone hit or blocker encountered/resolved
- ✅ New stable business fact confirmed (license, channel policy, supplier)
- ✅ Research finding worth keeping past today
- ✅ Handoff needed to other agent (Ava ↔ Harry)
- ✅ SOP created or updated

**DO NOT store:**
- ❌ Scratch calculations or intermediate work
- ❌ Info retrievable from source in <5s (live API data, current prices)
- ❌ Credentials or API keys
- ❌ Verbatim conversation transcripts (summarize instead)

**When to update MEMORY.md (rare):**
Only for ultra-stable facts that must load even if Supabase is unreachable.
Keep MEMORY.md under 150 lines.

---

## Mandatory Metadata Tags

Every Supabase store call must include these fields:

```
type:     fact | project | decision | sop | insight | event
channel:  amazon | ebay | walmart | shopify | ecell | all
project:  <exact project ID from PROJECTS.md, or "" if none>
status:   active | closed | superseded
owner:    harry | ava | shared
tier:     1 (stable/never expires) | 2 (active, default) | 3 (episodic, 30d TTL)
```

**Project IDs (use exactly):**
`nbcu-po-automation` | `sales-dashboard` | `ecell-website` | `saas-spinoff`
`catalog-health` | `marketing-campaigns` | `supabase-schema`

---

## How to Write Good Semantic Queries

**Rule:** Always include at least one of: brand name, channel name, or project ID in the query string. Add at least one `meta_filter` constraint.

```
✅ GOOD: "Amazon listing policy for licensed NFL Head Case products"
✅ GOOD: "NBCU FedEx shipment workflow and current PO status"
✅ GOOD: "Supabase catalog schema device model SKU format"
✅ GOOD: "Head Case Designs royalty calculation method per unit sold"
✅ GOOD: "sales dashboard BigQuery Cloud Run deployment status"

❌ BAD:  "orders"
❌ BAD:  "what happened last week"
❌ BAD:  "project status"
❌ BAD:  "information about listings"
```

---

## Store Commands (Quick Reference)

**Harry (PowerShell):**
```powershell
# Store a decision
.\scripts\memory_ops.ps1 -op store `
  -content "DECISION: [what] RATIONALE: [why] REJECTED: [alternatives]" `
  -type decision -project "nbcu-po-automation" -tier 2

# Store a stable fact (tier 1 = never expires)
.\scripts\memory_ops.ps1 -op store `
  -content "Head Case Designs royalty rate for NFL licenses is X% of net revenue" `
  -type fact -channel "all" -tier 1

# Store a cross-agent handoff
.\scripts\memory_ops.ps1 -op store `
  -content "HANDOFF TO AVA: [what, where files are, deadline]" `
  -type event -project "<project>" -tier 2
```

**Ava (bash/zsh):**
```bash
./scripts/memory_ops.sh store "DECISION: [what] RATIONALE: [why]" decision "nbcu-po-automation" "all" 2
./scripts/memory_ops.sh search "NBCU current state and blockers" "nbcu-po-automation"
```

---

## Cross-Agent Handoff Protocol

When handing off work to the other agent:

```
1. Harry → stores handoff record to agent='shared', meta.owner='ava', meta.status='active'
2. Ava → at session start, queries: search "pending handoffs tasks for Ava"
3. Ava picks up record, executes, then updates meta.status='closed'
```

No Telegram message needed if both agents follow session start routine.

---

## Namespacing Rules

```
agent='harry'   → Harry-only context (Windows ops, runbooks, technical notes)
agent='ava'     → Ava-only context (design briefs, creative direction)
agent='shared'  → Business facts, projects, decisions, SOPs — readable by both
```

**When in doubt: use 'shared'.** Err on the side of sharing.

---

## Compression (automatic — no action needed)

- Tier 3 records auto-expire after 30 days
- Weekly Sunday 02:00 cron summarizes Tier 3 groups into Tier 2 insights
- You only need to manually supersede outdated facts:
  ```powershell
  # Mark old record superseded (Harry)
  # Get the old record ID first via search, then:
  Invoke-RestMethod -Uri "$SUPABASE_URL/rest/v1/agent_memory?id=eq.<old-id>" `
    -Method PATCH -Body '{"meta":{"status":"superseded"}}' ...
  ```

---

*End of SOP. Full architecture and implementation details: gdrive:Clawdbot Shared Folder/Brain/MEMORY_ARCHITECTURE.md*
