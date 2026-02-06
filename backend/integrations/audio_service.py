import os
from typing import Optional
from backend.integrations.siliconflow import generate_audio_siliconflow

# Fallback/Local dummy runner import (will be created next)
# from backend.integrations.local_tts_runner import generate_audio_local

def generate_voice(text: str, output_path: str, model: str = "fish-speech-1.5", reference_audio: str = None) -> Optional[str]:
    """
    Unified entry point for voice generation.
    Routes to appropriate provider based on model name.
    
    Supported Models:
    - fish-speech-1.5 (SiliconFlow/Fish API)
    - f5-tts (SiliconFlow or Local)
    - gpt-sovits (Local - typical port 9880)
    - chat-tts (Local)
    - parler-tts (Local)
    """
    
    # 1. SiliconFlow / API Models
    if "fish" in model.lower() or "f5" in model.lower():
        # Prefer API for heavy models if key exists
        if os.getenv("SILICONFLOW_API_KEY"):
            return generate_audio_siliconflow(text, output_path, model, reference_audio)
        else:
            print("⚠ SILICONFLOW_API_KEY missing, trying local fallback...")
            
    # 2. Local Models (GPT-SoVITS, ChatTTS, Parler)
    # This logic assumes a local service is running or a local python script runner
    try:
        from backend.integrations.local_tts_runner import generate_audio_local
        return generate_audio_local(text, output_path, model, reference_audio)
    except ImportError:
         print("⚠ Local TTS runner not found.")
    except Exception as e:
        print(f"⚠ Local TTS failed: {e}")

    return None
