# AI-Powered Artwork Placement — Gemini Vision POC

**Created:** 2026-02-01
**Status:** Concept Design
**Key Tech:** Gemini (Nano Banana Pro) + Photoshop Scripting

---

## The Problem

**Steps 1 & 2 are the bottleneck:**
- Manual artwork placement takes 15-30 min per design
- Requires judgment: "will this logo cross a seam?"
- Repetitive across 5+ products per design
- Human error: misaligned key art, obscured logos

**Current manual process:**
```
Raw Artwork → Human reviews → Manually positions in each template → Checks seams → Adjusts → Repeats for each product
```

---

## The Solution: Gemini-Guided Batch Placement

**New AI-assisted process:**
```
Raw Artwork → Gemini analyzes key elements → Calculates optimal placement per product → Auto-positions in templates → Human QC (optional)
```

---

## How It Works

### Step 1: Artwork Analysis

Feed Gemini the raw design:

```
PROMPT:
"Analyze this artwork for console skin placement. Identify:
1. Key focal points (logos, faces, text, brand marks)
2. Pattern repeat areas (safe to crop/tile)
3. Critical elements that must remain visible
4. Suggested focal center point (x%, y%)

Return as JSON."
```

**Gemini Response:**
```json
{
  "focalPoints": [
    {"type": "logo", "x": 45, "y": 30, "width": 20, "height": 15, "priority": "critical"},
    {"type": "character_face", "x": 60, "y": 50, "width": 25, "height": 30, "priority": "high"}
  ],
  "patternAreas": [
    {"x": 0, "y": 0, "width": 100, "height": 20, "type": "tileable"}
  ],
  "suggestedCenter": {"x": 52, "y": 45},
  "safeMargins": {"top": 10, "bottom": 5, "left": 8, "right": 8}
}
```

### Step 2: Template Constraint Mapping

Each product has predefined danger zones:

```json
{
  "PS5SCS": {
    "seams": [
      {"x1": 48, "y1": 0, "x2": 52, "y2": 100, "type": "vertical_seam"},
      {"x1": 0, "y1": 45, "x2": 100, "y2": 55, "type": "horizontal_fold"}
    ],
    "safeZones": [
      {"x": 10, "y": 60, "width": 30, "height": 20, "label": "logo_safe"}
    ],
    "dimensions": {"width": 3000, "height": 2000}
  }
}
```

### Step 3: Placement Calculation

```
PROMPT:
"Given this artwork analysis and PS5SCS template constraints, calculate optimal placement:

Artwork focal points: [logo at 45%,30%, face at 60%,50%]
Template seams: [vertical at 48-52%, horizontal fold at 45-55%]
Safe zones: [logo area at 10%,60%]

Requirements:
- Logo must not cross any seam
- Face should be fully visible
- Maintain aspect ratio
- Allow 5% bleed on edges

Return: scale factor, x_offset, y_offset, rotation (if needed)"
```

**Gemini Response:**
```json
{
  "placement": {
    "scale": 1.15,
    "x_offset": -3,
    "y_offset": 8,
    "rotation": 0
  },
  "validation": {
    "logo_visible": true,
    "logo_seam_clear": true,
    "face_visible": true,
    "bleed_ok": true
  },
  "confidence": 0.94
}
```

### Step 4: Batch Apply to Photoshop

JSX script reads placement data and applies:

```javascript
// Apply Gemini-calculated placement
var placement = loadPlacement(designCode, productCode);

var artLayer = doc.artLayers.getByName("artwork");
artLayer.resize(placement.scale * 100, placement.scale * 100, AnchorPosition.MIDDLECENTER);
artLayer.translate(placement.x_offset, placement.y_offset);
if (placement.rotation !== 0) {
    artLayer.rotate(placement.rotation, AnchorPosition.MIDDLECENTER);
}
```

---

## Implementation Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        BATCH PROCESSOR                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Raw Artwork  │───▶│   Gemini     │───▶│  Placement   │      │
│  │   Folder     │    │   Vision     │    │    JSON      │      │
│  └──────────────┘    │  Analysis    │    └──────┬───────┘      │
│                      └──────────────┘           │              │
│                                                 │              │
│  ┌──────────────┐    ┌──────────────┐          │              │
│  │  Template    │───▶│  Constraint  │──────────┤              │
│  │  Configs     │    │   Mapper     │          │              │
│  └──────────────┘    └──────────────┘          │              │
│                                                 │              │
│                      ┌──────────────┐          │              │
│                      │  Photoshop   │◀─────────┘              │
│                      │   Script     │                          │
│                      └──────┬───────┘                          │
│                             │                                  │
│                      ┌──────▼───────┐                          │
│                      │   Mockups    │                          │
│                      │   Output     │                          │
│                      └──────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Test: Nano Banana Pro

