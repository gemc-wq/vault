# Fulfillment Health Dashboard — Initial Data Logic

## Veeqo Ingestion
Target Endpoint: `GET https://api.veeqo.com/orders`

### Backlog Query Strategy
1. **Identify Aged Backlog:**
   - Filter: `status=awaiting_fulfillment`
   - Filter: `created_at_max=<current_time - 48h>`
   - Result: List of orders breaching North Star fulfillment targets.

2. **Regional Bottleneck Detection:**
   - Use `allocated_at=<warehouse_id>` to split Florida, UK, and PH backlogs.
   - Cross-reference with weather data (Orlando alerts).

3. **Bottleneck SKU Analysis:**
   - Aggregate line items from aged orders.
   - Rank top 20 SKUs by volume to identify stock-outs vs. workflow issues.

## Visualization Requirements (v1)
- Red/Amber/Green status by Node.
- CS Impact Projection (predicted ticket volume based on backlog size).
