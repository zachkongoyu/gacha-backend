"""AI service main application for content generation."""

from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import uuid
from datetime import datetime

from shared.auth import decode_access_token
from shared.database import create_db_pool, close_db_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan (startup and shutdown)."""
    # Startup
    await create_db_pool()
    yield
    # Shutdown
    await close_db_pool()


app = FastAPI(
    title="AI Service",
    description="AI content generation service",
    version="0.1.0",
    lifespan=lifespan,
)


class JobRequest(BaseModel):
    """AI job creation request."""

    job_type: str  # e.g., "character_art", "item_description", "story"
    parameters: Dict[str, Any]


class JobResponse(BaseModel):
    """AI job response."""

    job_id: str
    job_type: str
    status: str  # queued, processing, completed, failed
    created_at: str
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {"service": "ai", "status": "running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """Extract user ID from JWT token."""
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.split(" ")[1]
    token_data = decode_access_token(token)

    if token_data is None:
        return None

    return token_data.user_id


@app.post("/jobs", response_model=JobResponse)
async def create_job(job_request: JobRequest, authorization: Optional[str] = Header(None)):
    """
    Create a new AI generation job.

    Args:
        job_request: Job configuration
        authorization: JWT token in Authorization header

    Returns:
        Created job details
    """
    user_id = get_current_user(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Generate job ID
    job_id = str(uuid.uuid4())

    # Stub job creation (in real implementation, queue to background worker)
    return JobResponse(
        job_id=job_id,
        job_type=job_request.job_type,
        status="queued",
        created_at=datetime.utcnow().isoformat() + "Z",
    )


@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, authorization: Optional[str] = Header(None)):
    """
    Get status and results of an AI job.

    Args:
        job_id: Job ID
        authorization: JWT token in Authorization header

    Returns:
        Job details and results
    """
    user_id = get_current_user(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Stub job status (in real implementation, fetch from database/queue)
    return JobResponse(
        job_id=job_id,
        job_type="character_art",
        status="completed",
        created_at="2026-01-01T00:00:00Z",
        completed_at="2026-01-01T00:05:00Z",
        result={
            "image_url": f"https://cdn.example.com/generated/{job_id}.png",
            "prompt_used": "A fantasy character with magical powers",
            "model_version": "v1.0",
        },
    )


@app.get("/jobs")
async def list_jobs(
    status: Optional[str] = None,
    job_type: Optional[str] = None,
    authorization: Optional[str] = Header(None),
):
    """
    List user's AI jobs.

    Args:
        status: Optional filter by status
        job_type: Optional filter by job type
        authorization: JWT token in Authorization header

    Returns:
        List of jobs
    """
    user_id = get_current_user(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Stub job list
    jobs = [
        {
            "job_id": "job_001",
            "job_type": "character_art",
            "status": "completed",
            "created_at": "2026-01-01T00:00:00Z",
        },
        {
            "job_id": "job_002",
            "job_type": "item_description",
            "status": "processing",
            "created_at": "2026-01-02T00:00:00Z",
        },
    ]

    # Apply filters
    if status:
        jobs = [job for job in jobs if job["status"] == status]
    if job_type:
        jobs = [job for job in jobs if job["job_type"] == job_type]

    return {"jobs": jobs, "total": len(jobs)}


@app.get("/models")
async def list_models():
    """
    List available AI models and capabilities.

    Returns:
        Available models
    """
    return {
        "models": [
            {
                "model_id": "character_art_v1",
                "name": "Character Art Generator v1",
                "type": "character_art",
                "capabilities": ["fantasy", "sci-fi", "modern"],
                "cost_per_generation": 10,
            },
            {
                "model_id": "description_v1",
                "name": "Item Description Generator v1",
                "type": "item_description",
                "capabilities": ["weapons", "characters", "materials"],
                "cost_per_generation": 5,
            },
        ]
    }
