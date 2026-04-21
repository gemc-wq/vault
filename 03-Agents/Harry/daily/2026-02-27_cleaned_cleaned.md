# 2026-02-27

## Decisions
- **Shared Brain (Cem):** Implement a shared "Brain" on Google Shared Drive (via rclone) for Harry and Ava to ensure project state persists across restarts.
- **Agent Coordination:** Use a dedicated Telegram group for Harry and Ava to coordinate directly, bypassing Cem as a router.
    - **Documentation:** Create a central "root" document containing rclone remotes, active projects, sync instructions, and agent re-orientation constraints.

## Deliverables
- **NBCU PO Automation:** Generated `nbcu_fedex_only_3pos_0p5lb_11x7x1.csv` from PDFs 263, 264, and 265.
  - **Path:** `gdrive:Clawdbot Shared Folder/Brain/Projects/nbcu-po-automation/nbcu_fedex_only_3pos_0p5lb_11x7x1.csv`

## Blockers
- **Resolved:** Ava gateway outage fixed by correcting `channels.telegram.groupPolicy` (valid values: `open`, `disabled`, or `allowlist`).
- **Ongoing:** Sales Dashboard tile in `business-dashboard` still points to old GitHub Pages URL; requires update to internal route `/apps/sales-dashboard` and Cloud Run redeployment.

## Knowledge
- **rclone / Shared Drive Paths:**
  - Remote: `gdrive:`
  - Canonical Root: `gdrive:Clawdbot Shared Folder/`
  - Projects Root: `gdrive:Clawdbot Shared Folder/Brain/Projects/`
  - Local Windows Mirror: `C:\Users\gemc\clawd\gdrive_shared\`
- **macOS Configuration:** Hidden `.openclaw` folder is accessible via Finder (`Cmd+Shift+G`) at `/Users/clawdbot