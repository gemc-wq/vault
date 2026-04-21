#!/usr/bin/env python3
"""Generate Shopify-ready Walmart listing CSVs from target, EAN, and BC data."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, parse, request
import os


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
CACHE_DIR = OUTPUT_DIR / "bc_cache"
RATE_LIMIT_SECONDS = 0.25
BC_BASE_URL = "https://api.bigcommerce.com/stores/otle45p56l/v3/catalog/products"
BC_AUTH_TOKEN = os.getenv("BIGCOMMERCE_ACCESS_TOKEN", "")
VENDOR = "Head Case Designs"
GOOGLE_CONDITION = "New"
DEFAULT_WEIGHT_GRAMS = 85
PRODUCT_CATEGORY_PHONE_CASE = (
    "Electronics > Communications > Telephony > Mobile Phone Cases"
)
PRODUCT_CATEGORY_GAMING_SKIN = (
    "Electronics > Video Game Consoles & Accessories > Video Game Console Accessories"
)
PRODUCT_CATEGORY_DESK_MAT = "Office Supplies > Desk Pads & Blotters"


LICENSE_MAP = {
    "NARU": "Naruto Shippuden",
    "PNUT": "Peanuts",
    "HPOT": "Harry Potter",
    "DRGB": "Dragon Ball",
    "AFC": "Arsenal FC",
    "FCB": "FC Barcelona",
    "LFC": "Liverpool FC",
    "RMCF": "Real Madrid CF",
    "RMOR": "Rick and Morty",
    "THFC": "Tottenham Hotspur",
    "CFC": "Chelsea FC",
    "MCB": "Manchester City",
    "MCF": "Manchester City",
    "BVR": "Bayer Leverkusen",
    "BV": "Bayer Leverkusen",
    "IMGC": "IMG College",
    "WWE2": "WWE",
    "WWE": "WWE",
    "NFL": "NFL",
    "NBA2": "NBA",
    "NBA": "NBA",
    "NHL": "NHL",
    "PPUF": "Powerpuff Girls",
    "BTMC": "Batman Classic",
    "ADVE": "Adventure Time",
    "OHIO": "Ohio State",
    "GMOR": "Gaming",
    "SPRC": "Snoopy Racing",
    "SCDO": "Scooby-Doo",
    "HATS": "Hats Collection",
    "SUPN": "Supernatural",
    "IRON": "Iron Maiden",
    "WMG": "Warner Music",
    "LTOO": "Looney Tunes",
    "TDKR": "The Dark Knight Rises",
    "ACM": "AC Milan",
    "ROMA": "AS Roma",
    "UFC": "UFC",
    "FLAG": "Flags",
    "F1309": "Formula 1",
    "FRND": "Friends",
    "FKFLOR": "FK Floral",
}

CASE_TYPE_MAP = {
    "HTPCR": "Hybrid MagSafe Case",
    "HB401": "Hybrid Hard MagSafe Case",
    "HLBWH": "Leather Wallet Case",
    "HB6CR": "Clear MagSafe Case",
    "HB7BK": "Black MagSafe Case",
    "HC": "Hard Case",
    "H8939": "Vinyl Gaming Skin",
    "HDMWH": "Desk Mat",
}

SHORT_CASE_TYPE_MAP = {
    "HTPCR": "MagSafe Case",
    "HB401": "Hard MagSafe Case",
    "HLBWH": "Wallet Case",
    "HB6CR": "Clear MagSafe Case",
    "HB7BK": "Black MagSafe Case",
    "HC": "Hard Case",
    "H8939": "Gaming Skin",
    "HDMWH": "Desk Mat",
}

FEATURE_MAP = {
    "HTPCR": [
        "TPU bumper + PC hard back for dual-material protection",
        "Integrated magnetic ring for MagSafe charging and accessories",
        "Military-grade drop protection with shock-absorbing edges",
        "Raised bezels help protect the screen and camera",
        "Slim profile with precise cutouts for buttons and ports",
    ],
    "HB401": [
        "TPU bumper + PC hard back with reinforced impact resistance",
        "Integrated magnetic ring for MagSafe charging and accessories",
        "Reinforced corners for enhanced drop protection",
        "Raised screen lip and camera ring protection",
        "Scratch-resistant UV-printed graphics with a lightweight feel",
    ],
    "HLBWH": [
        "Premium faux leather finish with card slots and cash pocket",
        "Magnetic closure keeps your phone secure on the go",
        "Converts into a hands-free viewing stand",
        "Full 360-degree protection when closed",
        "Precise cutouts preserve access to ports and buttons",
    ],
    "HB6CR": [
        "Crystal-clear shell with built-in MagSafe compatibility",
        "Military-grade drop protection for daily use",
        "Anti-yellowing material helps preserve clarity",
        "Raised edges help protect the screen and camera",
        "Slim fit with precise cutouts and responsive button covers",
    ],
    "HB7BK": [
        "Sleek black finish with embedded MagSafe magnets",
        "Strong magnetic alignment for chargers and accessories",
        "Impact-resistant bumper edges help absorb drops",
        "Enhanced grip texture for confident handling",
        "Raised screen and camera protection with precise cutouts",
    ],
    "HC": [
        "Durable hard-shell construction for everyday protection",
        "Slim snap-on profile with precise cutouts",
        "Scratch-resistant high-resolution printed graphics",
        "Raised edges help guard the screen and camera",
        "Designed for a secure, model-specific fit",
    ],
    "H8939": [
        "Precision-cut vinyl skin for a clean, tailored fit",
        "Bubble-free application with easy repositioning",
        "Scratch-resistant printed finish",
        "Thin profile adds style without bulk",
        "Removes cleanly when it is time for a refresh",
    ],
    "HDMWH": [
        "Smooth fabric surface for precise mouse tracking",
        "Premium print with vivid, long-lasting color",
        "Non-slip rubber base keeps the mat in place",
        "Comfortable desk coverage for work or gaming",
        "Durable stitched-style finish for everyday use",
    ],
}

WEIGHT_MAP = {
    "HTPCR": 85,
    "HB401": 90,
    "HLBWH": 120,
    "HB6CR": 90,
    "HB7BK": 95,
    "HC": 80,
    "H8939": 20,
    "HDMWH": 500,
}


@dataclass
class VariantCandidate:
    sku: str
    canonical_type: str
    original_type: str
    device_code: str
    design_code: str
    variant_code: str
    barcode: str


@dataclass
class ProductRowContext:
    handle: str
    title: str
    seo_title: str
    seo_description: str
    description_html: str
    product_category: str
    product_type_label: str
    design_code: str
    brand_code: str
    image_url: str
    image_alt: str
    device_code: str = ""
    full_device_name: str = ""
    variant_group_id: str = ""


@dataclass
class BuildStats:
    products_generated: int = 0
    variants_generated: int = 0
    total_rows: int = 0
    designs_skipped_no_bc: list[str] = field(default_factory=list)
    missing_eans: list[str] = field(default_factory=list)
    sample_titles: list[str] = field(default_factory=list)
    inferred_devices: bool = False
    ean_variants: int = 0


def canonical_product_type(product_type: str) -> str:
    if product_type.startswith("F") and product_type not in {"FLAG", "F1309"}:
        return product_type[1:]
    return product_type


def parse_sku(sku: str) -> tuple[str, str, str, str]:
    parts = sku.split("-", 3)
    if len(parts) == 3:
        return parts[0], parts[1], parts[2], ""
    if len(parts) == 4:
        return parts[0], parts[1], parts[2], parts[3]
    raise ValueError(f"Unexpected SKU format: {sku}")


def load_json(path: Path) -> Any:
    with path.open() as handle:
        return json.load(handle)


def slugify(value: str) -> str:
    lowered = value.lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    return lowered.strip("-")


def infer_license(design_code: str, bc_brand_code: str | None = None) -> str:
    if bc_brand_code:
        return LICENSE_MAP.get(bc_brand_code.upper(), bc_brand_code)
    for prefix in sorted(LICENSE_MAP, key=len, reverse=True):
        if design_code.startswith(prefix):
            return LICENSE_MAP[prefix]
    return "Head Case Designs"


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def clean_description_html(value: str | None) -> str:
    text = value or ""
    text = re.sub(r"(?is)<h[1-6][^>]*>\s*(english|deutsch|fran[cç]ais|italiano)\s*</h[1-6]>", "", text)
    text = re.sub(r"(?is)<strong>\s*(english|deutsch|fran[cç]ais|italiano)\s*</strong>", "", text)
    text = re.sub(r"\n{2,}", "\n", text).strip()
    return text


def title_case_device(value: str) -> str:
    if not value:
        return value
    value = value.replace(" 5g", " 5G").replace(" 4g", " 4G")
    return value


def normalize_device_name(value: str) -> str:
    value = clean_text(value)
    value = re.sub(r"^Apple\s+", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^Samsung\s+Samsung\s+", "Samsung ", value, flags=re.IGNORECASE)
    value = re.sub(r"^OnePlus\s+OnePlus\s+", "OnePlus ", value, flags=re.IGNORECASE)
    return title_case_device(value)


def prettify_device_code(device_code: str) -> str:
    if re.fullmatch(r"\d+X\d+X\d+", device_code):
        parts = device_code.split("X")
        return f"{parts[0]} x {parts[1]} x {parts[2]} mm"
    fallback = device_code.replace("_", " ").replace("-", " ")
    fallback = re.sub(r"(?<=[A-Za-z])(?=\d)", " ", fallback)
    fallback = re.sub(r"(?<=\d)(?=[A-Za-z])", " ", fallback)
    return fallback


def build_device_name(
    device_code: str,
    device_map: dict[str, str],
    bc_device_model: str | None,
) -> str:
    mapped = device_map.get(device_code)
    if mapped:
        return normalize_device_name(mapped)
    if bc_device_model:
        return normalize_device_name(bc_device_model)
    return normalize_device_name(prettify_device_code(device_code))


def product_category_for(canonical_type: str) -> str:
    if canonical_type == "HDMWH":
        return PRODUCT_CATEGORY_DESK_MAT
    if canonical_type == "H8939":
        return PRODUCT_CATEGORY_GAMING_SKIN
    return PRODUCT_CATEGORY_PHONE_CASE


def google_product_type_label(canonical_type: str) -> str:
    return CASE_TYPE_MAP.get(canonical_type, canonical_type)


def select_image_url(images: list[dict[str, Any]]) -> str:
    for key in ("url_standard", "url_zoom", "url_thumbnail"):
        for image in images:
            value = image.get(key)
            if value:
                return value
    return ""


class BigCommerceClient:
    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.last_call_at = 0.0

    def fetch_design(self, design_code: str) -> dict[str, Any] | None:
        cache_path = self.cache_dir / f"{design_code}.json"
        if cache_path.exists():
            return load_json(cache_path)

        time_since_last = time.time() - self.last_call_at
        if time_since_last < RATE_LIMIT_SECONDS:
            time.sleep(RATE_LIMIT_SECONDS - time_since_last)

        query = parse.urlencode(
            {
                "sku:like": design_code,
                "include": "custom_fields,images",
                "limit": 1,
            }
        )
        req = request.Request(
            f"{BC_BASE_URL}?{query}",
            headers={
                "Accept": "application/json",
                "X-Auth-Token": BC_AUTH_TOKEN,
            },
        )

        try:
            with request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except error.URLError:
            return None
        finally:
            self.last_call_at = time.time()

        data = payload.get("data") or []
        product = data[0] if data else None
        if product is None:
            return None

        with cache_path.open("w") as handle:
            json.dump(product, handle, indent=2)
        return product


def build_bc_lookup(product: dict[str, Any] | None) -> dict[str, str]:
    if not product:
        return {}
    lookup = {}
    for field_item in product.get("custom_fields", []):
        name = field_item.get("name")
        value = field_item.get("value")
        if name and value:
            lookup[name] = value
    return lookup


def design_story(
    design_code: str,
    design_name: str,
    license_name: str,
    bc_description: str,
) -> str:
    cleaned_bc = re.sub(r"(?is)<[^>]+>", " ", bc_description)
    cleaned_bc = clean_text(cleaned_bc)
    if cleaned_bc:
        return cleaned_bc[:320].rstrip(".") + "."
    return (
        f"{design_name} brings authentic {license_name} artwork to everyday carry. "
        "It is part of the Head Case Designs licensed lineup built for fans who want standout style."
    )


def build_description_html(
    canonical_type: str,
    license_name: str,
    design_name: str,
    full_device_name: str,
    bc_description: str,
) -> str:
    features = FEATURE_MAP.get(canonical_type, FEATURE_MAP["HC"])
    hero = (
        f"Show off {html.escape(design_name)} with this officially licensed "
        f"{html.escape(license_name)} {html.escape(SHORT_CASE_TYPE_MAP.get(canonical_type, 'product'))}. "
        f"It is designed to bring standout artwork and dependable everyday protection to {html.escape(full_device_name)}."
    )
    about = html.escape(
        design_story(
            design_code="",
            design_name=design_name,
            license_name=license_name,
            bc_description=bc_description,
        )
    )
    bullets = "\n".join(f"<li>{html.escape(feature)}</li>" for feature in features[:4])
    bullets += f"\n<li>Compatible with {html.escape(full_device_name)}</li>"
    return (
        '<div class="product-description">\n'
        f'  <p class="hero">{hero}</p>\n'
        "  <h3>Features</h3>\n"
        "  <ul>\n"
        f"{indent_lines(bullets, 4)}\n"
        "  </ul>\n"
        "  <h3>About the Design</h3>\n"
        f"  <p>{about}</p>\n"
        "</div>"
    )


def build_grouped_description_html(
    license_name: str,
    design_name: str,
    bc_description: str,
) -> str:
    hero = (
        f"Show off {html.escape(design_name)} with this officially licensed "
        f"{html.escape(license_name)} phone case collection from Head Case Designs. "
        "Choose your compatible model and preferred case style from the available variants."
    )
    about = html.escape(
        design_story(
            design_code="",
            design_name=design_name,
            license_name=license_name,
            bc_description=bc_description,
        )
    )
    bullets = [
        "Officially licensed artwork printed with vivid, lasting color",
        "Multiple compatible phone models available as variants",
        "Choose from premium case styles including MagSafe and wallet options",
        "Model-specific fit and cutouts on every variant",
    ]
    bullet_html = "\n".join(f"<li>{html.escape(feature)}</li>" for feature in bullets)
    return (
        '<div class="product-description">\n'
        f'  <p class="hero">{hero}</p>\n'
        "  <h3>Features</h3>\n"
        "  <ul>\n"
        f"{indent_lines(bullet_html, 4)}\n"
        "  </ul>\n"
        "  <h3>About the Design</h3>\n"
        f"  <p>{about}</p>\n"
        "</div>"
    )


def indent_lines(value: str, spaces: int) -> str:
    prefix = " " * spaces
    return "\n".join(f"{prefix}{line}" if line else line for line in value.splitlines())


def build_meta_description(
    license_name: str,
    design_name: str,
    case_type: str,
    full_device_name: str,
    canonical_type: str,
) -> str:
    key_feature = {
        "HTPCR": "Military-grade MagSafe protection",
        "HB401": "dual-material MagSafe protection",
        "HLBWH": "wallet storage and full-cover protection",
        "HB6CR": "clear MagSafe protection",
        "HB7BK": "black MagSafe protection",
        "HC": "hard-shell everyday protection",
        "H8939": "precision-cut scratch protection",
        "HDMWH": "premium non-slip desk comfort",
    }.get(canonical_type, "premium everyday protection")
    meta = (
        f"Official {license_name} {design_name} {case_type} for {full_device_name}. "
        f"{key_feature}. Shop Head Case Designs - 8M+ cases sold worldwide."
    )
    return meta[:320]


def build_title(
    license_name: str,
    design_name: str,
    case_type: str,
    full_device_name: str,
) -> str:
    title = (
        f"{license_name} {design_name} Official {case_type} for {full_device_name} | "
        "Military Grade MagSafe Protection"
    )
    return title[:200]


def build_grouped_title(
    license_name: str,
    design_name: str,
) -> str:
    title = f"{license_name} {design_name} Official Phone Case Collection"
    return title[:200]


def build_grouped_meta_description(
    license_name: str,
    design_name: str,
) -> str:
    meta = (
        f"Official {license_name} {design_name} phone case collection from Head Case Designs. "
        "Choose your compatible model and preferred case type."
    )
    return meta[:320]


def build_tags(design_code: str, brand_code: str, device_code: str, product_type: str) -> str:
    return (
        f"lineup:{design_code}, brand:{brand_code or 'unknown'}, "
        f"device:{device_code}, type:{product_type}, pulse-champion"
    )


def stable_price(row_group: list[dict[str, Any]], bc_lookup: dict[str, str], canonical_type: str) -> str:
    bc_price = clean_text(bc_lookup.get("Price_US"))
    if bc_price:
        return bc_price
    fallback_prices = {
        "HTPCR": "17.95",
        "HB401": "19.95",
        "HLBWH": "24.95",
        "HB6CR": "24.95",
        "HB7BK": "24.95",
        "HC": "19.95",
        "H8939": "12.95",
        "HDMWH": "29.95",
    }
    return fallback_prices.get(canonical_type, "19.95")


def map_design_candidates(
    ean_lookup: dict[str, str],
) -> tuple[dict[str, list[VariantCandidate]], dict[tuple[str, str], list[VariantCandidate]]]:
    by_design: dict[str, list[VariantCandidate]] = defaultdict(list)
    by_design_type: dict[tuple[str, str], list[VariantCandidate]] = defaultdict(list)
    for sku, barcode in ean_lookup.items():
        try:
            product_type, device_code, design_code, variant_code = parse_sku(sku)
        except ValueError:
            continue
        candidate = VariantCandidate(
            sku=sku,
            canonical_type=canonical_product_type(product_type),
            original_type=product_type,
            device_code=device_code,
            design_code=design_code,
            variant_code=variant_code,
            barcode=barcode,
        )
        by_design[design_code].append(candidate)
        by_design_type[(design_code, candidate.canonical_type)].append(candidate)
    return by_design, by_design_type


def aggregate_designs(
    targets: list[dict[str, Any]],
    ean_only: bool,
    product_type_filter: str | None,
    by_design: dict[str, list[VariantCandidate]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in targets:
        canonical_type = canonical_product_type(row["product_type"])
        if product_type_filter and canonical_type != product_type_filter:
            continue
        grouped[row["design_code"]].append(row)

    designs = []
    for design_code, rows in grouped.items():
        if ean_only and not by_design.get(design_code):
            continue
        revenue = sum(float(row.get("revenue_90d", 0) or 0) for row in rows)
        designs.append(
            {
                "design_code": design_code,
                "rows": rows,
                "revenue_90d": revenue,
                "product_types": sorted({canonical_product_type(row["product_type"]) for row in rows}),
            }
        )
    designs.sort(key=lambda item: (-item["revenue_90d"], item["design_code"]))
    return designs


def infer_global_device_ranking(
    targets: list[dict[str, Any]],
    by_design_type: dict[tuple[str, str], list[VariantCandidate]],
) -> list[str]:
    scores: Counter[str] = Counter()
    for row in targets:
        canonical_type = canonical_product_type(row["product_type"])
        key = (row["design_code"], canonical_type)
        candidates = by_design_type.get(key, [])
        device_codes = {candidate.device_code for candidate in candidates}
        if not device_codes:
            continue
        share = float(row.get("revenue_90d", 0) or 0) / len(device_codes)
        for device_code in device_codes:
            scores[device_code] += share
    return [device_code for device_code, _ in scores.most_common()]


def choose_top_devices_for_design(
    design_code: str,
    product_types: list[str],
    by_design_type: dict[tuple[str, str], list[VariantCandidate]],
    global_device_rank: list[str],
    limit: int = 15,
) -> list[str]:
    available_by_type = []
    for canonical_type in product_types:
        candidates = by_design_type.get((design_code, canonical_type), [])
        device_codes = {candidate.device_code for candidate in candidates}
        if device_codes:
            available_by_type.append(device_codes)

    if not available_by_type:
        return []

    shared_devices = set.intersection(*available_by_type) if len(available_by_type) > 1 else set(available_by_type[0])
    pool = shared_devices or set.union(*available_by_type)
    chosen = [device_code for device_code in global_device_rank if device_code in pool][:limit]
    if len(chosen) < limit:
        remaining = sorted(pool - set(chosen))
        chosen.extend(remaining[: max(0, limit - len(chosen))])
    return chosen


def choose_variant_for_type(
    candidates: list[VariantCandidate],
    device_code: str,
) -> VariantCandidate | None:
    matches = [candidate for candidate in candidates if candidate.device_code == device_code]
    if not matches:
        return None
    matches.sort(
        key=lambda candidate: (
            candidate.original_type.startswith("F"),
            candidate.variant_code,
            candidate.sku,
        )
    )
    return matches[0]


def primary_product_type(rows: list[dict[str, Any]]) -> str:
    ranked = sorted(
        rows,
        key=lambda row: (
            -float(row.get("revenue_90d", 0) or 0),
            canonical_product_type(row["product_type"]),
        ),
    )
    return canonical_product_type(ranked[0]["product_type"])


def build_row(
    headers: list[str],
    context: ProductRowContext,
    variant: VariantCandidate,
    position: int,
    price: str,
) -> dict[str, str]:
    row = {header: "" for header in headers}
    row["Title"] = context.title
    row["URL handle"] = context.handle
    row["Description"] = context.description_html
    row["Vendor"] = VENDOR
    row["Product category"] = context.product_category
    row["Type"] = context.product_type_label
    row["Tags"] = build_tags(context.design_code, context.brand_code, context.device_code, variant.canonical_type)
    row["Published on online store"] = "FALSE"
    row["Status"] = "draft"
    row["SKU"] = variant.sku
    row["Barcode"] = variant.barcode
    row["Option1 name"] = "Case Type"
    row["Option1 value"] = CASE_TYPE_MAP.get(variant.canonical_type, variant.canonical_type)
    row["Price"] = price
    row["Charge tax"] = "TRUE"
    row["Continue selling when out of stock"] = "TRUE"
    row["Weight value (grams)"] = str(WEIGHT_MAP.get(variant.canonical_type, DEFAULT_WEIGHT_GRAMS))
    row["Weight unit for display"] = "g"
    row["Requires shipping"] = "TRUE"
    row["Fulfillment service"] = "manual"
    row["Product image URL"] = context.image_url
    row["Image position"] = str(position)
    row["Image alt text"] = context.image_alt
    row["Variant image URL"] = context.image_url
    row["Gift card"] = "FALSE"
    row["SEO title"] = context.seo_title
    row["SEO description"] = context.seo_description
    row["Google Shopping / Google product category"] = context.product_category
    row["Google Shopping / Manufacturer part number (MPN)"] = variant.sku
    row["Google Shopping / Ad group name"] = variant.design_code
    row["Google Shopping / Ads labels"] = f"pulse-champion,{variant.canonical_type}"
    row["Google Shopping / Condition"] = GOOGLE_CONDITION
    row["Google Shopping / Custom product"] = "FALSE"
    row["Google Shopping / Custom label 0"] = variant.design_code
    row["Google Shopping / Custom label 1"] = variant.device_code
    row["Google Shopping / Custom label 2"] = variant.canonical_type
    row["Google Shopping / Custom label 3"] = "walmart"
    row["Google Shopping / Custom label 4"] = "draft"
    return row


def build_walmart_row(
    headers: list[str],
    context: ProductRowContext,
    variant: VariantCandidate,
    full_device_name: str,
    position: int,
    price: str,
    is_first_variant: bool,
) -> dict[str, str]:
    row = {header: "" for header in headers}
    row["Title"] = context.title if is_first_variant else ""
    row["URL handle"] = context.handle
    row["Description"] = context.description_html if is_first_variant else ""
    row["Vendor"] = VENDOR if is_first_variant else ""
    row["Product category"] = context.product_category if is_first_variant else ""
    row["Type"] = context.product_type_label if is_first_variant else ""
    row["Tags"] = (
        build_tags(context.design_code, context.brand_code, variant.device_code, variant.canonical_type)
        if is_first_variant
        else ""
    )
    row["Published on online store"] = "FALSE" if is_first_variant else ""
    row["Status"] = "draft" if is_first_variant else ""
    row["SKU"] = variant.sku
    row["Barcode"] = variant.barcode
    row["Option1 name"] = "Compatible Model"
    row["Option1 value"] = full_device_name
    row["Option2 name"] = "Case Type"
    row["Option2 value"] = CASE_TYPE_MAP.get(variant.canonical_type, variant.canonical_type)
    row["Price"] = price
    row["Charge tax"] = "TRUE"
    row["Continue selling when out of stock"] = "TRUE"
    row["Weight value (grams)"] = str(WEIGHT_MAP.get(variant.canonical_type, DEFAULT_WEIGHT_GRAMS))
    row["Weight unit for display"] = "g"
    row["Requires shipping"] = "TRUE"
    row["Fulfillment service"] = "manual"
    row["Product image URL"] = context.image_url if is_first_variant else ""
    row["Image position"] = str(position) if is_first_variant else ""
    row["Image alt text"] = context.image_alt if is_first_variant else ""
    row["Variant image URL"] = context.image_url
    row["Gift card"] = "FALSE"
    row["SEO title"] = context.seo_title if is_first_variant else ""
    row["SEO description"] = context.seo_description if is_first_variant else ""
    row["Google Shopping / Google product category"] = context.product_category
    row["Google Shopping / Manufacturer part number (MPN)"] = variant.sku
    row["Google Shopping / Ad group name"] = variant.design_code
    row["Google Shopping / Ads labels"] = f"pulse-champion,{variant.canonical_type}"
    row["Google Shopping / Condition"] = GOOGLE_CONDITION
    row["Google Shopping / Custom product"] = "FALSE"
    row["Google Shopping / Custom label 0"] = variant.design_code
    row["Google Shopping / Custom label 1"] = variant.device_code
    row["Google Shopping / Custom label 2"] = variant.canonical_type
    row["Google Shopping / Custom label 3"] = "walmart"
    row["Google Shopping / Custom label 4"] = context.variant_group_id
    if "Variant Group ID" in row:
        row["Variant Group ID"] = context.variant_group_id
    return row


def walmart_headers(base_headers: list[str]) -> list[str]:
    headers = list(base_headers)
    if "Variant Group ID" not in headers:
        insert_at = headers.index("Gift card") if "Gift card" in headers else len(headers)
        headers.insert(insert_at, "Variant Group ID")
    return headers


def grouped_product_type_label(product_types: list[str]) -> str:
    categories = {product_category_for(product_type) for product_type in product_types}
    if len(product_types) == 1:
        return google_product_type_label(product_types[0])
    if categories == {PRODUCT_CATEGORY_PHONE_CASE}:
        return "Phone Case"
    return "Accessory"


def resolve_design_name(product: dict[str, Any] | None, bc_lookup: dict[str, str], design_code: str) -> str:
    for key in ("DesignName",):
        value = clean_text(bc_lookup.get(key))
        if value:
            return value
    name = clean_text((product or {}).get("name"))
    if name:
        return name
    return design_code


def resolve_brand_code(bc_lookup: dict[str, str], design_code: str) -> str:
    brand_code = clean_text(bc_lookup.get("BrandCode"))
    if brand_code:
        return brand_code
    for prefix in sorted(LICENSE_MAP, key=len, reverse=True):
        if design_code.startswith(prefix):
            return prefix
    return "HCD"


def report_markdown(
    report_path: Path,
    stats: BuildStats,
    output_csv: Path,
    selected_design_count: int,
) -> None:
    coverage = 0.0
    if stats.variants_generated:
        coverage = (stats.ean_variants / stats.variants_generated) * 100

    lines = [
        "# Walmart Shopify Generation Report",
        "",
        f"- Generated at: {datetime.now().isoformat(timespec='seconds')}",
        f"- CSV output: `{output_csv}`",
        f"- Designs processed: {selected_design_count}",
        f"- Products generated: {stats.products_generated}",
        f"- Variants generated: {stats.variants_generated}",
        f"- Total CSV rows: {stats.total_rows}",
        f"- EAN coverage: {stats.ean_variants}/{stats.variants_generated} ({coverage:.1f}%)",
        "",
        "## Notes",
        "",
        (
            "- Device ranking was inferred by apportioning target revenue across "
            "EAN-backed device availability because `walmart_targets.json` does not contain per-device revenue."
            if stats.inferred_devices
            else "- Device ranking came directly from the available data."
        ),
        "",
        "## Designs Skipped (No BigCommerce Data)",
        "",
    ]

    if stats.designs_skipped_no_bc:
        lines.extend(f"- {code}" for code in stats.designs_skipped_no_bc)
    else:
        lines.append("- None")

    lines.extend(["", "## Sample Titles", ""])
    if stats.sample_titles:
        lines.extend(f"- {title}" for title in stats.sample_titles[:5])
    else:
        lines.append("- None generated")

    lines.extend(["", "## Missing EANs", ""])
    if stats.missing_eans:
        for entry in sorted(set(stats.missing_eans))[:200]:
            lines.append(f"- `{entry}`")
    else:
        lines.append("- None")

    report_path.write_text("\n".join(lines) + "\n")


def generate_rows(args: argparse.Namespace) -> tuple[Path, Path, BuildStats]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    base_headers = load_json(ROOT / "shopify_headers.json")
    headers = walmart_headers(base_headers) if args.mode == "walmart" else base_headers
    targets = load_json(ROOT / "walmart_targets.json")
    ean_lookup = load_json(ROOT / "ean_lookup.json")
    device_map = load_json(ROOT / "device_map.json")

    by_design, by_design_type = map_design_candidates(ean_lookup)
    selected_designs = aggregate_designs(
        targets=targets,
        ean_only=args.ean_only,
        product_type_filter=canonical_product_type(args.product_type) if args.product_type else None,
        by_design=by_design,
    )

    if args.design:
        selected_designs = [item for item in selected_designs if item["design_code"] == args.design]
    if args.top:
        selected_designs = selected_designs[: args.top]
    elif not args.all:
        selected_designs = selected_designs[:50]

    global_device_rank = infer_global_device_ranking(targets, by_design_type)
    bc_client = BigCommerceClient(CACHE_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_prefix = "walmart_grouped" if args.mode == "walmart" else "shopify_walmart"
    csv_path = OUTPUT_DIR / f"{output_prefix}_{timestamp}.csv"
    report_path = OUTPUT_DIR / "generation_report.md"
    stats = BuildStats(inferred_devices=True)

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()

        for design_entry in selected_designs:
            design_code = design_entry["design_code"]
            product = bc_client.fetch_design(design_code)
            if not product:
                stats.designs_skipped_no_bc.append(design_code)
                continue

            bc_lookup = build_bc_lookup(product)
            brand_code = resolve_brand_code(bc_lookup, design_code)
            license_name = infer_license(design_code, brand_code)
            design_name = resolve_design_name(product, bc_lookup, design_code)
            bc_description = clean_description_html(product.get("description"))
            image_url = select_image_url(product.get("images", []))
            sample_sku = clean_text(product.get("sku"))
            sample_device_model = clean_text(bc_lookup.get("DeviceModel"))
            if sample_sku and sample_device_model:
                try:
                    _, sample_device_code, _, _ = parse_sku(sample_sku)
                    device_map.setdefault(sample_device_code, sample_device_model)
                except ValueError:
                    pass
            device_codes = choose_top_devices_for_design(
                design_code=design_code,
                product_types=design_entry["product_types"],
                by_design_type=by_design_type,
                global_device_rank=global_device_rank,
            )

            if not device_codes:
                for candidate in by_design.get(design_code, [])[:15]:
                    if candidate.device_code not in device_codes:
                        device_codes.append(candidate.device_code)
            lead_type = primary_product_type(design_entry["rows"])
            price_by_type = {
                canonical_type: stable_price(
                    [row for row in design_entry["rows"] if canonical_product_type(row["product_type"]) == canonical_type],
                    bc_lookup,
                    canonical_type,
                )
                for canonical_type in design_entry["product_types"]
            }

            if args.mode == "walmart":
                grouped_variants: list[tuple[VariantCandidate, str]] = []
                for device_code in device_codes[:15]:
                    full_device_name = build_device_name(
                        device_code=device_code,
                        device_map=device_map,
                        bc_device_model=bc_lookup.get("DeviceModel"),
                    )
                    for canonical_type in sorted(design_entry["product_types"]):
                        candidate = choose_variant_for_type(
                            by_design_type.get((design_code, canonical_type), []),
                            device_code,
                        )
                        if candidate:
                            grouped_variants.append((candidate, full_device_name))
                        else:
                            stats.missing_eans.append(f"{canonical_type}-{device_code}-{design_code}")

                if not grouped_variants:
                    continue

                title = build_grouped_title(
                    license_name=license_name,
                    design_name=design_name,
                )
                product_category = product_category_for(lead_type)
                context = ProductRowContext(
                    handle=slugify(f"{license_name}-{design_name}-phone-case"),
                    title=title,
                    seo_title=title,
                    seo_description=build_grouped_meta_description(
                        license_name=license_name,
                        design_name=design_name,
                    ),
                    description_html=build_grouped_description_html(
                        license_name=license_name,
                        design_name=design_name,
                        bc_description=bc_description,
                    ),
                    product_category=product_category,
                    product_type_label=grouped_product_type_label(design_entry["product_types"]),
                    design_code=design_code,
                    brand_code=brand_code,
                    image_url=image_url,
                    image_alt=title,
                    variant_group_id=f"HCD-{design_code}",
                )
                stats.products_generated += 1
                if len(stats.sample_titles) < 5:
                    stats.sample_titles.append(title)

                for position, (variant, full_device_name) in enumerate(grouped_variants, start=1):
                    row = build_walmart_row(
                        headers=headers,
                        context=context,
                        variant=variant,
                        full_device_name=full_device_name,
                        position=position,
                        price=price_by_type.get(variant.canonical_type, "19.95"),
                        is_first_variant=position == 1,
                    )
                    writer.writerow(row)
                    stats.variants_generated += 1
                    stats.total_rows += 1
                    if variant.barcode:
                        stats.ean_variants += 1
                    else:
                        stats.missing_eans.append(variant.sku)
                continue

            for device_code in device_codes[:15]:
                full_device_name = build_device_name(
                    device_code=device_code,
                    device_map=device_map,
                    bc_device_model=bc_lookup.get("DeviceModel"),
                )
                product_rows: list[VariantCandidate] = []
                for canonical_type in design_entry["product_types"]:
                    candidate = choose_variant_for_type(
                        by_design_type.get((design_code, canonical_type), []),
                        device_code,
                    )
                    if candidate:
                        product_rows.append(candidate)
                    else:
                        stats.missing_eans.append(f"{canonical_type}-{device_code}-{design_code}")
                if not product_rows:
                    continue
                product_rows.sort(key=lambda variant: (variant.canonical_type != lead_type, variant.canonical_type, variant.sku))

                title = build_title(
                    license_name=license_name,
                    design_name=design_name,
                    case_type=CASE_TYPE_MAP.get(lead_type, lead_type),
                    full_device_name=full_device_name,
                )
                seo_description = build_meta_description(
                    license_name=license_name,
                    design_name=design_name,
                    case_type=CASE_TYPE_MAP.get(lead_type, lead_type),
                    full_device_name=full_device_name,
                    canonical_type=lead_type,
                )
                handle_slug = slugify(f"{license_name}-{design_name}-{device_code}")
                product_category = product_category_for(lead_type)
                context = ProductRowContext(
                    handle=handle_slug,
                    title=title,
                    seo_title=title,
                    seo_description=seo_description,
                    description_html=build_description_html(
                        canonical_type=lead_type,
                        license_name=license_name,
                        design_name=design_name,
                        full_device_name=full_device_name,
                        bc_description=bc_description,
                    ),
                    product_category=product_category,
                    product_type_label=google_product_type_label(lead_type),
                    design_code=design_code,
                    brand_code=brand_code,
                    device_code=device_code,
                    full_device_name=full_device_name,
                    image_url=image_url,
                    image_alt=title,
                )
                stats.products_generated += 1
                if len(stats.sample_titles) < 5:
                    stats.sample_titles.append(title)

                for position, variant in enumerate(product_rows, start=1):
                    row = build_row(
                        headers=headers,
                        context=context,
                        variant=variant,
                        position=position,
                        price=price_by_type.get(variant.canonical_type, "19.95"),
                    )
                    writer.writerow(row)
                    stats.variants_generated += 1
                    stats.total_rows += 1
                    if variant.barcode:
                        stats.ean_variants += 1
                    else:
                        stats.missing_eans.append(variant.sku)

    report_markdown(report_path, stats, csv_path, len(selected_designs))
    return csv_path, report_path, stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Shopify-ready CSV listings for Walmart marketplace products."
    )
    parser.add_argument("--mode", choices=("shopify", "walmart"), default="shopify", help="Output structure to generate.")
    parser.add_argument("--top", type=int, help="Generate listings for the top N designs after filtering.")
    parser.add_argument("--design", help="Generate listings for a single design code.")
    parser.add_argument("--all", action="store_true", help="Generate listings for all eligible designs.")
    parser.add_argument("--ean-only", action="store_true", help="Only include designs flagged with EAN coverage.")
    parser.add_argument("--product-type", help="Filter to a canonical product type such as HTPCR or HB401.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        csv_path, report_path, stats = generate_rows(args)
    except KeyboardInterrupt:
        return 130

    print(f"CSV: {csv_path}")
    print(f"Report: {report_path}")
    print(
        f"Products={stats.products_generated} Variants={stats.variants_generated} Rows={stats.total_rows}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
