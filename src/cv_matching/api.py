"""FastAPI application for CV matching service."""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .config import settings
from .models import MatchingRequest, MatchingResponse
from .matcher import CVMatchingService
from .profiler import profiler
import uuid


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered CV-Job Description matching system using OpenAI LLM",
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize CV matching service
cv_service = CVMatchingService()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "CV Matching API",
        "version": settings.app_version,
        "status": "active",
        "endpoints": {
            "match": "/match",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "CV Matching API",
        "version": settings.app_version
    }


@app.post("/match")
async def match_cv_to_job(request: dict):
    """
    Match CV against job description.
    """
    session_id = str(uuid.uuid4())[:8]
    profiler.start_session(session_id)
    
    try:
        with profiler.time_block("Request Processing", details=f"Input size: {len(str(request))} chars"):
            # Pass whatever the user sends directly to LLM
            response = await cv_service.match_cv_to_job_raw(request)
            
            # Add profiling data to response before ending session
            response["profiling"] = profiler.get_session_summary(session_id)
            return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CV matching failed: {str(e)}"
        )
    finally:
        profiler.end_session(session_id)


@app.post("/match/summary")
async def get_matching_summary(request: dict):
    """
    Get a summary of CV matching results.
    """
    try:
        # Pass whatever the user sends directly to LLM
        response = await cv_service.match_cv_to_job_raw(request)
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CV matching failed: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


def run_server():
    """Run the FastAPI server."""
    uvicorn.run(
        "cv_matching.api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )
    
if __name__ == "__main__":
    run_server()
