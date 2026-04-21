# EOD Automation MVP

Node.js MVP that fetches Slack EOD messages, parses them with regex/string rules, and generates a daily markdown digest plus raw JSON.

## Requirements

- Node.js 18+
- `SLACK_BOT_TOKEN` with access to:
  - `#eod-creative-graphics` (`C0AHQJK60NP`)
  - `#eod-listings` (`C0AHUUGJK7G`)
  - `#eod` (`C09T8A2P2HX`)

## Install

```bash
npm install
```

## Usage

Default behavior parses yesterday in the local machine timezone:

```bash
export SLACK_BOT_TOKEN=xoxb-...
node src/eod-parser.js
```

Parse a specific day:

```bash
node src/eod-parser.js --date 2026-03-07
```

Preview output without writing files:

```bash
node src/eod-parser.js --date 2026-03-07 --dry-run
```

## Output

Writes to `output/`:

- `output/YYYY-MM-DD-eod-digest.md`
- `output/YYYY-MM-DD-eod-raw.json`

`--dry-run` prints both payloads to stdout instead.

## Parsing Rules

- Staff name and team come from `slack-user-map.json`, with header-based name extraction as a fallback.
- Date comes from an ISO or month-name date in the message header, otherwise the Slack timestamp date.
- Brands and product types are matched from known lists.
- SKU counts use nearby numeric heuristics around `SKU`, brand names, and product type codes.
- Activity type is inferred from keywords for `creation`, `replication`, `QA`, `title_checking`, `shipping`, and `database_update`.
- Unknown Slack users are preserved as `Unknown (<user_id>)`.

## Notes

- This MVP only uses deterministic parsing. No LLM calls are made.
- Multi-line EODs are supported because the raw Slack message text is parsed as a single block.
- If there are no messages for the selected date, the digest still renders attendance and missing-report sections.
