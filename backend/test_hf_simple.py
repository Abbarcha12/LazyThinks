import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_hf():
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        print("No API Key")
        return

    headers = {"Authorization": f"Bearer {api_key}"}
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    
    print(f"Testing HF API with key: {api_key[:4]}...{api_key[-4:]}")
    
    payload = {"inputs": "Astronaut riding a horse on mars"}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
    else:
        print("Success! Image generated (not saving, just checking 200 OK)")

if __name__ == "__main__":
    test_hf()
