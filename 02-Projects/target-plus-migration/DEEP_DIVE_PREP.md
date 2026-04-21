# Target+ / Feedonomics Migration — Deep Dive Prep
> For: Monday March 10, 2026 @ 2PM ET
> Prepared: 2026-03-06

## Situation
- Target+ is LIVE and generating orders
- Orders flow to both BigCommerce AND Shopify
- Fulfillment/tracking goes back to Target via BigCommerce
- **Feedonomics manages the product feed — contract ends in ~2 weeks**
- Jay Mark (Listing Lead, PH) is aligned on migration

## Key Questions for Cem (BEFORE Monday)
1. **SKU count** on Target+ — how many active listings?
2. **Exact Feedonomics contract end date** — is it March 20? March 22?
3. **Monthly Target+ revenue** — what's at risk if feed breaks?
4. **Shopify vs BigCommerce preference** — which platform should be the source of truth going forward?
5. **Feedonomics monthly cost** — what are we saving by dropping them?

## Replacement Options

### Option A: Shopify Marketplace Connect (Recommended)
- **Formerly Codisto** — Shopify's official marketplace integration
- Free to install, additional charges may apply
- Supports: Amazon, Target+, Walmart, eBay
- 4.2★ rating (1,922 reviews) — 79% five-star
- **Pros:** Native Shopify integration, single dashboard, real-time sync, free base tier, official Target+ partnership (June 2024)
- **Cons:** 13% one-star reviews (check failure modes), may need manual mapping for 500+ device catalog
- **Migration path:** Already partially done per March 5 notes — Jay Mark aligned

### Option B: Stay on BigCommerce (keep current flow)
- Continue using BigCommerce as feed source
- Find BigCommerce-native feed tool (Feedonomics alternative)
- Options: DataFeedWatch, GoDataFeed, ChannelAdvisor
- **Pros:** No migration risk, familiar flow
- **Cons:** Maintaining two platforms (BC + Shopify), ongoing feed tool cost

### Option C: Custom feed via API
- Build direct Target+ API integration
- Use existing Supabase inventory as source
- **Pros:** Full control, no third-party dependency
- **Cons:** Dev time, maintenance burden, risk during transition

## Recommendation
**Option A (Shopify Marketplace Connect)** — aligns with the existing Shopify infrastructure, zero feed tool cost, and the migration is already partially underway. Risk is manageable if we start mapping SKUs this week before Feedonomics expires.

## Action Plan (if approved Monday)
1. **This week:** Get SKU count + current feed format from Feedonomics
2. **March 10-14:** Install Shopify Marketplace Connect, map product catalog
3. **March 14-17:** Test sync (parallel run with Feedonomics still active)
4. **March 17+:** Cut over to Shopify MC, deactivate Feedonomics

## Shopify Marketplace Connect — Details (researched 2026-03-07)
- **Developer:** Shopify (first-party, formerly Codisto — acquired)
- **Rating:** 4.2★ / 1,923 reviews — 79% five-star, 13% one-star
- **Pricing:** Free to install; usage-based charges may apply (not publicly listed — need to confirm tier for our SKU volume)
- **Supported marketplaces:** Amazon, Target+, Walmart, eBay — unlimited account connections
- **Languages:** EN, DE, ES, FR, IT
- **Key features:** Real-time listing/order/inventory sync, flexible fulfillment, built-in currency conversion
- **Merchant sentiment (positive):** Strong support, streamlined multi-channel, reliable sync, reduces admin overhead
- **1-star failure patterns (13%):** Likely sync errors at scale, large catalog mapping issues, support response times — **we should stress-test with a small SKU batch before full cutover**

## Feedonomics Comparison
- **Pricing:** Custom/quote-based, SKU-count-driven, no revenue share — likely $500-2,000+/mo for our catalog size
- **What we lose:** Managed feed optimization, dedicated account management, feed transformation rules
- **What we gain by dropping:** Cost savings, single-platform simplicity (no BC → Feedonomics → Target chain)

## Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Feedonomics expires before MC migration complete | HIGH | CRITICAL — listings go dark | Get exact expiry date Monday; negotiate 2-week extension if possible |
| Shopify MC sync errors at scale (500+ devices × N designs) | MEDIUM | HIGH — partial catalog loss | Start with top 50 devices (86.5% revenue), expand incrementally |
| Target+ delists products during feed gap | LOW-MED | HIGH — re-onboarding delay | Maintain parallel feed during overlap period |
| Shopify MC hidden costs at our SKU volume | LOW | MEDIUM — budget surprise | Ask Shopify MC team directly before committing |
| Image/asset formatting mismatch between platforms | MEDIUM | LOW — fixable post-migration | Audit Target+ image requirements vs. Shopify catalog |

## Pre-Meeting Agenda (Monday 2PM)
1. **Get the numbers** — SKU count, exact Feedonomics end date, monthly Target+ revenue, monthly Feedonomics cost
2. **Platform decision** — Shopify as single source of truth going forward? (impacts everything downstream)
3. **Migration approach** — Phase 1: top 50 devices only (covers 86.5% revenue), Phase 2: long tail
4. **Timeline commitment** — Can Jay Mark start mapping this week?
5. **Fallback plan** — If Feedonomics can't extend, what's our manual stopgap?

## Open Risks
- If Feedonomics expires before migration is complete → feed breaks → Target+ listings go dark
- Need to understand Feedonomics grace period / wind-down process
- Image replication backlog could delay new listings on Target+
- **NEW:** At 3.44M Amazon SKUs + 95K Walmart SKUs, Shopify MC could be the unified feed for ALL marketplaces (not just Target+) — worth discussing Monday as long-term play
