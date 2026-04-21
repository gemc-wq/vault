# Task: Wire Real Data into PULSE Dashboard Leaderboards

## Context
The PULSE dashboard scaffold exists with mock data. You need to replace mock data with REAL velocity data from BigQuery and add three leaderboard views to the home page.

## Real Data Source
File: `/Users/openclaw/.openclaw/workspace/results/pulse_velocity_raw.json`

Structure:
```json
{
  "surging": [...],      // 154 rows, velocity_ratio >= 2.0
  "accelerating": [...], // 146 rows, velocity_ratio 1.3-2.0
  "dying": [...]         // 0 rows currently
}
```

Each row has these fields:
```typescript
{
  design: string,        // e.g. "ALYNAMI", "IRONGAR"
  product_type: string,  // e.g. "HDMWH", "HTPCR", "HB401"
  brand: string,         // e.g. "Iron Maiden", "Liverpool Football Club"
  velocity_2mo: number,  // revenue in last 2 months (USD)
  baseline_monthly: number, // average monthly revenue in prior 4 months
  velocity_ratio: number,   // velocity_2mo / 2 / baseline_monthly
  total_rev: number,     // total 6-month revenue
  orders: number,        // total orders
  velocity_orders: number, // orders in velocity window
  marketplaces: number,  // count of distinct marketplaces
  aov: number           // average order value
}
```

## License Obligation Data
File: `/Users/openclaw/.openclaw/workspace/results/PULSE_PRIORITY_BRIEF_2026-03-10.md`

Key licenses at risk (hardcode for now):
```typescript
const licenseRisk = {
  "Real Madrid": { mgPerYear: 50000, currentPacePerMonth: 612, targetPacePerMonth: 4167, pctOfTarget: 15 },
  "National Basketball Association": { mgPerYear: 100000, currentPacePerMonth: 4103, targetPacePerMonth: 8333, pctOfTarget: 49 },
  "Liverpool Football Club": { mgPerYear: 128000, currentPacePerMonth: 42667, targetPacePerMonth: 10667, pctOfTarget: 400 },
  "Peanuts Worldwide": { mgPerYear: 25400, currentPacePerMonth: 61333, targetPacePerMonth: 2117, pctOfTarget: 2900 },
};
```

## What to Build

### 1. Replace mock-data.ts with real-data.ts
- Import the JSON file at build time (use `import velocityData from '../../results/pulse_velocity_raw.json'`)
- Map the raw rows to `VelocityRow` type (map `velocity_ratio` → `velocityRatio`, `product_type` → `productType`, compute `signalTier` from ratio, use `total_rev` as `revenue90d`, set `device` to "All Devices")
- Compute real summary stats from the data
- Generate real velocity trend data by aggregating total_rev across the 300 rows
- Update ALL existing mock-data imports to use real data

### 2. Three Leaderboard Tabs on Home Page
Add a tabbed leaderboard section below the stat cards with three views:

**Tab 1: Revenue Leaderboard** (default)
- Rank by `velocity_2mo` descending
- Columns: Rank, Design, Brand, Product Type, 2mo Revenue, Velocity Ratio, Signal, Marketplaces, AOV
- Color the velocity ratio: green (≥2x), cyan (1.3-2x), amber (<1.3x), red (<0.3x)
- Show top 50 by default with "Show All" toggle

**Tab 2: Velocity Leaderboard**
- Rank by `velocity_ratio` descending
- Same columns but sorted by velocity ratio
- Highlight "breakout" designs (ratio >5x) with a 🚀 badge

**Tab 3: License Risk Leaderboard**
- Group by brand/license
- Columns: License, MG/Year, Current Pace, Target Pace, Gap %, Surging Designs Count, Total 2mo Revenue
- Color code: Red (<50% target), Amber (50-100%), Green (>100%)
- Sort by gap % ascending (worst gaps first)
- Use the hardcoded licenseRisk data above + aggregate velocity data per brand

### 3. Update Stat Cards with Real Numbers
Replace the 4 stat cards:
- "Designs Tracked" → count of all rows (300)
- "Surging" → count of surging rows (154)
- "Accelerating" → count of accelerating (146)
- "Total 2mo Revenue" → sum of velocity_2mo across all rows

### 4. Filter Bar Updates
Replace mock filters with real values extracted from the data:
- Brand filter: unique brands from real data
- Product Type filter: unique product_types from real data
- Signal Tier: keep existing ["Surging", "Accelerating", "Steady", "Declining", "Dying"]
- Make filters functional (actually filter the table rows)

### 5. Style Requirements
- Keep the existing dark theme (slate-950, slate-900, etc.)
- Tab selector: pill-style tabs with active state
- Tables: hover highlight rows, sticky header
- Revenue numbers: USD formatted with $ and commas
- Velocity ratios: 1 decimal place + "x" suffix
- Signal badges: use existing SignalBadge component
- License risk rows: gradient background from green→amber→red based on gap%
- Responsive: stack on mobile, full table on desktop

### 6. Make Filters Work
The FilterBar component currently doesn't filter anything. Wire it up:
- Use React state for active filters
- Filter the displayed rows based on selected brand, product type, signal tier
- Show filter count badge when filters are active
- Add search box that filters by design name or brand

## File Changes Required
1. `lib/mock-data.ts` → Keep file but add real data exports alongside mock data
2. `app/page.tsx` → Major rewrite with tabs, real data, working filters
3. `lib/types.ts` → Add any new types needed (LicenseRiskRow, LeaderboardTab, etc.)
4. `components/leaderboard-tabs.tsx` → New component for the three tabs
5. `components/data-table.tsx` → Ensure sorting works on all numeric columns
6. `app/api/velocity/route.ts` → Return real data instead of mock

## Build & Test
After changes, run `npm run build` and ensure clean compile. No TypeScript errors.

## Important
- This is a Next.js 16 app with React 19
- Using Tailwind CSS v4 (no tailwind.config.js — uses CSS @import)
- All components are client-side ("use client")
- The JSON data file is at an absolute path — use a relative import from the lib/ directory. Copy the JSON file to `lib/velocity-data.json` first.
