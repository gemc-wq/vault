# Skill: Spec Drift Detector
**Owner:** Sentinel | **Schedule:** Weekly Monday 4AM ET
**Priority:** P2 — drift compounds silently over weeks
**Model:** Gemma 4 for comparison, Haiku for judgment

---

## Purpose

Compare active project specs (Zero 2.0, ListingForge, Control Centre, etc.) against what's actually been built. Detect when implementation diverges from spec — either the code drifted or the spec is outdated.

---

## Active Specs to Watch

| Spec | Location | Repo / Implementation |
|------|----------|----------------------|
| Zero 2.0 | Vault/01-Projects/Zero-2.0/SPEC.md | ecell-app, fulfillment portal |
| ListingForge | Vault/01-Projects/ListingForge/ | TBD (blocked) |
| Control Centre | Vault/01-Projects/Control-Centre/ | ecell-app/control-centre (future) |
| PULSE V2 | Vault/01-Projects/PULSE/ | pulse-v2 repo |
| PIE | Vault/01-Projects/PIE/ | product-intelligence-engine repo |

---

## Check Logic

```
Weekly Monday 4AM ET:
  1. For each active spec:
     a. Read spec file (latest version from Vault)
     b. Read recent git commits in the corresponding repo (last 7 days)
     c. Compare: do commits align with spec priorities?
     d. Check for:
        - Features built that aren't in spec (scope creep)
        - Spec requirements with no matching code changes (stalled)
        - Contradictions between spec and implementation
  
  2. For Zero 2.0 specifically:
     a. Compare Supabase schema against spec's data model
     b. Check API endpoints match spec's API design
     c. Flag any endpoints that exist in code but not in spec
  
  3. Generate drift report:
     a. List all drifts found
     b. Classify: SCOPE_CREEP, STALLED, CONTRADICTION, SPEC_OUTDATED
     c. Recommend: update spec or realign code
  
  4. Save to data/sentinel/spec-drift-{date}.md
  5. Include in weekly Sentinel digest to Athena
```

---

## Drift Categories

| Category | Signal | Action |
|----------|--------|--------|
| **SCOPE_CREEP** | Code changes not in spec | Either add to spec or revert |
| **STALLED** | Spec requirement, no code progress in 2+ weeks | Flag as blocker |
| **CONTRADICTION** | Code does opposite of spec | Urgent — which is correct? |
| **SPEC_OUTDATED** | Spec references deprecated patterns/tables | Update spec |
| **ORPHANED** | Spec exists but no repo/implementation at all | Decide: build or archive |

---

## Git Analysis

```bash
# Recent commits in repo
git -C /Users/openclaw/projects/{repo} log --oneline --since="7 days ago"

# Files changed
git -C /Users/openclaw/projects/{repo} diff --stat HEAD~10..HEAD

# Look for schema/migration changes
git -C /Users/openclaw/projects/{repo} log --oneline --all -- "**/migrations/**" "**/schema*"
```

---

## Alert Format

```
--- SENTINEL REPORT ---
Severity: INFO
Skill: spec-drift
What: Weekly spec drift report — {date}

{project_name}:
  Status: {ALIGNED / DRIFTED / STALLED}
  Drifts found: {count}
  Details:
    - {drift_type}: {description}
  Recommendation: {action}

---
```

---

## Changelog
- 2026-04-13 — Created. Drift categories, git analysis, spec comparison approach.
