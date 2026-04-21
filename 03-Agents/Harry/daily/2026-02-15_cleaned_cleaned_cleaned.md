# 2026-02-15

**Decisions**
- **Agent Architecture**: Split roles between **Coding agents** (Codex, Claude Code) for development/APIs and **Clawdbot sub-agents** (Gemini Flash) for research and routine operations.
- **Ava's Model Stack**: 
    - Main: GPT-5.2
    - Coding: Codex (via OAuth)
    - Bulk/Light tasks: Gemini Flash
    - Website copy/Brand voice: Sonnet (**Cem decision** for superior personalized copy).
    - *Note