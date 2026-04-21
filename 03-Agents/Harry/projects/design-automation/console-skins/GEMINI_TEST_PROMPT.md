# Gemini Nano Banana Pro — Artwork Placement Prompt

## Manual Test Prompt

Copy this prompt and test with Nano Banana Pro. Attach the raw artwork image.

---

### PROMPT FOR ARTWORK ANALYSIS

```
You are an artwork placement specialist for gaming console skins. Analyze this design artwork and provide placement instructions.

TASK: Analyze the artwork and identify:

1. **KEY ELEMENTS** - Find all important visual elements:
   - Logos/brand marks (text or graphic)
   - Character faces (must not be cut off)
   - Important text/titles
   - Focal point of the design

2. **ELEMENT PRIORITIES**:
   - CRITICAL: Must be fully visible and centered (logos, titles)
   - HIGH: Should be visible but can be partially cropped (main characters)
   - MEDIUM: Nice to have visible (secondary characters, decorative elements)
   - LOW: Pattern/background elements (safe to crop)

3. **PLACEMENT ZONES**: For each product template, specify where the key elements should go:
   - PS5_CONSOLE: Two vertical plates (left + right). Logo typically goes lower third.
   - CONTROLLER: Touchpad (center-top), left grip, right grip. Logo on touchpad.

Return your analysis as JSON:

{
  "design_name": "detected name or description",
  "artwork_type": "character_collage | pattern | single_character | logo_centric",
  "key_elements": [
    {
      "type": "logo | character | text | pattern",
      "description": "what it is",
      "current_position": {"x_percent": 0-100, "y_percent": 0-100},
      "size_percent": {"width": 0-100, "height": 0-100},
      "priority": "critical | high | medium | low"
    }
  ],
  "placement_recommendations": {
    "PS5_CONSOLE": {
      "scale": 1.0,
      "x_offset_percent": 0,
      "y_offset_percent": 0,
      "logo_position": "lower_third | center | upper_third",
      "notes": "specific advice"
    },
    "CONTROLLER": {
      "scale": 1.0,
      "x_offset_percent": 0,
      "y_offset_percent": 0,
      "touchpad_element": "which element goes on touchpad",
      "notes": "specific advice"
    }
  },
  "warnings": ["any issues detected"]
}
```

---

### PROMPT FOR PLACEMENT CALCULATION (Step 2)

After analyzing, use this prompt with the template constraints:

```
You are calculating precise artwork placement for console skin production.

ARTWORK ANALYSIS:
[paste the JSON from step 1]

TEMPLATE CONSTRAINTS (PS5 Slim Digital Console):
{
  "product_code": "PS5SDCS",
  "dimensions": {"width": 3000, "height": 4000},
  "danger_zones": [
    {"name": "center_seam", "x1": 48, "x2": 52, "y1": 0, "y2": 100, "type": "vertical"},
    {"name": "top_curve", "x1": 0, "x2": 100, "y1": 0, "y2": 8, "type": "horizontal"},
    {"name": "bottom_cutout", "x1": 40, "x2": 60, "y1": 92, "y2": 100, "type": "avoid"}
  ],
  "safe_zones": [
    {"name": "logo_area_left", "x1": 10, "x2": 45, "y1": 65, "y2": 85},
    {"name": "logo_area_right", "x1": 55, "x2": 90, "y1": 65, "y2": 85}
  ],
  "bleed_required": 5
}

RULES:
1. Critical elements must NOT cross danger zones
2. Logo should be placed in one of the safe zones
3. Maintain aspect ratio of original artwork
4. Scale to fill template with required bleed
5. Character faces should not be cut by seams

Calculate optimal placement and return:

{
  "product_code": "PS5SDCS",
  "transform": {
    "scale_percent": 100-150,
    "x_offset_percent": -50 to +50,
    "y_offset_percent": -50 to +50,
    "rotation_degrees": 0
  },
  "element_positions": [
    {
      "element": "logo",
      "final_position": {"x": 0-100, "y": 0-100},
      "seam_clear": true/false,
      "in_safe_zone": true/false
    }
  ],
  "validation": {
    "all_critical_visible": true/false,
    "no_seam_conflicts": true/false,
    "bleed_adequate": true/false,
    "confidence": 0.0-1.0
  },
  "warnings": []
}
```

---

## Quick Test Checklist

1. Open Nano Banana Pro (or Gemini directly)
2. Upload a sample artwork (e.g., the Miraculous Heroez pattern)
3. Paste the ARTWORK ANALYSIS prompt
4. Review the JSON output
5. Paste the PLACEMENT CALCULATION prompt with constraints
6. Review the transform values
7. Manually verify in Photoshop if placement makes sense

---

## Expected Flow in Antigravity Frontend

```
┌─────────────────────────────────────────────────────────────┐
│                    ARTWORK PLACEMENT TOOL                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [UPLOAD ARTWORK]  [DROP ZONE]                              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │              [Artwork Preview]                      │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Select Products:                                           │
│  [x] PS5 Console    [x] PS5 Controller    [ ] Steam Deck   │
│                                                             │
│  [ANALYZE & CALCULATE]                                      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ RESULTS:                                            │   │
│  │                                                     │   │
│  │ PS5 Console:                                        │   │
│  │   Scale: 115% | Offset: +3%, -2% | ✓ Logo Safe     │   │
│  │   [Preview] [Apply to PSD]                          │   │
│  │                                                     │   │
│  │ PS5 Controller:                                     │   │
│  │   Scale: 108% | Offset: 0%, +5% | ✓ Logo Safe      │   │
│  │   [Preview] [Apply to PSD]                          │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [BATCH APPLY ALL]  [EXPORT PLACEMENT JSON]                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
