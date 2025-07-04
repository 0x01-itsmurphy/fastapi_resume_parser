import spacy
from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pdfminer.high_level import extract_text
from pypdf import PdfReader
from spacy.matcher import Matcher
from mangum import Mangum
from typing import Dict, Any, List, Optional
import logging
import os
from functools import lru_cache
from pydantic import BaseSettings

from . import utils as utl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with modern configuration
app = FastAPI(
    title="Resume Parser API",
    description="A FastAPI application for parsing resumes and extracting structured information",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    logger.info("spaCy model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load spaCy model: {e}")
    raise HTTPException(status_code=500, detail="Failed to initialize NLP model")


@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint returning API status"""
    return {"status": 200, "message": "Resume Parser API is running", "version": "2.0.0"}


@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "resume-parser"}


@app.post("/parse_resume", response_model=Dict[str, Any])
async def parse_resume(file: UploadFile = File(...)):
    """
    Parse resume using spaCy NLP - Legacy endpoint
    This endpoint has known issues and is deprecated.
    Please use /parse endpoint instead.
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Download and read the PDF file
        contents = await file.read()
        pdf_reader = PdfReader(BytesIO(contents))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")

        # Process the plain text using spaCy
        doc = nlp(text)
        logger.info(f"Processing document with {len(doc)} tokens")

        # Extract information using utility functions
        email = utl.get_email(text)
        phone_number = utl.get_phone(text)
        name_ext = utl.extract_name(text)
        skills = utl.extract_skills_new(text)
        edu = utl.extract_education(text)

        # Extract entities using spaCy
        name = None
        experience = None
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text
            elif ent.label_ == "EXPERIENCE":
                experience = ent.text

        # Return the extracted information
        return {
            "name": name_ext,
            "email": email,
            "phone": phone_number,
            "skills": skills,
            "education": edu,
            "experience": experience,
            "status": "success"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


@app.post("/parse", response_model=Dict[str, Any])
async def parse(file: UploadFile = File(...)):
    """
    Advanced resume parsing endpoint with comprehensive data extraction
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Check file size (limit to 10MB)
        file_size = len(await file.read())
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File size too large. Maximum 10MB allowed.")
        
        # Reset file pointer
        await file.seek(0)
        
        # Download and read the PDF file
        contents = await file.read()
        pdf_reader = PdfReader(BytesIO(contents))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")

        # Also try pdfminer for better text extraction
        await file.seek(0)
        try:
            data = extract_text(file.file)
            if len(data) > len(text):  # Use the better extraction
                text = data
        except Exception as e:
            logger.warning(f"pdfminer extraction failed: {e}, using pypdf")
            data = text

        logger.info(f"Extracted text length: {len(text)} characters")

        # Process the plain text using spaCy
        doc = nlp(text)

        # Extract all information using utility functions
        name = utl.extract_name(data)
        email = utl.get_email(data)
        phone = utl.get_phone(data)
        linkedIn = utl.linkedin(data)
        github = utl.extract_github(data)
        others_urls = utl.extract_urls(data)
        skills = utl.extract_skills_new(data)
        course_name = utl.extract_course_name(data)
        specializations = utl.extract_specializations(data)
        college = utl.get_college(data)
        languages = utl.get_language(data)
        location = utl.get_location(data)
        extracted_zip = utl.extract_zip_code(data)

        # Prepare response
        response_data = {
            "status": "success",
            "filename": file.filename,
            "personal_info": {
                "name": name,
                "email": email,
                "phone_number": phone,
            },
            "social_links": {
                "linkedin": linkedIn,
                "github": github,
                "others": others_urls,
            },
            "skills": skills,
            "education_details": {
                "courses": course_name,
                "specializations": specializations,
                "college": college,
            },
            "address": {
                "location": location,
                "zip_code": extracted_zip
            },
            "languages": languages,
            "processing_info": {
                "text_length": len(text),
                "tokens_processed": len(doc),
                "entities_found": len(doc.ents)
            }
        }

        # Only include raw_data in development mode
        if app.debug:
            response_data["raw_data"] = data

        return response_data
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "FastAPI Resume Parser"
    app_version: str = "2.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    max_file_size: int = 10485760  # 10MB
    cors_origins: str = "*"
    log_level: str = "info"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()


handler = Mangum(app)
