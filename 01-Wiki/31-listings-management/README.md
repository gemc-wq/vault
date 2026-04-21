# Listings Management System — PH Team Direction
> **Owner:** Ava | **Status:** Scoped | **Created:** 2026-03-21
> **SaaS Candidate:** ✅ Autonomous marketplace team management

## Problem
20 PH staff (listings + creative) work without data-driven direction. $500K+ annual labor directed by guesswork.

## Three Loops

### Loop 1: Weekly Listings Direction
- PULSE champions × marketplace gaps → weekly target list
- Posted to Slack #listings every Monday 8 AM
- EOD cross-reference tracks completion

### Loop 2: License Performance Monitor
- MG vs actual revenue per license
- Flags at-risk licenses (e.g., NBA $200K MG, underperforming)
- Weekly report to Slack #marketing

### Loop 3: 14-Day Conversion Attribution
- Match new listings (by open_date) to sessions data 2 weeks later
- Classify: Winner / Needs Work / Underperformer
- Bi-weekly performance report to Slack #listings

## Key Design Points
- 14-day Amazon attribution window — listings measured 2 weeks after creation
- Champions = Combined Back Case Revenue (HTPCR + HC + HB401)
- Gap analysis runs per marketplace (Amazon US, UK, Walmart, OnBuy)

## Files
- Spec: `projects/LISTINGS_MANAGEMENT_SYSTEM_SPEC.md`
- Baselines: `wiki/25-pulse-dashboard/CONVERSION_BASELINES.md`
- Champion methodology: MEMORY.md → Master Architecture
