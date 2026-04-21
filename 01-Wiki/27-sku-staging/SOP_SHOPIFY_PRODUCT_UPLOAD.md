# SOP: Shopify Product Upload
**Version:** 1.0 | **Date:** 2026-04-06 | **Owner:** Ava
**Status:** APPROVED — use for ALL Shopify uploads

---

## The Problem with Previous Uploads

The March 2026 Shopify upload was **non-compliant** on 4 counts:
1. Titles used raw design codes (RMCF, CFC, IMGC) not brand names (Real Madrid CF, Chelsea FC)
2. Descriptions were missing — no hero copy, no features, no design context
3. Inventory set to 0 — should always be 9999 for print-on-demand
4. SEO meta fields missing entirely

**This SOP prevents that from happening again.**

---

## Step 1: Design Code → Brand Name Resolution (MANDATORY)

Before any title is written, resolve the design code to its full license/brand name.
**Never use the design code in a customer-facing title.**

### Brand Code Lookup Table (required fields)

| Design Prefix | Brand Name | License Type |
|---|---|---|
| NARU | Naruto Shippuden | Anime |
| NARUICO | Naruto Shippuden — Iconic | Anime |
| NARUCHA | Naruto Shippuden — Characters | Anime |
| NARUKEY | Naruto Shippuden — Key Art | Anime |
| DRGB | Dragon Ball | Anime |
| DRGBSUSC | Dragon Ball Super — Universe Survival | Anime |
| HOTS | Hatsune Miku | Music/Anime |
| HATSGRA | Hatsune Miku — Graphics | Music/Anime |
| HPOT | Harry Potter | Entertainment |
| HPOTDH37 | Harry Potter — Deathly Hallows | Entertainment |
| PNUT | Peanuts | Entertainment |
| PNUTCHA | Peanuts — Charlie Brown Characters | Entertainment |
| PNUTHAL | Peanuts — Halloween | Entertainment |
| PNUTBOA | Peanuts — Best of All | Entertainment |
| WWE / WWE2 | WWE — [Character Name] | Sport/Ent |
| NBA / NBA2 | NBA — [Team Name] | Sport |
| NBA2MAVLG | NBA — Dallas Mavericks | Sport |
| NBA2WAR | NBA — Golden State Warriors | Sport |
| NBA2NKN | NBA — New York Knicks | Sport |
| NBA2LOS | NBA — Los Angeles Lakers | Sport |
| NBA2CEL | NBA — Boston Celtics | Sport |
| NHL | NHL Hockey — [Team Name] | Sport |
| NHLBOSB | NHL — Boston Bruins | Sport |
| NHLPITP | NHL — Pittsburgh Penguins | Sport |
| NFL | NFL — [Team Name] | Sport |
| RMCF | Real Madrid CF | Football |
| RMCFORI | Real Madrid CF — Origin | Football |
| RMCFRET | Real Madrid CF — Retro | Football |
| AFC / AFCKIT | Arsenal FC | Football |
| AFCLOGOS | Arsenal FC — Logos | Football |
| FCB / FCBCKT | FC Barcelona | Football |
| FCB KIT25 | FC Barcelona — Kit 2025/26 | Football |
| LFC / LFCLVBRD | Liverpool FC | Football |
| CFC | Chelsea FC | Football |
| THFC | Tottenham Hotspur | Football |
| MCB | Manchester City | Football |
| BTMC | Batman | DC Comics |
| BTMCHUS | Batman — Hush | DC Comics |
| SPRC | Superman | DC Comics |
| IMGC | [Full College/University Name] | College Sport |
| IMGCUAL | University of Alabama | College Sport |
| IMGCUOK | University of Oklahoma | College Sport |
| IMGCUTK | University of Tennessee | College Sport |
| IMGCPSU | Penn State University | College Sport |
| IMGCAUB | Auburn University | College Sport |
| IMGCLSU | LSU | College Sport |
| OHIOLOGO | Ohio State University | College Sport |
| FLAG | [Country Name] Flag | Flags |
| RMOR | Rick and Morty | Entertainment |
| ADVE | Adventure Time | Entertainment |
| SCDO | Scooby-Doo | Entertainment |
| PPUF | The Powerpuff Girls | Entertainment |
| LTOO | Looney Tunes | Entertainment |
| IRON | Iron Maiden | Music |
| FRND | Friends (TV Show) | Entertainment |

