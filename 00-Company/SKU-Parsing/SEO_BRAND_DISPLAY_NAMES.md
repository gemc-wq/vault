# SEO Brand Display Names
*Owner: Ava | Created: 2026-04-09 | LLM-verified + Cem-reviewed*

## Purpose
This table defines the **consumer-facing SEO display name** for each brand code used in product titles across Shopify, Walmart, Amazon, and all marketplaces.

## Rules Applied
1. **Strip licensor prefix** — remove "Time Warner", "Bravado", "Universal Studios", "Ubisoft" etc.
2. **Strip internal suffixes** — remove "Core", "Custom", "Classic", "TV Series", "Movie YYYY", "Franchise"
3. **Normalise case** — no ALL CAPS; use standard title case
4. **Use the consumer search term** — what people actually type into Amazon/Google
5. **IMGC** — use per-design university name from `imgc_design_map.json`, not "IMG College"

---

## Verified SEO Names

| Code | Internal Label | ✅ SEO Display Name |
|---|---|---|
| AFC | Arsenal Football Club | Arsenal FC |
| ATM | Atletico de Madrid | Atletico Madrid |
| AVLA | Aston Villa FC | Aston Villa FC |
| BHA | Brighton & Hove Albion F.C | Brighton & Hove Albion FC |
| BTMC | Time Warner Batman Core | Batman |
| BVBE | Bravado - BILLIE EILISH | Billie Eilish |
| BVGUN | Bravado Guns N Roses | Guns N' Roses |
| BVQUEE | Bravado Queen | Queen |
| BVRS | Bravado The Rolling Stones | The Rolling Stones |
| BVSK | Bravado Slipknot | Slipknot |
| CFC | CHELSEA FOOTBALL CLUB | Chelsea FC |
| DRGBS | Dragon Ball Super | Dragon Ball Super |
| EVFC | Everton FC | Everton FC |
| FCB | FC BARCELONA | FC Barcelona |
| HPOT | Time Warner HARRY POTTER | Harry Potter |
| IMGC | IMG College | *(use university name from imgc_design_map.json)* |
| IRON | Iron Maiden | Iron Maiden |
| JFC | Juventus Football Club | Juventus FC |
| LFC | Liverpool Football Club | Liverpool FC |
| MC | Manchester City Football Club | Manchester City FC |
| NARU | Naruto Shippuden | Naruto Shippuden |
| NBA | National Basketball Association | NBA |
| NCFC | Newcastle United Football Club | Newcastle United FC |
| NFL | National Football League | NFL |
| NHL | National Hockey League | NHL |
| OHIO | Ohio State University | Ohio State University |
| PNUT | PEANUTS | Peanuts |
| RMCF | Real Madrid CF | Real Madrid |
| RMOR | Rick And Morty | Rick and Morty |
| STREK | Star Trek | Star Trek |
| THFC | Tottenham Hotspur F.C. | Tottenham Hotspur FC |
| WFC | West Ham United Football Club | West Ham United FC |
| WWE | World Wrestling Entertainment | WWE |

---

## Machine-Readable Version
`seo_brand_display_names.json` — same directory. Use this in all listing generation scripts.

## Status
- ✅ 33 codes verified (Apr 9 2026) — covers all current Shopify products + top sellers
- ⏳ Remaining ~720 codes from `SKU_Parsing_by_Brand.txt` — to be processed in batches

## Next Steps
1. Re-apply corrected SEO names to all 248 live Shopify titles
2. Process remaining 720 codes in batches of 50 via LLM
3. Use `seo_brand_display_names.json` as the lookup in all future upload scripts

---
*Source: LLM verification (Codex gpt-5.4) + Cem's rule: strip licensor prefix + internal suffixes*
