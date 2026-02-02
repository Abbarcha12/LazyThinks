import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
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
