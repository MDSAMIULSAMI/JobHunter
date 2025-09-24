"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class JobSearchRequest(BaseModel):
    location: str = Field(default="India", description="Location to search for jobs (required)")
    search_keyword: str = Field(..., description="Search keyword (required)")
    results_wanted: Optional[int] = Field(default=10, ge=1, le=200, description="Number of results wanted (1-200)")


class JobPost(BaseModel):
    id: Optional[str] = None
    title: str
    company_name: Optional[str] = None
    job_url: str
    location: Optional[str] = None
    description: Optional[str] = None
    company_url: Optional[str] = None
    job_type: Optional[str] = None
    date_posted: Optional[str] = None
    is_remote: Optional[bool] = None
    site: str
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    currency: Optional[str] = None
    interval: Optional[str] = None


class JobSearchResponse(BaseModel):
    success: bool
    message: str
    total_jobs: int
    jobs: List[JobPost]
    search_params: Dict[str, Any]
    timestamp: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str


class ResumeOutput(BaseModel):
    search_keywords: str = Field(default="Not provided or Not found")
    email: str = Field(default="Not provided or Not found")
    phone: str = Field(default="Not provided or Not found")
    education: str = Field(default="Not provided or Not found")
    name: str = Field(default="Not provided or Not found")
    skills: str = Field(default="Not provided or Not found")
    experience: str = Field(default="Not provided or Not found")
    field_of_interest: str = Field(default="Not provided or Not found")
    achievements: str = Field(default="Not provided or Not found")
    certifications: str = Field(default="Not provided or Not found")
    projects: str = Field(default="Not provided or Not found")
    languages: str = Field(default="Not provided or Not found")


class ResumeResult(BaseModel):
    Output: ResumeOutput


class ResumeAnalysisResponse(BaseModel):
    id: str
    name: str
    result: ResumeResult


# New models for keyword extraction and job search integration
class KeywordExtractionResponse(BaseModel):
    success: bool
    resume_data: ResumeOutput
    timestamp: str


class KeywordJobSearchRequest(BaseModel):
    selected_keyword: str = Field(..., description="Selected keyword from resume analysis")
    location: str = Field(default="India", description="Location to search for jobs")
    results_wanted: Optional[int] = Field(default=10, ge=1, le=200, description="Number of results wanted (1-200)")


class CustomResumeRequest(BaseModel):
    job_details: str = Field(..., description="Job details/description for tailoring the resume")
    resume_details: str = Field(..., description="Resume information to be tailored")


class CustomResumeResponse(BaseModel):
    success: bool
    latex_code: str
    message: str
    timestamp: str