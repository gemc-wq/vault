# PIE Design Insights — Synthesized from Atlas Analysis
*Date: 2026-03-07 | Source: 304K orders, $6.56M revenue, 3,919 unique designs*

---

## 1. Revenue Concentration — The "216 Rule"

**Elbow point: 216 designs capture ~64% of all revenue.**

| Bucket | Designs | Cumulative Rev | % of Total |
|--------|---------|---------------|------------|
| Top 50 | 50 | $2.34M | 35.6% |
| Top 100 | 100 | $3.25M | 49.6% |
| Top 216 (elbow) | 216 | ~$4.2M | ~64% |
| Top 500 | 500 | $5.34M | 81.3% |
| Long tail | 3,419 | $1.22M | 18.7% |

**Implication for PIE:** The top ~200 designs are the must-haves. The long tail (3,400+ designs) collectively earns less than the top 50. Aggressive pruning is justified.

---

## 2. Brand Power Rankings (Top 50)

| Brand | Designs in Top 50 | Combined Rev | Region Lean |
|-------|-------------------|-------------|-------------|
| Liverpool FC | 8 | $388K | 🇬🇧 UK-dominant (80%+ UK rev) |
| Harry Potter | 6 | $434K | 🌍 Global (US 55%, UK 20%, EU 20%) |
| Peanuts | 6 | $378K | 🇺🇸 US-dominant (65-70% US) |
| Arsenal FC | 6 | $191K | 🇬🇧 UK-dominant (75%+ UK) |
| WWE | 3 | $103K | 🇺🇸 US-dominant (60-65% US) |
| Naruto | 3 | $113K | 🇺🇸 US-dominant (80%+ US) |
| Newcastle Utd | 2 | $92K | 🇬🇧 UK-dominant (95%+ UK) |
| FC Barcelona | 2 | $119K | 🇺🇸🇪🇺 US + EU split |
| Chelsea FC | 1 | $32K | 🇬🇧 UK-dominant |

**Key insight:** UK football clubs (Liverpool, Arsenal, Newcastle, Chelsea, Spurs, Rangers) = 19 of top 50 designs. This is a **UK-first catalog** by design count, even though US generates higher per-design revenue.

---

## 3. Regional Playbook

### 🇺🇸 US Market (Best for Target+, Amazon FBA, DTC)
**Top brands:** Harry Potter, Peanuts, WWE, Naruto, Dragon Ball, Gilmore Girls, Adventure Time, Batman, Billie Eilish, Supernatural
**Top devices:** iPhone 16 series, iPhone 13-15 (strong catalog longevity)
**Desk mats:** Harry Potter (HPOTGRA), Adventure Time, Naruto, Rick & Morty — all show 600X300X3 as top device
**⚠️ Target+ exclusion:** No US sports (NFL/NBA/NHL/NCAA) — but UK football IS allowed

### 🇬🇧 UK Market (eBay, Amazon UK)
**Top brands:** Liverpool FC, Arsenal, Newcastle, Tottenham, Chelsea, Rangers, Man City
**Top devices:** Samsung A16 5G (!), iPhone 12-16, PS5 skins
**Insight:** UK football drives massive volume but ONLY in UK — don't push these on US marketplaces

### 🇪🇺 EU Market (Amazon DE/FR/IT/ES)
**Top brands:** FC Barcelona, Harry Potter, Iron Maiden, Peanuts
**Insight:** EU is a supporting market, not a primary one. Harry Potter + Barcelona travel best.

---

## 4. Product Type Signals (from Top Device Codes)

| Device Code Pattern | Product Type | Appearances in Top 50 | Revenue Signal |
|--------------------|--------------|-----------------------|----------------|
| IPH* | Phone cases (iPhone) | 30+ | DOMINANT |
| A165G | Phone cases (Samsung) | 2 | UK market |
| S921U | Phone cases (Samsung) | 1 | US market |
| 600X300X3 | Desk mats | 3 | High-value, US-leaning |
| DS5CT / DS5EGCT | PS5 Console skins | 5 | UK + US, growing |
| AIRPDPRO | AirPods Pro cases | 1 | US, niche |
| PS5PBD | PS5 controller skins | 1 | UK-only |
| 250X300X3 | Smaller desk mats | 1 | Emerging |

**Insight:** Phone cases dominate, but **desk mats and PS5 skins are in the top 50**. These are NOT niche — they're revenue contributors. PIE must include them.

---

## 5. Emerging Brands to Watch

| Brand | Top 50 Position | Trajectory Signal |
|-------|----------------|-------------------|
| **Naruto** | #15, #31, #45 | 3 designs in top 50, IPH17PMAX showing = current-gen demand |
| **Dragon Ball Super** | #20 | IPH17PMAX top device = current-gen, US-heavy |
| **Billie Eilish** | #36 | Even US/UK/EU split = global appeal |
| **Iron Maiden** | #47 | Unusually balanced across all 3 regions |

These are the "growth" brands vs. the "established" brands (HP, Peanuts, LFC). PIE should weight recent momentum, not just total revenue.

---

## 6. Actionable Recommendations for PIE Scoring

