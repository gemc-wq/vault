# GoHeadCase Warehouse — Headless Shopify POC Spec (v0.1)

## Shopify backend
- Store: `head-case-1499.myshopify.com`

## Storefronts (same backend)
1) **Warehouse (main)** — broad audience
2) **Gaming Store** — `gaming.goheadcase.com` (separate storefront experience)

Visibility control: `storefront_visibility = warehouse | gaming | both`

Bridge products: **Desk mats / mouse mats** = `both`

## POC product scope (Warehouse)
- Phone cases: **Snap + Wallet**
- Tablet cases (limited)
- Desk mats + mouse mats

Phase 1.5: laptop products + AirPods holders

## Core UX requirement: Design-first cross-sell
### Primary browse mode
- **Shop Designs** grid (default)

### Design Hub page (must-have)
Design page that lets a customer buy multiple products from one design:
- Choose product type (phone case / wallet / tablet / mat)
- Choose device (for cases)
- Add to cart
- “Complete the set” module: add matching mat / case type in 1 click

## Navigation (Warehouse)
- Shop Designs (default)
- Phone Cases
- Tablet Cases
- Desk Mats
- Best Sellers / New
- Search
- CTA: Gaming Store → `gaming.goheadcase.com`

## Navigation (Gaming)
- Console
- Controller
- Handheld
- Desk Mats
- Bundles
- Search

## Page templates
1) Home (Warehouse)
2) Design Grid (filters)
3) Design Hub (cross-sell engine)
4) Collection page (product-type view)
5) Cart (bundle-friendly)
6) Static: shipping/returns/contact

## Analytics (POC KPIs)
- Add-to-cart rate on Design Hub
- Items per order
- Attach rate (2nd item)
- Conversion rate by device category

## Open items
- Decide POC domain for Warehouse: `warehouse.goheadcase.com` (recommended) vs replacing `goheadcase.com`
- Decide initial design set size (recommend 20–50)
