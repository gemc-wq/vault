# n8n Email Triage Workflow v1 (READ ONLY)

## Goal
Pull Gmail read-only → store in Supabase Email Memory → send digest to Telegram → generate drafts (no auto-send).

## Trigger
- Cron: every 15–60 minutes (start hourly)

## Nodes (high level)
1) **Gmail: Search/List messages**
   - scope: read-only
   - query: `newer_than:2d -category:promotions` (tune)
   - pull Inbox + optionally Sent

2) **Gmail: Get message + thread**
   - fetch full text/plain (and html if needed)

3) **Sanitize / Normalize**
   - strip tracking, signatures (basic heuristics)
   - detect prompt injection patterns

4) **LLM: Classify + Summarize + Draft**
   Output JSON:
   - triage_bucket: action | waiting | fyi | noise
   - urgency_score (0–100)
   - requires_reply boolean
   - 2–3 bullet summary
   - suggested_next_action
   - optional draft_reply

5) **Supabase: Upsert contacts + threads + emails**
   - emails keyed by message_id
   - threads keyed by thread_id

6) **Digest builder**
   - group by triage_bucket
   - include: sender, subject, 1-line summary, link to Gmail thread

7) **Telegram: Send digest**
   - daily summary + optional urgent pings

## Guardrails
- No gmail.modify
- No outbound email actions
- Store only text (skip attachments initially)

## Next upgrades
- Add embeddings (pgvector) after 3–7 days stable ingestion
- Add commitments extraction (who owes what + due dates)
- Add Orbit task creation from ACTION items
