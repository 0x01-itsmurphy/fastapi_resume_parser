#!/usr/bin/env python3
"""
Test script for FastAPI Resume Parser
"""
import json
from pathlib import Path

import requests


def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
    except requests.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8000")


def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed with status {response.status_code}")
    except requests.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8000")


def test_parse_endpoint_with_sample():
    """Test the parse endpoint with a sample PDF if available"""
    # This is a basic test - you would need to provide a sample PDF
    print("📄 Parse endpoint test requires a sample PDF file")
    print("   To test manually, use:")
    print(
        "   curl -X POST 'http://localhost:8000/v1/resumes/parse' "
        "-H 'Content-Type: multipart/form-data' -F 'file=@your_resume.pdf'"
    )


def main():
    """Main test function"""
    print("🧪 Testing FastAPI Resume Parser")
    print("=" * 40)

    # Test endpoints
    test_health_endpoint()
    print()
    test_root_endpoint()
    print()
    test_parse_endpoint_with_sample()

    print("\n🎉 Basic tests completed!")
    print("📚 Visit http://localhost:8000/docs for interactive API documentation")


if __name__ == "__main__":
    main()
