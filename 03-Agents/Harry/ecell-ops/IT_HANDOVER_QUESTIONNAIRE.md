# IT Handover Questionnaire
*For departing IT Manager | Deadline: Friday Feb 14, 2026*
*Please be as detailed as possible — this is our only reference going forward.*

---

## 1. SERVER & HOSTING

1.1. List ALL servers (cloud and physical) with:
- Provider (AWS, Google Cloud, other?)
- IP addresses / hostnames
- What runs on each server
- Login credentials (username + how to access — SSH keys, passwords, RDP)

1.2. Where is the **production database** hosted? (AWS RDS? EC2? Other?)
- Connection string / host / port
- Database type (MySQL, SQL Server, Postgres?)
- Admin username and password
- Any read-only users for reporting?

1.3. Where is the **Google Cloud SQL clone** hosted?
- Project ID
- Instance name
- Connection details
- How does the daily sync work? (script, Cloud SQL replication, manual?)

1.4. **CDN configuration:**
- Which CDN provider?
- What domains/assets does it serve?
- Admin login details
- Where is the configuration managed?

1.5. **Domain & DNS:**
- Who manages DNS for ecellglobal.com, goheadcase.com, and other domains?
- Registrar login details
- Any critical DNS records to be aware of?

---

## 2. DATABASES

2.1. List ALL databases with:
- Name and purpose
- Type (MySQL, SQL Server, Postgres, BigQuery)
- Host and connection details
- Size (approximate)
- Which applications read/write to each

2.2. **Production order database:**
- Full schema documentation (or where to find it)
- Key tables (orders, products, customers, inventory)
- Any stored procedures or views we rely on?

2.3. **Inventory database (MySQL):**
- Connection details
- Schema / table structure
- How is stock booked in and out?
- What triggers the zero-stock alerts?

2.4. **BigQuery:**
- Project and dataset names
- What data flows into BigQuery and how?
- Any scheduled queries or views?
- Who has access?

---

## 3. CRON JOBS & SCHEDULED TASKS

3.1. List EVERY cron job / scheduled task with:
- What it does (plain English)
- How often it runs
- Which server it runs on
- The actual command / script path
- What happens if it fails?
- Does anyone get alerted on failure?

3.2. Specifically:
- The **daily database sync** (AWS → Google Cloud) — how does it work?
- The **inventory zero-stock check** — what script, what frequency?
- The **order download** from marketplaces — automated or manual?
- Any **backup jobs** — what gets backed up, where, how often?

---

## 4. APIs & INTEGRATIONS

4.1. List ALL API integrations with:
- Platform (Amazon, eBay, BigCommerce, etc.)
- API type (REST, SOAP, other)
- API keys / credentials / tokens
- Where are the credentials stored?
- Any rate limits or quotas to be aware of?

4.2. **Amazon SP-API:**
- Seller ID / Account
- App registration details
- Refresh tokens
- Which endpoints are used (Orders, Feeds, Reports?)

4.3. **eBay API:**
- Account(s) connected
- OAuth tokens
- Which API version (Trading API, Fulfillment API, Browse API?)

4.4. **Shipping carrier APIs:**
- Royal Mail — API credentials + integration method
- USPS — API credentials
- FedEx — API credentials + account number
- Amazon Shipping — how is it triggered?
- Deutsche Post — API or manual?

4.5. **Veco:**
- Account details
- API access (if any)
- Current integration status per carrier/market

---

## 5. PICKING LIST SYSTEM

5.1. How does the picking list generation work end-to-end?
- What triggers it?
- What data source does it pull from?
- How are orders assigned to sites (UK/US/Philippines)?
- What format is the output (PDF, Excel, app screen)?

5.2. Where is the picking list application code hosted?
- Repository (GitHub, local, other?)
- Tech stack (language, framework)
- How to deploy updates

5.3. What does the internal app do beyond picking lists?
- Features list
- User accounts / access levels
- Where is it hosted?

---

## 6. PRINT FILE GENERATION

6.1. The script that generates print files from SKUs:
- Where is the code?
- What language is it written in?
- What are the inputs and outputs?
- How does it handle the camera hole placement?

6.2. Where are the design source files stored?
- File server / S3 / local?
- Folder structure
- Total size (approximate)
- How are new designs added to the system?

6.3. Template management:
- Where is the template-to-device mapping maintained?
- How are new device templates created?
- Who currently creates them?

---

## 7. SECURITY & ACCESS

7.1. List ALL service accounts, API keys, and shared passwords with:
- What they access
- Where they're stored (password manager, config file, etc.)
- Any that expire soon?

7.2. SSL certificates:
- Which domains have SSL?
- When do they expire?
- Auto-renewal or manual?

7.3. Firewall rules:
- Any custom firewall rules on servers?
- IP allowlists?
- VPN access required for anything?

---

## 8. KNOWN ISSUES & GOTCHAS

8.1. Is there anything that regularly breaks and needs manual fixing?

8.2. Any workarounds or hacks in place that we should know about?

8.3. Any upcoming renewals, expirations, or deadlines we should watch for?

8.4. If you could only tell us THREE things to watch out for, what would they be?

---

## 9. DOCUMENTATION

9.1. Is there any existing documentation? Where is it?
- Wiki, Notion, Google Docs, local files?

9.2. Any architecture diagrams?

9.3. Any runbooks for common tasks (restart a service, fix a failed job, etc.)?

---

*Please return this completed document to Cem by Thursday Feb 13 at the latest. For credentials, a secure method (password manager share or encrypted file) is preferred.*
