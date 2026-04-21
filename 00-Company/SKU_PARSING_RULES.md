# SKU Parsing Rules — Head Case Designs

> **Purpose:** Definitive reference for parsing Custom_Label / SKU codes across all systems (PULSE, Conversion Dashboard, Shopify staging, Walmart matrix, sales analytics).
> **Owner:** Ava | **Created:** 2026-03-15 | **Source:** Cem directives + data analysis

---

## SKU Format

```
{PRODUCT_TYPE}-{DEVICE_CODE}-{DESIGN_CODE}-{VARIANT}
```

**Examples:**
- `HTPCR-IPH17PMAX-NARUICO-AKA` → Hybrid MagSafe Case, iPhone 17 Pro Max, Naruto Iconic, Akatsuki variant
- `FHTPCR-IPHSE4-PNUTCHA-SNO` → FBA Soft Gel Case, iPhone SE 4, Peanuts Charlie Brown, Snoopy variant
- `HDMWH-900X400X4-NARUGRAT-TRA` → Desk Mat, 900×400×4mm, Naruto Grateful, Traditional variant
- `H8939-DS4CT-RMORGRA-TSP` → Gaming Skin, DualSense 4 Controller, Real Madrid Original, Team Spirit variant

### Parsing Rules

| Position | Field | Split by | Notes |
|----------|-------|----------|-------|
| `[0]` | Product Type | `-` | May have `F` prefix for FBA (see below) |
| `[1]` | Device Code | `-` | Internal code, map to full name via `device_code_map.json` |
| `[2]` | Design Code | `-` | Maps to a lineup/collection, NOT individual artwork |
| `[3]` | Variant | `-` | Specific design variant within the collection (optional, may be absent) |

**Edge cases:**
- Some SKUs have only 3 parts (no variant): `HC-IPH15-DRGBSUSC`
- Some device codes contain hyphens internally — always split from left, max 4 parts
- `Custom_Label` in BQ = full SKU string, unparsed

---

## ⚠️ Critical Rule: FBA Prefix `F`

**SKUs prefixed with `F` are FBA (Fulfilled by Amazon) versions of the SAME product.**

| FBM (Merchant Fulfilled) | FBA (Amazon Fulfilled) | Same Product? |
|--------------------------|------------------------|---------------|
| `HTPCR` | `FHTPCR` | ✅ YES — Hybrid MagSafe Case |
| `HC` | `FHC` | ✅ YES — Hard Case |
| `HLBWH` | `FHLBWH` | ✅ YES — Leather Wallet |
| `HB401` | `FHB401` | ✅ YES — Hard Case v2 |
| `HB6CR` | `FHB6CR` | ✅ YES — Clear MagSafe |
| `HB7BK` | `FHB7BK` | ✅ YES — Black MagSafe |
| `H8939` | `FH8939` | ✅ YES — Gaming Skin |
| `HDMWH` | `FHDMWH` | ✅ YES — Desk Mat |
| `HSTWH` | `FHSTWH` | ✅ YES — Sticker |
| `HGCRD` | `FHGCRD` | ✅ YES — Gaming Carry Case Red |
| `H7805` | `FH7805` | ✅ YES — Controller Skin |
| `HA805` | `FHA805` | ✅ YES — MagSafe Soft Gel |
| `HA501` | `FHA501` | ✅ YES — Credit Card Holder |
| `H9039` | `FH9039` | ✅ YES — Skin variant |

### For all dashboards and analytics:
```python
# Strip F prefix to get canonical product type
def canonical_product_type(product_type):
    if product_type.startswith('F') and product_type != 'FLAG':
        return product_type[1:]
    return product_type
```

**Always combine FBA + FBM when reporting:**
- `HTPCR` + `FHTPCR` = total Soft Gel Case sales
- `HDMWH` + `FHDMWH` = total Desk Mat sales
- Revenue, orders, sessions — all merged under the canonical type

---

## Product Type Reference

