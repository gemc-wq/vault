# Ecom Expert RAG — Schema + Corpus Plan (v1)

## Goal
Create a retrieval layer that makes our “expert council” behave like an Apple/Casetify/OtterBox-grade ecommerce team: consistent critique, repeatable template decisions, and fast creative production.

This RAG is **not** “train on the internet.” It’s a curated canon + internal playbooks + experiment results.

---

## 1) Knowledge Domains (collections)
### A. Gold-Standard Benchmarks (external reference)
- Brands: Apple, Casetify, OtterBox, Fanatics/official stores, Skinit (as anti-pattern)
- Page types: Home, PLP/collections, PDP, cart/checkout, collab/drop pages, gift flows
- Social: top performing Reels/TikToks, paid creative patterns

### B. GoHeadCase System (internal truth)
- Template bible: modules, spacing/type rules, mobile rules
- Asset bible: required assets, ratios, safe zones, naming conventions
- Offer rules: shipping promises, returns, warranties, trust signals

### C. Economics & Constraints
- Unit economics assumptions (price, landed cost, royalties, marketplace fees)
- CAC ceilings, margin floors, SKU kill rules

### D. Data & Learnings
- Amazon business reports (sessions/units/sales)
- Future: BigQuery orders/inventory views + experiment log

---

## 2) Document Types (what we store)
### 2.1 Screenshot Pack (benchmark)
- `screenshots/{brand}/{yyyy-mm-dd}/{pageType}/...png`
- Companion note `.md` per page describing: hierarchy, modules, motion, trust, what to steal.

### 2.2 Pattern Card (atomic best practice)
One pattern per file:
- `patterns/{domain}/{patternName}.md`
- Example: `patterns/pdp/hero_above_fold.md`

### 2.3 Rubric / Scorecard
- `rubrics/design_critic_rubric.md`
- Scoring dimensions + definitions + examples.

### 2.4 Template Spec
- `templates/universe_landing_v1.md`
- `templates/homepage_v1.md`
- `templates/pdp_v1.md`

### 2.5 Experiment Record
- `experiments/{yyyy-mm-dd}_{hypothesis_slug}.md`
- Hypothesis, variants, audience, results, decision.

### 2.6 Data Dictionary
- `data/dictionaries/designcode_to_license.csv`
- `data/dictionaries/product_type_legend.md`

---

## 3) Metadata Schema (for retrieval)
All chunks should carry metadata fields:

### Required
- `source_type`: screenshot_note | pattern | rubric | template | experiment | dataset_doc | meeting_note
- `brand`: Apple | Casetify | OtterBox | GoHeadCase | Fanatics | Skinit | (etc)
- `page_type`: home | plp | pdp | nav | cart | checkout | collab | drop | gift
- `channel`: web | amazon | tiktok | instagram | youtube | email | sms
- `universe`: anime | sports | fantasy | characters | gaming | (nullable)
- `intent`: discovery | gift | conversion | retention | upsell
- `region`: US | UK | global | (nullable)
- `date_added`: ISO date

### Optional (high value)
- `device_focus`: iph | samsung | multi | (nullable)
- `price_tier`: budget | mid | premium
- `motion_level`: none | subtle | heavy
- `trust_signal`: licensed | protection | shipping | reviews | warranty
- `kpi_target`: cvt | aov | cac | ltv | roas

---

## 4) Chunking + Embedding Rules
- Chunk by headings/sections.
- Keep chunks ~200–600 tokens.
- Always include a short “TL;DR” line at top of each pattern/template section.
- Store canonical “Do/Don’t” bullets (these retrieve extremely well).

---

## 5) Retrieval Strategy (per agent)
### Design Critic
Query filters: `page_type`, `brand in [Apple,Casetify,OtterBox]`, `source_type in [rubric,pattern,screenshot_note]`
Return: rubric + 3–8 closest patterns + 2 benchmark examples.

### UX Architect
Filters: `source_type in [template,pattern]`, `page_type`, `intent`
Return: component specs + mobile rules + hierarchy guidance.

### CRO Strategist
Filters: `source_type in [experiment,pattern,data]`, `kpi_target`
Return: test ideas ranked by expected lift and feasibility.

### Creative Director
Filters: `source_type in [asset_spec,pattern,screenshot_note]`, `channel`
Return: asset checklist + examples + production prompts.

---

## 6) Minimal Corpus to Start (Week 1)
1) **20 benchmark pages** total
   - 8 Casetify (home, PLP, PDP, collab/drop)
   - 6 Apple (product pages, nav patterns)
   - 4 OtterBox (protection proof systems)
   - 2 Fanatics/official (sports merchandising)

2) **30 pattern cards**
   - 10 navigation/IA
   - 10 PDP conversion mechanics
   - 10 trust + shipping + gift flows

3) **3 templates**
   - Universe landing v1
   - PDP v1
   - Cart/checkout trust v1

---

## 7) Directory Layout (Brain)
Recommended Brain root:
- `Brain/Projects/goheadcase/rag/`
  - `screenshots/`
  - `notes/`
  - `patterns/`
  - `rubrics/`
  - `templates/`
  - `experiments/`
  - `data/`

---

## 8) Next Build Steps
1) Create folders + seed with rubric + templates.
2) Start screenshot capture + note-writing pipeline.
3) Ingest your Amazon reports + data dictionary.
4) Add an “experiment log” process so wins become retrieval assets.
