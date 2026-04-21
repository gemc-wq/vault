import requests
import json
import os
from datetime import datetime, timedelta

# Veeqo API Config
API_KEY = os.environ.get('VEEQO_API_KEY')
BASE_URL = "https://api.veeqo.com"

def get_aged_backlog(warehouse_id=None, hours=48):
    """
    Fetch orders in 'awaiting_fulfillment' status created more than X hours ago.
    """
    if not API_KEY:
        return {"error": "VEEQO_API_KEY not set"}
    
    threshold_time = datetime.utcnow() - timedelta(hours=hours)
    # Veeqo expects YYYY-MM-DD HH:MM:SS
    created_at_max = threshold_time.strftime('%Y-%m-%d %H:%M:%S')
    
    headers = {'x-api-key': API_KEY}
    params = {
        'status': 'awaiting_fulfillment',
        'page_size': 100
    }
    
    if warehouse_id:
        params['allocated_at'] = warehouse_id

    # Note: Veeqo API doesn't have a direct 'created_at_max' filter in docs, 
    # so we fetch and filter locally or use updated_at_min if appropriate.
    # For now, we'll fetch the first page and filter.
    
    response = requests.get(f"{BASE_URL}/orders", headers=headers, params=params)
    
    if response.status_code != 200:
        return {"error": f"API Error: {response.status_code}", "detail": response.text}
    
    orders = response.json()
    aged_orders = [o for o in orders if o['created_at'] < created_at_max.replace(' ', 'T') + 'Z']
    
    return aged_orders

if __name__ == "__main__":
    # Placeholder for test run
    print("Veeqo Triage Script Ready.")
