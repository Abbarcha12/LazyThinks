import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from dotenv import load_dotenv

load_dotenv()


def get_elevenlabs_client():
    """Initialize and return ElevenLabs client"""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
    return ElevenLabs(api_key=api_key)


def get_available_voices():
    """
    Get list of available voices from ElevenLabs
    Returns list of voices with id, name, and preview_url
    """
    try:
        client = get_elevenlabs_client()
        voices = client.voices.get_all()
        
        # Format voice data for frontend
        voice_list = []
        for voice in voices.voices:
            voice_list.append({
                "id": voice.voice_id,
                "name": voice.name,
                "category": voice.category if hasattr(voice, 'category') else "premade",
                "description": voice.description if hasattr(voice, 'description') else "",
                "labels": voice.labels if hasattr(voice, 'labels') else {}
            })
        
        return voice_list
    except Exception as e:
        print(f"Error fetching voices: {e}")
        raise e


def generate_voice_audio(text: str, voice_id: str, output_path: str = None):
    """
    Generate voice audio using ElevenLabs API
    
    Args:
        text: Text to convert to speech
        voice_id: ID of the voice to use
        output_path: Optional path to save the audio file
    
    Returns:
        Path to the saved audio file
    """
    try:
        client = get_elevenlabs_client()
        
        # Generate audio
        audio = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2"  # High quality model
        )
        
        # Save audio to file
        if not output_path:
            # Create audio directory if it doesn't exist
            audio_dir = os.path.join(os.path.dirname(__file__), "generated_audio")
            os.makedirs(audio_dir, exist_ok=True)
            
            # Generate filename
            import time
            timestamp = int(time.time())
            output_path = os.path.join(audio_dir, f"voice_{timestamp}.mp3")
        
        # Save the audio
        save(audio, output_path)
        
        return output_path
    except Exception as e:
        print(f"Error generating audio: {e}")
        raise e


def get_voice_by_id(voice_id: str):
    """Get detailed information about a specific voice"""
    try:
        client = get_elevenlabs_client()
        voice = client.voices.get(voice_id)
        return {
            "id": voice.voice_id,
            "name": voice.name,
            "category": voice.category if hasattr(voice, 'category') else "premade",
            "description": voice.description if hasattr(voice, 'description') else "",
            "labels": voice.labels if hasattr(voice, 'labels') else {}
        }
    except Exception as e:
        print(f"Error fetching voice: {e}")
        raise e
