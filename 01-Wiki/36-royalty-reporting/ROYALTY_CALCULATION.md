# Royalty Calculation

## Legacy PHP royalty management
Primary admin source: `barcode/royalty_report_manager.phpRON20210426`

### Master tables
- `t_royalty_information`
- `t_royalty_information_temp`
- `t_royalty_rates`
- `t_user_profile`

### Config / reference code
```php
$license_status = array("1" => "Active", "0" => "Inactive", "5" => "Duplicate");
```

```php
$sql = "SELECT f_royalty_id, f_rate, f_effective_date FROM t_royalty_rates WHERE f_status = 1 GROUP BY f_royalty_id ORDER BY f_effective_date DESC";
```

### Data model fields
Observed fields include:
- `f_royalty_id`
- `f_royalty_name`
- `f_property_name`
- `f_licensor_agent_name`
- `f_reporting_frequency`
- `f_payment_currency`
- `f_royalty_rate`
- `f_royalty_rate_type`
- `f_supplier_code`
- `f_accounting_type`
- `f_royalty_status`

### Approval workflow
Edits can stage into `t_royalty_information_temp` before approval, with submitter resolved through `t_user_profile`.

## BigQuery-based royalty app
Sources:
- `royalty-app/app/services/bigquery.py`
- `royalty-app/sql/royalty_report_detailed.sql`

### BigQuery client
```python
def create_client() -> bigquery.Client:
    return bigquery.Client(project=settings.gcp_project_id)
```

### Datasets / tables referenced
- ``instant-contact-479316-i4.zero_dataset.orders``
- ``instant-contact-479316-i4.cfxb2b_db.brands``
- ``instant-contact-479316-i4.elcell_co_uk_barcode.t_royalty_information``
- ``instant-contact-479316-i4.elcell_co_uk_barcode.t_royalty_rates``

## Detailed calculation logic
From `royalty_report_detailed.sql`:

```sql
CASE
  WHEN UPPER(f_royalty_rate_type) = 'PERCENTAGE'
    THEN ROUND(SUM(net_sale) * applicable_rate / 100, 2)
  WHEN UPPER(f_royalty_rate_type) = 'UNIT'
    THEN ROUND(SUM(quantity) * applicable_rate, 2)
  ELSE 0
END AS royalty_owed
```

### Important joins
```sql
INNER JOIN `...cfxb2b_db.brands` AS b
  ON od.Brand = b.Name
INNER JOIN `...elcell_co_uk_barcode.t_royalty_information` AS ri
  ON b.Label = ri.f_property_name
```

This means license matching is effectively:
1. order.Brand → brands.Name
2. brands.Label → royalty_information.f_property_name

### Historical rate lookup
```sql
LEFT JOIN `...t_royalty_rates` AS rr
  ON br.f_royalty_id = rr.f_royalty_id
 AND rr.f_effective_date <= br.Paid_Date
 AND rr.f_status = 'Active'
```

The report chooses the latest rate effective on the order's paid date; if none exists, it falls back to the default rate on `t_royalty_information`.

## Report filters
- exclude `Status = 'Cancelled'`
- exclude refunded orders (`Is_Refunded IS NULL OR FALSE`)
- date range via `@start_date`, `@end_date`
- active royalty records only (`ri.f_royalty_status = 'Active'`)

## Report output grain
Grouped by:
- royalty id / name
- property / licensor
- rate type / currency
- marketplace
- brand
- product
- custom label
- applicable rate

That is much more granular than the legacy PHP admin pages.

## License tracking per brand
Brand/license mapping is not direct on orders alone. The chain is:

`orders.Brand` -> `brands.Name` -> `brands.Label` -> `t_royalty_information.f_property_name`

So `brands.Label` is the critical bridge field that must be preserved in any future portal.

## Hardcoded values to externalize
- GCP project id source / dataset names
- status strings (`Cancelled`, `Active`, `PERCENTAGE`, `UNIT`)
- dump directories:
  - `/var/www/barcode/royalty_report_dumps/RRInfroDB_DUMP/`
  - `/var/www/barcode/royalty_report_dumps/RRStatementEmail/`

## What to Replicate
1. Keep royalty contracts as versioned records with effective dates.
2. Separate contract master data from calculation outputs.
3. Preserve the brand-to-license bridge explicitly; do not rely on fuzzy matching.
4. Support both percentage and per-unit royalty methods.
5. Expose report drilldown by marketplace / brand / product / SKU.
6. Add validation for missing brand-label-to-property mappings.

---

## Royalty Reporting Automation SOP

### Objective
Build a one-click royalty reporting workflow where a user selects a date range once, runs a batch job, and receives all licensor-specific royalty output files automatically.

