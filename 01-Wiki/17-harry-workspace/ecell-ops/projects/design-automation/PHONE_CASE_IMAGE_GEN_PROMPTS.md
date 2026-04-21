# Phone Case Image Gen Prompts
> Source: Notion page "Prompts for phone case image gen" (Cem, Feb 7-8 2026)
> Notion URL: https://www.notion.so/Prompts-for-phone-case-image-gen-3006887b1dd780a7bd8cff227bd8feb1

---

## General Shot Direction

Create different angled views. Hero Angle: A 30° isometric turn that showcases the back design, the raised camera protection lip, and the side button tactile profile. Perspective is as phone standing up on. Create multiple shots as to rotate around the case 360 degrees, but at 45 degree intervals.

High-Key Lighting: Studio-grade softbox lighting ensures the material texture is visible while providing professional depth.

---

## ChatGPT → Firefly Prompt

Apply the provided 2D Naruto Shippuden spiral / sun emblem artwork flat to the inside back of the clear case, centered and correctly scaled. The artwork is printed, not embossed, and clearly visible through the case.

Camera angle is straight-on rear view. Product is perfectly centered.

Background is pure white with no texture or gradient. Lighting is soft, even studio lighting with a minimal shadow under the phone.

No text, no badges, no props, no hands, no reflections obscuring the design. Clean, sharp, high-resolution commercial product photography suitable for Amazon main image.

---

## Gemini Image Prompt

**Subject:** Samsung S25 Ultra clear case fitted on device, featuring Naruto 'Sun Seal' design centered on back plate below camera module.
**Angle:** 30-degree isometric turn showing back design, side button profile, and raised camera protection lip.
**Orientation:** Phone standing vertically upright.
**Lighting:** Professional studio softbox high-key, pure white background (RGB 255,255,255), soft contact shadow on floor.
**Details:** Sharp focus on the orange spiral logo and the crystal clear TPU bumper edges.
**Tech Specs:** 8k resolution, photorealistic, ray-traced, unreal engine 5 style, large format ready.

---

## Gemini Video Prompt (360° Rotation)

Generate these 8 images in sequence. The lighting and phone position must remain *identical* except for the rotation.

- **Frame 1 (0° - Front):** "Front view of Samsung S25 Ultra with clear case, screen off (black), standing upright. Studio lighting, white background."
- **Frame 2 (45° - Front Right):** "45-degree isometric view, phone standing upright, showing screen and right side buttons."
- **Frame 3 (90° - Right Side):** "90-degree side profile view, phone standing upright, focusing on button tactile profile and slim case thickness."
- **Frame 4 (135° - Back Right - HERO):** "135-degree rear isometric view, phone standing upright, showcasing the back Naruto design and camera protection lip."
- **Frame 5 (180° - Back):** "Straight-on back view, phone standing upright, full view of Naruto design centered below cameras."
- **Frame 6 (225° - Back Left):** "225-degree rear isometric view, phone standing upright, showing left side bumper and back design."
- **Frame 7 (270° - Left Side):** "90-degree left side profile view, phone standing upright, smooth TPU texture."
- **Frame 8 (315° - Front Left):** "315-degree front isometric view, phone standing upright, showing screen and left bumper edge."

---

## Python Stitcher (frames → GIF/MP4)

```python
import imageio
import os

def create_360_rotation_video(image_folder, output_file, fps=8):
    """
    Stitches a sequence of images into a rotating video/GIF.
    Assumes images are named 'frame_001.png', 'frame_002.png', etc.
    """
    images = []
    filenames = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
    
    for filename in filenames:
        images.append(imageio.imread(os.path.join(image_folder, filename)))
    
    imageio.mimsave(output_file, images, fps=fps, loop=0)
    print(f"Video saved to {output_file}")

# Usage:
# create_360_rotation_video('path/to/rendered_frames', 's25_ultra_360_view.gif')
```
