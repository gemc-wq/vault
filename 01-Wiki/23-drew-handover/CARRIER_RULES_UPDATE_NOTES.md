# Carrier Rules — Updated Requirements (Cem, March 9 2026)

## Key Changes from Original Matrix

### 1. Veeqo Gap Analysis Required FIRST
- Harry must investigate what Veeqo CAN and CAN'T do for automation rules
- Need full gap analysis before committing to Veeqo for everything
- Time saved from removing manual triggers could be wasted if Veeqo lacks flexibility

### 2. Non-Amazon Labels: Not Tied to Veeqo
- Could use ShipStation or another provider for non-Amazon labels
- UK and US must be evaluated SEPARATELY — different providers may win
- Multiple providers exist — need comparison analysis

### 3. Country Routing Simplified
- **US = US states ONLY** (domestic)
- **UK = UK domestic + ALL international** (except Japan)
- **Japan** = separate routing (PH production, small stickers)
- NO separate EU routing — it all goes through UK

### 4. Carrier Change: EVRI Replaces Deutsche Post
- **EVRI** is the new international carrier (NOT Deutsche Post)
- Need cost analysis: Royal Mail International vs EVRI split
- Country-by-country analysis needed for RM vs EVRI routing
- EVRI integration is a **separate project**

### 5. SKU Parsing Drives Everything
- Package sizing and product routing rules come from SKU parsing
- Example: `HTPCR-IPH17` = HardCase TPU Clear - iPhone 17
- SKU prefix determines:
  - Product type (case, skin, desk mat, sticker)
  - Device model
  - Equipment requirements (which sites can produce)
  - Inventory deduction (blank case matching)

### 6. Equipment-Restricted SKU Prefixes (STRICT RULES)
- **HDMWH** (Desk Mats) → NEVER PO to Philippines (no equipment)
- **H89 / H90** (Skins) → NEVER PO to Philippines
- **HSTWH** (Stickers) → NEVER PO to Philippines
- These are hard rules for the routing engine — not overridable

### 7. Inventory Management (Separate Project with Harry)
- When SKU `HTPCR-IPH17-XXXX` sells → deduct 1 unit of blank `HTPCR-IPH17`
- Need: supplier order tracking + reorder level triggers
- This is the Finance/Ops pillar work — Harry builds, Ava reviews

### 8. Label Sorting Requirement (OPERATIONAL)
- ALL shipping labels MUST be sorted by SKU alphabetically
- Reason: print files are sorted by SKU → labels must match order
- If labels come from multiple sources (Veeqo + Stamps), operators get two unsorted stacks → mismatch nightmare
- **Strong argument for single provider** (all labels from one source, sorted consistently)
- If using multiple providers: must merge and re-sort before printing

## PO Wave Sequencing (Timezone-Driven)

**Philippines is +8 UK, +12 US.** This drives the entire PO wave order:

### Wave Priority:
```
1. PH FIRST (morning PH time = overnight UK/US)
   → PO all Philippines-stock items first
   → PH team starts printing immediately
   → Generate PH labels → image gen → print files → production

2. UK SECOND (morning UK time)  
   → Whatever remains after PH allocation
   → UK labels generated, sent to GDrive
   → Same-day shipping cutoff: ~2-3 PM UK local

3. US THIRD (morning US time)
   → Remaining US-stock items
   → FL labels generated, sent to GDrive  
   → Same-day shipping cutoff: ~2-3 PM EST

4. AFTERNOON WAVES (smaller batches)
   → Late-arriving orders for same-day cutoff
   → UK afternoon PO, US afternoon PO
   → These are smaller volume
```

### Rationale:
- PH gets the head start (12 hours ahead of US)
- PH processes their print files while UK/US are still sleeping
- UK and US operators arrive to labels already waiting in GDrive
- Afternoon waves handle stragglers for same-day cutoff

## Rule Simplification Insight (Cem, March 9)

The PHP code is ~1,300 lines likely because it **parses SKU for every order** — the length is SKU-driven iteration, not rule complexity. The actual business rules are:

### Hard Rules (Fixed):
1. **Location PO rules** — based on inventory location + equipment capability
   - HDMWH (desk mats) → NEVER PH
   - H89/H90 (skins) → NEVER PH  
   - HSTWH (stickers) → NEVER PH
   - Dynamic override: printer down → divert to PH (done ahead of time)
2. **Carrier rules** — straightforward and fixed per region
   - Amazon → Always Buy Amazon Shipping
   - US non-Amazon → Stamps/Veeqo
   - UK domestic → Royal Mail
   - International → Royal Mail vs EVRI (cost split TBD)
   - Japan → PH small stickers

### Dynamic Rules:
- Location-based (inventory availability at each site)
- Equipment overrides (printer downtime → PH fallback)
- These change operationally, not programmatically

## SO/PO Process — SEPARATE (Finance)
- Intercompany billing task — NOT part of shipping migration
- Harry owns this as Finance/Ops pillar
- **However:** Harry DOES need to own the final handoff to ImageGen (shipped export → print files)

## Implications

1. **Single provider preferred** — operationally, one label source sorted by SKU is far cleaner than merging from multiple
2. **Veeqo gap analysis is P0** — before we invest in configuration, Harry must confirm Veeqo can handle: carrier rules, SKU-based routing, label sorting, automation flexibility
3. **EVRI is a new workstream** — requires carrier account setup, API integration, cost analysis by country
4. **Inventory management ties into this** — SKU parsing is the shared foundation across shipping rules, production routing, AND inventory
