# IT Infrastructure Notes — Drew Ramos Handover
*Source: Multiple emails, Jan-Feb 2026*

## NAS Storage (PH Office)
- **QNAP NAS** — used for Creative files and Production hi-res image storage
- 2 drives needed replacement (as of Feb 2026):
  - WD60EFRX (6TB WD Red NAS)
  - WD140EFFX (14TB WD Red NAS)
- Separate NAS units for PH office and PH production

## Zero System Architecture
- **Zero 1 (original):** ec2-34-196-137-61.compute-1.amazonaws.com — does NOT run Amazon SP-API
- **Zero 2 (updated):** ec2-3-81-155-102.compute-1.amazonaws.com — runs Amazon SP-API
- **Database:** RDS cluster at cluster.cluster-cvaofazjtifp.us-east-1.rds.amazonaws.com
- **Local mirror:** 192.168.20.160 (database), 192.168.20.57 (code)
- Zero has been developed for 10+ years — many undocumented tables/scripts

## Drew's Google Workspace
- Contains all historical documentation from staff
- Key reference: Bobby's documentation (email subject: "Iren Documentation")
- Drew's GDrive has accumulated handover docs from all departments over the years

## Key Contact for Zero
- **Patrick Gaña** (p.gana@ecellglobal.com) — knows all relevant scripts, tables, cron jobs, and day-to-day operations
- **Drew Ramos** — drewramos@outlook.com / +639175246909 (no longer with company, but offered post-departure support to Patrick)
