# Vault Critical Fixes — Plan of Record
**Created:** 2026-04-19 | **Author:** Claude (via Cem session) | **Status:** APPROVED by Cem — executing
**Owner:** Athena (orchestration) + Cem (approvals)

---

## Decisions Locked (2026-04-19)

Cem answered the open questions. Locked decisions:

1. **Telegram digest timing:** Separate message (not tacked onto the 8:00 AM EOD automation). Rationale: compile summary and EOD business brief have different cognitive loads and different response actions; merging them dilutes both.
2. **Archive policy:** Keep `02-Projects/zz-archive/` in the vault forever. No auto-purge. Storage is cheap, retrievability matters.
3. **Compiler model:** Sonnet 4.6 as default for nightly compile. Haiku 4.5 reserved for lightweight tasks (alert triage, correction detection). Opus 4.7 for monthly deep compile only.
4. **Correction detection scope:** BOTH Telegram AND Claude Code session transcripts. Important caveat from Cem: *"I normally ask Claude Code to update SOP and PRD."* This changes the architecture — see new breakdown addition below.

---

## TL;DR

The multi-agent architecture is sound. Execution has three specific breakdowns burning ~80% of the productivity this stack should deliver. This doc is the fix plan. Each fix is scoped, owned, and has a clear "done" definition.

Target: all four fixes live within 14 days. System running clean for 2 weeks after that. Then add Lola.

---

## Context Snapshot

**What's built and working:**
- 4 live agents (Athena, Ava, Hermes, Harry) with defined roles and skill ownership
- Three-layer knowledge system (Raw → Wiki → Compiled)
- Collaboration framework with handoff protocol (v2.0 as of today)
- Agent-cron architecture pattern replacing N8N
- Centralised TASK_SHEET and AGENT_ROSTER
- AI Autonomous Impact Analysis ranking 8 leverage points
- 261 project docs across 61 folders

**Symptoms Cem flagged (April 19 high-level notes):**
- Splintered projects with incomplete information
- Project briefs inaccurate → output below standard
- Agent chats on Telegram time-consuming due to no mistake logging
- Source-of-truth docs drifting
- Cem is the bottleneck — projects only complete when he drives end-to-end in Claude Code

**Root cause diagnosis:** three breakdowns below.

---

## Breakdown #1 — The Compiler Is Down

### What's Broken
- `BLOCKERS.md` reports: *"⚠️ Gemma 4 unavailable — manual review needed"*
- Nightly compile has been failing. Compiled outputs are stale.
- Harry's last log is 8 days old (Apr 3), confirming the pipeline has been broken ≥5 days.
- Agents start sessions, read stale TASK_SHEET and PROJECT_BOARD, act on outdated truth, write contradictory logs. Cycle compounds daily.

### Fix (REVISED 2026-04-19 EVENING)
**Primary: Claude Code Routines** running nightly on Anthropic's cloud, triggered by schedule, against the vault git repo. See `COMPILER_ROUTINES_SETUP.md`.

**Fallback: launchd on ZEUS** running `claude -p` headless against Obsidian MCP. See `CLAUDE_CODE_COMPILER_SPEC.md`.

Both paths share the same authoritative prompt at `00-Company/skills/compiler/PROMPT.md`. The Routine dispatcher is at `00-Company/skills/compiler/ROUTINE_PROMPT.md`.

**Model locked: Sonnet 4.6** for nightly and weekly. Opus 4.7 for monthly.

**Why Routines over launchd as primary:**
- No local infra required; ZEUS can be asleep
- PR review IS the pending-validation workflow (maps onto §11 of AGENT_COLLABORATION.md natively)
- GitHub mobile notifications = Cem gets morning nudge automatically
- Git history = full audit trail of every compile, revertible forever
- Prerequisite: vault pushed to private GitHub repo (~15 min one-time setup)

### Done When
- [ ] Vault is a git repo pushed to private GitHub
- [ ] `ROUTINE_PROMPT.md` and `PROMPT.md` committed to repo
- [ ] Routine created at claude.ai/code/routines, configured with Sonnet 4.6
- [ ] First manual run produces clean PR
- [ ] Schedule trigger active (02:00 ET)
- [ ] First three consecutive nightly compiles complete successfully
- [ ] `BLOCKERS.md` no longer reports "Gemma 4 unavailable"

