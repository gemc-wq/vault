# Tailscale Setup Guide — PH to Mac Studio Data Bridge
**Date:** 2026-04-10 | **Author:** Athena
**Purpose:** Secure read-only access to PH MySQL (192.168.20.160) from Mac Studio via Tailscale mesh VPN

---

## Overview

```
Mac Studio (openclaw)          Tailscale Network          PH Office
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ Python sync      │       │  Encrypted tunnel │       │ PH PC (Splashtop)│
│ script           │◄─────►│  No firewall      │◄─────►│ Subnet router    │
│                  │       │  changes needed   │       │                  │
│ BigQuery writer  │       └──────────────────┘       │  ┌──────────────┐│
│                  │                                    │  │192.168.20.160││
│ Cron: every 6hr  │         Direct MySQL access        │  │MySQL 8.0     ││
│                  │◄──────────────────────────────────►│  │67GB, 453 tbl ││
└──────────────────┘         (read-only)                │  └──────────────┘│
                                                        └──────────────────┘
```

---

## Step 1: Create Tailscale Account

1. Go to https://login.tailscale.com
2. Sign up with your Google account (gemc@ecellglobal.com) or create a new account
3. This creates your **Tailnet** — your private mesh network

---

## Step 2: Install Tailscale on Mac Studio

Open Terminal on the Mac Studio:

```bash
# Install via Homebrew
brew install --cask tailscale

# Or download from https://tailscale.com/download/mac
```

After install:
1. Open Tailscale from Applications (or menu bar icon)
2. Click **Log in** — authenticate with the same account from Step 1
3. Note the Tailscale IP assigned (e.g., 100.x.y.z)

Verify it's connected:
```bash
tailscale status
```

---

## Step 3: Install Tailscale on PH PC (via Splashtop)

1. Remote into the PH PC via Splashtop
2. Check the OS — likely Windows. Download from: https://tailscale.com/download/windows
3. Run the installer (no admin changes to the firewall needed)
4. Log in with the **same Tailscale account** from Step 1
5. Note the Tailscale IP assigned to the PH PC (e.g., 100.a.b.c)

---

## Step 4: Enable Subnet Routing on PH PC

This is the key step — it lets the Mac Studio reach the entire PH LAN (192.168.20.0/24) through the PH PC.

On the PH PC (Windows CMD as Administrator):

```cmd
tailscale up --advertise-routes=192.168.20.0/24
```

Then approve the subnet route in the Tailscale admin console:
1. Go to https://login.tailscale.com/admin/machines
2. Find the PH PC
3. Click the **...** menu → **Edit route settings**
4. Enable the `192.168.20.0/24` subnet route
5. Click **Save**

On the Mac Studio, accept the subnet route:
```bash
# Verify you can see the PH PC
tailscale status

# Test reaching the MySQL server
ping 192.168.20.160
```

If ping works, the tunnel is live. 🎉

---

## Step 5: Create Read-Only MySQL User on PH Database

Connect to 192.168.20.160 via the PH PC (or from Mac Studio once Tailscale is up):

```bash
mysql -h 192.168.20.160 -u root -p
```

Then run:

```sql
-- Create read-only user for Athena sync
CREATE USER 'athena_readonly'@'%' IDENTIFIED BY 'EcellSync2026!ReadOnly';

-- Grant SELECT only on key inventory/product tables
GRANT SELECT ON *.* TO 'athena_readonly'@'%';

-- If you want to restrict to specific tables only (safer):
-- GRANT SELECT ON zero_db.blank_inventory TO 'athena_readonly'@'%';
-- GRANT SELECT ON zero_db.design_codes TO 'athena_readonly'@'%';
-- GRANT SELECT ON zero_db.products TO 'athena_readonly'@'%';
-- (add more tables as needed)

FLUSH PRIVILEGES;
```

⚠️ **Change the password** before running this. The one above is a placeholder.

Verify from Mac Studio:
```bash
mysql -h 192.168.20.160 -u athena_readonly -p -e "SELECT COUNT(*) FROM information_schema.tables;"
```

---

## Step 6: Test Connection from Mac Studio

```bash
# Install MySQL client if not already present
brew install mysql-client

# Test direct connection over Tailscale
mysql -h 192.168.20.160 -u athena_readonly -p -e "SHOW DATABASES;"
```

Expected output: list of databases on the PH server. If this works, the full pipeline is viable.

---

## Step 7: BigQuery Sync Script

Save this to `~/zeus-agent/scripts/ph_to_bigquery_sync.py`:

