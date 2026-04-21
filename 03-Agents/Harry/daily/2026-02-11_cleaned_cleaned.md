# 2026-02-11

**Decisions**
- **IT Management Transition:** Harry and Cem will assume IT responsibilities following the IT Manager's departure on Feb 14, 2026.
- **CS Bot Scope:** Limited to ecellglobal.com, goheadcase.com, and future microsites; Amazon/eBay automation is out of scope.
- **CS Co-Pilot Strategy:** Implementing a Chrome extension for Amazon/eBay (AI drafts replies $\rightarrow$ Human approval $\rightarrow$ Data sent to Supabase for reporting).
- **Agent Division of Labor:** 
    - **Harry:** Business automation, production, shipping, inventory, print pipeline, and IT handover.
    - **Ava:** Website builds, microsites, front-end design, and marketing content.
- **System Architecture:** 
    - **VPS (Harry's Brain):** Gateway, N8N, messaging, and orchestration.
    - **Windows PC (Harry's Hands):** Coding (Claude Code), builds, and browser automation.
    - **iMac (Ava's Machine):** Dedicated to web/design.
- **TTS Provider:** Switched from OpenAI TTS to ElevenLabs due to quota exhaustion.

**Deliverables**
- **Windows PC Node Setup:** Installed Node.js, Git, and `clawdbot`; created "Clawdbot Node" Scheduled Task.
- **IT Handover Documentation:** Created `gdrive_shared/08_Infrastructure/IT_HANDOVER_QUESTIONNAIRE.md`.
- **Google Drive Infrastructure:** Implemented new folder structure (`01_Customer_Service` through `08_Infrastructure`) with initial SOPs.

**Blockers**
- **Node Connectivity:** `clawdbot node run` failing due to incorrect gateway configuration.
- **Pending Items:** Cloud SQL credentials, CS email App Password, eBay login, Product-to-site mapping table, EPS workflow docs, and camera hole obstruction examples.

**Knowledge**
- **Windows PC Environment:** User `gemc`; includes MS SQL Server, NVIDIA GPU, FedEx shipping software, and UltraViewer.
- **CS Co-Pilot Workflow:** Extension reads page $\rightarrow$ AI drafts $\rightarrow$ Human sends $\rightarrow$ Data to Supabase for operational intelligence.
- **TTS Implementation:** Use ElevenLabs API via the direct `message` tool with `asVoice: true` and a file path to bypass the failing built-in `tts` tool.

**Carry-forwards**
- **Configuration Update:** Update `node.json` with gateway `3.1`.