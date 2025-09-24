"""
API route handlers for the FastAPI application.
"""

from fastapi import APIRouter, HTTPException, Query, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Dict, Any
from datetime import datetime

from .models import (
    JobSearchRequest, JobSearchResponse, 
    ResumeAnalysisResponse, CustomResumeRequest, CustomResumeResponse
)
from .services import JobService, ResumeService
from .utils import get_available_sites
from scraper.model import Site

# Create routers for different endpoint groups
job_router = APIRouter(prefix="/jobs", tags=["jobs"])
resume_router = APIRouter(prefix="/resume", tags=["resume"])
general_router = APIRouter(tags=["general"])


@general_router.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "JobSpy FastAPI - Job Aggregation Service",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }


@general_router.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "JobSpy FastAPI",
        "version": "1.0.0"
    }


@job_router.post("/search", response_model=JobSearchResponse)
async def search_jobs_post(request: JobSearchRequest):
    """
    Search for jobs based on location and keyword
    
    - **location**: Location to search for jobs (required)
    - **search_keyword**: Search keyword/term (required) 
    - **results_wanted**: Number of results wanted (1-500, default: 50)
    
    Returns jobs from the last 72 hours from all available job boards.
    """
    try:
        return await JobService.search_jobs(request)
    except HTTPException:
        raise
    except Exception as e:
        # Return a more user-friendly error response instead of generic 500
        return JSONResponse(
            status_code=200,  # Return 200 but with success: false
            content={
                "success": False,
                "message": f"Unable to complete job search due to technical issues. Many job sites may be blocking requests or experiencing issues. Error: {str(e)}",
                "total_jobs": 0,
                "jobs": [],
                "search_params": {
                    "location": request.location,
                    "search_keyword": request.search_keyword,
                    "results_wanted": request.results_wanted
                },
                "timestamp": datetime.now().isoformat()
            }
        )


@job_router.get("/search", response_model=JobSearchResponse)
async def search_jobs_get(
    location: str = Query(default="India", description="Location to search for jobs"),
    search_keyword: str = Query(..., description="Search keyword"),
    results_wanted: int = Query(default=10, ge=1, le=200, description="Number of results wanted")
):
    """
    GET endpoint for job search (alternative to POST)
    """
    request = JobSearchRequest(
        location=location,
        search_keyword=search_keyword,
        results_wanted=results_wanted
    )
    return await search_jobs_post(request)


@job_router.get("/available-sites", response_model=Dict[str, Any])
async def get_available_sites_endpoint():
    """Get list of available job sites"""
    return {
        "available_sites": [
            {
                "name": site.value,
                "description": f"Jobs from {site.value.replace('_', ' ').title()}"
            }
            for site in Site
        ]
    }


@resume_router.post("/upload", response_model=ResumeAnalysisResponse)
async def upload_resume(resume_file: UploadFile = File(..., description="Resume PDF file to analyze")):
    """
    Upload a resume PDF file for analysis and job matching
    """
    # Validate file type
    if not resume_file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    # Read the file content
    file_content = await resume_file.read()
    
    return await ResumeService.analyze_resume(file_content, resume_file.filename)


@resume_router.post("/custom-builder", response_model=CustomResumeResponse)
async def custom_resume_builder(request: CustomResumeRequest):
    """
    Generate a tailored LaTeX resume code based on job details and resume information
    
    - **job_details**: Job details/description for tailoring the resume (required)
    - **resume_details**: Resume information to be tailored (required)
    
    Returns LaTeX code for a tailored resume.
    """
    return await ResumeService.build_custom_resume(request)


# Legacy endpoints for backward compatibility
@general_router.post("/search-jobs", response_model=JobSearchResponse)
async def search_jobs_legacy(request: JobSearchRequest):
    """Legacy endpoint - use /jobs/search instead"""
    return await search_jobs_post(request)


@general_router.get("/search-jobs", response_model=JobSearchResponse)
async def search_jobs_get_legacy(
    location: str = Query(default="India", description="Location to search for jobs"),
    search_keyword: str = Query(..., description="Search keyword"),
    results_wanted: int = Query(default=10, ge=1, le=200, description="Number of results wanted")
):
    """Legacy endpoint - use /jobs/search instead"""
    return await search_jobs_get(location, search_keyword, results_wanted)


@general_router.get("/available-sites", response_model=Dict[str, Any])
async def get_available_sites_legacy():
    """Legacy endpoint - use /jobs/available-sites instead"""
    return await get_available_sites_endpoint()


@general_router.post("/upload-resume", response_model=ResumeAnalysisResponse)
async def upload_resume_legacy(resume_file: UploadFile = File(..., description="Resume PDF file to analyze")):
    """Legacy endpoint - use /resume/upload instead"""
    return await upload_resume(resume_file)


@general_router.post("/custom-resume-builder", response_model=CustomResumeResponse)
async def custom_resume_builder_legacy(request: CustomResumeRequest):
    """Legacy endpoint - use /resume/custom-builder instead"""
    return await custom_resume_builder(request)