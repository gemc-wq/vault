# Legacy Royalty Report Logic Extraction

## Objective
Extract the old PHP-based royalty reporting logic from Zero/barcode so it can be replicated in Supabase/BigQuery and used to feed the newer JSON-driven royalty app automatically.

## Primary Legacy Source
- `projects/zero-codebase/barcode/get_1d_sales.phpDREW042418`

## Supporting Legacy Source
- `projects/zero-codebase/barcode/royalty_report_manager.phpRON20191107`

---

## 1. Core legacy data dependencies

### Royalty master tables
The legacy manager/admin layer depends on:
- `t_royalty_information`
- `t_royalty_information_temp`
- `t_royalty_rates`

These store:
- licensor / royalty name
- property name
- reporting frequency
- payment currency
- royalty rate
- royalty rate type
- accounting type
- supplier code
- entity
- effective-date rate history

### Other lookup/data sources used by legacy reporting engine
From `get_1d_sales.phpDREW042418`:
- `SYSCountryCode` — country -> EU / non-EU classification
- `headcase.tblLineups` — lineup names
- `headcase.tblDesignProductAvailability`
- `headcase.tblDesigns` — design names
- Sage order return tables for tax/account extraction

### Sales/order source fields pulled by the report engine
Observed report row fields include:
- `Brand Name`
- `Sales Record Number`
- `Sage Order Number`
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
- `DSN`
- `Description`
- `Item Title`
- `Quantity`
- `Paid Date`
- `Royalty Rate`
- `EU-NonEU Country`
- `Total Net Sales`
- `Sage ER`
- `GBP Net Sales Amount`

---

## 2. Legacy processing flow

### Step A — classify the brand/licensor from Custom Label
The script derives a `Brand Name` by parsing `Custom_Label` and matching family/license prefixes.

Key dependency:
- `GetAllLicensedBrand()`
- `IdentifyFamilyCodeLicenseID(...)`

This is not the same as Ava’s modern SKU parsing rules. It is a royalty-report-specific licensor resolution path.

### Step B — derive base SKU + DSN
The script parses:
- `SKU`
- `DSN`
from `Custom_Label`

It then rewrites them heavily for reporting purposes.

### Step C — look up royalty rate / licensor metadata
The script calls:
- `GetLicensorInformation(...)`

This reads from `t_royalty_information` and returns fields such as:
- `f_reporting_frequency`
- `f_payment_currency`
- `f_royalty_rate`
- `f_royalty_rate_type`
- `f_supplier_code`
- `f_supplier_currency`
- `f_accounting_type`
- `f_entity`

For IMGC-style special cases, the licensor name and rate can be overridden by hardcoded `imgc_royalty_info` mappings.

### Step D — assign exchange rate
The script assigns `Sage ER` based on paid date against exchange-rate periods.

Observed behavior:
- exchange rate selected by date window
- then stored per row as `Sage ER`

### Step E — classify country as EU / non-EU
The script loads `SYSCountryCode` and maps:
- `Country` -> `EU-NonEU Country`

This is a legacy geographic reporting helper and may feed territory-based downstream outputs.

### Step F — apply exclusion rules
Observed exclusions:
- conflicting lineup blacklist (`$conflicting_lineups`)
- special Juventus user exclusion:
  - if SKU starts `JFC` and `User ID == "JUVENTUS F.C S.P.A"` then skip

### Step G — rewrite SKU for licensor reporting
This is a major logic block.

The script performs large chains of `if/elseif` SKU remapping rules, including:
- LFC-specific rewrites
- One Direction rewrites
- brand/family-specific rewrites
- custom-label-sensitive rewrites

Examples observed:
- `LFCNEW` -> `LB-LFCJERS2` or `LFCJERS2` depending on product type in custom label
- `LFCCREST` -> `H10-LFC-CREST`, `HBL-LFCCREST`, or `LFCCREST1` depending on context
- `LFCLVBRD` -> multiple royalty SKUs depending on product form
- dozens of One Direction shorthand codes rewritten into licensor-recognized SKUs

This confirms the royalty report SKU is a **licensor-facing reporting SKU**, not the internal analytics SKU.

### Step H — rewrite Description per licensor rules
This is another major logic block.

The script uses hardcoded mapping arrays and branch logic for:
- `one_direction_descriptions`
- `cosmo_img_refs`
- `twd_descriptions`
- `dean_descriptions`
- `ob_descriptions`
- `nfl_descriptions`
- `wwe_descriptions`
- `nba_descriptions`
- `preacher_descriptions`
- `imgc_royalty_info`
- `outlander_descriptions`
- `stevenbrown_descriptions`

Description resolution patterns include:
- direct lookup by rewritten SKU
- lookup by `SKU-DSN`
- substring match against `Item Title`
- `GetLineupName(old_sku)`
- `GetDesignName(old_sku-DSN)`
- IMGC-specific `royalty_code`

If no special case applies, default description becomes:
- `GetLineupName(old_sku)`

### Step I — enrich with Sage financial data
Function:
- `FillupLicenseCodesDetails($sales)`

This calls Sage and adds:
- `AC-Ref`
- `Tax`
- `Net Sales`
- `Total Net Sales`
- `GBP Net Sales Amount`

