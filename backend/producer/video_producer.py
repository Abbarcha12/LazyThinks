import os
import time
import json
from typing import Dict, Any, List
from backend.utils import generate_ugc_script_breakdown
from backend.integrations.audio_service import generate_voice
from backend.integrations.huggingface import generate_image_huggingface, generate_video_huggingface
from backend.video_processing.stitcher import stitch_videos, create_thumbnail, create_static_video_from_image
from analytics_models import SessionLocal, VideoJob

class VideoProducer:
    """
    The Director Agent: Orchestrates the creation of high-quality UGC videos.
    Uses Groq (Llama 3.3) for scripts, Edge TTS for voice, and Hugging Face (SDXL/SVD) for visuals.
    """
    
    def __init__(self, job_id: str, base_dir: str):
        self.job_id = job_id
        self.base_dir = base_dir
        self.temp_dir = os.path.join(base_dir, "temp", job_id)
        self.output_dir = os.path.join(base_dir, "generated_videos")
        
        # Ensure directories exist
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(os.path.join(self.temp_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.temp_dir, "clips"), exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def update_status(self, status: str, progress: int, message: str = None, result: dict = None, error: str = None):
        """Update job status in database"""
        db = SessionLocal()
        try:
            job = db.query(VideoJob).filter(VideoJob.id == self.job_id).first()
            if job:
                job.status = status
                job.progress = progress
                if message: job.message = message
                if result: job.result = result
                if error: job.error = error
                db.commit()
        except Exception as e:
            print(f"Error updating status: {e}")
        finally:
            db.close()

    def produce_video(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the full production pipeline"""
        try:
            self.update_status('processing', 5, "Starting production pipeline...")
            
            # 1. Script Generation (Groq - Llama 3.3)
            self.update_status('processing', 10, "Generating script with Groq...")
            script_data = self._generate_script(request_data)
            
            shots = script_data.get('shots', [])
            if not shots:
                raise ValueError("Script generation returned no shots.")

            # 2. Asset Generation (Parallel-ish)
            self.update_status('processing', 20, f"Generating assets for {len(shots)} shots...")
            
            # 2a. Voiceover (Edge TTS - Free)
            voice_path = self._generate_voiceover(script_data.get('voice_script', {}))
            
            # 2b. Visuals (Hugging Face SDXL -> SVD)
            video_clips = self._generate_visuals(shots)
            
            # 3. Post-Production (Stitching)
            self.update_status('processing', 90, "Stitching final video...")
            final_video_path = self._assemble_video(video_clips, voice_path)
            
            # 4. Finalize
            thumbnail_path = create_thumbnail(final_video_path)
            
            result = {
                'status': 'completed',
                'video_path': final_video_path,
                'thumbnail_path': thumbnail_path,
                'job_id': self.job_id,
                'script': script_data
            }
            
            self.update_status('completed', 100, "Production complete!", result=result)
            return result
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.update_status('failed', 0, str(e), error=str(e))
            raise e

    def _generate_script(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate script using Groq (Llama 3.3) - FREE"""
        return generate_ugc_script_breakdown(
            idea=data.get('idea'),
            niche=data.get('niche'),
            tone=data.get('tone', 'energetic'),
            platform=data.get('platform', 'tiktok'),
            length=data.get('duration', 30)
            # Now defaults to "groq" in utils.py
        )

    def _generate_voiceover(self, voice_script: Dict[str, Any]) -> str:
        """Generate voice using Edge TTS - FREE"""
        text = voice_script.get('full_text', '')
        output_path = os.path.join(self.temp_dir, "voice.mp3")
        
        self.update_status('processing', 30, "Synthesizing voiceover (Edge TTS)...")
        
        # Use Edge TTS (free, no API key needed)
        path = generate_voice(text, output_path, model="edge-tts")
        
        if not path or not os.path.exists(path):
            raise Exception("Voice generation failed.")
            
        return path

    def _generate_visuals(self, shots: List[Dict[str, Any]]) -> List[str]:
        """Generate images and video clips"""
        clips = []
        total_shots = len(shots)
        
        for i, shot in enumerate(shots):
            progress = 40 + int((i / total_shots) * 40) # 40% to 80%
            self.update_status('processing', progress, f"Rendering shot {i+1}/{total_shots}...")
            
            # 1. Generate Image (Hugging Face SDXL - FREE)
            img_prompt = shot.get('image_prompt')
            img_path = os.path.join(self.temp_dir, "images", f"shot_{i+1}.png")
            
            generated_img = generate_image_huggingface(img_prompt, img_path)
            
            if not generated_img:
                print(f"Image gen failed for shot {i+1}, skipping...")
                continue
                
            # 2. Generate Video (Stable Video Diffusion - FREE)
            video_prompt = shot.get('video_prompt', img_prompt)
            clip_path = os.path.join(self.temp_dir, "clips", f"clip_{i+1}.mp4")
            
            print(f"Animating shot {i+1} with Stable Video Diffusion...")
            generated_clip = generate_video_huggingface(generated_img, clip_path)
            
            if not generated_clip:
                print(f"Video gen failed for shot {i+1}, using static fallback.")
                # Fallback to static video
                generated_clip = create_static_video_from_image(
                    generated_img, shot.get('duration', 3), clip_path
                )
            
            clips.append(generated_clip)
            
        return clips

    def _assemble_video(self, clips: List[str], audio_path: str) -> str:
        """Stitch clips and audio"""
        filename = f"final_ugc_{int(time.time())}.mp4"
        output_path = os.path.join(self.output_dir, filename)
        
        return stitch_videos(
            video_clips_paths=clips,
            audio_path=audio_path,
            output_path=output_path
        )
