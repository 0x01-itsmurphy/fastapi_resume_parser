"""
Pydantic models for request/response validation.
"""
from typing import List, Optional, Dict, Any, Set
from pydantic import BaseModel, Field, field_validator


class PersonalInfo(BaseModel):
    """Personal information extracted from resume."""
    name: Optional[str] = Field(None, description="Full name of the candidate")
    email: Set[str] = Field(default_factory=set, description="Email addresses")
    phone_number: Optional[str] = Field(None, description="Phone number")


class SocialLinks(BaseModel):
    """Social media links extracted from resume."""
    linkedin: str = Field("", description="LinkedIn profile URL")
    github: str = Field("", description="GitHub username")
    others: List[str] = Field(default_factory=list, description="Other URLs")


class EducationDetails(BaseModel):
    """Education information extracted from resume."""
    courses: List[str] = Field(default_factory=list, description="Degree courses")
    specializations: List[str] = Field(default_factory=list, description="Specializations")
    college: List[str] = Field(default_factory=list, description="Educational institutions")


class Address(BaseModel):
    """Address information extracted from resume."""
    location: Optional[Dict[str, Any]] = Field(None, description="Location details")
    zip_code: List[str] = Field(default_factory=list, description="Zip/postal codes")


class ProcessingInfo(BaseModel):
    """Metadata about the resume processing."""
    text_length: int = Field(..., description="Total characters extracted")
    tokens_processed: int = Field(..., description="Number of tokens processed by NLP")
    entities_found: int = Field(..., description="Number of named entities found")


class ResumeParseResponse(BaseModel):
    """Complete response for resume parsing."""
    status: str = Field("success", description="Processing status")
    filename: str = Field(..., description="Original filename")
    personal_info: PersonalInfo
    social_links: SocialLinks
    skills: List[str] = Field(default_factory=list, description="Extracted skills")
    education_details: EducationDetails
    address: Address
    languages: Optional[List[str]] = Field(None, description="Languages known")
    processing_info: ProcessingInfo
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "filename": "john_doe_resume.pdf",
                "personal_info": {
                    "name": "John Doe",
                    "email": ["john.doe@example.com"],
                    "phone_number": "+1234567890"
                },
                "social_links": {
                    "linkedin": "linkedin.com/in/johndoe",
                    "github": "johndoe",
                    "others": []
                },
                "skills": ["Python", "FastAPI", "Machine Learning"],
                "education_details": {
                    "courses": ["B.Tech"],
                    "specializations": ["Computer Science"],
                    "college": ["University of Technology"]
                },
                "address": {
                    "location": None,
                    "zip_code": ["12345"]
                },
                "languages": ["English"],
                "processing_info": {
                    "text_length": 1250,
                    "tokens_processed": 320,
                    "entities_found": 15
                }
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")


class RootResponse(BaseModel):
    """Root endpoint response."""
    status: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Status message")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(None, description="Type of error")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Only PDF files are supported",
                "error_type": "ValidationError"
            }
        }
