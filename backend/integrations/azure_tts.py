"""
Azure Text-to-Speech Integration
Cost: FREE tier (5M chars/month) or $4 per 1M chars
Quality: High-quality neural voices
"""

import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()


def get_azure_speech_config():
    """Initialize Azure Speech Service configuration"""
    api_key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION", "eastus")
    
    if not api_key:
        raise ValueError("AZURE_SPEECH_KEY not found in environment variables")
    
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    return speech_config


def generate_voice_azure(text: str, voice_name: str = "en-US-JennyNeural", output_path: str = None):
    """
    Generate voice audio using Azure TTS
    
    Args:
        text: Text to convert to speech
        voice_name: Azure neural voice name (default: en-US-JennyNeural)
        output_path: Path to save MP3 file
    
    Returns:
        Path to generated audio file
    
    Available voices:
        - en-US-JennyNeural (Female, friendly)
        - en-US-GuyNeural (Male, professional)
        - en-US-AriaNeural (Female, warm)
        - en-US-DavisNeural (Male, authoritative)
        - en-US-SaraNeural (Female, casual)
    """
    try:
        # Create config
        speech_config = get_azure_speech_config()
        speech_config.speech_synthesis_voice_name = voice_name
        
        # Set output format to MP3
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
        )
        
        # Generate filename if not provided
        if not output_path:
            audio_dir = os.path.join(os.path.dirname(__file__), "..", "generated_audio")
            os.makedirs(audio_dir, exist_ok=True)
            
            import time
            timestamp = int(time.time())
            output_path = os.path.join(audio_dir, f"voice_azure_{timestamp}.mp3")
        
        # Configure audio output
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
        
        # Create synthesizer
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        
        # Generate speech
        result = synthesizer.speak_text_async(text).get()
        
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"✓ Voice generated successfully: {output_path}")
            return output_path
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation.reason}")
            if cancellation.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation.error_details}")
            raise Exception(f"Azure TTS failed: {cancellation.error_details}")
        
    except Exception as e:
        print(f"Error generating voice with Azure TTS: {e}")
        raise e


def get_azure_voices():
    """
    Get list of popular Azure neural voices for UGC
    
    Returns:
        List of voice dictionaries with id, name, gender, description
    """
    return [
        {
            "id": "en-US-JennyNeural",
            "name": "Jenny",
            "gender": "Female",
            "description": "Friendly, conversational, perfect for casual UGC",
            "age": "Young adult"
        },
        {
            "id": "en-US-GuyNeural",
            "name": "Guy",
            "gender": "Male",
            "description": "Professional, clear, great for product demos",
            "age": "Adult"
        },
        {
            "id": "en-US-AriaNeural",
            "name": "Aria",
            "gender": "Female",
            "description": "Warm, empathetic, ideal for emotional stories",
            "age": "Adult"
        },
        {
            "id": "en-US-DavisNeural",
            "name": "Davis",
            "gender": "Male",
            "description": "Authoritative, trustworthy, good for expert reviews",
            "age": "Adult"
        },
        {
            "id": "en-US-SaraNeural",
            "name": "Sara",
            "gender": "Female",
            "description": "Casual, relatable, great for lifestyle content",
            "age": "Young adult"
        },
        {
            "id": "en-US-TonyNeural",
            "name": "Tony",
            "gender": "Male",
            "description": "Energetic, upbeat, perfect for fitness/sports",
            "age": "Young adult"
        },
        {
            "id": "en-US-NancyNeural",
            "name": "Nancy",
            "gender": "Female",
            "description": "Professional, mature, ideal for beauty/wellness",
            "age": "Mature"
        },
        {
            "id": "en-US-JasonNeural",
            "name": "Jason",
            "gender": "Male",
            "description": "Casual, friendly, good for tech reviews",
            "age": "Young adult"
        }
    ]


def test_azure_connection():
    """Test Azure TTS connection and generate sample audio"""
    try:
        print("Testing Azure TTS connection...")
        test_text = "Hey there! This is a test of Azure Text to Speech. If you can hear this, everything is working perfectly!"
        
        output_path = generate_voice_azure(test_text, "en-US-JennyNeural")
        print(f"✓ Test successful! Audio saved to: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Azure TTS test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the module
    test_azure_connection()
