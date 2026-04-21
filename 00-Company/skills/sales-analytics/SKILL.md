# Sales Analytics — Skill Document

> Domain: Sales reporting, metric interpretation, and data-driven decisions for Ecell Global's Amazon business.

## Reporting Hierarchy

```
Company
  -> Marketplace (US, UK, DE, FR, IT, ES)
    -> License (e.g., Naruto, Dragon Ball, One Piece)
      -> Design (content block artwork)
        -> Parent ASIN (product listing)
          -> Child ASIN / Variant (size, color, device)
```

Every metric can be sliced at any level. Default roll-up is Marketplace -> Design.

## Reporting Cadence

| Cadence  | Report                     | Source              | Owner   |
|----------|----------------------------|---------------------|---------|
| Daily    | Order count, revenue       | SP-API middleware    | Hermes  |
| Weekly   | Sales & Traffic (Business) | SP-API -> BigQuery   | Hermes  |
| Weekly   | PULSE Leaderboard          | BigQuery analysis    | Hermes  |
| Weekly   | Active Listings delta      | SP-API -> BigQuery   | Hermes  |
| Monthly  | Settlements / P&L          | SP-API + manual      | Athena  |
| Ad-hoc   | Strategy reviews           | Ava analysis         | Ava     |

## Key Metrics

| Metric          | Definition                                    | Good     | Bad      |
|-----------------|-----------------------------------------------|----------|----------|
| Revenue         | Net sales after returns                       | Growing  | Declining|
| Units           | Total units sold                              | Growing  | Declining|
| CVR             | Units / Sessions                              | >4%      | <2%      |
| Sessions        | Unique visits to listing                      | Growing  | Flat     |
| Page Views      | Total views (inc. repeat)                     | Growing  | Flat     |
| ACOS            | Ad Spend / Ad Revenue                         | <25%     | >35%     |
| ROAS            | Ad Revenue / Ad Spend (1/ACOS)                | >4x      | <2.8x   |
| CPC             | Cost per click on ads                         | <$0.50   | >$1.00   |
| Velocity        | Units/day trending (7d MA)                    | Rising   | Falling  |

## Decision Framework

| Condition                              | Action                                       |
|----------------------------------------|----------------------------------------------|
| CVR >4% on FBM listing                | Candidate for FBA migration (expect 2-3x lift)|
| ACOS >35% on >$500 spend (7d)         | Pause campaign or restructure keywords       |
| ACOS <15% on >$200 spend (7d)         | Increase budget, expand match types           |
| HB401 vs HTPCR same design            | HB401 converts ~4x higher -- prioritize       |
| Design velocity declining 3 weeks     | Check suppression, listing health, competition|
| New design, 0 sessions after 7 days   | Check indexing, keyword presence, catalog errors|
| FBA CVR lift <1.5x vs FBM             | Review pricing, images, Buy Box ownership     |

## Data Sources

| Source                    | Location                          | Access Method           |
|---------------------------|-----------------------------------|-------------------------|
| BigQuery                  | `amazon_reports` dataset          | SQL via BigQuery API    |
| SP-API Middleware         | Google Cloud Run                  | Automated report pulls  |
| Seller Central (manual)   | sellercentral.amazon.com          | CSV download            |
| OpenClaw Gateway          | localhost:18789                    | HTTP API (Hermes, etc.) |

## Agent Responsibilities

| Agent   | Role in Sales Analytics                                      |
|---------|--------------------------------------------------------------|
| Hermes  | Weekly analytics crons, PULSE generation, report automation  |
| Ava     | Strategy decisions, FBA migration calls, budget allocation   |
| Athena  | Pipeline/middleware maintenance, BigQuery schema, SP-API     |
| Zeus    | Orchestration, escalation to Cem, cross-agent coordination   |
