"""
Celery Configuration for Background Task Processing
"""

from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

# Redis broker URL
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize Celery app
app = Celery(
    'ugc_video_generator',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['tasks.video_generation_task']
)

# Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=1800,  # 30 minutes max per task
    task_soft_time_limit=1500,  # 25 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=10,
    result_expires=3600,  # Results expire after 1 hour
)

# Optional: Configure periodic tasks (celery beat)
app.conf.beat_schedule = {
    # Add periodic tasks here if needed
}

if __name__ == '__main__':
    app.start()
