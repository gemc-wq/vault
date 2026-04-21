import os
from PIL import Image, ImageDraw

def generate_mock_artwork(width, height, color, text):
    """Generates a simple color block with text as mock artwork."""
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)
    # Simple cross to visualize alignment
    draw.line((0, 0, width, height), fill="white", width=5)
    draw.line((0, height, width, 0), fill="white", width=5)
    return img

def build_jig_composite(config, output_path):
    """
    Composites artwork onto a production jig based on config.
    """
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
    
    # 1. Create the production canvas
    # Using a dark grey background to simulate a production tray
    composite = Image.new('RGB', (canvas_w, canvas_h), color=(50, 50, 50))
    
    # 2. Create the mock artwork to be repeated
    artwork = generate_mock_artwork(item_w, item_h, (0, 120, 215), config['f_PhoneCode'])
    
    print(f"Building jig composite for {config['f_PhoneCode']}...")
    
    count = 0
    for r in range(rows):
        for c in range(cols):
            x = start_x + (c * (item_w + margin_x))
            y = start_y + (r * (item_h + margin_y))
            
            # Boundary check before pasting
            if x + item_w <= canvas_w and y + item_h <= canvas_h:
                composite.paste(artwork, (x, y))
                count += 1
            else:
                print(f"⚠️ Warning: Item at R{r}C{c} overflows canvas at ({x}, {y})")

    # 3. Save the result
    composite.save(output_path)
    print(f"✅ Composite saved to: {output_path} ({count} items placed)")

# IPH5C Config from 2014 SQL dump
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

output_dir = "/Users/openclaw/.openclaw/workspace/projects/listing-forge/output"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "iph5c_jig_composite_poc.jpg")

if __name__ == "__main__":
    build_jig_composite(iph5c_config, output_file)
