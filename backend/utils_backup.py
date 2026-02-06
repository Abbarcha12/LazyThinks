import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Define the data structure for job extraction
class JobPosting(BaseModel):
    role: str = Field(description="The job title or role")
    company_name: str = Field(description="name of the company")
    summary: str = Field(description="Brief summary of the job description")
    experience: str = Field(description="Years of experience required")
    skills: list[str] = Field(description="List of required skills")

def process_job_and_generate_proposal(url: str = None, job_description: str = None):
    try:
        content = ""
        # 1. Load Data
        if url:
            # Mimic a real browser to avoid blocking (403/401)
            loader = WebBaseLoader(url, header_template={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            docs = loader.load()
            content = "\\n".join([d.page_content for d in docs])
        elif job_description:
            content = job_description
        else:
            raise ValueError("Either 'url' or 'job_description' must be provided.")
        
        # 2. Setup LLM (Two instances: one for extraction, one for creative writing)
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Extraction LLM: Low temperature for accuracy
        llm_extract = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama-3.3-70b-versatile")
        
        # Proposal LLM: Higher temperature for persuasive creativity
        llm_proposal = ChatGroq(temperature=0.8, groq_api_key=api_key, model_name="llama-3.3-70b-versatile")
            
        llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama-3.3-70b-versatile")
        
        # 3. Extraction Step
        parser = JsonOutputParser(pydantic_object=JobPosting)
        
        extraction_prompt = PromptTemplate(
            template="""
            Extract the following information from the job description below.
            Return a JSON object with the following keys: role, company_name, summary, experience, skills.
            
            {format_instructions}
            
            JOB DESCRIPTION:
            {job_description}
            """,
            input_variables=["job_description"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        
        extraction_chain = extraction_prompt | llm_extract | parser
        job_data = extraction_chain.invoke({"job_description": content})
        
        # 4. Proposal Generation Step (Psychological / Deep Insight Style)
        proposal_prompt = PromptTemplate(
            template="""
            ### JOB DETAILS:
            Role: {role}
            Company: {company_name}
            Summary: {summary}
            Experience Required: {experience}
            Skills: {skills}
            
            ### INSTRUCTION:
            You are an Elite Consultant who solves high-value business problems. 
            Your goal is to "hunt" the client mentally—showing you understand their problem better than they do.
            
            **THE "MENTAL HUNTER" FRAMEWORK:**
            
            1.  **The Diagnosis (The Hook):** 
                *   Ignore the "I am..." intro.
                *   Immediately validate their *pain* or *fear*.
                *   Example: "Scaling a Node.js backend without proper architecture is usually where teams fail..." or "You are looking for X, but the real challenge is actually Y..."
                *   *Goal:* Make them say, "Wow, he gets it."
                
            2.  **The Authority (The Pivot):**
                *   Don't just list skills. Explain *why* your approach prevents disaster or guarantees ROI.
                *   Use strong, confident language. No "I think" or "I hope".
                
            3.  **The Proof (The Kill):**
                *   "I recently fixed this exact issue for [Client/Project] by implementing [Mechanism], which resulted in [Outcome]."
                
            4.  **The Power CTA:**
                *   Don't ask "Can we talk?".
                *   Command the next step gently but firmly: "If you want to solve [Problem] once and for all, let's have a brief chat."
            
            **FORMATTING RULES:**
            *   **Double Spacing:** You MUST put an empty line between every paragraph (use \\n\\n).
            *   **Bold Keywords:** Use **Markdown bold** for the most important impact words (Revenue, Efficiency, Scale, Performance).
            
            **TONE:** 
            *   Dominant but polite. 
            *   Insightful. 
            *   "Peer-to-Peer" (You are an expert talking to a business owner).
            
            **EXAMPLE OF A WINNING PROPOSAL:**
            
            "Building a **scalable** e-commerce backend isn't just about writing clean code—it's about preventing the bottlenecks that kill conversion rates during traffic spikes.
            
            I've architected distributed Node.js systems for clients processing 10M+ monthly transactions. My approach focuses on **database optimization**, **caching strategies**, and **load balancing**—the three pillars that actually move the needle on uptime and revenue.
            
            For a recent SaaS client, I rebuilt their payment processing pipeline, cutting response time by 60% and eliminating timeout errors during peak hours. That translated to a 23% boost in completed checkouts.
            
            If you want to scale without breaking your current system, let's schedule a quick technical review."
            
            ---
            
            Now write YOUR proposal based on the job details above. Do NOT use placeholders. Sign off simply.
            
            ### PROPOSAL:
            """,
            input_variables=["role", "company_name", "summary", "experience", "skills"]
        )
        
        # Using StrOutputParser with the creative LLM
        from langchain_core.output_parsers import StrOutputParser
        email_chain = proposal_prompt | llm_proposal | StrOutputParser()
        
        email_content = email_chain.invoke({
            "role": job_data.get("role", "N/A"),
            "company_name": job_data.get("company_name", "Client"),
            "summary": job_data.get("summary", "N/A"),
            "experience": job_data.get("experience", "N/A"),
            "skills": ", ".join(job_data.get("skills", [])),
        })
        
        return {
            "email": email_content,
            "job_details": job_data
        }
        
    except Exception as e:
        print(f"Error generating email: {e}")
        raise e


def generate_ugc_script_breakdown(idea: str, niche: str, tone: str, platform: str, length: int, language: str = "english", model_provider: str = "groq"):
    """
    Generates a complete UGC video script with shot-by-shot breakdown.
    Follows industry-standard 5-part structure: Hook → Problem → Solution → Proof → CTA
    """
    try:
        llm = None
        
        # Select Provider
        if model_provider == "siliconflow":
            api_key = os.getenv("SILICONFLOW_API_KEY")
            if not api_key:
                 # Fallback to Groq if SF key missing but Groq exists
                 if os.getenv("GROQ_API_KEY"):
                     print("⚠ SiliconFlow key missing, falling back to Groq")
                     model_provider = "groq"
                 else:
                    raise ValueError("SILICONFLOW_API_KEY not found")
            
            if model_provider == "siliconflow":
                # Use DeepSeek-V3 or Qwen-2.5 as requested
                llm = ChatOpenAI(
                    model="deepseek-ai/DeepSeek-V3", # or "Qwen/Qwen2.5-72B-Instruct"
                    openai_api_key=api_key,
                    openai_api_base="https://api.siliconflow.cn/v1",
                    temperature=0.9
                )
                print("🧠 Using SiliconFlow (DeepSeek-V3) for script generation")

        if model_provider == "groq" or llm is None:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            llm = ChatGroq(temperature=0.9, groq_api_key=api_key, model_name="llama-3.3-70b-versatile")
            print("⚡ Using Groq (Llama-3) for script generation")
        
        # Calculate approximate number of shots based on length
        # 5-12 seconds per shot
        num_shots = max(6, min(12, length // 5))
        
        # UGC Script Generation Prompt
        ugc_prompt = PromptTemplate(
            template="""You are an expert UGC (User Generated Content) video scriptwriter. 
Your task is to create a highly engaging, authentic-feeling {length}-second video script for {platform}.

## PRODUCT/IDEA:
{idea}

## TARGET AUDIENCE:
{niche}

## TONE:
{tone}

## LANGUAGE:
{language}

## UGC VIDEO STRUCTURE (5 parts):
1. HOOK (3 seconds, 1 shot) - Grab immediate attention
   - Ask provocative question
   - Show bold claim
   - Call out specific person
   - Pattern interrupt

2. PROBLEM (5-8 seconds, 1-2 shots) - Establish pain point
   - Describe the struggle/frustration
   - Make it relatable and emotional

3. SOLUTION (8-12 seconds, 2-3 shots) - Introduce product
   - "Then I tried..."
   - Natural transition
   - Show excitement/discovery

4. PROOF/DEMO (8-12 seconds, 2-4 shots) - Build credibility
   - Before/after results
   - Key features (2-3 max)
   - How it actually works
   - Real testimonial feel

5. CTA (3-5 seconds, 1 shot) - Drive action
   - Direct command
   - Urgency or incentive
   - "Link in bio" / "Use code XYZ"

## YOUR TASK:
Generate exactly {num_shots} shots. For EACH shot, provide:

1. **shot_number**: Sequential number (1, 2, 3...)
2. **type**: One of: hook, problem, solution, proof, b-roll, cta
3. **duration**: 5-12 seconds (total should equal ~{length}s)
4. **scene**: Detailed visual description (setting, action, props) - KEEP IN ENGLISH
5. **script**: Natural, conversational dialogue (include "umm", pauses, realistic speech) - WRITE IN {language}
6. **emotion**: excited, surprised, curious, frustrated, relieved, confident
7. **camera**: static, slow-zoom, pan, handheld, selfie-angle
8. **image_prompt**: Detailed prompt for generating first-frame reference image (for Midjourney/DALL-E) - KEEP IN ENGLISH
9. **video_prompt**: Detailed prompt for video generator (HeyGen/Runway) - include scene + script + emotion + movement - KEEP IN ENGLISH

## CRITICAL RULES:
- Make script feel AUTHENTIC and HUMAN (not robotic or salesy)
- Use first-person perspective ("I", "my")
- Include natural speech patterns ("okay so", "honestly", "literally")
- Each shot must flow naturally to the next
- Total duration should be close to {length} seconds
- **Image/Video Prompts MUST be in ENGLISH** regardless of script language.
- **Scene descriptions MUST be in ENGLISH**.
- **Script/Dialogue MUST be in {language}**.
  - If {language} is Urdu, use proper Urdu script (e.g., "کیا حال ہے"). output the script text in Urdu characters so the TTS engine can read it correctly.
  - If {language} is English, use English.

## OUTPUT FORMAT:
Return ONLY a valid JSON object with this structure:
{{
  "video_concept": {{
    "hook": "brief hook strategy (English)",
    "problem": "pain point summary (English)",
    "solution": "product introduction approach (English)",
    "proof": "credibility strategy (English)",
    "cta": "call to action (English)"
  }},
  "shots": [
    {{
      "shot_number": 1,
      "type": "hook",
      "duration": 3,
      "scene": "Close-up of person's face...",
      "script": "Okay so this literally changed my life...",
      "emotion": "excitement",
      "camera": "static, selfie-angle",
      "image_prompt": "Close-up portrait...",
      "video_prompt": "Young person records selfie..."
    }},
    ... (continue for all {num_shots} shots)
  ],
  "production_notes": {{
    "character_description": "Describe ideal character",
    "setting": "Primary locations",
    "total_estimated_duration": {length},
    "tips": ["tip 1", "tip 2", "tip 3"]
  }},
  "voice_script": {{
    "full_text": "Complete script combining all dialogue...",
    "suggested_voice": "Young female, energetic...",
    "estimated_duration": {length}
  }}
}}

Generate the complete UGC video script now:""",
            input_variables=["idea", "niche", "tone", "platform", "length", "num_shots", "language"]
        )
        
        # Output parser
        from langchain_core.output_parsers import JsonOutputParser
        parser = JsonOutputParser()
        
        # Chain
        chain = ugc_prompt | llm | parser
        
        # Generate
        result = chain.invoke({
            "idea": idea,
            "niche": niche,
            "tone": tone,
            "platform": platform,
            "length": length,
            "num_shots": num_shots,
            "language": language
        })
        
        return result
        
    except Exception as e:
        print(f"Error generating UGC script: {e}")
        raise e

