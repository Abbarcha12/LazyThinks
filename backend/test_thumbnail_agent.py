import os
import sys
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multi_agent_system import ThumbnailAgent
from langchain_groq import ChatGroq
import json

def test_thumbnail_agent():
    print("🧪 Testing Thumbnail Agent...")
    
    # Check keys
    if not os.getenv("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY not found in .env")
        return
    
    if not os.getenv("HUGGINGFACE_API_KEY"):
        print("⚠️ HUGGINGFACE_API_KEY not found in .env. Image generation might fail.")
    
    # Initialize Agent
    try:
        llm = ChatGroq(
            temperature=0.7,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )
        agent = ThumbnailAgent(llm)
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return

    # Mock Data
    title = "How to Build an AI Agent in 10 Minutes (Free Tool)"
    concept = "Tutorial on building AI agents"
    niche = "Tech Education"
    research_data = {
        "patterns": {
            "contains_number": 80,
            "average_length": 45,
            "contains_face": True
        }
    }
    conversation_id = "test-conv-123"

    print(f"\n📝 Input: {title}")
    
    # Run Agent
    try:
        result = agent.generate_thumbnails(
            conversation_id=conversation_id,
            title=title,
            video_concept=concept,
            niche=niche,
            research_data=research_data
        )
        
        print("\n✅ Result Recieved:")
        print(json.dumps(result, indent=2))
        
        # Verify output structure
        assert "strategy" in result
        assert "competitor_insights" in result
        assert "generated_thumbnails" in result
        
        if result["generated_thumbnails"]:
            print(f"\n🖼️ Generated {len(result['generated_thumbnails'])} images")
            for img in result["generated_thumbnails"]:
                print(f"   - {img['image_url']}")
        else:
            print("\n⚠️ No images generated (Check HF API key or logs)")

    except Exception as e:
        print(f"❌ Error execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_thumbnail_agent()
