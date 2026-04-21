#!/usr/bin/env python3
"""Create Command Center tables and seed project data in Supabase."""
import json
import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY env vars")

sb = create_client(SUPABASE_URL, SUPABASE_KEY)

# Try to read from cc_projects to check if table exists
try:
    result = sb.table("cc_projects").select("id").limit(1).execute()
    print(f"cc_projects table exists, {len(result.data)} rows found")
    table_exists = True
except Exception as e:
    print(f"cc_projects table doesn't exist yet: {e}")
    table_exists = False
    print("\n⚠️  You need to run the SQL in setup_tables.sql via Supabase Dashboard SQL Editor:")
    print("   https://supabase.com/dashboard/project/auzjmawughepxbtpwuhe/sql/new")
    print("   Then re-run this script to seed data.")
    exit(1)

# Check if already seeded
result = sb.table("cc_projects").select("id").execute()
if len(result.data) > 0:
    print(f"Already have {len(result.data)} projects. Skipping seed.")
    exit(0)

# Seed projects
script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, "seed_projects.json")) as f:
    projects = json.load(f)

# Convert blockers field to proper JSONB
for p in projects:
    if "blockers" not in p:
        p["blockers"] = []
    if "brain_paths" not in p:
        p["brain_paths"] = []
    if "orbit_task_ids" not in p:
        p["orbit_task_ids"] = []
    if "revenue_opportunity" not in p:
        p["revenue_opportunity"] = None

result = sb.table("cc_projects").insert(projects).execute()
print(f"✅ Seeded {len(result.data)} projects into cc_projects")

# Seed key decisions
decisions = [
    {"decision": "3-store Shopify architecture (Microsite Backend / GoHeadCase / Target+)", "rationale": "Different stores need different product sets and channel rules", "decided_by": "cem"},
    {"decision": "Start with Anime microsite first", "rationale": "Smaller catalog, passionate buyers, validates tech stack before scaling", "decided_by": "ava"},
    {"decision": "Harry parked, Ava absorbs COO role", "rationale": "Harry unproductive on GPT-5.2, asking Cem to run every command", "decided_by": "cem"},
    {"decision": "Clean install on Mac Studio, no transfer from iMac", "rationale": "iMac at 95% disk, bloated. Fresh start avoids carrying tech debt", "decided_by": "cem"},
    {"decision": "EAN source = Walmart export (not BigCommerce 55GB)", "rationale": "BigCommerce CSV too large, Walmart already has clean GTINs", "decided_by": "ava"},
    {"decision": "OnBuy UK launch approved", "rationale": "Low risk, 2% lower fees than Amazon UK, CedCommerce Shopify integration available", "decided_by": "cem"},
    {"decision": "Weekly Momentum Brief over Dashboard tab for AI insights", "rationale": "Push to Cem vs. requiring him to check a dashboard", "decided_by": "cem"},
    {"decision": "Codex CLI (free GPT-5.3) for all coding, Sonnet as fallback", "rationale": "Zero cost for builds, saves API budget for strategy work", "decided_by": "ava"},
    {"decision": "MD files + pgvector for memory architecture", "rationale": "MD for human-readable/portable, pgvector for semantic search", "decided_by": "ava"},
    {"decision": "BigQuery over Supabase for ASIN lookup table", "rationale": "Dashboard already queries BigQuery, avoids second data source", "decided_by": "ava"},
]

# Get first project ID for foreign key (we'll leave project_id null for org-level decisions)
result = sb.table("cc_decisions").insert(decisions).execute()
print(f"✅ Seeded {len(result.data)} decisions into cc_decisions")

print("\n🎯 Command Center data ready. Now build the frontend.")
