# Zero Legacy System — Summary
*Source: ZERO_SYSTEM_SUMMARY.md (Cem, Mar 20) + Drew Handover files + Patrick IT Team Profile*
*Added to wiki: 2026-03-20*

---

## What Zero Is
Decade-old PHP/MySQL ERP for Head Case Designs. Handles order management, inventory, production, licensing/royalties, and marketplace integrations. Organic growth, no documentation, no version control.

## Infrastructure

### Servers (EC2, us-east-1)
| Name | IP | Type | Role |
|------|-----|------|------|
| Zero1 | 34.196.137.61 | t2.large | Original Zero — MWS only (legacy) |
| Zero2 | 3.81.155.102 | t3.medium | Updated Zero — runs Amazon SP-API |
| Ecellglobal | 54.86.30.14 | t2.micro | Global/B2B site |
| Local | 192.168.20.57 | On-prem | XAMPP codebase |

### Databases
| Location | Host | MySQL | Size | Tables | Purpose |
|----------|------|-------|------|--------|---------|
| Aurora RDS | cluster...rds.amazonaws.com | 8.0.39 | 439 GB | 476 | **Orders/Sales — all marketplace data** |
| .160 (local) | 192.168.20.160 | 8.0.45 | 67 GB | 453 | **Product/Design data only** |
| .182 (local) | 192.168.20.182 | 5.7.33 | — | — | Idle/legacy |

**CRITICAL:** Aurora and .160 are independent masters with NO replication. 23-table divergence. BUT per team clarification: .160 = product data, Aurora = orders/sales. They serve different domains.

### Database Routing (barcode.php)
- Cron jobs (no SERVER_NAME) → Aurora RDS
- `bar_uk` / `bar_uk2014` / `sage_2013` → Aurora RDS
- `bar_au` → 192.168.20.173
- `bar_us` → 192.168.20.66
- Databases ONLY on .160: bigcommerce, dekr, marketing, rakuten, walmart (product data, NOT order imports)

### AWS Costs
- Current: ~$5,226/mo (314% increase recently)
- Forecast: ~$6,206/mo
- Main drivers: S3, EC2, RDS

## Technical Debt
1. No version control — 55+ dated backup copies of scripts
2. Legacy PHP — deprecated `mysql_*` functions (removed in PHP 7.0)
3. SQL injection vulnerabilities — raw `$_POST` values in queries
4. No replication — two independent masters
5. Patrick Gaña is sole knowledge holder for day-to-day ops
6. Dead code everywhere — many scripts/tables unused
7. Amazon MWS dependency (sunset) — SP-API on Zero2 but not fully migrated

## Amazon SP-API Migration
- **Deadline:** Orders API v0 removal — **3/27/2027**
- 3 files affected on Zero2 (3.81.155.102)
- All 6 deprecated v0 endpoints mapped to v2026-01-01
- ZeroCloud app credentials active until September 2026
- Zero1 uses MWS (even older) but Zero2 handles active imports

## Royalty Report System
- `t_royalty_information` — licensor records (rates, contracts, contacts)
- Key scripts: `royalty_report_manager.php`, `get_1d_sales*.php`
- **OUT OF SCOPE for Zero 2.0 v1** — Finance system handles this

## Key Personnel
- **Patrick Gaña** — Runs the entire order-to-label pipeline daily (see IT Team Profile)
- **Bobby (Iren)** — Documentation via email
- **Drew Ramos** — AWS account holder (departed, handover complete)

## Related
- [[wiki/30-zero-2/ZERO_2_BUILD_PLAN|Zero 2.0 Build Plan]]
- [[wiki/30-zero-2/STAFF_AUTOMATION_MAP|Staff Automation Map]]
- [[wiki/23-drew-handover/ZERO_INFRASTRUCTURE_MAP|Zero Infrastructure Map]]
- [[wiki/23-drew-handover/PATRICK_IT_TEAM_PROFILE|Patrick IT Team Profile]]
