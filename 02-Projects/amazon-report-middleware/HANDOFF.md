# Technical Handoff Documentation
## Amazon Report Middleware
**Everything you need to operate, maintain, and extend this system**

| Field | Value |
|-------|-------|
| Last Updated | April 14, 2026 |
| Owner | Cem (gemc@ecellglobal.com) |
| Environment | Production |
| GCP Project | `instant-contact-479316-i4` |
| Region | `europe-west1` |
| Cloud Run Service | `amazon-report-middleware` |
| Service Account | `175143437106-compute@developer.gserviceaccount.com` |
| Source Code | `/Users/cem/Desktop/Repos/amazon-report-middleware/` |
| Git Status | Initialized, first commit `7e25c94` on `main` |

---

## 1. Quick Start Guide

### 1.1 Verify System Health

```bash
curl https://amazon-report-middleware-175143437106.europe-west1.run.app/health
```
Expected: `{"status": "ok", "timestamp": "..."}`

### 1.2 Trigger a Report Manually

```bash
gcloud scheduler jobs run report-active-listings-uk \
  --project=instant-contact-479316-i4 \
  --location=europe-west1
```

### 1.3 Check Job Status

```bash
gcloud scheduler jobs describe report-active-listings-uk \
  --project=instant-contact-479316-i4 \
  --location=europe-west1
```

Status codes: `0` = OK, `9` = FAILED_PRECONDITION, `13` = INTERNAL, `14` = UNAVAILABLE

### 1.4 View Logs

```bash
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="amazon-report-middleware"' \
  --project=instant-contact-479316-i4 \
  --limit=20 --format="value(textPayload)" --freshness=1h
```

### 1.5 Access Swagger UI

Navigate to the service URL + `/docs` with a valid identity token. The Swagger UI lets you test all endpoints interactively.

---

## 2. Codebase Structure

Source code: `/Users/cem/Desktop/Repos/amazon-report-middleware/`

| File | Lines | Purpose |
|------|-------|---------|
| `main.py` | ~510 | FastAPI app: routes, models, auth dependency, BQ endpoints |
| `report_engine.py` | ~350 | SP-API and Ads API: create, check, download, `request_and_wait` |
| `config.py` | ~156 | Settings, Secret Manager loader, marketplace config |
| `auth.py` | ~50 | API key verification middleware |
| `bigquery_loader.py` | ~120 | BQ table creation, data loading, query helpers |
| `Dockerfile` | ~20 | Python 3.12 slim, pip install, uvicorn entrypoint |
| `requirements.txt` | ~15 | python-amazon-sp-api, fastapi, uvicorn, google-cloud-* |
| `deploy.sh` | ~30 | Deployment helper script |
| `.gitignore` | 6 | Excludes .env, __pycache__, logs, .DS_Store |

### Key Dependencies

```
python-amazon-sp-api
fastapi
uvicorn[standard]
slowapi
google-cloud-secret-manager
google-cloud-bigquery
google-cloud-logging
pydantic
```

---

## 3. Deployment Procedures

### 3.1 Standard Deploy

```bash
cd /Users/cem/Desktop/Repos/amazon-report-middleware

gcloud run deploy amazon-report-middleware \
  --project=instant-contact-479316-i4 \
  --region=europe-west1 \
  --source=. \
  --no-allow-unauthenticated \
  --memory=512Mi \
  --timeout=600 \
  --min-instances=0 \
  --max-instances=3 \
  --quiet
```

This builds a container from source, pushes to Artifact Registry, and deploys. Takes 2-4 minutes.

> **Important:** Code was deployed directly to Cloud Run via `--source=.` (source deploy). There is no CI/CD pipeline. Git was initialized on April 14, 2026 with the first commit. Consider setting up GitHub + Cloud Build for future deployments.

### 3.2 Rollback

```bash
# List recent revisions
gcloud run revisions list \
  --service=amazon-report-middleware \
  --project=instant-contact-479316-i4 \
  --region=europe-west1

# Route 100% traffic to a previous revision
gcloud run services update-traffic amazon-report-middleware \
  --to-revisions=amazon-report-middleware-00019-xkl=100 \
  --project=instant-contact-479316-i4 \
  --region=europe-west1
```

### 3.3 Key Deployment Settings

| Setting | Value | Notes |
|---------|-------|-------|
| Memory | 512Mi | Sufficient for report processing |
| Timeout | 600s | Max Cloud Run allows; reports poll up to 540s internally |
| Min Instances | 0 | Scale to zero when idle (cost saving) |
| Max Instances | 3 | Limits concurrent report processing |
| Auth | `--no-allow-unauthenticated` | GCP org policy blocks `allUsers` |

---

## 4. Credential Management

### 4.1 Secret Manager Secrets

All secrets in project `instant-contact-479316-i4`:

