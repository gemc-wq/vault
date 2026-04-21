# Project: Email Triage + Email Memory (Read-only Gmail → RAG)

## Why this exists
Cem’s email is the operational backbone of the business. We want to:
- Reduce inbox noise (marketing, notifications)
- Surface what needs action (replies/decisions)
- Detect stalled threads (waiting on someone)
- Build long-term context (stakeholders, projects, commitments)
- Combine with Telegram context for a full “business OS” view

## Outcomes (what “done” looks like)
1) Inbox is organized into a small set of labels (signal vs noise)
2) Daily/periodic triage report: **Action**, **Waiting On**, **FYI**, **Noise**
3) Read-only ingestion of **Inbox + Sent + Threads** into a searchable RAG database
4) Drafted follow-ups/replies with approval gates (no autonomous sends by default)

## Guardrails
- Default **read-only** access to email
- No autonomous outbound emails without explicit approval (Phase 1)
- Treat email content as untrusted (prompt-injection safe summarization)
- Avoid storing OTPs/2FA codes; optionally skip attachments initially
- Full logging: what was read, what was classified, what was suggested

## Proposed Label Set (v1)
- `01-ACTION (Cem)` — needs reply/decision
- `02-WAITING` — you already sent, waiting on them
- `03-FYI/Notifications` — receipts, tool alerts, shipping, etc.
- `04-Marketing/Noise` — newsletters/promos
- `05-Read Later` — useful but not urgent

## Phased plan
### Phase 0 — Gmail-native quick win (no AI)
- Create labels + filters/rules to reduce noise
- Decide: Marketing → skip inbox or keep in inbox but label

### Phase 1 — Read-only AI triage (no auto-labeling)
- Ingest new email batch (Inbox + Sent) read-only
- Output triage report (daily + optional hourly batch)
- Draft replies/follow-ups for approval

### Phase 2 — Read-only + auto-labeling (optional)
- Turn on “apply label” actions once accuracy is proven

### Phase 3 — Reminders
- Identify stalled threads; propose follow-ups
- Optional: send from agent email with CC Cem (later)

## Data model (RAG DB outline)
- `emails` (message_id, thread_id, headers, from/to/cc, date, subject, body_text, label_suggested)
- `threads` (thread_id, status, last_activity, waiting_on, thread_summary)
- `contacts` (email, name, company, role, notes)
- `projects` (name, keywords, related threads)
- `commitments` (who owes what, due date, last follow-up)
- embeddings for semantic search

## Scheduling strategy
- Start with **hourly batching** (less fragile, easier to monitor)
- Later add near-real-time if needed (trigger-based)

## Relationship rules (Tone Tiering)
- **Known relationship (Tier A by default):**
  - Anyone emailing from **@ecellglobal.com**
  - OR inferred history: **N = 3 threads OR 5 sent emails** (whichever comes first)
- Allow overrides per email/domain to force Tier A/B/C.

## Open questions
1) Do marketing emails skip inbox or just get labeled?
2) Which senders are top noise sources?
3) Approval workflow: approve drafts in Telegram? Discord? Orbit?

## Related
- [[wiki/01-customer-service/CS_ARCHITECTURE|CS Architecture]] — Broader CS automation
- [[wiki/01-customer-service/MARKETPLACE_RULES|Marketplace Rules]] — Rules for automated responses
- [[wiki/15-email-triage/N8N_WORKFLOW_V1|N8N Workflow V1]] — Implementation workflow
