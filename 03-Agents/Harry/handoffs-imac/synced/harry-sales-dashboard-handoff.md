# Handoff: Sales Dashboard → Cloud Run Deployment

## Working Version
- **Vercel (live):** https://sales-dashboard-iota-six.vercel.app
- **Git repo:** https://github.com/gemc-wq/sales-dashboard
- **Local path:** /Users/clawdbot/.openclaw/workspace/sales-dashboard/

## Stack
- Vite + React + Recharts + Tailwind
- Currently CSV-fed (Jan 2026 snapshot)
- Base path is `/` (was `/sales-dashboard/` which broke Cloud Run + GitHub Pages)

## What's Broken
- Cloud Run deploy fails: `storage.objects.get` permission denied on project `instant-contact-479316-i4`
  - Service account `175143437106-compute@developer.gserviceaccount.com` needs Storage Object Viewer role
- GitHub Pages at gemc-wq.github.io/sales-dashboard/ is blank (old build with wrong base path, needs re-push)

## Cloud Run Services (existing)
- `sales-dashboard` on `instant-contact-479316-i4` (us-east1 + europe-west1) — old build, blank page
- `ecell-dashboard` on `opsecellglobal` (us-east1) — ecell.app hub

## What Harry Needs To Do
1. Fix GCS permissions on `instant-contact-479316-i4` for Cloud Run deploys
2. `gcloud run deploy sales-dashboard --source=. --project=instant-contact-479316-i4 --region=us-east1 --allow-unauthenticated`
3. Phase 2: Connect to BigQuery `zero_dataset.orders` for live data (replace CSV imports)

## Vercel Credentials
- Token: in Google Drive → Brain/Credentials/API Keys for Ava (1).txt
- Team: ecells-projects-3c3b03d7
- Git author must be gemc99@me.com
