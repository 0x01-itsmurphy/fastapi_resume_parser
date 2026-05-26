"""Centralized NLP model loading and access."""

from typing import Any

import spacy

from app.core.errors import NlpModelError
from app.core.logging import get_logger

logger = get_logger(__name__)


class NlpService:
    """Lazy-loading wrapper around the configured spaCy model."""

    def __init__(self, model_name: str = "en_core_web_sm") -> None:
        self.model_name = model_name
        self._nlp: Any | None = None

    def load(self) -> Any:
        """Load the NLP model once and return it."""
        if self._nlp is None:
            try:
                self._nlp = spacy.load(self.model_name)
                logger.info("spaCy model loaded: %s", self.model_name)
            except Exception as exc:
                logger.error("Failed to load spaCy model %s: %s", self.model_name, exc)
                raise NlpModelError(f"Failed to load NLP model: {self.model_name}") from exc
        return self._nlp

    def process(self, text: str) -> Any:
        """Process text with the NLP model."""
        return self.load()(text)
