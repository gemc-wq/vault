#!/usr/bin/env python3
"""Push Head Case Designs products to Walmart Marketplace via the feed API."""

from __future__ import annotations

import argparse
import base64
import csv
import json
import re
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, parse, request
import os


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
BC_CACHE_DIR = OUTPUT_DIR / "bc_cache"

DEFAULT_CLIENT_ID = os.getenv("WALMART_CLIENT_ID", "")
DEFAULT_CLIENT_SECRET = os.getenv("WALMART_CLIENT_SECRET", "")
DEFAULT_TOKEN_URL = "https://marketplace.walmartapis.com/v3/token"
DEFAULT_FEED_URL = "https://marketplace.walmartapis.com/v3/feeds?feedType=item"
DEFAULT_BRAND = "Head Case Designs"
DEFAULT_PRODUCT_TYPE = "HTPCR"
DEFAULT_PRICE = 19.95
DEFAULT_CURRENCY = "USD"
DEFAULT_LAG_TIME = 900

BC_BASE_URL = "https://api.bigcommerce.com/stores/otle45p56l/v3/catalog/products"
BC_AUTH_TOKEN = os.getenv("BIGCOMMERCE_ACCESS_TOKEN", "")

TOP_DEVICES = [
    "IPH17PMAX",
    "IPH16",
    "IPH17",
    "IPH15",
    "IPH17PRO",
    "IPH14",
    "IPH13",
    "IPH16PMAX",
    "IPHSE4",
    "IPH15PMAX",
    "IPH12",
    "S938U",
    "IPH16PRO",
    "A165G",
    "IPH13PMAX",
    "IPH11",
    "IPH14PMAX",
    "S931X",
    "A152024",
    "S928U",
    "IPH7",
    "IPH16PLUS",
    "IPH14PLUS",
    "IPH15PRO",
    "IPH14PRO",
    "IPH15PLUS",
    "IPH13PRO",
    "IPH12PMAX",
    "S918X",
    "S911X",
]

DEVICE_BRAND_SHORT = {
    "IPH": "IPH",
    "S9": "SAM",
    "S8": "SAM",
    "S7": "SAM",
    "A1": "SAM",
    "A5": "SAM",
}

DEVICE_BRAND_NAME = {
    "IPH": "Apple",
    "S9": "Samsung",
    "S8": "Samsung",
    "S7": "Samsung",
    "A1": "Samsung",
    "A5": "Samsung",
}

CASE_TYPE_NAME = {
    "HTPCR": "Soft Gel Case",
    "HB401": "Hard Back Case",
}

IMAGE_TEMPLATE = {
    "HTPCR": "https://elcellonline.com/atg/{DESIGN}/{VARIANT}/TP-CR-{DEVICE}-1.jpg",
    "HB401": "https://elcellonline.com/atg/{DESIGN}/{VARIANT}/B4-01-{DEVICE}-1.jpg",
}

