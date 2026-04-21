import sqlite3
import json

DB_PATH = "/Users/openclaw/.openclaw/workspace/data/local_listings.db"
RESULTS_PATH = "/Users/openclaw/.openclaw/workspace/projects/sku-staging/ean_search_results.json"

def search_in_listings():
    with open(RESULTS_PATH, 'r') as f:
        data = json.load(f)
    
    missing = data['missing']
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    found_in_listings = {}
    still_missing = []
    
    print(f"Searching for {len(missing)} missing groups in listings tables...")
    
    for code in missing:
        # Search in US current
        cursor.execute("SELECT seller_sku, product_id FROM listings_current WHERE seller_sku LIKE ? AND product_id_type = '4' LIMIT 5", (f'%-{code}-%',))
        rows = cursor.fetchall()
        
        if not rows:
            # Search in UK current
            cursor.execute("SELECT seller_sku, product_id FROM listings_uk_current WHERE seller_sku LIKE ? AND product_id_type = '4' LIMIT 5", (f'%-{code}-%',))
            rows = cursor.fetchall()
            
        if rows:
            found_in_listings[code] = [{"sku": r[0], "gtin": r[1]} for r in rows]
            print(f"Found {code} in listings!")
        else:
            still_missing.append(code)
            
    conn.close()
    
    print(f"Newly found: {len(found_in_listings)}")
    print(f"Still missing: {len(still_missing)}")
    
    # Merge results
    data['found'].update(found_in_listings)
    data['missing'] = still_missing
    data['found_count'] = len(data['found'])
    data['missing_count'] = len(data['missing'])
    
    with open(RESULTS_PATH, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    search_in_listings()
