# Contributing to FastAPI Resume Parser

Thank you for your interest in contributing to the FastAPI Resume Parser project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/fastapi_resume_parser.git`
3. Add the upstream repository: `git remote add upstream https://github.com/ORIGINAL_OWNER/fastapi_resume_parser.git`

## Development Setup

1. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Download required NLTK data:**

   ```bash
   python -c "import nltk; nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('maxent_ne_chunker_tab'); nltk.download('stopwords'); nltk.download('words')"
   ```

4. **Run the development server:**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## Making Changes

1. **Create a new branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Write tests** for your changes

4. **Run the test suite:**

   ```bash
   pytest
   ```

5. **Format your code:**

   ```bash
   black app/ tests/
   isort app/ tests/
   ```

6. **Type check your code:**
   ```bash
   mypy app/
   ```

## Testing

- Write unit tests for all new functions
- Write integration tests for API endpoints
- Ensure test coverage remains above 75%
- Run tests with: `pytest --cov=app`

## Code Style

This project follows:

- **PEP 8** for Python code style
- **Black** for code formatting (line length: 100)
- **isort** for import sorting
- **Type hints** for all function signatures
- **Docstrings** in Google style format

Example function:

```python
def extract_email(text: str) -> Set[str]:
    """Extract email addresses from text.

    Args:
        text: Input text to search for emails

    Returns:
        Set of email addresses found
    """
    # Implementation
```

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass:**

   ```bash
   pytest
   black --check app/ tests/
   isort --check app/ tests/
   flake8 app/ tests/
   mypy app/
   ```

4. **Update CHANGELOG.md** with your changes

5. **Submit a pull request** with:

   - Clear description of changes
   - Link to related issues
   - Screenshots for UI changes
   - Test results

6. **Wait for review** - maintainers will review and provide feedback

## Questions?

Feel free to open an issue for:

- Bug reports
- Feature requests
- Questions about contributing

Thank you for contributing! 🎉
