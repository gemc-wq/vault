# Skill: Creative & Design
**Weight: 30% | Heartbeat: 3x per cycle | Agent: Sven (rebuild)**

---

## Why #1
In POD e-commerce, the product IS the design. Sales are driven by image quality. Casetify hit $300M by going creative-first, ops-second. Without compelling visuals, every other skill stalls — listings can't convert, marketing has no content, new licenses can't launch.

## Scope
- Product image generation (mockups, lifestyle, marketing)
- Design direction briefs for PH creative team
- Competitor visual research and benchmarking (Casetify grade)
- Email campaign visuals (11K GoHeadCase subscribers, zero campaigns)
- License launch creative packages (One Piece = pilot)
- Social media visual content
- Presentation assets with real product imagery

## Agent: Sven (Rebuild Spec)
- **Primary model:** Gemini 3.1 Pro (image understanding + generation)
- **Secondary:** OpenAI Image Gen 2 (high-quality product renders)
- **Corpus:** Casetify benchmarks at `02-Projects/goheadcase/rag/benchmarks/`
- **Output channel:** Slack #creative, #graphics
- **Workflow:**
  1. PULSE or Cem identifies design/license → Creative skill triggers
  2. Sven receives brief: design assets, competitor examples, target products
  3. Sven generates: 3-5 marketing concepts, visual direction doc, reference board
  4. Posts to Slack #creative for PH team
  5. PH designers execute precision mockups and listing images
  6. Sven reviews output against Casetify benchmark quality

## Active Projects
| Project | Status | Priority |
|---------|--------|----------|
| One Piece creative direction | 🟡 Needs visual brief | P0 |
| Sven agent rebuild | 🔴 Not started | P0 |
| GoHeadCase email content | 🔴 Zero campaigns, 11K subs | P1 |
| Product photography AI upgrade | 🟡 Midjourney/NanoBanana2 viable | P1 |
| IREN/DRECO modernization (Lane 2) | 🟡 Print automation | P2 |

## Key Metrics
- Time from design brief → listing-ready images
- Number of AI-assisted vs manual-only product images
- GoHeadCase email campaign open/click rates (once started)
- Casetify quality score (subjective benchmark, 1-10 per image set)

## Context (from Ava's memory)
- Image Automation = #1 bottleneck. Once solved: <1 min per SKU.
- 13 canvas templates per design → DRECO renders per device → S3 upload
- S3 CDN: elcellonline.com/atg/{DESIGN}/{VARIANT}/{PREFIX}-{DEVICE}-{POS}.jpg
- Cem proved workflow: Google AI Studio + ChatGPT/Ava prompts → microsites (anime site, GoHeadCase)
