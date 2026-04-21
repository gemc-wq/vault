# ATHENA ONBOARDING BRIEF v2
**Prepared by:** Ava (CPO/Strategy)
**Date:** 2026-04-06 (updated from Apr 5 original)
**Purpose:** Current state brief — verified by Ava before Athena proceeds

---

## 🏢 WHO WE ARE

**Ecell Global** — licensed tech accessories manufacturer. $5M+ annual revenue.
- **Offices:** Orlando FL (US), UK, Philippines (PH), Japan, Hong Kong
- **Retail brand:** Head Case Designs
- **Products:** HTPCR, HB401, HLBWH, HB6CR, HB7BK, HC (phone cases), HDMWH (desk mats), H8939 (gaming skins)
- **Marketplaces:** Amazon (US/UK/DE), Shopify (→Target Plus), TikTok Shop, Walmart (staging), GoHeadCase DTC

**North Star:** World's #1 licensed tech accessories company.
1. **Coverage** — every top design on every marketplace
2. **Speed** — order to doorstep < 48 hours
3. **Intelligence** — data-driven decisions

---

## 👥 YOUR TEAM

| Agent | Role | Model | Status |
|-------|------|-------|--------|
| **Ava** | CPO / Strategy | Sonnet 4.6 | Active |
| **Harry** | COO / Builder | Sonnet 4.6 (iMac) | ⚠️ Underperforming — 3rd week of low output |
| **Hermes** | Analyst | Kimi K2.5 | Active |
| **Jay Mark** | PH AI Guy | Human | Back today (Apr 7) |
| **Sven** | Creative Director | Gemini 3.1 Pro | Active |
| **Echo** | Copywriter | Sonnet 4.6 | On call |
| **Pixel** | Data/ETL | Gemini Flash | ✅ Auth fixed Apr 6 |
| **Bolt** | Research/Scout | Gemini Flash | ✅ Auth fixed Apr 6 |

**Cost rule:** All crons and background jobs on FREE models only. Never Anthropic API for background work.

---

## 🔑 WHAT HAPPENED SINCE APR 5

### Major wins:
1. **One Piece license SIGNED** — 15% royalty, Apr 2026–Mar 2028, 7 product types
2. **One Piece creative brief live** → https://gamma.app/docs/exyhd5wbvbf1hw3 — posted to #creative
3. **Bea (PH Creative Manager) briefed** — asked to create FigJam board for One Piece
4. **Operational Blueprint V3 written** — the new canonical end-to-end process map (wiki/OPERATIONAL_BLUEPRINT_V3.md)
5. **Amazon Middleware API confirmed live** — request + poll + download working. BQ loader needs chunking fix.
6. **Vault structure live on GDrive** — Brain/ava-obsidian-vault/harry/ synced with Harry's projects + memory
7. **All 6 Gemini agents re-authenticated** — Pixel, Bolt, Sven, Atlas, Prism, Sven2 all working
8. **Jig data extracted** — 8,199 device rows incl iPhone 17, Samsung S25 → Brain/Projects/listing-forge/
9. **Shopify product upload SOP written** — titles, images, inventory=9999 rules codified

