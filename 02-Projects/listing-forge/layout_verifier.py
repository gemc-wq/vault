import json

def calculate_jig_layout(config):
    """
    Calculates the top-left coordinates for every item in a production jig.
    
    Logic based on t_jig_measurement schema:
    - Canvas (W, H)
    - Padding (X, Y) - The initial offset from top-left of canvas to first item.
    - Grid (CountX, CountY) - Number of items across and down.
    - Item Size (PhoneWidth, PhoneHeight) - The box for the individual case.
    - PhoneMargin (X, Y) - The spacing BETWEEN items in the grid.
    """
    
    layout = []
    
    canvas_w = config['f_Width']
    canvas_h = config['f_Height']
    start_x = config['f_PaddingX']
    start_y = config['f_PaddingY']
    cols = config['f_ItemsCountX']
    rows = config['f_ItemsCountY']
    item_w = config['f_PhoneWidth']
    item_h = config['f_PhoneHeight']
    margin_x = config['f_PhoneMarginX']
    margin_y = config['f_PhoneMarginY']
    
    print(f"Jig for {config['f_PhoneCode']}: {cols}x{rows} grid on {canvas_w}x{canvas_h} canvas")
    
    for r in range(rows):
        for c in range(cols):
            # Coordinate formula:
            # X = StartPaddingX + (ColumnIndex * (ItemWidth + MarginX))
            # Y = StartPaddingY + (RowIndex * (ItemHeight + MarginY))
            x = start_x + (c * (item_w + margin_x))
            y = start_y + (r * (item_h + margin_y))
            
            layout.append({
                "row": r,
                "col": c,
                "x": x,
                "y": y,
                "w": item_w,
                "h": item_h
            })
            
    return layout

# Testing with iPhone 5C (IPH5C) values from 2014 SQL dump
iph5c_config = {
    "f_PhoneCode": "IPH5C",
    "f_Width": 7200,
    "f_Height": 4800,
    "f_PaddingX": 478,
    "f_PaddingY": 381,
    "f_ItemsCountX": 4,
    "f_ItemsCountY": 5,
    "f_PhoneWidth": 1495,
    "f_PhoneHeight": 739,
    "f_PhoneMarginX": 89,
    "f_PhoneMarginY": 87
}

layout_results = calculate_jig_layout(iph5c_config)

# Print first row and last row to verify
print("\nTop-Left (Row 0, Col 0):", layout_results[0])
print("Bottom-Right (Row 4, Col 3):", layout_results[-1])

# Boundary Check
last_item = layout_results[-1]
final_x_edge = last_item['x'] + last_item['w']
final_y_edge = last_item['y'] + last_item['h']

print(f"\nFinal Edge check:")
print(f"Right edge: {final_x_edge} (Canvas: {iph5c_config['f_Width']})")
print(f"Bottom edge: {final_y_edge} (Canvas: {iph5c_config['f_Height']})")

if final_x_edge <= iph5c_config['f_Width'] and final_y_edge <= iph5c_config['f_Height']:
    print("\n✅ LAYOUT VALID: Items fit within production canvas.")
else:
    print("\n❌ LAYOUT INVALID: Items overflow canvas boundaries.")
