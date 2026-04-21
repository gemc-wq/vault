# Sales Pipeline — Active Projects & Priorities
*Created: 2026-04-07 | Source: Cem directive | Status: ACTIVE*

---

## P0: Quick Wins (Revenue Impact)

### 1. Walmart Listings — Top Sellers Refresh
- **Status:** Stale listings for top sellers. Quickest win available.
- **Action:** Get all top sellers listed/refreshed on Walmart.
- **Blocker:** Walmart API item creation still failing. Codisto/Shopify Marketplace Connect path forward.
- **Owner:** TBD (ListingForge dependency)

### 2. OnBuy UK — Product Listings + API Monitoring
- **Status:** Jay Mark started listing process.
- **Action:** Complete listings, set up API monitoring for order flow.
- **Note:** OnBuy API available — need monitoring dashboard.
- **Owner:** Jay Mark (listings), Ava/Hermes (monitoring)

---

## P1: Medium-Term Expansion

### 3. Kaufland DE — German Marketplace
- **Status:** UNBLOCKED — Netherlands tax registration COMPLETE (confirmed Apr 7)
- **Blockers:**
  - ~~Netherlands tax number~~ ✅ DONE (Apr 7)
  - European OSS (One Stop Shop) number (still pending — check status)
- **Current fulfillment:** UK → Germany (cross-border, 7-10 business days, customs delays)
- **Target fulfillment:** EU 3PL partner (print-on-demand), 3-4 business days
- **Impact:** Overnight improvement from 7-10 days → 3-4 days for Amazon DE orders too
- **This is a BIG win** — faster delivery = better conversion = higher BSR on Amazon DE
- **Action items:**
  1. Track Netherlands tax number application status
  2. Track EU OSS registration status
  3. Identify EU 3PL fulfillment partner
  4. Once registered: onboard 3PL, redirect DE/EU orders, list on Kaufland

---

## P1: Conversion Optimization (US)

### 4. FBA Conversion App — High-Ticket Items
- **Concept:** Convert select high-value US items to FBA (Fulfilled by Amazon) for better conversion rates.
- **Why:** FBA items get Prime badge, higher search ranking, better Buy Box win rate.
- **Selection criteria:** Big-ticket items where FBA economics work (higher ASP absorbs FBA fees).
- **Status:** Needs scoping
- **Owner:** TBD

### 5. Amazon Prime Conversion — Shipping Data Analysis
- **Concept:** Identify products where customers ALREADY pay $10.99 for 2-day FedEx shipping → these are Prime conversion candidates.
- **Logic:**
  - Current: Product $19.99 + $6.99 standard shipping OR $10.99 2-day shipping
  - Customer paying $10.99 2-day = willing to pay $30.98 total
  - Prime conversion: $29.99 with free Prime shipping
  - These customers won't be put off by the higher sticker price — they're already paying it
- **Risk:** Higher price ($29.99 vs $19.99) may deter standard-shipping customers
- **Mitigation:** Only convert products with HIGH 2-day shipping uptake — data proves willingness to pay
- **Analysis needed:**
  1. Pull shipping method breakdown by SKU from order data (standard vs 2-day)
  2. Identify SKUs where >X% of customers choose 2-day
  3. Calculate break-even: FBA fees + higher price vs current margin + shipping revenue
  4. Pilot: Convert top 10-20 candidates, measure conversion rate change over 30 days
- **Data source:** BQ orders table (shipping method field), Amazon Business Reports
- **Owner:** Hermes (data pull), Ava (analysis), Cem (approval)

---

## Cross-Cutting: EU Fulfillment Upgrade

The Netherlands tax + EU OSS registration unlocks more than just Kaufland:
- **Amazon DE:** Faster delivery (7-10 → 3-4 days) improves conversion + BSR
- **Kaufland DE:** New marketplace access
- **Future EU marketplaces:** Foundation for any EU expansion
- **Track separately** as a strategic enabler, not just a Kaufland blocker

---

## Summary — Updated Project Tiers (Sales Pillar)

| Priority | Project | Status | Impact |
|----------|---------|--------|--------|
| P0 | Walmart top sellers refresh | Stale, needs listing | Quick revenue |
| P0 | OnBuy UK listings + monitoring | Jay Mark started | New marketplace |
| P1 | Kaufland DE | BLOCKED (tax numbers) | EU expansion |
| P1 | FBA Conversion (high-ticket) | Needs scoping | US conversion uplift |
| P1 | Amazon Prime analysis | Needs data pull | US conversion + Prime badge |
| ENABLER | Netherlands tax + EU OSS | Pending registration | Unlocks all EU |