Exact formulas observed:
- `Net Sales = Price - LineTaxValue`
- `Total Net Sales = Net Sales * Quantity`
- `GBP Net Sales Amount = Total Net Sales / Sage ER`

This is the core net-sales conversion path in legacy logic.

### Step J — group and export report outputs
The report is then:
- grouped by master license (`GroupRoyaltyReport`)
- split into sheets per brand/license (`GroupByLicenseNamePerSheet`)
- further aggregated by `Description` (`GroupReportByItemDescription`)
- exported as royalty statement spreadsheets (`GenerateExcelfileDownloadReport`)
- summarized for invoice/export rows (`GetLicenseSummary`, `GetRoyaltyForInvoiceData`)

---

## 3. Legacy royalty formulas

### Net sales formulas
From `FillupLicenseCodesDetails(...)`:
- `Net Sales = Price - Tax`
- `Total Net Sales = Net Sales * Quantity`
- `GBP Net Sales Amount = Total Net Sales / Sage ER`

### Royalty formulas
From `GetLicenseSummary(...)` and `GetRoyaltyForInvoiceData(...)`:

#### Percentage-based royalty
- `Royalty = GBP Net Sales Amount * (f_royalty_rate / 100)`

#### Unit-based royalty
Observed implementation:
- `Royalty = Quantity / f_royalty_rate`

This is unusual, because modern/unit logic would normally be `Quantity * per_unit_rate`.
This should be validated carefully before replication.
It may reflect a legacy data-entry convention where `f_royalty_rate` stored units-per-currency rather than currency-per-unit.

---

## 4. Output structures in legacy engine

### Royalty statement spreadsheet columns
Observed table headers:
- `Period`
- `SKU`
- `Description`
- `Currency`
- `Units Sold`
- `Selling Price`
- `Total Price`
- `Exchange Rate`
- `Total(GBP)`
- `%`
- `Royalty`

Notes:
- output currency in statement body is normalized to GBP
- grouped rows aggregate by `Description`
- footer includes:
  - Totals Current Period
  - Totals B/F from previous period
  - Totals C/F inc this period
  - Advances
  - Payment Due

### Invoice/export rows
From `GetRoyaltyForInvoiceData(...)`, output fields include:
- `Supplier`
- `Amount`
- `Nominal Account`
- `Reference`
- `Remarks`
- `Date`
- `Sage Company`
- `Currency`
- `Reporting Frequency`
- `Accounting Type`
- `Total Quantity`
- `Royalty Rate`

This appears to be the financial/export interface for payable royalty entries.

---

## 5. Key hardcoded logic categories to externalize

### A. Licensor master metadata
Externalize from DB:
- royalty master info
- rate history
- frequency/currency/accounting/entity/supplier fields

### B. SKU remapping rules
Externalize from PHP into structured rules table/config:
- exact-match rewrites
- product-type-sensitive rewrites using `Custom Label`
- licensor-specific reporting SKU standards

### C. Description mapping rules
Externalize from PHP arrays into reference tables:
- exact SKU -> description
- SKU+DSN -> description
- title contains -> description
- lineup/design derived descriptions
- IMGC royalty-code overrides

### D. Country / territory logic
Externalize:
- country -> EU/non-EU mapping
- later licensor-specific territory mapping into JSON app layer

### E. Exchange-rate logic
Externalize:
- effective-date exchange rate table
- date-window selection logic

### F. Exclusion logic
Externalize:
- conflicting lineup blacklist
- user/brand suppression rules

---

## 6. Why this matters
The legacy royalty system is not just a query over sales plus a rate.
It is a rule engine with four distinct responsibilities:

1. licensor resolution
2. reporting SKU normalization
3. licensor-facing description normalization
4. financial normalization into GBP + royalty calculation

If only the DB tables are copied into Supabase/BQ, the automation will miss the part that makes reports acceptable to licensors.

---

## 7. Recommended replication target model

### Suggested tables
- `royalty_licenses`
- `royalty_rates`
- `royalty_exchange_rates`
- `royalty_country_classification`
- `royalty_exclusion_rules`
- `royalty_sku_rewrite_rules`
- `royalty_description_rules`
- `royalty_reference_skus`
- `royalty_report_templates`
- `royalty_channel_mappings`
- `royalty_territory_mappings`

### Suggested deterministic pipeline
`orders -> licensor resolution -> exclusions -> exchange rate lookup -> net sales normalization -> reporting SKU rewrite -> reporting description rewrite -> royalty calculation -> licensor-specific output export`

---

## 8. Most important unresolved question
**Unit royalty formula requires validation.**

Legacy implementation uses:
- `Quantity / f_royalty_rate`

That may be correct for legacy data-entry conventions, or it may be a historical quirk.
Do not replicate blindly without checking a real unit-rate licensor example.

---

## 9. Immediate next recommended task
Produce a second extraction pass that turns the legacy PHP into structured inventories:
1. all SKU rewrite rules by licensor
2. all description mapping sources by licensor
3. all financial formula dependencies and source fields
4. all required source tables / joins for a Supabase implementation
