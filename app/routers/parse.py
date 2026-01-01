"""
Resume parsing endpoints.
"""
from io import BytesIO
from typing import Dict, Any

import spacy
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from pypdf import PdfReader
from pdfminer.high_level import extract_text

from app.core.config import settings
from app.core.logging import get_logger
from app.models.schemas import ResumeParseResponse, ErrorResponse
from app import utils as utl

logger = get_logger(__name__)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("spaCy model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load spaCy model: {e}")
    raise RuntimeError("Failed to initialize NLP model") from e

router = APIRouter(prefix="/parse", tags=["parsing"])


def validate_pdf_file(file: UploadFile) -> None:
    """Validate uploaded file is a PDF.
    
    Args:
        file: Uploaded file to validate
        
    Raises:
        HTTPException: If file is not a PDF
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )


async def validate_file_size(file: UploadFile) -> None:
    """Validate file size is within limits.
    
    Args:
        file: Uploaded file to validate
        
    Raises:
        HTTPException: If file is too large
    """
    file_size = len(await file.read())
    if file_size > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size too large. Maximum {settings.max_file_size / 1024 / 1024}MB allowed."
        )
    await file.seek(0)


@router.post("", response_model=ResumeParseResponse, responses={
    400: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
async def parse_resume(file: UploadFile = File(...)) -> ResumeParseResponse:
    """
    Advanced resume parsing endpoint with comprehensive data extraction.
    
    This endpoint accepts a PDF resume and extracts:
    - Personal information (name, email, phone)
    - Social media links (LinkedIn, GitHub)  
    - Skills and technologies
    - Education details
    - Work experience
    - Location and address
    - Languages
    
    Args:
        file: PDF resume file to parse
        
    Returns:
        Structured resume data
        
    Raises:
        HTTPException: For invalid files or processing errors
    """
    try:
        # Validate file
        validate_pdf_file(file)
        await validate_file_size(file)
        
        # Extract text from PDF
        contents = await file.read()
        pdf_reader = PdfReader(BytesIO(contents))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        if not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No text could be extracted from the PDF"
            )

        # Try pdfminer for better text extraction
        await file.seek(0)
        try:
            data = extract_text(file.file)
            if len(data) > len(text):
                text = data
        except Exception as e:
            logger.warning(f"pdfminer extraction failed: {e}, using pypdf")
            data = text

        logger.info(f"Extracted text length: {len(text)} characters")

        # Process with spaCy
        doc = nlp(text)

        # Extract all information
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
        return ResumeParseResponse(
            status="success",
            filename=file.filename,
            personal_info={
                "name": name,
                "email": email,
                "phone_number": phone,
            },
            social_links={
                "linkedin": linkedIn,
                "github": github,
                "others": others_urls,
            },
            skills=skills,
            education_details={
                "courses": course_name,
                "specializations": specializations,
                "college": college,
            },
            address={
                "location": location,
                "zip_code": extracted_zip
            },
            languages=languages,
            processing_info={
                "text_length": len(text),
                "tokens_processed": len(doc),
                "entities_found": len(doc.ents)
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {str(e)}"
        ) from e
