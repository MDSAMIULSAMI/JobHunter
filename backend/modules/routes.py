"""
API route handlers for the FastAPI application.
"""

from fastapi import APIRouter, HTTPException, Query, File, UploadFile
from fastapi.responses import JSONResponse, Response
from typing import Dict, Any
from datetime import datetime
import json
from .pdf_utils import PDFGenerator

from .models import (
    JobSearchRequest, JobSearchResponse, 
    ResumeAnalysisResponse, CustomResumeRequest, CustomResumeResponse,
    KeywordExtractionResponse, KeywordJobSearchRequest,
    JobResumeCustomizationRequest, JobResumeCustomizationResponse
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
        "message": "JobHunter FastAPI - Job Aggregation Service",
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
        "service": "JobHunter FastAPI",
        "version": "1.0.6"
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


@resume_router.post("/upload-with-keywords", response_model=KeywordExtractionResponse)
async def upload_resume_with_keywords(resume_file: UploadFile = File(..., description="Resume PDF file to analyze and extract keywords")):
    """
    Upload a resume PDF file for analysis and extract keywords for job searching
    
    This endpoint analyzes the resume and extracts relevant keywords that can be used
    for job searching. Users can then select from these keywords to conduct targeted job searches.
    """
    # Validate file type
    if not resume_file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    # Read the file content
    file_content = await resume_file.read()
    
    return await ResumeService.analyze_resume_with_keywords(file_content, resume_file.filename)


@resume_router.post("/search-by-keyword", response_model=JobSearchResponse)
async def search_jobs_by_keyword(request: KeywordJobSearchRequest):
    """
    Search for jobs using a selected keyword from resume analysis
    
    - **selected_keyword**: Keyword selected from resume analysis (required)
    - **location**: Location to search for jobs (default: India)
    - **results_wanted**: Number of results wanted (1-200, default: 10)
    
    This endpoint is typically used after uploading a resume and selecting a keyword
    from the extracted keywords list.
    """
    return await ResumeService.search_jobs_by_keyword(request)


@resume_router.post("/custom-builder", response_model=CustomResumeResponse)
async def custom_resume_builder(request: CustomResumeRequest):
    """
    Generate a tailored LaTeX resume code based on job details and resume information
    
    - **job_details**: Job details/description for tailoring the resume (required)
    - **resume_details**: Resume information to be tailored (required)
    
    Returns LaTeX code for a tailored resume.
    """
    return await ResumeService.build_custom_resume(request)


@resume_router.post("/custom-builder/pdf")
async def custom_resume_builder_pdf(request: CustomResumeRequest):
    """
    Generate a tailored PDF resume based on job details and resume information
    
    - **job_details**: Job details/description for tailoring the resume (required)
    - **resume_details**: Resume information to be tailored (required)
    
    Returns PDF file for download.
    """
    # Get the custom resume response which contains the LaTeX code
    latex_response = await ResumeService.build_custom_resume(request)
    
    # Normalize LaTeX code so the PDF generator can use it
    latex_code = latex_response.latex_code
    try:
        parsed = json.loads(latex_code)
        if isinstance(parsed, dict):
            # Try the expected nested path
            candidate = parsed.get("result", {}).get("Output", {}).get("latex_resume")
            if isinstance(candidate, str):
                latex_code = candidate
            else:
                # Fallback: look for common top-level keys
                for key in ("latex_resume", "latex_code"):
                    val = parsed.get(key)
                    if isinstance(val, str):
                        latex_code = val
                        break
        elif isinstance(parsed, str):
            # If the JSON is just a LaTeX string, use it directly
            latex_code = parsed
    except json.JSONDecodeError:
        # Not JSON, keep as-is and try to unescape common sequences
        pass

    # Convert literal escaped sequences to their actual characters
    if "\\n" in latex_code and "\n" not in latex_code:
        latex_code = latex_code.replace("\\n", "\n")
    if "\\t" in latex_code and "\t" not in latex_code:
        latex_code = latex_code.replace("\\t", "\t")
    if latex_code.startswith('"') and latex_code.endswith('"'):
        latex_code = latex_code[1:-1]
    
    # Generate PDF from the LaTeX code
    pdf_bytes = PDFGenerator.generate_pdf_from_latex(latex_code)
    
    # Return the PDF file
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=customized_resume.pdf"
        }
    )


@resume_router.post("/customize-for-job/pdf")
async def customize_resume_for_job_pdf(request: JobResumeCustomizationRequest):
    """
    Generate a customized PDF resume for a specific job
    
    - **job_id**: Job ID for customization (required)
    - **job_title**: Job title (required)
    - **job_description**: Job description (required)
    - **company_name**: Company name (required)
    - **resume_data**: Resume data in string format (required)
    
    Returns PDF file for download.
    """
    pdf_bytes = await ResumeService.customize_resume_for_job_pdf(request)
    
    filename = f"resume_{request.job_title.replace(' ', '_').lower()}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


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

@resume_router.post("/customize-for-job", response_model=JobResumeCustomizationResponse)
async def customize_resume_for_job(request: JobResumeCustomizationRequest):
    """
    Generate a customized LaTeX resume for a specific job
    
    - **job_id**: Job ID for customization (required)
    - **job_title**: Job title (required)
    - **job_description**: Job description (required)
    - **company_name**: Company name (required)
    - **resume_data**: Resume data in string format (required)
    
    Returns LaTeX code for a job-specific tailored resume in the specified JSON structure.
    """
    return await ResumeService.customize_resume_for_job(request)