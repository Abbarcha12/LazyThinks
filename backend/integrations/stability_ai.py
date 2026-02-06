"""
Stability AI (Stable Diffusion) Integration
Cost: ~$0.002 per image (512x512)
Quality: High-quality, consistent style
"""

import os
import io
import time
import requests
import base64

def generate_image_stable_diffusion(prompt: str, output_path: str = None, width: int = 1344, height: int = 768, samples: int = 1):
    """
    Generate image(s) using Stable Diffusion XL via REST API
    
    Args:
        prompt: Text prompt for image generation
        output_path: Base path to save image (PNG). If samples > 1, suffixes will be added.
        width: Image width (default 1344 for 16:9)
        height: Image height (default 768 for 16:9)
        samples: Number of images to generate (default 1)
    
    Returns:
        List of paths to generated image files
    """
    try:
        api_key = os.getenv("STABILITY_API_KEY")
        if not api_key:
            raise ValueError("STABILITY_API_KEY not found in environment variables")
            
        api_host = os.getenv('API_HOST', 'https://api.stability.ai')
        engine_id = "stable-diffusion-xl-1024-v1-0"
        
        # Determine output directory and base filename
        if not output_path:
            image_dir = os.path.join(os.path.dirname(__file__), "..", "generated_images")
            os.makedirs(image_dir, exist_ok=True)
            timestamp = int(time.time())
            base_filename = f"image_{timestamp}"
            output_dir = image_dir
        else:
            output_dir = os.path.dirname(output_path)
            base_filename = os.path.splitext(os.path.basename(output_path))[0]
            if not output_dir:
                 output_dir = "."
        
        print(f"Generating {samples} image(s): {prompt[:50]}...")
        
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1
                    }
                ],
                "cfg_scale": 7,
                "height": height,
                "width": width,
                "samples": samples,
                "steps": 30,
            },
        )
        
        if response.status_code != 200:
            raise Exception(f"Non-200 response: {str(response.content)}")
            
        data = response.json()
        generated_paths = []
        
        for i, image in enumerate(data["artifacts"]):
            if image["finishReason"] == 'CONTENT_FILTERED':
                print(f"⚠ Image {i+1} filtered by safety filter.")
                continue
            
            # Construct filename
            if samples > 1:
                filename = f"{base_filename}_{i+1}.png"
            else:
                filename = f"{base_filename}.png"
                
            current_output_path = os.path.join(output_dir, filename)
                
            with open(current_output_path, "wb") as f:
                f.write(base64.b64decode(image["base64"]))
                print(f"✓ Image generated: {current_output_path}")
                generated_paths.append(current_output_path)
                
        if not generated_paths:
            raise Exception("No images generated (likely filtered)")
            
        return generated_paths
        
    except Exception as e:
        print(f"Error generating image with Stability AI: {e}")
        raise e


def batch_generate_images(prompts: list, output_dir: str = None):
    """
    Generate multiple images in batch (sequential)
    
    Args:
        prompts: List of text prompts
        output_dir: Directory to save images
    
    Returns:
        List of paths to generated images
    """
    try:
        if not output_dir:
            output_dir = os.path.join(os.path.dirname(__file__), "..", "generated_images")
        
        os.makedirs(output_dir, exist_ok=True)
        
        image_paths = []
        for idx, prompt in enumerate(prompts):
            print(f"Generating image {idx+1}/{len(prompts)}...")
            
            output_path = os.path.join(output_dir, f"shot_{idx+1}_{int(time.time())}.png")
            
            try:
                paths = generate_image_stable_diffusion(prompt, output_path)
                image_paths.extend(paths)
                
                # Small delay to avoid rate limits
                time.sleep(1)
                
            except Exception as e:
                print(f"Failed to generate image {idx+1}: {e}")
                # Create placeholder image on failure
                placeholder_path = create_placeholder_image(output_path, f"Shot {idx+1}")
                image_paths.append(placeholder_path)
        
        print(f"✓ Batch generation complete: {len(image_paths)} images")
        return image_paths
        
    except Exception as e:
        print(f"Error in batch generation: {e}")
        raise e


def create_placeholder_image(output_path: str, text: str = "Placeholder"):
    """Create a simple placeholder image when generation fails"""
    from PIL import Image, ImageDraw, ImageFont
    
    # Create black image
    img = Image.new('RGB', (1024, 1024), color='black')
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center text
    x = (1024 - text_width) // 2
    y = (1024 - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    img.save(output_path)
    print(f"Created placeholder image: {output_path}")
    return output_path


def enhance_prompt_for_ugc(base_prompt: str, shot_type: str = "ugc"):
    """
    Enhance prompts for UGC-style authentic images
    
    Args:
        base_prompt: Original prompt from script
        shot_type: Type of shot (hook, problem, solution, etc.)
    
    Returns:
        Enhanced prompt optimized for Stable Diffusion
    """
    # Add UGC-specific style modifiers
    style_suffix = ", authentic UGC style, natural lighting, smartphone camera quality, realistic, casual setting, relatable, not overly polished"
    
    # Add quality boosters
    quality_suffix = ", high quality, detailed, sharp focus"
    
    enhanced = base_prompt + style_suffix + quality_suffix
    
    return enhanced


def test_stability_connection():
    """Test Stability AI connection and generate sample image"""
    try:
        print("Testing Stability AI connection...")
        test_prompt = "A person holding a smartphone, taking a selfie, natural lighting, casual UGC style"
        
        output_path = generate_image_stable_diffusion(test_prompt)
        print(f"✓ Test successful! Image saved to: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Stability AI test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the module
    test_stability_connection()
