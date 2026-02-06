import os
import time
import requests
from typing import Optional, Dict, Any

def get_siliconflow_headers() -> Dict[str, str]:
    """Get SiliconFlow API headers with API Key from environment"""
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if not api_key:
        raise ValueError("SILICONFLOW_API_KEY not found in environment variables")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

def generate_image_flux(prompt: str, output_path: str, model: str = "flux-pro") -> Optional[str]:
    """
    Generate an image using the FLUX model via SiliconFlow API.
    
    Args:
        prompt: The text prompt for generation.
        output_path: Local path to save the generated image.
        model: Model identifier (e.g., 'flux-pro', 'flux-dev')
    
    Returns:
        Path to the saved image file, or None if failed.
    """
    # NOTE: Adjust endpoint and payload format according to actual SiliconFlow documentation
    url = "https://api.siliconflow.cn/v1/images/generations"  # Example endpoint
    
    payload = {
        "model": model,
        "prompt": prompt,
        "image_size": "1024x1024",
        "num_inference_steps": 25
    }
    
    print(f"🎨 Generating image with SiliconFlow FLUX ({model}): {prompt[:50]}...")
    
    try:
        response = requests.post(url, headers=get_siliconflow_headers(), json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            # Assuming standard OpenAI-compatible image response structure often used by these providers
            # {"data": [{"url": "..."}]}
            image_url = result.get('data', [{}])[0].get('url')
            
            if image_url:
                img_data = requests.get(image_url).content
                with open(output_path, 'wb') as f:
                    f.write(img_data)
                print(f"✓ Image saved to {output_path}")
                return output_path
            else:
                print(f"⚠ No image URL in response: {result}")
        else:
            print(f"⚠ SiliconFlow API Error ({response.status_code}): {response.text}")
            
    except Exception as e:
        print(f"⚠ Error generating image: {e}")
        
    return None

def generate_video_wan(image_path: str, prompt: str, output_path: str, duration: int = 5) -> Optional[str]:
    """
    Generate a video using Wan2.1 model via SiliconFlow API (Image-to-Video).
    
    Args:
        image_path: Path to the source image.
        prompt: Motion/content prompt for the video.
        output_path: Local path to save the generated video.
        duration: Helper duration (though model might have fixed duration).
        
    Returns:
        Path to the saved video file, or None if failed.
    """
    url = "https://api.siliconflow.cn/v1/video/generations" # Example endpoint for video
    
    # Needs to handle file upload or base64
    # Many new APIs accept image URLs or base64
    
    try:
        # Read image to base64
        with open(image_path, "rb") as f:
            import base64
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
            
        payload = {
            "model": "wan-2.1-i2v", # Hypothetical model name
            "prompt": prompt,
            "image": f"data:image/png;base64,{img_b64}", 
            "duration": duration
        }
        
        print(f"🎥 Generating video with SiliconFlow Wan2.1: {prompt[:50]}...")
        
        headers = get_siliconflow_headers()
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            # Often video generation is async, returning a task ID
            task_id = result.get('id')
            if task_id:
                return _poll_task_status(task_id, output_path, headers)
            else:
                 # Check for direct URL
                video_url = result.get('output', {}).get('url') # Example structure
                if video_url:
                     return _download_video(video_url, output_path)

        print(f"⚠ Video generation failed or unexpected response: {response.text}")

    except Exception as e:
        print(f"⚠ Error generating video: {e}")
        
    return None

def _poll_task_status(task_id: str, output_path: str, headers: Dict[str, str]) -> Optional[str]:
    """Poll for async task completion helper"""
    url = f"https://api.siliconflow.cn/v1/tasks/{task_id}" # Example
    
    for _ in range(60): # Poll for 5-10 mins
        time.sleep(10)
        try:
             resp = requests.get(url, headers=headers)
             data = resp.json()
             status = data.get('status')
             
             if status == 'SUCCEEDED':
                 video_url = data.get('result', {}).get('url')
                 return _download_video(video_url, output_path)
             elif status == 'FAILED':
                 print(f"Task failed: {data}")
                 return None
                 
             print(f"Task status: {status}...")
        except Exception as e:
            print(f"Polling error: {e}")
            
    return None

def generate_audio_siliconflow(text: str, output_path: str, model: str = "fish-speech-1.5", reference_audio: str = None) -> Optional[str]:
    """
    Generate audio using SiliconFlow/Fish Audio API.
    
    Args:
        text: Text to speak.
        output_path: Local path to save audio.
        model: Model identifier (e.g., 'fish-speech-1.5', 'f5-tts').
        reference_audio: Path to reference audio for voice cloning (optional).
    """
    url = "https://api.siliconflow.cn/v1/audio/speech" # Example endpoint
    # Note: If separate Fish Audio API is used, URL would differ.
    
    headers = get_siliconflow_headers()
    
    payload = {
        "model": model,
        "input": text,
        "response_format": "mp3",
        "voice": "default" # or reference ID
    }
    
    if reference_audio and os.path.exists(reference_audio):
         # Handle reference audio upload/encoding for cloning
         # For simplicity in this example, we assume API accepts generic 'voice' param 
         # or we would need a separate upload step.
         pass
         
    print(f"dictation Generating audio with SiliconFlow ({model}): {text[:50]}...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✓ Audio saved to {output_path}")
            return output_path
        else:
            print(f"⚠ SiliconFlow Audio Error ({response.status_code}): {response.text}")
            
    except Exception as e:
        print(f"⚠ Error generating audio: {e}")
        
    return None

def _download_video(url: str, path: str) -> str:
    print(f"Downloading video from {url}...")
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)
    print(f"✓ Video saved to {path}")
    return path
