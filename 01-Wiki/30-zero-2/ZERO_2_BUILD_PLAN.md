# Zero 2.0 — Build Plan (Assessed)
*Source: Cem's ZERO_2.0_BUILD_PLAN.md (Mar 18) + Ava's strategic assessment (Mar 20)*
*Added to wiki: 2026-03-20*

---

## Status: PLAN — Scope under review

## What It Is
Ground-up replacement for legacy Zero ERP. Agentic order flow + inventory/PO system with 5 AI agents (Orchestrator, Order, Inventory, Production, Fulfillment).

## Tech Stack
| Component | Technology |
|-----------|-----------|
| Backend | Python 3.12+, FastAPI |
| Database | PostgreSQL 16 |
| Task Queue | Celery + Redis |
| AI Engine | Claude API (Anthropic SDK) |
| Frontend | React + TypeScript |
| Deployment | Docker Compose |

## Three Parallel Systems (Future Vision)
1. **Zero 2.0** — Order flow, production, inventory/PO *(this project)*
2. **Content Creation** — Image generation pipeline
3. **Finance** — Xero integration

## Ava's Scope Recommendation (Mar 20)

### ✅ v1 Scope (Order Ingest + Fulfillment Sync)
| Module | What | Timeline |
|--------|------|----------|
| Order Ingest | Amazon SP-API + Shopify connectors → PostgreSQL | 4 weeks |
| Order Normalization | Unified schema, custom label parsing | Included |
| Fulfillment Sync | Tracking numbers → marketplace sync | 2 weeks |
| Parallel Run | Run alongside legacy Zero, compare | 2 weeks |

**Total: 8 weeks for 2 marketplaces end-to-end.**
Then add Walmart, eBay, Rakuten, BigCommerce (1-2 weeks each).

### ❌ Cut from v1
- Orchestrator Agent (premature coordination)
- React dashboard (use Supabase views + PULSE)
- Prometheus + Grafana (use basic logging)
- Kubernetes (Docker Compose is fine at our volume)
- Inventory/PO agents (Phase 2 after order flow proven)

### ⚠️ Flags
1. **10-week timeline for full ERP = unrealistic.** 200+ scripts with undocumented business rules.
2. **AI agents for order routing is over-engineered.** 95% deterministic rules. Save AI for anomaly detection.
3. **Builder not named.** Python/FastAPI project — who builds this?
4. **Amazon deadline is Mar 2027** — a year away. Time to do it right.
5. **Sage dependency buried** — picking lists query Sage via MSSQL. Needs Patrick's knowledge first.

### Key Principle
Deterministic rules for 95% of orders. AI escalation for the 5% edge cases. Don't call Claude API for every order.

## Against the North Star
- **Coverage:** No direct impact
- **Speed:** Yes — faster fulfillment, reduced manual steps
- **Intelligence:** No direct impact
- **Risk reduction:** Yes — Patrick bus factor, SQL injection, MWS sunset

## Relation to Harry's Work
Harry is currently building:
- Fulfillment label printing system (Veeqo integration)
- Procurement system spec (completed Mar 20)
- These overlap with Zero 2.0's Fulfillment Agent and Inventory Agent

**Recommendation:** Harry's Veeqo/label work IS the fulfillment piece of Zero 2.0. Don't duplicate.

## Key Legacy Files to Port
| File | Business Rules |
|------|---------------|
| `barcode/common_functions.php` | Duplicate detection, normalized inserts |
| `barcode/generate_purchase_order_automated_phAMG1_wh.php` | Auto-PO rules |
| `barcode/ShopifyImportOrders.php` | Canonical order import pattern |
| `barcode/sage_generate_picking_list_allocated.php` | Picking list + warehouse routing |
| `barcode/despatch_handler.php` | Despatch Express integration |
| `barcode/headcasecustomlabel.class.php` | Custom label parsing |
| `config/barcode.php` | Database routing logic |

## Prerequisites
- PostgreSQL 16 instance
- Redis instance
- Aurora RDS read credentials (or snapshot)
- All marketplace API credentials (most already in TOOLS.md)
- Patrick's review of active scripts vs dead code

## Related
- [[wiki/30-zero-2/ZERO_SYSTEM_SUMMARY|Zero System Summary]]
- [[wiki/30-zero-2/STAFF_AUTOMATION_MAP|Staff Automation Map]]
- [[projects/procurement/PROCUREMENT_SYSTEM_SPEC|Procurement System Spec]]
