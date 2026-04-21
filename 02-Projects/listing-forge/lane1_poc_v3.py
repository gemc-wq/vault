import os
from PIL import Image, ImageDraw, ImageFilter

def add_rounded_corners(im, radius):
    """Apply rounded corners to a PIL image."""
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    
    # Draw the 4 corners
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    
    im.putalpha(alpha)
    return im

def process_smart_object(image_path, output_path, rotation_angle=0, corner_radius=0):
    """
    Process an artwork image:
    1. Open image
    2. Apply rotation (if f_ImageRotation is specified)
    3. Apply rounded corners (if f_CornerRadius is specified)
    4. Save output
    """
    try:
        if not os.path.exists(image_path):
            print(f"File not found: {image_path}. Using blank canvas for POC.")
            im = Image.new('RGB', (1000, 2000), color=(200, 200, 200))
        else:
            im = Image.open(image_path).convert("RGBA")
            
        # 1. Apply Rotation
        if rotation_angle != 0:
            print(f"Applying rotation: {rotation_angle} degrees")
            # expand=True keeps the whole image after rotation
            im = im.rotate(rotation_angle, resample=Image.BICUBIC, expand=True)
            
        # 2. Apply Corner Radius
        if corner_radius > 0:
            print(f"Applying corner radius: {corner_radius}px")
            im = add_rounded_corners(im, corner_radius)
            
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        im.save(output_path, "PNG")
        print(f"Successfully saved processed image to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

if __name__ == "__main__":
    # Test values based on t_jig_measurement schema
    sample_input = "sample_artwork.jpg"
    sample_output = "output/v3_processed_artwork.png"
    
    # f_ImageRotation and f_CornerRadius from DB
    test_rotation = 90
    test_radius = 45
    
    print("Starting Lane 1 POC v3 (Rotation & Corner Radius)")
    process_smart_object(sample_input, sample_output, rotation_angle=test_rotation, corner_radius=test_radius)
