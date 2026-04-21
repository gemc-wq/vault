# Fulfillment Health Dashboard — Draft Spec

## Purpose
Triage the Florida fulfillment backlog ("mess") and monitor global fulfillment speed vs. North Star target (<48 hours).

## Data Requirements
- Veeqo Order Export (CSV/API)
- Carrier Status (USPS/FedEx/Evri)
- Customer Service (CS) Ticket Volume (from Analiza Peralta)

## Key Metrics
- **Aged Backlog:** Orders > 48h since payment without shipping label.
- **Node Health:** Breakdown of delays by warehouse (FL vs. UK vs. PH).
- **Weather Impact:** Delayed pick-ups in Orlando zip codes.
- **CS Burn:** Correlation between fulfillment delays and "Where is my order?" tickets.

## Action Plan
1. Ingest Veeqo "Awaiting Fulfillment" logs.
2. Cross-reference with Orlando weather alerts.
3. Identify top 10 bottleneck SKUs (stock outs vs. processing delays).
