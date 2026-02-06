from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os

load_dotenv()

app = FastAPI()

# Mount generated images directory
os.makedirs("generated_images", exist_ok=True)
app.mount("/generated_images", StaticFiles(directory="generated_images"), name="generated_images")

# Configure CORS
origins = [
    "http://localhost:5173",  # React default port
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

from pydantic import BaseModel
from utils import process_job_and_generate_proposal

class EmailRequest(BaseModel):
    url: str | None = None
    job_description: str | None = None

@app.post("/submit")
def generate_proposal(request: EmailRequest):
    try:
        if not request.url and not request.job_description:
             return {"status": "error", "message": "Please provide either a URL or Job Description text."}
             
        result = process_job_and_generate_proposal(url=request.url, job_description=request.job_description)
        return {"status": "success", "email": result["email"], "job_details": result["job_details"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/health/db")
def db_check():
    try:
        from db import get_chroma_client
        client = get_chroma_client()
        client.heartbeat()
        return {"status": "connected", "message": "ChromaDB is reachable"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# UGC Video Script Generator Endpoint
from models import UGCRequest, UGCScriptResponse
from utils import generate_ugc_script_breakdown

@app.post("/api/ugc/generate-script")
def generate_ugc_script(request: UGCRequest):
    """
    Generates a complete UGC video script with shot-by-shot breakdown.
    Returns prompts for image/video generation and production notes.
    """
    try:
        result = generate_ugc_script_breakdown(
            idea=request.idea,
            niche=request.niche,
            tone=request.tone,
            platform=request.platform,
            length=request.length,
            language=request.language
        )
        return {"status": "success", "data": result}
    except Exception as e:
        print(f"Error in UGC generation: {e}")
        return {"status": "error", "message": str(e)}


# Voice Generation Endpoints
from elevenlabs_integration import get_available_voices, generate_voice_audio, get_voice_by_id
from fastapi.responses import FileResponse

class VoiceGenerationRequest(BaseModel):
    text: str = Field(description="Text to convert to speech")
    voice_id: str = Field(description="ID of the voice to use")

@app.get("/api/voices/list")
def list_voices():
    """
    Get list of available ElevenLabs voices
    """
    try:
        voices = get_available_voices()
        return {"status": "success", "voices": voices}
    except ValueError as e:
        return {"status": "error", "message": "ElevenLabs API key not configured. Please add ELEVENLABS_API_KEY to .env file"}
    except Exception as e:
        print(f"Error listing voices: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/voices/generate")
def create_voice_audio(request: VoiceGenerationRequest):
    """
    Generate voice audio from text using ElevenLabs
    Returns path to generated audio file
    """
    try:
        audio_path = generate_voice_audio(
            text=request.text,
            voice_id=request.voice_id
        )
        
        # Return relative path for download
        import os
        filename = os.path.basename(audio_path)
        return {
            "status": "success",
            "audio_url": f"/api/voices/download/{filename}",
            "filename": filename
        }
    except ValueError as e:
        return {"status": "error", "message": "ElevenLabs API key not configured. Please add ELEVENLABS_API_KEY to .env file"}
    except Exception as e:
        print(f"Error generating audio: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/voices/download/{filename}")
def download_voice_audio(filename: str):
    """
    Download generated voice audio file
    """
    try:
        import os
        audio_dir = os.path.join(os.path.dirname(__file__), "generated_audio")
        file_path = os.path.join(audio_dir, filename)
        
        if not os.path.exists(file_path):
            return {"status": "error", "message": "File not found"}
        
        return FileResponse(
            file_path,
            media_type="audio/mpeg",
            filename=filename
        )
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return {"status": "error", "message": str(e)}



# ---------------------------------------------------
# Edge TTS (Free) Endpoints
# ---------------------------------------------------
from edge_tts_integration import list_edge_voices, generate_edge_audio

@app.get("/api/voices/edge/list")
def list_edge_voices_endpoint():
    """
    Get list of available Edge TTS voices
    """
    try:
        voices = list_edge_voices()
        formatted_voices = []
        for v in voices:
            formatted_voices.append({
                "voice_id": v["ShortName"],
                "name": f"{v['ShortName']} ({v['Gender']})",
                "category": "edge", # explicit category
                "preview_url": None
            })
        return {"status": "success", "voices": formatted_voices}
    except Exception as e:
        print(f"Error listing edge voices: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/voices/edge/generate")
def create_edge_voice_audio(request: VoiceGenerationRequest):
    """
    Generate voice audio from text using Edge TTS (Free)
    """
    try:
        audio_path = generate_edge_audio(
            text=request.text,
            voice=request.voice_id
        )
        
        # Return relative path for download
        import os
        filename = os.path.basename(audio_path)
        return {
            "status": "success",
            "audio_url": f"/api/voices/download/{filename}",
            "filename": filename
        }
    except Exception as e:
        print(f"Error generating Edge audio: {e}")
        return {"status": "error", "message": str(e)}


# ---------------------------------------------------
# XTTS Voice Cloning Endpoints (DISABLED - Model loading causes server hang)
# ---------------------------------------------------
# TODO: Re-enable after implementing lazy loading
# from fastapi import UploadFile, File, Form
# from xtts_integration import clone_voice
# import shutil
# 
# @app.post("/api/voices/xtts/generate")
# async def create_xtts_voice_audio(
#     text: str = Form(...),
#     reference_audio: UploadFile = File(...),
#     language: str = Form("en")
# ):
#     """
#     Generate voice audio using XTTS-v2 voice cloning.
#     Requires a reference audio file (3-10 seconds) to clone.
#     """
#     try:
#         # Save uploaded file temporarily
#         temp_dir = os.path.join(os.path.dirname(__file__), "temp")
#         if not os.path.exists(temp_dir):
#             os.makedirs(temp_dir)
#         
#         temp_path = os.path.join(temp_dir, f"ref_{reference_audio.filename}")
#         with open(temp_path, "wb") as buffer:
#             shutil.copyfileobj(reference_audio.file, buffer)
#         
#         # Generate cloned voice
#         audio_path = clone_voice(
#             text=text,
#             reference_audio_path=temp_path,
#             language=language
#         )
#         
#         # Cleanup temp file
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
#         
#         filename = os.path.basename(audio_path)
#         return {
#             "status": "success",
#             "audio_url": f"/api/voices/download/{filename}",
#             "filename": filename
#         }
#     except Exception as e:
#         print(f"Error in XTTS generation: {e}")
#         return {"status": "error", "message": str(e)}


# ---------------------------------------------------
# Full Automation Video Generation Endpoints (No Celery/Redis)
# ---------------------------------------------------
from fastapi import BackgroundTasks, Depends
from sqlalchemy.orm import Session
from tasks.video_generation_task import generate_complete_video_task
from analytics_models import VideoJob, get_db
import uuid

@app.post("/api/ugc/generate-video")
def start_video_generation(request: UGCScriptResponse, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Start the async video generation process using local thread.
    Returns task_id to poll for status.
    """
    try:
        job_id = str(uuid.uuid4())
        
        # Create Job record in DB
        new_job = VideoJob(
            id=job_id,
            status="pending",
            progress=0,
            message="Queued for generation..."
        )
        db.add(new_job)
        db.commit()
        
        # Convert Pydantic model to dict
        script_data = request.model_dump()
        
        # Start background task
        background_tasks.add_task(generate_complete_video_task, job_id, script_data)
        
        return {
            "status": "success", 
            "message": "Video generation started",
            "task_id": job_id
        }
    except Exception as e:
        print(f"Error starting video generation: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/ugc/video-status/{task_id}")
def get_video_status(task_id: str, db: Session = Depends(get_db)):
    """
    Check status of video generation task from DB.
    """
    try:
        job = db.query(VideoJob).filter(VideoJob.id == task_id).first()
        
        if not job:
            return {"status": "not_found", "message": "Task not found"}
            
        status = job.status
        # Map DB status to frontend expected status (PENDING, PROGRESS, SUCCESS, FAILURE)
        # Frontend expects: processing, completed, failed
        
        response = {
            "task_id": task_id,
            "status": status, # pending, processing, completed, failed
            "progress": job.progress,
            "message": job.message
        }
        
        if status == 'completed' and job.result:
             response["result"] = job.result
        
        if status == 'failed':
            response["error"] = job.error
            
        return response
        
    except Exception as e:
        print(f"Error checking task status: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/ugc/download/{video_id}")
def download_video(video_id: str):
    """
    Download generated video file
    """
    try:
        import os
        # Search in generated_videos and generated_videos/clips
        base_dir = os.path.dirname(__file__)
        possible_paths = [
            os.path.join(base_dir, "generated_videos", video_id),
            os.path.join(base_dir, "generated_videos", "clips", video_id),
            os.path.join(base_dir, "temp", video_id) # For thumbnails sometimes
        ]
        
        file_path = None
        for path in possible_paths:
            if os.path.exists(path):
                file_path = path
                break
        
        if not file_path:
             # Also try temp directory images/thumbnails if passed as video_id
            if "thumb" in video_id or "image" in video_id:
                 # Logic for finding images if needed, but let's stick to simple file serving
                 pass

        if not file_path or not os.path.exists(file_path):
             return {"status": "error", "message": "File not found"}

        media_type = "video/mp4"
        if video_id.endswith(".jpg") or video_id.endswith(".png"):
            media_type = "image/jpeg"

        return FileResponse(
            file_path,
            media_type=media_type,
            filename=video_id
        )
    except Exception as e:
        print(f"Error downloading video: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/ugc/videos")
def list_generated_videos():
    """
    List all generated UGC videos
    """
    try:
        import os
        base_dir = os.path.dirname(__file__)
        videos_dir = os.path.join(base_dir, "generated_videos")
        
        if not os.path.exists(videos_dir):
            return {"status": "success", "videos": []}
            
        videos = []
        for file in os.listdir(videos_dir):
            if file.endswith(".mp4"):
                 file_path = os.path.join(videos_dir, file)
                 stat = os.stat(file_path)
                 videos.append({
                     "filename": file,
                     "url": f"/api/ugc/download/{file}",
                     "size": stat.st_size,
                     "created_at": stat.st_ctime
                 })
        
        # Sort by creation time (newest first)
        videos.sort(key=lambda x: x["created_at"], reverse=True)
        
        return {"status": "success", "videos": videos}
    except Exception as e:
        print(f"Error listing videos: {e}")
        return {"status": "error", "message": str(e)}


# ---------------------------------------------------
# Data Analytics Tool Endpoints
# ---------------------------------------------------
from analytics_models import AnalyticsRecord, init_db, get_db
from analytics_utils import analyze_data_with_llm, get_available_models
from sqlalchemy.orm import Session
from fastapi import Depends

# Initialize analytics database on startup
init_db()

class AnalyticsRecordCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=1, max_length=100)
    value: float
    extra_data: dict | None = None

class AnalyticsAnalysisRequest(BaseModel):
    query: str = Field(min_length=1, description="Analysis query or question")
    model_name: str = Field(default="llama-3.3-70b-versatile", description="LLM model to use")
    category_filter: str | None = Field(default=None, description="Optional category filter")

@app.post("/api/analytics/records")
def create_analytics_record(record: AnalyticsRecordCreate, db: Session = Depends(get_db)):
    """
    Create a new analytics record in the database.
    """
    try:
        db_record = AnalyticsRecord(
            name=record.name,
            category=record.category,
            value=record.value,
            meta_data=record.metadata
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return {
            "status": "success",
            "message": "Record created successfully",
            "record": db_record.to_dict()
        }
    except Exception as e:
        db.rollback()
        print(f"Error creating record: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/analytics/records")
def get_analytics_records(
    category: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve analytics records with optional filtering.
    """
    try:
        query = db.query(AnalyticsRecord)
        
        if category:
            query = query.filter(AnalyticsRecord.category == category)
        
        records = query.order_by(AnalyticsRecord.created_at.desc()).limit(limit).all()
        
        return {
            "status": "success",
            "count": len(records),
            "records": [record.to_dict() for record in records]
        }
    except Exception as e:
        print(f"Error retrieving records: {e}")
        return {"status": "error", "message": str(e)}

@app.delete("/api/analytics/records/{record_id}")
def delete_analytics_record(record_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific analytics record.
    """
    try:
        record = db.query(AnalyticsRecord).filter(AnalyticsRecord.id == record_id).first()
        
        if not record:
            return {"status": "error", "message": "Record not found"}
        
        db.delete(record)
        db.commit()
        
        return {
            "status": "success",
            "message": f"Record {record_id} deleted successfully"
        }
    except Exception as e:
        db.rollback()
        print(f"Error deleting record: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/analytics/analyze")
def analyze_analytics_data(request: AnalyticsAnalysisRequest, db: Session = Depends(get_db)):
    """
    Analyze analytics data using LLM (Llama 3 or Grok).
    """
    try:
        # Get records with optional category filter
        query = db.query(AnalyticsRecord)
        
        if request.category_filter:
            query = query.filter(AnalyticsRecord.category == request.category_filter)
        
        records = query.order_by(AnalyticsRecord.created_at.desc()).all()
        
        if not records:
            return {
                "status": "success",
                "analysis": "No records found to analyze. Please add some data first."
            }
        
        # Perform analysis using LLM
        analysis_result = analyze_data_with_llm(
            records=records,
            query=request.query,
            model_name=request.model_name
        )
        
        return {
            "status": "success",
            "analysis": analysis_result,
            "records_analyzed": len(records),
            "model_used": request.model_name
        }
    except Exception as e:
        print(f"Error during analysis: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/analytics/models")
def list_available_models():
    """
    Get list of available LLM models for analytics.
    """
    try:
        models = get_available_models()
        return {"status": "success", "models": models}
    except Exception as e:
        print(f"Error listing models: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/analytics/seed")
def seed_sample_data(db: Session = Depends(get_db)):
    """
    Populate database with sample analytics data for demonstration.
    """
    try:
        import random
        from datetime import datetime, timedelta
        
        # Sample data categories and records
        sample_records = [
            # Sales Data
            {"name": "Q1 Revenue", "category": "Sales", "value": 125000, "metadata": {"region": "North America", "team": "Enterprise"}},
            {"name": "Q2 Revenue", "category": "Sales", "value": 148500, "metadata": {"region": "North America", "team": "Enterprise"}},
            {"name": "Q3 Revenue", "category": "Sales", "value": 132000, "metadata": {"region": "Europe", "team": "SMB"}},
            {"name": "Q4 Revenue", "category": "Sales", "value": 167200, "metadata": {"region": "Asia Pacific", "team": "Enterprise"}},
            
            # Marketing Data
            {"name": "Social Media Campaign", "category": "Marketing", "value": 45000, "metadata": {"platform": "LinkedIn", "ROI": "3.2x"}},
            {"name": "Email Campaign", "category": "Marketing", "value": 28500, "metadata": {"platform": "Email", "ROI": "4.5x"}},
            {"name": "PPC Advertising", "category": "Marketing", "value": 62300, "metadata": {"platform": "Google Ads", "ROI": "2.8x"}},
            {"name": "Content Marketing", "category": "Marketing", "value": 38700, "metadata": {"platform": "Blog", "ROI": "5.1x"}},
            
            # Operations Data
            {"name": "Infrastructure Costs", "category": "Operations", "value": 35000, "metadata": {"type": "Cloud Services", "vendor": "AWS"}},
            {"name": "Software Licenses", "category": "Operations", "value": 18500, "metadata": {"type": "SaaS", "count": 45}},
            {"name": "Team Training", "category": "Operations", "value": 12300, "metadata": {"type": "Professional Development", "participants": 28}},
            
            # Customer Success
            {"name": "Customer Retention", "category": "Customer Success", "value": 94.5, "metadata": {"metric": "percentage", "period": "annual"}},
            {"name": "NPS Score", "category": "Customer Success", "value": 68, "metadata": {"metric": "score", "benchmark": "excellent"}},
            {"name": "Support Tickets", "category": "Customer Success", "value": 342, "metadata": {"resolved": 328, "satisfaction": "4.2/5"}},
            
            # Product Metrics
            {"name": "Monthly Active Users", "category": "Product", "value": 25600, "metadata": {"growth": "+12%", "period": "MoM"}},
            {"name": "Feature Adoption", "category": "Product", "value": 78.3, "metadata": {"feature": "AI Assistant", "metric": "percentage"}},
            {"name": "App Performance", "category": "Product", "value": 99.8, "metadata": {"metric": "uptime %", "period": "monthly"}},
        ]
        
        # Insert sample records with varied timestamps
        inserted = 0
        for i, record_data in enumerate(sample_records):
            # Create records with staggered timestamps
            created_time = datetime.utcnow() - timedelta(days=len(sample_records)-i, hours=random.randint(0, 23))
            
            record = AnalyticsRecord(
                name=record_data["name"],
                category=record_data["category"],
                value=record_data["value"],
                meta_data=record_data["metadata"],
                created_at=created_time,
                updated_at=created_time
            )
            db.add(record)
            inserted += 1
        
        db.commit()
        
        return {
            "status": "success",
            "message": f"Successfully seeded {inserted} sample records",
            "records_inserted": inserted
        }
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        return {"status": "error", "message": str(e)}

@app.delete("/api/analytics/clear")
def clear_all_records(db: Session = Depends(get_db)):
    """
    Clear all analytics records from the database.
    """
    try:
        count = db.query(AnalyticsRecord).count()
        db.query(AnalyticsRecord).delete()
        db.commit()
        
        return {
            "status": "success",
            "message": f"Successfully deleted {count} records",
            "records_deleted": count
        }
    except Exception as e:
        db.rollback()
        print(f"Error clearing data: {e}")
        return {"status": "error", "message": str(e)}


# ---------------------------------------------------
# YouTube Title Generator Endpoint
# ---------------------------------------------------
from models import YouTubeTitleRequest, YouTubeTitleResponse
from youtube_title_generator import generate_youtube_titles

@app.post("/api/youtube/generate-titles", response_model=YouTubeTitleResponse)
def create_youtube_titles(request: YouTubeTitleRequest):
    """
    Generate SEO-optimized YouTube titles using proven formulas.
    
    Returns multiple title variations with SEO scores, CTR potential,
    and actionable tips for optimizing titles.
    
    Best practices implemented:
    - Front-load keywords in first 3-5 words
    - Optimal length: 55-60 characters
    - Strategic power word usage
    - Proven title formulas (How-To, Listicle, Authority Hook, etc.)
    """
    try:
        result = generate_youtube_titles(
            video_concept=request.video_concept,
            niche=request.niche,
            keywords=request.keywords,
            tone=request.tone,
            num_variations=request.num_variations
        )
        
        return result
        
    except Exception as e:
        print(f"Error generating YouTube titles: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating titles: {str(e)}")


# ---------------------------------------------------
# Multi-Agent Title Validation Endpoint
# ---------------------------------------------------
from models import TitleValidationRequest, MultiAgentValidationResponse, ValidatedTitleData, AgentMessageData
from multi_agent_system import create_agent_system
from a2a_protocol import protocol
import time

# Initialize agent system (lazy initialization)
_agent_system = None

def get_agent_system():
    global _agent_system
    if _agent_system is None:
        _agent_system = create_agent_system()
    return _agent_system

@app.post("/api/youtube/validate-titles-multiagent", response_model=MultiAgentValidationResponse)
async def validate_titles_with_agents(request: TitleValidationRequest):
    """
    Multi-Agent Title Validation System
    
    Three agents collaborate to validate YouTube titles:
    1. Research Agent: Investigates topic and gathers YouTube data
    2. Competitor Agent: Analyzes titles and suggests improvements
    3. Validator Agent: Makes final decisions with confidence scores
    
    Returns validated titles with evidence-based recommendations.
    """
    try:
        start_time = time.time()
        
        print("\n" + "="*60)
        print("🤖 MULTI-AGENT VALIDATION SYSTEM")
        print("="*60)
        
        # Get agent system
        agents = get_agent_system()
        
        # Create conversation
        conversation_id = protocol.create_conversation()
        print(f"📋 Conversation ID: {conversation_id}")
        
        # Step 1: Research Agent investigates topic
        research_data = agents["research"].research_topic(
            conversation_id=conversation_id,
            video_concept=request.video_concept,
            niche=request.niche,
            keywords=request.keywords
        )
        
        # Step 2: Competitor Agent analyzes titles
        competitor_analysis = agents["competitor"].analyze_titles(
            conversation_id=conversation_id,
            titles=request.titles_to_validate,
            research_data=research_data
        )
        
        # Step 3: Validator Agent makes final decisions
        validation_result = agents["validator"].validate_titles(
            conversation_id=conversation_id,
            original_titles=request.titles_to_validate,
            research_data=research_data,
            competitor_analysis=competitor_analysis
        )
        
        # Step 4: Thumbnail Agent designs for top pick
        thumbnail_data = None
        if validation_result.get('top_recommendation'):
            try:
                top_rec = validation_result['top_recommendation']
                # Ensure we have a valid title string
                title_text = top_rec['title'] if isinstance(top_rec, dict) else top_rec.title
                
                thumbnail_data = agents["thumbnail"].generate_thumbnails(
                    conversation_id=conversation_id,
                    title=title_text,
                    video_concept=request.video_concept,
                    niche=request.niche,
                    research_data=research_data
                )
            except Exception as e:
                print(f"Thumbnail generation error: {e}")
                # Don't fail the whole request if thumbnail fails
        
        # Get conversation log (after all agents work)
        conversation = protocol.format_conversation_for_display(conversation_id)
        
        # Calculate total confidence (average of approved titles)
        approved_titles = [t for t in validation_result['validated_titles'] if t['validation_status'] == 'APPROVED']
        total_confidence = (
            sum(t['confidence_score'] for t in approved_titles) / len(approved_titles)
            if approved_titles else 0.0
        )
        
        processing_time = time.time() - start_time
        
        # Format response
        response = {
            "validated_titles": [ValidatedTitleData(**t) for t in validation_result['validated_titles']],
            "top_recommendation": ValidatedTitleData(**validation_result['top_recommendation']) if validation_result.get('top_recommendation') else None,
            "conversation_log": [AgentMessageData(**msg) for msg in conversation],
            "research_summary": research_data.get('llm_analysis', {}),
            "competitor_analysis": {
                "total_analyzed": len(competitor_analysis.get('title_analyses', [])),
                "alternatives_generated": len(competitor_analysis.get('alternative_titles', []))
            },
            "final_recommendation": validation_result.get('final_recommendation', ''),
            "total_confidence": round(total_confidence, 2),
            "processing_time": round(processing_time, 2),
            "approved_count": validation_result.get('approved_count', 0),
            "thumbnail_data": thumbnail_data
        }
        
        print("="*60)
        print(f"✅ VALIDATION COMPLETE ({processing_time:.2f}s)")
        print(f"   Approved: {response['approved_count']}")
        print(f"   Confidence: {round(total_confidence * 100)}%")
        print("="*60 + "\n")
        
        return response
        
    except Exception as e:
        print(f"Error in multi-agent validation: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Multi-agent validation error: {str(e)}")