| Secret Name | Description | Status |
|-------------|-------------|--------|
| `EU_LWA_APP_ID` | EU Login with Amazon app ID | Active |
| `EU_LWA_CLIENT_SECRET` | EU LWA client secret | Active |
| `EU_REFRESH_TOKEN` | EU SP-API refresh token | Active |
| `EU_AWS_ACCESS_KEY` | EU STS access key | Active |
| `EU_AWS_SECRET_KEY` | EU STS secret key | Active |
| `US_LWA_APP_ID` | US Login with Amazon app ID | Active |
| `US_LWA_CLIENT_SECRET` | US LWA client secret | Active |
| `US_REFRESH_TOKEN` | US SP-API refresh token | Active |
| `US_AWS_ACCESS_KEY` | US STS access key | Active |
| `US_AWS_SECRET_KEY` | US STS secret key | Active |
| `ADS_CLIENT_ID` | Ads API client ID | **EMPTY** |
| `ADS_CLIENT_SECRET` | Ads API client secret | **EMPTY** |
| `ADS_EU_PROFILE_ID` | Ads EU profile ID | **EMPTY** |
| `ADS_EU_REFRESH_TOKEN` | Ads EU refresh token | **EMPTY** |
| `ADS_US_PROFILE_ID` | Ads US profile ID | **EMPTY** |
| `ADS_US_REFRESH_TOKEN` | Ads US refresh token | **EMPTY** |
| `API_KEYS` | JSON array of API key objects | Active |

### 4.2 Rotating Credentials

```bash
# Update a secret
echo -n "NEW_VALUE" | gcloud secrets versions add SECRET_NAME \
  --data-file=- --project=instant-contact-479316-i4

# Force fresh instance (secrets loaded on cold start)
gcloud run services update amazon-report-middleware \
  --region=europe-west1 \
  --project=instant-contact-479316-i4 \
  --update-env-vars=FORCE_RESTART=$(date +%s)
```

---

## 5. Monitoring & Troubleshooting

### 5.1 Common Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| HTTP 401 on cron trigger | Service account missing `run.invoker` role | `gcloud run services add-iam-policy-binding ... --member=serviceAccount:SA --role=roles/run.invoker` |
| HTTP 500 immediately | Missing `report_options` or credential error | Check logs for full traceback (`exc_info=True` enabled) |
| HTTP 408 timeout | Amazon report still processing after 540s | Normal for large catalogs; report will be ready on next poll |
| Scheduler status code 13 | INTERNAL error from Cloud Run | Check Cloud Run logs for details |
| IN_QUEUE for 5+ minutes | Amazon queuing during peak hours | Expected; cron at 6 AM UTC avoids peak |
| Deploy version conflict | Rapid successive deploys | Wait 30 seconds and retry |

### 5.2 Useful Log Queries

**Errors only:**
```bash
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="amazon-report-middleware" AND severity>=ERROR' \
  --project=instant-contact-479316-i4 --limit=10 --freshness=24h
```

**Successful deliveries:**
```bash
gcloud logging read \
  'resource.type="cloud_run_revision" AND textPayload:Delivered' \
  --project=instant-contact-479316-i4 --limit=10 --freshness=7d
```

**Specific report tracking:**
```bash
gcloud logging read \
  'resource.type="cloud_run_revision" AND textPayload:REPORT_ID_HERE' \
  --project=instant-contact-479316-i4 --limit=20 --freshness=1h
```

---

## 6. IAM & Permissions

| Principal | Role | Scope |
|-----------|------|-------|
| `175143437106-compute@developer.gserviceaccount.com` | `roles/run.invoker` | Cloud Run service |
| `gemc@ecellglobal.com` | `roles/run.invoker` | Cloud Run service |
| `175143437106-compute@developer.gserviceaccount.com` | `roles/secretmanager.secretAccessor` | Project-level |
| `175143437106-compute@developer.gserviceaccount.com` | `roles/bigquery.dataEditor` | Project-level |

---

## 7. How to Add New Reports

### 7.1 Adding an SP-API Report to Cron

1. Verify the report type works by calling `/api/v1/reports/request-and-wait` manually
2. Create a Cloud Scheduler job:

```bash
gcloud scheduler jobs create http report-{name}-{marketplace} \
  --project=instant-contact-479316-i4 \
  --location=europe-west1 \
  --schedule="0 6 * * 1" \
  --uri="https://amazon-report-middleware-175143437106.europe-west1.run.app/api/v1/reports/request-and-wait" \
  --http-method=POST \
  --headers="Content-Type=application/json,X-API-Key=sk_live_cron_2026" \
  --message-body='{"marketplace":"UK","report_type":"REPORT_TYPE","is_ads":false}' \
  --oidc-service-account-email=175143437106-compute@developer.gserviceaccount.com \
  --oidc-token-audience="https://amazon-report-middleware-175143437106.europe-west1.run.app" \
  --attempt-deadline=600s \
  --time-zone=UTC --quiet
```

### 7.2 Adding Brand Analytics Reports

Brand Analytics reports require `reportOptions`. Include them in the message-body:

```json
{
  "marketplace": "UK",
  "report_type": "GET_SALES_AND_TRAFFIC_REPORT",
  "is_ads": false,
  "report_options": {
    "asinGranularity": "CHILD",
    "dateGranularity": "DAY"
  }
}
```

