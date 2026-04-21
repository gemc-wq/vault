# Gemma 4 RAG Pipeline — Ecell Global
**Owner:** Ava | **Date:** 2026-04-05 | **Status:** Build

---

## Goal
Wire Gemma 4 26B (local Ollama) to Ecell's data so it can answer business analytics questions with full company context — zero API cost, zero latency, no Anthropic tokens.

## Architecture

```
User question
     ↓
Context Builder (Python)
  ├── SKU Parsing Rules (static markdown)
  ├── Design Code Map (BQ → JSON, 41K codes)
  ├── Device Code Map (182 devices, JSON)
  ├── Live Supabase query (top 50 designs by velocity, last 7d)
  └── Relevant schema snippets
     ↓
Ollama API (gemma4:26b at localhost:11434)
     ↓
Structured response
```

## Files to Build

### 1. `scripts/gemma4_rag.py` — Main RAG script
- Accepts a question via CLI or stdin
- Builds context from local data files
- Calls Ollama API (`POST /api/generate`)
- Returns structured answer

### 2. `data/design_code_brand_map.json` — Design code → brand/license mapping
- Build from: BQ `headcase.tblDesigns` (DesignLabel, BrandCode, LineupLabel)
- Format: `{"NARUICO": {"brand": "Naruto Shippuden", "lineup": "Naruto Iconic", "license": "NARU"}, ...}`

### 3. `data/rag_context_static.md` — Static context document
- SKU parsing rules (condensed)
- Product type reference table
- FBA prefix rules
- Region mapping
- Currency table

### 4. `scripts/build_design_map.py` — One-time BQ → JSON builder
- Query BQ `headcase.tblDesigns`
- Output `data/design_code_brand_map.json`

---

## Context Template

```
You are an AI data analyst for Ecell Global, a licensed tech accessories company.
You have deep knowledge of our product catalog, SKU structure, and business data.

=== SKU PARSING RULES ===
{sku_rules}

=== PRODUCT TYPES ===
{product_types}

=== DESIGN CODES (sample - top 100 by revenue) ===
{design_codes}

=== DEVICE CODES ===
{device_codes}

=== LIVE DATA (last 7 days) ===
{live_supabase_data}

=== QUESTION ===
{question}

Answer concisely with specific numbers where available. Use tables for comparisons.
```

---

## Ollama API Call

```python
import requests, json

def ask_gemma4(question, context):
    prompt = context.replace("{question}", question)
    resp = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma4:26b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,   # Low temp for analytics
            "num_ctx": 32768,     # Large context window
            "num_predict": 2048
        }
    })
    return resp.json()["response"]
```

---

## Live Data Queries (Supabase)

```python
# Top 50 designs last 7 days
top_designs = supabase.rpc("get_top_designs_7d", {}).execute()

# Current inventory alerts
alerts = supabase.table("blank_inventory")\
    .select("sku,product_type_code,device_code,free_stocks,alert_level")\
    .in_("alert_level", ["RED","BLACK"])\
    .limit(50).execute()
```

---

## Test Questions (validation suite)

1. "What are our top 10 selling designs in the last 7 days?"
2. "Parse this SKU: FHTPCR-IPH17PMAX-NARUICO-AKA"
3. "Which product types are most profitable?"
4. "What inventory is critically low right now?"
5. "How many HB401 listings do we have vs HTPCR?"
6. "What's the difference between NARUICO and NARUCHA?"
7. "Which Samsung devices should we prioritize for new listings?"

---

## Phase 2 (week 2) — Fine-tune with LoRA
Once RAG is validated:
- Build Q&A training pairs from our weekly analysis sessions
- Fine-tune `gemma4:26b` with LoRA on Mac Studio GPU (36GB RAM)
- Push fine-tuned model back to Ollama
- Compare RAG vs fine-tuned accuracy
