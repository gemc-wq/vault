# SKU Parsing — Reference Folder
*Owner: Ava | Created: 2026-04-09 | Source: Cem directives + data analysis*

This folder is the single source of truth for all SKU parsing, brand code mapping, and device code translation across every system — PULSE, Shopify, Walmart, Amazon analytics, BigQuery, Supabase, and any future marketplace.

---

## Files in this folder

| File | Purpose |
|---|---|
| `SKU_PARSING_RULES.md` | Core parsing logic — format, FBA rules, exceptions |
| `SKU_Parsing_by_Brand.txt` | **Source file from Cem** — 861 entries, Brand Name ↔ Code (tab-delimited) |
| `sku_brand_map.json` | Parsed version of the above — 750 unique codes, machine-readable |
| `device_code_map.json` | Device code → full device name (e.g. IPH17PMAX → iPhone 17 Pro Max) |
| `imgc_design_map.json` | IMG College design suffix → university name (IMGCPSU → Penn State, etc.) |

---

## SKU Format

```
{PRODUCT_TYPE}-{DEVICE_CODE}-{DESIGN_CODE}-{VARIANT}
```

**Example:** `HTPCR-IPH17PMAX-NARUICO-AKA`
- Product Type: `HTPCR` = Hybrid MagSafe Case
- Device: `IPH17PMAX` = iPhone 17 Pro Max
- Design: `NARUICO` = Naruto Iconic (brand code prefix: `NARU` = Naruto Shippuden)
- Variant: `AKA` = Akatsuki

---

## Brand Code → Display Name Rules (for product titles)

Use these display names in all consumer-facing titles. Do NOT use the raw internal strings from the brand file.

| Code | Internal Name | Display Name (use this) |
|---|---|---|
| AFC | Arsenal Football Club | Arsenal FC |
| CFC | CHELSEA FOOTBALL CLUB | Chelsea FC |
| LFC | Liverpool Football Club | Liverpool FC |
| AVLA | Aston Villa FC | Aston Villa FC |
| BTMC | Time Warner Batman Core | Batman |
| BVBE | Bravado - BILLIE EILISH | Billie Eilish |
| FCB | FC BARCELONA | FC Barcelona |
| IMGC | IMG College | (use university name from imgc_design_map.json) |
| MC | Manchester City Football Club | Manchester City FC |
| NARU | Naruto Shippuden | Naruto Shippuden |
| NCFC | Newcastle United Football Club | Newcastle United FC |
| NHL | National Hockey League | NHL |
| OHIO | Ohio State University | Ohio State University |
| PNUT | PEANUTS | Peanuts |
| RMCF | Real Madrid CF | Real Madrid CF |
| WWE | World Wrestling Entertainment | WWE |
| DRGBS | Dragon Ball Super | Dragon Ball Super |
| THFC | Tottenham Hotspur F.C. | Tottenham Hotspur |
| WFC | West Ham United Football Club | West Ham United FC |
| BHA | Brighton & Hove Albion F.C | Brighton & Hove Albion FC |
| NBA | National Basketball Association | NBA |
| NFL | National Football League | NFL |
| HPOT | Time Warner HARRY POTTER | Harry Potter |
| RMOR | Rick And Morty | Rick and Morty |
| BVRS | Bravado The Rolling Stones | The Rolling Stones |
| IRON | Iron Maiden | Iron Maiden |
| STREK | Star Trek | Star Trek |

*Add new entries here as new brands are uploaded. Keep this table as the display name standard.*

---

## Product Type → Display Name (for titles)

| Code | Display Name |
|---|---|
| HTPCR / FHTPCR | Hybrid MagSafe Case |
| HB401 / FHB401 | Hybrid Hard MagSafe Case |
| HLBWH | Leather Wallet Case |
| HB6CR | Clear MagSafe Case |
| HB7BK | Black MagSafe Case |
| HDMWH | Desk Mat |
| H8939 | Gaming Skin |

---

## Title Format Standard (Shopify / Walmart)

```
{Brand Display Name} {Design Name} {Product Type Display Name} for {Full Device Name}
```

**Example:**
- ✅ `Arsenal FC Away Hybrid MagSafe Case for iPhone 16 Pro Max`
- ✅ `Naruto Shippuden Akatsuki Hybrid MagSafe Case for iPhone 17 Pro Max`
- ✅ `Penn State University Hybrid MagSafe Case for iPhone 15 Pro`
- ❌ `AFC Away Soft Gel Case for IPH16PMAX` (wrong — uses internal codes)

---

## Key Reference Files (elsewhere)

- Workspace: `data/sku_brand_map.json`, `data/device_code_map.json`
- Wiki: `wiki/SKU_PARSING_RULES.md`
- Vault (this folder): `00-Company/SKU-Parsing/`

---

*Last updated: 2026-04-09 | Next: add display name overrides for all 750 codes*
