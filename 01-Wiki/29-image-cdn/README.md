# Product Image CDN — S3 Rules
> **Owner:** Ava | **Source:** Cem (Mar 18) | **Updated:** 2026-03-18

## Infrastructure
- **S3 Bucket:** ecellglobal
- **Image Root:** `/atg/`
- **Public URL:** `https://elcellonline.com/atg/` (points to S3)
- **Source DB:** Zero production at 192.168.20.160 (PH LAN)

## Folder Structure
```
/atg/{lineup_code}/{design_variant}/{image_files}
```
Example: `/atg/LFCKIT25/AWY/TP-CR-IPH17PMAX-1.jpg`

## URL Patterns

### Primary Product Images (for Shopify/Walmart feed)
| Type | Pattern | Example |
|------|---------|---------|
| **Design Main** | `/atg/{lineup}/{design}/{product}-{color}-{unit}-1.jpg` | `/atg/NARUICO/AKA/TP-CR-IPH17PMAX-1.jpg` |
| **Design Main 2** | `/atg/{lineup}/{design}/{product}-{color}-{unit}-2.jpg` | `/atg/NARUICO/AKA/TP-CR-IPH17PMAX-2.jpg` |
| **Design Main w/BG** | `/atg/{lineup}/{design}/{product}-{color}-{static-unit}-1b.jpg` | Background version |

### Secondary Images
| Type | Pattern |
|------|---------|
| Design Main Others | `/atg/{lineup}/{design}/{product}-{color}-{unit}-{dsn-ctr}.jpg` |
| Design Main Others Laptop | `/atg/{lineup}/{design}/{product}-{color}-{static-unit}-{dsn-ctr}-XX.jpg` |
| Design Grid | `/atg/{lineup}/{product}-{color}-{main-unit}-2A.jpg` |

### Feature/Supporting Images
| Type | Pattern |
|------|---------|
| Feature Group | `/atg/staticimages/features/2020/combined/{product}-{color}-{static-unit}-{l…}.jpg` |
| Feature | `/atg/staticimages/features/2020/{product}-{color}-{static-unit}-{fp-ctr}-{l…}.jpg` |
| New Feature | `/atg/staticimages/features/2020/{product}-{color}-{static-unit}-{fp-ctr}.jpg` |
| Feature Design | `/atg/{lineup}/{design}/{product}-{color}-{unit}-{fp-ctr}.jpg` |
| Packaging | `/atg/staticimages/features/{fp-brand}/HC-CR-{pack-unit}-5-EN.jpg` |

### Special
| Type | Pattern |
|------|---------|
| Tempered Main | `/atg/X/X/{product}-{color}-{unit}.jpg` |
| Design Strawberry | `/atg/{lineup}/{design}/{product}-{color}-{static-unit}-2-{lang-code}.jpg` |

## Variable Mapping (SKU → Image URL)

SKU format: `{PRODUCT_TYPE}-{DEVICE}-{DESIGN_CODE}-{VARIANT}`

| Image Variable | Source | Example |
|---------------|--------|---------|
| `{lineup}` | = design_code (SKU position 2) | NARUICO |
| `{design}` | = variant (SKU position 3) | AKA |
| `{product}` | = case prefix (mapped from product type) | TP-CR |
| `{color}` | Usually empty or part of product prefix | - |
| `{unit}` | = device_code (SKU position 1) | IPH17PMAX |

### Product Type → Image Prefix Mapping
| Product Type | Image Prefix | Confirmed |
|---|---|---|
| HTPCR | TP-CR | ✅ (verified Mar 18) |
| HB401 | HB-01 | ⚠️ (limited coverage) |
| HLBWH | LB-WH | ⚠️ (not tested) |
| HC | HC-CR | ⚠️ (not tested) |
| HB6CR | H6-CR | ⚠️ (not tested) |
| HB7BK | H7-BK | ⚠️ (not tested) |
| H8939 | H8-39 or 89-39? | ❌ (need to verify) |
| HDMWH | DM-WH? | ❌ (need to verify) |
| FHTPCR | TP-CR (same as HTPCR) | likely |

## For Shopify/Walmart Lister
```python
def get_image_url(design_code, variant, product_type, device_code):
    PREFIX_MAP = {
        'HTPCR': 'TP-CR', 'HB401': 'HB-01', 'HLBWH': 'LB-WH',
        'HC': 'HC-CR', 'HB6CR': 'H6-CR', 'HB7BK': 'H7-BK',
    }
    prefix = PREFIX_MAP.get(product_type, 'TP-CR')  # fallback to TP-CR
    return f"https://elcellonline.com/atg/{design_code}/{variant}/{prefix}-{device_code}-1.jpg"
```

## Coverage Notes
- TP-CR: widest coverage (up to iPhone 17 Pro Max)
- HY-BK: stops at iPhone 16 (no iPhone 17 yet)
- Other prefixes: coverage varies, need to verify per product type
- Only position 1 (hero image) consistently available; position 2+ may not exist
- Static feature images under `/atg/staticimages/` are shared across all devices
