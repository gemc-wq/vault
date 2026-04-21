# Content Drop — April 1, 2026

## Decisions
- **Inventory Ordering App Scope**: Cem confirmed the scope includes the UK, PH, and FL sites.
- **Inventory Page Requirements**: Each site page must feature the top 50 selling items and include "on order" quantities.

## Deliverables
- **Head Case Content Drop**: Completed 5-7 product descriptions and social media posts for NFL, Anime, WWE, Harry Potter, Peanness, and Gaming/Retro collections.
- **Universal Template**: Created a customizable "Officially Licensed [BRAND] Soft Gel Case" template.
- **Documentation**: Established new Wiki project at `wiki/inventory-ordering-app/PROJECT.md`.

## Knowledge
- **Inventory Traffic Light Logic**: 
    - **Red**: < 14 days stock
    - **Amber**: < 21 days stock
    - **Green**: 21+ days stock
- **Stock-out Estimation Logic**: Calculate days cover using a weighted average of the last 7 and 30 days sales (heavier weighting on the last 7 days), including a flag for material velocity deviations.
- **Head Case Brand Voice**: Conversational, "You/your" focused, detail-oriented, and avoids "exclamation point spam."
- **Technical Details**: 
    - Procurement codebase location: `tmp/procurement-system`.
    - Frontend must adhere to the app style guide located in the Wiki.

## Carry-forwards
- **Marketing Execution**: 
    - Pair new copy with product photography.
    - A/B test long vs. short descriptions on Amazon.
    - Develop TikTok series: "POV: You found the case."