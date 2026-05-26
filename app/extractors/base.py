"""Extractor interfaces."""

from typing import Any, Protocol, TypeVar

T = TypeVar("T", covariant=True)


class Extractor(Protocol[T]):
    """Common interface for all extractors."""

    def extract(self, text: str, doc: Any | None = None) -> T:
        """Extract structured data from resume text."""
        ...
