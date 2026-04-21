# Procurement System SOP — Placing Your First Order

**App URL:** https://procurement-system-one.vercel.app  
**Last Updated:** 2026-04-01  
**Owner:** Cem (Operations) | Support: Harry (COO)

---

## Quick Start (5-Minute Overview)

The Procurement Control Tower automates inventory replenishment across UK, Florida, and Philippines warehouses. It tells you what to order, when to order it, and from which supplier.

**The 4-Step Workflow:**
1. **Check Dashboard** → See what's critical (BLACK = out of stock, RED = <7 days)
2. **Generate Suggestions** → Run the reorder engine
3. **Approve Items** → Review and approve suggested quantities
4. **Create PO Batch** → System generates supplier POs automatically

---

## Step-by-Step: Placing an Order

### Step 1: Review Dashboard Alerts

1. Go to https://procurement-system-one.vercel.app
2. Review the 6 alert cards:
   - **🔴 Critical (No Stock)** — Order immediately
   - **🟠 Low Stock (<7 days)** — Order this week
   - **🟡 Warning (<14 days)** — Plan to order
   - **🟢 Healthy** — No action needed
   - **💀 Dead Stock** — Consider clearance
   - **✅ Active SKUs** — Total catalog health

3. Click any card to see the items in that category

---

### Step 2: Generate Reorder Suggestions

1. Click **"Reorder Queue"** in the navigation
2. Click **"⚡ Generate Reorder Suggestions"**
3. The system will:
   - Check current stock levels
   - Calculate daily demand velocity
   - Compare against reorder points
   - Suggest quantities for items below threshold

**What you see:**
| Column | Meaning |
|--------|---------|
| Item Code | SKU identifier |
| Warehouse | UK / FL / PH |
| Supplier | Who to order from |
| In Stock | Current quantity |
| Days Left | Stock coverage at current velocity |
| Reorder Pt | Minimum threshold |
| Suggest Qty | System-recommended order quantity |
| Unit Cost | From supplier price list |
| Est. Total | Suggest Qty × Unit Cost |

---

### Step 3: Approve or Reject Suggestions

For each suggested item:

**To Approve:**
- Click **"✓ Approve"** → Item turns green, added to PO batch queue

**To Reject:**
- Click **"✗ Reject"** → Item removed from queue

**To Modify:**
- Currently: Approve then manually adjust with supplier
- Future: Direct quantity editing (Phase 2)

**Tips:**
- Prioritize 🔴 Critical and 🟠 Low Stock items
- Check supplier currency (RMB/USD) — impacts payment timing
- Consider batching by supplier to minimize shipping costs

---

### Step 4: Create PO Batch

Once you've approved all items:

1. Click **"📦 Create PO Batch (X approved)"**
2. System automatically:
   - Groups items by supplier
   - Creates separate POs per supplier-warehouse pair
   - Assigns batch number
   - Sets status to "draft"

3. Go to **"Purchase Orders"** page to view your batch

**What you see:**
```
Batch #123
├── PO-1: XINTAI → UK (¥ currency)
│   └── 15 items · 2,400 units
├── PO-2: TOKO → FL ($ currency)
│   └── 8 items · 1,200 units
└── PO-3: JIZHAN → PH (¥ currency)
│   └── 5 items · 800 units
```

---

### Step 5: Send POs to Suppliers

**Current Process (Manual):**
1. Export PO details from the app
2. Email/fax to supplier with your standard PO template
3. Mark PO as "sent" in system (coming in Phase 3)

**Future Process (Phase 3):**
- Direct email integration
- Supplier portal access
- PDF generation

---

## Understanding the Data

### Alert Levels

| Alert | Days of Stock | Action Required |
|-------|---------------|-----------------|
| 🔴 BLACK | 0 (out of stock) | **Immediate order** — expedite if possible |
| 🟠 RED | < 7 days | **Order this week** — standard lead time |
| 🟡 YELLOW | 7–14 days | **Plan order** — include in next batch |
| 🟢 GREEN | > 14 days | No action — monitor |
| 💀 DEAD | No sales 90+ days | Review for clearance |

### Reorder Calculation

```
Suggested Qty = (Demand Velocity × Lead Time Days) + Safety Stock − Current Stock

Where:
- Demand Velocity = Units sold per day (30-day rolling average)
- Lead Time Days = Supplier-specific (default: 21 days China→UK/US)
- Safety Stock = 7 days coverage (configurable per item)
```

---

## Supplier Reference

| Supplier | Currency | Products | Lead Time |
|----------|----------|----------|-----------|
| XINTAI | RMB (¥) | HTPCR, HC blanks | 21 days |
| HUAQING | RMB (¥) | HB401 blanks | 21 days |
| TOKO | USD ($) | HB6CR, HB7BK, HDMWH | 21 days |
| JIZHAN | RMB (¥) | HLBWH phone/Kindle/iPad | 21 days |
| ECELLSZ | RMB (¥) | HDMWH small mats | 14 days |

---

## Current Limitations (Phase 1)

**What Works:**
- ✅ Dashboard alerts
- ✅ Reorder suggestions
- ✅ Approve/reject workflow
- ✅ PO batch creation
- ✅ Multi-supplier grouping

**What's Coming (Phase 2–3):**
- 🔄 PO split algorithm (velocity by region, PH capacity cap)
- 🔄 China receiving UI (replaces 192.168.20.57)
- 🔄 Direct PDF export
- 🔄 Email integration
- 🔄 Full COGS dashboard (needs shipping/packaging costs)

---

## Troubleshooting

**"No suggestions generated"**
→ All items above reorder point. Check BLACK/RED alerts instead.

**"Supplier shows as '—'"**
→ Missing supplier mapping. Contact Harry to update item_master.

**"Days Left shows '—'"**
→ No sales velocity data (new item or dead stock). Use manual judgment.

**"Currency looks wrong"**
→ Check supplier_currency_map table. Contact Harry to fix.

---

## Support

**Technical Issues:** Harry (COO) — via Telegram or Orbit PM  
**Data Questions:** Check BigQuery `production_tracker` and `elcell_co_uk_barcode` datasets  
**Feature Requests:** Add to Orbit PM under "Procurement System"

---

## First Order Checklist

Before placing your first order:

- [ ] Reviewed dashboard alerts
- [ ] Generated reorder suggestions
- [ ] Approved at least one item
- [ ] Created PO batch
- [ ] Verified supplier and currency
- [ ] Checked total order value
- [ ] Exported PO details
- [ ] Emailed supplier with PO

**You're ready to go!**

---

*Document Version: 1.0 (Phase 1)*  
*Next Review: After Phase 2 deployment*
