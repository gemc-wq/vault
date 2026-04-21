# SOP: Inventory Tracking & Replenishment
*Version: DRAFT 0.1 | Created: 2026-02-11 | Status: IN DEVELOPMENT*

---

## Purpose
Standard operating procedure for tracking physical blank stock and triggering replenishment from China suppliers.

---

## What We Track

### Blank Products (NOT finished goods)
Inventory is tracked at the **Blank SKU** level: `Product Type + Device Model`

Example:
- `HTPCR-IPH16` = TPU Clear Case blanks for iPhone 16
- `HC-S24` = Hard Case blanks for Samsung S24

**We do NOT track finished designs** — designs are digital files applied at print time.

---

## Stock Locations

| Site | Stock Types | Notes |
|------|------------|-------|
| Philippines | Full range of UV-printed products | Largest stock holding |
| UK | UV-printed + skins (H89) + laser-cut | Some unique product types |
| US (Florida) | Skins (H89) + stickers | Limited range |

Not every blank is stocked at every site — pre-defined mapping exists.

---

## Current Process

### Stock In (Purchasing from China)
- [ ] Purchase order placed with China supplier
- [ ] Lead time: 15-30 days
- [ ] Goods received → booked into inventory system
- [ ] Currently on MySQL with self-calculation

### Stock Out (Order Fulfillment)
- [ ] Order fulfilled → decrement stock
- [ ] `UPDATE stock SET quantity = quantity - 1 WHERE type = 'HTPCR' AND device = 'IPH16'`
- [ ] Cron job monitors for zero-stock items

### Stock Monitoring
- Cron job checks inventory levels
- Flags items at zero stock
- Pre-defined rules determine which items print at which site
- Zero stock at local site → reroute to Philippines

---

## Replenishment Logic (Target)

### Velocity-Based Reordering
```
Safety Stock = Max Daily Use × Max Lead Time
Reorder Point = Average Daily Use × Average Lead Time + Safety Stock
```

**Example:**
- IPH16 cases sell 100/day average
- China lead time: 20 days average, 30 days max
- Safety stock: 100 × 30 = 3,000 units
- Reorder at: (100 × 20) + 3,000 = 5,000 units

### Alerts
- **Yellow:** Stock below reorder point → draft purchase order
- **Red:** Stock below safety stock → urgent reorder + reroute to Philippines
- **Black:** Zero stock → stop taking orders for that product/device combo

---

## Data Source
- **Current:** MySQL database (legacy, 15 years old)
- **Target:** Supabase (unified schema with event-based inventory)
- **Cem to share:** Current MySQL inventory database structure

---

## Automation Opportunities

| Process | Current | Target |
|---------|---------|--------|
| Stock monitoring | Cron + manual | Real-time dashboard |
| Reorder triggers | Manual | Velocity-based alerts |
| Purchase orders | Manual email | Auto-draft PO for approval |
| Stock-out rerouting | Manual trigger | Automated site failover |
| Daily production report | Manual | Auto-generated summary |

---

*This SOP needs: Current MySQL schema from Cem, China supplier lead time data, historical sales velocity data per product/device.*