We can test this concept immediately using the skill:

```bash
# 1. Analyze artwork
clawdbot skill nano-banana-pro analyze \
  --image "raw_artwork.jpg" \
  --prompt "Identify key focal points for console skin placement..."

# 2. Calculate placement  
clawdbot skill nano-banana-pro calculate \
  --context "artwork_analysis.json" \
  --template "PS5SCS_constraints.json" \
  --prompt "Calculate optimal placement..."
```

---

## POC Script: analyze_artwork.js

```javascript
// Node.js script to analyze artwork via Gemini

const fs = require('fs');
const path = require('path');

async function analyzeArtwork(imagePath) {
    // Load image as base64
    const imageBuffer = fs.readFileSync(imagePath);
    const base64Image = imageBuffer.toString('base64');
    
    // Call Gemini via Nano Banana Pro
    const prompt = `
    Analyze this artwork for gaming console skin placement.
    
    Identify and return as JSON:
    1. "focalPoints": array of {type, x_percent, y_percent, width_percent, height_percent, priority}
       - Types: logo, text, character_face, brand_mark, pattern_center
       - Priority: critical, high, medium, low
    2. "patternAreas": areas safe to crop/tile
    3. "suggestedCenter": optimal center point for scaling
    4. "dominantColors": top 3 hex colors
    5. "artworkType": photo, illustration, pattern, mixed
    
    Coordinates as percentages (0-100) from top-left.
    `;
    
    // ... API call to Gemini
    
    return analysisResult;
}

async function calculatePlacement(analysis, templateConstraints) {
    const prompt = `
    Given artwork analysis and template constraints, calculate optimal placement.
    
    ARTWORK:
    ${JSON.stringify(analysis, null, 2)}
    
    TEMPLATE (${templateConstraints.productCode}):
    - Dimensions: ${templateConstraints.width}x${templateConstraints.height}
    - Seams (AVOID): ${JSON.stringify(templateConstraints.seams)}
    - Safe zones: ${JSON.stringify(templateConstraints.safeZones)}
    
    RULES:
    - Critical focal points must NOT cross seams
    - Maintain artwork aspect ratio
    - Allow 5% bleed on all edges
    - Prefer centering unless it conflicts with seams
    
    Return JSON: {scale, x_offset, y_offset, rotation, confidence, warnings}
    `;
    
    // ... API call to Gemini
    
    return placementResult;
}

// Batch process all artwork in folder
async function batchProcess(artworkFolder, outputFolder) {
    const artworks = fs.readdirSync(artworkFolder).filter(f => /\.(jpg|png|psd)$/i.test(f));
    
    const products = ['PS5SCS', 'PS5SDCS', 'DS5EGCT', 'STMDECK'];
    const results = {};
    
    for (const artwork of artworks) {
        const designCode = path.parse(artwork).name;
        results[designCode] = {};
        
        // Analyze once
        const analysis = await analyzeArtwork(path.join(artworkFolder, artwork));
        
        // Calculate placement for each product
        for (const product of products) {
            const constraints = loadTemplateConstraints(product);
            const placement = await calculatePlacement(analysis, constraints);
            results[designCode][product] = placement;
        }
    }
    
    // Save placement map
    fs.writeFileSync(
        path.join(outputFolder, 'placements.json'),
        JSON.stringify(results, null, 2)
    );
    
    return results;
}

module.exports = { analyzeArtwork, calculatePlacement, batchProcess };
```

---

## Expected Time Savings

| Step | Current | With AI |
|------|---------|---------|
| Analyze artwork | 5 min | 10 sec |
| Position in PS5SCS | 8 min | 5 sec |
| Position in DS5EGCT | 6 min | 5 sec |
| Position in other products | 15 min | 15 sec |
| QC check | 5 min | 3 min |
| **Total per design** | **39 min** | **~4 min** |

For a lineup of 5 designs × 4 products = **20 placements**
- Current: ~3 hours
- With AI: ~20 minutes

---

## Next Steps

1. **Create template constraint files** for each product (seam maps, safe zones)
2. **Test Gemini analysis** on sample artwork
3. **Build placement calculator** prompt
4. **Create Photoshop script** to apply placements
5. **Integrate into batch workflow**

---

## Questions for Cem

1. Do we have seam/cutline diagrams for each product?
2. Are there "golden rules" for logo placement we should encode?
3. Should AI flag for human review, or auto-apply if confidence > 90%?
4. Priority products to start with?
