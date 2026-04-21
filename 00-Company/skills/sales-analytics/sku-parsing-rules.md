# SKU Parsing Rules

> How to decode, group, and analyze Ecell Global SKU strings.

## SKU Format

```
{ProductType}-{DeviceCode}-{DesignCode}-{VariantCode}
```

Example: `HTPCR-IPH17PMAX-NARUICO-CLR`

## FBA Detection

- **F-prefix** on ProductType = FBA variant
- `FHTPCR-IPH17PMAX-NARUICO-CLR` is the FBA twin of `HTPCR-IPH17PMAX-NARUICO-CLR`
- To find FBM/FBA pairs: strip the leading `F` from ProductType, match remaining segments

## Product Types

| Code   | Full Name                  | Tier     | Notes                         |
|--------|----------------------------|----------|-------------------------------|
| HB401  | Hard Back Case (premium)   | Premium  | ~4x CVR vs HTPCR             |
| HTPCR  | Hard Thin Clear Case       | Standard | Highest volume, lowest margin |
| STPCR  | Soft Thin Clear Case       | Standard | TPU material                  |
| STPFL  | Flip Wallet Case           | Premium  | Higher AOV                    |

With F-prefix (FBA variants): `FHB401`, `FHTPCR`, `FSTPCR`, `FSTPFL`

## Device Codes

| Code        | Device                        |
|-------------|-------------------------------|
| IPH17PMAX   | iPhone 17 Pro Max             |
| IPH17PRO    | iPhone 17 Pro                 |
| IPH17       | iPhone 17                     |
| IPH16PMAX   | iPhone 16 Pro Max             |
| IPH16PRO    | iPhone 16 Pro                 |
| SAMGS26U    | Samsung Galaxy S26 Ultra      |
| SAMGS26P    | Samsung Galaxy S26+           |
| SAMGS26     | Samsung Galaxy S26            |
| SAMGS25U    | Samsung Galaxy S25 Ultra      |

Pattern: `{Brand}{Series}{Model}{Variant}`
- IPH = iPhone, SAM = Samsung, PIX = Pixel
- Variant suffixes: PMAX = Pro Max, PRO = Pro, U = Ultra, P = Plus

## Design Codes

- Reference licensed content blocks
- Example: `NARUICO` = Naruto Ichigo crossover design
- Each design code maps to a specific artwork/content block
- Design codes are consistent across product types and devices

## Content Block Model

- **30 content blocks** serve **200K+ parent SKUs**
- Each content block = a license or license crossover with multiple design variants
- Combinatorial explosion: 30 blocks x 4 product types x N devices x variants = massive catalog

## Revenue Concentration

- **590 champion designs** drive **80% of revenue** ($352K of $440K)
- Long tail: remaining ~200K SKUs drive 20%
- Priority: champion designs get FBA migration, ad spend, listing optimization first

## Parsing Logic (Pseudocode)

```
def parse_sku(sku: str) -> dict:
    parts = sku.split("-")
    product_type = parts[0]
    is_fba = product_type.startswith("F")
    base_product_type = product_type[1:] if is_fba else product_type
    return {
        "product_type": product_type,
        "base_product_type": base_product_type,
        "is_fba": is_fba,
        "device_code": parts[1] if len(parts) > 1 else None,
        "design_code": parts[2] if len(parts) > 2 else None,
        "variant_code": parts[3] if len(parts) > 3 else None,
        "base_sku": f"{base_product_type}-{'-'.join(parts[1:])}"
    }
```

## Grouping Rules

| Group By         | Method                                              | Use Case                    |
|------------------|-----------------------------------------------------|-----------------------------|
| FBM/FBA pair     | Match on base_sku (strip F-prefix)                  | Conversion lift analysis    |
| Design family    | Match on design_code across product types + devices | Design performance ranking  |
| Device family    | Match on device_code across product types + designs | Device demand analysis      |
| Product type     | Match on base_product_type                          | Margin/CVR analysis by type |
| Content block    | Map design_code -> content block                    | License-level reporting     |
