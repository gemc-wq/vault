# Inventory Ordering App — Project Wiki
**Version:** 1.0  
**Date:** 2026-04-01  
**Owner:** Harry (COO, Ecell Global)  
**Status:** Active build

---

## 1. Overview

Inventory Ordering App is the operational reorder and stock-cover tool for blank inventory across Ecell sites. It is the next evolution of the Procurement Control Tower and is being shaped for direct use by the operations team.

Primary sites in scope:
- **UK**
- **PH**
- **FL**

Primary goal:
- show the top 50 selling **device / product type** inventory items for each site
- estimate stock-out risk using local demand
- make reorder urgency obvious with traffic-light status
- show whether stock is already on order

---

## 2. Confirmed Product Requirements

### Site pages
The app needs a dedicated inventory page for each location:
- UK
- PH
- FL

Each location page should focus on the **top 50 selling items** for that region.

### Item grain
Inventory should be tracked and displayed at the **device / product type** level using the operational item code standard.

### Traffic-light logic
Cem confirmed the status thresholds as:
- **Red** = less than **14 days** of stock
- **Amber** = less than **21 days** of stock
- **Green** = **21+ days** of stock

### On-order visibility
Each item row must show if any quantity is already **on order**.

### Stock-out estimate
Days of stock / stock-out estimate must be calculated using that **region’s own expected sales velocity**.

Velocity model:
- use **last 7 days** sales
- use **last 30 days** sales
- weight **last 7 days more heavily** than last 30 days
- flag items where the recent daily velocity is materially different from the 30-day baseline

This is intended to catch sudden spikes or collapses in demand.

---

## 3. Recommended Calculation Model

### Weighted daily velocity
Initial implementation target:
- `daily_velocity_7d = sales_last_7d / 7`
- `daily_velocity_30d = sales_last_30d / 30`
- `weighted_daily_velocity = (daily_velocity_7d * 0.7) + (daily_velocity_30d * 0.3)`

This reflects Cem’s instruction to weight the last 7 days more heavily.

### Days of stock
- `days_of_stock = free_stock / weighted_daily_velocity`
- if weighted velocity is zero, show `null` / no estimate

### Velocity anomaly flag
Flag an item when recent daily velocity is materially off baseline.

Suggested first-pass rule:
- if `daily_velocity_30d > 0`
- and `ABS(daily_velocity_7d - daily_velocity_30d) / daily_velocity_30d >= 0.35`
- then set `velocity_flag = true`

This threshold can be tuned after live review.

### Traffic-light evaluation
Use the weighted stock-cover result:
- **RED** if `days_of_stock < 14`
- **AMBER** if `days_of_stock < 21`
- **GREEN** otherwise

Optional future state:
- separate hard-out-of-stock badge when `free_stock <= 0`

---

## 4. UI / UX Direction

The frontend should be adjusted to follow the **Ecell app style guide in the wiki**.

Current direction to implement:
- cleaner app shell and navigation
- less prototype-style presentation
- site-specific pages/cards for UK / PH / FL
- clearer KPI hierarchy
- operational table design with stock cover, alert state, and on-order visibility emphasized
- consistent color usage for alert states
- readable executive / operations view first, detail second

If no separate design-style file exists yet in wiki, this project page acts as the current canonical product spec until the shared style guide is added or linked.

---

## 5. Data Model Requirements

Each inventory row should support at minimum:
- `item_code`
- `description`
- `warehouse`
- `product_group`
- `supplier`
- `free_stocks`
- `on_order`
- `sales_last_7d`
- `sales_last_30d`
- `daily_velocity_7d`
- `daily_velocity_30d`
- `weighted_daily_velocity`
- `days_of_stock`
- `velocity_flag`
- `alert_level`
- `snapshot_date`

---

## 6. Page Structure

### Dashboard
Should summarize:
- critical low-stock items by site
- on-order exposure
- top-risk items likely to stock out soon
- quick links into UK / PH / FL inventory pages

### Site Inventory Pages
Separate views for:
- `/inventory/uk`
- `/inventory/ph`
- `/inventory/fl`

Each page should show:
- top 50 selling items for that site
- item code + description
- free stock
- on-order qty
- 7-day sales
- 30-day sales
- weighted daily velocity
- stock-out estimate in days
- traffic-light status
- velocity anomaly flag

### Global Inventory View
Optional combined page for cross-site filtering and search.

---

## 7. Build Notes / Current State

Current app exists under:
- `tmp/procurement-system`

Existing pages include:
- dashboard
- inventory
- reorder queue
- purchase orders

Current inventory page needs to be upgraded to:
- match confirmed traffic-light thresholds
- add location-specific pages
- show top 50 selling items per site
- use weighted 7d / 30d regional velocity
- show velocity anomaly flag
- better align with wiki style expectations

---

## 8. Immediate Build Tasks

1. **Document project in memory and wiki** ✅
2. **Review current frontend against wiki style direction**
3. **Refactor dashboard styling**
4. **Create UK / PH / FL inventory pages**
5. **Implement top-50 ranking by regional sales**
6. **Update stock-cover calculations to weighted 7d / 30d model**
7. **Add velocity anomaly flag**
8. **Ensure on-order quantities are visible in all site tables**

---

## 9. Open Data / Engineering Notes

Items to confirm during implementation:
- exact source for PH live/test inventory in current app
- exact source for `on_order` per site
- whether ranking should use item quantity sold or order-line count
- whether top 50 should be based on 30-day sales, weighted sales, or another agreed ranking metric

Default implementation recommendation unless otherwise specified:
- top 50 ranking by **30-day units sold** per region
- stock cover by **weighted daily velocity**

---

## 10. Status

Cem confirmed this should be documented now into memory and a new wiki project.

This page is the canonical project reference for the current inventory ordering app scope as of 2026-04-01.
