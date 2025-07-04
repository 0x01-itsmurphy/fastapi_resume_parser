#!/bin/bash
# FastAPI Resume Parser - Quick Start Script

echo "🚀 FastAPI Resume Parser - Quick Start"
echo "======================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✅ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo "🧠 Downloading spaCy model..."
python -m spacy download en_core_web_sm

# Run tests
echo "🧪 Running basic tests..."
python -c "import fastapi; print('✅ FastAPI imported successfully')"
python -c "import spacy; print('✅ spaCy imported successfully')"
python -c "import app.main; print('✅ App imports successfully')"

echo ""
echo "🎉 Setup complete!"
echo "📚 To start the server, run:"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "📖 Then visit: http://localhost:8000/docs"
