# Phase 3: Portal UI — Antigravity Build Brief

## Project Path
`/Users/openclaw/projects/procurement-system`

## Stack
- Next.js 16 + TypeScript + Tailwind CSS 4
- Supabase (client at `lib/db.ts`)
- Types at `lib/types/database.ts`

## Style Guide (Ecell Global — Wiki #33, MANDATORY)

### Colors
- **Brand Cobalt:** `#0047AB` (primary actions, active nav) / Light: `#E8F0FE` / Dark: `#003380`
- **Neutrals:** Background `#FAFBFC`, Cards `#ffffff`, Text `#171717`, Secondary `#71717a`, Borders `#e4e4e7`
- **Status Traffic Light:** Emerald `#10b981` (good), Amber `#f59e0b` (warning), Red `#ef4444` (danger)

### Typography
- Font: Inter (already in globals.css)
- Page titles: `text-3xl font-semibold tracking-tight`
- Card titles: `text-sm font-semibold`
- Body: `text-sm`
- Secondary: `text-xs text-zinc-500`

### Components
- Cards: `rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm transition hover:border-zinc-300 hover:shadow-md`
- Status badges: `inline-flex items-center rounded-full border border-{color}-500/30 bg-{color}-500/10 px-2 py-0.5 text-[11px] font-semibold text-{color}-700`
- Traffic light dots: `w-4 h-4 bg-{color}-500 shadow-{color}-500/40 rounded-full shadow-md`
- Buttons primary: `bg-[#0047AB] text-white rounded-lg px-4 py-2 hover:bg-[#003380]`
- Nav active: `bg-[#0047AB] text-white rounded-lg`
- Nav inactive: `text-gray-700 hover:bg-gray-100 rounded-lg`
- No heavy shadows — `shadow-sm` or `shadow-md` only

### Layout
- Sidebar pattern: `w-56 min-h-screen bg-white border-r border-zinc-200`
- Main content: `flex-1 overflow-auto p-8 bg-[#FAFBFC]`

## Tailwind v4 Theme (already in globals.css)
```css
@theme {
  --color-cobalt: #0047AB;
  --color-cobalt-light: #E8F0FE;
  --color-cobalt-dark: #003380;
}
```

## What Already Exists
- `app/page.tsx` — Dashboard (basic dark theme, needs restyling to light Ecell theme)
- `app/inventory/page.tsx` — Inventory table
- `app/reorder/page.tsx` — Reorder queue
- `app/po/page.tsx` — PO batches
- `app/layout.tsx` — Simple body layout (no sidebar yet)
- `app/globals.css` — Updated with Ecell Cobalt tokens
- API routes: `/api/inventory/*`, `/api/reorder/*`, `/api/po/*`, `/api/health`, `/api/transfers/*`

## Database Tables (Supabase)
```
internal_transfers: id, transfer_number, item_code, from_warehouse, to_warehouse, qty, reason,
  priority (HIGH/MEDIUM/LOW), status (SUGGESTED/PENDING/APPROVED/PICKED/SHIPPED/DELIVERED_PENDING/RECEIVED/CANCELLED),
  tracking_number, created_at, approved_at, shipped_at, received_at, received_qty, damage_notes

best_sellers_daily: item_code, warehouse, rank, velocity_7d, velocity_30d, velocity_used,
  sales_last_7d, sales_last_30d, free_stocks, days_of_cover, stock_risk (CRITICAL/LOW/OK), snapshot_date

system_health: component, last_run_at, last_status (SUCCESS/FAILED/RUNNING), error_message

warehouses: code (UK/Florida/PH/CN/TRANSIT/FL/ZONE_US/ZONE_UK), name, zone (US/UK/SHARED/STAGING)

blank_inventory: item_code, warehouse, free_stocks, in_transit

suppliers: name, currency, lead_time_days, payment_terms, is_active
```

## BUILD THESE FILES

