# GoHeadCase Shopify — Product Selection Matrix v1
## BigCommerce → Shopify Lite Store Rules

**Author:** Ava | **Date:** 2026-03-06
**Target:** ~200K SKUs from 1.89M BigCommerce catalogue
**Purpose:** Hard-coded rules for which products enter the GoHeadCase Shopify store
**Feeds:** DTC microsites + Target+ (30K items) + Walmart (95K items) + OnBuy UK

---

## 1. PRODUCT TYPE RULES (What we sell)

Based on Supabase sales data (Jan 2025 – Feb 2026, 304K orders):

| Code | Product Type | Orders | Revenue | % Rev | Include | Target+ | Walmart |
|------|-------------|--------|---------|-------|---------|---------|---------|
| HTPCR | TPU Snap Case (Clear) | 132K | £8.04M | 42% | ✅ YES | ✅ | ✅ |
| HLBWH | Leather Wallet Case | 60K | £7.28M | 38% | ✅ YES | ✅ | ✅ |
| HC | Hard Case | 53K | £2.23M | 12% | ✅ YES | ✅ | ✅ |
| H8939 | Console Skins (PS5 etc) | 24K | £609K | 3% | ✅ YES | ✅ | ✅ |
| HDMWH | Desk Mat | 7.8K | £183K | 1% | ✅ YES | ✅ | ✅ |
| HHYBK | Hybrid Case | 7.8K | £173K | 1% | ✅ YES | ✅ | ✅ |
| HB401 | MagSafe Case | 6.8K | £133K | 0.7% | ✅ YES | ✅ | ✅ |
| HA805 | AirPods Case | 2.2K | £51K | 0.3% | ✅ YES | ✅ | ✅ |
| HB6CR | Crossbody Case | 2.2K | £50K | 0.3% | ✅ YES | ✅ | ✅ |
| H8940 | Console Skins (Other) | 1.1K | £20K | 0.1% | ⚠️ Phase 2 | ✅ | ❌ |

**EXCLUDED product types:**
- `Z%` — Legacy items (discontinued)
- `H8%` except H8939 — Legacy PS5 skins (low stock)
- Any product type with <500 orders in trailing 12 months

**TOTAL: 9 product types in Phase 1**

---

## 2. DEVICE MODEL RULES (What devices we support)

Based on Supabase top sellers + current market relevance:

### Tier 1: Must-Have (captures ~80% of phone case revenue)

| Device | Code | Top Product Type Revenue | Priority |
|--------|------|------------------------|----------|
| iPhone 16 | IPH16 | £671K (HTPCR alone) | 🔴 |
| iPhone 15 | IPH15 | £801K (HTPCR alone) | 🔴 |
| iPhone 14 | IPH14 | £544K | 🔴 |
| iPhone 13 | IPH13 | £417K | 🔴 |
| iPhone 12 | IPH12 | £361K | 🔴 |
| iPhone SE 4 | IPHSE4 | £513K | 🔴 |
| iPhone 16 Pro Max | IPH16PMAX | £148K | 🔴 |
| iPhone 16 Pro | IPH16PRO | 🔴 |
| iPhone 15 Pro Max | IPH15PMAX | 🔴 |
| iPhone 15 Pro | IPH15PRO | 🔴 |
| iPhone 14 Pro Max | IPH14PMAX | 🔴 |
| iPhone 14 Pro | IPH14PRO | 🔴 |
| iPhone 14 Plus | IPH14PLUS | 🟠 |
| iPhone 15 Plus | IPH15PLUS | 🟠 |
| iPhone 16 Plus | IPH16PLUS | 🟠 |
| iPhone 13 Pro | IPH13PRO | 🟠 |
| iPhone 13 Pro Max | IPH13PMAX | 🟠 |

### Tier 2: Samsung + Mid-Range (captures next ~10%)

| Device | Code | Notes |
|--------|------|-------|
| Samsung Galaxy A16 5G | A165G | £98K revenue — #6 overall device! |
| Samsung Galaxy S24 Ultra | S928U | Top Samsung flagship |
| Samsung Galaxy S25 Ultra | S938B | Current gen |
| Samsung Galaxy A55 5G | A555G | Top mid-range |
| Samsung Galaxy A15 | A155G | Budget segment |

### Tier 3: Additional (remaining ~10%)

| Device | Code | Notes |
|--------|------|-------|
| Google Pixel 9 | GPX9 | Growing Android |
| Google Pixel 9 Pro | GPX9PRO | |
| Samsung Galaxy S24 | S921B | |
| Samsung Galaxy S25 | S931B | |

### Console Devices (for H8939 skins)

| Device | Code |
|--------|------|
| PS5 Controller | DS5CT |
| PS5 Console | PS5 |
| Nintendo Switch | NSW |
| Xbox Series X | XSX |

**TOTAL: ~26 phone/tablet models + 4 console devices = 30 devices**

---

## 3. BRAND / LICENSE RULES (What designs we sell)

### Target+ RESTRICTIONS (hard-coded exclusions):
❌ **NO US Sports on Target+:**
- NFL (code: NFL*)
- NBA (code: NBA*)
- NHL (code: NHL*)
- NCAA/Collegiate (code: COLL*, NCAA*)
- MLS (code: MLS*)

✅ **US Sports OK on Walmart + DTC microsites**

### Brand Tiers by Revenue (from Phase 0 Micro Catalogue + sales data):

**Tier A — Top 20 brands (include ALL designs):**

