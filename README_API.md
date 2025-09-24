# JobSpy FastAPI Application

A FastAPI wrapper for the JobSpy library that aggregates job postings from multiple job boards including LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs, Bayt, Naukri, and BDJobs.

## Features

- **Multi-source Job Aggregation**: Fetches jobs from 8+ job boards simultaneously
- **72-hour Fresh Jobs**: Only returns job postings from the last 72 hours
- **In-memory Caching**: Efficient caching system to avoid redundant API calls
- **Input Validation**: Comprehensive request validation with clear error messages
- **Async Processing**: Non-blocking job scraping using thread pools
- **Clean API Design**: RESTful endpoints with comprehensive documentation
- **Error Handling**: Robust error handling with detailed error responses

## Quick Start

### Option 1: Direct Python Execution

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

### Option 2: Docker

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Search Jobs (POST)
**Endpoint**: `POST /search-jobs`

**Request Body**:
```json
{
  "location": "New York, NY",
  "search_keyword": "software engineer",
  "results_wanted": 100,
  "distance": 50
}
```

**Response**:
```json
{
  "success": true,
  "message": "Successfully found 95 jobs",
  "total_jobs": 95,
  "jobs": [
    {
      "id": "123456",
      "title": "Senior Software Engineer",
      "company_name": "Tech Corp",
      "job_url": "https://example.com/job/123456",
      "location": "New York, NY",
      "description": "Job description...",
      "job_type": "Full-time",
      "date_posted": "2024-01-15",
      "is_remote": false,
      "site": "linkedin",
      "min_amount": 120000,
      "max_amount": 150000,
      "currency": "USD",
      "interval": "yearly"
    }
  ],
  "search_params": {
    "location": "New York, NY",
    "search_keyword": "software engineer",
    "results_wanted": 100,
    "distance": 50
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Search Jobs (GET)
**Endpoint**: `GET /search-jobs?location=New York&search_keyword=developer&results_wanted=50`

Same functionality as POST endpoint but using query parameters.

### 3. Health Check
**Endpoint**: `GET /health`

Returns API health status and cache information.

### 4. Cache Information
**Endpoint**: `GET /cache-info`

Returns detailed information about cached searches.

### 5. Clear Cache
**Endpoint**: `DELETE /cache`

Manually clears all cached data.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| location | string | Yes | - | Location to search for jobs |
| search_keyword | string | Yes | - | Search keyword/term |
| results_wanted | integer | No | 50 | Number of results (1-500) |
| distance | integer | No | 50 | Search radius in miles (1-100) |

## Job Sources

The API aggregates jobs from the following sources:
- LinkedIn
- Indeed
- Glassdoor
- ZipRecruiter
- Google Jobs
- Bayt
- Naukri
- BDJobs

## Caching Strategy

- **Cache Duration**: 72 hours
- **Cache Key**: Based on location and search keyword
- **Automatic Cleanup**: Expired entries are automatically removed
- **Manual Control**: Cache can be cleared via API endpoint

## Error Handling

The API provides detailed error responses:

```json
{
  "success": false,
  "error": "HTTP 400",
  "message": "Location is required and cannot be empty"
}
```

Common error scenarios:
- Missing required parameters (400)
- Invalid parameter values (400)
- Job scraping failures (500)
- Network timeouts (500)

## Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Logging

The application includes comprehensive logging:
- Request/response logging
- Cache operations
- Error tracking
- Performance metrics

## Performance Considerations

- **Concurrent Scraping**: Uses ThreadPoolExecutor for parallel job board scraping
- **Smart Caching**: Reduces redundant API calls
- **Async Processing**: Non-blocking request handling
- **Memory Management**: Automatic cache cleanup

## Example Usage

### Python Client
```python
import requests

# Search for jobs
response = requests.post("http://localhost:8000/search-jobs", json={
    "location": "San Francisco, CA",
    "search_keyword": "python developer",
    "results_wanted": 100,
    "distance": 25
})

jobs_data = response.json()
print(f"Found {jobs_data['total_jobs']} jobs")
```

### cURL
```bash
curl -X POST "http://localhost:8000/search-jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Seattle, WA",
    "search_keyword": "data scientist",
    "results_wanted": 75
  }'
```

## Development

To contribute or modify the application:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Make your changes
4. Test the API: `python run.py`
5. Access documentation: `http://localhost:8000/docs`

## License

This project uses the JobSpy library and follows its licensing terms.