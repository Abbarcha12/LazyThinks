import requests
import json

url = "http://127.0.0.1:8000/api/proposal/generate-multiagent"
data = {
    "job_description": "Seeking a Senior AI Engineer to build a RAG-based chatbot. Must have experience with Pinecone, LangChain, and Groq."
}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, json=data, timeout=120)
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS!")
        print(f"Status: {result.get('status')}")
        print("-" * 30)
        print("FINAL PROPOSAL:")
        print(result.get("email"))
        print("-" * 30)
        print("AGENT LOGS:")
        for log in result.get("conversation_logs", []):
            print(f"[{log['sender']}] -> {log['receiver']}: {type(log['content'])}")
    else:
        print(f"❌ FAILED: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ ERROR: {e}")