| Brand | Code | Category | Revenue Rank | Target+ | Walmart |
|-------|------|----------|-------------|---------|---------|
| Liverpool FC | LFC | Sports | #1 | ✅ | ✅ |
| Arsenal FC | AFC | Sports | #2 | ✅ | ✅ |
| Man City FC | MCFC | Sports | #3 | ✅ | ✅ |
| Newcastle | NUFC | Sports | #4 | ✅ | ✅ |
| Tottenham | THFC | Sports | #5 | ✅ | ✅ |
| Harry Potter | HPOT | Entertainment | #6 | ✅ | ✅ |
| Chelsea FC | CFC | Sports | #7 | ✅ | ✅ |
| Peanuts | PNUT | Entertainment | #8 | ✅ | ✅ |
| Aston Villa | AVLA | Sports | #9 | ✅ | ✅ |
| West Ham | WHAM | Sports | #10 | ✅ | ✅ |
| Rangers FC | RFC | Sports | #11 | ✅ | ✅ |
| WWE | WWE | Entertainment | #12 | ✅ | ✅ |
| NFL | NFL | Sports | #13 | ❌ Target | ✅ Walmart |
| Scotland | SCOT | Sports | #14 | ✅ | ✅ |
| Batman/DC | BAT* | Entertainment | #15 | ✅ | ✅ |
| Iron Maiden | IRON | Entertainment | #16 | ✅ | ✅ |
| Dragon Ball | DRGB | Anime | #17 | ✅ | ✅ |
| Rick & Morty | RICK | Entertainment | #18 | ✅ | ✅ |
| Naruto | NARU | Anime | #19 | ✅ | ✅ |
| Hatsune Miku | HMIK | Anime | #20 | ✅ | ✅ |

**Tier B — Next 30 brands (include top 10 designs each):**
- All remaining football clubs with >£5K revenue
- NBA teams (top 10) — ❌ Target, ✅ Walmart + DTC
- Remaining DC Comics IPs
- Jujutsu Kaisen, My Hero Academia, One Piece
- Pac-Man, Atari, classic gaming
- All remaining music licenses

**Tier C — Long tail (include top 5 designs each):**
- All remaining active licensed brands with sales in trailing 12 months
- Non-licensed/art brands with >1K annual sales

**Tier D — EXCLUDE:**
- Brands with zero sales in trailing 12 months
- Discontinued licenses
- One-off/custom designs with no reorder potential

---

## 4. SKU CALCULATION

```
Tier A brands: 20 brands × ~50 designs avg × 30 devices × 5 product types = 150,000 SKUs
Tier B brands: 30 brands × 10 designs × 30 devices × 3 product types = 27,000 SKUs
Tier C brands: ~100 brands × 5 designs × 20 devices × 2 product types = 20,000 SKUs
Console skins: 50 brands × 20 designs × 4 devices = 4,000 SKUs
Desk mats: 50 brands × 10 designs × 1 size = 500 SKUs

ESTIMATED TOTAL: ~201,500 SKUs
```

---

## 5. MARKETPLACE OVERLAP MATRIX

| Rule | Target+ | Walmart | DTC Microsites |
|------|---------|---------|----------------|
| US Sports (NFL/NBA/NHL) | ❌ BLOCKED | ✅ | ✅ |
| UK Football | ✅ | ✅ | ✅ |
| Entertainment (HP, Peanuts, DC) | ✅ | ✅ | ✅ |
| Anime | ✅ | ✅ | ✅ |
| Music (Iron Maiden etc) | ✅ | ✅ | ✅ |
| Non-licensed art | ✅ | ✅ | ✅ |
| Console skins | ✅ | ✅ | ❌ (separate store) |

---

## 6. DATA PIPELINE FOR IMPORT

```
Step 1: Query BigCommerce API (1.89M SKUs)
  → Filter by: product_type IN [HTPCR, HLBWH, HC, H8939, HDMWH, HHYBK, HB401, HA805, HB6CR]
  → Filter by: device IN [Tier 1 + Tier 2 + Tier 3 list]
  → Filter by: brand IN [Tier A full + Tier B top 10 + Tier C top 5]
  → Exclude: zero sales trailing 12mo, discontinued, Z%, H8%

Step 2: Write to Supabase (catalogue table)
  → Include: SKU, title, description, price, images, brand, device, product_type
  → Flag: target_eligible (bool), walmart_eligible (bool)

Step 3: Shopify Bulk Import (via Admin API)
  → Push ~200K products in batches
  → Tag: marketplace:target, marketplace:walmart, category:sports/anime/entertainment

Step 4: Marketplace Connect Mapping
  → Match Shopify products to Target+ TCINs by SKU
  → Match to Walmart items by GTIN/UPC
```

---

## 7. OPEN DECISIONS FOR CEM

1. ✅ ~~Launch order~~ Sports first (confirmed)
2. **Samsung expansion:** Include Galaxy A16 5G? (£98K revenue — it's your #6 device globally)
3. **Google Pixel:** Include Pixel 9 series? (growing but small)
4. **Console skins:** Include in GoHeadCase Shopify or separate store?
5. **Desk mats:** Only top 50 designs or full catalogue?
6. **Non-licensed art brands:** Include or DTC-only?
7. **Pricing:** Mirror BigCommerce prices or adjust for marketplace fees?

---

*Next step: Run BigCommerce API export with these filters, load to Supabase, then bulk push to GoHeadCase Shopify.*
*Dependent on: BigCommerce API access (Harry had credentials), Supabase catalogue table creation*
