# Task: Restyle PULSE Dashboard to Match Sales Dashboard V2

## Reference Style (Sales Dashboard V2)
The Sales Dashboard V2 uses a **LIGHT theme** with these exact patterns:

### Colors & Background
- Page background: `bg-gradient-to-br from-slate-50 to-blue-50`
- Cards: `bg-white rounded-xl shadow-sm border border-gray-100`
- Card hover: `hover:shadow-md transition-shadow`
- Text primary: `text-gray-900`
- Text secondary: `text-gray-500`
- Text muted: `text-gray-400`
- Accent color: blue-600 (`#2563eb`)
- Tab active: `bg-blue-600 text-white shadow-md`
- Tab inactive: `text-gray-600 hover:bg-gray-100`

### Layout
- `min-h-screen` with gradient background
- `max-w-7xl mx-auto` for content width
- `p-6` page padding
- Cards use `p-5` or `p-6`
- Stat cards: white background, colored value text, gray labels
- Section spacing: `mb-6` between major sections

### Component Patterns
```jsx
// Stat Card
<div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:shadow-md transition-shadow">
  <p className="text-gray-500 text-sm font-medium mb-1">{title}</p>
  <p className="text-3xl font-bold" style={{ color }}>{value}</p>
  {subtitle && <p className="text-gray-400 text-xs mt-1">{subtitle}</p>}
</div>

// Tab buttons (pill-style in a white container)
<div className="flex gap-1 bg-white p-1 rounded-xl shadow-sm overflow-x-auto">
  <button className={`px-4 py-2 rounded-lg font-medium text-sm whitespace-nowrap transition-all ${
    active ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100'
  }`}>

// Chart container
<div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
  <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>
</div>

// Tables inside white cards
<table className="min-w-full text-left text-sm">
  <thead className="text-xs uppercase tracking-wide text-gray-500 border-b border-gray-200">
  <tbody>
    <tr className="border-b border-gray-100 hover:bg-gray-50 text-gray-700">
```

### Chart Colors (from Sales Dashboard V2)
```js
const CHART_COLORS = ['#3b82f6','#06b6d4','#f59e0b','#f97316','#8b5cf6','#ec4899','#0ea5e9','#a855f7','#10b981','#ef4444'];
```

### Signal Tier Colors (adapt to light theme)
- Surging: emerald/green (`text-emerald-600 bg-emerald-50 border-emerald-200`)
- Accelerating: cyan/teal (`text-cyan-600 bg-cyan-50 border-cyan-200`)
- Steady: gray (`text-gray-600 bg-gray-50 border-gray-200`)
- Declining: amber (`text-amber-600 bg-amber-50 border-amber-200`)
- Dying: rose/red (`text-rose-600 bg-rose-50 border-rose-200`)

### License Risk Row Colors (gradient backgrounds, light theme)
- Green (>100% target): `bg-gradient-to-r from-emerald-50 to-white`
- Amber (50-100%): `bg-gradient-to-r from-amber-50 to-white`
- Red (<50%): `bg-gradient-to-r from-rose-50 to-white`

## What to Change

### 1. Global Theme Switch (Dark → Light)
**Files to update:**
- `app/globals.css` — Remove any dark background. Set `body { background: ... }` to match `from-slate-50 to-blue-50`
- `app/layout.tsx` — Remove `dark` class if present. Set body to light theme bg.
- `components/dashboard-shell.tsx` — Replace dark sidebar with light sidebar matching Sales Dashboard V2 style

### 2. Sidebar Restyle
Current: Dark sidebar with `bg-slate-950/70` cards
New: Light sidebar:
- Background: `bg-white border-r border-gray-200`
- Logo area: clean white with blue accent
- Nav links: `text-gray-600 hover:bg-gray-100 rounded-lg`
- Active link: `bg-blue-50 text-blue-600 font-medium`
- Small text/descriptions: `text-gray-400`

### 3. All Page Components
Replace all dark theme classes across ALL files:
- `bg-slate-950/70` → `bg-white`
- `border-white/10` → `border-gray-100`
- `text-white` → `text-gray-900`
- `text-slate-300` → `text-gray-600`
- `text-slate-400` → `text-gray-500`
- `text-slate-500` → `text-gray-400`
- `text-cyan-300` → `text-blue-600`
- `bg-black/20` → `bg-gray-50`
- `bg-white/5` → `bg-gray-50`
- `shadow-[0_20px_60px...]` → `shadow-sm`
- `rounded-3xl` → `rounded-xl` (matching Sales Dashboard V2 card radius)
- `hover:bg-white/[0.03]` → `hover:bg-gray-50`

