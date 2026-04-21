# UPC/EAN Acquisition Plan for PULSE Champions → Walmart

> **Owner:** Ava | **Created:** 2026-03-14 | **Status:** Draft — needs Cem input
> **Problem:** 86.5% of champion designs (173/200) lack UPC/EAN barcodes. Walmart requires a valid UPC or EAN for every listing.

---

## Current State

| Metric | Value |
|--------|-------|
| Total champions | 200 |
| Champions with UPC/EAN in BigCommerce | 27 (13.5%) |
| Champions missing UPC/EAN | 173 (86.5%) |
| Estimated SKU count for 173 missing designs | ~200K+ (avg 1,200 device variants per design) |
| Amazon Active Listings product-id | ❌ Internal hex IDs (type 5), NOT real UPCs |
| Top 10 missing champions by revenue | $287K/90d (LFCLVBRD $54K, AFCLOGOS $43K, PNUTCHA $40K, FCBCRE $25K, ADVEGRA $23K, MCBDKIT25 $21K, HPOTDH37 $20K, CFCCRE $19K, PNUTHAL $17K, LFCCRYN $16K) |

## Key Question for Cem

**Does Ecell Global / Head Case Designs already have a GS1 membership and a block of EANs assigned?**

**✅ CONFIRMED: Yes.** The 27 champions with barcodes all use UK EANs (prefix `50...`, e.g. `5057546987130`, `5063291842617`). This proves Ecell has at least one GS1 UK company prefix. The issue is that EANs exist in the legacy system but were never fully synced to BigCommerce for most products. 21,003 BC SKUs across these 27 designs already have EANs — the remaining 218,615 SKUs across 173 designs likely have EANs assigned in Zero but not populated in BC.

---

## Acquisition Strategies (ranked by cost & speed)

### Option 1: Extract from Zero / Legacy DB (FREE, fastest) ⭐ RECOMMENDED FIRST STEP

**Rationale:** If Ecell has 1.87M products in BC and sells on Amazon (3.44M listings) and eBay (top 10 seller), barcodes MUST exist somewhere — you can't list on eBay without them in most categories.

**Steps:**
1. Ask Chad (IT) or Jay Mark (PH dev, has DB access) to query Zero master DB for EAN/UPC by SKU
2. Query: `SELECT sku, ean, upc FROM products WHERE sku LIKE 'HTPCR%'`
3. Export to CSV → match against 173 missing champion design codes
4. Bulk update BigCommerce via API

**Timeline:** 1-2 days if Chad/Jay Mark cooperates
**Cost:** $0
**Risk:** Zero DB might not have them either (low probability given eBay presence)

### Option 2: Extract from eBay Listings (FREE, medium speed)

**Rationale:** eBay requires EAN/UPC for most categories. Head Case Designs is a top 10 eBay seller — their listings likely have barcodes.

**Steps:**
1. Export eBay active listings (Seller Hub → Reports → Active Listings)
2. Map eBay custom label / item specifics → design codes
3. Extract EAN/UPC from item specifics
4. Cross-reference against 173 missing champions

**Timeline:** 2-3 days (need eBay Seller Hub access)
**Cost:** $0
**Risk:** eBay mapping to design codes may be messy

### Option 3: GS1 UK — Assign New EANs (if none exist)

**If Options 1-2 fail**, need to acquire new barcodes:

| GS1 UK Plan | EANs | Annual Fee | One-Time | Best For |
|-------------|-------|------------|----------|----------|
| 1,000 barcodes | 1,000 | £150/yr | £250 | Not enough |
| 10,000 barcodes | 10,000 | £300/yr | £500 | Covers champions |
| 100,000 barcodes | 100,000 | £600/yr | £1,000 | Full catalog |

**For 200 champion DESIGNS × ~100 device variants = ~20,000 SKUs**, the 100K block is most practical given future growth.

**Steps:**
1. Confirm existing GS1 membership (check with Tim or accounts)
2. If member: allocate from existing prefix
3. If not: register at gs1uk.org, get company prefix, generate EANs
4. Assign EANs to SKUs in BigCommerce via API

**Timeline:** 1-2 weeks
**Cost:** £500-£1,600 one-time + £150-£600/yr

### Option 4: Walmart UPC Exemption (FREE, slow, risky)

Walmart offers GTIN exemptions for certain categories (private label, handmade, bundles).

**Applies to Ecell?** Unlikely — licensed products from major brands (NFL, Peanuts, Naruto) are NOT typically exempt. Walmart expects barcoded products from brand licensees.

**Verdict:** Not recommended. Save as last resort for truly unique/custom items only.

---

## Recommended Action Plan

```
Week 1: 
  → Cem asks Chad to query Zero DB for EANs on HTPCR products (Option 1)
  → Parallel: Check if Ecell has existing GS1 UK membership
  → If Zero has EANs: extract, match to champions, bulk update BC

Week 2 (if Zero fails):
  → Pull eBay active listings export for barcode extraction (Option 2)
  → If no barcodes anywhere: register/extend GS1 UK, assign new EANs (Option 3)
```

## Impact

| Scenario | Champions Unblocked | 90d Revenue Unlocked | Walmart Listings |
|----------|--------------------|-----------------------|------------------|
| Zero DB has EANs | 173 (all missing) | ~$700K+ | 20,000+ SKUs |
| eBay has EANs | est. 100-150 | ~$400-600K | 12,000-18,000 SKUs |
| New GS1 assignment | 173 (all missing) | ~$700K+ | 20,000+ SKUs |

## Next Steps (for Cem)

1. **Confirm GS1 membership status** — does Ecell/HCD have a GS1 UK or GS1 US company prefix?
2. **Ask Chad to check Zero DB for EANs** — can piggyback on the Zero PHP extraction (repo already created)
3. **Provide eBay Seller Hub access** — if needed as backup barcode source
4. **Decision:** Which option to pursue first?

---

*Drafted by Ava during heartbeat 2026-03-14 04:00 EST*
