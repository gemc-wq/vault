# ListingForge — PH Workflow Audit
> Source: Console Skin Replication Step-by-step Guide (Brain/Projects/design-automation/)
> Analyzed: 2026-03-06

## Current Process: 14 Steps, Heavily Manual
1. Email intake with PSD link + design guide + Google Sheet tracker
2. Download + standardized folder structure
3. Review placement rules (logos, safe zones, cut lines, bleed)
4. Open pre-built console PSD templates in Photoshop
5. Place art via Smart Objects (double-click → paste → scale → save)
6. Organize 3-5+ designs per PSD with named group folders
7. Repeat across ALL console types (PS5, PS4, PS4 Pro, controllers, handhelds)
8. Cross-check PSD group names vs Google Sheet tracker
9. Build Photoshop Actions for mockup generation
10. Write JSX scripts for batch export
11. Test run on one design
12. Full script execution (Photoshop locked during this)
13. QC spot-check
14. Handoff to Creative/Production

## Tools
- **Adobe Photoshop** (Smart Objects, Actions, ExtendScript/JSX)
- **Google Sheets** (tracker with design codes, names, sequence)
- **Email** (intake/handoff)
- **Local file system** (no version control)

## Bottlenecks (ranked)
1. **Naming mismatches** — PSD names ↔ Sheet tracker ↔ script variables must be EXACT. Single biggest failure point.
2. **Repetitive manual layout** (Steps 5-7) — Same design placed across every console template manually. This is where 630 SKUs/day comes from.
3. **Cross-console consistency** — Logo/legal placement rules differ per template shape.
4. **Script debugging** — Fragile automation; any naming change breaks the chain.
5. **Photoshop lockout** — Can't use PS during full batch export.
6. **No version control** — Local folders only, risk of overwrites.

## Automation Opportunities for ListingForge
| Bottleneck | ListingForge Solution | Feasibility |
|---|---|---|
| Naming mismatches | Auto-generate names from single source (DB) | ✅ Easy |
| Repetitive layout | AI-powered design placement OR server-side Smart Object manipulation | ⚠️ Needs validation — this is the hard part |
| Consistency checks | Rule engine for placement validation | ✅ Medium |
| Script debugging | Eliminate scripts — server-side rendering | ✅ If image gen works |
| PS lockout | Move rendering off Photoshop entirely | ✅ If image gen works |
| Version control | Built into app (Supabase job history) | ✅ Easy |

## Key Insight
**The entire workflow hinges on Photoshop Smart Objects.** If ListingForge can replicate Smart Object behavior (overlay design onto device template with correct transforms), it replaces Steps 4-12 entirely. That's 9 of 14 steps = ~65% of the work.

But the quality bar is HIGH — logos can't cross panel breaks, crests can't be distorted, legal lines must be readable. This is why the image gen test harness is critical before building the full app.

## Existing Assets (on Drive)
- 5 console templates already digitized as JSON configs:
  - PS5 Standard, PS5 Slim Digital, DualSense Edge, Asus ROG Ally, Steam Deck
- Reference mockup images (LFC iPhone 16 Pro, MCFC Samsung S25/Ultra)
- Design automation SOP + replication guide PDF

## Next Steps
1. Pull one of the console template JSONs + a reference mockup
2. Test if Gemini/DALL-E/Midjourney can place a design onto the template with correct transforms
3. Compare output quality to Photoshop Smart Object output
4. Score with Cem/Jeff → go/no-go on ListingForge build
