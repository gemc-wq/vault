# S3 Image URL Rules — Head Case Designs
*Source: Jessie Morales (j.morales@ecellglobal.com), Email Mar 31 2026*
*Owner: Ava | Added to Vault: 2026-04-10 | Critical for: Shopify, Walmart, Blueprint V3*

---

## Infrastructure

- **S3 Bucket:** ecellglobal
- **Image Root:** `https://elcellonline.com/atg/`
- **Source DB:** Zero production at 192.168.20.160 (PH LAN)

---

## Core URL Pattern

```
https://elcellonline.com/atg/{LINEUP}/{VARIANT}/{CASE_PREFIX}-{DEVICE}-{POSITION}.jpg
```

**Example:**
```
https://elcellonline.com/atg/NARUICO/AKA/TP-CR-IPH17PMAX-1.jpg
```

| Variable | Source | Example |
|---|---|---|
| `{LINEUP}` | Design code (SKU position 2) | NARUICO |
| `{VARIANT}` | Variant folder code (see Variant Naming Rules) | AKA |
| `{CASE_PREFIX}` | Product type prefix (see table below) | TP-CR |
| `{DEVICE}` | Device code — same as SKU device code | IPH17PMAX |
| `{POSITION}` | Image position number (1–6 for new cases) | 1 |

---

## Case Prefix → Image Prefix Mapping

| Product Type (SKU) | Image Prefix | Confirmed |
|---|---|---|
| HTPCR / FHTPCR | TP-CR | ✅ Widest coverage |
| HY-BK | HY-BK | ✅ |
| B1-BK | B1-BK | ✅ |
| HLBWH | LB-WH | ✅ |
| HC / HC-CR | HC-CR | ✅ |
| HB6CR | B6-CR | ✅ |
| HB7BK | B7-BK | ✅ |
| HB401 | B4-01 | ✅ |

---

## Image Positions

### Old-Style Cases (TP-CR and most existing lineups)
**1 position only:**
| Position | Label | Description |
|---|---|---|
| 1 | Front and Back | Front-facing and back view product shot |

### New-Style Cases (NBA lineups and newer — 6 positions)
| Position | Label | Description |
|---|---|---|
| 1 | Hero View | Front and back view of phone case |
| 2 | Feature Image 1 | Product feature callout |
| 3 | Feature Image 2 | Product feature callout |
| 4 | Feature Image 3 | Product feature callout |
| 5 | Marketing / Lifestyle 1 | Lifestyle image |
| 6 | Marketing / Lifestyle 2 | Lifestyle image |

**Key rule:** For Shopify/Walmart listings on new-style products, upload all 6 positions. For old-style (TP-CR), only position 1 exists — do not attempt 2–6.

---

## Variant Naming Rules

The variant folder name is **not always the first 3 letters** of the design name. It's a specific code assigned per design. Examples from Naruto Shippuden:

| Design Name | Design Code | LB-WH Variant |
|---|---|---|
| Akatsuki | AKA | LAKA |
| Naruto Uzumaki | NUZ | LNUZ |
| Itachi Uchiha | ITA | LITA |
| Kakashi Hatake | KAK | LKAK |
| Sasuke Uchiha | SAS | LSAS |
| Pain | PAI | LPAI |

**Note on LB-WH (Leather Wallet):** Variant codes are prefixed with `L`. See `s3_image_url_rules.json` → "Variant Naming Rules" sheet for full table.

---

## Coverage Notes

- **TP-CR**: Widest device coverage — up to iPhone 17 Pro Max
- **HY-BK**: Limited — stops at iPhone 16
- **Other prefixes**: Coverage varies — check before generating URLs
- The "Coverage & Exceptions" sheet (2,132 rows) documents all device codes with gaps — saved in `s3_image_url_rules.json`

---

## Feature/Group Images (Shared Static)

Static feature images (shared across designs, per device group) are stored at:
```
https://elcellonline.com/atg/staticimages/features/2020/combined/
```

**⚠️ Status:** URL pattern from wiki is currently returning 404s. Correct static unit codes for device groups need to be confirmed with Jessie/IT before automating. Do not assume device-specific codes work here.

**Action needed:** Get one working example URL from Jessie for the iPhone feature image group to establish the correct pattern.

---

## For Pipeline Builders (Blueprint V3)

```python
def get_product_image_url(lineup, variant, product_type, device_code, position=1):
    PREFIX_MAP = {
        'HTPCR': 'TP-CR', 'FHTPCR': 'TP-CR',
        'HB401': 'B4-01', 'FHB401': 'B4-01',
        'HLBWH': 'LB-WH',
        'HC': 'HC-CR',
        'HB6CR': 'B6-CR',
        'HB7BK': 'B7-BK',
        'HYBK': 'HY-BK',
    }
    prefix = PREFIX_MAP.get(product_type, 'TP-CR')
    return f"https://elcellonline.com/atg/{lineup}/{variant}/{prefix}-{device_code}-{position}.jpg"

# Hero image (always use this for main product image)
url = get_product_image_url('NARUICO', 'AKA', 'HTPCR', 'IPH17PMAX', position=1)
# → https://elcellonline.com/atg/NARUICO/AKA/TP-CR-IPH17PMAX-1.jpg
```

---

## Files

| File | Contents |
|---|---|
| `S3_IMAGE_URL_RULES.md` | This document — human-readable rules |
| `s3_image_url_rules.json` | Machine-readable — all 3 sheets from Jessie's spreadsheet |
| `device_code_map.json` | Device code → full device name |
| `sku_brand_map.json` | Brand code → brand name (750 entries) |
| `SKU_PARSING_RULES.md` | Core SKU parsing logic |

---

*Source email: "Re: S3 Image URL Rules — Need Full Documentation" from j.morales@ecellglobal.com, Mar 31 2026*
*Thread ID: 19d41698de52756e | Message ID: 19d423928f2240c0*
