# Antigravity Frontend Specification
## AI-Powered Artwork Placement Tool

---

## Overview

A web interface for batch processing console skin artwork placement using Gemini Vision AI.

---

## Core Flow

```
Upload Artwork → AI Analyzes → Calculate Placements → Preview → Export
```

---

## API Endpoints Needed

### 1. Analyze Artwork
```
POST /api/artwork/analyze
Content-Type: multipart/form-data

Body:
- file: [image file]
- design_code: string (optional)

Response:
{
  "analysis_id": "uuid",
  "design_name": "Miraculous Heroez",
  "artwork_type": "character_collage",
  "key_elements": [...],
  "thumbnail_url": "/uploads/xxx_thumb.jpg"
}
```

### 2. Calculate Placements
```
POST /api/placement/calculate
Content-Type: application/json

Body:
{
  "analysis_id": "uuid",
  "products": ["PS5SCS", "PS5SDCS", "DS5EGCT"],
  "options": {
    "auto_apply_threshold": 0.9,
    "prefer_logo_position": "lower_third"
  }
}

Response:
{
  "job_id": "uuid",
  "placements": {
    "PS5SCS": {
      "transform": {"scale": 1.15, "x_offset": 3, "y_offset": -2},
      "confidence": 0.94,
      "preview_url": "/previews/xxx_PS5SCS.jpg"
    },
    ...
  }
}
```

### 3. Export Placements
```
GET /api/placement/export/{job_id}?format=json|jsx|psd

Response (format=json):
{
  "placements": {...},
  "photoshop_instructions": [...]
}

Response (format=jsx):
// Downloadable Photoshop script
```

---

## UI Components

### 1. Upload Zone
```jsx
<UploadZone
  accept="image/*,.psd"
  multiple={true}
  onUpload={handleAnalyze}
>
  <p>Drop artwork files here</p>
  <p>Supports: JPG, PNG, PSD</p>
</UploadZone>
```

### 2. Product Selector
```jsx
<ProductSelector
  products={[
    { code: 'PS5SCS', name: 'PS5 Console', icon: '🎮' },
    { code: 'PS5SDCS', name: 'PS5 Slim', icon: '🎮' },
    { code: 'DS5EGCT', name: 'Controller', icon: '🕹️' },
    { code: 'STMDECK', name: 'Steam Deck', icon: '🎲' }
  ]}
  selected={selectedProducts}
  onChange={setSelectedProducts}
/>
```

### 3. Analysis Results
```jsx
<AnalysisResults
  elements={[
    { type: 'logo', position: {x: 50, y: 70}, priority: 'critical' },
    { type: 'character', position: {x: 30, y: 40}, priority: 'high' }
  ]}
  warnings={['Logo near seam boundary']}
/>
```

### 4. Placement Preview
```jsx
<PlacementPreview
  product="PS5SCS"
  originalImage={artworkUrl}
  transform={{ scale: 1.15, x: 3, y: -2 }}
  dangerZones={templateConstraints.PS5SCS.danger_zones}
  safeZones={templateConstraints.PS5SCS.safe_zones}
  showOverlay={true}
/>
```

### 5. Batch Results Table
```jsx
<BatchResults
  jobs={[
    { 
      design: 'MIRACAR_HPA',
      products: {
        PS5SCS: { status: 'complete', confidence: 0.94 },
        DS5EGCT: { status: 'complete', confidence: 0.91 }
      }
    }
  ]}
  onExport={handleExport}
  onApplyAll={handleApplyAll}
/>
```

---

## State Management

```typescript
interface AppState {
  // Uploads
  uploads: UploadedArtwork[];
  currentAnalysis: ArtworkAnalysis | null;
  
  // Products
  selectedProducts: ProductCode[];
  templateConstraints: TemplateConstraints;
  
  // Placements
  placements: Map<string, ProductPlacement>;
  batchJobs: BatchJob[];
  
  // UI
  isProcessing: boolean;
  errors: string[];
}
```

---

## Gemini Integration

### Option A: Direct API Call
```typescript
async function analyzeWithGemini(imageBase64: string): Promise<Analysis> {
  const response = await fetch('https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${GEMINI_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      contents: [{
        parts: [
          { text: ANALYSIS_PROMPT },
          { inline_data: { mime_type: 'image/jpeg', data: imageBase64 }}
        ]
      }]
    })
  });
  
  return parseGeminiResponse(await response.json());
}
```

### Option B: Via Nano Banana Pro Skill
```typescript
async function analyzeViaNanaBanana(imagePath: string): Promise<Analysis> {
  const result = await clawdbot.skill('nano-banana-pro').run({
    image: imagePath,
    prompt: ANALYSIS_PROMPT
  });
  
  return JSON.parse(result.text);
}
```

---

## File Structure

```
antigravity-placement-tool/
├── src/
│   ├── components/
│   │   ├── UploadZone.tsx
│   │   ├── ProductSelector.tsx
│   │   ├── AnalysisResults.tsx
│   │   ├── PlacementPreview.tsx
│   │   └── BatchResults.tsx
│   ├── api/
│   │   ├── gemini.ts
│   │   └── photoshop.ts
│   ├── hooks/
│   │   ├── useAnalysis.ts
│   │   └── usePlacements.ts
│   ├── data/
│   │   └── template_constraints.json
│   └── App.tsx
├── public/
│   └── templates/
│       ├── PS5SCS_overlay.png
│       ├── DS5EGCT_overlay.png
│       └── ...
└── package.json
```

---

## MVP Scope

### Phase 1 (Week 1)
- [ ] Single image upload
- [ ] Gemini analysis integration
- [ ] Display detected elements
- [ ] Single product placement calculation

### Phase 2 (Week 2)
- [ ] Multi-product selection
- [ ] Preview with danger zone overlay
- [ ] Export placement JSON

### Phase 3 (Week 3)
- [ ] Batch upload support
- [ ] Photoshop script export
- [ ] Progress tracking

### Phase 4 (Week 4)
- [ ] Confidence threshold auto-apply
- [ ] Manual adjustment UI
- [ ] Integration with existing PSD workflow
