# FastAPI Resume Parser

A modern, high-performance resume parsing API built with FastAPI that extracts structured information from PDF resumes using advanced NLP techniques.

## 🚀 Features

- **PDF Text Extraction**: Supports multiple PDF parsing methods (PyPDF, pdfminer)
- **NLP Processing**: Uses spaCy for advanced natural language processing
- **Comprehensive Data Extraction**:
  - Personal Information (name, email, phone)
  - Social Media Links (LinkedIn, GitHub, etc.)
  - Skills and Technologies
  - Education Details
  - Work Experience
  - Location and Address Information
  - Languages
- **Modern FastAPI**: Built with the latest FastAPI features
- **Error Handling**: Robust error handling and logging
- **Docker Support**: Containerized for easy deployment
- **AWS Lambda Ready**: Configured for serverless deployment

## 📋 Requirements

- Python 3.9+
- FastAPI 0.115.6+
- spaCy with English model
- Various PDF processing libraries (see requirements.txt)

## 🛠️ Installation

### Option 1: Quick Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd fastapi_resume_parser

# Run the development setup script
python run_dev.py
```

### Option 2: Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy English model
python -m spacy download en_core_web_sm

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Docker

```bash
# Build the Docker image
docker build -t fastapi-resume-parser .

# Run the container
docker run -p 8000:8000 fastapi-resume-parser
```

## 🔧 Usage

### API Endpoints

#### 1. Health Check
```bash
GET /health
```

#### 2. Basic Resume Parsing (Legacy)
```bash
POST /parse_resume
Content-Type: multipart/form-data
Body: file (PDF)
```

#### 3. Advanced Resume Parsing (Recommended)
```bash
POST /parse
Content-Type: multipart/form-data
Body: file (PDF)
```

### Example Response

```json
{
  "status": "success",
  "filename": "john_doe_resume.pdf",
  "personal_info": {
    "name": "John Doe",
    "email": ["john.doe@example.com"],
    "phone_number": "+1234567890"
  },
  "social_links": {
    "linkedin": "linkedin.com/in/johndoe",
    "github": "johndoe",
    "others": []
  },
  "skills": ["Python", "Machine Learning", "FastAPI", "Docker"],
  "education_details": {
    "courses": ["B.Tech"],
    "specializations": ["Computer Science"],
    "college": ["University of Technology"]
  },
  "address": {
    "location": {...},
    "zip_code": ["12345"]
  },
  "languages": ["English", "Spanish"],
  "processing_info": {
    "text_length": 1250,
    "tokens_processed": 320,
    "entities_found": 15
  }
}
```

## 🌐 API Documentation

Once the server is running, you can access:

- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative API Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🧪 Testing

```bash
# Test the API with curl
curl -X POST "http://localhost:8000/parse" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/resume.pdf"
```

## 🚀 Deployment

### Local Development
```bash
python run_dev.py
```

### Production with Docker
```bash
docker build -t fastapi-resume-parser .
docker run -p 8000:8000 fastapi-resume-parser
```

### AWS Lambda (Serverless)
The application is configured for AWS Lambda deployment using Mangum. Update the Dockerfile to use the Lambda base image and deploy using AWS SAM or Serverless Framework.

## 📁 Project Structure

```
fastapi_resume_parser/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── utils.py         # Utility functions for parsing
│   └── assets/          # Static assets
│       ├── skills.csv
│       └── spe.csv
├── Dockerfile           # Container configuration
├── requirements.txt     # Python dependencies
├── run_dev.py          # Development setup script
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables
- `DEBUG`: Enable debug mode (default: False)
- `LOG_LEVEL`: Set logging level (default: INFO)
- `MAX_FILE_SIZE`: Maximum file size for uploads (default: 10MB)

### Skills Database
The application uses a comprehensive skills database that includes:
- Programming languages
- Frameworks and libraries
- Databases
- Cloud platforms
- Tools and technologies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🐛 Known Issues

- Large PDF files may take longer to process
- Some complex PDF layouts may not parse correctly
- Location extraction depends on external geocoding services

## 🔄 Updates (v2.0.0)

- Updated to FastAPI 0.115.6
- Improved error handling and logging
- Enhanced skills extraction with comprehensive database
- Added health check endpoint
- Modernized Dockerfile with multi-stage builds
- Added comprehensive API documentation
- Improved response structure with metadata

## 📞 Support

For support, please open an issue in the repository or contact the maintainers.

Please replace the placeholders with your actual file names and variables. If you have any issues, feel free to ask for help. Happy coding! 😊


if you encounter an error stating that the pip module is not found, you can use the following steps to ensure pip is installed and upgraded:

Open your command prompt or terminal.
Run the following command to ensure pip is installed and upgraded:

```
py -m ensurepip --upgrade
```

This command will install pip if it’s not already installed, and upgrade it to the latest version.