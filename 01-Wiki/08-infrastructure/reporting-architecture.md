# reporting-architecture
*Auto-created by vault compiler on 2026-04-19*

The Weekly Listings Delta Reporting architecture uses BigQuery as the primary layer for raw data, history, and diffing. Supabase is used only as an optional downstream layer for serving tables.
