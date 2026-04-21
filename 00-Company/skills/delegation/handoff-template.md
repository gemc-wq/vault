# Agent Handoff Template

> Standard format for delegating tasks between agents. Copy this template and fill in all sections before handing off.

---

```markdown
# Agent Handoff: {Task Name}

## Context
- What is this task about?
- Why does it matter? (revenue impact, deadline, dependency)
- What has already been done?
- Link to prior work/conversation if any

## Objective
- Clear success criteria (measurable, specific)
- Example: "Generate PULSE leaderboard for US marketplace for week ending 2026-04-13 with top 50 designs by velocity"

## Relevant Skills
- List skill doc paths the receiving agent should load before starting
- Example:
  - `00-Company/skills/sales-analytics/SKILL.md`
  - `00-Company/skills/sales-analytics/sku-parsing-rules.md`
  - `00-Company/skills/sales-analytics/reporting-structure.md`

## Data Access
- Data sources needed (BigQuery tables, SP-API, vault files, external APIs)
- Credentials reference (e.g., "use OPENCLAW_GATEWAY_TOKEN from .env" -- never paste actual keys)
- BigQuery dataset/table names if applicable
- Any filters or date ranges to apply

## Constraints
- Budget limit (e.g., max $0.50 Claude spend, max 100K BigQuery bytes)
- Rate limits (e.g., SP-API throttling: 1 req/sec for GET_MERCHANT_LISTINGS)
- Safety guardrails:
  - Dry-run before committing changes (listing updates, price changes)
  - Human approval required for: spend >$100, listing deletions, price changes >10%
  - Never modify production data without explicit Cem approval

## Expected Output
- Format: report | code change | analysis | recommendation | action
- Delivery method: vault file path | Telegram message | email | BigQuery table
- Deadline: specific datetime or SLA (e.g., "within 2 hours")
- Example output format if applicable

## Escalation
- Escalate to Cem if: budget exceeded, ambiguous requirements, safety guardrail triggered
- Escalate to Athena if: infrastructure/API failure, data pipeline broken
- Out of scope decisions (list what the agent should NOT decide):
  - Pricing strategy changes
  - New marketplace launches
  - License negotiations
  - Ad budget >$500/week changes
```

---

## Usage Rules

1. **Every cross-agent delegation MUST use this template.** No free-form handoffs.
2. **Skill docs are mandatory.** If the task touches a domain, load the skill doc. Agents without domain context make bad decisions.
3. **Constraints are non-negotiable.** If a constraint is missing, ask the delegating agent to add one before proceeding.
4. **Escalation paths must be defined.** An agent without an escalation path will either stall or make unauthorized decisions.
5. **Measurable objectives only.** "Improve sales" is not an objective. "Identify top 10 designs with CVR >4% FBM and no FBA variant in US marketplace" is.
