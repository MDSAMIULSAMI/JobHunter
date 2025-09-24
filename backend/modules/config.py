"""
Configuration and logging setup for the FastAPI application.
"""
import logging
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the JobHunter directory to the Python path - use insert(0) to prioritize
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scraper'))

# FastAPI app configuration
def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="JobHunter FastAPI",
        description="A FastAPI wrapper for JobHunter that aggregates job postings from multiple job boards",
        version="1.0.6"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
    
    return app

# Global logger instance
def get_logger():
    """Get the configured logger instance."""
    return logger