# inventory traffic light logic
*Auto-created by vault compiler on 2026-04-13*

- Inventory status thresholds:
- **BLACK**: `free_stocks` = 0
- **RED**: `days_of_stock` < 14
- **YELLOW**: `days_of_stock` < 21
- **GREEN**: `days_of_stock` >= 21
