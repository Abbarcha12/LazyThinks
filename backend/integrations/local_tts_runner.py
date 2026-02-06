import requests
from typing import Optional

def generate_audio_local(text: str, output_path: str, model: str = "gpt-sovits", reference_audio: str = None) -> Optional[str]:
    """
    Generate audio using a locally running TTS server.
    
    Expected Local Ports:
    - GPT-SoVITS: 9880 (default)
    - ChatTTS: 5000 (common default for flask wrappers)
    """
    print(f"🎤 Generating local audio ({model})...")
    
    try:
        if "gpt-sovits" in model.lower():
            # Standard GPT-SoVITS API call (simplified)
            url = "http://127.0.0.1:9880"
            payload = {
                "text": text,
                "text_algo": "all_zh", # or auto
                "character": "default"
            }
            # Note: Real GPT-SoVITS often uses GET / POST with query params or specific endpoints
            # This is a placeholder structure
            # response = requests.post(f"{url}/tts", json=payload)
            print("⚠ Local GPT-SoVITS not connected (Requires running server at port 9880)")
            return None

        elif "chat-tts" in model.lower():
             # Placeholder for ChatTTS
             print("⚠ Local ChatTTS not connected")
             return None

    except Exception as e:
        print(f"⚠ Local TTS Error: {e}")
        
    return None
