"""
Health check and root endpoints.
"""
from fastapi import APIRouter
from app.models.schemas import HealthResponse, RootResponse
from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    """Root endpoint returning API status.
    
    Returns:
        API status information
    """
    return RootResponse(
        status=200,
        message=f"{settings.app_name} is running",
        version=settings.app_version
    )


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint for monitoring.
    
    Returns:
        Health status of the service
    """
    return HealthResponse(
        status="healthy",
        service="resume-parser"
    )
