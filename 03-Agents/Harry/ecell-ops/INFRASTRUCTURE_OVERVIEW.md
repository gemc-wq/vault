# Infrastructure Overview
*Version: 1.0 | Created: 2026-02-11*

---

## Compute Nodes

| Node | Type | Location | Status | Purpose |
|------|------|----------|--------|---------|
| AWS Server (Ubuntu) | Cloud VM | us-east-2 | ✅ Running | Harry's primary — gateway, N8N, agents |
| Cem's iMac | Desktop | Windermere, FL | 🔴 Node pairing broken | Dev node, browser automation |
| Windows PC (dedicated) | Desktop | Windermere, FL | 📅 Setting up | Dedicated Harry node |
| Cem's MacBook Pro | Laptop | Mobile | Available | 96GB — potential dev node / local LLM |

---

## Services

| Service | Host | Port | Status |
|---------|------|------|--------|
| Clawdbot Gateway | AWS | 18789 | ✅ Running |
| N8N | AWS | 5678 | ✅ Running |
| Supabase | Cloud (supabase.co) | — | ✅ Active |
| Google Cloud SQL | GCloud | TBD | 🔴 Need connection details |

---

## Databases

| Database | Type | Purpose | Status |
|----------|------|---------|--------|
| Supabase (nuvspkgplkdqochokhhi) | Postgres | Product catalog, future sales/inventory | ✅ Active |
| AWS Production DB | SQL Server | Live production orders | ✅ Running (don't touch) |
| Google Cloud SQL | MySQL clone | Daily sync of production — safe for testing | 🔴 Need access |
| BigQuery | Data warehouse | Reporting/analytics | Available |
| MySQL (legacy) | MySQL | Inventory management | Cem to share |

---

## AI Models & Costs

| Use Case | Model | Provider | Cost |
|----------|-------|----------|------|
| Harry (orchestration) | Claude Opus 4.6 | Anthropic API | API key |
| Harry (default) | Claude Sonnet 4.5 | Anthropic API | ~10x cheaper |
| Sub-agents | Gemini 3 Flash | Google | Pennies |
| N8N CS Bot | GPT-4o-mini | OpenRouter | ~$0.01/interaction |
| TTS (voice notes) | ElevenLabs Turbo v2.5 | ElevenLabs | Pay-per-use |
| Future: Packing verification | Gemini Flash Vision | Google Vertex AI | ~$0.001/scan |

---

## API Keys & Credentials

| Service | Location | Status |
|---------|----------|--------|
| Anthropic | Gateway config | ✅ |
| Google (Gemini) | Gateway config | ✅ |
| OpenRouter | Gateway config | ✅ |
| Moonshot (Kimi K2.5) | Gateway config | ✅ |
| ElevenLabs | Gateway config + skills | ✅ |
| Supabase | `~/.config/supabase/credentials` | ✅ |
| Notion | `~/.config/notion/api_key` | ✅ |
| Slack | Gateway config | ✅ |
| Brave Search | Gateway config | ✅ |
| Airtable | `~/.config/airtable/credentials` | ✅ |
| HeadCase CS Email | `~/.config/headcase-cs/email_credentials` | 🟡 Needs App Password |
| Google Cloud SQL | TBD | 🔴 Pending |
| eBay API | TBD | 🔴 Pending |
| Amazon SP-API | TBD | Available (from Feb 8) |

---

## Communication Channels

| Channel | Platform | Status |
|---------|----------|--------|
| Telegram | Primary — Cem ↔ Harry | ✅ Active |
| Slack | Team workspace | ✅ Active |

---

## Google Drive Sync

- **Folder:** Clawdbot Shared Folder
- **Local:** `/home/ubuntu/clawd/gdrive_shared/`
- **Sync:** `rclone sync "gdrive:/Clawdbot Shared Folder" /home/ubuntu/clawd/gdrive_shared`
- **Direction:** Bidirectional (manual sync)
