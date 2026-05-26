"""Upload validation service."""

from fastapi import UploadFile

from app.core.config import settings
from app.core.errors import FileTooLargeError, InvalidFileError


class UploadValidationService:
    """Validate resume uploads before expensive parsing begins."""

    def __init__(
        self,
        max_file_size: int | None = None,
        allowed_extensions: list[str] | None = None,
    ) -> None:
        self.max_file_size = max_file_size or settings.max_file_size
        self.allowed_extensions = allowed_extensions or settings.allowed_extensions

    def validate(self, file: UploadFile, contents: bytes) -> None:
        """Validate filename, size, and PDF signature."""
        self._validate_filename(file.filename)
        self._validate_size(contents)
        self._validate_pdf_signature(contents)

    def _validate_filename(self, filename: str | None) -> None:
        if not filename:
            raise InvalidFileError("A filename is required")

        lower_filename = filename.lower()
        if not any(lower_filename.endswith(ext.lower()) for ext in self.allowed_extensions):
            raise InvalidFileError("Only PDF files are supported")

    def _validate_size(self, contents: bytes) -> None:
        if len(contents) == 0:
            raise InvalidFileError("Uploaded file is empty")

        if len(contents) > self.max_file_size:
            megabytes = self.max_file_size / 1024 / 1024
            raise FileTooLargeError(f"File size too large. Maximum {megabytes:g}MB allowed.")

    def _validate_pdf_signature(self, contents: bytes) -> None:
        if not contents.startswith(b"%PDF"):
            raise InvalidFileError("Uploaded file is not a valid PDF")
