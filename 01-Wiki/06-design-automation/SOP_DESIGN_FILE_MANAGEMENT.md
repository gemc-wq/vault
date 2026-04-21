# SOP: Design File Management & Automation
*Version: DRAFT 0.1 | Created: 2026-02-11 | Status: IN DEVELOPMENT*

---

## Purpose
Standard operating procedure for managing design files (PSD/EPS/TIFF), template mapping, and automated print file generation.

---

## Design File Types

| Format | Purpose | Tool | Typical Size |
|--------|---------|------|-------------|
| PSD | Master design files | Adobe Photoshop | ~128MB |
| EPS | Vinyl skin print files | Adobe Illustrator | Varies |
| TIFF | Flatbed jig layouts | Printer software | Large |
| AI | Illustrator source files | Adobe Illustrator | Varies |

---

## SKU-to-Design Mapping

```
SKU: HTPCR-IPH16-HPOTDH37-HOP
      │      │      │       │
      │      │      └───────┴── Design code + variant → digital file lookup
      │      └── Device model → template selection
      └── Product type → production method
```

### Lookup Chain
1. **Product Type** → determines print method (UV / vinyl / laser)
2. **Device Model** → determines physical template (cutout positions, dimensions)
3. **Design Code** → finds the source design file (PSD/EPS)
4. **Variant** → selects specific version of the design

---

## Template Management

### Device Templates
Every `Product Type + Device Model` combination has a production template:
- Template defines: printable area, cutout positions (camera, buttons, ports), bleed zones
- Stored as: `Template_Map` table in database
- Example: `HTPCR-IPH16` → `Template_V2_Phone_Large`

### Camera Hole Challenge ⚠️
- Each phone model has different camera cutout positions
- Design must be placed to avoid obstruction
- Current script sometimes fails → manual fix required
- **New devices = new templates = potential for new issues**

---

## Current Process (Manual — 3 staff daily)

1. Receive shipped label list (Excel from Veco)
2. Extract SKU list from labels
3. Decompose each SKU to identify design file
4. Locate source design file in storage
5. Open in Photoshop/Illustrator
6. Place design into device-specific template
7. Check for camera hole / cutout conflicts
8. Export production-ready file (TIFF for jig, EPS for skins)
9. Nest EPS files for vinyl skin print jobs
10. Organize by jig layout / alphabetical by device

**Peak season:** 4 staff on this process

---

## Target Process (Hybrid Automation)

### Automated (80% of orders)
1. SKU decomposed automatically (Supabase lookup)
2. Design file retrieved from storage (API/S3)
3. Template matched automatically
4. Design placed into template programmatically
5. Standard cutouts handled by predefined rules
6. Production file exported and queued

### AI-Assisted (15% of orders)
- Gemini Vision checks design placement
- Detects camera hole / cutout conflicts
- Suggests repositioning or flags for review
- Validates output quality

### Manual Review (5% of orders)
- Custom/personalized products
- New devices without templates
- Complex designs that AI cannot resolve
- Edge cases flagged by the system

---

## Storage Architecture

### Current
- Design files stored in cloud (tiered: high-frequency vs archive)
- *Details needed from Cem on exact storage setup*

### Target
- **Hot cache:** Pre-rendered production files for high-volume designs (e.g., LFC, Harry Potter)
- **Warm storage:** All standard designs, retrieved on demand
- **Archive:** Legacy/discontinued designs
- **Supabase:** Metadata, SKU-to-file mapping, template registry

### Flattening Cache
High-volume designs pre-rendered into production-ready files:
- Reduces per-order processing from ~30s (PSD render) to <1s (retrieval)
- Top sellers: Naruto, LFC, Peanuts, Harry Potter, Brighton FC

---

## Documentation Needed
- [ ] EPS workflow documentation (Google Drive shared folder)
- [ ] Camera hole obstruction examples (before/after)
- [ ] Current script/tool used for print file generation
- [ ] Storage structure for design files
- [ ] Template creation process for new devices

---

*This SOP will be expanded as we receive EPS workflow docs and examples of current failures.*