**⚠️ IMGC Rule:** IMGC prefix = college sports. ALWAYS resolve to full institution name.
`IMGCUAL` → "University of Alabama" NOT "IMGCUAL"

---

## Step 2: Title Format (MANDATORY)

```
{License/Brand Name} {Collection/Character} Official {Case Type} for {Full Device Name} | {Key Feature}
```

### Good examples:
✅ `Naruto Shippuden Akatsuki Iconic Official Hybrid MagSafe Case for iPhone 17 Pro Max | Military Grade Protection`
✅ `Real Madrid CF Retro 99/00 Official Hybrid MagSafe Case for Samsung Galaxy S24 Ultra | Military Grade Protection`
✅ `University of Oklahoma Boomer Sooner Official Hybrid MagSafe Case for iPhone 16 | Military Grade Protection`
✅ `Chelsea FC Crest Official Hybrid MagSafe Case for iPhone 15 Pro | Military Grade Protection`

### Bad examples:
❌ `RMCFRET Case for IPH17PMAX` — never use codes
❌ `IMGCUOK Black Marble Case` — not a title, no brand name
❌ `Head Case Designs Phone Case` — generic, useless

### Title Rules:
- **Max 200 characters** (Shopify limit), aim for 80-120
- **License/Brand FIRST** — SEO priority
- **"Official"** always included — signals authenticity
- **Full device name** — never device codes
- **Key feature after pipe** — consistent: "Military Grade Protection" for HTPCR/HB401

---

## Step 3: Case Type Display Names

| SKU Code | Title Name | Description Name |
|---|---|---|
| HTPCR | Hybrid MagSafe Case | hybrid TPU and PC hard back case with MagSafe compatibility |
| HB401 | Hybrid Hard MagSafe Case | reinforced hybrid case with MagSafe and military-grade protection |
| HLBWH | Leather Wallet Case | premium leather wallet case with card slots and magnetic closure |
| HB6CR | Clear MagSafe Case | crystal-clear case with integrated MagSafe ring |
| HB7BK | Black MagSafe Case | sleek black case with embedded MagSafe magnets |
| HDMWH | Desk Mat | large-format gaming and office desk mat |
| H8939 | Vinyl Skin | precision-cut vinyl gaming skin |

---

## Step 4: Description Structure (MANDATORY)

Every product needs a description. No exceptions.

```html
<div class="product-description">
  <p><strong>{Hero sentence — what makes this design/collection special. 1-2 sentences.}</strong></p>
  
  <h3>Features</h3>
  <ul>
    <li>Officially Licensed {Full Brand Name} product</li>
    <li>{Feature 1 from case type template below}</li>
    <li>{Feature 2}</li>
    <li>{Feature 3}</li>
    <li>Designed and printed by Head Case Designs — 8M+ cases sold worldwide</li>
    <li>Precision fit for {Full Device Name}</li>
  </ul>
  
  <h3>About the Design</h3>
  <p>{2-3 sentences about the specific design/artwork/collection. Reference characters, moments, or aesthetic.}</p>
</div>
```

### HTPCR Feature Bullets:
- TPU bumper + PC hard back — dual-material shock protection
- Integrated magnetic ring — MagSafe compatible for wireless charging and accessories
- Military-grade drop protection with shock-absorbing edges
- Raised bezels protect screen and camera lens
- High-resolution UV-printed scratch-resistant graphics

### HB401 Feature Bullets:
- Reinforced hybrid construction — TPU bumper + hard PC back
- Integrated MagSafe magnetic ring for accessories and wireless charging
- Enhanced impact resistance with reinforced corner protection
- Raised camera ring and screen lip — full-perimeter protection
- Premium UV-printed graphics, scratch-resistant finish

