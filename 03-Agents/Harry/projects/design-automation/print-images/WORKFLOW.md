# Print Image Creation Workflow

**Purpose:** Create production-ready .EPS files for manufacturing/printing.

## Current Manual Process

### Step 1: Prepare Cut File
- Use the cut file from Product Image workflow
- File prepared in Step 2 of that process

### Step 2: Load Vecras Template
- Open Vecras-purchased template (e.g., 89-39-DS5EGCT)
- This is a print-specific template with proper bleed/trim

### Step 3: Create .EPS
- Drag cut file into Vecras template
- Export as .EPS format for production

---

## Input Files
- Cut file from Product Image workflow
- Vecras template for specific device

## Output Files
- Print-ready .EPS file
- Proper bleed, trim marks, color profile for manufacturing

---

## Automation Target

**Automate the entire process:**
- Script to:
  1. Take cut file from product workflow
  2. Auto-place into correct Vecras template
  3. Export .EPS with correct settings

---

## Template Mapping

| Device | Vecras Template |
|--------|-----------------|
| DS5 Controller | 89-39-DS5EGCT |
| (others TBD) | |

---

## Questions to Resolve
1. Full list of Vecras templates and device mappings
2. .EPS export settings (color profile, bleed, etc.)
3. Where do Vecras templates live?
4. Is this always a 1:1 mapping (one cut file → one template)?

---

*Status: Awaiting files and video analysis*
