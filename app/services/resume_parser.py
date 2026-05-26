"""Resume parser orchestration service."""

from fastapi import UploadFile

from app.domain.models import ProcessingInfo, ResumeParseResult
from app.extractors.contact import ContactExtractor
from app.extractors.education import EducationExtractor
from app.extractors.languages import LanguageExtractor
from app.extractors.location import LocationExtractor
from app.extractors.profiles import ProfileExtractor
from app.extractors.skills import SkillExtractor
from app.services.nlp_service import NlpService
from app.services.pdf_text_extractor import PdfTextExtractor
from app.services.validation import UploadValidationService


class ResumeParserService:
    """Coordinate validation, text extraction, NLP, and field extractors."""

    def __init__(
        self,
        validator: UploadValidationService | None = None,
        text_extractor: PdfTextExtractor | None = None,
        nlp_service: NlpService | None = None,
        contact_extractor: ContactExtractor | None = None,
        profile_extractor: ProfileExtractor | None = None,
        skill_extractor: SkillExtractor | None = None,
        education_extractor: EducationExtractor | None = None,
        location_extractor: LocationExtractor | None = None,
        language_extractor: LanguageExtractor | None = None,
    ) -> None:
        self.validator = validator or UploadValidationService()
        self.text_extractor = text_extractor or PdfTextExtractor()
        self.nlp_service = nlp_service or NlpService()
        self.contact_extractor = contact_extractor or ContactExtractor()
        self.profile_extractor = profile_extractor or ProfileExtractor()
        self.skill_extractor = skill_extractor or SkillExtractor()
        self.education_extractor = education_extractor or EducationExtractor()
        self.location_extractor = location_extractor or LocationExtractor()
        self.language_extractor = language_extractor or LanguageExtractor()

    async def parse_upload(self, file: UploadFile) -> ResumeParseResult:
        """Parse a FastAPI upload into structured resume data."""
        contents = await file.read()
        self.validator.validate(file, contents)

        text = self.text_extractor.extract(contents)
        doc = self.nlp_service.process(text)

        return ResumeParseResult(
            status="success",
            filename=file.filename or "resume.pdf",
            personal_info=self.contact_extractor.extract(text, doc),
            social_links=self.profile_extractor.extract(text, doc),
            skills=self.skill_extractor.extract(text, doc),
            education_details=self.education_extractor.extract(text, doc),
            address=self.location_extractor.extract(text, doc),
            languages=self.language_extractor.extract(text, doc),
            processing_info=ProcessingInfo(
                text_length=len(text),
                tokens_processed=len(doc),
                entities_found=len(doc.ents),
            ),
        )
