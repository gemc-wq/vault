# Carrier Rules Matrix — Zero → Veeqo Migration
*Created: 2026-03-09 | Status: DRAFT — awaiting full PHP codebase for edge cases*
*Source: Patrick's email, PHP screenshot, Cem walkthrough, shipping carrier rules doc*

> ⚠️ **DYNAMIC RULES** — These change based on business needs, carrier pricing, and operational capacity. The Veeqo configuration must be easily editable (UI-based), unlike the hardcoded PHP.

---

## 🔴 CRITICAL: Amazon Buy Shipping Requirement

**ALL Amazon orders MUST go through Veeqo's "Buy Amazon Shipping" integration.**

Why:
- Amazon's **Late Delivery Protection** only applies when using Amazon Buy Shipping
- If Amazon's chosen carrier delivers late, **Amazon absorbs the blame** (no seller metrics hit)
- If we use our own carrier (USPS/FedEx direct) and it's late, **our account takes the hit**
- Account health suspension = catastrophic revenue loss

**Rule: Amazon order → ALWAYS use Veeqo Buy Amazon Shipping. No exceptions.**

---

## Carrier Selection Rules (Current State from Patrick)

### By Region + Channel

| Order Source | Buyer Region | Fulfillment Site | Carrier / Service | Notes |
|-------------|-------------|-----------------|-------------------|-------|
| **Amazon US** | US | FL or PH | **Amazon Buy Shipping** | ⚠️ MANDATORY for late delivery protection |
| **Amazon US** | US (USPS fallback) | FL or PH | USPS Buy Shipping | Only when Amazon Buy Shipping unavailable |
| **Non-Amazon US** (Walmart, eBay, Etsy, Shopify, TikTok, Fanatics) | US | FL | Stamps.com / Veeqo | Veeqo already handles FL non-Amazon |
| **Amazon UK** | UK | UK or PH | **Amazon Buy Shipping UK** | Same late delivery protection logic |
| **Non-Amazon UK** | UK domestic | UK or PH | Royal Mail RM24 Tracked LBT | TRN = Large Letter, TPN = Parcel |
| **Amazon UK** (Buy Shipping) | UK | UK | Amazon-generated RM24 labels | Amazon selects RM24 Tracked LBT |
| **Europe (DE, FR, IT, etc.)** | EU | UK (or PH→UK freight) | Royal Mail International | MTK = Large Letter, MP7 = Parcel |
| **Germany specific** | DE | UK | Royal Mail / Deutsche Post | Cost comparison — cheapest wins |
| **Japan** | JP | PH | Small stickers → PH Production | Unique label format |
| **Rest of World** | International | UK | Royal Mail International | Manual process — NOT yet in Veeqo |

### By Product Type (from PHP)

| Product Code | Product Type | Special Routing | Carrier Impact |
|-------------|-------------|----------------|----------------|
| 90 | Skins | UK or FL only (NOT PH) | Standard carrier per region |
| ST | Stickers | UK or FL only (NOT PH) | Standard carrier per region |
| DM | Desk Mats | Special handling | May affect parcel vs letter |
| A9 | TBD | Excluded from certain PO routes | TBD from PHP |
| B6 | TBD | Excluded from skin routes | TBD from PHP |
| B7 | TBD | Excluded from skin routes | TBD from PHP |
| 89 | Specific skin variant | Separate routing | TBD from PHP |

### By Day/Time (from PHP — Weekend/Holiday Rules)

| Condition | Rule | Label |
|-----------|------|-------|
| Friday after 9 PM | Hold for Monday PH PO | `NonUKBuyerCountryOrdersNonSkinsForMondayPHPO` |
| Saturday before 3 AM | Hold for Monday PH PO | Same as above |
| US orders + skins + hold period | Hold for Monday FL PO | `USBuyerCountryOrdersSkinsHB6HB7HoldForMondayFLPO` |
| US orders + non-desk-mat + non-skins | Route to PH | `USBuyerCountryNonDeskMatSkinsB6B7OrdersPHPO` |

---

## Three-Layer Routing Logic (Veeqo Equivalent)

### Layer 1: Equipment Capability (HARD RULES — not overridable)

| Product Type | UK | FL | PH | Rule |
|-------------|----|----|----|----|
| Skins (H89) | ✅ | ✅ | ❌ | NEVER route skins to PH |
| Stickers | ✅ | ✅ | ❌ | NEVER route stickers to PH |
| Laser-cut | ✅ | ❌ | ❌ | UK only |
| UV-printed cases | ✅ | ❌ | ✅ | UK or PH, not FL |
| Standard cases | ✅ | ✅ | ✅ | Any site |
| Desk mats | ✅ | ✅ | ❓ | TBD — check PH capability |

### Layer 2: Stock Availability (DYNAMIC — checked at PO time)

```
IF buyer_country IN (US countries) AND product available at FL:
  → Route to FL
ELIF buyer_country IN (UK countries) AND product available at UK:
  → Route to UK  
ELIF product available at PH:
  → Route to PH (consolidation model)
ELSE:
  → Flag for manual review (out of stock everywhere)
```

