
import os
import requests
from dotenv import load_dotenv

# Load env vars
load_dotenv()

VIDEO_MODEL = "stabilityai/stable-video-diffusion-img2vid-xt"
API_URL = f"https://api-inference.huggingface.co/models/{VIDEO_MODEL}"
TOKEN = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not TOKEN:
    print("❌ Token not found in .env")
    exit(1)

headers = {"Authorization": f"Bearer {TOKEN}"}

# Create a simple test image (red square)
from PIL import Image
img = Image.new('RGB', (1024, 576), color = 'red')
img.save('test_input.png')

print(f"🚀 Testing HF SVD with model: {VIDEO_MODEL}")
print("Sending test_input.png...")

with open("test_input.png", "rb") as f:
    data = f.read()

try:
    response = requests.post(API_URL, headers=headers, data=data)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        with open("test_output.mp4", "wb") as f:
            f.write(response.content)
        print("✅ SUCCESS: Video saved to test_output.mp4")
    else:
        print(f"❌ ERROR: {response.text}")
        
except Exception as e:
    print(f"❌ EXCEPTION: {e}")
