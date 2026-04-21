# Console Skin Replication — Improved Workflow POC

**Created:** 2026-02-01
**Status:** Proof of Concept
**Author:** Harry (AI Assistant)

---

## Executive Summary

This document outlines an improved, more automated workflow for console skin replication based on analysis of:
- Current JSX script (`New_Skins_Consoles-2.jsx`)
- Step-by-step PDF guide
- Pipeline diagram from Gemini POC

**Goal:** Reduce manual touchpoints from ~12 steps to ~3, with validation and error prevention built-in.

---

## Current Workflow Pain Points

| Issue | Impact | Root Cause |
|-------|--------|------------|
| Manual lineup entry | Human error, slow | Dialog-based input |
| Hardcoded Windows paths | Not portable to Mac | Script design |
| No validation before run | Wasted time on failures | Missing checks |
| Design code mismatch | Export errors | Manual naming |
| No progress visibility | Anxiety, can't multitask | Silent processing |

---

## Proposed Improvements

### 1. Config-Driven Processing

Replace hardcoded paths and lineup data with a JSON config:

```json
{
  "workspace": {
    "mac": "/Users/clawdbot/Replication",
    "windows": "C:/Replication"
  },
  "paths": {
    "psd": "{{workspace}}/PSD",
    "assets": "{{workspace}}/Assets", 
    "output": "{{workspace}}/Output",
    "mockups": "{{workspace}}/Mockups"
  },
  "products": [
    {"code": "PS5SCS", "name": "PS5 Standard Console Skin", "action": "NEWSKIN"},
    {"code": "PS5SDCS", "name": "PS5 Slim Digital Console Skin", "action": "NEWSKIN"},
    {"code": "DS5EGCT", "name": "DualSense Edge Controller", "action": "NEWSKIN"},
    {"code": "ASROGA", "name": "Asus ROG Ally", "action": "NEWSKIN"},
    {"code": "STMDECK", "name": "Steam Deck", "action": "NEWSKIN"}
  ],
  "printers": ["CAT", "HPA", "LAD"],
  "exportQuality": 80
}
```

### 2. Google Sheets Integration

Auto-pull lineup data from the Creative tracker:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Google Sheet   │────▶│  Sync Script     │────▶│  Local Config   │
│  (Design Codes) │     │  (Node.js/Python)│     │  (lineups.json) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

**Benefits:**
- Creative updates tracker → Replication auto-syncs
- No manual typing of lineup names
- Version history in Google Sheets

### 3. Pre-Flight Validation

Before processing, verify:

```javascript
// Validation checklist
✓ PSD file exists for each product type
✓ Smart Object structure intact (not flattened)
✓ Design group count matches tracker
✓ Group names follow convention (001_CODE_NAME)
✓ Assets folder has required display.psd files
✓ Output folder is writable
✓ Photoshop actions installed (NEWSKIN, etc.)
```

**On failure:** Generate detailed error report, don't run.

### 4. Progress Dashboard

Real-time status via Slack/Telegram:

```
🚀 Starting: MIRACAR lineup (5 designs × 4 products)
├── ✅ PS5SCS: LAD, CAT, HPA exported
├── ✅ DS5EGCT: LAD, CAT, HPA exported  
├── 🔄 PS5SDCS: Processing CAT...
├── ⏳ STMDECK: Queued
└── 📊 Progress: 12/20 (60%)

Estimated completion: 8 minutes
```

### 5. Automated Folder Watching

No manual trigger needed:

```
┌─────────────────────┐
│  Creative drops     │
│  raw PSD in folder  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Watcher detects    │
│  new file           │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Auto-validate      │
│  + process          │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Notify completion  │
│  via Slack/Telegram │
└─────────────────────┘
```

---

## Implementation Phases

### Phase 1: Cross-Platform Config (Week 1)
- [ ] Create config.json structure
- [ ] Update JSX to read config
- [ ] Support Mac + Windows paths
- [ ] Test on iMac with sample files

### Phase 2: Validation Layer (Week 2)
- [ ] Pre-flight check script
- [ ] Error reporting
- [ ] Photoshop action installer script

### Phase 3: Google Sheets Sync (Week 3)
- [ ] Sheets API integration
- [ ] Auto-generate lineups.json
- [ ] Cron job for periodic sync

### Phase 4: Progress & Notifications (Week 4)
- [ ] Slack/Telegram webhook integration
- [ ] Real-time progress updates
- [ ] Completion summaries with thumbnails

### Phase 5: Folder Watching (Week 5)
- [ ] Node.js watcher service
- [ ] Auto-trigger on new files
- [ ] Queue management for multiple lineups

---

## Modernized Script Structure

```javascript
// New_Skins_Consoles_v3.jsx

#target photoshop
#include "lib/config-loader.jsx"
#include "lib/validator.jsx"
#include "lib/progress-reporter.jsx"

// Load config (auto-detects OS)
var config = ConfigLoader.load();
var lineup = ConfigLoader.getLineupFromArgs() || showLineupDialog();

// Pre-flight validation
var validation = Validator.check(config, lineup);
if (!validation.ok) {
    ProgressReporter.error(validation.errors);
    exit();
}

ProgressReporter.start(lineup);

// Process each product
config.products.forEach(function(product) {
    ProgressReporter.update(product.code, "processing");
    
    var psdFile = new File(config.paths.psd + "/" + product.code + ".psd");
    if (!psdFile.exists) {
        ProgressReporter.skip(product.code, "PSD not found");
        return;
    }
    
    processProduct(product, lineup, config);
    ProgressReporter.update(product.code, "complete");
});

ProgressReporter.complete();
```

---

## Quick Win: Updated Script for Mac

Here's an immediately usable Mac-compatible version:

```javascript
// Set these for your Mac setup
var psdPath = '/Users/clawdbot/Desktop/Replication Process Sample Files/PSD/';
var savePath = '/Users/clawdbot/Desktop/Replication Process Sample Files/Output/';
var assetPath = '/Users/clawdbot/Desktop/Replication Process Sample Files/Assets/';

// ... rest of script with updated paths
```

---

## Metrics & Success Criteria

| Metric | Current | Target |
|--------|---------|--------|
| Time per lineup (5 designs) | ~45 min | ~10 min |
| Manual steps | 12 | 3 |
| Error rate | ~15% | <2% |
| Setup time for new product | 2 hours | 15 min |

---

## Next Steps

1. **Immediate:** Test current script on iMac with sample files
2. **This week:** Create Mac-compatible config version
3. **Next week:** Build validation layer
4. **Ongoing:** Iterate based on feedback

---

## Files Created

- `POC_IMPROVED_WORKFLOW.md` — This document
- `config-template.json` — Configuration template (coming)
- `New_Skins_Consoles_v3.jsx` — Modernized script (coming)
- `validator.jsx` — Pre-flight checks (coming)

---

*"The best automation is invisible — Creative drops files, mockups appear."*
