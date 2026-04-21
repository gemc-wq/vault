# AutoPricer — AI Pricing Optimizer
> **Owner:** Ava | **Status:** Scoped | **Created:** 2026-03-21
> **SaaS Candidate:** ✅ "AutoPrice — AI Marketplace Pricing Optimizer"
> **Pattern:** Karpathy's AutoResearch + Claude Code autonomous loop

## Concept
LLM agent autonomously experiments with pricing to maximize revenue per session. Runs weekly, accumulates learnings, gets smarter each cycle.

## The Loop
```
Identify (quadrant) → Hypothesize (price change) → Deploy (API)
→ Wait (14 days) → Measure (conversion) → Keep/Revert → Learn → Repeat
```

## Agent Architecture
- **Engine:** Claude Sonnet 4.6 via OpenClaw cron (weekly Saturday)
- **Memory:** `resource.md` — accumulated pricing learnings across cycles
- **Data:** Amazon Business Reports (sessions/conversion) + Supabase experiment tracking
- **APIs:** Walmart MP_MAINTENANCE (working), Amazon SP-API Pricing (needs role)
- **Dashboard:** Next.js on Vercel — experiment tracker, quadrant chart, learnings viewer

## Key Finding (Mar 21)
- Best sellers ≠ best converters — ZERO overlap top 10 by revenue vs top 10 by conversion
- Revenue is driven by SESSION VOLUME, not conversion efficiency
- Untapped revenue in: price increases on Stars, price decreases on Q-Marks, PPC on Cash Cows

## Test Strategies
1. **Price reduction on Q-Marks** (13 candidates) — $19.95→$17.95
2. **Price increase on Stars** (30 candidates) — $19.95→$21.95
3. **Free shipping test** — $24.95 free vs $19.95+$6.99
4. **Device-specific pricing** — premium for new, discount for old

## Guardrails
- Price floor: COGS + royalty (~$8-10/unit)
- Max 20 SKUs per test cycle
- Min 14-day test duration
- Auto-revert if conversion drops >30%
- Min 50 sessions/week for statistical significance

## Files
- Spec: `projects/PRICING_OPTIMIZER_SPEC.md`
- Baselines: `wiki/25-pulse-dashboard/CONVERSION_BASELINES.md`
- Research: `research/claude-code-autoresearch-takeaways.md`

## Dependencies
- Amazon SP-API: needs "Pricing" + "Reporting" roles (Cem to add in Seller Central)
- Walmart API: MP_MAINTENANCE works for price updates ✅
- Conversion data: weekly Amazon Business Reports (manual download until SP-API roles added)
