"""Education detail extraction."""

import csv
import re
from pathlib import Path
from typing import Any, Iterable, List, Set

from app.domain.models import EducationDetails


class EducationExtractor:
    """Extract courses, specializations, and institution-like lines."""

    DEGREE_PATTERNS = [
        r"B\.A\.",
        r"B\.S\.",
        r"B\.Sc\.",
        r"M\.A\.",
        r"M\.S\.",
        r"M\.Sc\.",
        r"Ph\.D\.",
        r"M\.B\.A\.",
        r"B\.E\.",
        r"M\.E\.",
        r"B\.Tech\.",
        r"M\.Tech\.",
        r"B\.Com\.",
        r"M\.Com\.",
        r"SSC",
        r"HSC",
        r"CBSE",
        r"ICSE",
        r"[^a-zA-Z\d]Board",
        r"Bachelor of Technology(?: in [\w\s]+)?",
        r"Master of Technology(?: in [\w\s]+)?",
        r"Bachelor of Science(?: in [\w\s]+)?",
        r"Master of Science(?: in [\w\s]+)?",
        r"Bachelor of Arts(?: in [\w\s]+)?",
        r"Master of Arts(?: in [\w\s]+)?",
        r"Doctor of Philosophy(?: in [\w\s]+)?",
        r"Bachelor of Commerce(?: in [\w\s]+)?",
        r"Master of Commerce(?: in [\w\s]+)?",
        r"Bachelor of Engineering(?: in [\w\s]+)?",
        r"Master of Engineering(?: in [\w\s]+)?",
        r"Associate of Arts(?: in [\w\s]+)?",
        r"Associate of Science(?: in [\w\s]+)?",
        r"Associate of Applied Science(?: in [\w\s]+)?",
        r"Juris Doctor(?: in [\w\s]+)?",
        r"J\.D\.",
        r"Diploma(?: in [\w\s]+)?",
        r"Postgraduate Diploma(?: in [\w\s]+)?",
        r"Graduate Diploma(?: in [\w\s]+)?",
        r"Advanced Diploma(?: in [\w\s]+)?",
    ]

    INSTITUTION_KEYWORDS = (
        "school",
        "college",
        "univers",
        "academy",
        "faculty",
        "institute",
        "polytechnic",
    )

    def __init__(self, specializations_path: Path | None = None) -> None:
        self.specializations_path = (
            specializations_path
            or Path(__file__).resolve().parents[1] / "resources" / "specializations.csv"
        )
        self.specializations = self._load_specializations()
        self.degree_pattern = re.compile("|".join(self.DEGREE_PATTERNS), re.IGNORECASE)

    def extract(self, text: str, doc: Any | None = None) -> EducationDetails:
        return EducationDetails(
            courses=self.extract_courses(text),
            specializations=self.extract_specializations(text),
            college=self.extract_colleges(text),
        )

    def extract_courses(self, text: str) -> List[str]:
        return self._dedupe(match.strip() for match in self.degree_pattern.findall(text))

    def extract_specializations(self, text: str) -> List[str]:
        text_lower = text.lower()
        return self._dedupe(
            specialization
            for specialization in self.specializations
            if re.search(rf"\b{re.escape(specialization.lower())}\b", text_lower)
        )

    def extract_colleges(self, text: str) -> List[str]:
        lines = []
        for line in text.splitlines():
            clean_line = line.strip()
            lower_line = clean_line.lower()
            if clean_line and any(keyword in lower_line for keyword in self.INSTITUTION_KEYWORDS):
                lines.append(clean_line)
        return self._dedupe(lines)

    def _load_specializations(self) -> Set[str]:
        if not self.specializations_path.exists():
            return set()

        specializations: Set[str] = set()
        with self.specializations_path.open(
            "r", encoding="utf-8", errors="ignore", newline=""
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                major = row.get("Major", "").strip()
                if major:
                    specializations.add(major.title())
        return specializations

    def _dedupe(self, values: Iterable[str]) -> List[str]:
        seen: Set[str] = set()
        result: List[str] = []
        for value in values:
            normalized = value.strip()
            key = normalized.lower()
            if normalized and key not in seen:
                seen.add(key)
                result.append(normalized)
        return result
