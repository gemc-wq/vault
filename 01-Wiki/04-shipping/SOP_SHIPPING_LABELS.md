# SOP: Shipping Label Process & Carrier Selection
*Version: DRAFT 0.1 | Created: 2026-02-11 | Status: IN DEVELOPMENT*

---

## Purpose
Standard operating procedure for shipping label generation, carrier selection, and fulfillment handoff.

---

## Carrier Selection Rules

### Decision Flow
```
Order arrives
  → Determine destination country
    → Determine service level (standard / express / prime)
      → Check if Amazon order (carrier override?)
        → Select carrier
          → Generate label
```

### UK Orders
| Condition | Carrier |
|-----------|---------|
| Standard | Royal Mail First Class |

### European Orders (from UK)
| Condition | Carrier |
|-----------|---------|
| Cost comparison | Royal Mail OR Deutsche Post (choose cheapest) |

*Pricing matrix maintained for cost comparison — TBD where this lives.*

### US Orders
| Condition | Carrier |
|-----------|---------|
| Standard | USPS |
| Premium 2-day | FedEx (negotiated flat rate) |
| Amazon order | **Check Amazon shipping requirement** |

### Amazon Shipping Override (US)
- Amazon dictates carrier based on zip code and delivery promise
- Override is mandatory — ignoring it damages seller metrics
- Sometimes forces next-day ($~30) vs standard ($5-6)
- **Policy:** Accept 5% non-compliance to avoid excessive shipping costs
- Monitor: seller metrics must stay near 100%

### International / Rest of World
- Handled from UK site
- Carriers: *TBD — not yet configured in Veco*
- Currently manual process

---

## Philippines Consolidation Shipping

### When Philippines Fulfills for UK/US:
1. Print individual consumer shipping labels (final-mile labels)
2. Pack items individually, ready for end customer
3. Consolidate 100-200 items into one large carton
4. Ship carton via freight (UPS / international freight)
5. UK/US receives carton → opens → merges with local items → hands to courier

---

## Veco Integration

### Current Status
| Market | Veco Status | Manual? |
|--------|-------------|---------|
| US | ✅ Ready | Automated |
| UK (domestic) | 🟡 Nearly ready | Semi-automated |
| Europe | ❌ Not configured | Manual (Excel) |
| International | ❌ Not configured | Manual (Excel) |

### Manual Process (Being Replaced by Veco)
1. Download order data from platforms
2. Filter in Excel by destination/carrier rules
3. Upload to carrier system (Royal Mail portal, etc.)
4. Print labels (PDF)
5. Sort labels by SKU (custom field)
6. Trigger shipment

**Staff:** 2 full-time in Philippines on this process

### Veco Process (Target)
1. Orders auto-imported into Veco
2. Carrier rules applied automatically
3. Labels generated and printed
4. Export shipped list for print file generation
5. Tracking pushed back to platforms

---

## Label-to-Print-File Reconciliation

**CRITICAL RULE:** Every shipping label must have a matching print file. Every print file must have a matching label.

### Reconciliation Check
- After labels exported from Veco (Excel)
- Before print files sent to printer
- Compare: label SKU list vs print file list
- Flag any mismatches for resolution
- **No orphans allowed on either side**

---

*Next steps: Complete Veco configuration for Europe/International. Document pricing matrix for European carriers. Automate reconciliation check.*
