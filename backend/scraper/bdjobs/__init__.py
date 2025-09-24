# __init__.py
from __future__ import annotations

import random
import time
import re
from datetime import datetime
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin, urlparse, parse_qs

from bs4 import BeautifulSoup
from bs4.element import Tag

from scraper.model import (
    JobPost,
    Location,
    JobResponse,
    Country,
    Scraper,
    ScraperInput,
    Site,
    DescriptionFormat,
)
from scraper.util import (
    create_session,
    create_logger,
)

log = create_logger("BDJobs")

# Headers for BDJobs requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Referer": "https://jobs.bdjobs.com/",
    "Cache-Control": "max-age=0",
}

# Fix the search parameters
search_params = {
    "hidJobSearch": "jobsearch",
}


def is_bangladesh_location(location: str) -> bool:
    """Check if the requested location is in Bangladesh or compatible with BDJobs"""
    if not location:
        return True
    
    location_lower = location.lower()
    bangladesh_indicators = [
        'bangladesh', 'dhaka', 'chittagong', 'sylhet', 'rajshahi', 'khulna', 
        'barisal', 'rangpur', 'mymensingh', 'comilla', 'narayanganj', 'gazipur',
        'bd', 'bengal'
    ]
    
    return any(indicator in location_lower for indicator in bangladesh_indicators)


def parse_location(location_text: str, country: str = "bangladesh") -> Location:
    """Parse location text into a Location object"""
    if not location_text:
        return Location(city="Dhaka", country=Country.from_string(country))
    
    location_text = location_text.strip()
    parts = location_text.split(",")
    if len(parts) >= 2:
        city = parts[0].strip()
        state = parts[1].strip() if len(parts) > 1 else None
        return Location(city=city, state=state, country=Country.from_string(country))
    else:
        return Location(city=location_text.strip(), country=Country.from_string(country))


def extract_job_id_from_url(url: str) -> str:
    """Extract job ID from BDJobs URL"""
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        job_id = query_params.get('id', [None])[0]
        if job_id:
            return f"bdjobs-{job_id}"
    except:
        pass
    return f"bdjobs-{hash(url)}"


def find_job_listings(soup: BeautifulSoup) -> List[Any]:
    """Find job listing elements in the HTML with improved selectors"""
    # Try multiple selectors based on BDJobs structure
    job_selectors = [
        # Main job listing containers
        "div[class*='job']",
        "tr[class*='job']",
        "div[class*='sout']",
        "div[class*='norm']",
        "div[class*='featured']",
        # Table rows containing job data
        "table tr",
        # Any element containing job detail links
        "*:has(a[href*='jobdetail'])",
    ]
    
    for selector in job_selectors:
        try:
            elements = soup.select(selector)
            # Filter elements that actually contain job links
            job_elements = []
            for elem in elements:
                if elem.find("a", href=lambda h: h and "jobdetail" in h.lower()):
                    job_elements.append(elem)
            
            if job_elements and len(job_elements) > 0:
                log.info(f"Found {len(job_elements)} job elements using selector: {selector}")
                return job_elements
        except Exception as e:
            log.debug(f"Selector {selector} failed: {e}")
            continue
    
    # Fallback: find all job links and get their parent containers
    job_links = soup.find_all("a", href=lambda h: h and "jobdetail" in h.lower())
    if job_links:
        log.info(f"Fallback: Found {len(job_links)} job links")
        return [link.find_parent(['tr', 'div', 'td']) or link.parent for link in job_links if link.parent]
    
    return []


