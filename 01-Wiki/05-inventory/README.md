# Inventory Management
> **Updated:** 2026-03-18

## Inventory Tracker v1 (built Mar 12)
- Supabase: `blank_inventory` table + `v_inventory_alerts_v2` view
- Snapshot: 5,193 active blank SKUs (PH 2,936, UK 2,502, FL 1,195)
- 77% dead stock (zero sales)
- Scripts: `scripts/snapshot_inventory.py`, `deduct_inventory.py`, `setup_inventory_schema.py`
- Spec: `scripts/INVENTORY_SPEC.md`

## Local SQLite Database (built Mar 15)
- `data/local_listings.db` — 2.6 GB
- US listings: 3.43M (from Mar 15 Active Listings Report)
- UK listings: 5.09M (from Mar 11 Active Listings Report)
- EAN database: 600K records (473K assigned, 52K valid unassigned)
- Delta refresh script: `scripts/refresh_listings.py`
- Query speed: <1ms ASIN lookup, 17ms full count

## EAN Management
- Combined lookup: `data/ean/combined_ean_lookup.json` (480K mappings)
- Sources: Target master list (35K) + PH database (473K) + auto-assigned (7.3K)
- Auto-assignment engine for new SKUs without EANs
