# Walmart Listing Data Profile
*Generated: 2026-03-10 04:46 AM EST | Source: BQ `zero_dataset.walmart_active_listings`*

## Executive Summary

**95,640 published listings generating $1,058 in 90 days.** That's $0.011 per listing per quarter. The channel is functionally dormant despite having massive catalog coverage.

---

## Key Findings

### 1. Revenue: Catastrophically Low
| Metric | Value |
|--------|-------|
| Active listings | 95,640 |
| SKUs with any sale (90d) | 49 |
| Total orders (90d) | 50 |
| Total revenue (90d) | $1,057.50 |
| Revenue per listing per quarter | $0.011 |
| Top SKU orders | 2 (max) |
| Avg order value | $21.15 |

**17 of 49 sold SKUs don't match active listings** — either delisted or SKU naming mismatch. Need investigation.

### 2. Title Length: 99.9% Non-Compliant
Walmart recommends **50-75 characters**. Our distribution:

| Bucket | Count | % |
|--------|-------|---|
| <50 (too short) | 9 | 0.0% |
| **50-75 (ideal)** | **55** | **0.1%** |
| 76-100 (borderline) | 7,335 | 7.7% |
| 101-150 (long) | 69,315 | 72.5% |
| 150+ (way too long) | 18,926 | 19.8% |

**Average title length: 133 chars** — nearly 2x the recommended max.

Typical title pattern: `Head Case Designs Officially Licensed [Artist/License] [Collection] [Design Name] [Case Type] Case [Compatible with/for] [Device]`

The "Head Case Designs Officially Licensed" prefix alone is 38 chars, consuming 50-76% of the ideal budget.

### 3. Reviews: Virtually Zero
| Metric | Value |
|--------|-------|
| SKUs with any reviews | 68 (0.07%) |
| Total reviews | 83 |
| 95,572 SKUs | 0 reviews |

**Implication:** Content quality is literally the only conversion lever. No social proof exists.

### 4. Pricing: Well-Positioned
| Metric | Value |
|--------|-------|
| Avg price | $21.28 |
| Min | $9.95 |
| Max | $39.95 |
| In $10-30 sweet spot | 90,762 (94.9%) |

Pricing is NOT the problem.

### 5. Buy Box: Strong
| Metric | Value |
|--------|-------|
| Buy box eligible | 95,551 (99.9%) |

### 6. Product Mix
| Product Type | Count | Avg Price | Reviews |
|-------------|-------|-----------|---------|
| Cell Phone Cases | 86,316 (90.3%) | $20.86 | 66 |
| Tablet Cases | 3,908 | $26.75 | 3 |
| Gaming Skins | 2,369 | $23.20 | 9 |
| Gaming Accessories | 2,087 | $22.71 | 4 |
| Laptop Skins | 931 | $28.87 | 0 |
| Tablet Skins | 24 | $26.45 | 1 |
| Other (Volleyball, Pet) | 5 | ~$19 | 0 |

### 7. Brand Distribution
| Brand | Count |
|-------|-------|
| Head Case Designs | 95,610 (99.97%) |
| Ecell | 26 |
| Cat Coquillette | 2 |
| Others | 2 |

### 8. Catalog Structure
- **4,546 variant groups** with 1,797 primary variants
- Avg ~21 variants per group (design × device)
- All 95,640 are ACTIVE + PUBLISHED

---

## Schema Limitations

The bulk export only contains: `sku, item_id, product_name, lifecycle_status, publish_status, product_type, price, currency, buy_box_eligible, gtin, upc, brand, reviews_count, average_rating, variant_group_id, primary_variant`

**Missing from export (needed for full audit):**
- Feature bullets (count + content)
- Product description (length + quality)
- Image URLs (count + quality)
- Category/attribute completeness
- Search keywords/backend terms

→ **Need Walmart Item API** or Seller Center content export for Phase 2.

---

## Recommendations (Priority Order)

### P0: Title Optimization (Quick Win, Highest Impact)
**99.9% of titles exceed Walmart recommended length.** This likely suppresses search ranking.
- Shorten from "Head Case Designs Officially Licensed [License] [Collection] [Design] [Type] Case Compatible with [Device]" 
- To: "Head Case [License] [Design] [Type] – [Device]"
- Could reduce avg from 133→70 chars
- **Can be done programmatically** from existing SKU data (design_code + device_code parsing)
- **Scope:** 95,576 titles need shortening

### P1: Content Enrichment (Needs API Access)
- Pull full listing content via Walmart Item API
- Audit bullet count, description length, image count
- Create gold-standard templates per product type

### P2: Revenue Investigation
- Why are only 49 of 95K SKUs selling?
- Are listings getting impressions at all? (Need Walmart Seller Center analytics)
- 17 sold SKUs not in active listings — SKU mismatch or recently delisted?
- Cross-ref with PULSE velocity data: are designs that sell on Amazon/eBay also listed but not selling on Walmart?

### P3: Review Strategy
- 83 reviews across 95K SKUs = essentially zero social proof
- Consider Walmart's Spark Reviews program
- Priority: Get reviews on top 50 revenue-generating designs (if they exist)

---

*Next steps: Spawn Atlas for programmatic title scoring → Echo for template creation → Present findings to Cem.*