### Phone Cases (core 5 for Shopify/Walmart)
| Code | Canonical | Display Name | Price (US) |
|------|-----------|-------------|------------|
| HTPCR / FHTPCR | HTPCR | Hybrid MagSafe Case | $19.95 |
| HB401 / FHB401 | HB401 | Hybrid Hard MagSafe Case | $19.95 |
| HLBWH / FHLBWH | HLBWH | Leather Wallet Case | $24.95 |
| HB6CR / FHB6CR | HB6CR | Clear MagSafe Case | $24.95 |
| HB7BK / FHB7BK | HB7BK | Black MagSafe Case | $24.95 |

### Other Phone Cases
| Code | Canonical | Display Name |
|------|-----------|-------------|
| HC / FHC | HC | Hard Case (Classic) |
| HA805 / FHA805 | HA805 | MagSafe Soft Gel |
| HB1BK | HB1BK | Bumper Case |
| HHYBK | HHYBK | Hybrid Case |

### Non-Phone Products
| Code | Canonical | Display Name |
|------|-----------|-------------|
| HDMWH / FHDMWH | HDMWH | Desk Mat (White base) |
| H8939 / FH8939 | H8939 | Gaming Skin / Vinyl Skin |
| H9039 / FH9039 | H9039 | Skin variant |
| H4621 | H4621 | HP Board / Tablet Case |
| H7805 / FH7805 | H7805 | Controller Skin |
| HSTWH / FHSTWH | HSTWH | Sticker |
| HGCBK | HGCBK | Gaming Carry Case (Black) |
| HGCRD / FHGCRD | HGCRD | Gaming Carry Case (Red) |
| HA501 / FHA501 | HA501 | Credit Card Holder |
| HA921 | HA921 | Unknown accessory |
| HA605 | HA605 | Unknown accessory |

### Shopify-Only Codes
| Code | Display Name |
|------|-------------|
| HLCCG | Leather Case Clear Green |
| HLCCR | Leather Case Clear Red |
| HLCBT | Leather Case Bluetooth |
| HCC01 | Hard Case Custom 01 |
| HCC21 | Hard Case Custom 21 |
| HGSBL | Gaming Skin Blue |
| HGSRD | Gaming Skin Red |

---

## Design Code Structure

Design codes map to **lineups/collections**, not individual artworks.

```
{BRAND_PREFIX}{COLLECTION}{OPTIONAL_SUFFIX}
```

