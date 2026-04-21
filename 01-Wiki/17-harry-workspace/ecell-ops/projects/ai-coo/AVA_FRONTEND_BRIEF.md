# ECELL DASHBOARD + PRODUCT ENTRY — Frontend Build Brief for Ava
> From: Harry (COO) + Cem (CEO)
> Date: 2026-02-09 (v2 — updated with final schema)
> Priority: HIGH — Start immediately

---

## Overview

Build a central dashboard portal with two initial apps:
1. **Product Entry** — Manual data entry into Supabase (the human trigger for the pipeline)
2. **Image Maker** — Already briefed separately (`AVA_IMAGE_MAKER_BRIEF.md`)

Both apps live under one dashboard URL.

---

## Dashboard Portal

Simple landing page with app cards:
- 📝 **Product Entry** — "Create new products"
- 🖼️ **Image Maker** — "Generate product images"
- ✅ **Approval Queue** — "Review pending items" (Phase 2)
- 📊 **Pipeline View** — "Track product status" (Phase 2)

Clean, minimal UI. White/grey palette. Navy accents. No clutter.

---

## Supabase Connection

**Project URL:** `https://nuvspkgplkdqochokhhi.supabase.co`
**Anon Key:** `sb_publishable_NReQwcvnfMEdpCy6OfornQ_or7kwlJW`
**Service Key (server-side only):** `[REDACTED_SUPABASE_SECRET_KEY]`

Use anon key on frontend. Service key for server-side writes only.

---

## Database Schema — What's Available

### Tables

| Table | Rows | Purpose | Access |
|-------|------|---------|--------|
| `product_types` | 61 | Product type codes (HC, HHYBK, HTPCR…) | READ |
| `brands` | 30 | Device brands with sort order | READ |
| `device_types` | 11 | Device categories (phone, tablet, gaming…) | READ |
| `devices` | 2,636 | All device models with `device_type` column | READ |
| `licenses` | 871 (465 active) | Licensed properties (NFL, WWE, Harry Potter…) | READ |
| `products` | — | Product master records | READ/WRITE |
| `designs` | — | Design artwork linked to products | READ/WRITE |
| `product_images` | — | Generated product images | READ/WRITE |
| `approvals` | — | Approval queue entries | WRITE |

### Views (use these instead of raw tables where available)

| View | Purpose | Use For |
|------|---------|---------|
| `device_selector` | Devices with brand sorting, device type info, icons | **Device dropdown** |
| `product_types_by_category` | Product types grouped by category | **Product type dropdown** |
| `devices_by_type` | Device count per category | **Device type tabs** |
| `device_counts_by_brand` | Stats per brand | Analytics |
| `pending_approvals` | Queued approval items | Approval Queue (Phase 2) |
| `pipeline_overview` | Full pipeline status | Pipeline View (Phase 2) |

### RPC Functions (call via Supabase `.rpc()`)

| Function | Input | Returns | Use For |
|----------|-------|---------|---------|
| `search_devices(search_term)` | text | `{id, display_name, model_code, brand, device_type}` | **Device search/autocomplete** |
| `get_product_type(p_code)` | text | `{id, code, display_name, category, base_cost_usd}` | Product type lookup |

### Product Types (61 codes, 4 categories)

| Category | Count | Examples |
|----------|-------|---------|
| `phone_case` | 35 | HC (Hard Crystal), HHYBK (Hybrid Gel), HTPCR (Soft Gel), HB8CR (MagSafe Bumper) |
| `accessory` | 20 | H3401 (Leather Strap), HA501 (MagSafe Wallet), HDMWH (Desk Mat), HCCWH (Car Charger) |
| `audio_case` | 5 | H7805 (Clear Audio Case), H7601 (Hard Audio Case), HA605 (Soft Gel Audio) |
| `screen_protector` | 1 | H7100 (Tempered Glass) |

### Device Types (11 categories)

| Code | Name | Icon | Count | Example Devices |
|------|------|------|-------|-----------------|
| `phone` | Smartphones | 📱 | 2,284 | iPhone 16 Pro Max, Galaxy S25 Ultra, Pixel 9 |
| `tablet` | Tablets | 📱 | 108 | iPad Pro, Galaxy Tab, Fire HD |
| `gaming_console` | Gaming Consoles | 🎮 | 92 | PS5, Xbox Series X, Nintendo Switch, Steam Deck |
| `accessory` | Accessories | ⚡ | 43 | Apple Watch, chargers, adapters |
| `laptop` | Laptops | 💻 | 26 | MacBook Pro, Surface Pro |
| `audio` | Audio Devices | 🎧 | 22 | AirPods, Galaxy Buds, Beats |
| `other` | Other | ❓ | 19 | Miscellaneous |
| `smart_home` | Smart Home | 🏠 | 17 | Echo Dot, Echo |
| `e_reader` | E-Readers | 📚 | 15 | Kindle, Paperwhite, Oasis |
| `gaming_accessory` | Gaming Accessories | 🎮 | 3 | Desk mats (S/L/XL) |
| `car_mount` | Car Mounts | 🚗 | 1 | MagSafe car mount |

