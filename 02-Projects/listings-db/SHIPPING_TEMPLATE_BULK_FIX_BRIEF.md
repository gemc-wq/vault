# Shipping Template Bulk Fix — Jay Mark Brief
**From:** Ava | **Date:** 2026-03-30 | **Priority:** URGENT

> **Update 2026-04-16 — workflow now lives in the web UI**
>
> The manual flat-file workflow described below is preserved as the **fallback path**, but the primary tool is now:
>
> **Web UI** at `localhost:3001/dashboard` (then `/listings` and `/revisions`)
> — see [[LISTINGS_PIPELINE_PRD]] §16 and [[LISTINGS_PIPELINE_SOP]] §5B.
>
> The dashboard surfaces:
> - **Real wrong-template counts** by Product Type / Device / Product×Device / Licence — pulled from the latest pipeline run
> - **In Stock filter** that re-ranks against live Supabase blank inventory (refreshed on demand from the Refresh Inventory button)
> - **Verified backlog** as of the 2026-04-16 US run: 1,888,789 wrong-template listings; 543,082 actionable when filtered to in-stock SKUs
>
> When the **Fix Listings** + **Revisions** pages are wired (next phase, owned by the listings-pipeline session), Jay Mark's flat-file generation will be one click from the dashboard. Until then, the fallback workflow below stands.

---

## ⚠️ Critical Rule Before Fixing (Cem directive 2026-03-30)
**Nationwide Prime (UK) = same-day dispatch commitment.**

Before assigning a UK listing to Nationwide Prime, you MUST confirm UK blank stock > 0 for that device. If a device has zero UK stock, putting it on Nationwide Prime is misleading — customers see fast delivery but we can't fulfill. In that case, Default Amazon Template (or suppressing the listing) is actually correct.

**Fix priority:**
1. 🔴 UK listings on Nationwide Prime with ZERO UK stock → remove from Prime template immediately
2. 🟡 UK listings on Default Template WITH UK stock → upgrade to Nationwide Prime
3. 🟢 US listings on Default Template → upgrade to Reduced Shipping Template (no inventory gate for US)

## The Problem
As of the Mar 28/26 listings snapshots, a significant number of listings are assigned to the wrong shipping template. This means customers see slower delivery estimates than they should, which directly hurts conversion.

| Region | Correct Template | Wrong Template | Count |
|--------|-----------------|----------------|-------|
| US | Reduced Shipping Template | Default Amazon Template | ~76,136 |
| US | Reduced Shipping Template | Nationwide Prime | ~937 |
| UK | Nationwide Prime | Default Amazon Template | ~45,308 |
| UK | Nationwide Prime | Reduced Shipping Template | ~546 |

**Total affected: ~122,000+ listings across US and UK.**

---

## Why This Matters
- **Nationwide Prime** (UK) = fast delivery badge shown to customers → higher conversion
- **Reduced Shipping Template** (US) = lower displayed shipping cost → higher conversion
- **Default Amazon Template** = slow/expensive shipping shown → customers choose competitor

Every listing on the wrong template is converting below its potential.

---

## Immediate Action Required

### Step 1: Confirm impact scope in Seller Central
1. Log into Amazon Seller Central US → Inventory → Manage All Inventory
2. Filter by Shipping Template = "Default Amazon Template"
3. Note how many SKUs appear
4. Repeat for Amazon Seller Central UK

### Step 2: Bulk fix via flat file (fastest method)
Amazon allows bulk shipping template changes via inventory file upload:

1. Download the current inventory loader flat file (Inventory → Add Products via Upload → Download spreadsheet)
2. Filter rows where `merchant_shipping_group` ≠ correct template
3. Set `merchant_shipping_group` to correct value for all affected rows
4. Upload the corrected file

**For US:** Set all "Default Amazon Template" listings → "Reduced Shipping Template"
**For UK:** Set all "Default Amazon Template" listings → "Nationwide Prime"

### Step 3: Verify after upload
Wait 24 hours, then spot-check 10 random ASINs in each marketplace to confirm template updated.

---

## Going Forward
From this week, a Wednesday automated audit will catch any new wrong-template listings within 14 days of being uploaded, before they accumulate. This bulk fix clears the existing backlog.

**Owner:** Jay Mark Catacutan (j.catacutan@ecellglobal.com)
**Deadline:** Before end of this week (Apr 4)
**Escalate to:** Ava if bulk upload fails or Seller Central blocks the change
