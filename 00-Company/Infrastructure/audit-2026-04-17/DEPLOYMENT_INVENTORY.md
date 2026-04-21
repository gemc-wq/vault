# Deployment Inventory — Phase 1
*Generated: 2026-04-17 by Athena | Status: PARTIAL — GitHub + GCP sweep pending*

## 1. Vercel Projects (gemc99-boop / ecells-projects-3c3b03d7)

**Total: 26 projects**

### Production-domain apps
| Project | Domain | Last deploy | Notes |
|---|---|---|---|
| business-dashboard | **ecell.app** | 49d ago | Main ecell.app pointer |
| ecell-site | **ecellglobal.com** | 29d ago | Corporate site |

### Active / recent (< 14d)
| Project | URL | Last deploy |
|---|---|---|
| pulse-dashboard-v2 | pulse-dashboard-v2.vercel.app | 9h |
| ecell-inventory | ecell-inventory-ecells-projects-3c3b03d7.vercel.app | 6d |
| deploy2 | deploy2-ecells-projects-3c3b03d7.vercel.app | 6d |
| procurement-system | procurement-system-ecells-projects-3c3b03d7.vercel.app | 6d |
| vercel-deploy | vercel-deploy-ecells-projects-3c3b03d7.vercel.app | 6d |

### Dashboards (30-50d, likely stale)
| Project | URL | Last deploy |
|---|---|---|
| conversion-dashboard | conversion-dashboard-kohl.vercel.app | 33d |
| sales-dashboard-v2 | sales-dashboard-v2-nine.vercel.app | 38d |
| sales-dashboard | sales-dashboard-iota-six.vercel.app | 46d |
| pulse-dashboard | pulse-dashboard-inky.vercel.app | 38d |
| prune-app | prune-app-xi.vercel.app | 38d |
| blueprint-dashboard | **— NO URL** | 39d | **BROKEN** |
| command-center | command-center-one-puce.vercel.app | 43d |
| dashboard-product-entry | dashboard-product-entry.vercel.app | 46d |
| orbit-pm | orbit-pm.vercel.app | 46d |
| mission-control-v2 | mission-control-v2-three.vercel.app | 53d |

### Frontends / microsites
| Project | URL | Last deploy |
|---|---|---|
| goheadcase-frontend | goheadcase-frontend.vercel.app | 46d |
| sports-frontend | sports-frontend-three.vercel.app | 46d |
| anime-frontend | anime-frontend-lilac.vercel.app | 46d |
| ecell-website | ecell-website-blond.vercel.app | 53d | **possible duplicate of ecell-site** |
| storefront | storefront-phi-eosin.vercel.app | 53d |

### Misc / unclear
| Project | URL | Last deploy |
|---|---|---|
| app | app-zeta-sable.vercel.app | 41d | Generic name — needs identification |
| nba-deploy | nba-deploy.vercel.app | 53d |
| esale-api | esale-api.vercel.app | 53d |
| orbit-team-build | orbit-team-build.vercel.app | 53d |

### Duplicates / suspicious — likely retire candidates
- `sales-dashboard` vs `sales-dashboard-v2`
- `pulse-dashboard` vs `pulse-dashboard-v2`
- `ecell-site` vs `ecell-website`
- `deploy2`, `vercel-deploy` — looks like experimental scaffolds
- `blueprint-dashboard` — broken (no production URL)

---

## 2. Supabase Projects

| Project | Ref | Status | Region | Created |
|---|---|---|---|---|
| **gemc-wq's Project** | auzjmawughepxbtpwuhe | ACTIVE_HEALTHY | us-east-1 | 2026-02-08 |
| email-memory | lndbltopyytqrvrovwai | **INACTIVE (paused)** | us-east-1 | 2026-02-22 |

### Main project (auzjmawughepxbtpwuhe) — 80+ public tables

**Procurement / Inventory:** blank_inventory, inventory, internal_transfers, po_batches, po_order_lines, po_supplier_orders, purchase_orders, reorder_suggestions, stock_adjustments, supplier_currency_map, supplier_invoices, suppliers, warehouses, packaging_profiles

**Listings / Marketplace:** marketplace_listings, walmart_listings, listings_delta, listings_weekly_summary, best_sellers_daily

**Catalog:** designs, devices, lineups, products, product_types, product_group_config

**CFX (pricing):** cfx_brands, cfx_brand_code, cfx_channels, cfx_colors, cfx_currencies, cfx_designs, cfx_devices, cfx_ean_lookup, cfx_marketplace, cfx_prices, cfx_pricing_categories, cfx_product_colors, cfx_product_types, cfx_products, cfx_unit_brand, cfx_unit_display_category

**Orders / Fulfillment:** orders, shipments, shipment_lines, fulfillment_orders, fulfillment_rules

**Analytics / Ops:** amazon_conversion_data, audit_log, cc_decisions, cc_metrics, cc_projects, operational_events, sync_log, system_health, fx_rates_daily

**RAG / Brain:** brain_chunks, brain_documents

**Infra:** cron_run_lock, users

---

## 3. GCP Projects (20 visible under gemc@ecellglobal.com)

Full Cloud Run + BigQuery sweep in progress. Known projects of interest:
- **bionic-factor-487900-b2** — likely hosts production Cloud Run services
- **opsecellglobal** — ops infra
- **ecellglobal-email-oauth** — email OAuth backend
- **Ava** (gen-lang-client-0930523931) — agent project
- **title-tracker-485905**
- **unified-campaign-6dkbb**
- 14 additional (multiple `gen-lang-client-*` Gemini scratch projects + 7 `sys-*` untitled)

Most untitled `sys-*` projects likely dormant — to be confirmed.

---

## 4. Access Scorecard

| Layer | Status |
|---|---|
| Vercel (gemc99-boop / ecells-projects) | ✅ Live — 26 projects inventoried |
| Supabase management API | ✅ Live — 2 projects visible |
| gcloud (20 GCP projects) | ✅ Live — Cloud Run + BQ sweep in progress |
| GitHub (gemc99-boop + gemc-wq) | ❌ **BLOCKED — awaiting `gh auth login` or PAT** |
| Additional Vercel team (if gemc-wq separate) | ⚠️ Unknown — needs confirmation |

---

## 5. Immediate Red Flags
1. **`blueprint-dashboard`** has no production URL → broken, investigate or retire
2. **`deploy2`**, **`vercel-deploy`** — scaffolding names still live, almost certainly retire candidates
3. **Dashboard duplicates**: sales-dashboard (v1 + v2), pulse-dashboard (v1 + v2) — old versions likely redundant
4. **`ecell-site` vs `ecell-website`** — both exist, only one points to ecellglobal.com
5. **Supabase `email-memory`** INACTIVE — is it intentional pause or forgotten?
6. **`nuvspkgplkdqochokhhi`** — referenced in Harry's iMac memory but NOT visible under this Supabase account. Possible: different account, possibly gemc99-boop's separate Supabase org, or deleted.

---

## 6. Next Steps (Phase 2)

1. **Unblock GitHub** — Cem to run `gh auth login` for both accounts
2. **Cross-reference**: each Vercel project → linked git repo → Cloud Run service (if any)
3. **Env var extraction** per Vercel project: identify which Supabase / BigQuery each app reads
4. **App-to-table matrix**: build the dependency map
5. **Probe**: HTTP + auth health check on each URL — classify WORKING / BROKEN / ABANDONED
6. **PRD drafting**: priority order by revenue impact
