"""
Video Processing & Stitching Module
Uses MoviePy and FFmpeg to combine video clips with audio
"""

import os
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    CompositeVideoClip,
    TextClip
)
from moviepy.video.fx.all import fadein, fadeout
import time


def stitch_videos(video_clips_paths: list, audio_path: str, output_path: str = None, fade_duration: float = 0.3):
    """
    Stitch multiple video clips together with transitions and audio
    
    Args:
        video_clips_paths: List of paths to video clips (in order)
        audio_path: Path to voice audio file
        output_path: Path to save final video
        fade_duration: Duration of fade transitions in seconds
    
    Returns:
        Path to final stitched video
    """
    try:
        print(f"Loading {len(video_clips_paths)} video clips...")
        
        # Load all video clips
        clips = []
        for idx, clip_path in enumerate(video_clips_paths):
            if not os.path.exists(clip_path):
                print(f"⚠ Warning: Clip {idx+1} not found: {clip_path}")
                continue
            
            clip = VideoFileClip(clip_path)
            
            # Add fade transitions (except first and last)
            if idx > 0:
                clip = clip.fx(fadein, fade_duration)
            if idx < len(video_clips_paths) - 1:
                clip = clip.fx(fadeout, fade_duration)
            
            clips.append(clip)
            print(f"  ✓ Loaded clip {idx+1}: {clip.duration:.1f}s")
        
        if not clips:
            raise Exception("No valid video clips found")
        
        # Concatenate all clips
        print("Concatenating clips...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Load and add audio
        if audio_path and os.path.exists(audio_path):
            print("Adding voice audio...")
            audio = AudioFileClip(audio_path)
            
            # Trim or loop audio to match video duration
            if audio.duration < final_video.duration:
                print(f"⚠ Audio ({audio.duration:.1f}s) shorter than video ({final_video.duration:.1f}s)")
            elif audio.duration > final_video.duration:
                audio = audio.subclip(0, final_video.duration)
            
            final_video = final_video.set_audio(audio)
        
        # Ensure output directory exists
        if not output_path:
            output_dir = os.path.join(os.path.dirname(__file__), "..", "generated_videos")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"ugc_video_{int(time.time())}.mp4")
        else:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Export final video
        print(f"Exporting final video to: {output_path}")
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=30,
            preset='medium',
            ffmpeg_params=['-crf', '23']  # Quality (18-28, lower = better)
        )
        
        # Close all clips to free memory
        for clip in clips:
            clip.close()
        if audio_path and os.path.exists(audio_path):
            audio.close()
        final_video.close()
        
        print(f"✓ Video stitching complete: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error stitching videos: {e}")
        raise e


def resize_to_vertical_format(video_path: str, output_path: str = None, target_width: int = 1080, target_height: int = 1920):
    """
    Resize video to vertical format (9:16 for Instagram/TikTok)
    
    Args:
        video_path: Path to input video
        output_path: Path to save resized video
        target_width: Target width in pixels (default 1080)
        target_height: Target height in pixels (default 1920)
    
    Returns:
        Path to resized video
    """
    try:
        clip = VideoFileClip(video_path)
        
        # Calculate aspect ratios
        original_aspect = clip.w / clip.h
        target_aspect = target_width / target_height
        
        # Resize and crop to fit vertical format
        if original_aspect > target_aspect:
            # Video is too wide, crop width
            new_width = int(clip.h * target_aspect)
            x_center = clip.w / 2
            clip = clip.crop(x_center=x_center, width=new_width, height=clip.h)
        else:
            # Video is too tall, crop height
            new_height = int(clip.w / target_aspect)
            y_center = clip.h / 2
            clip = clip.crop(y_center=y_center, width=clip.w, height=new_height)
        
        # Resize to target resolution
        clip = clip.resize((target_width, target_height))
        
        if not output_path:
            output_path = video_path.replace('.mp4', '_vertical.mp4')
        
        clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=30
        )
        
        clip.close()
        
        print(f"✓ Video resized to {target_width}x{target_height}: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error resizing video: {e}")
        raise e


def add_subtitles_to_video(video_path: str, subtitles_data: list, output_path: str = None):
    """
    Add subtitles to video (optional feature)
    
    Args:
        video_path: Path to video
        subtitles_data: List of dicts with {start, end, text}
        output_path: Path to save video with subtitles
    
    Returns:
        Path to video with subtitles
    """
    try:
        video = VideoFileClip(video_path)
        
        # Create subtitle clips
        subtitle_clips = []
        for sub in subtitles_data:
            txt_clip = (TextClip(
                sub['text'],
                fontsize=60,
                color='white',
                stroke_color='black',
                stroke_width=2,
                font='Arial-Bold',
                method='caption',
                size=(video.w * 0.9, None)
            )
            .set_position(('center', 0.8), relative=True)
            .set_start(sub['start'])
            .set_duration(sub['end'] - sub['start']))
            
            subtitle_clips.append(txt_clip)
        
        # Composite video with subtitles
        final_video = CompositeVideoClip([video] + subtitle_clips)
        
        if not output_path:
            output_path = video_path.replace('.mp4', '_subtitled.mp4')
        
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=30
        )
        
        video.close()
        final_video.close()
        
        print(f"✓ Subtitles added: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error adding subtitles: {e}")
        raise e


def create_thumbnail(video_path: str, output_path: str = None, timestamp: float = 1.0):
    """
    Extract thumbnail from video
    
    Args:
        video_path: Path to video
        output_path: Path to save thumbnail image
        timestamp: Timestamp to extract frame from (seconds)
    
    Returns:
        Path to thumbnail image
    """
    try:
        clip = VideoFileClip(video_path)
        
        # Get frame at timestamp
        frame = clip.get_frame(timestamp)
        
        # Save as image
        if not output_path:
            output_path = video_path.replace('.mp4', '_thumb.jpg')
        
        from PIL import Image
        img = Image.fromarray(frame)
        img.save(output_path, quality=85)
        
        clip.close()
        
        print(f"✓ Thumbnail created: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        raise e



def create_static_video_from_image(image_path: str, duration: float, output_path: str):
    """
    Create a static video clip from an image.
    Used as fallback when AI video generation fails.
    """
    try:
        clip = ImageClip(image_path).set_duration(duration)
        clip.write_videofile(
            output_path, 
            fps=24, 
            codec='libx264',
            audio_codec='aac'
        )
        clip.close()
        print(f"✓ Static video created: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error creating static video: {e}")
        return None


if __name__ == "__main__":
    print("Video processing module loaded successfully")
