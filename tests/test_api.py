"""
Unit tests for the FastAPI Resume Parser API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_resume_parser_service
from app.main import app
from app.services.resume_parser import ResumeParserService

client = TestClient(app)


class TestHealthEndpoints:
    """Test suite for health check and root endpoints."""

    def test_root_endpoint(self):
        """Test the root endpoint returns correct status."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert "Resume Parser" in data["message"]
        assert "version" in data

    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "resume-parser"


class TestParseEndpoint:
    """Test suite for resume parsing endpoints."""

    def test_parse_without_file(self):
        """Test parse endpoint without file upload."""
        response = client.post("/parse")
        assert response.status_code == 422  # Unprocessable Entity

    def test_parse_with_non_pdf(self):
        """Test parse endpoint with non-PDF file."""
        files = {"file": ("test.txt", b"test content", "text/plain")}
        response = client.post("/parse", files=files)
        assert response.status_code == 400
        assert "PDF" in response.json()["detail"]

    def test_parse_with_empty_pdf(self):
        """Test parse endpoint with empty PDF."""
        # Create a minimal but invalid PDF
        files = {"file": ("test.pdf", b"%PDF-", "application/pdf")}
        response = client.post("/parse", files=files)
        assert response.status_code == 422

    def test_v1_parse_with_non_pdf(self):
        """Test versioned parse endpoint with non-PDF file."""
        files = {"file": ("test.txt", b"test content", "text/plain")}
        response = client.post("/v1/resumes/parse", files=files)
        assert response.status_code == 400
        assert "PDF" in response.json()["detail"]

    def test_parse_success_serializes_domain_result(self):
        """Test successful parser domain result is serialized into API schema."""
        parser = ResumeParserService()
        text = "\n".join(
            [
                "Jane Doe",
                "jane@example.com",
                "+1 555 123 4567",
                "https://github.com/janedoe",
                "Skills: Python, FastAPI, Docker",
                "Bachelor of Science in Computer Science",
                "English, French",
            ]
        )

        app.dependency_overrides = {}
        app.dependency_overrides[get_resume_parser_service] = lambda: parser
        parser.text_extractor.extract = lambda contents: text

        try:
            files = {"file": ("resume.pdf", b"%PDF-1.4\nstub", "application/pdf")}
            response = client.post("/v1/resumes/parse", files=files)
        finally:
            app.dependency_overrides = {}

        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "resume.pdf"
        assert data["personal_info"]["email"] == ["jane@example.com"]
        assert "Python" in data["skills"]


class TestErrorHandling:
    """Test suite for error handling."""

    def test_404_endpoint(self):
        """Test non-existent endpoint returns 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_invalid_method(self):
        """Test invalid HTTP method."""
        response = client.get("/parse")  # Should be POST
        assert response.status_code == 405  # Method Not Allowed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
