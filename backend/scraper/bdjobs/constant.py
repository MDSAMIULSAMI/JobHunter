#constant.py
# Headers for BDJobs requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Referer": "https://jobs.bdjobs.com/",
    "Cache-Control": "max-age=0",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
}

# Search parameters that work best for BDJobs
search_params = {
    "hidJobSearch": "jobsearch",
    "txtKeyword": "",  # This will be set dynamically
    "cboWorkPlace": "-1",  # All locations
    "cboCategory": "-1",   # All categories
}

# Updated selectors for job listings based on current BDJobs structure
job_selectors = [
    "div.job-list-item",     # Main job listing container
    "div.job-item",          # Alternative job item selector
    "div.sout-jobs-wrapper", # Search result wrapper
    "div.norm-jobs-wrapper", # Normal job wrapper
    "div.featured-wrap",     # Featured job wrapper
    "div.job-card",          # Job card container
    "tr.job-item",           # Table row format (if they use tables)
]

# Date formats used by BDJobs
date_formats = [
    "%d %b %Y",
    "%d-%b-%Y", 
    "%d %B %Y",
    "%B %d, %Y",
    "%d/%m/%Y",
    "%Y-%m-%d",
    "%d.%m.%Y",
]