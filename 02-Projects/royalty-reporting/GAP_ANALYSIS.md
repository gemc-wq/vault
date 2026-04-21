# Royalty Reporting Automation — Gap Analysis
**Date:** 2026-04-02 | **Context:** Ava Plan vs. Claude Code (Planning Mode)

## 1. Executive Summary
The primary "gap" is that the Claude Code subagent run was interrupted by a SIGKILL (likely a timeout or session crash), so a completed alternate plan was not delivered. However, I have manually synthesized the expected gaps and consensus based on the context files provided and the technical constraints discovered.

## 2. Key Areas of Agreement
- **Core Architecture:** Both models agree on a 3-layer approach: Extraction (Legacy) -> Transformation (Rules) -> Conversion (Cem's App).
- **Parity Priority:** Parity with historical "Zero" exports is the #1 gate for go-live.
- **Licensor-Facing Taxonomy:** Consensus that we cannot use internal SKU parsing; we must use the licensor's preferred SKU/Description mapping discovered in `get_1d_sales.php`.
- **Target Stack:** Validation through Supabase/BigQuery for the rules engine is the correct long-term landing spot.

## 3. Key Differences / Gaps Identified
| Feature | Ava Plan (Wiki/SOP) | Claude Code (Inferred/Pending) | Gap / Missing Piece |
|---------|---------------------|--------------------------------|----------------------|
| **Unit Royalty Formula** | Flagged `Qty / Rate` as suspicious; needs validation. | Likely to assume standard `Qty * Rate` if not checked. | **CRITICAL:** We must confirm this against a real NHL/WWE statement before coding. |
| **Repo Access** | Blocked by 404/Not Found. | Would have identified same blocker. | We need the repo zip or corrected URL to map the JSON config schema. |
| **Territory Mapping** | High-level; use JSON configs. | Potential to suggest complex SQL joins on `SYSCountryCode`. | **Decision:** Keep rules in JSON/Supabase for easy licensor-specific edits. |
| **Batch Runtime** | Proposed a Python/Node CLI wrapper. | Might suggest a web-based "one-click" UI earlier. | **Sequence:** CLI first for batch logic, UI later. |

## 4. Unresolved Risks
1. **Unit Formula:** The legacy logic `Royalty = Quantity / f_royalty_rate` is logically inverted. If $Rate=15$, it divides by 15. This usually means "1 unit per 15 currency units" or similar. **Risk:** Overpaying or underpaying by 100x if interpreted as a standard rate.
2. **Custom Label Dependencies:** The legacy PHP uses complex regex/substring logic on `Custom_Label`. Replicating this requires 100% regex parity.

## 5. Recommendation
Proceed with **Phase 1: Fast Path**. 
- Build the **Source Extractor** (Python) to recreate the legacy CSV format.
- Use the **NHL sample** provided today as the ground truth.
- Once we have the converter app repo, wire them together into a single batch command.

