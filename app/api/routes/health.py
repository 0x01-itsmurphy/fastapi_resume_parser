"""Health check and root endpoints."""

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.responses import HealthResponse, RootResponse

router = APIRouter(tags=["health"])


@router.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    """Return API status information."""
    return RootResponse(
        status=200,
        message=f"{settings.app_name} is running",
        version=settings.app_version,
    )


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Return service health information."""
    return HealthResponse(status="healthy", service="resume-parser")
