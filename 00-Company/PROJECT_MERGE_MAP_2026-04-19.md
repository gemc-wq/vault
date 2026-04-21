# Project Merge Map — Proposal for Cem Approval
**Created:** 2026-04-19 | **Status:** DRAFT — awaiting Cem review
**Goal:** Collapse 61 folders in `02-Projects/` → ≤30 canonical projects

---

## How to Use This Doc

Each row below proposes: `current-folder(s)` → `canonical-folder`.

Cem: review each group, mark one of:
- ✅ **Approve** — merge as proposed
- ✏️ **Edit** — keep plan but rename / re-group (add note)
- ❌ **Reject** — keep folders separate (add reason)

Once approved, Athena executes in one batch:
1. Read all docs in source folders
2. Consolidate into canonical folder with clear sub-structure
3. Archive source folders to `02-Projects/zz-archive/YYYY-MM-DD-pre-merge/`
4. Register canonical project in `02-Projects/_INDEX.md`
5. Log in CHANGE_LOG.md

**Nothing is deleted.** Sources go to archive. Fully reversible.

---

## Naming Convention (Proposed)

Format: `domain-object-qualifier`
- **domain** = business area (marketplace, dashboard, finance, ops, tool, ai, product)
- **object** = the thing (walmart, pulse, royalty, etc.)
- **qualifier** = optional (v3, launch, audit)

Examples:
- `marketplace-walmart-launch`
- `dashboard-pulse-v3`
- `finance-royalty-reporting`
- `ai-image-generation`
- `tool-listing-forge`

---

## The Merge Map

### Group 1 — Dashboards (Pulse / Command Center)
**Current:**
- `pulse-dashboard/`
- `pulse-dashboard-v2/`
- `pulse-unified/`
- `command-center/`
- `dashboard-product-entry/`

**Proposed canonical:** `dashboard-pulse/`
**Sub-structure:**
```
dashboard-pulse/
├── README.md              ← canonical: status, owner, purpose
├── v1-deprecated/         ← old pulse-dashboard content
├── v2-current/            ← pulse-dashboard-v2 content (Ava)
├── v3-unified-plan/       ← pulse-unified content (future)
├── command-center/        ← kept as sub-module (Athena's ops view)
└── product-entry-tool/    ← kept as sub-module (data entry UI)
```
**Rationale:** These are all views onto the same operational data. Consolidating gives one README with clear version/sub-module status. Ava owns.

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 2 — Walmart Marketplace
**Current:**
- `walmart/`
- `walmart-lister/`
- `walmart-listing-audit/`
- `walmart-review-strategy/`

**Proposed canonical:** `marketplace-walmart/`
**Sub-structure:**
```
marketplace-walmart/
├── README.md              ← status, owner, revenue target
├── launch-plan/           ← from walmart/
├── lister-tool/           ← from walmart-lister/ (if separate from listing-forge)
├── audits/                ← from walmart-listing-audit/
└── review-strategy/       ← from walmart-review-strategy/
```
**Rationale:** All Walmart work in one place. $750K gap cited in impact analysis — deserves a single project home.

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 3 — Other Marketplaces
**Current:**
- `shopify-repush/`
- `target-plus-migration/`
- `bigcommerce-api/`

**Proposed: keep separate, rename for consistency:**
- `marketplace-shopify-repush/`
- `marketplace-target-plus/`
- `marketplace-bigcommerce/`

**Rationale:** Distinct marketplaces, distinct launch plans. Rename only for `_INDEX.md` sort order.

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 4 — Finance
**Current:**
- `finance/`
- `finance-ops/`
- `Projects/Finance/` (outside main tree)
- `royalty-reporting/`
- `procurement/`

