"""
FastAPI Resume Parser - Main Application

A modern, high-performance resume parsing API built with FastAPI that extracts
structured information from PDF resumes using advanced NLP techniques.
"""
import spacy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from mangum import Mangum

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.routers import health, parse

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A FastAPI application for parsing resumes and extracting structured information using NLP",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    try:
        # Verify spaCy model is available
        nlp = spacy.load("en_core_web_sm")
        logger.info("spaCy model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load spaCy model: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown."""
    logger.info(f"Shutting down {settings.app_name}")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors.
    
    Args:
        request: The request that caused the error
        exc: The exception that was raised
        
    Returns:
        JSON response with error details
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_type": type(exc).__name__
        }
    )


# Include routers
app.include_router(health.router)
app.include_router(parse.router)

# AWS Lambda handler
handler = Mangum(app)
