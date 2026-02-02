from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",  # React default port
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

