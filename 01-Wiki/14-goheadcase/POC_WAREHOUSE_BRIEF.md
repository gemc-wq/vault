# POC Brief — GoHeadCase Warehouse (US-first) + Gaming Store (subdomain)

## Summary
We will launch a proof-of-concept **headless Shopify** implementation that demonstrates the core commercial mechanic:
- **Design-first shopping**
- **Cross-sell from one design → multiple products**
- **80/20 device coverage** to keep SKU/variant counts manageable

This POC is **not theme-specific** — it is a new GoHeadCase “warehouse-style” storefront.

In parallel, we will run a **Gaming Store** as a separate storefront experience at:
- `gaming.goheadcase.com`

Both storefronts share **one Shopify backend** for catalog + ops.

---

## Goals (what this POC must prove)
1. We can run a modern DTC storefront with **Shopify backend** and a custom frontend (headless).
2. Customers can easily buy **multiple products** from a single design (bundling/cross-sell).
3. We can operate with an 80/20 product+device set (avoid BigCommerce-scale SKU explosion).
4. We can split navigation cleanly without losing revenue: **Warehouse** vs **Gaming Store**.

---

## Storefronts

### A) GoHeadCase Warehouse (main)
**Audience:** broad DTC buyers (style/value vs Casetify/Burga).

**POC product scope**
- Phone cases: **Snap + Wallet**
- Tablet cases: iPad (limited)
- Desk mats: mouse mats + desk mats

**Primary browse mode:** Shop by Design

**Navigation (POC)**
- Shop Designs
- Phone Cases
- Tablet Cases
- Desk Mats
- Best Sellers / New
- Search
- CTA: **Gaming Store** → `gaming.goheadcase.com`

### B) Gaming Store (separate frontend)
**Subdomain:** `gaming.goheadcase.com`

**Audience:** gaming-centric buyers; different intent + merchandising.

**POC scope:** minimal at first (can be “coming soon” with email capture), then expand.

**Navigation (example)**
- Console skins
- Controller
- Handheld
- Desk mats
- Bundles

---

## Core UX Requirement: “Design Hub” (cross-sell engine)

### Design-first flow
1) User enters via **Design Grid** (or search)
2) Clicks a design → lands on **Design Hub page**
3) On Design Hub, user selects:
   - Product type (phone case / wallet / iPad / mat)
   - Device (from supported list)
4) User adds one or more items to cart via:
   - quick add
   - “Complete the set” module (bundle-style)

### Non-negotiables
- Each design should be purchasable across multiple product types.
- Strong “matching set” UI to drive multi-item carts.

---

## 80/20 Rules (collection-aware, ops-safe)

### Device coverage
- US-first; UK second.
- Define a **Core Device Set v1** that captures ~80% of volume/profit signals.
- Cap initial device list to keep variants manageable.

### Cross-sell coverage
- For included phone devices: offer **Snap + Wallet** whenever available.

### Variant caps (guardrail)
- POC should target a hard ceiling on variants (exact number set after first device list + design count).

---

## Shopify Backend Structure (Option A)

### Single Shopify store
- One admin for products, collections, pricing, inventory, ops.

### Two storefront experiences
Visibility controlled via:
- Collections / tags / metafields:
  - `storefront: warehouse | gaming | both`
  - `product_type: phone_case | wallet_case | ipad_case | desk_mat | ...`

---

## Analytics & KPIs (POC)
- Track:
  - add-to-cart rate on Design Hub
  - average items per order
  - attach rate (second item added)
  - conversion rate by device category
  - top landing pages → design hub conversion

Inputs available:
- GA4 exports (traffic, landing pages, countries, device category)
- Supabase views (sales by device/product type)

---

## Build Plan (high level)
1) Finalize Core Device Set v1 (US-first)
2) Select initial design set (20–50) + map to products
3) Implement storefront:
   - Home
   - Design Grid
   - Design Hub
   - Product pages (as needed)
   - Cart
   - Checkout (Shopify hosted)
4) Implement Gaming storefront skeleton at `gaming.goheadcase.com`

---

## Open questions
1) Do we include **laptop skins** in the warehouse POC (for the Ohio State cross-sell example) or as Phase 1.5?
2) Which first “hero design set” should we use for POC: Sports-heavy, Entertainment-heavy, or a balanced mix?
