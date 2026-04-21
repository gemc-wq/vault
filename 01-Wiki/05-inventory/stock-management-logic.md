# stock-management-logic
*Auto-created by vault compiler on 2026-04-13*

- **Inventory Traffic Light Logic**:
- **Red**: < 14 days stock
- **Amber**: < 21 days stock
- **Green**: 21+ days stock
- **Stock-out Estimation Logic**: Days cover must be calculated using a weighted average of the last 7 days and last 30 days sales (heavier weighting on the last 7 days), including a flag if daily velocity deviates materially from the baseline.
