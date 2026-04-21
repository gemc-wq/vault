# Advisory Report: Inventory Ordering App — REVISED
**Prepared by:** Hermes (Operations Librarian)
**Date:** 2026-04-13
**Reference:** PROJECT.md v2.0 + Cem Clarifications

---

## Executive Summary

After Cem's clarifications, the Inventory Ordering App is **cleared for build** with resolved ambiguities. Key conflicts addressed:

| Issue | Resolution |
|-------|------------|
| Data source conflict | BigQuery mirrors AWS MySQL via Datastream (not stale) |
| Schema collision | Use Harry's existing Supabase schema |
| PULSE integration | Simple SKU parsing on orders tables |
| Architecture | Cloud Run apps accessed via ecell.app portal |
| Ownership | Jay Mark NOT assigned — need builder identified |

---

## Clarified Architecture

### Data Flow (CORRECTED)
```
AWS MySQL (Source)
      ↓
   Datastream
      ↓
BigQuery zero_dataset (Mirror)
      ↓
  Sync Job (2hr)
      ↓
Supabase (App Database)
```

**Status:** This pipeline is live. No MySQL migration needed — Datastream handles replication.

### App Architecture (CLARIFIED)
```
ecell.app (Portal/Dashboard)
      │
      ├─── /inventory → Inventory Ordering App (Cloud Run)
      ├─── /fulfillment → Fulfillment Portal (Cloud Run)
      ├─── /listings → Listings Tracker (Cloud Run)
      └─── /licenses → License Manager (Cloud Run)
```

**Status:** ecell.app is the unified entry point. Apps run on Cloud Run.

---

## Operational Context — Distribution Logic

### Site Responsibilities

| Site | Primary Role | Products | Volume |
|------|--------------|----------|--------|
| **FL (Florida)** | US printing hub | HTPCR, HC, HB401, H89**, HDMWH | ~50% of US |
| **UK** | UK + ROW orders | All products for UK/ROW | UK volume |
| **PH (Philippines)** | Overflow + FBA + Saturday | HLBWH (US), overflow UK/FL, ALL FBA, ALL Saturday | ~25% total |
| **CN (China)** | Sourcing & distribution | Distributes blanks to FL/UK/PH based on usage | N/A |

### Country Routing Rules (Fixed)

| Customer Location | Fulfillment Site | Notes |
|-------------------|------------------|-------|
| US | FL (primary) | HTPCR, HC, HB401, H89**, HDMWH |
| US | PH (overflow/HLBWH) | HLBWH products |
| UK | UK (primary) | All products |
| ROW | UK (primary) | All products |
| UK/ROW overflow | PH | Monday overload |
| FBA (all markets) | PH | All FBA printed in PH |
| Saturday orders (all) | PH | Weekend production |

### Velocity Calculation

**Total Sales Velocity = Sum of all sites' daily velocity**

This drives reorder levels to avoid stock-out. China distributes stock proportionally based on:
- Each site's historical usage
- Fixed country routing rules
- Product type mapping per site

---

## PO Creation Enhancements

### Shipping Plan Attachment
When PO created, system also generates:
- **Shipping plan** (destination site allocation)
- **Order sheet export** (CSV + PDF)
- **Supplier-optimized format** for Ben (China office)

### Rounding Rules
- Quantities round to **base 10** or **base 100**
- Example: 47 units → 50 (base 10) or 100 (base 100)
- Rounding direction based on velocity trend:
  - **Rising velocity** → round UP
  - **Stable/falling velocity** → round DOWN

---

## Revised Recommendations

### RESOLVED — No Action Needed
- ✅ Data source: BigQuery via Datastream (confirmed live)
- ✅ Schema: Use Harry's existing Supabase tables
- ✅ Architecture: Cloud Run + ecell.app portal
- ✅ PULSE: Simple SKU parsing, no complex integration

### NEW — Action Required

| Priority | Action | Owner |
|----------|--------|-------|
| **CRITICAL** | Assign builder (Jay Mark NOT on this project) | Cem |
| HIGH | Define rounding logic rules (base 10 vs 100 threshold) | Harry |
| HIGH | Document site allocation formula for China distribution | Harry |
| MEDIUM | Build PO → shipping plan → CSV/PDF export | Builder |
| MEDIUM | Add rounding logic to quantity calculations | Builder |

---

## Updated SWOT

### Strengths (Revised)
- ✅ Data pipeline verified (Datastream → BigQuery → Supabase)
- ✅ Schema exists (Harry's tables ready)
- ✅ Architecture clear (Cloud Run + ecell.app)
- ✅ Distribution logic documented (FL/UK/PH split)
- ✅ Rounding rules defined (base 10/100)

### Weaknesses (Revised)
- 🔴 No builder assigned
- 🟡 Rounding threshold undefined (when to use base 10 vs base 100?)
- 🟡 Site allocation formula not codified

### Opportunities (Same)
- 50%+ efficiency gain automating China workflows
- Stock-out prevention via velocity-based reordering
- PO + shipping plan + export in one flow

### Threats (Reduced)
- Schema conflict: RESOLVED
- Data source conflict: RESOLVED
- IREN2 dependency: Still a risk for print files (separate project)

---

## Questions for Cem (UPDATED)

1. **Who is building this?** Need to assign developer.
2. **Rounding threshold:** At what quantity level do we switch from base 10 to base 100?
   - Example: <100 units → round to 10s, >100 units → round to 100s?
3. **Site allocation formula:** Should China auto-calculate based on 30-day velocity per site, or manual review?

---

## Summary

The Inventory Ordering App is well-designed and ready for build. The clarifications resolve all critical gaps. Main blocker is **assigning a builder** since Jay Mark is not on this project.

The distribution logic (FL handles US printing, PH handles overflow/FBA/Saturday, UK handles UK/ROW) should be codified into the shipping plan generator.

---

*Revised by Hermes | 2026-04-13*
*Previous version archived as: ADVISORY_INVENTORY_ORDERING_APP.md*
