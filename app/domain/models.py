"""Internal domain models used by the parsing pipeline."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass(frozen=True)
class PersonalInfo:
    name: Optional[str] = None
    email: Set[str] = field(default_factory=set)
    phone_number: Optional[str] = None


@dataclass(frozen=True)
class SocialLinks:
    linkedin: str = ""
    github: str = ""
    others: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class EducationDetails:
    courses: List[str] = field(default_factory=list)
    specializations: List[str] = field(default_factory=list)
    college: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Address:
    location: Optional[Dict[str, Any]] = None
    zip_code: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ProcessingInfo:
    text_length: int
    tokens_processed: int
    entities_found: int


@dataclass(frozen=True)
class ResumeParseResult:
    status: str
    filename: str
    personal_info: PersonalInfo
    social_links: SocialLinks
    skills: List[str]
    education_details: EducationDetails
    address: Address
    languages: Optional[List[str]]
    processing_info: ProcessingInfo
