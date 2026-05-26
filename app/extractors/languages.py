"""Language extraction."""

import re
from typing import Any, List, Optional


class LanguageExtractor:
    """Extract known human languages from resume text."""

    LANGUAGES = [
        "English",
        "Marathi",
        "Telugu",
        "Hindi",
        "Malayalam",
        "Kannada",
        "Tamil",
        "Spanish",
        "French",
        "Urdu",
        "Bengali",
        "Punjabi",
        "Gujarati",
    ]

    def extract(self, text: str, doc: Any | None = None) -> Optional[List[str]]:
        found = []
        for language in self.LANGUAGES:
            if re.search(rf"\b{re.escape(language)}\b", text, re.IGNORECASE):
                found.append(language)
        return found or None
