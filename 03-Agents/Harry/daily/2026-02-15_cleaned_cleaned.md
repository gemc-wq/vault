# 2026-02-15

**Decisions**
- **Agent Architecture**: Split roles between **Coding agents** (Codex, Claude Code) for development/APIs and **Clawdbot sub-agents** (Gemini Flash) for research and routine operations.
- **Ava's Model Stack**: 
    - Main: GPT-5.2
    - Coding: Codex (via OAuth)
    - Bulk/Light tasks: Gemini Flash
    - Website copy/Brand voice: Sonnet (**Cem decision** for superior personalized copy).
    - *Note: K2.5 removed from stack.*
- **Communication Structure**: 
    - **Telegram**: Cem $\leftrightarrow$ Harry (Strategy/Decisions).
    - **Discord**: Harry $\leftrightarrow$ Ava (Coordination) with Cem visibility.
    - **Mission Control**: Single source of truth for task status.
    - **Briefings**: Daily audio briefings for Cem at 6:30 AM EST.

**Deliverables**
- **Mission Control v2 Deployed**: [https://mission-control-v2-three.vercel.app](https://mission-control-v2-three.vercel.app) (Stack: Next.js 15, Tailwind, dnd-kit, React Flow, Supabase).
- **Operational Plan Q1 2026**: Created at `projects/OPERATIONAL_PLAN_Q1_2026.md`.
- **Tailscale Mesh**: Established on `tail461b28.ts.net`.
    - Harry (hp-cem): `100.120.86.40`
    - Ava (cems-imac): `100.91.149.92`
    - Ava's gateway: `https://cems-imac.tail461b28.ts.net` (proxying 443 $\to$ localhost:187189).
- **Project Infrastructure**: Created directories: `f