### Known Brand Prefixes → License
| Prefix | License | Notes |
|--------|---------|-------|
| NARU | Naruto Shippuden | NARUICO=Iconic, NARUCHA=Characters, NARUKEY=Keyart |
| PNUT | Peanuts | PNUTCHA=Charlie Brown, PNUTHAL=Halloween, PNUTBOA=Best of All |
| HPOT | Harry Potter | HPOTDH37=Deathly Hallows, HPOTPRI2=Prisoner, HPOTSOR=Sorcerer |
| DRGB | Dragon Ball | DRGBSUSC=Super Characters, DRGBSUSA=Super Art |
| AFC | Arsenal FC | AFCKIT25=Kit 25/26, AFCLOGOS=Logos, AFCCRE=Crest |
| FCB | FC Barcelona | FCBCKT8=Kit, FCBCRE=Crest |
| LFC | Liverpool FC | LFCLVBRD=Liverbird, LFCKIT25=Kit |
| RMCF | Real Madrid CF | RMCFKIT25=Kit, RMCFRET=Retro |
| RMOR | Rick and Morty | RMORGRA=Graphics ⚠️ NOT Real Madrid! |
| THFC | Tottenham | THFCKIT25=Kit, THFCBAD=Badge |
| CFC | Chelsea FC | CFCCRE=Crest |
| MCB | Man City Badge | MCBDKIT25=Kit |
| MCF | Man City FC | MCFTEAM=Team |
| BVR | Bayer Leverkusen | BVRSLCOL=Colors |
| BV | Bayer Leverkusen (alt) | BV1975KY, BVBEKYA, BVQUEEKY |
| IMGC | College Sports (IMG) | IMGCUAL=Alabama, IMGCUAAR=Arkansas, IMGCUOK=Oklahoma |
| WWE / WWE2 | WWE Wrestling | WWE2JEY=Jey Uso, WWE2CRH=Cody Rhodes |
| NFL | NFL | NFLLOSSE=Logos |
| NBA / NBA2 | NBA Basketball | NBA2WAR=Warriors, NBA2LOS=Lakers, NBA2CEL=Celtics |
| NHL | NHL Hockey | NHLBOSB=Boston, NHLDALS=Dallas, NHLPITP=Pittsburgh |
| PPUF | Powerpuff Girls | PPUFGRA=Graphics |
| BTMC | Batman Classic | BTMCHUS=Hush, BTMCLCO=Classic Logo |
| ADVE | Adventure Time | ADVEGRA=Graphics |
| OHIO | Ohio State | OHIOLOGO=Logo, OHIOFLOG=Flag Logo |
| GMOR | Gamer/Gaming | GMORGRA=Graphics |
| SPRC | Snoopy Racing | SPRCLOG=Logo, SPRCCOM=Comic |
| SCDO | Scooby-Doo | SCDOGRA=Graphics, SCDOMYS=Mystery |
| HATS | Hats Collection | HATSGRA=Graphics |
| SUPN | Supernatural | SUPNKEY=Keyart |
| IRON | Iron Maiden | IRONALB=Album, IRONGAR=Graphics |
| WMG | Warner Music | WMGRATTRE=Grateful Dead |
| LTOO | Looney Tunes | LTOOGCH=Graphics |
| TDKR | Dark Knight Rises | TDKRLOG=Logo |
| ACM | AC Milan | ACMGLO=Logo |
| ROMA | AS Roma | ROMACREG=Crest |
| UFC | UFC | UFCLOGO=Logo |
| FLAG | Flags | National flags (NOT FBA prefix!) |
| F1309 | Formula 1 | F1309GRA=Graphics (NOT FBA prefix!) |

### ⚠️ FBA Prefix Exceptions
These design codes START with F but are NOT FBA:
- `FLAG` — National flags
- `F1309` — Formula 1
- `FRND` — Friends (TV show)
- `FKFLOR` — FK Floral

**Rule:** Only strip `F` from the PRODUCT TYPE position `[0]`, never from design codes.

---

## Device Code Mapping

Device codes are internal, not customer-facing. Map to full names for all dashboards and listings.

### Key Mappings (from BigCommerce `DeviceModel` custom field)
| Code | Full Name |
|------|-----------|
| IPH17PMAX | iPhone 17 Pro Max |
| IPH17PRO | iPhone 17 Pro |
| IPH17 | iPhone 17 |
| IPH17AIR | iPhone Air |
| IPHSE4 | iPhone SE (4th Gen) |
| IPH16PMAX | iPhone 16 Pro Max |
| IPH16PRO | iPhone 16 Pro |
| IPH16 | iPhone 16 |
| IPH16PLUS | iPhone 16 Plus |
| IPH15PMAX | iPhone 15 Pro Max |
| IPH15PRO | iPhone 15 Pro |
| IPH15 | iPhone 15 |
| IPH15PLUS | iPhone 15 Plus |
| IPH14PMAX | iPhone 14 Pro Max |
| IPH14PRO | iPhone 14 Pro |
| IPH14 | iPhone 14 |
| IPH13PMAX | iPhone 13 Pro Max |
| IPH13PRO | iPhone 13 Pro |
| IPH13 | iPhone 13 |
| IPH12 | iPhone 12 / 12 Pro |
| IPH11 | iPhone 11 |
| S938U | Samsung Galaxy S25 Ultra |
| S936X | Samsung Galaxy S25+ |
| S931X | Samsung Galaxy S25 |
| S928U | Samsung Galaxy S24 Ultra 5G |
| S926U | Samsung Galaxy S24+ 5G |
| S921U | Samsung Galaxy S24 5G |
| A165G | Samsung Galaxy A16 5G |
| A152024 | Samsung Galaxy A15 (2024) |
| PIX9PRO | Google Pixel 9 Pro |
| IPAD102 | iPad 10.2" |
| IPADAIR20 | iPad Air (2020) |
| DS4CT | DualSense 4 Controller |
| 900X400X4 | Desk Mat 900×400mm (Large) |
| 600X300X3 | Desk Mat 600×300mm (Medium) |
| 300X250X3 | Desk Mat 300×250mm (Small) |
| SWTCH2 | Nintendo Switch 2 |

