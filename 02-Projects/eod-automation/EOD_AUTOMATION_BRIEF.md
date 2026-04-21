# EOD Analysis Automation — Project Brief
*Author: Ava | Date: 2026-03-08 | Status: BRIEF*

## Problem
- 38 PH staff submit daily EOD reports across 3 Slack channels (#eod-creative-graphics, #eod-listings, #eod)
- Reports are unstructured text — varying formats, inconsistent detail levels
- Currently: Nobody consistently reads/analyzes them → missed patterns, no accountability metrics
- Cem and Bea (PH Creative Manager) have no aggregated view of daily output across teams

## Goal
Automated daily digest that extracts structured data from EOD Slack messages and produces:
1. **Daily summary** — who reported, who didn't, total output by team
2. **Production metrics** — SKUs created/updated, brands worked on, device types covered
3. **Trend tracking** — weekly/monthly output trends per person and team
4. **Alert flags** — missing EODs, declining output, unusual patterns

## Data Sources

### Slack Channels (already connected via Bot Token)
| Channel | ID | Team | Typical Post Time (PHT) |
|---------|-----|------|------------------------|
| #eod-creative-graphics | C0AHQJK60NP | Creative + Graphics (12 staff) | 10-11 PM PHT (10-11 AM EST) |
| #eod-listings | C0AHUUGJK7G | Listings (8 staff) | 10-11 PM PHT |
| #eod | C09T8A2P2HX | General EOD (misc) | Varies |

### Staff Roster (for attendance tracking)
- Full roster at `org/ph-staff-roster.md`
- Key: Map Slack user IDs → staff names → teams

## Architecture Options

### Option A: Cron + LLM Parse (Recommended — Simple)
1. **8 AM EST cron** pulls last 24h messages from 3 channels via Slack API
2. **LLM (Flash/cheap)** parses each EOD into structured JSON:
   ```json
   {
     "staff_name": "Danica Matias",
     "team": "Graphics",
     "date": "2026-03-06",
     "items": [
       {"type": "asset_creation", "brand": "NBA", "product_types": ["BC","HB4","HB1"], "sku_count": null},
       {"type": "asset_creation", "brand": "WWE", "product_types": ["BC","HB4","HB1"], "sku_count": null}
     ],
     "raw_text": "..."
   }
   ```
3. **Store** in Supabase table `eod_reports` (or local JSON for MVP)
4. **Generate digest** → send to Cem via Telegram/Signal

### Option B: n8n Workflow
- Use existing n8n instance (https://n8n.ecellglobal.com)
- Slack trigger → LLM node → Supabase insert → Telegram notification
- More robust but higher setup effort

### Option C: OpenClaw Heartbeat (Current — Manual)
- What we do now: Ava reads Slack in heartbeat, summarizes manually
- Not scalable, burns Opus tokens, inconsistent

## Recommended: Option A (Cron + Flash)
- **Phase 1 (MVP):** Script that pulls Slack → parses with Gemini Flash → writes daily markdown to `memory/eod/YYYY-MM-DD.md`
- **Phase 2:** Add Supabase storage + trend dashboards
- **Phase 3:** Integrate into n8n for full automation

## Schema: `eod_reports` (Phase 2)

```sql
CREATE TABLE eod_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  staff_name TEXT NOT NULL,
  slack_user_id TEXT,
  team TEXT NOT NULL,  -- 'creative', 'graphics', 'listings', 'production', 'cs'
  report_date DATE NOT NULL,
  brands_worked TEXT[],  -- ['NBA', 'WWE', 'Arsenal']
  product_types TEXT[],  -- ['BC', 'HB4', 'HLBWH', 'HDMWH']
  sku_count INT,
  activity_type TEXT,  -- 'creation', 'replication', 'QA', 'title_checking', 'other'
  summary TEXT,
  raw_message TEXT,
  slack_ts TEXT,
  parsed_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(slack_user_id, report_date, slack_ts)
);
```

## EOD Patterns Observed (from Mar 6 sample)

### Creative Team Format (Nesley, Nina):
- Starts with "Creative Team EOD — [Name] — [Date]"
- Sections: TECHNICAL (Title Checking), then brand × product type × SKU count
- Example: "BC, HB1, HB4 • NBA – 28 SKUs"

### Graphics Team Format (Danica, Jay V.):
- Starts with "Graphics Team EOD — [Name] — [Date]"
- Sections: Technical → brand/product type descriptions
- Less structured, more narrative

### Listings Team Format (Chadle, Mariela, Patricia, Evita):
- Starts with "Listing Team EOD — [Name] — [Date]"
- More varied — includes database updates, shipping templates, discontinued items
- Mariela: device database updates (iPhone 17 for Rakuten)
- Patricia: listing rules, brand exclusions, Geon production

## Parsing Strategy
- **Step 1:** Regex extract name + date from header line
- **Step 2:** LLM extract brands, product types, SKU counts, activity types
- **Step 3:** Validate against known brand list and product type codes
- **Known product types:** BC, HB1, HB4, HTPCR, HLBWH, HDMWH, HC, H89 (gaming skins)
- **Known brands:** NBA, NFL, WWE, Arsenal, Peanuts, Harry Potter, Naruto, Dragon Ball Z, Hatsune Miku, Billie Eilish, England Rugby, etc.

## Effort Estimate
| Phase | Effort | Owner | Timeline |
|-------|--------|-------|----------|
| Phase 1 (MVP script) | 2-3 hours | Forge (Codex) | 1 day |
| Phase 2 (Supabase + trends) | 4-6 hours | Forge | 3 days |
| Phase 3 (n8n integration) | 2-3 hours | Harry/Forge | 1 week |

## Success Metrics
- 100% of EODs captured and parsed within 1 hour of posting
- Weekly output trends visible per staff member
- Missing EOD alerts sent same-day
- Cem gets daily digest by 9 AM EST without reading Slack

## Dependencies
- ✅ Slack Bot Token (connected)
- ✅ Channel access (joined #eod-creative-graphics, #eod-listings)
- ✅ Staff roster → Slack user ID mapping — built at `org/slack-user-map.md` (includes JSON export for script consumption)
- ⚠️ Supabase table creation (Phase 2)

## Next Steps
1. ~~Build Slack user ID → staff name mapping~~ ✅ DONE — `org/slack-user-map.md`
2. Spawn Forge to build MVP parsing script (Phase 1)
3. Test on last 7 days of EOD data
4. Verify uncertain Slack mappings (Anthony=Tony?, Ric=Ricardo?) with Cem or Bea