### 7.3 Enabling Ads API Reports

1. Populate `ADS_*` secrets in Secret Manager with real credentials from the Amazon Ads console
2. Set `is_ads: true` in the request body
3. The system uses Ads API v3 endpoints with the configured profile IDs

---

## 8. API Key Reference

| Key | Name | Use Case |
|-----|------|----------|
| `sk_live_ecell_2026` | ecell | Production: Swagger UI, manual testing, dashboards |
| `sk_live_claude_2026` | claude | AI agent integration (Claude, GPTs, etc.) |
| `sk_live_cron_2026` | cron | Cloud Scheduler automation |

To add a new API key, update the `API_KEYS` secret in Secret Manager with the new key object appended to the JSON array.

---

## 9. Complete Cron Job List

All 28 jobs, schedule: `0 6 * * 1` (Monday 6 AM UTC):

### Sales & Traffic 14d (6 jobs)

| Job Name | Marketplace | Report Options |
|----------|------------|----------------|
| `report-sales-traffic-14d-uk` | UK | `asinGranularity=CHILD, dateGranularity=DAY` |
| `report-sales-traffic-14d-de` | DE | `asinGranularity=CHILD, dateGranularity=DAY` |
| `report-sales-traffic-14d-fr` | FR | `asinGranularity=CHILD, dateGranularity=DAY` |
| `report-sales-traffic-14d-it` | IT | `asinGranularity=CHILD, dateGranularity=DAY` |
| `report-sales-traffic-14d-es` | ES | `asinGranularity=CHILD, dateGranularity=DAY` |
| `report-sales-traffic-14d-us` | US | `asinGranularity=CHILD, dateGranularity=DAY` |

### Sales & Traffic 30d (6 jobs)

| Job Name | Marketplace | Report Options |
|----------|------------|----------------|
| `report-sales-traffic-30d-uk` | UK | `asinGranularity=CHILD, dateGranularity=DAY` |
| `report-sales-traffic-30d-de` | DE | `asinGranularity=CHILD, dateGranularity=DAY` |
| `report-sales-traffic-30d-fr` | FR | `asinGranularity=CHILD, dateGranularity=DAY` |
| `report-sales-traffic-30d-it` | IT | `asinGranularity=CHILD, dateGranularity=DAY` |
| `report-sales-traffic-30d-es` | ES | `asinGranularity=CHILD, dateGranularity=DAY` |
| `report-sales-traffic-30d-us` | US | `asinGranularity=CHILD, dateGranularity=DAY` |

### Active Listings (6 jobs)

| Job Name | Marketplace | Report Type |
|----------|------------|-------------|
| `report-active-listings-uk` | UK | `GET_MERCHANT_LISTINGS_ALL_DATA` |
| `report-active-listings-de` | DE | `GET_MERCHANT_LISTINGS_ALL_DATA` |
| `report-active-listings-fr` | FR | `GET_MERCHANT_LISTINGS_ALL_DATA` |
| `report-active-listings-it` | IT | `GET_MERCHANT_LISTINGS_ALL_DATA` |
| `report-active-listings-es` | ES | `GET_MERCHANT_LISTINGS_ALL_DATA` |
| `report-active-listings-us` | US | `GET_MERCHANT_LISTINGS_ALL_DATA` |

### FBA Reports - US Only (4 jobs)

| Job Name | Report Type |
|----------|-------------|
| `report-fba-inventory-us` | `GET_AFN_INVENTORY_DATA` |
| `report-fba-fees-us` | `GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA` |
| `report-fba-reimbursements-us` | `GET_FBA_REIMBURSEMENTS_DATA` |
| `report-fba-restock-us` | `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` |

### Settlements (6 jobs)

| Job Name | Marketplace | Report Type |
|----------|------------|-------------|
| `report-settlements-uk` | UK | `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` |
| `report-settlements-de` | DE | `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` |
| `report-settlements-fr` | FR | `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` |
| `report-settlements-it` | IT | `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` |
| `report-settlements-es` | ES | `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` |
| `report-settlements-us` | US | `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` |

---

## 10. Version Control Status

> **Important:** This project was initially deployed directly to Cloud Run without git. A git repository was initialized on April 14, 2026.

```
Location: /Users/cem/Desktop/Repos/amazon-report-middleware/
Branch:   main
Commit:   7e25c94 - Initial commit: Amazon Report Middleware v1.0
Remote:   None configured
```

**Recommended next steps for version control:**
1. Create a GitHub/GitLab repository
2. Add remote: `git remote add origin git@github.com:ecellglobal/amazon-report-middleware.git`
3. Push: `git push -u origin main`
4. Consider setting up Cloud Build triggers for CI/CD

---

## 11. Contacts & Escalation

| Role | Name | Contact |
|------|------|---------|
| System Owner | Cem | gemc@ecellglobal.com |
| GCP Project | instant-contact-479316-i4 | Google Cloud Console |
| Amazon SP-API Support | Seller Central | https://sellercentral.amazon.com |
| Amazon Ads API | Ads Console | https://advertising.amazon.com |
