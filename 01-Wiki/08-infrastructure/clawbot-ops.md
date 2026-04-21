# clawbot-ops
*Auto-created by vault compiler on 2026-04-13*

- **Operational Rule:** Always use regular (non-admin) PowerShell as `gemc` for all operations. Running as Administrator causes file ownership conflicts and prevents the gateway from reading auth files (e.g., `device-auth.json`).
