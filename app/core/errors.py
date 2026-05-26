"""Application-specific exceptions for clean API error handling."""


class ResumeParserError(Exception):
    """Base class for expected parser errors."""

    status_code = 500
    error_type = "ResumeParserError"


class InvalidFileError(ResumeParserError):
    """Raised when an uploaded file is not an acceptable resume file."""

    status_code = 400
    error_type = "InvalidFileError"


class FileTooLargeError(ResumeParserError):
    """Raised when an uploaded file exceeds configured limits."""

    status_code = 413
    error_type = "FileTooLargeError"


class TextExtractionError(ResumeParserError):
    """Raised when text cannot be extracted from the uploaded PDF."""

    status_code = 422
    error_type = "TextExtractionError"


class NlpModelError(ResumeParserError):
    """Raised when the NLP model cannot be initialized or used."""

    status_code = 500
    error_type = "NlpModelError"
