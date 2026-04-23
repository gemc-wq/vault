# Active Blockers
*Auto-compiled: 2026-04-21 — Vault Compiler (claude-sonnet-4-6)*

---

## 🔴 P0 — Critical (Blocking Vault Automation)

| Blocker | Project | Owner | Days Blocked | What's Needed |
|---------|---------|-------|-------------|---------------|
| **Secret incident: 144 gitleaks findings** | Vault / All | Cem | 1 | Rotate credentials (GCP, AWS, Supabase, Slack, Shopify, BigCommerce, Walmart, Anthropic), delete raw key files, scrub docs, rewrite git history |
| **Compile Routine setup paused** | Vault automation | Cem | 1 | Complete secret remediation (see VAULT_EXECUTE_NOW_V2.md) before re-enabling automation |
| **OpenClaw: gemma4:26b sandbox-off + prism** | Infrastructure | Cem | 2 | Disable web tools (`prism`) for local Gemma 4 model OR enable sandbox — security critical |

---

## 🔴 P1 — High Priority

| Blocker | Project | Owner | Days Blocked | What's Needed |
|---------|---------|-------|-------------|---------------|
| **PH Database Access (Tailscale)** | Operations | Cem + Athena | 11+ | Setup guide ready — Cem to execute steps 1–3 |
| **SP-API Product Listing role not granted** | shipping-template-dashboard | Cem + Patrick | 7 | Add Product Listing role to SP-API app (Seller Central action) — blocks all 9,778 template fix executions |
| **Xero OAuth setup (UK+US)** | Finance-ops | Cem | 14+ | Required before invoice posting works in Phase 1 |
| **DB migrations not run** | Finance/Inventory | Harry | 17+ | Harry created migrations but they have not been executed |
| **Harry inactive 49+ days** | Finance Agent | Cem | 49 | Harry last log was 2026-03-03. Agent may be down or model upgrade (GPT-5.4) not yet deployed |

---

## 🟡 P2 — Waiting / Monitoring

| Blocker | Project | Owner | Days Blocked | What's Needed |
|---------|---------|-------|-------------|---------------|
| GoHeadCase email campaign | Marketing | Ava | — | Creative assets needed before launch (11K subs, zero campaigns) |
| Kaufland DE setup | Sales | Cem | 14+ | NL tax done; EU OSS registration still pending |
| EU 3PL partner identification | Operations | Cem | 14+ | Enabled by NL tax registration; no action yet |
| Hermes Gateway not running | Infrastructure | Cem/Athena | — | LaunchAgent `ai.hermes.gateway` needs restart |
| Walmart Tier 2 titles | Sales | Ava | — | Sample ready for Cem approval |

---

*Source: 04-Shared/active/VAULT_SECRET_INCIDENT_RESPONSE_2026-04-20.md, 03-Agents/Ava/memory/2026-04-19.md, TASK_SHEET.md*