---

## Product Entry App

### Two Input Modes

#### Mode 1: Single Entry Form

**Fields (in order):**

1. **Product Type** → Grouped dropdown from `product_types_by_category` view
   - Group headers: "Phone Cases", "Accessories", "Audio Cases", "Screen Protectors"
   - Display: `code — display_name` (e.g., "HC — Hard Crystal Back Case")
   - **Smart filtering:** When product type is selected, filter the device dropdown:
     - Phone cases → show `phone` + `tablet` devices
     - Audio cases → show `audio` devices only
     - Gaming cases (HGHCR, HGTCR, HGCBK, etc.) → show `gaming_console` devices
     - Accessories (desk mats, car mounts) → show relevant device types
     - Screen protectors → show `phone` + `tablet`

2. **Device Model** → Searchable dropdown using `search_devices()` RPC
   - **Tabbed by device type** (using `device_types` table for tab labels + icons)
   - Default tab: Smartphones (most common)
   - Within each tab: sorted by brand priority (Samsung → Apple → Google first)
   - Display: `brand — model` + model_code in grey
   - Pre-filter tabs based on product type selection (see above)
   - Search searches across all tabs

3. **Brand / Licensed Property** → Searchable dropdown from `licenses` table
   - Filter: `is_active = true` (465 active)
   - Display: `name` (e.g., "NFL", "Harry Potter", "Peanuts")
   - Allow "Original / No License" option for in-house designs

4. **Design Group Code** → Text input (e.g., "KIT25")

5. **Design Variation** → Text input (e.g., "HOM", "AWY", "THI")

6. **Design Title** → Text input (human-readable name)

7. **Notes** → Optional textarea

**SKU Auto-Generation (real-time preview):**
```
{PRODUCT_TYPE_CODE}-{DEVICE_MODEL_CODE}-{BRAND_CODE}{DESIGN_GROUP}-{VARIATION}
Example: H8939-DS5EGCT-RMCFKIT25-HOM
```
SKU preview updates live below the form as fields are filled.

**On Submit:**
- Create record in `products` table (status: `'draft'`)
- Create linked record in `designs` table
- Create `approvals` entry (entity_type: `'product'`, action: `'approve_product'`)
- Show success message with generated SKU
- Option to "Create Another" or "View in Pipeline"
- POST webhook to N8N (Harry will provide URL later)

#### Mode 2: CSV Bulk Upload

- Drag-and-drop CSV upload zone
- Column mapping step (map CSV columns to fields)
- Preview table with auto-generated SKUs
- Validation (highlight errors: missing fields, duplicate SKUs, invalid codes)
- "Import All" → batch insert to Supabase
- Summary: "X products created, Y errors"

**Required CSV columns:**
```
product_type_code, device_code, brand_code, design_group, variation, design_title
```

**Validation rules:**
- `product_type_code` must exist in `product_types.code`
- `device_code` must exist in `devices.model_code`
- SKU must be unique in `products.sku`

---

## Supabase Query Examples

### Populate product type dropdown (grouped)
```javascript
const { data: productTypes } = await supabase
  .from('product_types_by_category')
  .select('*');
// Returns: [{category, code, display_name, sort_order}, ...]
```

### Device type tabs
```javascript
const { data: deviceTypes } = await supabase
  .from('device_types')
  .select('code, display_name, icon, sort_order')
  .eq('is_active', true)
  .order('sort_order');
```

### Device search (autocomplete)
```javascript
const { data: devices } = await supabase
  .rpc('search_devices', { search_term: 'iPhone 16' });
// Returns: [{id, display_name, model_code, brand, device_type}, ...]
```

### Devices filtered by type (tab click)
```javascript
const { data: phones } = await supabase
  .from('device_selector')
  .select('*')
  .eq('device_type', 'phone')
  .limit(50);
```

### Devices filtered by multiple types (smart filter)
```javascript
// When user selects a phone case product type:
const { data: compatible } = await supabase
  .from('device_selector')
  .select('*')
  .in('device_type', ['phone', 'tablet']);
```

### License/brand dropdown
```javascript
const { data: licenses } = await supabase
  .from('licenses')
  .select('id, name')
  .eq('is_active', true)
  .order('name');
```

