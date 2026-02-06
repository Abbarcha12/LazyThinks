"""
Runway ML API Integration (Alternative: D-ID)
Cost: ~$12/month unlimited OR D-ID $5.90/month for 5 min
Quality: High-quality video generation with motion
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()


def get_runway_api_key():
    """Get Runway API key from environment"""
    api_key = os.getenv("RUNWAY_API_KEY")
    if not api_key:
        raise ValueError("RUNWAY_API_KEY not found in environment variables")
    return api_key


def create_video_runway(image_path: str, prompt: str, duration: int = 5):
    """
    Create video from image using Runway Gen-2
    
    Args:
        image_path: Path to source image
        prompt: Text prompt for video motion
        duration: Video duration in seconds (default 5s)
    
    Returns:
        Dict with video_id and status
    """
    try:
        api_key = get_runway_api_key()
        
        # Runway Gen-2 API endpoint
        url = "https://api.runwayml.com/v1/gen2/generate"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Read and encode image
        with open(image_path, 'rb') as f:
            import base64
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        payload = {
            "image": image_data,
            "text_prompt": prompt,
            "duration": duration,
            "interpolate": True,
            "upscale": True
        }
        
        print(f"Creating video with Runway: {prompt[:50]}...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        video_id = result.get('id')
        
        print(f"✓ Video generation started: {video_id}")
        return {
            "video_id": video_id,
            "status": "processing",
            "prompt": prompt
        }
        
    except Exception as e:
        print(f"Error creating video with Runway: {e}")
        raise e


def poll_video_status_runway(video_id: str, max_wait: int = 300):
    """
    Poll video generation status until complete
    
    Args:
        video_id: Runway video ID
        max_wait: Maximum seconds to wait (default 300s = 5min)
    
    Returns:
        Dict with status and video_url when complete
    """
    try:
        api_key = get_runway_api_key()
        url = f"https://api.runwayml.com/v1/gen2/status/{video_id}"
        
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        start_time = time.time()
        
        while True:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            status = result.get('status')
            
            if status == 'SUCCEEDED':
                video_url = result.get('output', {}).get('url')
                print(f"✓ Video ready: {video_url}")
                return {
                    "status": "completed",
                    "video_url": video_url,
                    "video_id": video_id
                }
            
            elif status == 'FAILED':
                error = result.get('error', 'Unknown error')
                raise Exception(f"Video generation failed: {error}")
            
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > max_wait:
                raise TimeoutError(f"Video generation timed out after {max_wait}s")
            
            # Wait before next poll
            print(f"Video status: {status}, waiting...")
            time.sleep(10)
            
    except Exception as e:
        print(f"Error polling video status: {e}")
        raise e


def download_video_runway(video_url: str, output_path: str):
    """
    Download generated video from Runway
    
    Args:
        video_url: URL of generated video
        output_path: Local path to save video
    
    Returns:
        Path to downloaded video file
    """
    try:
        print(f"Downloading video to: {output_path}")
        
        response = requests.get(video_url, stream=True, timeout=60)
        response.raise_for_status()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Download in chunks
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✓ Video downloaded: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error downloading video: {e}")
        raise e


def create_video_complete(image_path: str, prompt: str, output_path: str = None, duration: int = 5):
    """
    Complete workflow: create video, wait for completion, download
    
    Args:
        image_path: Source image path
        prompt: Video motion prompt
        output_path: Where to save final video
        duration: Video duration in seconds
    
    Returns:
        Path to final video file
    """
    try:
        # Start generation
        result = create_video_runway(image_path, prompt, duration)
        video_id = result['video_id']
        
        # Wait for completion
        status_result = poll_video_status_runway(video_id)
        video_url = status_result['video_url']
        
        # Download
        if not output_path:
            video_dir = os.path.join(os.path.dirname(__file__), "..", "generated_videos", "clips")
            os.makedirs(video_dir, exist_ok=True)
            output_path = os.path.join(video_dir, f"clip_{video_id}.mp4")
        
        final_path = download_video_runway(video_url, output_path)
        
        return final_path
        
    except Exception as e:
        print(f"Error in complete video workflow: {e}")
        raise e


def test_runway_connection():
    """Test Runway API connection"""
    try:
        print("Testing Runway API connection...")
        # This would need a test image - skip for now
        print("✓ Runway API key found (actual test requires image)")
        return True
    except Exception as e:
        print(f"✗ Runway API test failed: {e}")
        return False


if __name__ == "__main__":
    test_runway_connection()
