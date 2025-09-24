"""
Business logic services for job scraping and resume analysis.
"""

import pandas as pd
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import os
import httpx
import json
import re
from datetime import datetime
from typing import List
from fastapi import HTTPException

from scraper import scrape_jobs
from scraper.model import Site
from .utils import get_available_sites, get_country_from_location, process_jobs_dataframe, handle_null_values
from .models import (
    JobSearchRequest, JobSearchResponse, JobPost,
    ResumeAnalysisResponse, ResumeResult, ResumeOutput,
    KeywordExtractionResponse, KeywordJobSearchRequest,
    CustomResumeRequest, CustomResumeResponse
)

logger = logging.getLogger(__name__)


class JobService:
    """Service for handling job search operations."""
    
    @staticmethod
    def scrape_jobs_wrapper(location: str, search_keyword: str, results_wanted: int) -> pd.DataFrame:
        """Wrapper function to scrape jobs from all available sites"""
        try:
            # Get available sites with location-based optimization
            sites = get_available_sites(location)
            
            # Determine appropriate country based on location
            country_code = get_country_from_location(location)
            
            logger.info(f"Starting job scraping for '{search_keyword}' in '{location}' from {len(sites)} sites")
            logger.info(f"Sites: {[site.value for site in sites]}")
            logger.info(f"Using country code: {country_code}")
            
            # Check if we're dealing with Bangladesh locations (BDJobs)
            location_lower = location.lower().strip()
            bangladesh_keywords = ['bangladesh', 'dhaka', 'chittagong', 'sylhet', 'rajshahi', 'khulna', 'barisal', 'rangpur', 'mymensingh']
            is_bangladesh = any(keyword in location_lower for keyword in bangladesh_keywords)
            
            # Adjust hours_old based on location and sites
            if is_bangladesh and hasattr(Site, 'BDJOBS') and Site.BDJOBS in sites:
                # For Bangladesh/BDJobs, don't use hours_old filter as BDJobs may not have proper date parsing
                logger.info("Bangladesh location with BDJobs detected - removing hours_old filter for better results")
                hours_old_param = None
            else:
                # For other locations/sites, use 72-hour filter
                hours_old_param = 72
            
            # Scrape jobs from all sites
            jobs_df = scrape_jobs(
                site_name=sites,
                search_term=search_keyword,
                location=location,
                results_wanted=results_wanted,
                hours_old=hours_old_param,  # Conditional hours_old parameter
                is_remote=False,  # Include both remote and on-site jobs
                country_indeed=country_code,  # Use dynamic country detection
                verbose=1
            )
            
            logger.info(f"Successfully scraped {len(jobs_df)} jobs")
            return jobs_df
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error scraping jobs: {error_msg}")
            
            # Don't raise HTTPException here, let the calling function handle it
            # Return empty DataFrame instead so the API can still respond gracefully
            logger.warning("Returning empty DataFrame due to scraping errors")
            return pd.DataFrame()
    
    @staticmethod
    async def search_jobs(request: JobSearchRequest) -> JobSearchResponse:
        """Search for jobs based on request parameters."""
        try:
            # Input validation
            if not request.location or not request.location.strip():
                raise HTTPException(status_code=400, detail="Location is required and cannot be empty")
            
            if not request.search_keyword or not request.search_keyword.strip():
                raise HTTPException(status_code=400, detail="Search keyword is required and cannot be empty")
            
            # Scrape jobs in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                jobs_df = await loop.run_in_executor(
                    executor, 
                    JobService.scrape_jobs_wrapper,
                    request.location,
                    request.search_keyword,
                    request.results_wanted
                )
            
            # Process the results
            if jobs_df.empty:
                # Provide more informative message when no jobs are found
                message = f"No jobs found for '{request.search_keyword}' in '{request.location}'. This could be due to site restrictions, rate limiting, or no matching jobs available."
                response_data = {
                    "success": True,
                    "message": message,
                    "total_jobs": 0,
                    "jobs": [],
                    "search_params": {
                        "location": request.location,
                        "search_keyword": request.search_keyword,
                        "results_wanted": request.results_wanted
                    },
                    "timestamp": datetime.now().isoformat()
                }
            else:
                jobs_list = process_jobs_dataframe(jobs_df)
                
                # Ensure we don't return more jobs than requested
                if len(jobs_list) > request.results_wanted:
                    jobs_list = jobs_list[:request.results_wanted]
                    logger.info(f"Limited final results to {request.results_wanted} as requested")
                
                response_data = {
                    "success": True,
                    "message": f"Successfully found {len(jobs_list)} jobs",
                    "total_jobs": len(jobs_list),
                    "jobs": jobs_list,
                    "search_params": {
                        "location": request.location,
                        "search_keyword": request.search_keyword,
                        "results_wanted": request.results_wanted
                    },
                    "timestamp": datetime.now().isoformat()
                }
            
            return JobSearchResponse(**response_data)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in search_jobs: {str(e)}")
            # Return a more user-friendly error response instead of generic 500
            response_data = {
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
            return JobSearchResponse(**response_data)


class ResumeService:
    """Service for handling resume analysis and generation."""
    
    @staticmethod
    def extract_keywords_from_resume_data(resume_data: ResumeOutput) -> List[str]:
        """Extract meaningful keywords from resume data for job searching."""
        keywords = set()
        
        # First priority: Extract from search_keywords if available (JSON string format)
        if resume_data.search_keywords and resume_data.search_keywords != "Not provided or Not found":
            try:
                # Try to parse as JSON array first
                import json
                search_keywords_list = json.loads(resume_data.search_keywords)
                if isinstance(search_keywords_list, list):
                    for keyword in search_keywords_list:
                        if isinstance(keyword, str) and len(keyword.strip()) > 2:
                            keywords.add(keyword.strip())
            except (json.JSONDecodeError, TypeError):
                # If JSON parsing fails, treat as comma-separated string
                search_text = resume_data.search_keywords.lower()
                search_items = re.split(r'[,;|\n•·-]', search_text)
                for keyword in search_items:
                    keyword = keyword.strip()
                    if len(keyword) > 2:
                        keywords.add(keyword.title())
        
        # Second priority: Extract from field of interest
        if resume_data.field_of_interest and resume_data.field_of_interest != "Not provided or Not found":
            field_text = resume_data.field_of_interest.lower()
            field_items = re.split(r'[,;|\n•·-]', field_text)
            for field in field_items:
                field = field.strip()
                if len(field) > 2:
                    keywords.add(field.title())
        
        # Third priority: Extract from skills
        if resume_data.skills and resume_data.skills != "Not provided or Not found":
            skills_text = resume_data.skills.lower()
            # Split by common delimiters and clean up
            skill_items = re.split(r'[,;|\n•·-]', skills_text)
            for skill in skill_items:
                skill = skill.strip()
                if len(skill) > 2 and skill not in ['and', 'or', 'the', 'with', 'using']:
                    keywords.add(skill.title())
        
        # Fourth priority: Extract from experience (job titles and technologies)
        if resume_data.experience and resume_data.experience != "Not provided or Not found":
            exp_text = resume_data.experience.lower()
            # Look for common job titles and technologies
            job_patterns = [
                r'\b(developer|engineer|analyst|manager|designer|consultant|specialist|coordinator|administrator|architect|lead|senior|junior)\b',
                r'\b(python|java|javascript|react|node|angular|vue|django|flask|spring|sql|mongodb|postgresql|mysql|aws|azure|docker|kubernetes)\b'
            ]
            for pattern in job_patterns:
                matches = re.findall(pattern, exp_text)
                for match in matches:
                    keywords.add(match.title())
        
        # Convert to sorted list and limit to reasonable number
        keyword_list = sorted(list(keywords))[:20]  # Limit to top 20 keywords
        
        # If no keywords found, provide some defaults based on available data
        if not keyword_list:
            if resume_data.field_of_interest and resume_data.field_of_interest != "Not provided or Not found":
                keyword_list = [resume_data.field_of_interest]
            else:
                keyword_list = ["Software Developer", "Data Analyst", "Project Manager"]
        
        return keyword_list
    
    @staticmethod
    async def analyze_resume_with_keywords(file_content: bytes, filename: str) -> KeywordExtractionResponse:
        """Analyze resume PDF file and return resume data with search keywords."""
        try:
            # First, get the standard resume analysis
            resume_analysis = await ResumeService.analyze_resume(file_content, filename)
            
            # Return the response with only resume data (which includes search_keywords)
            return KeywordExtractionResponse(
                success=True,
                resume_data=resume_analysis.result.Output,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error in analyze_resume_with_keywords: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze resume: {str(e)}"
            )
    
    @staticmethod
    async def search_jobs_by_keyword(request: KeywordJobSearchRequest) -> JobSearchResponse:
        """Search for jobs using a selected keyword from resume analysis."""
        try:
            # Create a job search request
            job_request = JobSearchRequest(
                location=request.location,
                search_keyword=request.selected_keyword,
                results_wanted=request.results_wanted
            )
            
            # Use the existing job search functionality
            return await JobService.search_jobs(job_request)
            
        except Exception as e:
            logger.error(f"Error in search_jobs_by_keyword: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to search jobs by keyword: {str(e)}"
            )
    
    @staticmethod
    async def analyze_resume(file_content: bytes, filename: str) -> ResumeAnalysisResponse:
        """Analyze resume PDF file."""
        try:
            # Prepare the file for the external API
            files = {
                'resume_file': (filename, file_content, 'application/pdf')
            }
            
            # Send request to the resume analysis API
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    os.getenv("RESUME_ANALYZER_API_URL"),
                    files=files
                )
                
                if response.status_code == 200:
                    # Parse the response from the external API
                    try:
                        # Assuming the external API returns JSON in the format you specified
                        api_response = response.json()
                        
                        # If the API returns the exact format, handle null values in the nested structure
                        if isinstance(api_response, dict) and "result" in api_response:
                            if "Output" in api_response["result"]:
                                api_response["result"]["Output"] = handle_null_values(api_response["result"]["Output"])
                            return ResumeAnalysisResponse(**api_response)
                        
                        # If the API returns just the output data, wrap it in the expected format
                        elif isinstance(api_response, dict):
                            processed_data = handle_null_values(api_response)
                            return ResumeAnalysisResponse(
                                id="M1RESUME07",
                                name="APIOutput",
                                result=ResumeResult(Output=ResumeOutput(**processed_data))
                            )
                        
                        # If the API returns a string, try to parse it as JSON
                        else:
                            parsed_data = json.loads(response.text)
                            processed_data = handle_null_values(parsed_data)
                            return ResumeAnalysisResponse(
                                id="M1RESUME07",
                                name="APIOutput",
                                result=ResumeResult(Output=ResumeOutput(**processed_data))
                            )
                            
                    except (json.JSONDecodeError, KeyError, TypeError) as e:
                        logger.error(f"Failed to parse API response: {e}")
                        # Return a default structure if parsing fails
                        default_data = handle_null_values({})
                        return ResumeAnalysisResponse(
                            id="M1RESUME07",
                            name="APIOutput",
                            result=ResumeResult(Output=ResumeOutput(**default_data))
                        )
                else:
                    logger.error(f"External API error: {response.status_code} - {response.text}")
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Resume analysis failed: {response.text}"
                    )
                    
        except httpx.TimeoutException:
            logger.error("Timeout while connecting to resume analysis service")
            raise HTTPException(
                status_code=504,
                detail="Resume analysis service timeout"
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise HTTPException(
                status_code=503,
                detail="Unable to connect to resume analysis service"
            )
        except Exception as e:
            logger.error(f"Unexpected error during resume upload: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
    
    @staticmethod
    async def build_custom_resume(request: CustomResumeRequest) -> CustomResumeResponse:
        """Generate a tailored LaTeX resume code based on job details and resume information."""
        try:
            # Validate input
            if not request.job_details or not request.job_details.strip():
                raise HTTPException(status_code=400, detail="Job details are required and cannot be empty")
            
            if not request.resume_details or not request.resume_details.strip():
                raise HTTPException(status_code=400, detail="Resume details are required and cannot be empty")
            
            # Prepare the payload for the external API
            payload = {
                "job_details": request.job_details.strip(),
                "resume_details": request.resume_details.strip()
            }
            
            # Make request to the external LaTeX resume generator API
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    os.getenv("CUSTOM_RESUME_BUILDER_API_URL"),
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    latex_code = response.text
                    return CustomResumeResponse(
                        success=True,
                        latex_code=latex_code,
                        message="LaTeX resume code generated successfully",
                        timestamp=datetime.now().isoformat()
                    )
                else:
                    logger.error(f"External API error: {response.status_code} - {response.text}")
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"External API error: {response.text}"
                    )
                    
        except httpx.TimeoutException:
            logger.error("Timeout while calling external resume generator API")
            raise HTTPException(
                status_code=504,
                detail="Request timeout while generating resume. Please try again."
            )
        except httpx.RequestError as e:
            logger.error(f"Request error while calling external API: {e}")
            raise HTTPException(
                status_code=503,
                detail="Unable to connect to resume generator service. Please try again later."
            )
        except Exception as e:
            logger.error(f"Unexpected error in custom_resume_builder: {e}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while generating the resume"
            )