### What Jay Mark starts today:
- New Supabase tables for design code → listing tracking (One Piece pilot)
- Fulfillment Portal testing (Harry's spec)
- Jig data validation for modern devices (iPhone 13–17, Samsung S21–S25)

---

## 📋 CURRENT PROJECT STATUS (verified Apr 7)

### 🔴 P0 — CRITICAL THIS WEEK

**1. One Piece Launch Pipeline**
- Creative: Brief sent to #creative, Bea creating FigJam board ✅
- Design codes: Jay Mark entering in new Supabase tables TODAY
- Next: ListingForge images once 5 designs approved
- Target: First 100 SKUs live Amazon US by end of week 2
- **Athena action:** Coordinate Jay Mark + Forge for the full pipeline

**2. Inventory Alert System (Harry's P0)**
- Harry has: DB schema (11 tables), Airweave stock-out monitor, blank_inventory table
- Missing: Daily alert script per office (UK/PH/FL) in multilingual format
- Languages: UK=English, PH=Tagalog/English, FL=Spanish/English
- Traffic lights: RED <14d, AMBER <21d, GREEN 21d+
- **Athena action:** Push Harry to deliver this week. If blocked, escalate to Cem.

**3. Fulfillment Portal (Harry)**
- Spec complete: Brain/ava-obsidian-vault/harry/projects/FULFILLMENT_PORTAL_SPEC.md
- Jay Mark = tester/operator
- **Athena action:** Brief Jay Mark today. Connect him to Harry for setup.

**4. BQ Loader Chunking Fix**
- Amazon Middleware API works perfectly EXCEPT bulk load to BQ OOM-crashes on large files
- Fix: stream-insert in 10K row chunks in bigquery_loader module
- **Athena action:** Assign to Harry. This unblocks the full weekly automation pipeline.

### 🟡 P1 — THIS WEEK

**5. Xero OAuth**
- Harry's Xero Finance App is blocked on UK + US OAuth credentials
- Cem needs to: go to developer.xero.com → copy Client ID + Client Secret for both orgs → send to Ava
- **Athena action:** Get this from Cem and relay to Harry securely

**6. Amazon Product Listing Scope**
- Currently Middleware = Reports only. Listings/Feeds API = Unauthorized.
- Fix: Cem adds "Product Listing" role in Seller Central → App & Services → edit app
- **Athena action:** Get Cem to add the scope. This unlocks bulk listing uploads + price changes.

**7. Shopify Bulk Upload (1,803 HB401 gaps)**
- EANs assigned, images from S3, CSV ready
- Blocked on: Cem go-ahead + SOP compliance (titles must use brand names not design codes)
- **Athena action:** Get Cem's approval to proceed with corrected SOP

**8. PO Corrections**
- From Harry's gap analysis: 11 EOL items to remove, HTPCR-IPH17PRO negative qty (-163), approve 70/15/15 shipping split
- **Athena action:** Get Cem decision on all three before next PO cycle

### ✅ RESOLVED (no action needed)

- NFL: 90-day sell-off window confirmed, reminder set for May 6
- Gemini agents: All re-authenticated Apr 6
- Jig data: Extracted and on GDrive
- Vault: Harry's projects synced

---

## 📊 OPERATIONAL BLUEPRINT V3

The new end-to-end process map is at: `wiki/OPERATIONAL_BLUEPRINT_V3.md`
GDrive: `Brain/Strategic/OPERATIONAL_BLUEPRINT_V3.md`

**10 stages:**
1. License Onboarding → ecell.app/licenses (to build)
2. Creative → Sven + PH team
3. SKU Generation → auto from design codes
4. ListingForge → composite images
5. Content → Echo
6. Listing Upload → Shopify + Amazon + Walmart
7. Print File Monitoring → Jay Mark's new tables
8. Fulfillment Portal → Harry
9. Finance → Xero app
10. Intelligence → PULSE + Hermes

**Athena's role:** Own stages 1–6 coordination. Delegate execution. Escalate blockers to Cem as one bundled message max once per day.

---

## 🧠 RULES OF ENGAGEMENT FOR ATHENA

1. **Read OPERATIONAL_BLUEPRINT_V3.md first** — that is the process. Everything maps to it.
2. **Harry is underperforming.** Don't wait for him to self-report. Check his deliverables daily. Escalate to Cem if he misses a 2-day deadline.
3. **Jay Mark is new and eager.** Give him clear, specific tasks. He can execute well with good briefs.
4. **Cost-aware routing.** Mechanical/repetitive tasks → Pixel/Flash (free). Strategy → Ava. Planning → Athena.
5. **One Piece is the pilot.** Every decision should test and prove the full pipeline. What works here scales to every future license.
6. **Never use Anthropic API for background crons.** Free models only for automated jobs.
7. **Bundle questions for Cem.** Max one Telegram message per day with all open questions. Don't drip them.

---

## 📁 KEY FILES

| File | Location | What it is |
|------|----------|------------|
| Operational Blueprint V3 | wiki/OPERATIONAL_BLUEPRINT_V3.md | THE process map |
| One Piece creative brief | projects/one-piece/CREATIVE_DIRECTION.md | Design direction |
| One Piece contract | projects/one-piece/CONTRACT_SUMMARY.md | License terms |
| Gamma deck | https://gamma.app/docs/exyhd5wbvbf1hw3 | Creative deck (live) |
| Harry's projects | Brain/ava-obsidian-vault/harry/INDEX.md | Harry's current state |
| Fulfillment Portal spec | Brain/ava-obsidian-vault/harry/projects/FULFILLMENT_PORTAL_SPEC.md | Build spec |
| Shopify SOP | wiki/27-sku-staging/SOP_SHOPIFY_PRODUCT_UPLOAD.md | Upload rules |
| Listings DB SOP | wiki/31-listings-management/SOP_LISTINGS_DB_MANAGEMENT.md | Delta analysis |

---

*Brief v2 — Ava verified 2026-04-06. Supersedes Apr 5 brief.*
