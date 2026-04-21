# ListingForge — Strategic Review
> Reviewed by: Ava | Date: 2026-03-06
> Original spec by: Harry (2026-02-08)

## Why This Matters Now
Image replication is confirmed as the **#1 bottleneck** across all projects (ecellglobal.com, microsites, new listings, marketplace expansion). From the March 5 BPA deep dive:
- Jessie Morales (Replication Lead) does **630 SKU replications/day** manually
- 6 creative staff + 8 listing staff = significant headcount on repetitive work
- Strategic goal: reduce ~16 PH heads via automation → ~$105K/yr savings

**With 95,640 Walmart SKUs (99.9% zero reviews) and 3.44M Amazon SKUs (100% FBM), the catalog scale makes manual listing creation unsustainable.**

## Spec Assessment

### What's Good
- **Phase strategy is right** — internal tool → dogfood → SaaS. Classic.
- **Tech stack is solid** — Next.js + Supabase + Vercel = our standard stack, free/cheap to run
- **Schema is well-designed** — proper RLS, audit trail, job queue
- **UI flow is logical** — upload → generate → review → export

### Concerns & Gaps

1. **Image generation quality is the whole ballgame.** The spec hand-waves with "refine iteratively" and depends on Jeff's Gemini prompt. Without high-quality mockups, nothing else matters. We need to validate image gen quality BEFORE building the full app.
   - **Recommendation:** Build a standalone image gen test harness FIRST. Upload 10 designs, generate mockups, get Jeff + Cem to score them. If quality < 80% acceptable, the app is premature.

2. **Scale mismatch.** The spec says "300+ devices" but our actual catalog is massive (3.44M Amazon SKUs). Phase 2 batch processing isn't optional — it's a Phase 1 requirement for internal use.
   - **Recommendation:** Build batch processing into MVP or the tool won't get adopted.

3. **No integration with existing PH workflow.** Jessie's team uses specific templates/processes. If ListingForge doesn't fit their flow, it'll be shelfware.
   - **Recommendation:** Interview Jessie or review EOD Slack logs (now in Airweave) to understand current process before building.

4. **Missing: device template library.** Mockup generation needs device frame templates (phone outlines, angles). Where do these come from? Stock? AI-generated? Jeff's existing assets?
   - **Recommendation:** Audit existing template assets before starting build.

5. **Content gen is the easy part.** With Gemini Flash, this is nearly solved. But the value proposition is 90% images, 10% copy.

## Priority vs. Other Projects

| Project | Revenue Impact | Cost Savings | Effort | Priority |
|---------|---------------|-------------|--------|----------|
| Target+ Migration | HIGH (live revenue at risk) | Medium | Low | **P0 — THIS WEEK** |
| ListingForge MVP | Medium-High (enables scale) | HIGH ($105K/yr) | High (4-6 weeks) | **P1 — Start after Target+** |
| Command Center Phase 2 | Low (internal tool) | Low | Medium | P2 |
| GoHeadCase POC | Medium | None | High | P2 |
| Email Triage | Low | Low | Medium | P3 |

## Recommended Next Steps
1. **Validate image gen** — Build test harness this week (Codex agent, 1 day)
2. **Audit PH workflow** — Pull Jessie's EOD logs from Airweave Slack data
3. **Audit device templates** — Check Drive for existing mockup templates
4. **Start ListingForge build** after Target+ deep dive (March 10+)
5. **Assign to Forge (Codex)** — This is a coding task, not a strategy task

## Open Question for Cem
Jeff's Gemini prompt for mockup generation — do we have access to it yet? This is the single biggest dependency.
