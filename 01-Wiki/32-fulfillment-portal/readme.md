# 32 — Fulfillment Portal

> Cloud-based fulfillment layer replacing Zero's dispatch workflow, IREN print files, and manual label generation.

## Status: 📋 APPROVED FOR BUILD

## Key Documents
- [[BUILD_SOP]] — Full build specification (15 sections)
- [[GAP_ANALYSIS]] — Harry's spec vs Ava's scope comparison (TBD)
- [[ROUTING_RULES]] — Extracted routing logic from Zero PHP (TBD — Jay Mark)

## Quick Links
- Harry's original spec: `gdrive:Brain/Projects/fulfillment-portal/SPEC.md`
- GPT-5.4 architecture research: `projects/fulfillment-portal/` (local)
- Zero infrastructure map: `wiki/23-drew-handover/ZERO_INFRASTRUCTURE_MAP.md`

## Architecture
```
AWS Aurora → Datastream → BigQuery → Supabase → FastAPI (Cloud Run) → Next.js (Vercel)
                                                    ↓
                                            Carrier APIs → Labels
                                                    ↓
                                            Writeback → Aurora → Marketplaces
```

## Build Phases
1. **Phase 1 (Weeks 1-4):** Order queue + Evri CSV + picking lists
2. **Phase 2 (Weeks 5-8):** Carrier APIs + tracking writeback + RBAC
3. **Phase 3 (Weeks 9-12):** Print file generation + Vision QC

## Team
| Person | Role |
|--------|------|
| Ava | Spec, rules engine, QA review |
| Harry | Architecture, Supabase, deployment |
| Jay Mark | Primary builder (FastAPI + carrier integrations) |
| Chad | IREN analysis, Aurora credentials |
| Cem | Carrier account setup, AWS access |

## Prerequisites (Cem)
- [ ] Royal Mail Business API account
- [ ] Stamps.com API credentials
- [ ] Evri corporate credentials
- [ ] Aurora RDS write credentials (from Chad)
- [ ] Amazon SP-API Shipping role
