# PULSE v2 — 5 Feature Changes

## Context
- Next.js app at `src/app/page.tsx` (main leaderboard page with 3 tabs: Devices, Design Groups, Champions)
- Filters in `src/components/Filters.tsx`
- Navigation sidebar in `src/components/Navigation.tsx`
- Data types in `src/lib/supabase.ts`
- Client-side fetch helpers in `src/lib/queries.ts`
- Server-side data in `src/lib/pulse-data.ts`
- Supabase RPC functions are used for data. Don't create new RPCs — reuse existing ones with different params.
- The `months` param controls lookback. RPCs accept `p_months` (integer). 1 month = 30 days in the RPC.
- Vercel deployment uses `npx vercel deploy --prod --yes --token <token>` — do NOT deploy, just build clean.

## Change 1: Add 30-day and 60-day lookback periods

**File:** `src/components/Filters.tsx`

The Period dropdown currently has: 3 months, 6 months, 12 months.

Change to: **1 month (30d), 2 months (60d), 3 months, 6 months, 12 months**

The `months` value maps directly to RPC `p_months` param, so `1` = ~30 days, `2` = ~60 days. No backend changes needed.

Update the `<select>` options:
```
<option value={1}>30 days</option>
<option value={2}>60 days</option>
<option value={3}>3 months</option>
<option value={6}>6 months</option>
<option value={12}>12 months</option>
```

## Change 2: Add HB4 and HB7 product types

**File:** `src/lib/supabase.ts`

Add `HB4` and `HB7` to:
1. The `ProductTypeCode` type union
2. The `PRODUCT_TYPE_OPTIONS` array

```typescript
export type ProductTypeCode = 'HTPCR' | 'HC' | 'HB6CR' | 'HLBWH' | 'H7805' | 'HDMWH' | 'H8939' | 'HB4' | 'HB7'

// Add to PRODUCT_TYPE_OPTIONS array:
{ code: 'HB4', label: 'HB4' },
{ code: 'HB7', label: 'HB7' },
```

## Change 3: Fix chart text cutoff

**File:** `src/app/page.tsx` — `CurveChart` component

The ReferenceLine label at the top gets cut off. Fix:
1. Increase `margin.top` from 8 to 24 in the `<LineChart>` component
2. Increase chart height from 200px to 220px

## Change 4: Export CSV button on Champions tab

**File:** `src/app/page.tsx` — `ChampionsPanel` component

Add an "Export CSV" button next to the Champions header. When clicked, export all champion rows as a CSV file with columns:
- `rank` (1-indexed)
- `child_design` (combined: `design_code-design_variant`)
- `design_group` (design_code alone)
- `variant` (design_variant alone) 
- `revenue` (number, no formatting)
- `orders` (number)
- `pct_of_total` (decimal like 0.034 for 3.4%)
- `outside_top_50` (true/false)

Use a client-side download approach (create Blob, click hidden anchor). Name the file `pulse-champions-{region}-{productType}-{months}m.csv`.

The ChampionsPanel component currently doesn't receive `region`, `productType`, or `months`. Thread these through from the parent as new props.

## Change 5: Top Movers page

Create a new page at `src/app/movers/page.tsx` and add it to the Navigation sidebar.

**Concept:** Compare 30-day leaderboard vs 90-day leaderboard to find designs with momentum.

**Data approach:**
- Fetch champion designs twice: once with `months=1` (30d) and once with `months=3` (90d)
- For each child design in the 30d list, find its rank in the 90d list
- Calculate a "momentum score": `rank_90d - rank_30d` (positive = climbing, negative = falling)
- Also calculate revenue ratio: `revenue_30d / (revenue_90d / 3)` — if > 1.0, it's accelerating

**UI:**
- Use shared Filters component (region, productType — no period selector since it's fixed 30d vs 90d)
- Show a table with columns: Rank (30d), Child Design, Revenue (30d), Revenue (90d), Rank Change (↑/↓ with number), Momentum (Accelerating 🟢 / Steady 🟡 / Decelerating 🔴)
- Sort by momentum score descending (biggest climbers first)
- Highlight "New Entries" — designs in 30d top 100 that aren't in 90d top 200 (brand new momentum)
- Add summary cards: Total Movers, Accelerating count, New Entries count

**Navigation:** Add to `src/components/Navigation.tsx`:
```
{ href: '/movers', label: 'Top Movers', icon: '🔥' }
```

Place it after Leaderboard in the nav order.

## Build & Verify
After all changes, run `npm run build` and fix any TypeScript errors. Do NOT deploy.