### HLBWH Feature Bullets:
- Premium faux leather exterior with inner card slots (2-3 cards)
- Magnetic closure keeps phone secure
- Folds out as a hands-free viewing stand
- Full 360° protection when closed
- Compatible with wireless charging (fold cover back)

---

## Step 5: Design-Specific Hero Copy Templates

### Naruto:
> "Join the Hidden Leaf with our officially licensed Naruto Shippuden collection. Featuring iconic artwork from the beloved anime series, this case brings your favourite character to life in stunning detail."

### Real Madrid CF:
> "Show your passion for Los Blancos with this officially licensed Real Madrid CF case. Premium quality meet football heritage — wear your club's colours with pride."

### Harry Potter:
> "Immerse yourself in the wizarding world with officially licensed Harry Potter artwork. Perfect for fans who want to carry a piece of Hogwarts with them."

### NBA:
> "Rep your team with this officially licensed NBA case. Premium graphics celebrate your favourite franchise in style."

*(Add one template per major license — Echo generates these at scale)*

---

## Step 6: Inventory Settings (MANDATORY)

| Field | Value | Reason |
|---|---|---|
| `Inventory policy` | `shopify` (tracked) | Required for orders |
| `Quantity` | `9999` | Print-on-demand — never truly out of stock |
| `Continue selling when out of stock` | `true` | Backup — always allow orders |

**Never set inventory to 0. 0 = product appears out of stock = no sales.**

---

## Step 7: SEO / Meta Fields (MANDATORY)

Every product needs:

**SEO Title:**
```
{License Name} {Design Name} {Case Type} for {Device} — Head Case Designs
```
Max 60 chars ideally, 70 max.

**SEO Description:**
```
Official {License Name} {Case Type} for {Full Device Name}. {Key feature}. 
Shop Head Case Designs — officially licensed, 8M+ cases sold worldwide.
```
Max 320 chars. Front-load keywords.

---

## Step 8: Product Tags (MANDATORY)

Every product must have tags for Shopify collections and filtering:

```
{license name}, {character/design name}, {case type}, {device brand}, 
{device model}, official, licensed, head case designs, {product type}
```

**Example for Naruto Akatsuki HTPCR iPhone 17 Pro Max:**
```
naruto, naruto shippuden, akatsuki, hybrid case, magsafe case, iphone, 
iphone 17 pro max, official, licensed, head case designs, phone case, anime
```

---

## Step 9: Pre-Upload Checklist

Before any batch is uploaded, run this checklist on a sample of 5 random products:

- [ ] Title starts with full brand/license name (not a code)
- [ ] Title includes full device name (not device code)
- [ ] Title includes case type in human language
- [ ] Description has hero paragraph
- [ ] Description has feature bullets (case-type specific)
- [ ] Description has "About the Design" paragraph
- [ ] Inventory = 9999
- [ ] Continue selling = true
- [ ] SEO title field populated
- [ ] SEO description field populated
- [ ] Tags populated with license, character, device, case type
- [ ] Product type field set correctly

**If any item fails the checklist: STOP. Fix the generator. Do not upload.**

---

## Content Generation Pipeline

```
1. Parse SKU → extract: product_type, device_code, design_code, variant
2. Resolve design_code → brand name (lookup table above)
3. Resolve device_code → full device name (device_code_map.json)
4. Resolve product_type → case type display name
5. Build title from template
6. Generate description: hero copy (design-specific) + feature bullets (type-specific) + design paragraph
7. Set inventory: 9999, continue_selling: true
8. Build SEO title + description
9. Build tags
10. QA check on sample → if pass, export CSV → upload
```

**Echo (Sonnet 4.6) generates hero copy and design paragraphs at batch scale.**
**Everything else is template-based — no AI needed.**

---

## Step 10: Image Rules (MANDATORY)

**Image CDN base:** `https://elcellonline.com/atg/`
**Pattern:** `/atg/{design_code}/{variant}/{prefix}-{device_code}-{position}.jpg`

