# Print File Pipeline — eCELL Global / Head Case Designs
*Documented: 2026-02-10 | Source: Cem walkthrough*

---

## Overview

The print file pipeline is the bridge between a shipped order and the physical printed product. It is currently the **#1 automation target** — 5-7 staff daily managing this process.

---

## Two Print File Types

### 1. TIFF Files — Flatbed/Jig Printing
- **Used for:** Phone cases, tablet cases, hard accessories
- **Method:** Products placed in jig (tray) layouts on flatbed UV printer
- **Grouping:** Sorted alphabetically by device model (e.g., all iPhones on one jig)
- **Software:** Printer-specific software manages grouping and layout
- **Printers:** Mimaki/Roland UV printers

### 2. EPS Files — Vinyl Skins
- **Used for:** Console skins, laptop skins (H89 product codes)
- **Method:** Individual EPS files nested together per print job
- **Complexity:** Higher — camera holes, speaker cutouts, button placements vary by device
- **Tool:** Adobe Illustrator-based workflow
- **Documentation:** Available in Google Drive shared folder (to be retrieved)

---

## Current Manual Process

### Step 1: Label Processing (2 staff)
1. Sales data dumps into Veco (updates every 2 minutes)
2. Staff process and print shipping labels in Veco
3. Click "Ship" → export shipped labels to Excel
4. **This Excel = the definitive list** of what needs printing

### Step 2: Print File Generation (3 staff)
1. Take the label export (Excel list of shipped SKUs)
2. Decompose each SKU to identify the design file
3. Look up the source design file (EPS/PSD/TIFF)
4. Generate production-ready print files
5. Handle layout, nesting, and device-specific adjustments
6. **Camera hole issue:** Current script sometimes places designs over camera cutouts — requires manual fix

### Critical Rule
**Labels and print files must match 1:1.** No orphans on either side.
- Can't have labels without corresponding print files (order unfulfillable)
- Can't have print files without labels (wasted production)
- Reconciliation between the two is essential

---

## Staffing Impact

| Role | Normal Season | Peak Season (Dec) |
|------|-------------|-------------------|
| Label management | 2 staff | 2-3 staff |
| Print file generation | 3 staff | 4 staff |
| **Total** | **5-6 staff** | **7 staff** |

**Annual cost:** ~5-6 full-time Philippines staff dedicated to this process

---

## Known Issues with Current Script

### Camera Hole Obstruction
- Phone case templates have camera cutouts in different positions per device model
- The current replication script sometimes places design artwork over the camera hole
- Requires manual inspection and adjustment
- Each new phone release = new template = new potential for issues

### Design Placement Intelligence Needed
- Not a simple template swap — designs need intelligent placement
- Involves PSD files (Photoshop) and Adobe Illustrator (.ai/.eps) files
- Started as a project involving complex file manipulation

---

## Proposed Automation — Hybrid Approach

### Deterministic Layer (Script/N8N)
- SKU decomposition and design file lookup (from Supabase catalog)
- File retrieval from storage (S3/cloud)
- Basic template matching (product type + device → template)
- Label-to-print-file reconciliation
- Batch grouping and jig layout generation

### AI Layer (Gemini Vision / Flash)
- Camera hole avoidance — vision model checks design placement
- Quality validation — does the output look correct?
- Exception handling — missing files, unknown SKUs, custom orders
- Design adjustment suggestions when cutouts interfere

### Expected Impact
- **80% of orders:** Fully automated (standard products, standard layouts)
- **15% of orders:** AI-assisted (needs placement adjustment)
- **5% of orders:** Manual review (custom products, edge cases)
- **Headcount reduction:** 3-4 staff redeployable to other tasks

---

## File Formats Reference

| Format | Used For | Size | Tool |
|--------|----------|------|------|
| PSD | Master design files | ~128MB each | Adobe Photoshop |
| EPS | Vinyl skin print files | Varies | Adobe Illustrator |
| TIFF | Flatbed jig layouts | Large | Printer software |
| PDF | Shipping labels | Small | Veco/carrier system |

---

## Connections to Other Systems

- **Supabase:** Product catalog, SKU → design file mapping, device templates
- **Veco:** Shipping label generation, shipped order list (export to Excel)
- **Gemini Vision:** Design placement verification, camera hole detection
- **Inventory System:** Stock levels determine what gets printed where
- **Google Drive:** EPS workflow documentation, design file archives

---

*Next steps: Get EPS workflow documentation from shared drive. Get examples of camera hole obstruction failures. Map the exact script/tool used for print file generation.*