class BDJobs(Scraper):
    base_url = "https://jobs.bdjobs.com"
    search_url = "https://jobs.bdjobs.com/jobsearch.asp"
    delay = 2
    band_delay = 3

    def __init__(self, proxies: list[str] | str | None = None, ca_cert: str | None = None, user_agent: str | None = None):
        """Initialize BDJobs scraper"""
        super().__init__(Site.BDJOBS, proxies=proxies, ca_cert=ca_cert, user_agent=user_agent)
        self.session = create_session(
            proxies=self.proxies,
            ca_cert=ca_cert,
            is_tls=False,
            has_retry=True,
            delay=5,
            clear_cookies=True,
        )
        # Use custom user_agent if provided, otherwise use default headers
        session_headers = headers.copy()
        if user_agent:
            session_headers["User-Agent"] = user_agent
        self.session.headers.update(session_headers)
        self.scraper_input = None
        self.country = "bangladesh"

    def scrape(self, scraper_input: ScraperInput) -> JobResponse:
        """Scrape BDJobs for jobs"""
        self.scraper_input = scraper_input
        job_list: list[JobPost] = []
        seen_ids = set()
        page = 1

        # Check if the requested location is compatible with BDJobs
        if scraper_input.location and not is_bangladesh_location(scraper_input.location):
            log.info(f"BDJobs: Skipping search for location '{scraper_input.location}' as it's outside Bangladesh")
            return JobResponse(jobs=[])

        # Set up search parameters - FIX: Use correct parameter name
        params = search_params.copy()
        if scraper_input.search_term:
            params["txtKeyword"] = scraper_input.search_term  # Changed from txtsearch to txtKeyword
            
        # Add location parameter if it's a Bangladesh location
        if scraper_input.location and is_bangladesh_location(scraper_input.location):
            params["txtlocation"] = scraper_input.location

        continue_search = lambda: len(job_list) < scraper_input.results_wanted

        while continue_search() and page <= 5:  # Limit to 5 pages
            log.info(f"BDJobs search page: {page}")

            try:
                if page > 1:
                    params["pg"] = page

                response = self.session.get(
                    self.search_url,
                    params=params,
                    timeout=60,
                )

                if response.status_code != 200:
                    log.error(f"BDJobs response status code {response.status_code}")
                    break

                soup = BeautifulSoup(response.text, "html.parser")
                job_cards = find_job_listings(soup)

                if not job_cards:
                    log.info("No more job listings found on BDJobs")
                    break

                log.info(f"Found {len(job_cards)} job cards on BDJobs page {page}")

                for job_card in job_cards:
                    try:
                        job_post = self._process_job(job_card)
                        if job_post and job_post.id not in seen_ids:
                            seen_ids.add(job_post.id)
                            job_list.append(job_post)

                            if not continue_search():
                                break
                    except Exception as e:
                        log.error(f"Error processing BDJobs job card: {str(e)}")

                page += 1
                time.sleep(random.uniform(self.delay, self.delay + self.band_delay))

            except Exception as e:
                log.error(f"Error during BDJobs scraping: {str(e)}")
                break

        log.info(f"BDJobs: finished scraping")
        return JobResponse(jobs=job_list)

    def _process_job(self, job_card: Tag) -> Optional[JobPost]:
        """Process a job card element into a JobPost object with enhanced data extraction"""
        try:
            # Find job link
            job_link = job_card.find("a", href=lambda h: h and "jobdetail" in h.lower())
            if not job_link:
                job_link = job_card.find("a", href=True)
            
            if not job_link:
                return None

            job_url = job_link.get("href")
            if not job_url.startswith("http"):
                job_url = urljoin(self.base_url, job_url)

            # Extract job ID from URL
            job_id = extract_job_id_from_url(job_url)

            # Extract title - try multiple approaches
            title = None
            if job_link.get_text(strip=True):
                title = job_link.get_text(strip=True)
            else:
                # Look for title in nearby elements
                title_elem = job_card.find(["h1", "h2", "h3", "h4", "strong", "b"])
                if title_elem:
                    title = title_elem.get_text(strip=True)
            
            title = title or "N/A"

            # Extract company name - improved extraction
            company_name = "N/A"
            
            # Try multiple selectors for company name
            company_selectors = [
                lambda c: c and "company" in (c or "").lower(),
                lambda c: c and "employer" in (c or "").lower(),
                lambda c: c and "org" in (c or "").lower(),
            ]
            
            for selector in company_selectors:
                company_elem = job_card.find(["span", "div", "td", "p"], class_=selector)
                if company_elem:
                    company_name = company_elem.get_text(strip=True)
                    break
            
            # If still not found, look for text patterns
            if company_name == "N/A":
                all_text = job_card.get_text()
                # Look for company patterns in the text
                company_patterns = [
                    r'Company[:\s]+([^\n\r]+)',
                    r'Organization[:\s]+([^\n\r]+)',
                    r'Employer[:\s]+([^\n\r]+)',
                ]
                for pattern in company_patterns:
                    match = re.search(pattern, all_text, re.IGNORECASE)
                    if match:
                        company_name = match.group(1).strip()
                        break

            # Extract location - improved extraction
            location_text = "Dhaka, Bangladesh"
            
            # Try multiple selectors for location
            location_selectors = [
                lambda c: c and "location" in (c or "").lower(),
                lambda c: c and "address" in (c or "").lower(),
                lambda c: c and "place" in (c or "").lower(),
            ]
            
            for selector in location_selectors:
                location_elem = job_card.find(["span", "div", "td", "p"], class_=selector)
                if location_elem:
                    location_text = location_elem.get_text(strip=True)
                    break
            
            # If still not found, look for location patterns in text
            if location_text == "Dhaka, Bangladesh":
                all_text = job_card.get_text()
                location_patterns = [
                    r'Location[:\s]+([^\n\r]+)',
                    r'Address[:\s]+([^\n\r]+)',
                    r'Place[:\s]+([^\n\r]+)',
                ]
                for pattern in location_patterns:
                    match = re.search(pattern, all_text, re.IGNORECASE)
                    if match:
                        location_text = match.group(1).strip()
                        break

            location = parse_location(location_text, self.country)

            # Extract additional information
            description = None
            job_type = None
            date_posted = None
            
            # Try to extract job description or summary
            desc_elem = job_card.find(["div", "p", "span"], class_=lambda c: c and ("desc" in (c or "").lower() or "summary" in (c or "").lower()))
            if desc_elem:
                description = desc_elem.get_text(strip=True)
            
            # Try to extract job type
            type_elem = job_card.find(["span", "div"], class_=lambda c: c and "type" in (c or "").lower())
            if type_elem:
                job_type = type_elem.get_text(strip=True)
            
            # Try to extract date posted
            date_elem = job_card.find(["span", "div"], class_=lambda c: c and ("date" in (c or "").lower() or "deadline" in (c or "").lower()))
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                # Try to parse date
                try:
                    # Handle various date formats
                    if "deadline" in date_text.lower():
                        date_posted = date_text
                    else:
                        date_posted = date_text
                except:
                    date_posted = date_text

            # Create job post with enhanced data
            job_post = JobPost(
                id=job_id,
                title=title,
                company_name=company_name,
                location=location,
                job_url=job_url,
                description=description,
                job_type=job_type,
                date_posted=date_posted,
                is_remote=False,  # BDJobs typically doesn't have remote jobs
                site=self.site,
            )

            return job_post
            
        except Exception as e:
            log.error(f"Error in _process_job: {str(e)}")
            return None

    def _fetch_job_details(self, job_url: str) -> Dict[str, Any]:
        """Fetch additional job details from the job detail page"""
        try:
            response = self.session.get(job_url, timeout=15)
            if response.status_code != 200:
                return {}
            
            soup = BeautifulSoup(response.text, "html.parser")
            details = {}
            
            # Extract detailed description
            desc_selectors = [
                "div.job-description",
                "div.job-details",
                "div[class*='desc']",
                "div[class*='detail']",
            ]
            
            for selector in desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    details['description'] = desc_elem.get_text(strip=True)
                    break
            
            # Extract salary information
            salary_patterns = [
                r'Salary[:\s]+([^\n\r]+)',
                r'Compensation[:\s]+([^\n\r]+)',
                r'BDT\s*(\d+(?:,\d+)*)',
                r'Tk\s*(\d+(?:,\d+)*)',
            ]
            
            page_text = soup.get_text()
            for pattern in salary_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    details['salary'] = match.group(1).strip()
                    break
            
            return details
            
        except Exception as e:
            log.debug(f"Error fetching job details from {job_url}: {e}")
            return {}


# Export the BDJobs class
__all__ = ["BDJobs"]
