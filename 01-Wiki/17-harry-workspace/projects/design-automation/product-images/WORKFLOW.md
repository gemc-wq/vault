# Product Image Generation Workflow

**Purpose:** Create marketplace listing images (multiview mockups) for phone/controller skins.

## Current Manual Process

### Step 1: Open Source Files
- Open designer's RAW file (e.g., DS5 RAW FILE)
- Open target template (e.g., DS5EGCT.psd)

### Step 2: Manual Element Transfer
Transfer these elements from RAW → Template:
- [ ] Background
- [ ] Main logo
- [ ] Legal line

**This is the labor-intensive bottleneck.**

### Step 3: Run Multiview Script
- Script runs against DS5EGCT template
- Generates multiview listing images (front, back, angles)

---

## Input Files
- **RAW file:** Designer's flat artwork with all elements
- **Template:** DS5EGCT.psd (or device-specific template)

## Output Files
- Multiview listing images (JPG/PNG)
- Multiple angles for marketplace listings

---

## Automation Target

**Automate Step 2:**
- Illustrator/Photoshop script to:
  1. Open RAW file
  2. Open template
  3. Auto-copy designated layers (background, logo, legal)
  4. Auto-paste to correct positions in template
  5. Save and proceed to multiview script

---

## Training Videos
- VIDEO 1.mp4 — Source file setup
- VIDEO 2.mp4 — Manual element transfer
- VIDEO 3.mp4 — .EPS creation (belongs in print workflow)

---

## Questions to Resolve
1. Are layer names consistent across all RAW files?
2. What determines positioning in the template?
3. Is the multiview script already automated?
4. How many device templates need support?

---

*Status: Analyzing workflow*
