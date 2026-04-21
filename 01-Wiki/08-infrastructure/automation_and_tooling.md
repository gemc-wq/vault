# automation and tooling
*Auto-created by vault compiler on 2026-04-13*

- **Sub-agents:** Use `sessions_spawn` for coding (Codex/Claude Code) and analysis (Bolt/Atlas/Hermes).
- **Automation:** Use `cron` for recurring/background tasks.
- **Model Constraints:** Always use free models (Gemini Flash, Codex, Kimi) for background/cron work; avoid using Anthropic models for background tasks.
- **Tool Execution Order:** `read` $\rightarrow$ `web_search` $\rightarrow$ `web_fetch` $\rightarrow$ `exec`.
