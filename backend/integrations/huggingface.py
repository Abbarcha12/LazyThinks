import os
import requests
import time
import base64
from typing import List, Optional
from PIL import Image, ImageDraw

# Supported Models
IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
VIDEO_MODEL = "stabilityai/stable-video-diffusion-img2vid-xt"  # SVD 1.1

def get_headers():
    token = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        raise ValueError("Hugging Face API token not found. Please set HUGGINGFACE_API_KEY in .env")
    return {"Authorization": f"Bearer {token}"}

def generate_image_hf(prompt: str, output_path: str, negative_prompt: str = "") -> str:
    """
    Generate an image using Hugging Face Inference API (SDXL).
    """
    api_url = f"https://api-inference.huggingface.co/models/{IMAGE_MODEL}"
    headers = get_headers()
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": negative_prompt or "blurry, low quality, distorted, ugly, bad anatomy",
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "width": 1024,
            "height": 1024
        }
    }

    print(f"🎨 Generating image with HF ({IMAGE_MODEL}): {prompt[:50]}...")
    
    # Retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"✓ Image saved to {output_path}")
                return output_path
            
            elif "estimated_time" in response.json():
                wait_time = response.json().get("estimated_time", 10)
                print(f"⏳ Model loading, waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
                continue
                
            else:
                print(f"⚠ HF API Error ({response.status_code}): {response.text}")
                if attempt == max_retries - 1:
                    raise Exception(f"HF API Error: {response.text}")
                    
        except Exception as e:
            print(f"⚠ Error on attempt {attempt+1}: {e}")
            if attempt == max_retries - 1:
                raise e
            time.sleep(2)
            
    return None

def create_placeholder_image(output_path: str, text: str = "Image Gen Failed"):
    """Create a simple placeholder image using PIL"""
    try:
        img = Image.new('RGB', (1024, 1024), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        # simplistic text drawing
        d.text((50, 500), text, fill=(255, 255, 255))
        img.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error creating placeholder: {e}")
        return None

def batch_generate_images_hf(prompts: List[str], output_dir: str) -> List[str]:
    """
    Generate multiple images in batch with fallback and delays.
    """
    image_paths = []
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for i, prompt in enumerate(prompts):
        if i > 0:
            time.sleep(5) # Delay for rate limits
            
        output_path = os.path.join(output_dir, f"image_{i+1}.png")
        try:
            path = generate_image_hf(prompt, output_path)
            if path:
                image_paths.append(path)
            else:
                print(f"⚠ Failed to generate image for prompt: {prompt[:30]}. Using fallback.")
                placeholder = create_placeholder_image(output_path, f"Scene {i+1}")
                image_paths.append(placeholder)
        except Exception as e:
            print(f"⚠ Error generating image {i+1}: {e}. Using fallback.")
            placeholder = create_placeholder_image(output_path, f"Scene {i+1}")
            image_paths.append(placeholder)
            
    # Return all paths (including placeholders)
    return [p for p in image_paths if p]

def generate_video_hf(image_path: str, output_path: str) -> str:
    """
    Generate a video from an image using SVD via HF Inference API.
    Note: SVD API usually expects an image input.
    """
    api_url = f"https://api-inference.huggingface.co/models/{VIDEO_MODEL}"
    headers = get_headers()
    
    # Read image as bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    print(f"🎥 Generating video with HF SVD...")
    
    # Basic binary upload for SVD usually
    # But often HF API for SVD might not be standard 'inputs' json if inputs is an image
    # Let's try standard resize/base64 if needed, but direct binary often works for img2vid
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, headers=headers, data=image_bytes)
            
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"✓ Video saved to {output_path}")
                return output_path
                
            elif "estimated_time" in response.json():
                wait_time = response.json().get("estimated_time", 20)
                print(f"⏳ Model loading, waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
                continue
                
            else:
                print(f"⚠ HF API Error ({response.status_code}): {response.text}")
                if attempt == max_retries - 1:
                    raise Exception(f"HF API Error: {response.text}")
                    
        except Exception as e:
            print(f"⚠ Error on attempt {attempt+1}: {e}")
            if attempt == max_retries - 1:
                raise e
            time.sleep(5)
            
    return None
