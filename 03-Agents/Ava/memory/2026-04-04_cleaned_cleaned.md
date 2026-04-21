# 2026-04-04

**Decisions**
- **Architecture & Source of Truth**: Cem approved a 4-layer Vault model. The Wiki is now the canonical source; `ava-obsidian-vault/` and `ava-supplements/` are deprecated. GDrive is the source of truth for large files; Mac Studio files must be deleted after use.
- **Model & API Policy**: Use 26B MoE for Gemma 4 implementation (Cem correction). Use free models for all background work to manage costs. Anthropic calls are now API-billed (OAuth removed).
- **Memory Management**: Switched to local-only `embeddinggemma-300m` to prevent token burn.
- **Operational Blueprint**: V3 approved by Cem (10-stage process: License $\rightarrow$ Intelligence).

**Deliverables**
- **Documentation & SOPs**: Created `VAULT_OPERATING_SYSTEM.md`, `ZEUS_ARCHITECTURE.md`, `ATHENA_ONBOARDING_BRIEF.md`, and `SOP_CREATIVE_TO_REPLICATION_PROCESS.md`.
- **Development**: Completed Fulfillment Portal spec (`SPEC.md`) using BQ $\rightarrow$ Supabase $\rightarrow$ Next.js; completed Xero Finance App scope (11 tables).
- **Procurement**: PH order gap analysis completed; identified $1,014 savings per cycle via shipping split (70% PH / 15% UK / 15% FL).
- **Deployment**: Published Blueprint V3 to `wiki/` and `Brain/Strategic/`.

