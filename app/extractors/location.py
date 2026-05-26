"""Offline location and postal-code extraction."""

import re
from typing import Any

import locationtagger

from app.core.logging import get_logger
from app.domain.models import Address

logger = get_logger(__name__)


class LocationExtractor:
    """Extract location details without making external network calls."""

    ZIP_CODE_PATTERN = re.compile(r"\b(?:\d{5}(?:-\d{4})?|\d{6})\b")

    def extract(self, text: str, doc: Any | None = None) -> Address:
        return Address(
            location=self.extract_location(text),
            zip_code=self.extract_zip_codes(text),
        )

    def extract_zip_codes(self, text: str) -> list[str]:
        return list(dict.fromkeys(self.ZIP_CODE_PATTERN.findall(text)))

    def extract_location(self, text: str) -> dict[str, Any] | None:
        try:
            place = locationtagger.find_locations(text=text)
            cities = place.cities or []
            countries = place.countries or []
            regions = place.regions or []
        except Exception as exc:
            logger.warning("Offline location extraction failed: %s", exc)
            return None

        city = cities[0] if cities else None
        state = regions[0] if regions else None
        country = countries[0] if countries else None

        if not any([city, state, country]):
            return None

        return {
            "formatted": None,
            "streetNumber": None,
            "street": None,
            "apartmentNumber": None,
            "city": city,
            "postalCode": None,
            "state": state,
            "country": country,
        }
