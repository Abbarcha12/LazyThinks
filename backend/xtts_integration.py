import os
import torch
import uuid
from TTS.api import TTS

# Global model instance to avoid reloading (it's heavy)
xtts_model = None

def get_xtts_model():
    global xtts_model
    if xtts_model is None:
        print("Loading XTTS model... this may take a moment.")
        # Using gpu if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # Download and load the model
        xtts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    return xtts_model

def clone_voice(text, reference_audio_path, language="en"):
    """
    Generate audio using XTTS-v2 voice cloning.
    """
    try:
        tts = get_xtts_model()
        
        # Create output directory
        audio_dir = os.path.join(os.path.dirname(__file__), "generated_audio")
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
            
        filename = f"xtts_{uuid.uuid4()}.wav"
        output_path = os.path.join(audio_dir, filename)
        
        # Generate
        tts.tts_to_file(
            text=text,
            speaker_wav=reference_audio_path,
            language=language,
            file_path=output_path
        )
        
        return output_path
    except Exception as e:
        print(f"Error in XTTS cloning: {e}")
        raise e
