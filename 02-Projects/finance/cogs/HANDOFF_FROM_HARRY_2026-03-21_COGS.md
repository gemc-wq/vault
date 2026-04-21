# HANDOFF: Landed Cost / COGS Work
**From:** Harry | **To:** Ava | **Date:** 2026-03-22  
**Status:** Data gathered, files ready — pick up from here

---

## Context
Cem confirmed this workstream belongs to Ava, not Harry.
Harry has done the data gathering and modelling; Ava takes it to completion.

---

## Files ready for you

All in `workspace/outputs/`:
- `ECELL_COGS_FINAL_v2.xlsx` — corrected landed COGS (US + UK tabs)
- `ECELL_Monthly_COGS_Royalty_Calculator.xlsx` — monthly calculator with all 38 active licenses pre-loaded

GDrive copy also at:
`gdrive:Clawdbot Shared Folder/Brain/Projects/Finance/`

---

## What's confirmed

### Freight rates
- **CN→US (FedEx Intl Economy):** 1/3 of CN→UK rate (Cem confirmed)
  - Cases: $0.11/unit | Phone wallets: $0.32/unit | iPad wallets: $1.12/unit
  - Source: FedEx invoice 2-518-41039 (Mar 2026) + FedEx pricing agreement
- **CN→UK (UPS WW Express Saver):** actual Dec 2025 invoice
  - Cases: $0.336/unit | Phone wallets: $0.959/unit | iPad wallets: $3.358/unit

### Blank costs (confirmed by Cem, 2026-03-21)
| Product | Supplier | Cost | Currency |
|---------|---------|------|---------|
| HTPCR | XINTAI | ¥3.50 | RMB |
| HC | XINTAI | ¥3.50 | RMB (same as HTPCR) |
| HB401 | HUAQING | ¥6.50 | RMB |
| HB6CR / HB7BK | TOKO | $1.90 | USD |
| HLBWH phone | JIZHAN | ¥7.00 | RMB |
| HLBWH Kindle | JIZHAN | ¥14.00 | RMB |
| HLBWH iPad | JIZHAN | ¥15.00 | RMB |
| HDMWH 900×400 | TOKO | $1.76 | USD |
| HDMWH 600×300 | TOKO | $0.86 | USD |
| HDMWH 250×300 | ECELLSZ | ¥2.80 | RMB |

### Packaging (confirmed)
- Phone cases: **$0.134/unit** (Baolly, confirmed 2026-03-21)
- iPad wallets: **$0.46/unit** (Baolly, confirmed 2026-03-21)
- Desk mat small: $0.10 | medium: $0.10 | large: $0.12
- Padded envelopes: **£0.08/unit** (~$0.10)

### FX rates used
- ¥7.20 / USD | £1.27 / USD | €1.08 / USD

---

## Outstanding gaps (Ava to complete)

1. ~~Baolly box price~~ — **CONFIRMED**: $0.134 phone, $0.46 iPad (2026-03-21)
2. **Royalty % rates** — Tab 2 of calculator; rates per contract needed from Cem/accountant
3. **HC carton weight** — estimated at 22kg/500 units; confirm with XINTAI or Patrick
4. **PH-specific COGS** — PH fulfils US + UK orders; does PH have different freight rates or packaging costs?
5. **Printing costs** — ink, vinyl, wastage (~30-50%) not yet modelled for printed products

---

## Accounting treatment (confirmed by Cem, 2026-03-21)

**Two COGS definitions — use the right one for the right purpose:**

| Use | Definition | Components |
|-----|-----------|-----------|
| **Xero / accounting journals** | Supplier cost + packaging box | Blank product (XINTAI/TOKO/JIZHAN) + Baolly box |
| **Ava's margin/pricing model** | Full landed cost | Blank + freight + packaging |

Freight (FedEx/UPS invoices) is recorded separately as a logistics expense — not in accounting COGS.

The landed cost model (ECELL_COGS_FINAL_v2.xlsx) is for **Ava's margin analysis and pricing decisions**.
Xero journal entries use **blank cost + packaging only**.

---

## Next steps for Ava
- Get Baolly box price from Cem or email search
- Populate royalty rates in the calculator
- Decide whether to add PH lane as a third COGS column
- Build into finance reporting / Xero journal mapping when Xero write scopes unlock (April 2026)

