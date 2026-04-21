# Royalty Reporting Automation — Implementation Map

## Goal
Automate royalty reporting end-to-end so a user enters a date range once, runs one batch job, and gets all licensor-specific royalty output files generated automatically.

Target user flow:
1. Enter `from_date` and `to_date`
2. Pull/export legacy-format source data from Zero
3. Split/filter by licensor
4. Apply licensor-specific config JSON + lookup files
5. Generate all required output files in one batch
6. Save outputs to a predictable folder and optionally upload/distribute

---

## 1. System architecture

There are **three layers** in the future-state system:

### Layer A — Source extractor
Purpose:
- reproduce the old Zero royalty export format for a given date range
- output the same columns the existing converter app expects

Primary source format confirmed from sample CSV:
- `Brand Name`
- `Sales Record Number`
- `Sage Order Number`
- `AC-Ref`
- `Status`
- `Is Refunded`
- `User ID`
- `Buyer Name`
- `Address Line 1`
- `City`
- `Country`
- `State`
- `Custom Label`
- `SKU`
- `Description`
- `Item Title`
- `Quantity`
- `Currency`
- `Price`
- `Net Sales`
- `Tax`
- `Sale Date`
- `Paid Date`
- `Paypal ID`
- `Transaction ID`
- `Sage Company`
- `Site`
- `Royalty Rate`
- `EU-NonEU Country`
- `Total Net Sales`
- `Sage ER`
- `GBP Net Sales Amount`
- `Territory`
- `OLD Net Sales`
- `OLD Total Net Sales`
- `OLD GBP Net Sales Amount`

### Layer B — Legacy-logic replication engine
Purpose:
- replicate the old Zero logic deterministically
- especially the parts not already externalized in the new app

Responsibilities:
- brand/licensor resolution
- exchange-rate assignment
- net-sales normalization
- territory derivation
- royalty rate injection
- SKU rewrite rules
- description rewrite rules
- exclusions / edge-case filtering

### Layer C — Existing royalty report converter
Purpose:
- take normalized input and generate licensor-specific output files using JSON config files
- this is the app Cem says is already built

Current blocker:
- I could not access the GitHub repo at the provided URL (`gemc-wq/royalty-report-converter`) from here; GitHub returned `Repository not found`
- so this map assumes the converter app consumes the legacy export format or a very close normalized variant

---

## 2. Recommended implementation strategy

## Strategy recommendation: build in two phases

### Phase 1 — Batch automation on top of legacy-format export
Fastest path to value.

Build a runner that:
1. accepts date range
2. generates the legacy-format CSV from Zero data
3. runs converter for every licensor config
4. writes all outputs into `/outputs/YYYY-MM-DD_to_YYYY-MM-DD/`

This gets one-click batch reporting working without rewriting everything.

### Phase 2 — Full rules externalization into Supabase/BQ
Longer-term cleanup.

Move all legacy logic into durable tables/configs:
- royalty master data
- exchange rates
- territory mappings
- SKU rewrite rules
- description rewrite rules
- exclusions
- output template metadata

This removes dependence on legacy PHP.

---

## 3. Source extractor specification

## Inputs
- `from_date`
- `to_date`
- optional `license_filter[]`
- optional `site_filter[]`
- optional `include_refunds`

## Output
Single CSV in legacy royalty tracker shape.

## Data sources required
From legacy findings:
- order/sales source table(s)
- Sage return/tax/account lookup
- exchange-rate lookup with date windows
- `SYSCountryCode`
- royalty master tables:
  - `t_royalty_information`
  - `t_royalty_rates`
  - `t_royalty_information_temp`
- lineup/design lookups:
  - `headcase.tblLineups`
  - `headcase.tblDesigns`
  - `headcase.tblDesignProductAvailability`

## Required transformation stages inside extractor
1. load raw sales rows by date range
2. derive licensor / brand
3. parse base `SKU` and `DSN` from `Custom Label`
4. inject royalty master fields
5. compute / assign `Sage ER`
6. compute `Net Sales`, `Total Net Sales`, `GBP Net Sales Amount`
7. derive `EU-NonEU Country`
8. apply exclusion rules
9. apply reporting SKU rewrite rules
10. apply reporting Description rewrite rules
11. derive final `Territory`
12. output legacy-shape CSV