### 1. `app/components/SidebarNav.tsx` (NEW — client component)
- `'use client'` using `usePathname` from `next/navigation`
- Sidebar w-56, white background, border-r
- Brand: "Ecell Procurement" in text-xl font-bold text-[#0047AB] at top
- Nav links with icons (emoji fine): Dashboard (/), Inventory (/inventory), Reorder Queue (/reorder), PO Batches (/po), Transfers (/transfers), Zone Stock (/inventory/zones)
- Active = bg-[#0047AB] text-white, Inactive = text-gray-700 hover:bg-gray-100
- Bottom: "v2.0" in text-xs text-zinc-400

### 2. `app/layout.tsx` (UPDATE — add sidebar)
- Import SidebarNav component
- Layout: `flex h-screen` with SidebarNav + main content area
- Main: `flex-1 overflow-auto bg-[#FAFBFC]`
- Update metadata title to "Ecell Procurement Portal"
- Keep Inter/Geist font imports

### 3. `app/page.tsx` (UPDATE — enhanced dashboard, LIGHT THEME)
- Restyle from dark to light theme matching Ecell style guide
- Zone stock summary cards: "Zone US" and "Zone UK" with total free stocks, days of cover
- Data freshness indicator: fetch `/api/health`, show green/red dots per component based on last_run_at (<6h = green, else red)
- PH stock-out alert banner: if any items have stock_risk=CRITICAL, show red alert banner at top
- Best sellers widget: top 10 from best_sellers_daily with velocity and risk badges
- Keep existing alert summary cards but restyle to Ecell light theme with Cobalt accents
- Remove the hardcoded nav bar (now in sidebar)

### 4. `app/transfers/page.tsx` (NEW)
- Table of all internal_transfers fetched from Supabase
- Columns: Transfer #, Item Code, From → To, Qty, Priority badge, Status badge, Created, Actions
- Filter bar: status dropdown, destination dropdown, priority dropdown
- Status badges: SUGGESTED=zinc, PENDING=zinc, APPROVED=cobalt, PICKED=cobalt, SHIPPED=amber, DELIVERED_PENDING=amber, RECEIVED=emerald, CANCELLED=red
- Priority badges: HIGH=red, MEDIUM=amber, LOW=emerald
- Action buttons per status:
  - SUGGESTED → Approve / Reject
  - APPROVED → Mark Picked
  - PICKED → Ship (with tracking number input modal/inline)
  - SHIPPED → Mark Delivered
  - DELIVERED_PENDING → Confirm Receipt (with received_qty input + damage_notes textarea)
- Actions PATCH to `/api/transfers/{id}` with `{status, tracking_number?, received_qty?, damage_notes?}`
- Refresh table after each action

### 5. `app/inventory/zones/page.tsx` (NEW)
- Two sections: Zone US and Zone UK
- Each zone table: Item Code, PH Stock, FL/UK Stock, In Transit, Total, Days of Cover, Risk badge
- Days of cover color: <7d red, 7-14d amber, 14-30d emerald, >30d cobalt-light bg
- Summary cards at top per zone: Total SKUs, Critical count, Avg days of cover
- Fetch inventory data from Supabase (blank_inventory + best_sellers_daily joined)
- Query: group by item_code, aggregate across warehouses for zone view

### 6. `app/api/inventory/zones/route.ts` (NEW — API route)
- GET endpoint returning zone-aggregated inventory data
- Zone US = warehouses Florida + proportional PH share
- Zone UK = warehouses UK + proportional PH share
- For each item: aggregate free_stocks, in_transit, calculate days_of_cover from best_sellers velocity
- Return JSON: `{ zones: { us: ZoneItem[], uk: ZoneItem[] }, summary: { us: {...}, uk: {...} } }`

## CRITICAL RULES
- All pages use `'use client'` for interactivity
- Supabase client: `import { supabase } from '@/lib/db'`
- Light theme (bg-[#FAFBFC]) not dark
- Cobalt (#0047AB) for primary actions, not generic blue
- Traffic light status system (emerald/amber/red)
- Cards with rounded-2xl, shadow-sm
- No heavy shadows, no bright generic colors
- All interactive elements need loading states
- Error handling on all fetches