```python
#!/usr/bin/env python3
"""
PH MySQL → BigQuery Sync
Runs every 6 hours via cron. Read-only access to PH database over Tailscale.
"""
import os
import logging
from datetime import datetime
import mysql.connector
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)

# Config — update these
PH_MYSQL = {
    "host": "192.168.20.160",
    "user": "athena_readonly",
    "password": os.environ.get("PH_MYSQL_PASSWORD", ""),
    "database": "zero_db",  # Update to actual DB name
    "connect_timeout": 30,
}

BQ_PROJECT = "instant-contact-479316-i4"
BQ_DATASET = "zero_dataset"

# Tables to sync (PH table → BQ table)
SYNC_TABLES = {
    "blank_inventory": "ph_blank_inventory",
    "design_codes": "ph_design_codes",
    "products": "ph_products",
    # Add more as needed
}

def sync_table(mysql_conn, bq_client, source_table, dest_table):
    """Read from PH MySQL, write to BigQuery."""
    cursor = mysql_conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {source_table}")
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        log.info(f"  {source_table}: no rows, skipping")
        return 0

    table_id = f"{BQ_PROJECT}.{BQ_DATASET}.{dest_table}"

    # Auto-detect schema from first row
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # Full replace each sync
        autodetect=True,
    )

    job = bq_client.load_table_from_json(rows, table_id, job_config=job_config)
    job.result()  # Wait for completion

    log.info(f"  {source_table} → {dest_table}: {len(rows)} rows synced")
    return len(rows)

def main():
    log.info("=== PH → BigQuery Sync Starting ===")

    # Connect to PH MySQL over Tailscale
    try:
        mysql_conn = mysql.connector.connect(**PH_MYSQL)
        log.info(f"Connected to PH MySQL ({PH_MYSQL['host']})")
    except Exception as e:
        log.error(f"MySQL connection failed: {e}")
        log.error("Is Tailscale running? Check: tailscale status")
        return

    # Connect to BigQuery
    bq_client = bigquery.Client(project=BQ_PROJECT)

    total = 0
    for source, dest in SYNC_TABLES.items():
        try:
            total += sync_table(mysql_conn, bq_client, source, dest)
        except Exception as e:
            log.error(f"  Failed syncing {source}: {e}")

    mysql_conn.close()
    log.info(f"=== Sync Complete: {total} total rows across {len(SYNC_TABLES)} tables ===")

if __name__ == "__main__":
    main()
```

---

## Step 8: Set Up Cron (Every 6 Hours)

```bash
# Add to crontab
crontab -e
```

Add this line:
```
0 */6 * * * /Users/openclaw/zeus-agent/venv/bin/python3 /Users/openclaw/zeus-agent/scripts/ph_to_bigquery_sync.py >> /Users/openclaw/zeus-agent/logs/ph_sync.log 2>&1
```

This runs at midnight, 6 AM, noon, and 6 PM ET.

---

## Step 9: Verify End-to-End

1. **Tailscale**: `tailscale status` — both Mac Studio and PH PC online
2. **MySQL**: `mysql -h 192.168.20.160 -u athena_readonly -p -e "SELECT 1"` — connects
3. **Sync**: `python3 ~/zeus-agent/scripts/ph_to_bigquery_sync.py` — runs without error
4. **BigQuery**: Check `zero_dataset.ph_blank_inventory` has fresh data

---

## Safety Checklist

| Item | Status |
|------|--------|
| Tailscale only — no firewall ports opened | ✅ |
| Read-only MySQL user (SELECT only) | ✅ |
| Nothing installed on DB server (192.168.20.160) | ✅ |
| Tailscale on PH PC only (user's workstation) | ✅ |
| No writes to PH database | ✅ |
| IREN/DRECO unaffected | ✅ |
| Production workflow unchanged | ✅ |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Can't ping 192.168.20.160 | Check subnet route is approved in Tailscale admin |
| MySQL connection refused | Verify MySQL allows remote connections (bind-address in my.cnf) |
| MySQL access denied | Check athena_readonly user was created and FLUSH PRIVILEGES ran |
| Tailscale not connecting | Check both machines logged into same Tailnet account |
| Sync script fails | Check `PH_MYSQL_PASSWORD` env var is set |

---

## Dependencies to Install

```bash
# On Mac Studio
pip install mysql-connector-python google-cloud-bigquery

# MySQL client for testing
brew install mysql-client
```

---

*Once this is running, we'll have fresh PH inventory data in BigQuery every 6 hours — enabling inventory management, procurement forecasting, and the analytics pipeline from the Blueprint.*