1. **Design-first ranking is validated.** Top 216 designs × complete device families × 4 product types = estimated ~200K SKUs — aligns with PIE target.

2. **Regional segmentation is MANDATORY.** A design's rank should differ by marketplace:
   - US marketplace: rank by US revenue
   - UK marketplace: rank by UK revenue
   - Global DTC (GoHeadCase): rank by total revenue

3. **Product type expansion:** Every top-216 design should have HTPCR + HC + HB401 + HLBWH minimum. Add desk mat (600X300X3) and PS5 skin variants for brands that show demand.

4. **Device recency filter:** Designs showing IPH17PMAX or IPH16 as top device = actively selling on current-gen → prioritize. Designs peaking on IPH7/IPH11 = declining → lower weight.

5. **Currency normalization ready.** Atlas has the conversion rates; needs to be applied in Supabase (blocked on direct DB access). Until then, use Atlas's local calculations.

---

---

## 7. Amazon US Cross-Reference (Jan 1 – Feb 24, 2026)

*Source: `~/results/amazon-us-session-analysis.md` — ~80K rows from Amazon Business Report*

### 🔥 Critical Finding: Desk Mats Dominate Amazon Revenue
The **top 10 Amazon SKUs by revenue are ALL desk mats (HDMWH)**. Not phone cases. Desk mats for Naruto, Harry Potter, Peanuts, and Adventure Time are the single biggest revenue generators on Amazon US.

| Rank | SKU | Revenue | Conv Rate | Sessions |
|------|-----|---------|-----------|----------|
| 1 | HDMWH-600X300X3-NARUGRAT | $1,600 | 3.8% | 1,647 |
| 2 | HDMWH-600X300X3-HPOTGRA | $1,362 | 2.2% | 2,374 |
| 3 | HDMWH-900X400X4-HPOTGRA | $1,348 | 3.5% | 1,278 |
| 4 | HDMWH-600X300X3-NARUGRAT (ITA) | $1,246 | 2.4% | 2,040 |

**Implication:** PIE MUST prioritize desk mat variants for top designs, not just phone cases.

### 📈 Product Type Conversion Rankings (Amazon)
| Product Type | Sessions | Revenue | Conv Rate | Signal |
|-------------|----------|---------|-----------|--------|
| **HB401** | 9.3K | $16K | **8.3%** | 🚀 Massively underinvested — push PPC here |
| HC | 50K | $36K | 3.7% | Solid performer |
| HTPCR | 243K | $170K | 3.3% | Workhorse — highest absolute revenue |
| HDMWH | 57K | $36K | 2.5% | High margin, top individual SKU revenue |
| HLBWH | 85K | $46K | 2.1% | Good volume, Kindle/laptop cases |
| H8939 | 63K | $26K | 2.0% | ⚠️ Console skins: high traffic, poor conversion |

### ⚠️ Buy Box Alert
- **FHC product type: 63.6% Buy Box** — critical. Third-party sellers or hijackers stealing sales. Need Brand Registry takedown audit.
- H7805: 91.8% — borderline, investigate.

### 🎯 Device Insights (Amazon)
- **iPhone 17 Pro Max** = highest revenue device ($19.9K)
- **600x300 desk mats** = #2 device by revenue ($18.8K) — ahead of all other phone models
- **iPhone 15** has best phone conversion rate (4.6%) — legacy traffic converts well
- **Don't sunset older devices** — iPhone 12/14 converting at 7-9% on specific designs

### 💡 Synthesis: Orders Data vs. Amazon Sessions Data
| Insight | Orders Data (304K) | Amazon Sessions (80K) | Aligned? |
|---------|-------------------|----------------------|----------|
| Top brands | HP, Peanuts, LFC, Arsenal | Naruto, Peanuts, HP, Dragon Ball | ⚠️ Partial — UK football absent from US Amazon |
| Top product type | HTPCR, HLBWH, HC | HTPCR revenue, but HB401 best conversion | ✅ HTPCR confirmed #1 |
| Desk mats matter | In top 50 designs | Dominate top 10 SKUs | ✅✅ Even bigger than orders data suggested |
| Emerging brands | Naruto, Dragon Ball | Naruto #1 design by Amazon revenue | ✅ Confirmed growth trajectory |

---

## Next Steps
- [ ] Apply these insights to PIE scoring algorithm (Harry + Atlas)
- [ ] Run regional-specific top-200 for US-only marketplace selection (Target+, Amazon FBA)
- [ ] Cross-reference with BigCommerce catalog to ensure top designs have complete product type coverage
- [ ] Get fresh data from BigQuery (current data is 18 days stale as of Mar 7)
- [ ] **Audit FHC Buy Box immediately** — 63.6% is revenue leakage
- [ ] **Push PPC budget to HB401** — 8.3% conversion is the highest ROI opportunity
- [ ] **Investigate console skin conversion gap** — 63K sessions, only 2% CR on H8939

---

*Source data: `~/results/pie-design-rankings.md`, `~/results/pie-concentration-analysis.md`, `~/results/amazon-us-session-analysis.md`*
*Analysis: Atlas (Kimi K2.5) | Synthesis: Ava (Claude Opus 4.6)*