---

## 4. Proposed target schema (Supabase / BigQuery)

## Core transactional staging
### `royalty_source_sales`
Raw imported rows before transformation.

Suggested columns:
- `source_row_id`
- `source_system`
- `sales_record_number`
- `sale_date`
- `paid_date`
- `status`
- `is_refunded`
- `user_id`
- `buyer_name`
- `address_line_1`
- `city`
- `country`
- `state`
- `custom_label`
- `item_title`
- `quantity`
- `currency`
- `price`
- `tax`
- `paypal_id`
- `transaction_id`
- `sage_company`
- `site`

### `royalty_sales_normalized`
Post-transformation reporting rows.

Suggested columns:
- `report_run_id`
- `source_row_id`
- `brand_name`
- `licensor_key`
- `reporting_sku`
- `reporting_description`
- `base_sku`
- `dsn`
- `territory`
- `eu_non_eu_country`
- `currency`
- `price`
- `net_sales`
- `total_net_sales`
- `sage_er`
- `gbp_net_sales_amount`
- `royalty_rate`
- `royalty_rate_type`
- `royalty_amount`
- `site`
- `paid_date`
- `custom_label`
- `item_title`
- `normalization_notes_json`

## Rules / config tables
### `royalty_licenses`
- `licensor_key`
- `brand_name`
- `royalty_name`
- `property_name`
- `entity`
- `reporting_frequency`
- `payment_currency`
- `accounting_type`
- `supplier_code`
- `supplier_currency`
- `active`

### `royalty_rates`
- `licensor_key`
- `effective_from`
- `effective_to`
- `royalty_rate`
- `royalty_rate_type`
- `notes`

### `royalty_exchange_rates`
- `source_currency`
- `target_currency`
- `effective_from`
- `effective_to`
- `rate`
- `rate_source`

### `royalty_country_classification`
- `country_name`
- `eu_non_eu_flag`
- `default_territory`

### `royalty_territory_mappings`
- `licensor_key`
- `source_country`
- `source_site`
- `mapped_territory`
- `priority`

### `royalty_sku_rewrite_rules`
- `licensor_key`
- `match_type` (`exact`, `regex`, `contains`, `custom_label_contains`, `product_type_prefix`)
- `match_value`
- `secondary_match_value`
- `output_sku`
- `priority`
- `active`

### `royalty_description_rules`
- `licensor_key`
- `match_type`
- `match_value`
- `secondary_match_value`
- `output_description`
- `description_source_type` (`literal`, `lineup_name`, `design_name`, `royalty_code`, `concat`)
- `priority`
- `active`

### `royalty_reference_skus`
- `licensor_key`
- `approved_sku`
- `approved_description`
- `property`
- `contract`
- `product_category`
- `reference_payload_json`

### `royalty_exclusion_rules`
- `licensor_key`
- `match_type`
- `match_value`
- `reason`
- `active`

### `royalty_output_templates`
- `licensor_key`
- `config_file_name`
- `template_file_name`
- `output_type`
- `output_extension`
- `active`

---

## 5. Batch pipeline design

## Job: `generate_royalty_reports`

### Inputs
- `from_date`
- `to_date`
- `license_filter[]` optional
- `dry_run` optional

### Steps
1. **extract_source_data**
   - query source data for date range
   - produce `royalty_source_sales`
   - optional CSV export snapshot

2. **normalize_legacy_logic**
   - apply all transformation logic
   - populate `royalty_sales_normalized`

3. **partition_by_licensor**
   - create one normalized input dataset per `licensor_key`

4. **run_converter_configs**
   - iterate over available licensor JSON configs
   - feed matching normalized data into converter
   - produce final export files

5. **write_output_bundle**
   - save to:
     - `outputs/royalty/{from}_{to}/source/`
     - `outputs/royalty/{from}_{to}/normalized/`
     - `outputs/royalty/{from}_{to}/final/`
     - `outputs/royalty/{from}_{to}/logs/`

6. **validation_report**
   - counts by licensor
   - source rows vs output rows
   - zero-value rows
   - unknown SKU mappings
   - unknown territories
   - missing config warnings

---

## 6. Validation rules