### Layer 3: Manual Overrides (OPERATIONAL — staff-triggered)

| Override | Trigger | Action |
|----------|---------|--------|
| Printer downtime | FL or UK printer offline | Reroute to PH |
| Holidays | UK/US holiday approaching | PH pre-prints, freight ships |
| Peak season (Dec) | Volume spike | PH takes overflow |
| Saturday | Weekend cutoff | Specific PO wave rules |
| Carrier outage | USPS/RM disruption | Switch to backup carrier |

---

## Veeqo Configuration Plan

### Shipping Rules to Create

| Rule # | Condition | Carrier Assignment | Priority |
|--------|-----------|-------------------|----------|
| V-001 | Channel = Amazon US | Amazon Buy Shipping | **HIGHEST** |
| V-002 | Channel = Amazon UK | Amazon Buy Shipping UK | **HIGHEST** |
| V-003 | Channel = Amazon US + Buy Shipping unavailable | USPS Buy Shipping | HIGH |
| V-004 | Destination = US + Channel ≠ Amazon | Stamps.com or Veeqo USPS | MEDIUM |
| V-005 | Destination = UK domestic + Channel ≠ Amazon | Royal Mail RM24 Tracked | MEDIUM |
| V-006 | Destination = DE/FR/IT/EU | Royal Mail International | MEDIUM |
| V-007 | Destination = DE + weight/cost threshold | Deutsche Post (if cheaper) | MEDIUM |
| V-008 | Destination = JP | PH small sticker labels | LOW |
| V-009 | Destination = Rest of World | Royal Mail International | LOW |
| V-010 | Product = Skins/Stickers + Site = PH | **BLOCK** — reroute to UK/FL | **OVERRIDE** |

### Filtered Tabs for Operators

| Tab Name | Filter | Operator |
|----------|--------|----------|
| FL Premium (Amazon) | Site=FL + Channel=Amazon + Prime | FL operator |
| FL Non-Premium | Site=FL + Channel≠Amazon OR non-Prime | FL operator |
| UK All | Site=UK | UK operator |
| PH Consolidation | Site=PH | PH operator |
| PH → UK Freight | Site=PH + Destination=UK/EU | PH operator |
| PH → US Freight | Site=PH + Destination=US | PH operator |

### GDrive Label Distribution

| Folder | Who Pulls | Contents |
|--------|-----------|----------|
| 📁 UK Labels/ | UK operator | RM + Amazon UK labels |
| 📁 FL Labels/ | FL operator | USPS + Amazon US labels |
| 📁 PH Labels/ | PH operator | All PH production labels |
| 📁 PH→UK Freight/ | PH operator | Consolidation box labels |
| 📁 PH→US Freight/ | PH operator | Consolidation box labels |

---

## What We STILL Need (from PHP codebase)

| Unknown | Source | Impact |
|---------|--------|--------|
| Full list of product type codes and routing | `zero_POFiltering.php` lines 1-500 | Equipment capability rules |
| All country groupings (what counts as "UK countries", "US countries") | `zero_POFiltering.php` $us_countries, $uk_countries arrays | Routing accuracy |
| Complete weekend/holiday hold logic | `zero_POFiltering.php` lines 800-1300 | PO wave timing |
| Weight/dimension thresholds for carrier selection | Possibly in picking list PHP | Letter vs parcel classification |
| Stock check integration | Zero DB queries | Veeqo inventory sync |
| FBA-specific rules | Separate FBA process (Drew's email) | FBA stays on Amazon, but routing differs |
| B6/B7/A9/DM product definitions | PHP variable definitions | Routing exceptions |

---

## Validation Plan (Before Killing Lane 1)

1. **Side-by-side test:** Same 100 orders through both lanes
2. **Compare outputs:** Label carrier match rate must be >98%
3. **Edge case test:** Weekend orders, skin products, German addresses, PH overflow
4. **Amazon Buy Shipping verification:** Confirm late delivery protection is active
5. **Run parallel for 2 weeks minimum** before cutover
6. **Patrick signs off** — he's the operator who'll catch mismatches

---

## Related
- [[wiki/23-drew-handover/DUAL_LANE_PROCESS_FLOW|Dual Lane Process Flow]] — Full pipeline visualization
- [[wiki/23-drew-handover/PATRICK_WORKFLOW_PICKLIST_TO_IMAGE|Patrick's Workflow]] — Current manual process
- [[wiki/23-drew-handover/ZERO_INFRASTRUCTURE|Zero Infrastructure]] — PHP codebase location
- [[wiki/04-shipping/SHIPPING_CARRIER_RULES|Shipping Carrier Rules]] — Three-layer routing logic
- [[wiki/23-drew-handover/VEEQO_REPLACEMENT_ANALYSIS|Veeqo Replacement Analysis]] — Platform selection rationale
- [[wiki/23-drew-handover/PATRICK_IT_TEAM_PROFILE|Patrick IT Team]] — Who validates the migration
- [[wiki/12-org/PH_STAFF_ROSTER|PH Staff Roster]] — Staff impact
