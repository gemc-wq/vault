# SEO & Content Rewrite Framework

> **Owner:** Ava + Echo (Sonnet 4.6) | **Created:** 2026-03-15
> **Purpose:** Standardize product titles, descriptions, and bullet points before Shopify/Walmart upload

---

## Problem

Current BigCommerce data has:
- ❌ Titles using internal device codes (IPH17PMAX) instead of full names (iPhone 17 Pro Max)
- ❌ Descriptions with 4 languages crammed into one HTML block (EN/DE/FR/IT)
- ❌ No case type in title (just "Case" — doesn't say Soft Gel vs Hard Case vs MagSafe)
- ❌ Generic SEO — missing license name prominence, no key features
- ❌ Amazon-style keyword stuffing in some, bare-bones in others

---

## Title Format Standard

### Phone Cases (HTPCR, HB401, HLBWH, HB6, HB7)
```
{License Name} {Design Name} Official {Case Type} for {Full Device Name} | {Key Feature}
```
**Example:**
```
Naruto Shippuden Akatsuki Official Soft Gel Case for iPhone 17 Pro Max | Military Grade Protection
```

**Rules:**
- License name first (brand recognition + SEO)
- Design name second (differentiator within license)
- "Official" — signals authenticity (licensed product)
- Case type = human-readable (not HTPCR → "Soft Gel Case")
- Full device name (not IPH17PMAX → "iPhone 17 Pro Max")
- Pipe separator before key feature
- Max 200 chars (Shopify limit), ideally 80-120 for clean display
- Walmart title max: 200 chars, should front-load key terms

### Desk Mats (HDM)
```
{License Name} {Design Name} Official Desk Mat | {Size} | Premium Non-Slip
```

### Gaming Skins (H89)
```
{License Name} {Design Name} Official Vinyl Skin for {Device} | Precision Cut, Easy Apply
```

---

## Case Type Display Names

| Code | Display Name | Short Name |
|------|-------------|------------|
| HTPCR | Hybrid MagSafe Case | MagSafe Case |
| HB401 | Hybrid Hard MagSafe Case | Hard MagSafe |
| HLBWH | Leather Wallet Case | Wallet Case |
| HB6 | Clear MagSafe Case | Clear MagSafe |
| HB7 | Black MagSafe Case | Black MagSafe |
| FHTPCR | Clear Soft Gel Case | Clear Gel |
| HA805 | MagSafe Soft Gel Case | MagSafe Gel |

---

## Device Code → Full Name Mapping

**Source:** BigCommerce custom field `DeviceModel` (most reliable)
**Fallback:** Build mapping table from known codes

| Code | Full Name |
|------|-----------|
| IPH17PMAX | iPhone 17 Pro Max |
| IPH17PRO | iPhone 17 Pro |
| IPH17 | iPhone 17 |
| IPH17AIR | iPhone Air |
| IPHSE4 | iPhone SE (4th Gen) |
| IPH16PMAX | iPhone 16 Pro Max |
| IPH16PRO | iPhone 16 Pro |
| S938U | Samsung Galaxy S25 Ultra |
| S936U | Samsung Galaxy S25+ |
| S931U | Samsung Galaxy S25 |
| A156 | Samsung Galaxy A16 |
| PIX9PRO | Google Pixel 9 Pro |
*(Expand from BC DeviceModel field — ~1,322 devices in catalog)*

---

## Description Structure

### Shopify Description (HTML)
```html
<div class="product-description">
  <p class="hero">{1-2 sentence hero copy — what makes this design special}</p>
  
  <h3>Features</h3>
  <ul>
    <li>Officially Licensed {License Name} product</li>
    <li>{Case-type-specific feature 1}</li>
    <li>{Case-type-specific feature 2}</li>
    <li>{Case-type-specific feature 3}</li>
    <li>Compatible with {Full Device Name}</li>
  </ul>
  
  <h3>About the Design</h3>
  <p>{Design-specific copy — 2-3 sentences about the artwork/collection}</p>
</div>
```

### Case-Type Feature Templates

**HTPCR (Hybrid MagSafe Case):**
- TPU bumper + PC hard back — dual-material protection
- Integrated magnetic ring — MagSafe compatible for wireless charging & accessories
- Military-grade drop protection with shock-absorbing edges
- Raised bezels protect screen and camera lens
- Slim profile, precise cutouts for all ports and buttons
- High-resolution scratch-resistant printed graphics

**HB401 (Hybrid Hard MagSafe Case):**
- TPU bumper + PC hard back — premium dual-material construction
- Integrated magnetic ring — MagSafe compatible
- Enhanced impact resistance with reinforced corners
- Raised camera ring and screen lip protection
- Lightweight yet durable — doesn't add bulk
- Scratch-resistant UV-printed graphics

**HLBWH (Leather Wallet):**
- Premium faux leather with card slots and cash pocket
- Magnetic closure keeps phone secure
- Converts to hands-free viewing stand
- Full 360° protection when closed

**HB6 (Clear MagSafe):**
- Crystal-clear case shows off your phone's design
- Built-in MagSafe ring for wireless charging
- Military-grade drop protection
- Anti-yellowing technology

**HB7 (Black MagSafe):**
- Sleek black finish with embedded MagSafe magnets
- Strong magnet alignment for accessories
- Enhanced grip texture
- Impact-resistant bumper edges

---

## Bullet Points (for Walmart / Amazon)

5 bullets per product:
1. **Officially Licensed** — Head Case Designs Officially Licensed {License} product
2. **Design** — {Design-specific feature or collection description}
3. **Protection** — {Case-type-specific protection feature}
4. **Quality** — High-resolution printed graphics, scratch-resistant
5. **Compatibility** — Designed specifically for {Full Device Name}

---

## SEO Meta Description
```
Official {License Name} {Design Name} {Case Type} for {Device}. 
{Key feature}. Shop Head Case Designs — 8M+ cases sold worldwide.
```
Max 320 chars. Front-load keywords.

---

## Content Generation Pipeline

```
BC Product Data (raw)
    ↓ extract: AmazonTitle, DesignName, BrandCode, DeviceModel, description
    ↓ map: device code → full name, product type → case type name
Echo Agent (Sonnet 4.6)
    ↓ input: raw data + template + rules above
    ↓ output: title, description HTML, 5 bullets, meta description
Quality Check (Ava review)
    ↓ spot-check 10% of batch
    ↓ flag: missing license name, wrong device, generic copy
Merge into Shopify CSV
    ↓ replace raw BC fields with Echo-rewritten content
Upload
```

### Batch Processing
- 50 designs per Echo batch (each design = ~10-15 devices = 500-750 products)
- Echo generates one template per design, we replicate across devices (only device name changes)
- Estimated: 200 designs × 1 Echo call each = 200 API calls
- Cost: ~$2-5 total (Sonnet 4.6 at ~$3/M input tokens)

---

## Implementation Steps

1. [ ] Build device code → full name mapping table (from BC DeviceModel field)
2. [ ] Create Echo prompt template with rules above
3. [ ] Test on 5 designs — review output quality
4. [ ] Batch process top 50 designs
5. [ ] Merge rewritten content into Shopify CSV generator
6. [ ] Cem reviews sample of 10 products before full upload
7. [ ] Scale to all 200+ champion designs

---

*This framework applies to ALL product groups (phone cases, desk mats, skins) and ALL marketplaces (Shopify/GoHeadCase, Walmart, OnBuy, Kaufland).*
