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
from typing import Optional

from scraper import scrape_jobs
from scraper.model import Site
from .utils import get_available_sites, get_country_from_location, process_jobs_dataframe, handle_null_values
from .pdf_utils import PDFGenerator
from .models import (
    JobSearchRequest, JobSearchResponse, JobPost,
    ResumeAnalysisResponse, ResumeResult, ResumeOutput,
    KeywordExtractionResponse, KeywordJobSearchRequest,
    CustomResumeRequest, CustomResumeResponse,
    JobResumeCustomizationRequest, JobResumeCustomizationResponse,
    LatexResumeResult, LatexResumeOutput
)

logger = logging.getLogger(__name__)


class JobService:
    """Service for handling job search operations."""
    
    @staticmethod
    def scrape_jobs_wrapper(location: str, search_keyword: str, results_wanted: int, is_remote: Optional[bool] = None) -> pd.DataFrame:
        """Wrapper function to scrape jobs from all available sites"""
        try:
            # Get available sites with location-based optimization
            sites = get_available_sites(location)
            
            # Determine appropriate country based on location
            country_code = get_country_from_location(location)
            
            logger.info(f"Starting job scraping for '{search_keyword}' in '{location}' from {len(sites)} sites")
            logger.info(f"Sites: {[site.value for site in sites]}")
            logger.info(f"Using country code: {country_code}")
            logger.info(f"Remote filter: {is_remote}")
            
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
            
            # If remote filtering is needed, request more jobs initially to account for filtering
            initial_results_wanted = results_wanted
            if is_remote is not None:
                # Request 2-3x more jobs to ensure we have enough after filtering
                initial_results_wanted = min(results_wanted * 3, 200)  # Cap at 200 (API limit)
                logger.info(f"Remote filtering enabled - requesting {initial_results_wanted} jobs initially to ensure {results_wanted} after filtering")
            
            # Scrape jobs from all sites
            jobs_df = scrape_jobs(
                site_name=sites,
                search_term=search_keyword,
                location=location,
                results_wanted=initial_results_wanted,
                hours_old=hours_old_param,  # Conditional hours_old parameter
                is_remote=is_remote if is_remote is not None else False,  # Pass the is_remote filter
                country_indeed=country_code,  # Use dynamic country detection
                verbose=2  # Increase verbosity to see more detailed logs
            )
            
            logger.info(f"Successfully scraped {len(jobs_df)} jobs")
            
            # Apply post-scraping filtering if needed
            if is_remote is not None and not jobs_df.empty:
                initial_count = len(jobs_df)
                if 'is_remote' in jobs_df.columns:
                    if is_remote:
                        # Filter for remote jobs only
                        jobs_df = jobs_df[jobs_df['is_remote'] == True]
                    else:
                        # Filter for non-remote jobs only
                        jobs_df = jobs_df[jobs_df['is_remote'] != True]
                    
                    filtered_count = len(jobs_df)
                    logger.info(f"Filtered jobs from {initial_count} to {filtered_count} based on remote preference")
                    
                    # If we still don't have enough jobs after filtering, try to get more
                    if filtered_count < results_wanted and initial_results_wanted < 200:
                        logger.info(f"Only {filtered_count} jobs after filtering, need {results_wanted}. Attempting additional scraping...")
                        additional_needed = results_wanted - filtered_count
                        additional_to_request = min(additional_needed * 2, 200 - initial_results_wanted)
                        
                        if additional_to_request > 0:
                            try:
                                additional_jobs_df = scrape_jobs(
                                    site_name=sites,
                                    search_term=search_keyword,
                                    location=location,
                                    results_wanted=additional_to_request,
                                    hours_old=hours_old_param,
                                    is_remote=is_remote if is_remote is not None else False,
                                    country_indeed=country_code,
                                    verbose=2
                                )
                                
                                if not additional_jobs_df.empty:
                                    # Apply the same filtering to additional jobs
                                    if 'is_remote' in additional_jobs_df.columns:
                                        if is_remote:
                                            additional_jobs_df = additional_jobs_df[additional_jobs_df['is_remote'] == True]
                                        else:
                                            additional_jobs_df = additional_jobs_df[additional_jobs_df['is_remote'] != True]
                                    
                                    # Combine with existing jobs, avoiding duplicates
                                    if 'job_url' in jobs_df.columns and 'job_url' in additional_jobs_df.columns:
                                        # Remove duplicates based on job_url
                                        existing_urls = set(jobs_df['job_url'].tolist())
                                        additional_jobs_df = additional_jobs_df[~additional_jobs_df['job_url'].isin(existing_urls)]
                                    
                                    jobs_df = pd.concat([jobs_df, additional_jobs_df], ignore_index=True)
                                    logger.info(f"Added {len(additional_jobs_df)} additional jobs, total now: {len(jobs_df)}")
                            except Exception as e:
                                logger.warning(f"Failed to get additional jobs: {str(e)}")
            
            # Limit to exact results_wanted
            if len(jobs_df) > results_wanted:
                jobs_df = jobs_df.head(results_wanted)
                logger.info(f"Limited results to exactly {results_wanted} jobs as requested")
            
            # Add debugging to see which sites returned jobs
            if not jobs_df.empty and 'site' in jobs_df.columns:
                site_counts = jobs_df['site'].value_counts()
                logger.info(f"Jobs by site: {site_counts.to_dict()}")
            
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
                    request.results_wanted,
                    request.is_remote
                )
            
            # Process the results
            if jobs_df.empty:
                # Provide more informative message when no jobs are found
                remote_filter_msg = ""
                if request.is_remote is not None:
                    remote_filter_msg = f" (remote filter: {'remote only' if request.is_remote else 'non-remote only'})"
                
                message = f"No jobs found for '{request.search_keyword}' in '{request.location}'{remote_filter_msg}. This could be due to site restrictions, rate limiting, or no matching jobs available."
                response_data = {
                    "success": True,
                    "message": message,
                    "total_jobs": 0,
                    "jobs": [],
                    "search_params": {
                        "location": request.location,
                        "search_keyword": request.search_keyword,
                        "results_wanted": request.results_wanted,
                        "is_remote": request.is_remote
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
                        "results_wanted": request.results_wanted,
                        "is_remote": request.is_remote
                    },
                    "timestamp": datetime.now().isoformat()
                }
            
            return JobSearchResponse(**response_data)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in search_jobs: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to search jobs: {str(e)}"
            )


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
                results_wanted=request.results_wanted,
                is_remote=request.is_remote
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
            async with httpx.AsyncClient(timeout=60.0) as client:
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
            async with httpx.AsyncClient(timeout=60.0) as client:
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
                        timestamp=datetime.now().isoformat(),
                        pdf_available=True
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
    
    @staticmethod
    async def build_custom_resume_pdf(request: CustomResumeRequest) -> bytes:
        """Generate a tailored PDF resume based on job details and resume information."""
        try:
            # Get LaTeX code first
            latex_response = await ResumeService.build_custom_resume(request)
            
            # Parse the LaTeX code if it's in JSON format
            latex_code = latex_response.latex_code
            try:
                latex_data = json.loads(latex_code)
                if latex_data.get("result", {}).get("Output", {}).get("latex_resume"):
                    latex_code = latex_data["result"]["Output"]["latex_resume"]
            except (json.JSONDecodeError, KeyError):
                # If it's not JSON or doesn't have the expected structure, use as is
                pass
            
            # Generate PDF from LaTeX
            pdf_bytes = PDFGenerator.generate_pdf_from_latex(latex_code)
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate PDF resume"
            )
    
    @staticmethod
    async def customize_resume_for_job_pdf(request: JobResumeCustomizationRequest) -> bytes:
        """Generate a customized PDF resume for a specific job."""
        try:
            # Get LaTeX code first
            latex_response = await ResumeService.customize_resume_for_job(request)
            
            # Extract LaTeX code from the response
            latex_code = latex_response.result.Output.latex_resume
            
            # Generate PDF from LaTeX
            pdf_bytes = PDFGenerator.generate_pdf_from_latex(latex_code)
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Error generating PDF for job customization: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate PDF resume for job"
            )

    @staticmethod
    async def customize_resume_for_job(request: JobResumeCustomizationRequest) -> JobResumeCustomizationResponse:
        """Generate a customized LaTeX resume for a specific job."""
        try:
            # Validate input
            if not request.job_description or not request.job_description.strip():
                raise HTTPException(status_code=400, detail="Job description is required and cannot be empty")
            
            if not request.resume_data or not request.resume_data.strip():
                raise HTTPException(status_code=400, detail="Resume data is required and cannot be empty")
            
            # Prepare the payload for the external API
            job_details = f"""
            Job Title: {request.job_title}
            Company: {request.company_name}
            Job Description: {request.job_description}
            """
            
            payload = {
                "job_details": job_details.strip(),
                "resume_details": request.resume_data.strip()
            }
            
            # Make request to the external LaTeX resume generator API
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    os.getenv("CUSTOM_RESUME_BUILDER_API_URL"),
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    latex_code = response.text
                    return JobResumeCustomizationResponse(
                        result=LatexResumeResult(
                            Output=LatexResumeOutput(latex_resume=latex_code)
                        )
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
            logger.error(f"Unexpected error in customize_resume_for_job: {e}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while generating the resume"
            )