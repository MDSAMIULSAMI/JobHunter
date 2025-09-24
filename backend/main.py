"""
FastAPI JobHunter Application - Refactored Main Entry Point

This is the main entry point for the JobHunter FastAPI application.
The application has been refactored into modular components for better maintainability.
"""

from fastapi import HTTPException
from modules.config import create_app, get_logger
from modules.routes import job_router, resume_router, general_router
from modules.exceptions import http_exception_handler, general_exception_handler

# Initialize logger
logger = get_logger()

# Create FastAPI app
app = create_app()

# Include routers
# app.include_router(general_router)
app.include_router(job_router)
app.include_router(resume_router)

# Add exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Log application startup
# logger.info("JobHunter FastAPI application started successfully")
# logger.info("Available endpoints:")
# logger.info("  - GET  /              : Root endpoint")
# logger.info("  - GET  /health        : Health check")
# logger.info("  - POST /jobs/search   : Search jobs")
# logger.info("  - GET  /jobs/search   : Search jobs (GET)")
# logger.info("  - GET  /jobs/available-sites : Available job sites")
# logger.info("  - POST /resume/upload : Upload resume for analysis")
# logger.info("  - POST /resume/custom-builder : Custom resume builder")
# logger.info("  - Legacy endpoints maintained for backward compatibility")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)