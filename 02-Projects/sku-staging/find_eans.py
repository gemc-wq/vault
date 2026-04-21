import sqlite3
import json
import os

DB_PATH = "/Users/openclaw/.openclaw/workspace/data/local_listings.db"
CHAMPIONS_PATH = "/Users/openclaw/.openclaw/workspace/projects/sku-staging/combined_backcase_champions.json"

def find_eans():
    with open(CHAMPIONS_PATH, 'r') as f:
        champions = json.load(f)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    results = {}
    missing = []
    
    # Extract unique design codes from champions
    # Note: 'design' in champions is usually DESIGN-VARIANT or just DESIGN
    # We need the part before the dash if it's the design code
    design_codes = set()
    for c in champions:
        design = c['design']
        if '-' in design:
            code = design.split('-')[0]
        else:
            code = design
        design_codes.add(code)
    
    print(f"Checking {len(design_codes)} unique design groups...")
    
    for code in sorted(list(design_codes)):
        # Search for any SKU in ean_database that contains this design code
        # Pattern: %-CODE-% or %-CODE (if at end)
        cursor.execute("SELECT sku, gtin FROM ean_database WHERE sku LIKE ? LIMIT 5", (f'%-{code}-%',))
        rows = cursor.fetchall()
        
        if rows:
            results[code] = [{"sku": r[0], "gtin": r[1]} for r in rows]
        else:
            # Try at the end of SKU
            cursor.execute("SELECT sku, gtin FROM ean_database WHERE sku LIKE ? LIMIT 5", (f'%-{code}',))
            rows = cursor.fetchall()
            if rows:
                results[code] = [{"sku": r[0], "gtin": r[1]} for r in rows]
            else:
                missing.append(code)
    
    conn.close()
    
    print(f"Found EANs for {len(results)} design groups.")
    print(f"Missing EANs for {len(missing)} design groups.")
    
    # Save results
    output = {
        "found_count": len(results),
        "missing_count": len(missing),
        "found": results,
        "missing": missing
    }
    
    output_path = "/Users/openclaw/.openclaw/workspace/projects/sku-staging/ean_search_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    find_eans()
