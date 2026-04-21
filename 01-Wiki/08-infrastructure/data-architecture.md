# Data Architecture
*Auto-created by vault compiler on 2026-04-13 | Consolidated*

- Memory Hierarchy: Vault is established as Layer 3 (the canonical source of truth for continuity).
- Automated sync to Vault occurs nightly at 11 PM.
- BigQuery (`instant-contact-479316-i4`) is now the primary data source for the Fulfillment Orchestrator, replacing the need for direct MySQL access.

See also: [[memory-hierarchy]], [[cloud-run-services]], [[supabase-project-details]]
