"""
Utility functions for the FastAPI application.
"""

import pandas as pd
from datetime import date, datetime
from typing import List
import logging

from .models import JobPost
from scraper.model import Site

logger = logging.getLogger(__name__)

# Check if BDJobs is available
try:
    BDJOBS_AVAILABLE = hasattr(Site, 'BDJOBS')
except:
    BDJOBS_AVAILABLE = False


def get_available_sites(location: str = None) -> List[Site]:
    """Get list of available sites, with proper regional optimization"""
    available_sites = []
    
    if not location:
        # Default sites when no location specified - only working sites
        return [Site.LINKEDIN, Site.INDEED, Site.GLASSDOOR]
    
    location_lower = location.lower().strip()
    
    # Define regional site mappings
    bangladesh_keywords = ['bangladesh', 'dhaka', 'chittagong', 'sylhet', 'rajshahi', 'khulna', 'barisal', 'rangpur', 'mymensingh']
    india_keywords = ['india', 'mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai', 'kolkata', 'pune']
    middle_east_keywords = ['uae', 'dubai', 'abu dhabi', 'qatar', 'doha', 'saudi arabia', 'riyadh', 'kuwait', 'bahrain', 'oman']
    usa_keywords = ['usa', 'united states', 'america', 'us', 'new york', 'california', 'texas', 'florida', 'chicago', 'los angeles', 'san francisco', 'seattle', 'boston', 'atlanta']
    canada_keywords = ['canada', 'toronto', 'vancouver', 'montreal', 'calgary', 'ottawa']
    uk_keywords = ['uk', 'united kingdom', 'london', 'manchester', 'birmingham', 'glasgow', 'edinburgh']
    
    # Check location and select appropriate sites
    is_bangladesh = any(keyword in location_lower for keyword in bangladesh_keywords)
    is_india = any(keyword in location_lower for keyword in india_keywords)
    is_middle_east = any(keyword in location_lower for keyword in middle_east_keywords)
    is_usa = any(keyword in location_lower for keyword in usa_keywords)
    is_canada = any(keyword in location_lower for keyword in canada_keywords)
    is_uk = any(keyword in location_lower for keyword in uk_keywords)
    
    # Core international sites (only working sites)
    core_sites = [Site.LINKEDIN, Site.INDEED, Site.GLASSDOOR]
    
    if is_bangladesh:
        # Bangladesh-specific optimization - only use working sites
        if BDJOBS_AVAILABLE:
            available_sites = [Site.BDJOBS] + core_sites
        else:
            available_sites = core_sites
        logger.info(f"Using Bangladesh-optimized sites for location: {location}")
        
    elif is_india:
        # India-specific optimization - only use working sites
        available_sites = core_sites
        logger.info(f"Using India-optimized sites for location: {location}")
        
    elif is_middle_east:
        # Middle East-specific optimization - only use working sites
        available_sites = core_sites
        logger.info(f"Using Middle East-optimized sites for location: {location}")
        
    elif is_usa:
        # USA-specific optimization - only use working sites
        available_sites = core_sites
        logger.info(f"Using USA-optimized sites for location: {location}")
        
    elif is_canada:
        # Canada-specific optimization - only use working sites
        available_sites = core_sites
        logger.info(f"Using Canada-optimized sites for location: {location}")
        
    elif is_uk:
        # UK-specific optimization - only use working sites
        available_sites = core_sites
        logger.info(f"Using UK-optimized sites for location: {location}")
        
    else:
        # Default for other international locations - only use working sites
        available_sites = core_sites
        logger.info(f"Using default international sites for location: {location}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_sites = []
    for site in available_sites:
        if site not in seen:
            seen.add(site)
            unique_sites.append(site)
    
    logger.info(f"Selected sites: {[site.value for site in unique_sites]}")
    return unique_sites


def get_country_from_location(location: str) -> str:
    """Determine the appropriate country code based on location with improved mapping"""
    if not location:
        return "usa"  # Default fallback
    
    location_lower = location.lower().strip()
    
    # Enhanced country mapping with more comprehensive coverage
    country_mapping = {
        # Bangladesh
        'bangladesh': 'bangladesh',
        'dhaka': 'bangladesh',
        'chittagong': 'bangladesh',
        'sylhet': 'bangladesh',
        'rajshahi': 'bangladesh',
        'khulna': 'bangladesh',
        'barisal': 'bangladesh',
        'rangpur': 'bangladesh',
        'mymensingh': 'bangladesh',
        'comilla': 'bangladesh',
        'narayanganj': 'bangladesh',
        'gazipur': 'bangladesh',
        
        # India
        'india': 'india',
        'mumbai': 'india',
        'delhi': 'india',
        'bangalore': 'india',
        'hyderabad': 'india',
        'chennai': 'india',
        'kolkata': 'india',
        'pune': 'india',
        'ahmedabad': 'india',
        'jaipur': 'india',
        'surat': 'india',
        'lucknow': 'india',
        'kanpur': 'india',
        'nagpur': 'india',
        'indore': 'india',
        'thane': 'india',
        'bhopal': 'india',
        'visakhapatnam': 'india',
        'pimpri': 'india',
        
        # Pakistan
        'pakistan': 'pakistan',
        'karachi': 'pakistan',
        'lahore': 'pakistan',
        'islamabad': 'pakistan',
        'rawalpindi': 'pakistan',
        'faisalabad': 'pakistan',
        
        # USA
        'usa': 'usa',
        'united states': 'usa',
        'america': 'usa',
        'us': 'usa',
        'new york': 'usa',
        'california': 'usa',
        'texas': 'usa',
        'florida': 'usa',
        'chicago': 'usa',
        'los angeles': 'usa',
        'san francisco': 'usa',
        'seattle': 'usa',
        'boston': 'usa',
        'atlanta': 'usa',
        'denver': 'usa',
        'phoenix': 'usa',
        'philadelphia': 'usa',
        'houston': 'usa',
        'dallas': 'usa',
        'miami': 'usa',
        'washington': 'usa',
        'las vegas': 'usa',
        'detroit': 'usa',
        'minneapolis': 'usa',
        'portland': 'usa',
        'san diego': 'usa',
        
        # Canada
        'canada': 'canada',
        'toronto': 'canada',
        'vancouver': 'canada',
        'montreal': 'canada',
        'calgary': 'canada',
        'ottawa': 'canada',
        'edmonton': 'canada',
        'winnipeg': 'canada',
        'quebec': 'canada',
        'hamilton': 'canada',
        
        # UK
        'uk': 'uk',
        'united kingdom': 'uk',
        'london': 'uk',
        'manchester': 'uk',
        'birmingham': 'uk',
        'glasgow': 'uk',
        'edinburgh': 'uk',
        'liverpool': 'uk',
        'bristol': 'uk',
        'leeds': 'uk',
        'sheffield': 'uk',
        'cardiff': 'uk',
        'belfast': 'uk',
        
        # Australia
        'australia': 'australia',
        'sydney': 'australia',
        'melbourne': 'australia',
        'brisbane': 'australia',
        'perth': 'australia',
        'adelaide': 'australia',
        'canberra': 'australia',
        
        # Germany
        'germany': 'germany',
        'berlin': 'germany',
        'munich': 'germany',
        'hamburg': 'germany',
        'cologne': 'germany',
        'frankfurt': 'germany',
        'stuttgart': 'germany',
        'düsseldorf': 'germany',
        'dortmund': 'germany',
        'essen': 'germany',
        
        # France
        'france': 'france',
        'paris': 'france',
        'lyon': 'france',
        'marseille': 'france',
        'toulouse': 'france',
        'nice': 'france',
        'nantes': 'france',
        'strasbourg': 'france',
        'montpellier': 'france',
        'bordeaux': 'france',
        
        # Middle East
        'uae': 'uae',
        'dubai': 'uae',
        'abu dhabi': 'uae',
        'sharjah': 'uae',
        'qatar': 'qatar',
        'doha': 'qatar',
        'saudi arabia': 'saudi',
        'riyadh': 'saudi',
        'jeddah': 'saudi',
        'kuwait': 'kuwait',
        'bahrain': 'bahrain',
        'oman': 'oman',
        'muscat': 'oman',
    }
    
    # Check for exact matches or partial matches
    for keyword, country in country_mapping.items():
        if keyword in location_lower:
            logger.info(f"Mapped location '{location}' to country '{country}'")
            return country
    
    # Default to USA if no match found
    logger.info(f"No specific mapping found for location '{location}', defaulting to 'usa'")
    return "usa"


def process_jobs_dataframe(jobs_df: pd.DataFrame) -> List[JobPost]:
    """Convert pandas DataFrame to list of JobPost objects"""
    jobs_list = []
    
    for _, row in jobs_df.iterrows():
        try:
            # Helper function to handle NaN values and type conversion
            def safe_get(value, default=None, convert_to_string=False):
                if pd.isna(value) or value is None:
                    return default
                
                # Convert date objects to string
                if isinstance(value, (date, datetime)):
                    return value.isoformat() if convert_to_string else str(value)
                
                # Convert to string if requested
                if convert_to_string and value is not None:
                    return str(value)
                
                return value
            
            job_post = JobPost(
                id=safe_get(row.get('id')),
                title=safe_get(row.get('title'), 'N/A'),
                company_name=safe_get(row.get('company'), 'N/A'),
                job_url=safe_get(row.get('job_url'), ''),
                location=safe_get(row.get('location')),
                description=safe_get(row.get('description')),
                company_url=safe_get(row.get('company_url')),
                job_type=safe_get(row.get('job_type')),
                date_posted=safe_get(row.get('date_posted'), convert_to_string=True),
                is_remote=safe_get(row.get('is_remote'), False),
                site=safe_get(row.get('site'), 'unknown'),
                min_amount=safe_get(row.get('min_amount')),
                max_amount=safe_get(row.get('max_amount')),
                currency=safe_get(row.get('currency')),
                interval=safe_get(row.get('interval'))
            )
            jobs_list.append(job_post)
        except Exception as e:
            logger.error(f"Error processing job row: {e}")
            # Log the problematic row data for debugging
            logger.debug(f"Problematic row data: {dict(row)}")
            continue
    
    return jobs_list


def handle_null_values(data: dict) -> dict:
    """
    Handle null, empty, or missing values by replacing them with 'Not provided or Not found'
    """
    default_value = "Not provided or Not found"
    
    # Define the expected fields
    expected_fields = [
        "search_keywords", "email", "phone", "education", "name", 
        "skills", "experience", "field_of_interest", "achievements", 
        "certifications", "projects", "languages"
    ]
    
    processed_data = {}
    
    for field in expected_fields:
        value = data.get(field)
        
        # Handle various null/empty cases
        if value is None or value == "" or value == "null" or value == "NULL" or (isinstance(value, str) and value.strip() == ""):
            processed_data[field] = default_value
        else:
            processed_data[field] = str(value)
    
    return processed_data