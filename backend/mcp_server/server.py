import os
import sys

# Add parent directory to path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from mcp.server.fastmcp import FastMCP
from backend.integrations.siliconflow import generate_image_flux, generate_video_wan
from backend.utils import generate_ugc_script_breakdown
from backend.integrations.audio_service import generate_voice
import json

# Initialize FastMCP Server
mcp = FastMCP("VideoGenerationMCP")

@mcp.tool()
def generate_image(prompt: str, output_dir: str = "./generated_images") -> str:
    """
    Generate a high-quality image using FLUX model.
    
    Args:
        prompt: Detailed description of the image to generate.
        output_dir: Directory to save the image (default: ./generated_images).
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"flux_{int(os.times()[4])}.png" # simplistic timestamp
    output_path = os.path.join(output_dir, filename)
    
    result_path = generate_image_flux(prompt, output_path)
    
    if result_path:
        return f"Image generated successfully: {result_path}"
    else:
        return "Failed to generate image."

@mcp.tool()
def generate_video(image_path: str, prompt: str, output_dir: str = "./generated_videos") -> str:
    """
    Generate a video from an image using Wan2.1 model.
    
    Args:
        image_path: Path to the source image to animate.
        prompt: Description of the motion/scene.
        output_dir: Directory to save the video (default: ./generated_videos).
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"wan_{int(os.times()[4])}.mp4"
    output_path = os.path.join(output_dir, filename)
    
    result_path = generate_video_wan(image_path, prompt, output_path)
    
    if result_path:
        return f"Video generated successfully: {result_path}"
    else:
        return "Failed to generate video."

@mcp.tool()
def generate_script(idea: str, niche: str, tone: str, platform: str, length: int, model: str = "groq") -> str:
    """
    Generate a high-quality video script using Advanced LLMs (DeepSeek/Qwen).
    
    Args:
        idea: Core product or video idea.
        niche: Target audience.
        tone: Desired tone (e.g., energetic, professional).
        platform: Target platform (tiktok, instagram).
        length: Desired duration in seconds.
        model: 'siliconflow' (for DeepSeek) or 'groq'.
    """
    try:
        result = generate_ugc_script_breakdown(
            idea=idea, 
            niche=niche, 
            tone=tone, 
            platform=platform, 
            length=length, 
            model_provider=model
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error generating script: {str(e)}"

@mcp.tool()
def generate_voice(text: str, output_dir: str = "./generated_audio", model: str = "fish-speech-1.5") -> str:
    """
    Generate realistic voiceover using Advanced TTS models.
    
    Args:
        text: The text to be spoken.
        output_dir: Directory to save the audio file.
        model: Model to use. Options:
               - 'fish-speech-1.5' (Best Multi-lingual, API)
               - 'f5-tts' (Best Cloning, API/Local)
               - 'gpt-sovits' (Best Custom UI, Local)
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"voice_{int(os.times()[4])}.mp3"
    output_path = os.path.join(output_dir, filename)
    
    result_path = generate_voice(text, output_path, model)
    
    if result_path:
        return f"Audio generated successfully: {result_path}"
    else:
        return "Failed to generate audio (Check API Key or Local Server status)."


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
