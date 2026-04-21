import os
from lane1_poc_v3 import process_smart_object
from lane2_seo_poc import generate_seo_copy
from lane3_export_poc import generate_shopify_export

def run_pipeline(designs, devices, case_type):
    print("🚀 Starting ListingForge Pipeline...")
    
    # 1. Lane 1: Image Generation
    print("\n--- [LANE 1] Image Generation ---")
    for design in designs:
        input_art = f"raw_art/{design['code']}.jpg"
        output_img = f"output/images/{design['code']}_jig.png"
        
        # Simulate processing (would normally call process_smart_object here)
        print(f"Generated composite for {design['code']}")
        # Assign mock image URL for the export
        design['image_url'] = f"https://elcellonline.com/mockups/{design['code']}.jpg"

    # 2. Lane 2: SEO Copy Generation
    print("\n--- [LANE 2] SEO Copy Generation ---")
    for design in designs:
        for device in devices:
            seo_data = generate_seo_copy(design['name'], device['name'], case_type)
            # Flatten bullets for the HTML body description
            design['bullets'] = " ".join([f"<li>{b}</li>" for b in seo_data['bullets']])
            print(f"Generated SEO copy for {design['code']} x {device['code']}")

    # 3. Lane 3: Shopify CSV Export
    print("\n--- [LANE 3] Shopify CSV Export ---")
    export_path = "output/shopify_listingforge_import.csv"
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    generate_shopify_export(designs, devices, export_path)
    print(f"Pipeline complete. Export saved to {export_path}")

if __name__ == "__main__":
    test_designs = [
        {"code": "NARUICO", "name": "Naruto Shippuden Akatsuki", "gtin": "00506075082063"},
        {"code": "HPOTDH37", "name": "Harry Potter Deathly Hallows", "gtin": "00506075082064"}
    ]
    test_devices = [
        {"code": "IPH16", "name": "iPhone 16"},
        {"code": "S24", "name": "Galaxy S24"}
    ]
    
    run_pipeline(test_designs, test_devices, "Hybrid MagSafe Case")