### 4. Stat Cards
Match Sales Dashboard V2 exactly:
```jsx
<div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:shadow-md transition-shadow">
  <p className="text-gray-500 text-sm font-medium mb-1">{label}</p>
  <p className="text-3xl font-bold" style={{ color: accentColor }}>{value}</p>
  <p className="text-gray-400 text-xs mt-1">{detail}</p>
</div>
```
Colors for stat cards:
- Designs tracked: `#1f2937` (gray-900)
- Surging: `#10b981` (emerald)
- Accelerating: `#06b6d4` (cyan)
- Total 2mo Revenue: `#2563eb` (blue)

### 5. Leaderboard Tabs
Replace pill-style dark tabs with Sales Dashboard V2 style:
```jsx
<div className="flex gap-1 bg-white p-1 rounded-xl shadow-sm overflow-x-auto">
  <button className={active ? 'bg-blue-600 text-white shadow-md rounded-lg px-4 py-2 text-sm font-medium' : 'text-gray-600 hover:bg-gray-100 rounded-lg px-4 py-2 text-sm font-medium'}>
```

### 6. Filter Bar
- Search: white background, gray border, gray placeholder
- Dropdowns: white background, gray border
- Filter badges: light style (`bg-blue-50 text-blue-600`)
- Clear button: `border-gray-200 text-gray-600 hover:bg-gray-50`

### 7. Data Tables
- Table container: `bg-white rounded-xl shadow-sm border border-gray-100 p-6`
- Header: `text-xs uppercase tracking-wide text-gray-500 border-b border-gray-200 bg-gray-50/50`
- Rows: `border-b border-gray-100 text-gray-700 hover:bg-gray-50`
- Sticky header: `bg-white/95 backdrop-blur`

### 8. Charts (RevenueTrendChart)
- Container: white card with shadow
- Chart colors: use `CHART_COLORS` from Sales Dashboard V2
- Tooltip: `bg-white rounded-lg shadow-lg border border-gray-200`
- Grid lines: `stroke="#f1f5f9"` (slate-100)

### 9. Signal Badges
Replace dark-theme badge styles:
```jsx
Surging: "border-emerald-200 bg-emerald-50 text-emerald-700"
Accelerating: "border-cyan-200 bg-cyan-50 text-cyan-700"
Steady: "border-gray-200 bg-gray-50 text-gray-600"
Declining: "border-amber-200 bg-amber-50 text-amber-700"
Dying: "border-rose-200 bg-rose-50 text-rose-700"
```

### 10. Page Header
- Title: `text-3xl font-bold text-gray-900`
- Subtitle: `text-gray-500 text-sm`
- Eyebrow: `text-xs uppercase tracking-wide text-gray-400`

### 11. ALL Other Pages (list-it, build-it, complete-it, fix-boost, licenses, tracking)
Apply the same light theme transformation to EVERY page. Don't leave any dark-themed pages.

## Files to Modify (ALL of these)
1. `app/globals.css`
2. `app/layout.tsx`
3. `app/page.tsx`
4. `app/list-it/page.tsx`
5. `app/complete-it/page.tsx`
6. `app/build-it/page.tsx`
7. `app/build-it/drill-down/page.tsx`
8. `app/fix-boost/page.tsx`
9. `app/licenses/page.tsx`
10. `app/tracking/page.tsx`
11. `components/dashboard-shell.tsx`
12. `components/sidebar.tsx`
13. `components/stat-card.tsx`
14. `components/data-table.tsx`
15. `components/filter-bar.tsx`
16. `components/signal-badge.tsx`
17. `components/page-header.tsx`
18. `components/leaderboard-tabs.tsx`
19. `components/revenue-trend-chart.tsx`
20. `components/revenue-trend-chart-inner.tsx`
21. `components/build-matrix.tsx`
22. `components/license-dashboard-client.tsx`
23. `components/tracking-chart.tsx`
24. `components/tracking-chart-inner.tsx`
25. `lib/mock-data.ts` (update signalStyles)

## Critical Rules
- Do NOT change any data logic, types, or API routes
- Do NOT remove any functionality (filters, tabs, sorting, etc.)
- ONLY change visual styling
- Keep all Tailwind classes (just swap dark→light equivalents)
- Run `npm run build` at the end to verify clean compile
- The app uses Tailwind CSS v4 (no config file, uses CSS @import)