**Proposed:**
- `finance-ops/` — keep as primary (has most recent activity, Cem's active CLI project)
- `finance-royalty-reporting/` — keep separate (distinct deliverable, Harry domain)
- `finance-procurement/` — keep separate (PO management, Harry domain)
- Merge `finance/` and `Projects/Finance/` contents into `finance-ops/archive/`

**Rationale:** Finance has three genuinely distinct streams: ops platform (Xero integration), royalty compliance, and procurement. The legacy `finance/` and orphan `Projects/Finance/` are stale.

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 5 — Listings Infrastructure
**Current:**
- `listing-forge/`
- `listings-db/`
- `listings-intelligence/`
- `weekly-listing-audit/`
- `LISTINGS_MANAGEMENT_SYSTEM_SPEC.md` (loose file at root of `02-Projects/`)

**Proposed:**
- `tool-listing-forge/` — keep (MVP tool, Jay Mark building)
- `tool-listings-db/` — keep (backend schema, listings data warehouse)
- `analytics-listings-intelligence/` — keep (analytics layer)
- `ops-weekly-listing-audit/` — keep (cron job output, Hermes owns)
- Move loose `LISTINGS_MANAGEMENT_SYSTEM_SPEC.md` into `tool-listing-forge/` as root spec

**Rationale:** These are genuinely distinct pieces of the listings stack (tool, DB, analytics, audit). Rename prefix makes domain clear. Don't collapse — they have different owners and lifecycles.

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 6 — Prune
**Current:**
- `prune/`
- `prune-app/`

**Proposed canonical:** `tool-prune/`
**Rationale:** Same dead-stock identification tool, likely spec + implementation split. Consolidate.

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 7 — Fulfillment
**Current:**
- `fulfillment-portal/`
- `fulfillment-dashboard/`
- `shipping-template-dashboard/`

**Proposed canonical:** `ops-fulfillment-portal/`
**Sub-structure:**
```
ops-fulfillment-portal/
├── README.md              ← status (Jay Mark taking over from Harry)
├── portal-spec/           ← from fulfillment-portal/
├── dashboard/             ← from fulfillment-dashboard/
└── shipping-templates/    ← from shipping-template-dashboard/
```
**Rationale:** Portal + dashboard + templates are one fulfillment ops stack. One README for handover clarity.

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 8 — PULSE vs Amazon Data
**Current:**
- `amazon-data-analytics/`
- `amazon-report-middleware/`

**Proposed:**
- `analytics-amazon-data/` — merge both here (middleware feeds analytics)

**Rationale:** Middleware and analytics are two stages of one pipeline. One project owner, one README.

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 9 — AI Infrastructure
**Current:**
- `brain-memory-layer/`
- `gemma4-rag/`
- `nemoclaw-rd/`
- `openclaw-saas/`
- `delegait/`
- `sentinel-agent/`

**Proposed:**
- `ai-memory-layer/` (from brain-memory-layer — consolidated with gemma4-rag if same thing)
- `ai-nemoclaw-rd/` (keep — R&D experiment)
- `product-openclaw-saas/` (SaaS product idea)
- `product-delegait/` (separate SaaS product)
- `agent-sentinel/` (operational monitoring agent)

**Rationale:** Separate infrastructure, R&D, product ideas, and operational agents. Prefix makes type obvious.

**Question for Cem:** Are `brain-memory-layer` and `gemma4-rag` the same project? If yes — merge. If no — keep both with rename.

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 10 — Infrastructure & Ops
**Current:**
- `infrastructure/`
- `supabase-rls-fix/`
- `eod-automation/`
- `vault/`
- `hermes-deployment/`

**Proposed:**
- `infra-core/` (was `infrastructure/`)
- `infra-supabase/` (absorb `supabase-rls-fix/` — it's done, archive its contents here)
- `ops-eod-automation/`
- `infra-vault/` (was `vault/`)
- `agent-hermes-deployment/` (Hermes-specific deploy work)

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 11 — Product / Launches
**Current:**
- `one-piece/`
- `new-products/`
- `world-cup-2026/`
- `GOHEADCASE_PRODUCT_MATRIX.md` (loose file)

**Proposed:**
- `launch-one-piece/` (P0 pilot — keep as is, rename only)
- `launch-new-products/` (general pipeline)
- `launch-world-cup-2026/`
- Move `GOHEADCASE_PRODUCT_MATRIX.md` into `00-Company/` or `01-Wiki/14-goheadcase/` — it's reference, not a project

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 12 — Legacy / Archive Candidates
**Current (likely dormant, need to archive):**
- `ppc-autoresearch/` (5.6K files, research)
- `image-tests/`
- `playbook-revision/`
- `org/`
- `99-On-Hold/` (already an archive folder)
- Root-level loose files: `PRICING_OPTIMIZER_SPEC.md`, `WEEKLY_STRATEGIC_BRIEF_2026-03-06.md`

**Proposed:**
- Move `ppc-autoresearch/`, `image-tests/`, `playbook-revision/`, `org/` into `zz-archive/`
- Keep `99-On-Hold/` for intentionally paused work
- Move loose root-level docs into appropriate canonical folders or `zz-archive/`

Cem decision: [ ] ✅ [ ] ✏️ [ ] ❌   Note: _______________

---

### Group 13 — Keep As-Is (Already Canonical)
These folders have clear names, single purposes, and active ownership. Rename for prefix consistency only:

| Current | Rename To | Owner |
|---------|-----------|-------|
| `ecell-app/` | `product-ecell-app/` | Jay Mark |
| `ecell-website/` | `product-ecell-website/` | PH Creative |
| `iren-dreco/` | `ops-iren-dreco/` | Athena (Lane 2) |
| `inventory-ordering/` | `ops-inventory-ordering/` | Harry |
| `licensing/` | `ops-licensing/` | Cem |
| `marketing/` | `ops-marketing/` | Ava |
| `sku-staging/` | `ops-sku-staging/` | Ava |
| `product-intelligence-engine/` | `analytics-product-intelligence/` | Ava |
| `listings-intelligence/` | (covered in Group 5) | — |

Cem decision: [ ] ✅ approve all renames [ ] ✏️ edit list [ ] ❌ no renames   Note: _______________

---

## Resulting Structure (Post-Merge)

Estimated final project count: **~28 canonical folders** (down from 61)

```
02-Projects/
├── _INDEX.md                         ← NEW: canonical project list
│
├── launch-one-piece/                 ← P0: Blueprint V3 pilot
├── launch-new-products/
├── launch-world-cup-2026/
│
├── marketplace-walmart/              ← consolidated from 4
├── marketplace-shopify-repush/
├── marketplace-target-plus/
├── marketplace-bigcommerce/
│
├── tool-listing-forge/
├── tool-listings-db/
├── tool-prune/                       ← consolidated from 2
│
├── dashboard-pulse/                  ← consolidated from 5
│
├── analytics-amazon-data/            ← consolidated from 2
├── analytics-listings-intelligence/
├── analytics-product-intelligence/
│
├── finance-ops/                      ← consolidated from 3
├── finance-royalty-reporting/
├── finance-procurement/
│
├── ops-fulfillment-portal/           ← consolidated from 3
├── ops-iren-dreco/
├── ops-inventory-ordering/
├── ops-licensing/
├── ops-marketing/
├── ops-sku-staging/
├── ops-eod-automation/
├── ops-weekly-listing-audit/
│
├── product-ecell-app/
├── product-ecell-website/
├── product-openclaw-saas/
├── product-delegait/
│
├── ai-memory-layer/
├── ai-nemoclaw-rd/
├── ai-image-generation/              ← NEW: per impact analysis #1 priority
│
├── agent-sentinel/
├── agent-hermes-deployment/
│
├── infra-core/
├── infra-supabase/
├── infra-vault/
│
├── 99-On-Hold/                       ← intentionally paused
└── zz-archive/
    └── 2026-04-19-pre-merge/         ← all superseded folders
```

---

## Execution Protocol (Once Approved)

1. **Git snapshot** entire vault before touching anything
2. **Create `02-Projects/_INDEX.md`** with the canonical list
3. **Create `02-Projects/zz-archive/2026-04-19-pre-merge/`**
4. **For each merge group:**
   - Read all README / spec files in source folders
   - Synthesise into canonical folder's README.md with version history
   - Move remaining files into sub-folders per proposed structure
   - Move source folder into zz-archive
5. **Update `00-Company/compiled/PROJECT_BOARD.md`** to reference canonical names
6. **Update all `03-Agents/*/TOOLS.md`** references to renamed folders
7. **Update `00-Company/compiled/TASK_SHEET.md`** to use canonical project names
8. **Log to CHANGE_LOG.md**
9. **Notify Cem on Telegram** with before/after counts

---

## Questions for Cem Before Execution

1. Are `pulse-dashboard`, `pulse-dashboard-v2`, and `pulse-unified` genuinely versions of the same thing, or do they have distinct purposes I should preserve? (I'll verify by reading their READMEs if uncertain.)
2. Is `brain-memory-layer` the same as `gemma4-rag`? They sound related.
3. Does `command-center/` have a distinct purpose worth preserving as a top-level folder, or folding into `dashboard-pulse/`?
4. Do you want `ai-image-generation/` created as a NEW folder to hold the #1 priority from the impact analysis? (Currently the impact analysis is a loose file; this would give it a project home.)

---

*Once approved — partially or fully — Athena will execute. Sources go to archive, not the bin. Everything reversible for 90 days.*