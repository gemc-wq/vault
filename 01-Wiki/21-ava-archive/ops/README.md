# Ops: Backups + Logging (OpenClaw stack)

This folder contains lightweight, auditable scripts to back up:
- Brain (Google Drive via rclone)
- Local workspaces/repos (git mirrors + file snapshots)
- Optional: Supabase schemas/dumps (requires DB creds)

## Philosophy
- Prefer simple, deterministic backups over "smart" automations.
- Backups must be restorable with one command.
- Keep secrets out of repos. Use env vars and local config.

## Components

### 1) Brain mirror backup (Drive → local snapshot)
- `backups/brain_backup.sh`

### 2) Git repo mirror backups
- `backups/git_mirror_backup.sh`

### 3) OpenClaw config snapshot
- `backups/openclaw_config_backup.sh`

### 4) Optional Supabase backups
- `backups/supabase_schema_backup.sh` (placeholder; needs connection strings)

## Scheduling
Recommended: run nightly via cron (macOS launchd) or via OpenClaw cron once stable.

## Restore
Each script prints restore instructions and writes a manifest file under `backups/_manifests/`.