### Product Type → Image Prefix
| Product Type | Prefix |
|---|---|
| HTPCR / FHTPCR | TP-CR |
| HB401 / FHB401 | HB-01 |
| HLBWH / FHLBWH | LB-WH |
| HC / FHC | HC-CR |
| HB6CR | H6-CR |
| HB7BK | H7-BK |

### Required Image Set Per Product (minimum 4 images)

Each Shopify product must include ALL of the following that exist:

| # | Image | URL Pattern | Purpose |
|---|---|---|---|
| 1 | **Hero — front of case** | `.../TP-CR-{DEVICE}-1.jpg` | Main listing image |
| 2 | **Secondary angle** | `.../TP-CR-{DEVICE}-2.jpg` | Second product view |
| 3 | **Background version** | `.../TP-CR-{DEVICE}-1b.jpg` | Styled with background |
| 4 | **Feature group** | `.../staticimages/features/2020/combined/TP-CR-{DEVICE}-{n}.jpg` | Shows case features (drop test, MagSafe etc.) |
| 5 | **Lifestyle / in-use** | Any lifestyle from design folder | Aspirational |

### Image URL Example (NARUICO-AKA, HTPCR, iPhone 17 Pro Max)
```
https://elcellonline.com/atg/NARUICO/AKA/TP-CR-IPH17PMAX-1.jpg   ← Hero
https://elcellonline.com/atg/NARUICO/AKA/TP-CR-IPH17PMAX-2.jpg   ← Secondary
https://elcellonline.com/atg/NARUICO/AKA/TP-CR-IPH17PMAX-1b.jpg  ← With background
https://elcellonline.com/atg/staticimages/features/2020/combined/TP-CR-IPH17PMAX-1.jpg ← Features
```

### Image Loading Rules
1. **Always attempt position 1, 2, and 1b first** — these are design-specific
2. **Check if URL returns 200 before including it** — don't add broken image links
3. **Feature images are shared** — same URL across all designs for the same device + product type
4. **Minimum 1 image required** — if hero (position 1) doesn't exist, skip the product and flag it
5. **Max 10 images per Shopify product** — don't need more than that

### Image Validation Script Logic
```python
import requests

def get_product_images(design_code, variant, product_type, device_code):
    PREFIX_MAP = {
        'HTPCR': 'TP-CR', 'HB401': 'HB-01', 'HLBWH': 'LB-WH',
        'HC': 'HC-CR', 'HB6CR': 'H6-CR', 'HB7BK': 'H7-BK',
    }
    prefix = PREFIX_MAP.get(product_type, 'TP-CR')
    base = f"https://elcellonline.com/atg/{design_code}/{variant}"
    feature_base = f"https://elcellonline.com/atg/staticimages/features/2020/combined"
    
    candidates = [
        f"{base}/{prefix}-{device_code}-1.jpg",      # Hero
        f"{base}/{prefix}-{device_code}-2.jpg",      # Secondary  
        f"{base}/{prefix}-{device_code}-1b.jpg",     # With background
        f"{feature_base}/{prefix}-{device_code}-1.jpg",  # Feature shot
    ]
    
    valid = []
    for url in candidates:
        try:
            r = requests.head(url, timeout=3)
            if r.status_code == 200:
                valid.append(url)
        except:
            pass
    return valid  # Returns only images that actually exist
```

**The previous upload only used position 1. This is why products look bare. Fix: regenerate image list using validation script for all products.**

---

## What to Fix in the Existing Shopify Products

The March 2026 upload needs to be corrected:

| Issue | Fix |
|---|---|
| Titles with raw codes | Regenerate all titles using this SOP |
| Missing descriptions | Generate descriptions for all products using templates |
| Inventory = 0 | Bulk update all variants to 9999 |
| Missing SEO fields | Populate for all products |
| Missing tags | Add license, design, device, case type tags |

**This is a bulk fix job for Pixel (Gemini Flash) or Codex.**

---

*SOP v1.0 — 2026-04-06 | Back to drawing board, done properly this time.*
