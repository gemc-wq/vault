# NemoClaw R&D Project

**Created:** 2026-03-23
**Owner:** Ava (with Cem oversight)
**Status:** Research Phase

## Purpose
Evaluate NemoClaw (NVIDIA's enterprise AI agent security wrapper) as an R&D project to understand:
1. How to implement AI agents securely for a security-conscious business (Ecell Global)
2. What the enterprise AI agent market looks like for potential SaaS opportunities
3. How our current OpenClaw setup compares and what hardening we need

## Background
- **OpenClaw** = what we run today. Open-source, fast, community-driven. But has known security gaps (ClawHavoc supply chain attack, CVE-2026-25253, 900+ malicious skills on ClawHub)
- **NemoClaw** = NVIDIA's enterprise wrapper around OpenClaw. Launched at GTC 2026 (Mar 16). Adds OpenShell sandboxing, policy manifests, audit ledger, privacy router
- Key difference: OpenClaw security is application-layer; NemoClaw is kernel-level (out-of-process enforcement)

## Key NemoClaw Features to Evaluate
- **OpenShell Runtime** — sandboxed execution, YAML-based policy files
- **Privacy Router** — strips PII before sending to cloud models
- **Audit Ledger** — immutable logs, SIEM export (Splunk, Sentinel)
- **Identity Integration** — Okta, Microsoft Entra ID, Ping Identity
- **Compliance** — GDPR, HIPAA, SOC 2, EU AI Act aligned

## Research Questions
1. Can we run NemoClaw alongside OpenClaw on Mac Studio? (Requirements: Ubuntu 22.04+, 8GB+ RAM)
2. What security hardening should we apply to our current OpenClaw setup NOW?
3. Is there a SaaS opportunity in "AI agent security for SMBs"? (NemoClaw targets enterprise; gap exists for mid-market)
4. How does the OpenShell policy manifest work? Can we replicate key patterns?
5. What's the latency overhead? (Reports say 12-18% — acceptable for our use case?)

## SaaS Angle
The research shows a clear gap:
- OpenClaw = great for individuals/startups, terrible security
- NemoClaw = great for enterprise, overkill for SMBs
- **Nobody is serving the mid-market** — businesses like us that need security but can't justify DGX infrastructure
- Potential product: "AI Agent Security for SMBs" — lightweight governance layer, skill auditing, basic policy enforcement

## Current OpenClaw Security Status (Our Setup)
- Running on Mac Studio + iMac (Tailscale network)
- API keys stored in TOOLS.md and .env files (plaintext risk)
- Community skills installed (unaudited)
- No SIEM integration
- No formal audit trail beyond session logs

## Deployment Options (Researched Mar 23)

### Option A: NVIDIA Cloud (Free Tier via Brev)
- build.nvidia.com → "Try for free" → Launchable dashboard → pre-configured NemoClaw
- No local setup needed. Good for evaluation
- GPU: A100 default (can change)
- Requires: NVIDIA developer account + API key (nvapi-*)

### Option B: AWS Free Tier (Ubuntu)
- EC2 t2.micro = 1 vCPU, 1GB RAM → NOT ENOUGH (need 8GB min, 16GB recommended)
- EC2 t3.large (2 vCPU, 8GB) = ~$60/mo → viable for testing
- Better: DigitalOcean 1-Click Droplet (NemoClaw Marketplace) — $336/mo for full setup, but easy
- Best budget option: DigitalOcean 8GB droplet ~$48/mo + manual install

### Option C: One-Line Ubuntu Install
```bash
curl -fsSL https://nvidia.com/nemoclaw.sh | bash
```
- Requires: Ubuntu 22.04+, Docker, Node.js 20+, OpenShell CLI
- Steps: Docker → Node.js → OpenShell CLI (via gh) → NemoClaw install → onboard wizard
- Time: 10-15 minutes on fast connection
- Sandbox image: ~2.4GB compressed

### Option D: Your Video Guide (Cloud Setup <15 min)
- Video: https://youtu.be/dEL9tKwvejo — "Nvidia NemoClaw Cloud Setup in Under 15 Minutes"
- Likely covers Brev/NVIDIA cloud path with one-click setup

## Security Wrapper Idea — "Why Can't We Add One?" (Cem's Question)

**Answer: We absolutely can. And someone already started.**

### Existing Open-Source Security Layers for OpenClaw:
1. **OpenClaw PRISM** (arXiv:2603.11853, Mar 12 2026)
   - Zero-fork runtime security layer (no need to fork OpenClaw!)
   - In-process plugin + optional sidecar services
   - 10 lifecycle hooks: message ingress, prompt construction, tool execution, tool-result persistence, outbound messaging, sub-agent spawning, gateway startup
   - Hybrid heuristic + LLM scanning pipeline
   - Session-scoped risk accumulation with TTL-based decay
   - Hot-reloadable policy management
   - **This is basically "NemoClaw Lite" as an OpenClaw plugin**

2. **SlowMist Security Practice Guide** (github.com/slowmist/openclaw-security-practice-guide)
   - 3-Tier Defense Matrix: Pre-action → In-action → Post-action
   - Behavior blacklists, skill audit protocols, nightly automated audits
   - Can be deployed BY the agent itself (just send the guide to OpenClaw)
   - v2.8 Beta available with production-verified improvements
   - Includes red-teaming guide for testing

3. **Academic Security Analysis** (arXiv:2603.10387, Mar 11 2026)
   - Tested 47 adversarial scenarios across 6 attack categories (MITRE ATLAS + ATT&CK)
   - OpenClaw native defense rate: only 17%
   - With Human-in-the-Loop (HITL) layer: improved to 19-92%
   - Validates that a security wrapper dramatically improves safety

### Our SaaS Opportunity — "ShieldClaw" Concept
- **PRISM is academic, NemoClaw is enterprise, SlowMist is a guide**
- **Nobody has packaged this as a turnkey product for mid-market businesses**
- We could build: PRISM-based plugin + SlowMist best practices + simple web dashboard
- Target: Companies running OpenClaw who need security but not NVIDIA infrastructure
- Pricing: $29-99/mo per instance (vs NemoClaw's enterprise pricing)

## Most Searched AI Assistant Use Cases (X/Twitter, Mar 2026)

Based on research — what people actually WANT from AI assistants:

### Top Demand Signals (Anthropic Survey, Mar 18):
1. **Time-saving automation** — 1/3 of people want AI to save time in daily routines
2. **Financial security** — budgeting, investment optimization
3. **Cognitive load reduction** — reduce stress/decision fatigue
4. **Better work performance** — 1/4 want AI to help them do better, more fulfilling work

### Top Use Cases Driving Engagement on X:
1. **"AI that DOES things, not just talks"** — #1 trend (scheduling, emails, purchases)
2. **Multi-agent orchestration** — "autonomous agents running my business 24/7" (massive engagement)
3. **AI home automation** — controlling everything via WhatsApp/chat (Sonos, HVAC, cameras)
4. **AI for ecommerce** — product discovery, pricing, inventory management
5. **Personal AI agents** — email triage, calendar management, follow-ups
6. **AI security/governance** — growing fast as a concern AND a business opportunity

### Content Strategy Implication:
Our X account should focus on #2 (multi-agent orchestration) and #4 (AI for ecommerce) — because that's literally what we do. Nobody else is posting real operational data from a multi-agent AI stack managing 1.8M SKUs.

## Next Steps
- [ ] Audit our current OpenClaw skill installations
- [ ] Try NVIDIA free tier (Brev) for NemoClaw evaluation
- [ ] Deploy SlowMist Security Practice Guide on our OpenClaw instances (Mac Studio + iMac)
- [ ] Evaluate OpenClaw PRISM as a zero-fork security layer
- [ ] Research mid-market AI security competitors
- [ ] Draft "ShieldClaw" SaaS concept doc
- [ ] Assess SaaS viability for "AI Agent Governance Lite"
- [ ] Set up X account and content engine (separate project)

## References
- NemoClaw vs OpenClaw comparison: shareuhack.com, glbgpt.com, secondtalent.com, lumetric.ai
- NemoClaw install guide: secondtalent.com/resources/how-to-install-nvidia-nemoclaw
- DigitalOcean 1-Click: digitalocean.com/community/tutorials/how-to-set-up-nemoclaw
- OpenClaw PRISM paper: arxiv.org/abs/2603.11853
- SlowMist security guide: github.com/slowmist/openclaw-security-practice-guide
- OpenClaw security analysis: arxiv.org/abs/2603.10387
- OpenClaw 2026.2.23 hardening: penligent.ai
- Agentic AI market: $10.86B (Mar 2026), projected $251B by 2034, 44.6% CAGR
- Agentic commerce protocol launched Mar 17, 2026 — 1000 retail brands adopted week one
