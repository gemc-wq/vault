#!/usr/bin/env python3
"""
Gemini Nano Banana Image Generation Script
Generates lifestyle marketing images via Gemini's image generation API.
Usage: python3 gemini_image_gen.py --prompt "your prompt" --output output.png
"""

import argparse
import base64
import os
import sys

from google import genai

# Use the dedicated image analysis key or the main Gemini key
API_KEY = os.environ.get("GEMINI_API_KEY", "")

def generate_image(prompt: str, output_path: str, model: str = "imagen-4.0-generate-001"):
    """Generate an image using Gemini/Imagen and save to file."""
    client = genai.Client(api_key=API_KEY)
    
    # Try Imagen API first (dedicated image generation)
    if "imagen" in model:
        response = client.models.generate_images(
            model=model,
            prompt=prompt,
            config=genai.types.GenerateImagesConfig(
                number_of_images=1,
            ),
        )
        if response.generated_images:
            image_data = response.generated_images[0].image.image_bytes
            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"✅ Saved: {output_path} ({len(image_data)} bytes)")
            return True
        print("❌ No image generated")
        return False
    else:
        # Use Gemini multimodal model for image generation
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                with open(output_path, "wb") as f:
                    f.write(image_data)
                print(f"✅ Saved: {output_path} ({len(image_data)} bytes)")
                return True
            elif part.text is not None:
                print(f"Text response: {part.text}")
        print("❌ No image generated in response")
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate images via Gemini API")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--model", default="gemini-2.0-flash-exp", help="Model name")
    args = parser.parse_args()
    
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    
    success = generate_image(args.prompt, args.output, args.model)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
