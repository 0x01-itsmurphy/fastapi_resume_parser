# FastAPI Resume Parser

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

A modern, high-performance resume parsing API built with FastAPI that extracts structured information from PDF resumes using advanced NLP techniques.

## 🌟 Features

- **Advanced PDF Processing** - Supports multiple PDF parsing methods (PyPDF, pdfminer.six)
- **NLP-Powered Extraction** - Uses spaCy for intelligent text analysis
- **Comprehensive Data Extraction**:
  - 📧 Personal Information (name, email, phone)
  - 🔗 Social Media Links (LinkedIn, GitHub)
  - 💼 Skills and Technologies
  - 🎓 Education Details
  - 🗺️ Location and Address Information
  - 🌍 Languages
- **Modern FastAPI** - Built with FastAPI 0.128.0 with automatic OpenAPI documentation
- **Type-Safe** - Comprehensive type hints throughout
- **Production-Ready** - Proper error handling, logging, and validation
- **Maintainable Architecture** - Clear API, service, extractor, schema, and domain layers
- **Docker Support** - Containerized for easy deployment
- **AWS Lambda Ready** - Configured for serverless deployment

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/fastapi_resume_parser.git
   cd fastapi_resume_parser
   ```

2. **Create virtual environment**

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download required NLTK data**

   ```bash
   python -c "import nltk; nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('maxent_ne_chunker_tab'); nltk.download('stopwords'); nltk.download('words')"
   ```

5. **Run the server**

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Test the API**

   Visit http://localhost:8000/docs for interactive API documentation

## 📖 API Documentation

### Endpoints

| Method | Endpoint  | Description                          |
| ------ | --------- | ------------------------------------ |
| GET    | `/`       | Root endpoint - API status           |
| GET    | `/health` | Health check endpoint                |
| POST   | `/v1/resumes/parse` | Parse resume and extract information |
| POST   | `/parse`  | Backward-compatible parse endpoint   |

### Example Usage

**Using cURL:**

```bash
curl -X POST "http://localhost:8000/v1/resumes/parse" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
```

**Using Python:**

```python
import requests

url = "http://localhost:8000/v1/resumes/parse"
files = {"file": open("resume.pdf", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Response Format

```json
{
  "status": "success",
  "filename": "resume.pdf",
  "personal_info": {
    "name": "John Doe",
    "email": ["john.doe@example.com"],
    "phone_number": "+1234567890"
  },
  "social_links": {
    "linkedin": "linkedin.com/in/johndoe",
    "github": "johndoe"
  },
  "skills": ["Python", "FastAPI", "Machine Learning"],
  "education_details": {
    "courses": ["B.Tech"],
    "specializations": ["Computer Science"],
    "college": ["University of Technology"]
  },
  "languages": ["English"],
  "processing_info": {
    "text_length": 1250,
    "tokens_processed": 320,
    "entities_found": 15
  }
}
```

## 🏗️ Project Structure

```
fastapi_resume_parser/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   ├── errors.py          # Application-specific exceptions
│   │   └── logging.py         # Logging setup
│   ├── api/
│   │   ├── dependencies.py    # FastAPI dependency factories
│   │   └── routes/            # HTTP route modules
│   ├── domain/
│   │   └── models.py          # Internal parser result models
│   ├── extractors/            # Focused resume field extractors
│   ├── resources/             # Local parsing vocabularies
│   ├── schemas/
│   │   └── responses.py       # Public API response models
│   ├── services/              # Parser orchestration and infrastructure services
│   ├── main.py                # FastAPI application
├── tests/
│   └── test_api.py            # API tests
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── pyproject.toml             # Tool configurations
├── Dockerfile                 # Docker configuration
└── README.md                  # This file
```

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html
```

## 🛠️ Development

### Code Quality

This project uses several tools to maintain code quality:

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

### Pre-commit Hooks

Install pre-commit hooks to automatically check code quality:

```bash
pre-commit install
```

## 🐳 Docker

### Build and Run

```bash
# Build the image
docker build -t fastapi-resume-parser .

# Run the container
docker run -p 8000:8000 fastapi-resume-parser
```

## 🚀 Deployment

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
DEBUG=false
LOG_LEVEL=info
MAX_FILE_SIZE=10485760
CORS_ORIGINS=*
ALLOW_CREDENTIALS=false
```

### Production Deployment

The app is ready to deploy as a standard ASGI service with Uvicorn, as a Docker
container, or behind an API gateway using the included Mangum handler.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [spaCy](https://spacy.io/) - Industrial-strength NLP
- [pdfminer.six](https://github.com/pdfminer/pdfminer.six) - PDF text extraction

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using FastAPI and Python**
