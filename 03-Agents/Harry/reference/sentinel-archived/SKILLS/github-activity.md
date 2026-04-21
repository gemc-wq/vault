# Skill: GitHub Activity Watcher
**Owner:** Sentinel | **Schedule:** Daily 5AM ET
**Priority:** P1 — unreviewed changes can break production
**Model:** Gemma 4 for scanning, Haiku for risk assessment

---

## Purpose

Monitor all Ecell repos for commits, force pushes, migration changes, config changes, and dependency updates. Flag anything that needs review or could impact running systems.

---

## Repos to Watch

| Repo | Path | Primary Dev | Risk Level |
|------|------|-------------|------------|
| ecell-app | /Users/openclaw/projects/ecell-app | Jay Mark + PH | HIGH — production |
| fba-planner | /Users/openclaw/projects/fba-planner | Cem/Athena | MEDIUM |
| pulse-v2 | /Users/openclaw/projects/pulse-v2 | Hermes | MEDIUM |
| product-intelligence-engine | /Users/openclaw/projects/product-intelligence-engine | Hermes | MEDIUM |
| sales-dashboard-v2-repo | /Users/openclaw/projects/sales-dashboard-v2-repo | Hermes | LOW |
| blueprint-dashboard | /Users/openclaw/projects/blueprint-dashboard | Ava | LOW |
| EVRI | /Users/openclaw/projects/EVRI | Jay Mark | MEDIUM |
| zeus-agent | /Users/openclaw/zeus-agent | Athena | HIGH — infrastructure |

---

## Check Logic

```
Daily 5AM ET:
  1. For each repo:
     a. git fetch --all (if remote exists)
     b. git log --oneline --since="24 hours ago" --all
     c. Classify each commit by risk level
  
  2. High-risk commit patterns (ALERT):
     - Force push detected (reflog shows rebase/reset)
     - Migration files added/modified (**/migrations/**)
     - Environment config changed (.env*, config.*, next.config.*)
     - Package lock changed (package-lock.json, yarn.lock, requirements.txt)
     - Authentication/auth files modified
     - Database schema files modified
     - CI/CD config changed (.github/workflows/*, vercel.json)
     - .gitignore modified (security implications)
  
  3. Medium-risk patterns (WARNING in digest):
     - New dependencies added
     - API route changes
     - Supabase client usage changes
  
  4. Info patterns (log only):
     - Regular feature commits
     - Documentation changes
     - Test additions
  
  5. Cross-reference with security-audit skill:
     - If .gitignore was modified → trigger security scan
     - If new .env file appears → alert immediately
  
  6. Save to data/sentinel/github-activity-{date}.json
```

---

## Force Push Detection

```bash
# Check reflog for force pushes (local repos)
git -C {repo_path} reflog --since="24 hours ago" | grep -E "reset|rebase"

# For remote tracking
git -C {repo_path} log --walk-reflogs --oneline origin/main | head -5
```

Force push on main/master → P0 ALERT. Force push on feature branch → WARNING.

---

## Dependency Change Detection

```bash
# Node projects
git -C {repo_path} diff HEAD~1..HEAD -- package.json | grep -E '^\+.*"[^"]+": "'

# Python projects  
git -C {repo_path} diff HEAD~1..HEAD -- requirements.txt pyproject.toml
```

New dependency → check if it's known/trusted. Flag unknown packages.

---

## PH Staff Activity Tracking

Jay Mark and PH team work on ecell-app and EVRI. Track:
- Commit frequency (are they active?)
- What areas they're working in
- Any commits outside their usual scope (unexpected)

This feeds into Athena's staff productivity view — not punitive, just visibility.

---

## Alert Format

```
--- SENTINEL ALERT ---
Severity: CRITICAL / WARNING / INFO
Skill: github-activity
What: {risk_type} in {repo} — {commit_count} commits in 24h
Detail: 
  {commit_hash} {commit_message} ({author})
  Files: {changed_files}
Impact: {what could break}
Action: Review changes. {specific_recommendation}
---
```

---

## Daily Digest Format (for Athena morning brief)

```
## GitHub Activity — {date}

| Repo | Commits | Authors | Risk Items |
|------|---------|---------|------------|
| ecell-app | 5 | Jay Mark, PH-Dev2 | 1 migration, 1 config change |
| zeus-agent | 2 | Athena | 0 |
| pulse-v2 | 0 | — | — |

### Flagged Items
1. [HIGH] ecell-app: Migration 0043_add_tracking.sql added
2. [MED] ecell-app: package-lock.json updated (3 new deps)
```

---

## Changelog
- 2026-04-13 — Created. Repo inventory, risk classification, force push detection, PH staff tracking.
