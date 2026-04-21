import os
import json
import csv
import requests
from collections import defaultdict
from datetime import datetime, timedelta

# Configurations
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
BC_STORE_HASH = "otle45p56l"
BC_TOKEN = os.getenv("BIGCOMMERCE_ACCESS_TOKEN", "")
BC_HEADERS = {
    "X-Auth-Token": BC_TOKEN,
    "Accept": "application/json"
}

TOP_DEVICES = ["IPH17PMAX", "IPH17PRO", "IPH17", "IPH16PMAX", "IPH16PRO", "IPH16", "IPH15PMAX", "IPH15PRO", "S25ULTRA", "S25PLUS"]
CASE_PREFIX_MAP = {
    "HTPCR": "TP-CR",
    "HB401": "B4-01",
    "HC": "HC-CR",
    "HLBWH": "LB-WH",
    "HB6CR": "B6-CR",
    "HB7BK": "B7-BK"
}
TARGET_CASE_TYPES = ["HTPCR", "HB401", "HC"]

EAN_LOOKUP_FILE_1 = "/Users/openclaw/.openclaw/workspace/projects/sku-staging/output/shopify_import_top50_with_images.csv"
EAN_LOOKUP_FILE_2 = "/Users/openclaw/.openclaw/workspace/projects/walmart-lister/ean_lookup.json"
OUTPUT_DIR = "/Users/openclaw/.openclaw/workspace/projects/shopify-repush/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "shopify_products_top50.json")

def load_ean_lookup():
    ean_map = {}
    if os.path.exists(EAN_LOOKUP_FILE_1):
        try:
            with open(EAN_LOOKUP_FILE_1, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sku = row.get("SKU") or row.get("sku")
                    barcode = row.get("Barcode") or row.get("barcode") or row.get("EAN")
                    if sku and barcode:
                        ean_map[sku.upper()] = barcode
        except Exception as e:
            pass

    if os.path.exists(EAN_LOOKUP_FILE_2):
        try:
            with open(EAN_LOOKUP_FILE_2, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for k, v in data.items():
                        ean_map[k.upper()] = str(v)
        except Exception as e:
            pass
    return ean_map

def get_champion_designs():
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    date_90d_ago = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%S")
    limit = 1000
    offset = 0
    design_revenue = defaultdict(float)
    
    while True:
        url = f"{SUPABASE_URL}/rest/v1/orders?select=design_code,net_sale_usd,product_type_code&paid_date=gte.{date_90d_ago}&limit={limit}&offset={offset}"
        resp = requests.get(url, headers=headers)
        if not resp.ok:
            break
        data = resp.json()
        if not data:
            break
        for row in data:
            design_code = row.get("design_code")
            ptype = row.get("product_type_code", "")
            if ptype and ptype.startswith("F"):
                ptype = ptype[1:]
            if ptype in TARGET_CASE_TYPES and design_code:
                rev = float(row.get("net_sale_usd") or 0)
                design_revenue[design_code] += rev
        offset += limit

    sorted_designs = sorted(design_revenue.items(), key=lambda x: x[1], reverse=True)
    return [d[0] for d in sorted_designs[:50]]

def fetch_bc_product_data(design_code):
    url = f"https://api.bigcommerce.com/stores/{BC_STORE_HASH}/v3/catalog/products?keyword={design_code}&include=images,custom_fields,variants"
    resp = requests.get(url, headers=BC_HEADERS)
    if resp.ok:
        data = resp.json().get("data", [])
        for item in data:
            if design_code in item.get("sku", "").upper() or design_code in item.get("name", "").upper():
                return item
    return None

def check_s3_image(design, variant, case_type, device):
    prefix = CASE_PREFIX_MAP.get(case_type)
    if not prefix: return None
    url = f"https://elcellonline.com/atg/{design}/{variant}/{prefix}-{device}-1.jpg"
    try:
        if requests.head(url, timeout=3).status_code == 200:
            return url
    except:
        pass
    return None

def main():
    ean_map = load_ean_lookup()
    champions = get_champion_designs()
    
    shopify_products = []
    stats = {
        "total_prepared": 0,
        "s3_images": 0,
        "bc_images": 0,
        "no_images": 0,
        "has_ean": 0,
        "missing_ean": 0,
        "ready_for_push": 0,
        "blocked": 0
    }

    for design in champions:
        bc_data = fetch_bc_product_data(design)
        if not bc_data:
            continue
            
        bc_images = [img["url_standard"] for img in bc_data.get("images", []) if "url_standard" in img]
        custom_fields = {cf["name"]: cf["value"] for cf in bc_data.get("custom_fields", [])}
        
        design_name = custom_fields.get("DesignName", design)
        brand_name = custom_fields.get("BrandCode", "Head Case Designs")
        
        # Determine variant
        variants_data = bc_data.get("variants", [])
        sample_variant = "HOP" # fallback
        for v in variants_data:
            sku_parts = v.get("sku", "").split("-")
            if len(sku_parts) >= 4 and sku_parts[2] == design:
                sample_variant = sku_parts[3]
                break
        
        for device in TOP_DEVICES:
            for case_type in TARGET_CASE_TYPES:
                sku = f"{case_type}-{device}-{design}-{sample_variant}"
                ean = ean_map.get(sku.upper())
                
                if ean: stats["has_ean"] += 1
                else: stats["missing_ean"] += 1
                
                img_url = check_s3_image(design, sample_variant, case_type, device)
                if img_url:
                    stats["s3_images"] += 1
                elif bc_images:
                    img_url = bc_images[0]
                    stats["bc_images"] += 1
                else:
                    stats["no_images"] += 1
                
                if ean and img_url:
                    stats["ready_for_push"] += 1
                else:
                    stats["blocked"] += 1
                
                product = {
                    "title": f"{brand_name} {design_name} Case for {device}",
                    "body_html": bc_data.get("description", ""),
                    "vendor": "Head Case Designs",
                    "product_type": "Phone Case",
                    "tags": f"lineup:{design}, device:{device}, pulse-champion, brand:{brand_name}, type:{case_type}",
                    "variants": [
                        {
                            "sku": sku,
                            "price": "19.95" if case_type in ["HTPCR", "HB401"] else "24.95",
                            "barcode": ean or "",
                            "weight": 0.1 if case_type == "HTPCR" else (0.15 if case_type == "HB401" else 0.2),
                            "weight_unit": "kg",
                            "option1": "Soft Gel Case" if case_type == "HTPCR" else "Hybrid Case"
                        }
                    ],
                    "images": [{"src": img_url, "position": 1}] if img_url else [],
                    "metafields": [
                        {"namespace": "custom", "key": "brand_name", "value": brand_name, "type": "single_line_text_field"},
                        {"namespace": "custom", "key": "compatible_device", "value": device, "type": "single_line_text_field"},
                        {"namespace": "custom", "key": "case_type", "value": case_type, "type": "single_line_text_field"},
                        {"namespace": "custom", "key": "design_name", "value": design_name, "type": "single_line_text_field"}
                    ]
                }
                shopify_products.append(product)
                stats["total_prepared"] += 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(shopify_products, f, indent=2)
        
    print("\n--- Summary Report ---")
    print(f"Total products prepared: {stats['total_prepared']}")
    print(f"Images: {stats['s3_images']} S3 | {stats['bc_images']} BC Fallback | {stats['no_images']} None")
    print(f"EANs: {stats['has_ean']} Found | {stats['missing_ean']} Missing")
    print(f"Status: {stats['ready_for_push']} Ready for Push | {stats['blocked']} Blocked")
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