LICENSE_MAP = {
    "NARU": "Naruto Shippuden",
    "PNUT": "Peanuts",
    "HPOT": "Harry Potter",
    "DRGBS": "Dragon Ball Super",
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

VARIANT_NAME_OVERRIDES = {
    "AKA": "Akatsuki",
    "AND": "Android 17 & 18",
    "AWY": "Away",
    "FRI": "Frieza",
    "GOH": "Gohan",
    "GOK": "Goku",
    "HOM": "Home",
    "THI": "Third",
    "VEG": "Vegeta",
    "XOX": "XOXO",
}


@dataclass
class DesignRecord:
    design: str
    revenue: float
    orders: int
    types: list[str]


@dataclass
class DesignMetadata:
    license_name: str
    design_name: str
    short_description: str
    long_description: str


@dataclass
class CandidateResult:
    sku: str
    device_code: str
    full_device_name: str
    ean: str | None
    image_url: str
    image_exists: bool
    reason: str | None = None


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def strip_html(value: str | None) -> str:
    text = value or ""
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    return clean_text(text)


def title_case_device(value: str) -> str:
    if not value:
        return value
    return value.replace(" 5g", " 5G").replace(" 4g", " 4G")


def normalize_device_name(value: str) -> str:
    value = clean_text(value)
    value = re.sub(r"^Apple\s+", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^Samsung\s+Samsung\s+", "Samsung ", value, flags=re.IGNORECASE)
    return title_case_device(value)


def split_design(design: str) -> tuple[str, str]:
    parts = design.rsplit("-", 1)
    if len(parts) != 2:
        raise ValueError(f"Expected DESIGN-VARIANT format, got {design!r}")
    return parts[0], parts[1]


def parse_sku(sku: str) -> tuple[str, str, str, str]:
    parts = sku.split("-", 3)
    if len(parts) == 3:
        return parts[0], parts[1], parts[2], ""
    if len(parts) == 4:
        return parts[0], parts[1], parts[2], parts[3]
    raise ValueError(f"Unexpected SKU format: {sku}")


def device_brand_short(device_code: str) -> str:
    for prefix, short in DEVICE_BRAND_SHORT.items():
        if device_code.startswith(prefix):
            return short
    return device_code[:3]


def device_brand_name(device_code: str) -> str:
    for prefix, name in DEVICE_BRAND_NAME.items():
        if device_code.startswith(prefix):
            return name
    return ""


def infer_license(base_design: str, brand_code: str | None = None) -> str:
    if brand_code:
        normalized = clean_text(brand_code).upper()
        for prefix in sorted(LICENSE_MAP, key=len, reverse=True):
            if normalized.startswith(prefix):
                return LICENSE_MAP[prefix]
    normalized_design = base_design.upper()
    for prefix in sorted(LICENSE_MAP, key=len, reverse=True):
        if normalized_design.startswith(prefix):
            return LICENSE_MAP[prefix]
    return DEFAULT_BRAND


def prettify_variant_code(variant_code: str) -> str:
    if not variant_code:
        return ""
    normalized = variant_code.upper()
    if normalized in VARIANT_NAME_OVERRIDES:
        return VARIANT_NAME_OVERRIDES[normalized]
    return variant_code.replace("_", " ").title()


def is_usable_design_name(value: str, *, case_type_name: str) -> bool:
    normalized = clean_text(value)
    if not normalized:
        return False
    blocked_fragments = (
        case_type_name.lower(),
        "compatible with",
        " for ",
        "iphone",
        "samsung",
        "htc",
        "pixel",
    )
    lowered = normalized.lower()
    return not any(fragment in lowered for fragment in blocked_fragments)


def extract_design_name_from_title(
    product_name: str,
    license_name: str,
    case_type_name: str,
    full_device_name: str,
) -> str:
    value = clean_text(product_name)
    for prefix in (
        f"{license_name} ",
        f"{DEFAULT_BRAND} ",
        "Officially Licensed ",
    ):
        if value.startswith(prefix):
            value = value[len(prefix):]
    suffixes = [
        f" {case_type_name} Compatible with {full_device_name}",
        f" {case_type_name} for {full_device_name}",
        f" Compatible with {full_device_name}",
        f" for {full_device_name}",
    ]
    for suffix in suffixes:
        if value.endswith(suffix):
            value = value[: -len(suffix)]
    value = clean_text(value)
    if value.startswith(license_name):
        value = clean_text(value[len(license_name) :])
    return value


def build_title(
    license_name: str,
    design_name: str,
    case_type_name: str,
    full_device_name: str,
) -> str:
    title = (
        f"{DEFAULT_BRAND} Officially Licensed {license_name} {design_name} "
        f"{case_type_name} Compatible with {full_device_name}"
    )
    return clean_text(title)[:200]


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def default_paths() -> dict[str, Path]:
    return {
        "champions": ROOT / "combined_backcase_champions.json",
        "champions_alt": Path("/Users/openclaw/.openclaw/workspace/projects/sku-staging/combined_backcase_champions.json"),
        "ean": Path("/Users/openclaw/.openclaw/workspace/data/ean/combined_ean_lookup.json"),
        "device_map": Path("/Users/openclaw/.openclaw/workspace/data/device_code_map.json"),
    }


class BigCommerceClient:
    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, cache_key: str) -> Path:
        safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", cache_key)
        return self.cache_dir / f"{safe}.json"

    def fetch(self, query_sku: str, cache_key: str) -> dict[str, Any] | None:
        cache_path = self._cache_path(cache_key)
        if cache_path.exists():
            return load_json(cache_path)

        params = parse.urlencode(
            {
                "sku:like": query_sku,
                "include": "custom_fields,images",
                "limit": 10,
            }
        )
        req = request.Request(
            f"{BC_BASE_URL}?{params}",
            headers={
                "Accept": "application/json",
                "X-Auth-Token": BC_AUTH_TOKEN,
            },
        )
        try:
            with request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except Exception:
            return None

        products = payload.get("data") or []
        chosen = None
        for product in products:
            sku = clean_text(product.get("sku"))
            if query_sku in sku:
                chosen = product
                break
        if chosen is None and products:
            chosen = products[0]
        if chosen is None:
            return None

        with cache_path.open("w", encoding="utf-8") as handle:
            json.dump(chosen, handle, indent=2)
        return chosen


def build_bc_lookup(product: dict[str, Any] | None) -> dict[str, str]:
    if not product:
        return {}
    lookup: dict[str, str] = {}
    for field in product.get("custom_fields", []):
        name = clean_text(field.get("name"))
        value = clean_text(field.get("value"))
        if name and value:
            lookup[name] = value
    return lookup


def resolve_design_metadata(
    design: str,
    product_type: str,
    bc_client: BigCommerceClient,
    device_map: dict[str, str],
) -> DesignMetadata:
    base_design, variant_code = split_design(design)
    sample_device_code = TOP_DEVICES[0]
    sample_sku = f"{product_type}-{sample_device_code}-{base_design}-{variant_code}"
    product = bc_client.fetch(sample_sku, design) or bc_client.fetch(base_design, base_design)
    lookup = build_bc_lookup(product)
    license_name = infer_license(base_design, lookup.get("BrandCode"))
    sample_device_name = normalize_device_name(device_map.get(sample_device_code, sample_device_code))

    design_name = clean_text(lookup.get("DesignName"))
    if not design_name and product:
        design_name = extract_design_name_from_title(
            product_name=clean_text(product.get("name")),
            license_name=license_name,
            case_type_name=CASE_TYPE_NAME[product_type],
            full_device_name=sample_device_name,
        )
    if not is_usable_design_name(design_name, case_type_name=CASE_TYPE_NAME[product_type]):
        design_name = ""
    if not design_name:
        design_name = prettify_variant_code(variant_code)
    if not design_name:
        design_name = design

    long_description = strip_html((product or {}).get("description"))
    short_description = long_description[:900].rstrip(".")
    if short_description:
        short_description += "."
    else:
        short_description = (
            f"Officially licensed {license_name} {CASE_TYPE_NAME[product_type].lower()} "
            f"from {DEFAULT_BRAND}."
        )

    return DesignMetadata(
        license_name=license_name,
        design_name=design_name,
        short_description=short_description,
        long_description=long_description or short_description,
    )


class WalmartAuth:
    def __init__(self, client_id: str, client_secret: str, token_url: str, lag_time: int = DEFAULT_LAG_TIME) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.lag_time = lag_time
        self._token = ""
        self._expires_at = 0.0

    def bearer_token(self) -> str:
        if self._token and time.time() < self._expires_at:
            return self._token

        credentials = f"{self.client_id}:{self.client_secret}".encode("utf-8")
        basic = base64.b64encode(credentials).decode("ascii")
        body = parse.urlencode({"grant_type": "client_credentials"}).encode("utf-8")
        req = request.Request(
            self.token_url,
            data=body,
            headers={
                "Authorization": f"Basic {basic}",
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        token = clean_text(payload.get("access_token"))
        expires_in = int(payload.get("expires_in") or DEFAULT_LAG_TIME)
        if not token:
            raise RuntimeError(f"Token response did not include access_token: {payload}")
        self._token = token
        self._expires_at = time.time() + max(expires_in - 60, 60)
        return self._token


def read_json_response(resp: Any) -> Any:
    body = resp.read()
    if not body:
        return {}
    return json.loads(body.decode("utf-8"))


def http_json(
    url: str,
    method: str = "GET",
    *,
    headers: dict[str, str] | None = None,
    payload: Any | None = None,
) -> Any:
    data = None
    request_headers = dict(headers or {})
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    req = request.Request(url, data=data, headers=request_headers, method=method)
    with request.urlopen(req, timeout=60) as resp:
        return read_json_response(resp)


def head_exists(url: str, timeout: int = 20) -> bool:
    req = request.Request(url, method="HEAD")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400
    except error.HTTPError as exc:
        if exc.code == 405:
            fallback = request.Request(url, method="GET", headers={"Range": "bytes=0-0"})
            try:
                with request.urlopen(fallback, timeout=timeout) as resp:
                    return 200 <= resp.status < 400
            except Exception:
                return False
        return False
    except Exception:
        return False


def build_image_url(product_type: str, design: str, device_code: str) -> str:
    base_design, variant_code = split_design(design)
    template = IMAGE_TEMPLATE[product_type]
    return template.format(DESIGN=base_design, VARIANT=variant_code, DEVICE=device_code)


def resolve_device_name(device_code: str, device_map: dict[str, str]) -> str:
    mapped = device_map.get(device_code)
    if mapped:
        return normalize_device_name(mapped)
    return device_code


def build_variant_group_id(product_type: str, design: str, primary_device_code: str) -> str:
    return f"{product_type}-{device_brand_short(primary_device_code)}-{design}"


def build_item_payload(
    *,
    candidate: CandidateResult,
    metadata: DesignMetadata,
    product_type: str,
    variant_group_id: str,
    price: float,
    primary_sku: str,
) -> dict[str, Any]:
    case_type_name = CASE_TYPE_NAME[product_type]
    title = build_title(
        license_name=metadata.license_name,
        design_name=metadata.design_name,
        case_type_name=case_type_name,
        full_device_name=candidate.full_device_name,
    )
    device_brand = device_brand_name(candidate.device_code)
    item = {
        "sku": candidate.sku,
        "productType": "Cell Phone Cases",
        "variantGroupId": variant_group_id,
        "variantAttributeNames": ["actual_color", "size"],
        "isPrimaryVariant": candidate.sku == primary_sku,
        "Orderable": {
            "sku": candidate.sku,
            "productId": candidate.ean,
            "productIdType": "EAN",
            "price": price,
            "currency": DEFAULT_CURRENCY,
            "mustShipAlone": "No",
            "manufacturerPartNumber": candidate.sku,
        },
        "Visible": {
            "productName": title,
            "brand": DEFAULT_BRAND,
            "manufacturer": DEFAULT_BRAND,
            "mainImageUrl": candidate.image_url,
            "shortDescription": metadata.short_description,
            "longDescription": metadata.long_description[:4000],
            "actual_color": metadata.design_name,
            "size": candidate.full_device_name,
            "modelNumber": candidate.sku,
            "compatibleBrand": device_brand,
            "compatibleModels": [candidate.full_device_name],
            "cellPhoneCaseType": case_type_name,
            "material": "TPU" if product_type == "HTPCR" else "Polycarbonate",
        },
        "groupingAttributes": [
            {"name": "actual_color", "value": metadata.design_name},
            {"name": "size", "value": candidate.full_device_name},
        ],
    }
    return item


def parse_feed_url(feed_url: str) -> tuple[str, str | None]:
    parsed = parse.urlsplit(feed_url)
    params = parse.parse_qs(parsed.query)
    feed_type = params.get("feedType", [None])[0]
    base_url = parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
    return base_url, feed_type


def submit_feed(
    auth: WalmartAuth,
    feed_url: str,
    feed_payload: dict[str, Any],
    feed_type_override: str | None = None,
) -> tuple[str, dict[str, Any], str]:
    base_url, configured_feed_type = parse_feed_url(feed_url)
    feed_types = [feed_type_override or configured_feed_type or "item"]
    for fallback in ("MP_ITEM", "item"):
        if fallback not in feed_types:
            feed_types.append(fallback)

    token = auth.bearer_token()
    last_error: Exception | None = None
    for feed_type in feed_types:
        submit_url = f"{base_url}?feedType={parse.quote(feed_type, safe='')}"
        try:
            response = http_json(
                submit_url,
                method="POST",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {token}",
                    "WM_QOS.CORRELATION_ID": str(uuid.uuid4()),
                },
                payload=feed_payload,
            )
            feed_id = clean_text(
                response.get("feedId")
                or response.get("id")
                or response.get("feed_id")
                or response.get("data", {}).get("feedId")
            )
            if not feed_id:
                raise RuntimeError(f"Feed submission succeeded but no feedId was returned: {response}")
            return feed_id, response, feed_type
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            last_error = RuntimeError(f"Feed submit failed for feedType={feed_type}: HTTP {exc.code} {body}")
            if exc.code not in {400, 404, 415}:
                raise last_error
        except Exception as exc:
            last_error = exc
    assert last_error is not None
    raise last_error


def poll_feed(
    auth: WalmartAuth,
    feed_url: str,
    feed_id: str,
    *,
    poll_interval: int,
    timeout_seconds: int,
) -> dict[str, Any]:
    base_url, _ = parse_feed_url(feed_url)
    status_url = f"{base_url}/{feed_id}"
    deadline = time.time() + timeout_seconds
    while True:
        payload = http_json(
            status_url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {auth.bearer_token()}",
                "WM_QOS.CORRELATION_ID": str(uuid.uuid4()),
            },
        )
        status = clean_text(
            payload.get("feedStatus")
            or payload.get("status")
            or payload.get("processingStatus")
            or payload.get("data", {}).get("feedStatus")
        ).upper()
        if status in {"PROCESSED", "COMPLETED", "DONE", "ERROR", "FAILED"}:
            return payload
        if time.time() >= deadline:
            raise TimeoutError(f"Timed out waiting for feed {feed_id}. Last response: {payload}")
        time.sleep(poll_interval)


def maybe_fetch_result_document(url: str) -> list[dict[str, Any]]:
    if not url:
        return []
    try:
        req = request.Request(url, headers={"Accept": "application/json,text/csv,*/*"})
        with request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8", "replace")
    except Exception:
        return []

    try:
        parsed_json = json.loads(body)
    except json.JSONDecodeError:
        parsed_json = None

    if isinstance(parsed_json, list):
        return [row for row in parsed_json if isinstance(row, dict)]
    if isinstance(parsed_json, dict):
        for key in ("items", "itemDetails", "results", "errors"):
            value = parsed_json.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
        return [parsed_json]

    reader = csv.DictReader(body.splitlines())
    return [dict(row) for row in reader]


def summarize_feed_results(feed_status: dict[str, Any]) -> dict[str, Any]:
    result_url = ""
    for key in ("resultFileUrl", "itemDetailsUrl", "errorFileUrl", "downloadUrl"):
        result_url = clean_text(feed_status.get(key) or feed_status.get("data", {}).get(key))
        if result_url:
            break
    records = maybe_fetch_result_document(result_url)
    per_item: list[dict[str, str]] = []
    for record in records:
        sku = clean_text(
            record.get("sku")
            or record.get("SellerSku")
            or record.get("sellerSku")
            or record.get("itemIdentifier")
        )
        status = clean_text(record.get("status") or record.get("feedStatus") or record.get("result") or "UNKNOWN")
        message = clean_text(
            record.get("message")
            or record.get("description")
            or record.get("errorDescription")
            or record.get("errorMessage")
        )
        if sku or message:
            per_item.append({"sku": sku, "status": status, "message": message})

    return {
        "feed_status": clean_text(
            feed_status.get("feedStatus")
            or feed_status.get("status")
            or feed_status.get("processingStatus")
            or feed_status.get("data", {}).get("feedStatus")
        ),
        "result_url": result_url,
        "raw": feed_status,
        "items": per_item,
    }


def build_candidates(
    *,
    design: str,
    product_type: str,
    device_codes: list[str],
    ean_lookup: dict[str, str],
    device_map: dict[str, str],
    skip_image_check: bool,
    workers: int,
) -> tuple[list[CandidateResult], list[dict[str, str]]]:
    candidate_rows: list[tuple[str, str, str, str | None]] = []
    skipped: list[dict[str, str]] = []
    for device_code in device_codes:
        base_design, variant_code = split_design(design)
        sku = f"{product_type}-{device_code}-{base_design}-{variant_code}"
        ean = clean_text(ean_lookup.get(sku))
        full_device_name = resolve_device_name(device_code, device_map)
        image_url = build_image_url(product_type, design, device_code)
        if not ean:
            skipped.append({"sku": sku, "reason": "missing_ean"})
            continue
        candidate_rows.append((sku, device_code, full_device_name, ean))

    results: list[CandidateResult] = []
    if skip_image_check:
        for sku, device_code, full_device_name, ean in candidate_rows:
            results.append(
                CandidateResult(
                    sku=sku,
                    device_code=device_code,
                    full_device_name=full_device_name,
                    ean=ean,
                    image_url=build_image_url(product_type, design, device_code),
                    image_exists=True,
                )
            )
        return results, skipped

    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        future_map = {}
        for sku, device_code, full_device_name, ean in candidate_rows:
            image_url = build_image_url(product_type, design, device_code)
            future = executor.submit(head_exists, image_url)
            future_map[future] = (sku, device_code, full_device_name, ean, image_url)
        for future in as_completed(future_map):
            sku, device_code, full_device_name, ean, image_url = future_map[future]
            exists = future.result()
            if exists:
                results.append(
                    CandidateResult(
                        sku=sku,
                        device_code=device_code,
                        full_device_name=full_device_name,
                        ean=ean,
                        image_url=image_url,
                        image_exists=True,
                    )
                )
            else:
                skipped.append({"sku": sku, "reason": "missing_image"})
    results.sort(key=lambda item: device_codes.index(item.device_code))
    return results, skipped


def build_feed_payload(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "MPItemFeedHeader": {
            "version": "5.0",
            "locale": "en",
            "sellingChannel": "marketplace",
            "feedDate": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "MPItem": items,
    }


def load_designs(path: Path) -> list[DesignRecord]:
    payload = load_json(path)
    records: list[DesignRecord] = []
    for row in payload:
        records.append(
            DesignRecord(
                design=clean_text(row.get("design")),
                revenue=float(row.get("revenue") or 0),
                orders=int(row.get("orders") or 0),
                types=list(row.get("types") or []),
            )
        )
    return records


def choose_designs(records: list[DesignRecord], *, design: str | None, top: int | None) -> list[DesignRecord]:
    if design:
        selected = [row for row in records if row.design == design]
        if not selected:
            raise SystemExit(f"Design {design!r} was not found in champions data.")
        return selected
    if top:
        return records[:top]
    raise SystemExit("Provide either --design or --top.")


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload Walmart item feeds for Head Case designs.")
    parser.add_argument("--design", help="Single design code in DESIGN-VARIANT form, e.g. DRGBSUSC-GOK")
    parser.add_argument("--top", type=int, help="Upload the top N champion designs")
    parser.add_argument("--product-type", choices=sorted(CASE_TYPE_NAME), default=DEFAULT_PRODUCT_TYPE)
    parser.add_argument("--price", type=float, default=DEFAULT_PRICE)
    parser.add_argument("--dry-run", action="store_true", help="Build feed JSON and save it to output without submitting")
    parser.add_argument("--skip-image-check", action="store_true", help="Skip HEAD image validation")
    parser.add_argument("--poll-interval", type=int, default=30)
    parser.add_argument("--timeout", type=int, default=1800, help="Polling timeout in seconds")
    parser.add_argument("--workers", type=int, default=8, help="Concurrent image HEAD workers")
    parser.add_argument("--token-url", default=DEFAULT_TOKEN_URL)
    parser.add_argument("--feed-url", default=DEFAULT_FEED_URL)
    parser.add_argument("--feed-type", default=None, help="Override feedType query parameter if needed")
    parser.add_argument("--client-id", default=DEFAULT_CLIENT_ID)
    parser.add_argument("--client-secret", default=DEFAULT_CLIENT_SECRET)
    return parser.parse_args(argv)


def find_input_file(primary: Path, alternate: Path | None = None) -> Path:
    if primary.exists():
        return primary
    if alternate and alternate.exists():
        return alternate
    raise FileNotFoundError(f"Required input file not found: {primary}")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    BC_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    paths = default_paths()
    champions_path = find_input_file(paths["champions"], paths["champions_alt"])
    ean_path = find_input_file(paths["ean"])
    device_map_path = find_input_file(paths["device_map"])

    design_records = load_designs(champions_path)
    selected_designs = choose_designs(design_records, design=args.design, top=args.top)
    ean_lookup = load_json(ean_path)
    device_map = load_json(device_map_path)
    bc_client = BigCommerceClient(BC_CACHE_DIR)

    submitted: list[dict[str, Any]] = []
    for design_record in selected_designs:
        metadata = resolve_design_metadata(
            design=design_record.design,
            product_type=args.product_type,
            bc_client=bc_client,
            device_map=device_map,
        )
        candidates, skipped = build_candidates(
            design=design_record.design,
            product_type=args.product_type,
            device_codes=TOP_DEVICES,
            ean_lookup=ean_lookup,
            device_map=device_map,
            skip_image_check=args.skip_image_check,
            workers=args.workers,
        )

        if not candidates:
            result = {
                "design": design_record.design,
                "product_type": args.product_type,
                "status": "skipped",
                "reason": "no_valid_items",
                "skipped": skipped,
            }
            submitted.append(result)
            continue

        variant_group_id = build_variant_group_id(args.product_type, design_record.design, candidates[0].device_code)
        primary_sku = candidates[0].sku
        items = [
            build_item_payload(
                candidate=candidate,
                metadata=metadata,
                product_type=args.product_type,
                variant_group_id=variant_group_id,
                price=args.price,
                primary_sku=primary_sku,
            )
            for candidate in candidates
        ]
        feed_payload = build_feed_payload(items)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        feed_path = OUTPUT_DIR / f"walmart_feed_{design_record.design}_{args.product_type}_{timestamp}.json"
        save_json(feed_path, feed_payload)

        result: dict[str, Any] = {
            "design": design_record.design,
            "product_type": args.product_type,
            "variant_group_id": variant_group_id,
            "feed_json_path": str(feed_path),
            "item_count": len(items),
            "skipped": skipped,
        }

        if args.dry_run:
            result["status"] = "dry_run"
            submitted.append(result)
            continue

        auth = WalmartAuth(
            client_id=args.client_id,
            client_secret=args.client_secret,
            token_url=args.token_url,
        )
        try:
            feed_id, submit_response, used_feed_type = submit_feed(
                auth=auth,
                feed_url=args.feed_url,
                feed_payload=feed_payload,
                feed_type_override=args.feed_type,
            )
            status_payload = poll_feed(
                auth=auth,
                feed_url=args.feed_url,
                feed_id=feed_id,
                poll_interval=args.poll_interval,
                timeout_seconds=args.timeout,
            )
            summary = summarize_feed_results(status_payload)
            result.update(
                {
                    "status": "submitted",
                    "feed_id": feed_id,
                    "used_feed_type": used_feed_type,
                    "submit_response": submit_response,
                    "feed_summary": summary,
                }
            )
        except Exception as exc:
            result.update(
                {
                    "status": "error",
                    "error": str(exc),
                }
            )
        submitted.append(result)

    report_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = OUTPUT_DIR / f"walmart_upload_report_{report_timestamp}.json"
    save_json(report_path, submitted)

    for result in submitted:
        design = result["design"]
        status = result["status"]
        print(f"{design}: {status}")
        if result.get("feed_id"):
            print(f"  feed_id={result['feed_id']} feed_type={result.get('used_feed_type')}")
        if result.get("feed_summary", {}).get("feed_status"):
            print(f"  walmart_status={result['feed_summary']['feed_status']}")
        if result.get("item_count") is not None:
            print(f"  items={result['item_count']} skipped={len(result.get('skipped', []))}")
        if result.get("error"):
            print(f"  error={result['error']}")
        for item in result.get("feed_summary", {}).get("items", [])[:20]:
            print(f"  item sku={item['sku']} status={item['status']} message={item['message']}")

    print(f"Report saved to {report_path}")
    return 0 if all(row["status"] in {"dry_run", "submitted"} for row in submitted) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
