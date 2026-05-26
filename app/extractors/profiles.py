"""Social profile and URL extraction."""

import re
from typing import Any

from urlextract import URLExtract

from app.domain.models import SocialLinks


class ProfileExtractor:
    """Extract LinkedIn, GitHub, and other URLs."""

    LINKEDIN_PATTERN = re.compile(
        r"(?:(?:https?://)?(?:www\.)?)linkedin\.com/(?:pub|in|profile)/[-a-zA-Z0-9_%]+/?",
        re.IGNORECASE,
    )
    GITHUB_PATTERN = re.compile(
        r"(?:(?:https?://)?(?:www\.)?)github\.com/([A-Za-z0-9-]+)",
        re.IGNORECASE,
    )

    def __init__(self) -> None:
        self.url_extractor = URLExtract()

    def extract(self, text: str, doc: Any | None = None) -> SocialLinks:
        urls = self.url_extractor.find_urls(text)
        linkedin = self._first_match(self.LINKEDIN_PATTERN, text)
        github_match = self.GITHUB_PATTERN.search(text)
        github = github_match.group(1) if github_match else ""
        others = [url for url in urls if url != linkedin and "github.com" not in url.lower()]

        return SocialLinks(linkedin=linkedin, github=github, others=others)

    def _first_match(self, pattern: re.Pattern[str], text: str) -> str:
        match = pattern.search(text)
        return match.group(0) if match else ""
