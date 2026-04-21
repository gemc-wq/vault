# Conversion Intelligence Dashboard
> **Owner:** Ava | **Status:** LIVE | **Updated:** 2026-03-18

## URL
https://conversion-dashboard-kohl.vercel.app

## What It Does
Amazon US sessions and conversion analysis comparing 14-day vs 30-day lookback periods.
- **Leaderboard:** By license, product type, device, design — with velocity indicators
- **Scatter Plot:** Sessions vs Conversion Rate (quadrant: Stars/Question Marks/Cash Cows/Dogs)
- **Device Comparison:** Conversion rates across devices for same designs (iPhone 15+ got new images)
- **Alerts:** High sessions + low conversion, accelerating, declining, new & hot

## Data Sources
- Amazon Child ASIN Reports (14d + 30d) — CSV uploaded by Cem
- ASIN→SKU bridge from local SQLite (3.43M US listings)
- Listing creation dates from `open-date` field

## Key Findings (Mar 15)
- NBA: +14% velocity, 21.9% conversion — revised images working
- Powerpuff Girls: +32% velocity — validates HB6/HB7 expansion
- HB401: +7% velocity, 4.9% conversion — best conversion of any phone case type
- iPhone 17 Pro: +13%, 7.9% conversion — hottest device

## Stack
- Next.js 14, TypeScript, Tailwind, Recharts
- Static data (CSV parsed at build time)
- Vercel deployment

## Data Refresh
- Weekly: Cem downloads Amazon reports Friday 5 PM (cron reminder set)
- AirDrop to Mac Studio ~/Downloads/ → Ava rebuilds and redeploys