### Create product
```javascript
const { data, error } = await supabase
  .from('products')
  .insert({
    sku: generatedSku,
    device_id: selectedDevice.id,
    product_type_id: selectedProductType.id, // UUID from product_types
    case_type: selectedProductType.code,      // Keep legacy field too
    title: designTitle,
    status: 'draft'
  })
  .select()
  .single();
```

---

## Smart Product ↔ Device Compatibility

Map product type categories to allowed device types:

```javascript
const COMPATIBILITY_MAP = {
  'phone_case': ['phone', 'tablet'],
  'audio_case': ['audio'],
  'screen_protector': ['phone', 'tablet'],
  'accessory': null, // null = show all device types
};

// Special product codes that override category rules:
const PRODUCT_OVERRIDES = {
  'HGHCR': ['gaming_console'],      // Gaming Hard Case
  'HGTCR': ['gaming_console'],      // Gaming Soft Gel Case
  'HGCBK': ['gaming_console'],      // Gaming Travel Case (Black)
  'HGCBL': ['gaming_console'],      // Gaming Travel Case (Blue)
  'HGCRD': ['gaming_console'],      // Gaming Travel Case (Red)
  'HGCWH': ['gaming_console'],      // Gaming Travel Case (White)
  'HGC01': ['gaming_console'],      // Gaming Travel Case Bundle
  'HGC02': ['gaming_console'],
  'HGC18': ['gaming_console'],
  'HGC21': ['gaming_console'],
  'HGSBK': ['gaming_console'],      // Game Controller Skin
  'HGSBL': ['gaming_console'],
  'HGSRD': ['gaming_console'],
  'HGSDB': ['gaming_console'],
  'HA721': ['gaming_console'],      // Console Wrap
  'HA921': ['gaming_console'],      // Console + Controller Bundle
  'HLCCR': ['laptop'],              // Laptop Cases
  'HLCCG': ['laptop'],
  'HLCBT': ['laptop'],
  'HDMWH': ['gaming_accessory'],    // Desk Mat
  'HFMWH': ['gaming_accessory'],    // Floor Mat
  'HCCWH': ['car_mount'],           // Car Charger Mounts
  'HCCBK': ['car_mount'],
  'HCC01': ['car_mount'],
  'HCC21': ['car_mount'],
  'HC2BK': ['car_mount'],
  'HC201': ['car_mount'],
  'HH2BK': ['car_mount'],
  'HH201': ['car_mount'],
  'HMBBK': ['car_mount'],
  'HMB01': ['car_mount'],
};

function getCompatibleDeviceTypes(productCode, productCategory) {
  if (PRODUCT_OVERRIDES[productCode]) return PRODUCT_OVERRIDES[productCode];
  if (COMPATIBILITY_MAP[productCategory]) return COMPATIBILITY_MAP[productCategory];
  return null; // Show all
}
```

---

## Tech Stack

- **Next.js** (App Router)
- **@supabase/supabase-js** (v2)
- **Tailwind CSS** + **shadcn/ui** components
- **React Hook Form** for form handling
- **Papa Parse** for CSV parsing (client-side)
- **cmdk** or similar for searchable dropdown/combobox

## UI/UX Requirements

- Clean, minimal — white, grey, navy accents
- Mobile-responsive (Cem reviews on phone)
- Fast — preload device/brand data on mount
- SKU preview updates in real-time
- Success/error states are clear and obvious
- No auth required initially (internal tool, direct URL)
- Device selector should feel snappy — use `search_devices()` RPC for search, paginate the full list

---

## Build Order

1. **Dashboard shell** — Portal page with app cards
2. **Product Entry form** (single entry) — Dropdowns + smart filtering + SKU auto-gen + Supabase write
3. **CSV bulk upload** — Import mode with validation
4. **Image Maker** — Per separate brief (`AVA_IMAGE_MAKER_BRIEF.md`)

---

## Files Reference

| File | Location | Purpose |
|------|----------|---------|
| Master schema | `projects/ai-coo/supabase_schema.sql` | Original table definitions |
| Migration SQL | `projects/ai-coo/migration_001_actual_data.sql` | Product types + devices + views |
| Rollback | `projects/ai-coo/rollback_001.sql` | Emergency rollback |
| Image Maker brief | `projects/ai-coo/AVA_IMAGE_MAKER_BRIEF.md` | Separate app brief |
| Blueprint | `projects/ai-coo/BLUEPRINT.md` | Full business process flow |

---

*Brief prepared by Harry | 2026-02-09 v2*
*Schema deployed and verified ✅*
