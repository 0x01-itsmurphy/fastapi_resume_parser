#!/usr/bin/env python3
"""
Development server runner for FastAPI Resume Parser
"""
import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install dependencies from requirements.txt"""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def download_spacy_model():
    """Download spaCy English model"""
    print("Downloading spaCy model...")
    try:
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], 
                      check=True)
        print("✅ spaCy model downloaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download spaCy model: {e}")
        sys.exit(1)

def run_server():
    """Run the FastAPI development server"""
    print("Starting FastAPI development server...")
    try:
        subprocess.run([
            "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload",
            "--log-level", "info"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")

def main():
    """Main function"""
    print("🚀 FastAPI Resume Parser Development Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app/main.py").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    # Download spaCy model
    download_spacy_model()
    
    # Run server
    run_server()

if __name__ == "__main__":
    main()
