"""Personal contact information extraction."""

import re
from typing import Any, Optional, Set, cast

from app.domain.models import PersonalInfo


class ContactExtractor:
    """Extract candidate name, email addresses, and phone number."""

    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
    PHONE_PATTERN = re.compile(
        r"(?:(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,5}[\s.-]?\d{4,6})"
    )

    def extract(self, text: str, doc: Any | None = None) -> PersonalInfo:
        return PersonalInfo(
            name=self.extract_name(text, doc),
            email=self.extract_emails(text),
            phone_number=self.extract_phone(text),
        )

    def extract_name(self, text: str, doc: Any | None = None) -> Optional[str]:
        if doc is not None:
            for ent in doc.ents:
                if ent.label_ == "PERSON" and self._looks_like_name(ent.text):
                    return cast(str, ent.text.strip())

            proper_nouns = [token.text for token in doc[:30] if token.pos_ == "PROPN"]
            if len(proper_nouns) >= 2:
                return " ".join(proper_nouns[:2])

        for line in text.splitlines()[:8]:
            candidate = line.strip()
            if self._looks_like_name(candidate):
                return candidate

        return None

    def extract_emails(self, text: str) -> Set[str]:
        return set(self.EMAIL_PATTERN.findall(text))

    def extract_phone(self, text: str) -> Optional[str]:
        for match in self.PHONE_PATTERN.findall(text):
            number = match.strip()
            digits = re.sub(r"\D", "", number)
            if 8 <= len(digits) <= 15:
                return cast(str, number)
        return None

    def _looks_like_name(self, value: str) -> bool:
        words = [word for word in re.split(r"\s+", value.strip()) if word]
        if not 2 <= len(words) <= 4:
            return False
        return all(re.fullmatch(r"[A-Za-z][A-Za-z.'-]*", word) for word in words)