### Owner
Cem sets up git repo + creates routine. Athena owns `PROMPT.md` iteration.

---

## Breakdown #2 — Project Sprawl and No Intake Control

### What's Broken
- 61 folders in `02-Projects/` with severe duplication:
  - **Pulse:** `pulse-dashboard/` + `pulse-dashboard-v2/` + `pulse-unified/` + `command-center/` + `dashboard-product-entry/` (5 folders, probably 1 project)
  - **Walmart:** `walmart/` + `walmart-lister/` + `walmart-listing-audit/` + `walmart-review-strategy/`
  - **Finance:** `finance/` + `finance-ops/` + `Projects/Finance/` (one outside the main tree)
  - **Prune:** `prune/` + `prune-app/`
  - **Listings:** `listing-forge/` + `listings-db/` + `listings-intelligence/` + `weekly-listing-audit/`
  - **Fulfillment:** `fulfillment-portal/` + `fulfillment-dashboard/`
- Agents create new folders when Cem chats about work without checking for existing siblings
- No `_INDEX.md` for projects, so agents can't efficiently check "does this exist?"
- Project briefs incomplete because they don't inherit context from sibling folders
- Vault health report flags: *"181 filenames appear in multiple locations"*

### Fix
**Two-part fix:**

**Part A — One-time merge sprint.** See `PROJECT_MERGE_MAP_2026-04-19.md` for the proposed canonical-project list and the `current-folder → canonical-folder` mapping. Cem reviews and approves, Athena executes the merges in one batch. Archive folders go to `02-Projects/zz-archive/`. **Archive kept forever per Cem decision #2.**

**Part B — Project Intake Rule.** Codified in `AGENT_COLLABORATION.md` v2.0 §10. Only Athena creates new project folders. Any new folder requires overlap search + Cem approval + canonical naming + registration in `_INDEX.md`. Nightly compiler lints for violations.

### Done When
- [ ] `PROJECT_MERGE_MAP_2026-04-19.md` reviewed and approved by Cem
- [ ] Merge executed — projects consolidated to ≤30 canonical folders
- [ ] `02-Projects/_INDEX.md` created with all canonical projects, owner, status, one-line purpose
- [ ] `02-Projects/zz-archive/` populated with superseded folders (retained indefinitely)
- [ ] Athena's SOUL.md / TOOLS.md updated to enforce §10 intake rule
- [ ] First week with zero new folders created outside intake rule

### Owner
Cem approves merge map. Athena executes. Compiler enforces ongoing.

---

## Breakdown #3 — No Human Validation on Source-of-Truth

### What's Broken
- INDEX.md shows auto-promoted wiki pages on April 17, 18, 19 — pages land directly in `01-Wiki/` with no human sign-off
- Agents read these as canonical truth on session start
- Cem's own note confirms: *"Human must validate all sop docs to ensure accuracy"* — the gap is explicit
- Contradictions accumulate silently
- No mistake-logging feedback loop: when Cem corrects an agent in Telegram, the correction isn't captured back into the source docs

### Fix (REVISED 2026-04-19 EVENING)
**If using Routines (primary path):** PR review IS the pending validation workflow. Compiler writes to `claude/vault-compile-YYYY-MM-DD` branch, opens PR, Cem reviews diff on mobile, merge = canonical. No separate `_pending/` folder needed.

