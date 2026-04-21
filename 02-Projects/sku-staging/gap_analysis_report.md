# Design Code Gap Analysis Report
Generated: 2026-03-29 | Source: Active Brands License Mapping.xlsx vs Amazon Active Listings

---

## A) SUMMARY

| Metric | Count |
|--------|-------|
| Licensed brand codes (spreadsheet) | 399 |
| Active design codes on Amazon | 4,108 |
| Brand codes with ≥1 Amazon listing | **366 (91.7%)** |
| Brand codes with NO Amazon listing | **14 (3.5%)** — Active gaps |
| Amazon codes with no brand match | 1,448 (unlicensed / flags / national) |

**Coverage is strong — 92% of licensed brands are live on Amazon.**
The 14 missing brands are the actionable gap list.

---

## B) PER-LICENSOR COVERAGE

| Licensor | Total Codes | On Amazon | Gaps |
|----------|-------------|-----------|------|
| Warner Bros & Time Warner | 163 | 162 (99%) | 1 |
| Warner Music | 13 | 12 (92%) | 1 |
| Bravado (UMG) | 38 | 35 (92%) | 3 |
| IMG | 18 | 18 (100%) | 0 |
| Ubisoft | 14 | 12 (86%) | 2 |
| Toei Animation | 3 | 3 (100%) | 0 |
| EA and BioWare | 2 | 2 (100%) | 0 |
| Independent Artists | 27 | 27 (100%) | 0 |
| MGL Licensing | 2 | 2 (100%) | 0 |
| Lo Coco Licensing | 2 | 2 (100%) | 0 |
| Global Merchandising | 3 | 3 (100%) | 0 |
| Art Licensing | 3 | 3 (100%) | 0 |
| Tate and Co | 8 | 8 (100%) | 0 |

---

## C) TOP BRAND COVERAGE (by Amazon SKU count)

| Brand Code | Design Name | Design Variants | Amazon SKUs |
|-----------|-------------|-----------------|-------------|
| WWE | World Wrestling Entertainment | 177 | 112,150 |
| HPOT | Harry Potter | 86 | 76,148 |
| LFC | Liverpool FC | 64 | 69,979 |
| MC | Manchester City FC | 81 | 80,966 |
| IMGC | IMG College (US Universities) | 57 | 56,489 |
| NHL | National Hockey League | 41 | 52,937 |
| PNUT | Peanuts | 36 | 42,325 |
| ASSA | Assassin's Creed (Ubisoft) | 40 | 44,620 |
| WFC | West Ham United | 41 | 46,580 |
| NARU | Naruto (Toei) | ~30 | ~35,000 |

---

## D) ACTIVE LICENSED BRANDS NOT ON AMAZON (14 Gaps)
*These are active licenses we hold but have zero Amazon listings.*

| Priority | Brand Code | Design Name | Category | Action |
|----------|-----------|-------------|----------|--------|
| 🔴 High | BVROD | Rod Stewart | Music | Check if license still active — Bravado |
| 🔴 High | BVTUP | Tupac Shakur | Music | High-demand artist — why not listed? |
| 🔴 High | BVBB | The Beach Boys | Music | Classic brand — investigate |
| 🟡 Medium | WMJHA | Jack Harlow | Music | New artist — may need fresh designs |
| 🟡 Medium | BEAN | Beano | Entertainment | UK heritage brand — list on .co.uk? |
| 🟡 Medium | TOFC | Toulouse FC | Sports | French football — EU/OnBuy focus |
| 🟡 Medium | WDOG2 | Watchdogs 2 (Ubisoft) | Gaming | Gaming license — check if expired |
| 🟡 Medium | MHUNS2 | Monster Hunter Stories 2 | Gaming | Gaming license — Capcom? |
| 🟢 Low | TOMCGRW | Tom Clancy GRW | Gaming | Old Ubisoft title — low demand |
| 🟢 Low | WACK16 | Wacky Races 2016 | Entertainment | Dated property |
| 🟢 Low | BORE | Bored of Directors | Arts | Niche |
| 🟢 Low | RKAL | Rainer Kalwitz | Arts | Individual artist |
| 🟢 Low | DUPR | Dukla Praha | Arts | Very niche |
| 🟢 Low | LANT | Lantern Press | Arts | Art print — investigate |

---

## E) AMAZON CODES WITH NO LICENSE MATCH (1,448 codes)
Top candidates to investigate (high SKU count but no brand prefix match):

| Amazon Code | SKUs | Notes |
|-------------|------|-------|
| FLAG / CFLAGS | ~5,000 | National flags — not licensed, owned IP |
| NBA2xxx | ~10,000 | NBA city/team specific sub-codes |
| SHSXXX | Various | Unknown prefix |
| FBRE, FLP | Various | Possible FBA-prefix codes or legacy |

*These 1,448 codes likely include: (1) national/novelty designs we own outright, (2) sub-brand codes using different prefixes than the master list, (3) legacy codes predating the current naming convention.*

---

## RECOMMENDATIONS

1. **Immediate (this week):** Investigate Rod Stewart, Tupac, Beach Boys — all Bravado/UMG licenses. High-demand music artists with zero listings is unusual.
2. **Short-term:** Audit the 1,448 unmatched Amazon codes — create a supplementary mapping for sub-codes not in the master spreadsheet.
3. **Data fix:** Expand the design code spreadsheet to include sub-brand codes (e.g. `NARUICO`, `NARUCHA` not just `NARU`) for true 1:1 mapping.
4. **Load to Supabase:** Use the `design_codes` table (schema shared earlier) as the living version of this spreadsheet — queryable by Jay Mark and Harry.
