"""Skill extraction from local resources."""

import csv
import re
from pathlib import Path
from typing import Any, Iterable, List, Set


class SkillExtractor:
    """Extract known skills using a local skills vocabulary."""

    NON_SKILL_TERMS = {"arabic", "bengali", "business", "chinese", "com", "communication", "computer science", "english", "french", "german", "hindi", "http", "https", "information technology", "italian", "japanese", "korean", "leadership", "management", "net", "org", "portuguese", "spanish", "teamwork", "www"}

    def __init__(self, skills_path: Path | None = None) -> None:
        self.skills_path = (
            skills_path or Path(__file__).resolve().parents[1] / "resources" / "skills.csv"
        )
        self.skills = self._load_skills()

    def extract(self, text: str, doc: Any | None = None) -> List[str]:
        text_lower = text.lower()
        found: Set[str] = set()

        for skill in self.skills:
            # Skip non-technical terms
            if skill in self.NON_SKILL_TERMS:
                continue
                
            pattern = rf"(?<![A-Za-z0-9+#.]){re.escape(skill)}(?![A-Za-z0-9+#.])"
            if re.search(pattern, text_lower):
                found.add(skill)

        return [self._display_name(skill) for skill in sorted(found)]
    def _load_skills(self) -> Set[str]:
        if not self.skills_path.exists():
            return set()

        skills: Set[str] = set()
        with self.skills_path.open("r", encoding="utf-8", errors="ignore", newline="") as csvfile:
            # Read all rows and flatten them into a single list of skills
            for row in csv.reader(csvfile):
                skills.update(self._clean_values(row))
        return skills

    def _clean_values(self, values: Iterable[str]) -> Iterable[str]:
        for value in values:
            skill = value.strip().lower()
            if len(skill) >= 2 and skill != "technical skills":
                yield skill

    def _display_name(self, skill: str) -> str:
        preserve_upper = {"aws", "gcp", "html", "css", "sql", "api", "ios", "nlp", "qa", "ui", "ux"}
        if skill in preserve_upper:
            return skill.upper()
        # Handle versioned skills like node.js, node.js -> Node.js
        if '.' in skill and not skill.startswith('.') and not skill.endswith('.'):
            parts = skill.split('.')
            return '.'.join(part.title() for part in parts)
        return skill.title()
