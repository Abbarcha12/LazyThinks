"""
Video Generation Task (SQLite-based)
Orchestrates the complete UGC video generation pipeline running in a background thread.
"""

import os
import time
import uuid
from analytics_models import SessionLocal, VideoJob
from edge_tts_integration import generate_edge_audio
from integrations.stability_ai import enhance_prompt_for_ugc
from integrations.huggingface import batch_generate_images_hf, generate_video_hf
from video_processing.stitcher import stitch_videos, create_thumbnail, resize_to_vertical_format, create_static_video_from_image

def update_job_status(job_id: str, status: str, progress: int, message: str = None, result: dict = None, error: str = None):
    """Helper to update job status in SQLite"""
    db = SessionLocal()
    try:
        job = db.query(VideoJob).filter(VideoJob.id == job_id).first()
        if job:
            job.status = status
            job.progress = progress
            if message:
                job.message = message
            if result:
                job.result = result
            if error:
                job.error = error
            db.commit()
    except Exception as e:
        print(f"Error updating job status: {e}")
    finally:
        db.close()

def generate_complete_video_task(job_id: str, script_data: dict):
    """
    Complete video generation pipeline (Thread-based)
    
    Args:
        job_id: UUID of the VideoJob in SQLite
        script_data: Full UGC script data
    """
    from backend.producer.video_producer import VideoProducer
    
    try:
        # Define base directory (using current file path to locate root)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        # Initialize Producer (The "Director")
        producer = VideoProducer(job_id, base_dir)
        
        # Run Production
        # Note: script_data might contain the initial request like 'idea', 'niche' etc.
        # IF script_data already has 'shots' (pre-generated), we might need to adjust Producer to accept that.
        # But assuming the Producer handles full lifecycle or we pass data accordingly.
        # For this refactor, we pass the raw input if available, or structure it.
        
        return producer.produce_video(script_data)
        
    except Exception as e:
        print(f"Error in video generation task: {e}")
        update_job_status(job_id, 'failed', 0, str(e), error=str(e))

