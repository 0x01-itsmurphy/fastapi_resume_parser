"""Offline location and postal-code extraction."""

import re
from typing import Any

import locationtagger

from app.core.logging import get_logger
from app.domain.models import Address

logger = get_logger(__name__)


class LocationExtractor:
    """Extract location details without making external network calls."""

    # Common language names that should not be treated as locations
    LANGUAGE_NAMES = {
        'english', 'spanish', 'french', 'german', 'italian', 'portuguese',
        'russian', 'chinese', 'japanese', 'korean', 'arabic', 'hindi',
        'bengali', 'punjabi', 'marathi', 'gujarati', 'tamil', 'urdu',
        'pashto', 'turkish', 'vietnamese', 'thai', 'burmese', 'malay'
    }

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

        # Filter out language names from cities
        cities = [city for city in cities if city.lower() not in self.LANGUAGE_NAMES]
        
        # Additional filtering: remove single letters that are likely not real places
        cities = [city for city in cities if len(city) > 1]
        
        city = cities[0] if cities else None
        state = regions[0] if regions else None
        country = countries[0] if countries else None

        if not any([city, state, country]):
            return None

        # Improve city/state disambiguation for US locations
        # If we have a state but no country, and it looks like a US state, set country to US
        US_STATES = {
            'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado',
            'connecticut', 'delaware', 'florida', 'georgia', 'hawaii', 'idaho',
            'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana',
            'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota',
            'mississippi', 'missouri', 'montana', 'nebraska', 'nevada',
            'new hampshire', 'new jersey', 'new mexico', 'new york',
            'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon',
            'pennsylvania', 'rhode island', 'south carolina', 'south dakota',
            'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington',
            'west virginia', 'wisconsin', 'wyoming'
        }
        if state and state.lower() in US_STATES and not country:
            country = 'United States'

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
