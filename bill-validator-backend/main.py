"""
Medical Bill Validation System - FastAPI Backend with Color-Coded Results
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging
import time
from bill_validator import BillValidator
from models import (
    ValidationResponse, BillExtractionResponse, DocumentProcessingResponse, 
    ErrorResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Medical Bill Validation System with Color-Coded Results", 
    version="4.0.0",
    description="AI-powered medical bill validation system that provides color-coded results for easy identification of matches, partial matches, and mismatches"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize bill validator
validator = BillValidator()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Medical Bill Validation System API with Color-Coded Results", 
        "status": "active",
        "version": "4.0.0",
        "features": [
            "Extract bill entries from PDF tables",
            "Process supporting documents (bills, prescriptions, invoices)", 
            "Validate bills with color-coded results",
            "Green: Perfect match",
            "Red: Partial match with discrepancies",
            "Yellow: No supporting document found"
        ],
        "endpoints": [
            "/extract-bills - Extract bill entries from PDF",
            "/process-documents - Process supporting documents",
            "/validate-bills - Complete validation workflow with color coding"
        ]
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "validator_status": "initialized",
        "ai_service_url": validator.ai_service_url
    }

@app.get("/test-ai-service")
async def test_ai_service():
    """Test connection to AI service"""
    try:
        import aiohttp
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
            async with session.get("http://localhost:8001/") as response:
                if response.status == 200:
                    return {
                        "status": "success",
                        "ai_service": "connected",
                        "response": await response.json()
                    }
                else:
                    return {
                        "status": "error",
                        "ai_service": "unreachable",
                        "status_code": response.status
                    }
    except Exception as e:
        return {
            "status": "error",
            "ai_service": "connection_failed",
            "error": str(e)
        }

@app.post("/extract-bills", response_model=BillExtractionResponse)
async def extract_bill_entries(
    bill_entries_file: UploadFile = File(..., description="PDF or image containing bill entries table")
):
    """
    Extract bill entries from PDF table and return structured JSON
    
    This endpoint processes medical bill PDFs containing tables with columns like:
    - SI No, Bill/Cash Memo, Bill Date, Classification, Type of Treatment
    - Account Code, Description, Amount, Med Pass Amount, etc.
    
    Returns structured JSON data that can be used for validation.
    """
    try:
        start_time = time.time()
        
        # Check if file is PDF or image
        file_extension = bill_entries_file.filename.lower()
        logger.info(f"📁 File extension: {file_extension}")
        logger.info(f"📁 File content type: {bill_entries_file.content_type}")
        logger.info(f"📁 File size: {getattr(bill_entries_file, 'size', 'unknown')}")
        
        if not (file_extension.endswith('.pdf') or 
                file_extension.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))):
            logger.error(f"❌ Invalid file type: {file_extension}")
            raise HTTPException(
                status_code=400, 
                detail="File must be a PDF or image (JPG, PNG, BMP, TIFF) containing bill entries table"
            )
        
        logger.info(f"📋 Extracting bill entries from {bill_entries_file.filename}")
        
        try:
            bill_entries = await validator.extract_bill_entries(bill_entries_file)
            logger.info(f"📋 Validator returned {len(bill_entries) if bill_entries else 0} entries")
        except Exception as e:
            logger.error(f"❌ Validator error: {str(e)}")
            import traceback
            logger.error(f"❌ Validator traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=400,
                detail=f"Bill extraction failed: {str(e)}"
            )
        
        if not bill_entries:
            logger.warning("⚠️ No bill entries found in the file")
            raise HTTPException(
                status_code=400, 
                detail="No bill entries found in the PDF. Please ensure the PDF contains a readable table with medical expense entries."
            )
        
        extraction_time = time.time() - start_time
        
        response = BillExtractionResponse(
            message="Bill entries extracted successfully", 
            bill_entries=bill_entries, 
            count=len(bill_entries),
            extraction_time=extraction_time
        )
        
        logger.info(f"✅ Extracted {len(bill_entries)} bill entries in {extraction_time:.2f}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Bill extraction failed: {str(e)}")
        error_response = ErrorResponse(
            error="Bill extraction failed",
            details=str(e)
        )
        return JSONResponse(
            status_code=500,
            content=error_response.dict()
        )

@app.post("/process-documents", response_model=DocumentProcessingResponse)
async def process_documents(
    supporting_documents: List[UploadFile] = File(..., description="Supporting bill documents (PDFs/Images)")
):
    """
    Process supporting documents to extract bill information
    
    This endpoint processes various medical documents like:
    - Bills and invoices
    - Prescriptions
    - Medical reports
    - Receipts
    
    Uses AI to extract bill numbers, amounts, dates, and other relevant information
    for validation against the main bill entries.
    """
    try:
        start_time = time.time()
        
        if not supporting_documents:
            raise HTTPException(
                status_code=400, 
                detail="At least one supporting document must be provided"
            )
        
        logger.info(f"📄 Processing {len(supporting_documents)} supporting documents")
        
        processed_docs = await validator.process_supporting_documents(supporting_documents)
        
        processing_time = time.time() - start_time
        
        response = DocumentProcessingResponse(
            message="Documents processed successfully",
            processed_documents=processed_docs,
            count=len(processed_docs),
            processing_time=processing_time
        )
        
        logger.info(f"✅ Processed {len(processed_docs)} documents in {processing_time:.2f}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Document processing failed: {str(e)}")
        error_response = ErrorResponse(
            error="Document processing failed",
            details=str(e)
        )
        return JSONResponse(
            status_code=500,
            content=error_response.dict()
        )

@app.post("/validate-bills", response_model=ValidationResponse)
async def validate_bills(
    bill_entries_file: UploadFile = File(..., description="PDF or image containing bill entries table"),
    supporting_documents: List[UploadFile] = File(..., description="Supporting bill documents (PDFs/Images)")
):
    """
    Complete bill validation workflow with color-coded results
    
    This is the main endpoint that performs the complete validation:
    1. Extracts bill entries from the main PDF table
    2. Processes supporting documents to extract bill information
    3. Validates bills against supporting documents
    4. Returns color-coded results:
       - 🟢 Green: Perfect match (bill and document match completely)
       - 🔴 Red: Partial match (some fields don't match or have discrepancies)
       - 🟡 Yellow: No match (no supporting document found)
    
    The response includes detailed validation results with color coding,
    making it easy to identify which bills need attention.
    """
    try:
        logger.info("🚀 Starting complete bill validation workflow with color coding")
        
        # Validate file types
        file_extension = bill_entries_file.filename.lower()
        if not (file_extension.endswith('.pdf') or 
                file_extension.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))):
            raise HTTPException(
                status_code=400, 
                detail="Bill entries file must be a PDF or image (JPG, PNG, BMP, TIFF) containing the main table"
            )
        
        if not supporting_documents:
            raise HTTPException(
                status_code=400, 
                detail="At least one supporting document must be provided for validation"
            )
        
        # Run complete validation workflow
        validation_response = await validator.complete_validation_workflow(
            bill_entries_file, 
            supporting_documents
        )
        
        logger.info("✅ Validation completed successfully with color-coded results")
        return validation_response
        
    except ValueError as e:
        logger.error(f"❌ Validation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Validation failed: {str(e)}")
        error_response = ErrorResponse(
            error="Validation failed",
            details=str(e)
        )
        return JSONResponse(
            status_code=500,
            content=error_response.dict()
        )

@app.get("/validation-summary")
async def get_validation_summary():
    """
    Get a summary of the validation system capabilities and color coding legend
    """
    return {
        "system_info": {
            "name": "Medical Bill Validation System",
            "version": "4.0.0",
            "description": "AI-powered system for validating medical bills against supporting documents"
        },
        "color_coding": {
            "green": {
                "status": "Perfect Match",
                "description": "Bill and supporting document match completely",
                "meaning": "No action required - bill is properly documented"
            },
            "red": {
                "status": "Partial Match",
                "description": "Some fields don't match or have discrepancies",
                "meaning": "Review required - check for data entry errors or missing information"
            },
            "yellow": {
                "status": "No Match",
                "description": "No supporting document found for this bill",
                "meaning": "Action required - locate and upload missing supporting document"
            }
        },
        "validation_criteria": {
            "bill_number_matching": "Fuzzy matching with normalization (removes spaces, hyphens, etc.)",
            "amount_matching": "5% tolerance for amount differences",
            "date_matching": "Exact string comparison (can be enhanced with date parsing)",
            "confidence_threshold": "80% minimum confidence for document matching"
        },
        "supported_formats": {
            "bill_entries": "PDF with readable tables",
            "supporting_documents": "PDF, Images (JPG, PNG), Documents"
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "details": "An unexpected error occurred. Please try again later.",
            "timestamp": time.time()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
