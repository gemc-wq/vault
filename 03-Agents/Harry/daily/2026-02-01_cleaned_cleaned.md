# 2026-02-01 — Console Skin Automation POC

## Decisions
- **Clawdbot Configuration**: 
    - `compaction.memoryFlush.enabled` set to `true`.
    - `memorySearch.experimental.sessionMemory` set to `true`.
    - `memorySearch.sources` updated to `["memory", "sessions"]`.
- **Workflow Approval**: Cem approved the replication workflow analysis and the creation of the improved process POC.

## Deliverables
- **Improved Workflow Documentation**: `/home/ubuntu/clawd/projects/design-automation/console-skins/POC_IMPROVED_WORKFLOW.md`
- **Automation Configuration**: `/home/ubuntu/clawd/projects/design-automation/console-skins/config.json`

## Blockers
- **iMac Node Connectivity**: `cat` and `cp` commands are blocked due to missing `exec-approve` CLI.
    - **Resolution**: Manually create `~/.clawdbot/exec-approvals.json` on the iMac or use Google Drive for file transfers.

## Knowledge
- **Console Skin Replication Workflow**: Creative submits PSD + Google Sheet $\rightarrow$ Replicator generates folder structure $\rightarrow$ Layouts created in Smart Objects (no rasterization) $\rightarrow$ Naming: `[Index]_[Product_Name]` $\rightarrow$ JSX script executes Photoshop actions $\rightarrow$ Automated export and QC.
- **Product & Quality Identifiers**:
    - **Products**: `PS5SCS` (Standard), `PS5SDCS` (Slim Digital), `DS5EGCT` (Edge), `ASROGA` (ROG Ally), `STMDECK` (Steam Deck).
    - **Quality Tiers**: