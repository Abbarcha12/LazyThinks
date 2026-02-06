import edge_tts
import asyncio
import os
import uuid

# Common voices for easy access
POPULAR_VOICES = [
    {"ShortName": "en-US-ChristopherNeural", "Gender": "Male", "Locale": "en-US"},
    {"ShortName": "en-US-EricNeural", "Gender": "Male", "Locale": "en-US"},
    {"ShortName": "en-US-GuyNeural", "Gender": "Male", "Locale": "en-US"},
    {"ShortName": "en-US-JennyNeural", "Gender": "Female", "Locale": "en-US"},
    {"ShortName": "en-US-MichelleNeural", "Gender": "Female", "Locale": "en-US"},
    {"ShortName": "en-US-RogerNeural", "Gender": "Male", "Locale": "en-US"},
    {"ShortName": "en-UK-SoniaNeural", "Gender": "Female", "Locale": "en-GB"}, # Actually en-GB-SoniaNeural mostly.
    {"ShortName": "en-GB-RyanNeural", "Gender": "Male", "Locale": "en-GB"},
    {"ShortName": "en-GB-SoniaNeural", "Gender": "Female", "Locale": "en-GB"}
]

async def list_edge_voices_async():
    """
    List all available voices from Edge TTS (filtered to English and Urdu only)
    """
    try:
        all_voices = await edge_tts.list_voices()
        # Filter to only English and Urdu voices
        filtered_voices = [
            v for v in all_voices 
            if v.get('Locale', '').startswith('en-') or v.get('Locale', '').startswith('ur-')
        ]
        return filtered_voices
    except Exception as e:
        print(f"Error listing edge voices: {e}")
        return []

def list_edge_voices():
    """
    Sync wrapper for listing voices
    """
    return asyncio.run(list_edge_voices_async())

async def generate_edge_audio_async(text, voice, output_path):
    """
    Generate audio using Edge TTS
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path

def generate_edge_audio(text, voice="en-US-ChristopherNeural", output_path=None):
    """
    Sync wrapper for generating audio.
    Saves to 'generated_audio' directory if no path provided.
    """
    try:
        if not output_path:
            # Create output directory if not exists
            audio_dir = os.path.join(os.path.dirname(__file__), "generated_audio")
            if not os.path.exists(audio_dir):
                os.makedirs(audio_dir)
                
            filename = f"edge_{uuid.uuid4()}.mp3"
            output_path = os.path.join(audio_dir, filename)
        
        asyncio.run(generate_edge_audio_async(text, voice, output_path))
        
        return output_path
    except Exception as e:
        print(f"Error generating Edge audio: {e}")
        raise e
