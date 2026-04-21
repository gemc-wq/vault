# Git Hardening Reference
**Date:** 2026-04-20

## Hardened `.gitignore` baseline

```gitignore
# Obsidian
.obsidian/
!.obsidian/app.json
!.obsidian/appearance.json
!.obsidian/core-plugins.json
.trash/
.Trashes

# macOS / editor noise
.DS_Store
._*
*.tmp
*.swp
*~

# Build artefacts
node_modules/
dist/
build/
coverage/

# Secrets / auth material
.env
.env.*
*.env
**/secrets/
**/credentials*
**/*_token*
**/*_key*
*.pem
*.key
*.p12
*.mobileprovision

# Databases / raw exports / large machine artefacts
*.db
*.sqlite
*.sqlite3
*.sql
*.csv
*.tsv
*.xlsx
*.xls
*.parquet
*.pickle
*.pkl
*.gz
*.zip
*.tar
*.7z
*.jsonl

# Session / temp capture artefacts
03-Agents/*/sessions/*.tmp
03-Agents/Cem-Code/.capture-state

# Known heavy folders
02-Projects/zero-codebase/
02-Projects/ppc-autoresearch/
02-Projects/amazon-data-analytics/dashboard/
02-Projects/unified-listings/data/
**/exports/raw/
**/downloads/

# Logs
/var/log/
**/logs/
```

## Mandatory pre-push audit commands

```bash
cd /Users/openclaw/Vault

# 1. Find oversized files
find . -type f -size +25M

# 2. Review staged files
git diff --cached --name-only

# 3. Search tracked files for likely risky patterns
git ls-files | grep -Ei '(\.env|secret|token|oauth|\.db$|\.sqlite|\.csv$|\.tsv$|\.xlsx$|\.pem$|\.key$)' || true

# 4. Confirm ignores are actually active
git check-ignore -v 02-Projects/zero-codebase/README.md || true
git check-ignore -v 02-Projects/amazon-data-analytics/dashboard/listings.db || true

# 5. Optional but recommended secret scan
gitleaks detect --source . --verbose
```

## First-push checklist

- repo is private
- SSH auth works
- `.gitignore` installed before first broad `git add`
- no files >25MB are tracked
- no DB/export/session dump files are tracked
- no `.env` or secret-like file names are tracked
- secret scan is acceptable enough to proceed
- manual review completed before push

## Recommended pre-push hook direction
Use `gitleaks` or `git-secrets` to block pushes when likely secrets are detected.

Manual override should be rare and deliberate.