**Full mapping:** `data/device_code_map.json` (expand from BC API as needed)

---

## SQL Reference

### BQ (raw Custom_Label)
```sql
-- Parse SKU parts from Custom_Label
SELECT
  SPLIT(Custom_Label, '-')[SAFE_OFFSET(0)] as product_type_raw,
  -- Strip F prefix for canonical type
  CASE 
    WHEN STARTS_WITH(SPLIT(Custom_Label, '-')[SAFE_OFFSET(0)], 'F') 
         AND SPLIT(Custom_Label, '-')[SAFE_OFFSET(0)] NOT IN ('FLAG', 'F1309')
    THEN SUBSTR(SPLIT(Custom_Label, '-')[SAFE_OFFSET(0)], 2)
    ELSE SPLIT(Custom_Label, '-')[SAFE_OFFSET(0)]
  END as product_type,
  SPLIT(Custom_Label, '-')[SAFE_OFFSET(1)] as device_code,
  SPLIT(Custom_Label, '-')[SAFE_OFFSET(2)] as design_code,
  SPLIT(Custom_Label, '-')[SAFE_OFFSET(3)] as variant
FROM `instant-contact-479316-i4.zero_dataset.orders`
```

### Supabase (pre-parsed)
```sql
-- Supabase already has parsed columns
-- But product_type_code still has F prefix — strip in queries
SELECT
  CASE 
    WHEN product_type_code LIKE 'F%' 
         AND product_type_code NOT IN ('FLAG', 'F1309')
    THEN SUBSTRING(product_type_code FROM 2)
    ELSE product_type_code
  END as canonical_type,
  device_code,
  design_code,
  design_variant
FROM orders
```

### Python
```python
def parse_sku(sku):
    parts = sku.split('-', 3)  # Max 4 parts
    raw_type = parts[0] if len(parts) >= 1 else ''
    
    # Canonical product type (strip FBA F prefix)
    FBA_EXCEPTIONS = {'FLAG', 'F1309', 'FRND', 'FKFLOR'}
    if raw_type.startswith('F') and raw_type not in FBA_EXCEPTIONS:
        canonical_type = raw_type[1:]
        is_fba = True
    else:
        canonical_type = raw_type
        is_fba = False
    
    return {
        'product_type_raw': raw_type,
        'product_type': canonical_type,
        'is_fba': is_fba,
        'device_code': parts[1] if len(parts) >= 2 else '',
        'design_code': parts[2] if len(parts) >= 3 else '',
        'variant': parts[3] if len(parts) >= 4 else '',
    }
```

---

## Region Mapping (for PULSE / Gap Analysis)

Orders don't have a `region` column. Use `Buyer_Country` (BQ) or `buyer_country` (Supabase):

| Region | Buyer Countries |
|--------|----------------|
| US | `United States Of America`, `United States` |
| UK | `United Kingdom` |
| EU | `Germany`, `France`, `Italy`, `Spain`, `Austria`, `Belgium`, `Netherlands`, `Luxembourg`, `Sweden`, `Switzerland`, `Denmark`, `Finland`, `Ireland` |

**Note:** `PO_Location` (Florida, UK, PH) = fulfillment warehouse, NOT buyer region.

---

## Currency Normalization

BQ `Net_Sale` is a STRING in original currency. Supabase `net_sale_usd` is pre-converted.

| Currency | FX Rate (hardcoded) |
|----------|-------------------|
| USD | 1.0 |
| GBP | 1.27 |
| EUR | 1.08 |
| AUD | 0.65 |
| JPY | 0.0067 |
| SEK | 0.095 |
| CAD | 0.74 |

---

*This document is the single source of truth for SKU parsing. Update here first, then propagate to dashboards and scripts.*