### Scope
This SOP covers:
- extracting royalty source data in the legacy Zero-compatible format
- applying the required legacy transformation logic
- feeding the normalized input into the newer config-driven royalty converter
- generating all output files in batch
- validating parity against the old process before go-live

This SOP does **not** assume a full immediate rewrite of all royalty logic. It is designed to get a working batch system live first, then progressively externalize and modernize the rules.

### Recommended delivery strategy
**Recommendation: fast path first, full externalization second.**

Reason:
- fastest path to operational value
- lowest implementation risk
- allows parity testing against known legacy outputs before replacing old logic
- avoids rewriting fragmented PHP rules blindly

That means:
1. automate legacy-format royalty export generation
2. feed that export into the existing converter app in batch
3. verify output parity with real samples
4. only then externalize the rule engine into Supabase/BigQuery

---

## System Architecture

### Layer 1 — Source Extractor
Purpose:
- generate the legacy royalty tracker CSV for a chosen date range
- match the shape expected by downstream royalty conversion

Expected output columns include:
- Brand Name
- Sales Record Number
- Sage Order Number
- AC-Ref
- Status
- Is Refunded
- User ID
- Buyer Name
- Address Line 1
- City
- Country
- State
- Custom Label
- SKU
- Description
- Item Title
- Quantity
- Currency
- Price
- Net Sales
- Tax
- Sale Date
- Paid Date
- Paypal ID
- Transaction ID
- Sage Company
- Site
- Royalty Rate
- EU-NonEU Country
- Total Net Sales
- Sage ER
- GBP Net Sales Amount
- Territory
- OLD Net Sales
- OLD Total Net Sales
- OLD GBP Net Sales Amount

### Layer 2 — Legacy Logic Replication
Purpose:
- reproduce the business logic historically embedded in Zero/barcode PHP and royalty SQL

Responsibilities:
- licensor / brand resolution
- brand → property → royalty contract bridge
- exchange-rate assignment by effective date
- net sales normalization
- GBP conversion
- territory derivation
- EU/non-EU classification
- royalty rate lookup
- SKU rewrite rules for licensor-recognized reporting SKU
- Description rewrite rules for licensor-recognized reporting description
- exclusion rules and row suppression

### Layer 3 — Config-Driven Converter
Purpose:
- use existing licensor-specific JSON configs to generate final royalty files
- batch-generate all required outputs from one normalized input run

---

## Data Inputs and Dependencies

### Core transactional data
Required from orders/sales source:
- order identifiers
- paid date / sale date
- marketplace/site
- country/state
- custom label
- item title
- quantity
- currency
- price
- refund/cancel status

### Contract and rate master data
Required tables:
- `t_royalty_information`
- `t_royalty_information_temp`
- `t_royalty_rates`

Required fields include:
- `f_royalty_id`
- `f_royalty_name`
- `f_property_name`
- `f_reporting_frequency`
- `f_payment_currency`
- `f_royalty_rate`
- `f_royalty_rate_type`
- `f_supplier_code`
- `f_accounting_type`
- `f_royalty_status`

### Brand/license bridge
Critical bridge:
- `orders.Brand` -> `brands.Name`
- `brands.Label` -> `t_royalty_information.f_property_name`

This must be preserved explicitly. Do not replace it with fuzzy matching.

### Geographic and territory logic
Required dependencies:
- `SYSCountryCode`
- licensor-specific territory mappings
- consistent country normalization layer

### Exchange-rate logic
Required dependencies:
- effective-dated exchange-rate table or source
- selection logic based on paid date

### Reference assets
Required from newer converter layer:
- licensor JSON config files
- any reference/master SKU CSVs used by those configs
- any output templates or mapping files

---

## Workflow SOP

### Step 1 — Define reporting period
Input required:
- `from_date`
- `to_date`
- optional licensor filter

Output:
- a unique run id and output folder for the batch

### Step 2 — Extract source sales rows
Pull sales rows for the reporting period.

Minimum filters:
- exclude `Status = Cancelled`
- exclude refunded rows unless business rules explicitly require inclusion
- only include active royalty mappings/contracts

Write raw extracted data to a staging table or file snapshot.

### Step 3 — Resolve license / contract mapping
For each row:
- resolve brand
- bridge to property/royalty contract
- assign royalty id and applicable licensor

Validation:
- rows without a valid bridge must be isolated into an exceptions file

### Step 4 — Apply financial normalization
For each row:
- calculate `Net Sales`
- calculate `Total Net Sales`
- assign `Sage ER`
- calculate `GBP Net Sales Amount`

Current reference logic:
- percentage royalty support confirmed
- per-unit royalty support confirmed in SQL layer
- legacy PHP unit logic should not be copied blindly without sample validation

