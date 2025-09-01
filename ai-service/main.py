"""
AI Service Main Application
FastAPI service for Gemini AI integration with medical bill validation
"""
import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv

from gemini_service import GeminiAIService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Medical Bill AI Service",
    description="AI-powered medical bill validation using Google Gemini",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini AI Service
try:
    ai_service = GeminiAIService()
    logger.info("AI Service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AI Service: {e}")
    ai_service = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Medical Bill AI Service",
        "status": "active",
        "ai_service_status": "ready" if ai_service else "unavailable"
    }

@app.get("/status")
async def get_status():
    """Get detailed service status"""
    if not ai_service:
        raise HTTPException(status_code=503, detail="AI service not available")
    
    return ai_service.get_service_status()

@app.get("/test-model")
async def test_model():
    """Test if the Gemini model can be initialized"""
    if not ai_service:
        raise HTTPException(status_code=503, detail="AI service not available")
    
    try:
        # Test model initialization
        test_model = ai_service.test_model_initialization()
        return {
            "status": "success",
            "model_test": test_model
        }
    except Exception as e:
        logger.error(f"Model test failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

@app.post("/test-file-processing")
async def test_file_processing(
    files: List[UploadFile] = File(...)
):
    """Test file processing without AI call"""
    if not ai_service:
        raise HTTPException(status_code=503, detail="AI service not available")
    
    try:
        logger.info(f"🧪 Testing file processing with {len(files)} files")
        
        file_info = []
        for i, file in enumerate(files):
            logger.info(f"📁 Test File {i+1}: {file.filename}, type: {file.content_type}")
            
            # Read file content
            await file.seek(0)
            content = await file.read()
            logger.info(f"📄 File {i+1} content length: {len(content)} bytes")
            
            file_info.append({
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content),
                "first_bytes": content[:100].hex() if content else "empty"
            })
        
        return {
            "status": "success",
            "files_processed": len(files),
            "file_info": file_info
        }
        
    except Exception as e:
        logger.error(f"❌ File processing test failed: {e}")
        import traceback
        logger.error(f"❌ Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"File processing test failed: {str(e)}")

@app.post("/process")
async def process_with_ai(
    model: str = Form("gemini-2.5-pro"),
    prompt: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    Universal AI processing endpoint
    
    Args:
        model: AI model to use (default: gemini-2.5-pro)
        prompt: Custom prompt for AI processing
        files: List of files to process (images, PDFs, documents)
    
    Returns:
        AI processing results based on the prompt and files
    """
    if not ai_service:
        raise HTTPException(status_code=503, detail="AI service not available")
    
    try:
        logger.info(f"🔄 Processing request - Model: {model}, Files: {len(files)}")
        for i, file in enumerate(files):
            logger.info(f"📁 File {i+1}: {file.filename}, type: {file.content_type}, size: {file.size if hasattr(file, 'size') else 'unknown'}")
        
        # Process the request with the flexible AI service
        result = await ai_service.process_with_prompt(
            model=model,
            prompt=prompt,
            files=files
        )
        
        logger.info(f"✅ Processing completed successfully")
        
        return {
            "model_used": model,
            "files_processed": len(files),
            "prompt": prompt,
            "result": result,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"❌ Error processing with AI: {e}")
        import traceback
        logger.error(f"❌ Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("AI_SERVICE_PORT", 8001))
    host = os.getenv("AI_SERVICE_HOST", "0.0.0.0")
    
    uvicorn.run(
        app, 
        host=host, 
        port=port, 
        reload=True
    )
