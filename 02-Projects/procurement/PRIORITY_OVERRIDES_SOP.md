# Priority Overrides — Standard Operating Procedure

> **Owner:** Cem | **Date:** 2026-04-15
> **Status:** DRAFT — awaiting review
> **Audience:** Cem, Managers, Ops team
> **Prerequisite:** Priority Overrides feature deployed (Phase 4)

---

## 1. What Are Priority Overrides?

Priority overrides let you tell the reorder engine: "this item is more (or less) urgent than its product group suggests."

Normally, the system orders enough stock for **30 days** (standard items) or **45 days** (best sellers). A priority override multiplies that cover:

| Multiplier | Standard Item | Best Seller | When to Use |
|-----------|---------------|-------------|-------------|
| **0.5x** | 15 days | 23 days | Slow mover, reducing stock |
| **1.0x** | 30 days | 45 days | Normal (no override needed) |
| **1.5x** | 45 days | 68 days | Important item, extra buffer |
| **2.0x** | 60 days | 90 days | High priority — retailer commitment, Prime promise at risk |
| **3.0x** | 90 days | 135 days | Critical — seasonal stockpile, cannot stock out |

---

## 2. When to Set an Override

### Set HIGH (1.5x–2.0x) when:
- A retailer order is due and you need guaranteed stock
- An item's velocity is spiking but best-seller status hasn't caught up yet
- Amazon listing is on a Prime/fast template and stock is getting thin
- Supplier lead time is temporarily longer than usual

### Set CRITICAL (2.5x–3.0x) when:
- Item cannot stock out under any circumstances (contractual obligation)
- Seasonal peak approaching (Christmas, back-to-school)
- Supplier is unreliable — need extra safety stock

### Set LOW (0.5x–0.9x) when:
- Item is being discontinued — run down stock
- Known slow period ahead — reduce cover to free up cash
- Product quality issue — hold off on large orders

### Don't set an override when:
- The existing group-level multiplier is sufficient
- The item has no sales velocity (engine already skips these)
- You want to stop ordering entirely (use the reorder queue "Skip" action instead)

---

## 3. How to Set an Override (Manual)

### From the Dashboard

1. Go to **Inventory** page
2. Find the item (search or filter by product group)
3. Click **Set Priority** button on the item row
4. In the modal:
   - **Multiplier:** Drag slider or type value (0.5–3.0)
   - **Reason:** Required — explain WHY
   - **Severity:** Select CRITICAL / HIGH / MEDIUM / LOW
   - **Expires:** Set expiry date (default: 7 days). Leave blank for permanent
5. Click **Save**

### Editing an Existing Override

1. Go to **Priority Overrides** page
2. Find the override (filter by item code, source, or severity)
3. Click **Edit** on the row
4. Update fields
5. Click **Save**

### Removing an Override

1. Go to **Priority Overrides** page
2. Find the override
3. Click **Deactivate**
4. Item reverts to product-group multiplier on next reorder calculation

---

## 4. How Overrides Affect Reorder Calculations

The reorder engine runs daily (07:00 UTC cron) and on-demand.

**Lookup order:**
1. Check `priority_overrides` for active, non-expired override
2. If YES: use highest multiplier across all sources for this item
3. If NO: use `product_group_config.priority_multiplier`
4. If no group config: use default 1.0x

**Multiple sources:** If manual (1.5x) and Amazon compliance (2.0x) both exist, engine uses **2.0x** (highest wins).

**Expiry:** Auto-ignored after `expires_at`. No cleanup needed.

---

## 5. External Overrides (Amazon Compliance)

The Amazon unified-score system can write overrides via API. These appear with `source = amazon_compliance`.

| Override Reason | What Happened |
|-----------------|---------------|
| Prime promise at risk | Item on fast template but primary warehouse stock is low |
| Restricted prefix critical | Item uses PH-restricted prefix (HB6, HB7, HDMWH). No PH overflow possible |

These are set and cleared automatically. They show up in the dashboard for visibility.

---

## 6. Monitoring

### Daily Check
- Review active overrides for surprises
- Check overrides expiring today
- Verify reorder queue badges match expectations

### Weekly Review
- Filter overrides expiring within 7 days
- Renew if still needed, let expire if not
- Check permanent overrides — should any have an expiry?

---

## 7. Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Override not affecting reorder qty | Expired or deactivated | Check `expires_at` and `is_active` |
| Item ordering at default despite override | Override multiplier ≤ group config | Check `product_group_config` value |
| Multiple overrides for same item | Different sources | Normal — highest wins. Deactivate one if unwanted |
| Multiplier rejected | Value outside 0.5–3.0 | Adjust to within range |

---

## 8. Quick Reference

```
SET OVERRIDE:    Inventory page → Set Priority → fill form → Save
EDIT OVERRIDE:   Priority Overrides page → Edit → update → Save
REMOVE OVERRIDE: Priority Overrides page → Deactivate
VIEW ALL:        Priority Overrides page (filter by active/source/severity)
EFFECT:          Next reorder calc uses the override multiplier
EXPIRY:          Auto-ignored after expires_at — no cleanup needed
AUDIT:           All changes logged in audit_log table
```

---

*See [[PRIORITY_OVERRIDES_SCOPE]] for project boundaries and [[PRIORITY_OVERRIDES_PRD]] for technical specification.*