### Step 5 — Apply geography / territory logic
For each row:
- classify EU vs non-EU
- normalize country naming
- assign reporting territory according to licensor/channel rules

### Step 6 — Apply reporting SKU logic
For each row:
- derive reporting SKU from custom label / legacy rewrite rules / licensor references
- do not assume internal SKU = licensor SKU

### Step 7 — Apply reporting Description logic
For each row:
- derive final reporting description using licensor-facing rules
- use legacy mappings or config-driven mappings where appropriate

### Step 8 — Produce legacy-format normalized export
Write a canonical normalized CSV in the same legacy-compatible shape.

This file becomes the handoff into the converter app.

### Step 9 — Run batch converter
For each active licensor config:
- filter matching rows
- invoke converter
- generate final output file(s)
- save all artifacts under the current run folder

### Step 10 — Generate validation pack
For every run, produce:
- summary counts by licensor
- source row count vs normalized row count
- output file count
- total GBP net sales by licensor
- total royalty amount by licensor
- exceptions files for missing mappings or rule failures

---

## Validation and QA SOP

### Row-level checks
Every normalized row should have:
- licensor resolved
- royalty rate resolved
- reporting SKU populated
- reporting description populated
- currency populated
- territory populated
- GBP net sales amount populated where required

### Batch-level checks
For each licensor:
- source row count reconciles to normalized row count after exclusions
- quantity totals are explainable
- GBP net sales totals are within tolerance of legacy exports
- royalty totals are within tolerance of legacy exports
- final output file count matches expected config count

### Exceptions handling
Always generate separate exception files for:
- missing brand/property bridge
- unknown SKU rewrite
- unknown description mapping
- missing rate
- missing territory mapping
- zero-value sales rows

---

## Parity Testing SOP

### Objective
Prove the new automated flow reproduces the old reporting outputs before replacing the legacy process.

### Test order
1. choose one license first — recommended: NHL
2. obtain three artifacts for the same date range:
   - legacy input/export CSV
   - config JSON used by converter
   - final expected output file
3. run the new automated batch on the same period
4. compare:
   - row counts
   - quantity totals
   - GBP totals
   - royalty totals
   - final transformed SKU values
   - final transformed description values
   - territory assignments

### Acceptance rule
Do not promote to production until parity is acceptable on at least one live license and then at least 2–3 additional structurally different licensors.

---

## Risks, Gaps, and Open Questions

### Known risks
1. **Fragmented legacy logic**
   - logic is split across PHP, BigQuery SQL, master tables, JSON configs, and reference CSVs

2. **SKU rewrite complexity**
   - licensor-facing reporting SKU is not the same as internal SKU logic

3. **Description rewrite complexity**
   - descriptions may depend on legacy hardcoded arrays and product/title context

4. **Exchange-rate inconsistencies**
   - legacy vs newer logic may differ if rates are selected differently by date

5. **Unit-rate ambiguity**
   - legacy PHP showed unusual unit-royalty behavior in one area; needs validation with a real sample before replication

6. **Channel naming inconsistency**
   - sites/marketplaces are not standardized in raw data and must be normalized

7. **Country normalization noise**
   - e.g. `USA`, `United States`, `United States Of America`

### Open questions
- what is the exact interface/CLI contract of the current converter app?
- where are the active JSON config files stored now?
- which licenses already have stable config coverage?
- which reference SKU files are mandatory for output correctness?
- what is the preferred final runtime: local script, web app, or cron-driven batch job?

---

## Phased Rollout Recommendation

### Phase 1 — Operational batch MVP
Goal:
- one-click batch generation using legacy-format export + existing converter

Deliverables:
- date-range runner
- extractor script
- normalized export file
- batch converter wrapper
- output bundle folder structure
- validation summary

### Phase 2 — Rule externalization
Goal:
- move royalty logic into durable tables/config under Supabase/BigQuery

Deliverables:
- externalized rate tables
- externalized exchange-rate tables
- externalized territory mappings
- externalized SKU rewrite rules
- externalized description rewrite rules
- externalized exclusion rules

### Phase 3 — Production portal
Goal:
- simple user interface with run history and downloadable outputs

Deliverables:
- UI for date-range batch runs
- run logs
- exceptions dashboard
- approval/export workflow if needed

---

## Immediate next actions
1. Confirm the correct location/access method for the converter app and config files.
2. Pick NHL as parity-test license.
3. Collect the parity set:
   - source export
   - converter config JSON
   - expected final output
4. Build the extractor wrapper first.
5. Run one full NHL batch and compare output against legacy.
6. Only then expand to additional licenses.
