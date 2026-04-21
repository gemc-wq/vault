# Walmart Title Optimization Playbook
*Generated: 2026-03-10 07:46 AM EST | Author: Ava*

## Problem
99.9% of 95,640 Walmart titles exceed the recommended 50-75 character limit. Average: 133 chars. Only 55 titles (0.06%) are in the ideal range.

## Current Title Pattern
```
Head Case Designs Officially Licensed [License] [Collection] [Design Name] [Case Type Full] Compatible with [Brand] [Device]
```
Example (155 chars):
> Head Case Designs Officially Licensed Harry Potter Sorcerer's Stone I Gryffindor Crest Leather Book Wallet Case Cover Compatible with Google Google Pixel 4

## Proposed Shortening Rules

### Tier 1: Conservative (no brand removal)
| Find | Replace | Chars Saved |
|------|---------|-------------|
| `Head Case Designs Officially Licensed ` | `Head Case ` | 28 |
| `Leather Book Wallet Case Cover` | `Wallet Case` | 19 |
| `Hard Back Case` | `Hard Case` | 5 |
| `Vinyl Sticker Skin Decal Cover` | `Vinyl Skin` | 20 |
| `Compatible with ` | `for ` | 12 |

**Average savings: 40-59 chars per title**

**Result distribution (Tier 1):**
| Range | Before | After |
|-------|--------|-------|
| 50-75 ✅ | 0.1% | 9.6% |
| 76-100 | 7.7% | 69.6% |
| 101-120 | — | 17.5% |
| 120+ | 92.3% | 3.3% |

**Example (Tier 1):**
> Head Case Harry Potter Sorcerer's Stone I Gryffindor Crest Wallet Case for Google Pixel 4
> (91 chars — still over ideal but a 42% reduction)

### Tier 2: Aggressive (brand in attribute, not title)
Since `brand = "Head Case Designs"` is already a separate Walmart catalog attribute visible on the listing page, the brand prefix is redundant in the title.

| Find | Replace | Chars Saved |
|------|---------|-------------|
| `Head Case Designs Officially Licensed ` | *(remove)* | 38 |
| `Head Case Designs ` | *(remove)* | 19 |
| `Leather Book Wallet Case Cover` | `Wallet Case` | 19 |
| `Hard Back Case` | `Hard Case` | 5 |
| `Vinyl Sticker Skin Decal Cover` | `Vinyl Skin` | 20 |
| `Compatible with ` | `for ` | 12 |

**Example (Tier 2):**
> Harry Potter Sorcerer's Stone Gryffindor Crest Wallet Case for Google Pixel 4
> (78 chars — nearly ideal)

**Or even tighter:**
> Harry Potter Gryffindor Crest Wallet Case – Google Pixel 4
> (58 chars ✅ ideal)

### Tier 3: Walmart-Optimized Formula
```
[License] [Design] [Case Type] – [Device]
```
- Brand lives in Brand attribute field (searchable, visible)
- "Officially Licensed" → unnecessary when Brand = "Head Case Designs" (it's implied)
- Drop collection sub-names that add length without search value

---

## Case Type Distribution (for template mapping)
| Case Type | SKU Count | Avg Title Len | Short Name |
|-----------|-----------|---------------|------------|
| Soft Gel | 39,245 | 119.5 | Gel Case |
| Leather Wallet | 26,253 | 143.3 | Wallet Case |
| Hard Case | 9,722 | 127.7 | Hard Case |
| Hybrid | 9,141 | 125.0 | Hybrid Case |
| Vinyl Skin | 114 | 143.4 | Vinyl Skin |
| Other | 1,841 | 146.9 | *(varies)* |

## Implementation Path

### Phase 1: Bulk Title Regen (Programmatic)
1. Parse SKU codes → design_code, device_code, product_type_code
2. Cross-ref with BQ `headcase.tblDesigns` for license/design names
3. Apply Tier 2 or 3 shortening formula
4. Generate CSV of old→new title mappings
5. **Cem approval** on formula + 50-sample review
6. Bulk upload via Walmart Seller Center

### Phase 2: A/B Test (Optional, Recommended)
- Pick 500 SKUs with highest impressions
- Apply new titles to 250, keep old on 250
- Measure CTR/conversion over 30 days

### Blockers
- **Decision needed from Cem:** Tier 1, 2, or 3? (Recommend Tier 2 — brand stays visible via attribute, titles hit search-friendly length)
- **Need:** Walmart Seller Center bulk upload access (or API)
- **Need:** Cross-reference with `headcase.tblDesigns` for clean license names

---

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| SEO rank drop from title change | Low | Medium | Walmart algo favors shorter titles; we're currently penalized |
| Brand visibility loss (Tier 2/3) | Low | Low | Brand attribute field handles this |
| Bulk upload errors | Medium | Medium | Test with 100 SKUs first, validate before full push |
| License compliance (title wording) | Low | High | Check license agreements for title requirements |

---

*Recommendation: Present Tier 2 to Cem for approval. Estimated scope: 95K title rewrites via programmatic generation. No manual copywriting needed — this is a data transformation task.*
