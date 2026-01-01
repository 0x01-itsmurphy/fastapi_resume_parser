"""
Unit tests for the FastAPI Resume Parser API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

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
        assert response.status_code in [400, 500]  # Either validation or processing error


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
