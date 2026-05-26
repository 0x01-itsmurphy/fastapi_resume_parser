"""PDF text extraction service."""

from io import BytesIO

from pdfminer.high_level import extract_text
from pypdf import PdfReader

from app.core.errors import TextExtractionError
from app.core.logging import get_logger

logger = get_logger(__name__)


class PdfTextExtractor:
    """Extract text from PDF bytes using deterministic fallback logic."""

    def extract(self, contents: bytes) -> str:
        """Extract a single normalized text value from PDF bytes."""
        pypdf_text = self._extract_with_pypdf(contents)
        pdfminer_text = self._extract_with_pdfminer(contents)

        text = pdfminer_text if len(pdfminer_text) > len(pypdf_text) else pypdf_text
        text = self._normalize(text)

        if not text:
            raise TextExtractionError("No text could be extracted from the PDF")

        logger.info("Extracted %s characters from PDF", len(text))
        return text

    def _extract_with_pypdf(self, contents: bytes) -> str:
        try:
            pdf_reader = PdfReader(BytesIO(contents))
            return "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
        except Exception as exc:
            logger.warning("pypdf extraction failed: %s", exc)
            return ""

    def _extract_with_pdfminer(self, contents: bytes) -> str:
        try:
            return extract_text(BytesIO(contents)) or ""
        except Exception as exc:
            logger.warning("pdfminer extraction failed: %s", exc)
            return ""

    def _normalize(self, text: str) -> str:
        lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n")]
        return "\n".join(line for line in lines if line).strip()