## Row-level validation
For each normalized row validate:
- `brand_name` resolved
- `reporting_sku` not null
- `reporting_description` not null
- `royalty_rate` not null
- `sage_er` not null unless GBP-native row
- `gbp_net_sales_amount` not null

## Batch-level validation
For each licensor batch validate:
- row count > 0 when source sales exist
- total quantity matches source after exclusions
- total GBP net sales within tolerance of legacy export
- total royalty amount within tolerance of legacy export

## Exception buckets
Create explicit outputs for:
- `unknown_licensor_rows.csv`
- `unknown_sku_rules.csv`
- `unknown_description_rules.csv`
- `unknown_territory_rows.csv`
- `missing_rate_rows.csv`

---

## 7. What the sample CSV tells us already

From the attached NHL sample export:

### Confirmed fields available from extractor
- the legacy export already contains almost everything the converter should need
- especially:
  - licensor/brand
  - territory
  - normalized SKU
  - normalized description
  - GBP-normalized amount
  - royalty rate

### Confirmed site/channel diversity
Observed source sites include:
- `Amazon.com (US)`
- `Amazon.co.uk`
- `Amazon.de`
- `Amazon.fr`
- `Amazon.ie`
- `Fanatics D2C`
- `Rakuten`
- `Walmart`
- `Big Commerce`
- `e_cell`
- `head_case_designs-us`
- `ecell_accessorize`

This means the converter / normalization layer needs stable channel mapping rules.

### Confirmed currency diversity
Observed currencies include:
- `USD`
- `GBP`
- `EUR`
- `JPY`
- `AUD`

So exchange-rate normalization must be first-class, not a side note.

### Confirmed edge cases
Observed edge cases already present in sample:
- FBA rows
- zero-value sales rows
- multi-marketplace rows under same licensor
- non-UK territories reported as `United Kingdom` in `Territory` for some channels
- different `Site` names for similar channels
- localized product titles with encoding noise
- varying `Country` text values (`USA`, `United States`, `United States Of America`)

These need standardization rules before final output generation.

---

## 8. Immediate implementation backlog

## P0
1. **Gain access to converter repo**
   - current GitHub URL returned `Repository not found`
   - need either:
     - correct repo URL
     - repo made visible to current token/account
     - zip/local copy

2. **Inspect converter I/O contract**
   - exact CLI / run command
   - input file expectations
   - output file naming rules
   - config directory structure

3. **Build extractor spec from legacy source**
   - confirm exact source queries/tables
   - confirm whether extractor should call old PHP temporarily or be rebuilt directly in SQL/Python/Node

## P1
4. **Create canonical normalized schema**
5. **Externalize first ruleset (NHL)**
6. **Run parity test using attached NHL sample**

## P2
7. Add LFC / NFL / WWE / FCB next
8. Add full batch runner UI or command
9. Add scheduled / recurring generation option

---

## 9. Recommended technical shape

## Fastest practical build
- **Extractor:** Python or Node script
- **Rule storage:** Supabase tables or JSON during phase 1
- **Batch orchestrator:** simple CLI + optional web form
- **Output storage:** filesystem first, cloud later

## Recommended commands / flow
Example future UX:

```bash
royalty-batch run --from 2026-03-01 --to 2026-03-31
```

Outputs:
- `source_export.csv`
- `normalized_nhl.csv`
- `normalized_lfc.csv`
- final licensor files in configured formats
- `run_summary.json`
- `exceptions/*.csv`

---

## 10. What I need from Cem next

To move from map -> build cleanly, I need:

1. **Working access to the converter app**
   - corrected GitHub repo URL or a local copy

2. **One sample input + one expected output pair**
   Preferably for NHL first:
   - legacy export CSV in current format
   - final converter-generated licensor output file
   - matching config JSON used for that output

3. **Decision on build mode**
Choose one:
- **A. Fast path:** build batch wrapper around existing converter + legacy-format extractor
- **B. Clean path:** also start externalizing rules into Supabase now

---

## 11. My recommendation

Do **A first, B second**.

Reason:
- fastest route to business value
- least risk
- lets us verify parity against real reports before refactoring the rule engine
- once parity is proven, we can migrate rules out of old PHP safely

So the plan should be:
1. replicate/export legacy-format CSV automatically
2. feed it into your existing converter in batch
3. validate parity on NHL
4. then migrate the rules model into Supabase/BQ
