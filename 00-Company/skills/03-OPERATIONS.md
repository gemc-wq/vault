# Skill: Operations & Fulfillment
**Weight: 20% | Heartbeat: 1x per cycle | Agents: Jay Mark (builder), Ava (strategy)**

---

## Why #3
Operations is the delivery engine. Once Creative produces designs and Sales lists them, Operations prints, ships, and fulfills. The print pipeline consumes 5-7 PH staff daily — the #1 operational drag. Automating this frees human capacity for creative work.

## Scope
- Print file pipeline (IREN/DRECO → TIFF/EPS)
- Fulfillment portal and order management
- Shipping carrier management (Evri, Royal Mail, FedEx, USPS)
- EU 3PL fulfillment partner setup
- Inventory management and stock-out monitoring
- Zero 2.0 replacement system

## Active Projects
| Project | Status | Priority | Owner |
|---------|--------|----------|-------|
| Fulfillment Portal | 🟡 Jay Mark taking over | P1 | Jay Mark |
| EU 3PL setup | 🔴 Needs partner identified | P1 | Cem |
| Print pipeline automation | 🟡 Lane 2 of IREN/DRECO | P1 | — |
| Zero 2.0 | 🟡 Jay Mark scoping | P2 | Jay Mark |
| Inventory ordering app | 🟡 Harry built schema | P2 | Harry |
| Shipping label automation | 🟡 Evri CSV MVP | P2 | Jay Mark |
| ecell.app | 🟡 Jay Mark building | P2 | Jay Mark |

## Key Metrics
- Order → doorstep time (target: <48hr)
- Print file generation time per SKU
- EU delivery time (currently 7-10 days, target 3-4 days)
- Stock-out frequency by fulfillment location (FL, UK, PH)
- Manual steps remaining in print pipeline

## Context
- 3 fulfillment hubs: FL (US), UK (UK/EU/ROW), PH (Japan)
- Carriers: Evri CSV upload (no API), Royal Mail click-and-drop, USPS/FedEx via Stamps.com
- 13 canvas templates per design in DRECO pipeline
- LSE database must have lineups pre-inserted before DRECO runs
- Jay Mark new Supabase tables: licenses, license_designs, launch_tasks, etc.
- Procurement split: 7-day velocity by buyer country
