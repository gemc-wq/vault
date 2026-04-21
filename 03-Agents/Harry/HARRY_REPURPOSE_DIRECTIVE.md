# Harry Repurpose Directive — Finance Agent
*Date: 2026-04-07 | Directive: Cem | Executed by: Athena*

---

## Change Summary

Harry is repurposed from COO/Builder → **Finance Agent**.

### KEEPS (Finance scope)
| # | Project | Status |
|---|---------|--------|
| 1 | **Xero Finance App** (UK + US) | Scope complete, blocked on OAuth |
| 2 | **Inventory Ordering App** | Active build, 11 tables done |
| 3 | **Procurement System** | Gap analysis done, needs Cem approval |

### TRANSFERS TO JAY MARK
| # | Project | Reason |
|---|---------|--------|
| 4 | **Fulfillment Portal** | Jay Mark is the builder + tester. Harry's spec stands as-is. |
| 5 | **Zero 2.0** | Jay Mark has PHP knowledge. This was always his domain. |

### Harry's Updated Role Definition
```
Harry — Finance Agent (iMac, Sonnet 4.6)
Domain: Finance, Royalties, COGS, Procurement, Inventory
Blueprint V3: Stage 9 (Finance) + Stage 10 (Inventory/Procurement)

Deliverables:
1. Xero Finance App — AP intake, journal posting, revenue recording
2. Royalty tracking per license (accrual vs MG)
3. COGS per product type per office (currency-aware)
4. Procurement — PO generation, supplier invoicing, 3-way matching
5. Inventory alerts — traffic light per office, velocity-based reorder
6. Monthly royalty statements to licensors
```

### Harry's Updated INDEX.md (for Ava to push)
```markdown
# Harry — Finance Agent Project Index
*Last updated: 2026-04-07 by Athena (Cem directive)*

Harry runs on Claude Sonnet 4.6, iMac (cems-imac, Tailscale 100.91.149.92).
His domain: Finance, Royalties, COGS, Procurement, Inventory.
Blueprint V3: Stage 9 + Stage 10.

---

## Active Projects

### 1. Xero Finance App (UK + US)
**Status:** Scope complete, Xero OAuth pending
**Spec:** harry/projects/XERO_FINANCE_APP_SCOPE.md
- AP document intake → Xero bill posting
- Journal posting from operational reports
- Revenue recording (Amazon settlements, Shopify webhooks, Walmart)
- UK + US organisations (separate)
- **Blocked on:** Xero Client ID + Client Secret from Cem

### 2. Inventory Ordering App
**Status:** Active build
**Spec:** harry/projects/INVENTORY_ORDERING_APP.md
- Per-site pages: UK / PH / FL
- Top 50 items per region with traffic-light status (Red <14d, Amber <21d, Green 21d+)
- Weighted 7d/30d velocity model
- Stock-out alerts (multilingual: EN/Tagalog/Spanish)
- **DB schema:** 11 tables built
- **This week:** Deliver daily alert script per office

### 3. Procurement System
**Status:** PH gap analysis complete, awaiting Cem approval
**Spec:** harry/projects/PROCUREMENT_SYSTEM_SPEC.md
- 11 EOL items to remove (saves ¥1,000)
- HTPCR-IPH17PRO -163 qty fix
- Shipping split: 70% PH / 15% UK / 15% FL ($1,014 savings/PO)
- PO generation, supplier invoicing, 3-way matching
- **Blocked on:** Cem approval of split + EOL removal

### 4. Royalty Tracking (NEW)
**Status:** Starting — One Piece is pilot
- Per-sale royalty calculation (design_code → license → royalty_pct)
- Running accrual in Supabase
- Alert if pace below MG target
- Monthly royalty statement per licensor

---

## TRANSFERRED TO JAY MARK (Apr 7)
- Fulfillment Portal → Jay Mark builds + tests (Harry's spec stands)
- Zero 2.0 → Jay Mark owns (PHP knowledge transfer)
```

### Action Required — Ava
1. Update `vault/02-harry/INDEX.md` with the above
2. Update `vault/02-harry/SOUL.md` role definition
3. Update AGENTS.md to reflect Harry = Finance Agent
4. Sync changes back to GDrive
