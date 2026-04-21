import csv
import json
import os

def generate_shopify_export(designs, device_configs, output_file):
    """
    Mock integration for Lane 3 Bulk Export generation.
    Takes design definitions and device configurations, and outputs a Shopify CSV.
    """
    headers = [
        "Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags",
        "Published", "Option1 Name", "Option1 Value", "Variant SKU", "Variant Price", 
        "Variant Barcode", "Image Src"
    ]
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for design in designs:
            for device in device_configs:
                handle = f"{design['code']}-{device['code']}"
                title = f"{design['name']} Case for {device['name']}"
                body = f"<p>Premium {design['name']} design for your {device['name']}. {design.get('bullets', '')}</p>"
                sku = f"{device['code']}-{design['code']}"
                price = "24.99"
                
                # Write parent row
                writer.writerow([
                    handle, title, body, "Head Case Designs", "Phone Cases", "Case", 
                    f"{design['name']},{device['name']}", "TRUE", "Model", device['name'], 
                    sku, price, design.get("gtin", ""), design.get("image_url", "")
                ])

if __name__ == "__main__":
    print("Testing Lane 3 Shopify Export POC...")
    
    sample_designs = [
        {"code": "NARUICO", "name": "Naruto Shippuden Akatsuki", "gtin": "00506075082063", "image_url": "https://example.com/naruto.jpg"},
        {"code": "HPOTDH37", "name": "Harry Potter Deathly Hallows", "gtin": "00506075082064", "image_url": "https://example.com/hp.jpg"}
    ]
    
    sample_devices = [
        {"code": "IPH16", "name": "iPhone 16"},
        {"code": "S24", "name": "Galaxy S24"}
    ]
    
    output_path = "output/lane3_shopify_export_poc.csv"
    generate_shopify_export(sample_designs, sample_devices, output_path)
    
    print(f"Generated sample export at {output_path}")
