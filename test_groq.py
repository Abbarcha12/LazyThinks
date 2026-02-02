from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY not found in .env file.")
else:
    try:
        # Initialize ChatGroq
        llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama-3.3-70b-versatile")
        
        # Test the connection
        response = llm.invoke("Hello, assume you are a helpful assistant. Just say 'Connection successful!' and nothing else.")
        print(response.content)
        
    except Exception as e:
        print(f"An error occurred: {e}")
