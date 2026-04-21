# SKU Structure — New Product Lines
## Water Bottles & Metal Wall Art

> **Prepared by:** Ava | **Date:** 2026-03-24
> **Status:** PROPOSAL — needs Cem approval before PH team uses
> **Follows:** `wiki/SKU_PARSING_RULES.md` standard format: `{PRODUCT_TYPE}-{DEVICE/SIZE}-{DESIGN}-{VARIANT}`

---

## Product Type Codes

| Product | Code | FBA Code | Rationale |
|---------|------|----------|-----------|
| Water Bottle 24oz UV DTF | HWBT24 | FHWBT24 | H = Head Case, WBT = Water Bottle, 24 = 24oz |
| Water Bottle 32oz UV DTF | HWBT32 | FHWBT32 | Same pattern, 32 = 32oz |
| Water Bottle 24oz Laser | HWBL24 | FHWBL24 | WBL = Water Bottle Laser |
| Water Bottle 32oz Laser | HWBL32 | FHWBL32 | Same pattern |
| Metal Wall Art 300×400 | HMWA34 | FHMWA34 | MWA = Metal Wall Art, 34 = 300×400mm |

### Why separate codes for UV DTF vs Laser?
- Different pricing tiers ($39.99 vs $44.99)
- Different creative requirements (raster artwork vs vector-only)
- Different COGS ($4.50 base vs same base + laser setup)
- Follows precedent: HTPCR vs HC are separate codes for different case constructions of the same "phone case" category

### Alternative (simpler): Single bottle code
If Cem prefers fewer codes:
- `HWBT` for all water bottles, with size in device position and print method in variant
- e.g. `HWBT-24OZ-LFCORI-LSRCRS` (laser crest) vs `HWBT-24OZ-LFCORI-CLRWRP` (color wrap)
- **Downside:** Variant field now encodes print method AND design variant — breaks pattern

**Recommendation:** Use separate codes (HWBT24/HWBL24). Cleaner for analytics, pricing, and inventory.

---

## Device/Size Position

Since these aren't phone cases, this position holds the **physical variant** instead:

### Water Bottles
| Code | Meaning |
|------|---------|
| WHT | White body |
| BLU | Blue body |
| SLV | Silver body |
| RED | Red body |
| BLK | Black body (matte) |

**Note:** Size is already in the product type code (24/32). Body color goes in device position.
- Example: `HWBT24-WHT-PNUTCHA-SNO` = 24oz White UV DTF, Peanuts Charlie Brown, Snoopy variant

### Metal Wall Art
| Code | Meaning |
|------|---------|
| GLW | Gloss White coated (standard) |
| MTL | Raw metal / brushed (future) |

- Example: `HMWA34-GLW-MANCORI-BDG` = 300×400mm Gloss White, Man City Original, Badge variant

---

## Design & Variant Codes

Reuse existing design codes from the case catalog wherever possible:

### Approved Licenses for Launch
| License | Design Code(s) | Source |
|---------|----------------|--------|
| Man City | MANCORI, MANC* | Existing catalog |
| Tottenham | THOTORI, THOT* | Existing catalog |
| Warner Bros — Batman | BATM* | Existing catalog |
| Warner Bros — Harry Potter | HPOT* | Existing catalog |
| Warner Bros — Looney Tunes | LOON* | Existing catalog |
| Liverpool FC | LFC* | Existing catalog (seen on prototype bottles) |
| WWE | WWE* | Existing catalog (seen on prototype bottles) |
| Peanuts | PNUT* | Existing catalog |

**Key principle:** Same design code, same variant code across ALL product types. `PNUTCHA-SNO` means the same artwork whether on HTPCR, HWBT24, or HMWA34.

---

## Pricing Matrix

| Product Code | US Price | UK Price (est.) | Notes |
|-------------|----------|-----------------|-------|
| HWBT24 | $39.99 | £34.99 | UV DTF full-color |
| HWBT32 | $44.99 | £39.99 | UV DTF full-color |
| HWBL24 | $44.99 | £39.99 | Laser engraving premium |
| HWBL32 | $49.99 | £44.99 | Laser engraving premium |
| HMWA34 | $29.99 | £24.99 | Standard size |

---

## COGS Summary

| Product | Unit Cost | Shipping/Landed | Total COGS | Margin at Price |
|---------|-----------|-----------------|------------|-----------------|
| HWBT24 (UV DTF) | ~$4.50 (¥32.50) | ~$5.50 | ~$10.00 | 75% at $39.99 |
| HWBT32 (UV DTF) | ~$5.50 (¥40) | ~$6.50 | ~$12.00 | 73% at $44.99 |
| HWBL24 (Laser) | ~$4.50 + laser | ~$5.50 | ~$11.00 | 76% at $44.99 |
| HMWA34 | $3.94 + $2.10 mount | ~$3.00 | ~$9.04 | 70% at $29.99 |

**Note:** Bottle shipping estimates from Cem's note that freight is similar to HDMWH (desk mats). Landed cost $10-13 for 24oz confirmed.

---

## EAN Assignment

- New product types need EAN ranges allocated
- Check Zero DB for any pre-existing bottle/wall art EANs (unlikely — new category)
- If no existing EANs: request allocation from GS1 or use existing Ecell prefix + new product suffix
- **Blocker:** EAN availability determines marketplace readiness (Amazon accepts without, Walmart requires GTIN-14)

---

## Amazon Category & Browse Nodes

### Water Bottles
- **Primary:** Sports & Outdoors > Sports Water Bottles
- **Secondary:** Cell Phone Accessories > Stands (for MagSafe feature)
- **Item Type:** WATER_BOTTLE
- **Key attributes:** material, capacity_unit, insulation_type, special_feature (MagSafe compatible)

### Metal Wall Art
- **Primary:** Home & Kitchen > Wall Art > Metal Wall Art
- **Secondary:** Sports Fan Shop > Fan Décor > Wall Art (for sports licenses)
- **Item Type:** WALL_ART
- **Key attributes:** material_type (aluminum), mounting_type (magnetic), size

---

## Next Steps
1. ✅ SKU structure defined (this doc)
2. ⏳ Cem approval on product type codes
3. ⏳ EAN allocation (check Zero DB first, then GS1 if needed)
4. ⏳ PH team to measure actual bottle dimensions (template adjustment)
5. ⏳ First 5 designs selected for production (Cem to pick from approved licenses)
6. ⏳ Amazon listing flat file creation (once SKUs + EANs assigned)

---

*Follows `wiki/SKU_PARSING_RULES.md` conventions. Cross-compatible with PULSE, Conversion Dashboard, and all analytics.*