**If using launchd (fallback path):** Compiler writes to `01-Wiki/_pending/YYYY-MM-DD/`. Cem reviews via a separate Telegram message (per decision #1) in the morning.

**Part B — Correction Logging.** NEW: scope expanded per decision #4. See `CLAUDE_CODE_SESSION_CAPTURE.md` for the mechanism. Claude Code transcripts are captured into the vault hourly, become first-class agent memory, and the nightly compiler extracts corrections from them alongside Telegram-originated corrections.

**Part C — Retroactive cleanup.** First compiler run (either path) handles recent auto-promoted pages (Apr 17, 18, 19). In Routines mode, it proposes validation via PR comments. In launchd mode, it moves them into `_pending/`.

### Done When
- [ ] PR workflow (Routines) or `_pending/` workflow (launchd) operational
- [ ] Separate morning Telegram message for compile digest (per decision #1)
- [ ] `corrections.md` template added to each agent's memory folder
- [ ] 7 days of consistent review flow (Cem processing PRs or pending pages)
- [ ] Stale `_pending/` pages (>7 days) or open PRs (>48h) flagged in VAULT_HEALTH

### Owner
Athena owns the pending/PR workflow. Cem commits to the daily review (target: 5 min/morning).

---

## Breakdown #4 — Mistake Logging (SCOPE EXPANDED per decision #4)

### What's Broken
*Cem's own words:* "Agentic chat on telegram is time consuming when explaining errors and repeated mistakes because of no mistake logging."

*Additional context from decision #4:* "I normally ask Claude Code to update SOP and PRD."

Every correction Cem makes is lost the moment the session ends. This applies to:
- Telegram chats with agents
- **Claude Code sessions where Cem instructs updates to SOPs/PRDs** (new scope)

The same mistakes repeat across sessions because nothing writes them back to the source. And the SOP/PRD updates Cem makes via Claude Code don't flow back to other agents' knowledge.

### Fix
Three components:

**Component 1 — Telegram correction detection.** Athena's heartbeat skill watches for Cem's correction patterns in Telegram ("no", "wrong", "that's not how it works", "I already told you") and appends to the relevant agent's `corrections.md`.

**Component 2 — Claude Code session capture (NEW).** A lightweight hourly cron on ZEUS copies recent Claude Code session transcripts into `03-Agents/Cem-Code/sessions/YYYY-MM-DD/`. Obsidian Git plugin auto-commits. The nightly compiler treats these as agent memory logs and:
- Extracts corrections (same classifier as Telegram)
- Extracts SOP/PRD update instructions
- Distinguishes Cem-authored changes (which are already "approved") from agent-proposed changes (which need approval)
- Propagates Cem's SOP/PRD updates across other agents' knowledge via the wiki

See `CLAUDE_CODE_SESSION_CAPTURE.md` for the spec.

**Component 3 — Critical rule for the compiler: "Cem-via-Claude-Code = Cem-authored."** When the compiler detects a wiki/SOP/PRD file modified by Claude Code in a session where Cem was the prompter, treat the change as pre-approved. Do not route it through pending/PR approval. Log it in WEEKLY_DIGEST but don't block it.

### Done When
- [ ] Session capture cron installed and running hourly
- [ ] First week produces populated `03-Agents/Cem-Code/sessions/` folder
- [ ] Telegram correction detection running in Athena's heartbeat
- [ ] First week produces populated `corrections.md` per agent
- [ ] Compiler distinguishes Cem-authored vs agent-proposed changes correctly
- [ ] Repeat-mistake count decreases week over week (tracked in WEEKLY_DIGEST)

### Owner
Athena builds Telegram detection. Cem installs session-capture cron (trivial bash). Compiler handles correction promotion and authorship discrimination.

---

## Execution Sequence (14 Days) — REVISED

### Week 1 — Foundation
| Day | Task | Owner |
|-----|------|-------|
| Day 1 (today) | All docs written: critical fixes, merge map, compiler spec, Routines setup, PROMPT.md, dispatcher, collaboration v2.0, session capture | Claude (done) |
| Day 1 | Cem answers 4 open questions | Cem (done) |
| Day 2 | Cem git-inits vault, pushes to GitHub, installs Obsidian Git plugin | Cem |
| Day 2 | Cem reviews & approves `PROJECT_MERGE_MAP_2026-04-19.md` | Cem |
| Day 3 | Cem creates Routine at claude.ai/code/routines. Runs first compile manually. | Cem |
| Day 3 | Athena executes project merge per approved map | Athena |
| Day 4 | First automated nightly compile. Cem reviews PR in morning. | Cem + Routine |
| Day 4 | Cem installs session-capture cron on ZEUS | Cem |
| Day 5-7 | Iterate on compiler prompt based on PR quality. Telegram correction detection deployed. | Athena + Cem |

### Week 2 — Stabilisation
| Day | Task | Owner |
|-----|------|-------|
| Day 8-10 | Agents update SOUL.md with v2.0 rules. Session-capture producing first week of data. | Athena |
| Day 11-12 | Retroactive wiki cleanup for Apr 17-19 auto-promotions. | Compiler |
| Day 13 | First WEEKLY_DIGEST with success metrics. | Compiler |
| Day 14 | Go/no-go decision on adding Lola. | Cem |

---

## Success Metrics

Measured in `00-Company/compiled/WEEKLY_DIGEST.md`:

| Metric | Baseline (today) | Target (Day 14) |
|--------|------------------|-----------------|
| Projects Cem drove end-to-end | Most | <30% |
| Projects completed by agents autonomously | ~0 | >=3/week |
| `02-Projects/` folder count | 61 | ≤30 |
| Auto-promoted wiki pages without approval | ~7 (recent) | 0 |
| Pending approval backlog | N/A | <10 pages |
| Agent contradictions in logs | Unmeasured | Baseline established + trending down |
| Cem time spent explaining repeated mistakes | High | Tracked via corrections.md |
| Compiler run success rate | 0% (broken) | >95% |
| Claude Code sessions captured | 0 | All sessions since capture installed |

---

## What Is NOT in Scope

Deliberately excluded from this 14-day fix so we stay focused:

- **Adding Lola** — revisit Day 14 once the above is stable
- **Migrating remaining N8N workflows** — continue per AGENT_CRON_ARCHITECTURE plan, no change
- **Building new agents (Echo, Iris)** — no new agents until the 4 existing run clean
- **Product work** (One Piece, ListingForge, Fulfillment Portal) — continues in parallel, owned by existing agents
- **Image generation / listing automation** (top impact items) — this is the *enabler* for those. Fix the plumbing first.

---

## Risk & Mitigation

| Risk | Mitigation |
|------|------------|
| Routines hits 15/day limit | Metered overage available; nightly + weekly + monthly = ~1.2/day avg, plenty of headroom |
| Vault git repo too large after push | Gitignore `zero-codebase/` and `ppc-autoresearch/` (42K+ legacy files) — noted in setup doc |
| Cem skips daily PR review → pending pile grows | GitHub mobile push notifications; stale PRs >48h flagged in VAULT_HEALTH |
| Merge sprint breaks something (broken links, lost content) | Archive (don't delete) superseded folders. Git commit before merge. |
| Agents ignore v2.0 rules | Bootstrap prompt update in each SOUL.md; compiler lints for violations |
| Session capture misses sessions | Obsidian Git plugin auto-commits; if capture cron fails, Athena daily check flags it |
| Compiler mistakes Cem-via-Claude-Code edits for agent edits (and routes through pending) | Authorship rule in PROMPT.md §2.4 + frontmatter `last_updated_by`; session capture provides context |

---

## Remaining Open Questions (from COMPILER_ROUTINES_SETUP.md)

These emerged after Cem's original 4 answers. Answer when ready:

1. **GitHub account for the vault repo.** Personal account, Ecell org account, or new dedicated account?
2. **Repo access.** Just Cem, or also Jay Mark / other humans on the team?
3. **Gitignore decision on `zero-codebase/` and `ppc-autoresearch/`.** Recommendation: exclude. They're 42K+ legacy files of non-vault reference code.
4. **Timezone for schedule trigger.** Verify in the Routines UI which timezone it displays, then set to 02:00 ET equivalent.
5. **First-run timing.** Manually trigger during the day so Cem can watch the PR open? Strongly recommend yes.

---

## Changelog
- 2026-04-19 (evening) — Breakdown #4 scope expanded per decision #4; Routines becomes primary compile path; model locked to Sonnet 4.6; archive policy set to indefinite retention.
- 2026-04-19 (morning) — Created. Based on full vault read: INDEX, AGENT_ROSTER, AGENT_COLLABORATION, TASK_SHEET, BLOCKERS, VAULT_HEALTH, AGENT_CRON_ARCHITECTURE, AI_AUTONOMOUS_IMPACT_ANALYSIS, project tree scan.