from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class AnalyticsRecord(Base):
    """
    Model for storing analytics data records.
    """
    __tablename__ = "analytics_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)
    meta_data = Column(JSON, nullable=True)  # Store additional data as JSON
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "value": self.value,
            "metadata": self.meta_data,  # Return as 'metadata' in API responses
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class VideoJob(Base):
    """
    Model for tracking background video generation jobs.
    Replaces Celery/Redis for simple local deployment.
    """
    __tablename__ = "video_jobs"
    
    id = Column(String(36), primary_key=True, index=True) # UUID
    status = Column(String(50), default="pending") # pending, processing, completed, failed
    progress = Column(Integer, default=0)
    message = Column(String(255), default="Initializing...")
    result = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "task_id": self.id,
            "status": self.status,
            "progress": self.progress,
            "message": self.message,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat()
        }

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), "analytics.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
