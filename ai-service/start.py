#!/usr/bin/env python3
"""
Start script for the Medical Bill AI Service
"""
import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if environment is properly configured"""
    env_file = ".env"
    
    if not os.path.exists(env_file):
        logger.warning(f"{env_file} not found. Please copy env.example to .env and configure your API key.")
        return False
    
    # Check if GEMINI_API_KEY is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        logger.error("GEMINI_API_KEY not properly configured in .env file")
        return False
    
    return True

def install_dependencies():
    """Install required dependencies"""
    try:
        logger.info("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False

def start_service():
    """Start the AI service"""
    try:
        logger.info("Starting Medical Bill AI Service...")
        logger.info("Make sure you have configured your Gemini API key in .env file")
        logger.info("")
        logger.info("Service will start on http://localhost:8001")
        logger.info("API docs available at http://localhost:8001/docs")
        logger.info("-" * 50)
        
        # Import and run the main application
        from main import app
        import uvicorn
        
        port = int(os.getenv("AI_SERVICE_PORT", 8001))
        host = os.getenv("AI_SERVICE_HOST", "0.0.0.0")
        
        uvicorn.run("main:app", host=host, port=port, reload=True)
        
    except Exception as e:
        logger.error(f"Failed to start service: {e}")
        return False

def main():
    """Main function"""
    logger.info("Medical Bill AI Service Startup")
    logger.info("=" * 40)
    
    # Check dependencies
    if not check_environment():
        logger.error("Environment check failed. Please configure your .env file.")
        sys.exit(1)
    
    # Install dependencies if needed
    try:
        import google.generativeai
        import fastapi
        import uvicorn
    except ImportError:
        logger.info("Some dependencies missing. Installing...")
        if not install_dependencies():
            sys.exit(1)
    
    # Start the service
    start_service()

if __name__ == "__main__":
    main()
