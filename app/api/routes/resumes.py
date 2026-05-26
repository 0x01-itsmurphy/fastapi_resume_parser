"""Resume parsing endpoints."""

from dataclasses import asdict

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.dependencies import get_resume_parser_service
from app.core.errors import ResumeParserError
from app.core.logging import get_logger
from app.schemas.responses import ErrorResponse, ResumeParseResponse
from app.services.resume_parser import ResumeParserService

logger = get_logger(__name__)

router = APIRouter(prefix="/v1/resumes", tags=["resumes"])
legacy_router = APIRouter(prefix="/parse", tags=["parsing"])


@router.post(
    "/parse",
    response_model=ResumeParseResponse,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def parse_resume_v1(
    file: UploadFile = File(...),
    parser: ResumeParserService = Depends(get_resume_parser_service),
) -> ResumeParseResponse:
    """Parse a PDF resume into structured data."""
    return await _parse_resume(file=file, parser=parser)


@legacy_router.post(
    "",
    response_model=ResumeParseResponse,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def parse_resume_legacy(
    file: UploadFile = File(...),
    parser: ResumeParserService = Depends(get_resume_parser_service),
) -> ResumeParseResponse:
    """Backward-compatible parser endpoint."""
    return await _parse_resume(file=file, parser=parser)


async def _parse_resume(file: UploadFile, parser: ResumeParserService) -> ResumeParseResponse:
    try:
        result = await parser.parse_upload(file)
        return ResumeParseResponse.model_validate(asdict(result))
    except ResumeParserError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=str(exc),
            headers={"X-Error-Type": exc.error_type},
        ) from exc
    except Exception as exc:
        logger.error("Unexpected error processing resume: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing resume") from exc
