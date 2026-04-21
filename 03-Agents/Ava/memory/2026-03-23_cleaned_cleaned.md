# 2026-03-23 — Daily Notes

## Decisions
- **New Product Lines Approved (by Cem):** MagSafe Water Bottles and Aluminium Metal Wall Art.
- **Licenses Approved:** Man City, Tottenham Hotspur, and Warner Brothers (Batman, Harry Potter, Looney Tunes).
- **Sven (Gemini) Directive:** Must serve as the final content creator to achieve Casetify-quality standards (demonstrating product features), not merely as a mockup tool.
- **Target Plus Strategy:** Shopify is the confirmed distribution hub; all products added to Shopify automatically flow to Target Plus.

## Deliverables
- **New Product Documentation Package:** Located in `projects/new-products/` (includes `CREATVE_STANDARDS.md`, `CONTENT_RESEARCH_GUIDE.md`, `STYLE_GUIDE_BRIEF.md`, and `AI_IMAGE_PROMPTS.md`).
- **Creative Direction Deck:** [Gamma Presentation URL](https://gamma.app/docs/bd1bd9zy8bgq7).
- **Slack Brief:** Posted to `#creative` (C09SVCQS1C2) with 7-image shot lists.
- **Claude Code Listing Engine:** Successfully output 30 items in Walmart template format.

## Blockers
- **Sven (Gemini) Image Generation:** Gemini CLI cannot reliably composite product photos into scenes. 
    - *Resolution:* Transition to OpenAI image API, browser-based Gemini, or utilize the PH team for professional composites.
- **Walmart API Block:** Account-level block on `MP_ITEM` (item creation) is preventing automated uploads.
    - *Workaround:* Manual