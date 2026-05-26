"""FastAPI dependency factories."""

from functools import lru_cache

from app.services.resume_parser import ResumeParserService


@lru_cache()
def get_resume_parser_service() -> ResumeParserService:
    """Return the shared parser service instance for the process."""
    return ResumeParserService()
