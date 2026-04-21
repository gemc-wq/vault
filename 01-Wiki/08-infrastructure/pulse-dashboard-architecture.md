# pulse-dashboard-architecture
*Auto-created by vault compiler on 2026-04-18*

- The `/api/leaderboard` endpoint uses Supabase RPC instead of BigQuery to maintain architectural consistency with `/api/designs` and `/api/champions`. (Replaces previous BigQuery implementation).
