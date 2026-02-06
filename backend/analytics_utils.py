from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import json

load_dotenv()

def get_llm(model_name="llama-3.3-70b-versatile", temperature=0.7):
    """
    Get a configured LLM instance.
    
    Args:
        model_name: Model to use (llama-3.3-70b-versatile or mixtral-8x7b-32768)
        temperature: Creativity level (0-1)
    
    Returns:
        ChatGroq instance
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    return ChatGroq(
        api_key=api_key,
        model_name=model_name,
        temperature=temperature
    )

def format_records_for_analysis(records):
    """
    Format database records into a readable string for LLM analysis.
    
    Args:
        records: List of AnalyticsRecord objects
    
    Returns:
        Formatted string representation of the data
    """
    if not records:
        return "No records found in the database."
    
    # Convert records to dictionaries
    data = [record.to_dict() if hasattr(record, 'to_dict') else record for record in records]
    
    # Create a structured representation
    formatted = "📊 Analytics Data Summary\n\n"
    formatted += f"Total Records: {len(data)}\n\n"
    
    # Group by category
    categories = {}
    for record in data:
        cat = record.get('category', 'Uncategorized')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(record)
    
    formatted += "Categories:\n"
    for cat, cat_records in categories.items():
        formatted += f"  • {cat}: {len(cat_records)} records\n"
    
    formatted += "\n" + "="*50 + "\n\n"
    formatted += "Detailed Records:\n\n"
    
    for i, record in enumerate(data, 1):
        formatted += f"{i}. {record.get('name', 'N/A')}\n"
        formatted += f"   Category: {record.get('category', 'N/A')}\n"
        formatted += f"   Value: {record.get('value', 0)}\n"
        if record.get('metadata'):
            formatted += f"   Metadata: {json.dumps(record.get('metadata'), indent=6)}\n"
        formatted += f"   Created: {record.get('created_at', 'N/A')}\n"
        formatted += "\n"
    
    return formatted

def analyze_data_with_llm(records, query, model_name="llama-3.3-70b-versatile"):
    """
    Analyze analytics data using LLM.
    
    Args:
        records: List of AnalyticsRecord objects
        query: User's analysis query
        model_name: LLM model to use
    
    Returns:
        Analysis result as string
    """
    try:
        # Format data for analysis
        formatted_data = format_records_for_analysis(records)
        
        # Get LLM instance
        llm = get_llm(model_name=model_name, temperature=0.7)
        
        # Create system and user messages
        system_prompt = """You are an expert data analyst with deep expertise in extracting insights from structured data.
Your role is to:
- Analyze the provided analytics data thoroughly
- Identify patterns, trends, and anomalies
- Provide actionable insights and recommendations
- Use clear, professional language
- Format your response with markdown for better readability
- Include specific data points and statistics to support your analysis

Be concise but comprehensive. Focus on the most important findings."""

        user_prompt = f"""Here is the analytics data:

{formatted_data}

User Query: {query}

Please analyze the data and provide insights based on the query above."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        # Get response
        response = llm.invoke(messages)
        
        return response.content
        
    except Exception as e:
        raise Exception(f"Error during LLM analysis: {str(e)}")

def get_available_models():
    """
    Return list of available LLM models for analytics.
    
    Returns:
        List of model configurations
    """
    return [
        {
            "id": "llama-3.3-70b-versatile",
            "name": "Llama 3.3 70B",
            "description": "Meta's most powerful open model, great for complex analysis"
        },
        {
            "id": "mixtral-8x7b-32768",
            "name": "Mixtral 8x7B (Grok)",
            "description": "Fast and efficient model with large context window"
        },
        {
            "id": "llama-3.1-70b-versatile",
            "name": "Llama 3.1 70B",
            "description": "Previous generation Llama, still very capable"
        }
    ]
