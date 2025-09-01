"""
Gemini AI Service for Medical Bill Validation
"""
import os
import logging
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from PIL import Image
import io
import base64
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Warning: PyPDF2 not available. PDF processing will be limited.")
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiAIService:
    """Service class for interacting with Google Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini AI service"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        try:
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            
            # Initialize model with Gemini 2.5 Pro
            self.model = genai.GenerativeModel('gemini-2.5-pro')
            
            logger.info("Gemini AI Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {e}")
            self.api_key = None
            self.model = None
    
    async def process_with_prompt(self, model: str, prompt: str, files: List[Any]) -> Dict[str, Any]:
        """
        Universal processing method that takes model, prompt, and files
        
        Args:
            model: Model name to use (e.g., 'gemini-1.5-flash', 'gemini-1.5-pro')
            prompt: Custom prompt for processing
            files: List of uploaded files to process
            
        Returns:
            Processing results based on the prompt and files
        """
        # Mock service if API key not configured
        if not self.api_key or not self.model:
            return self._generate_mock_response(prompt, files)
        
        try:
            # Initialize the specified model
            if model not in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.5-pro', 'gemini-2.5-flash', 'gemini-2.0-flash-exp', 'gemini-2.0-pro', 'gemini-pro-vision']:
                model = 'gemini-2.5-pro'  # Default to Gemini 2.5 pro
            
            logger.info(f"🔄 Initializing Gemini model: {model}")
            
            try:
                processing_model = genai.GenerativeModel(model)
                logger.info(f"✅ Model {model} initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize model {model}, falling back to gemini-2.5-pro: {e}")
                model = 'gemini-2.5-pro'
                processing_model = genai.GenerativeModel(model)
                logger.info(f"✅ Fallback model {model} initialized successfully")
            
            # Prepare content for processing
            content_parts = [prompt]
            file_info = []
            
            # Process each file
            for file in files:
                try:
                    logger.info(f"📁 Processing file: {file.filename}, type: {file.content_type}")
                    
                    # Read file content
                    file_content = await file.read()
                    file_info.append({
                        "filename": file.filename,
                        "content_type": file.content_type,
                        "size": len(file_content)
                    })
                    
                    logger.info(f"📄 File content read: {len(file_content)} bytes")
                    
                    # Handle different file types
                    if file.content_type and file.content_type.startswith('image/'):
                        # Process as image
                        logger.info(f"🖼️ Processing as image: {file.filename}")
                        image = Image.open(io.BytesIO(file_content))
                        content_parts.append(image)
                        logger.info(f"✅ Image added to content parts")
                        
                    elif file.content_type == 'application/pdf':
                        # Process PDF files by extracting text content
                        logger.info(f"📄 Processing as PDF: {file.filename}")
                        if PDF_AVAILABLE:
                            try:
                                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                                pdf_text = ""
                                for page_num in range(len(pdf_reader.pages)):
                                    page = pdf_reader.pages[page_num]
                                    pdf_text += f"\n--- Page {page_num + 1} ---\n"
                                    pdf_text += page.extract_text()
                                
                                content_parts.append(f"PDF Document: {file.filename}\n\nContent:\n{pdf_text}")
                                logger.info(f"✅ Successfully extracted text from PDF: {file.filename}, text length: {len(pdf_text)}")
                            except Exception as e:
                                logger.warning(f"⚠️ Error processing PDF {file.filename}: {e}")
                                content_parts.append(f"[Error processing PDF: {file.filename} - {str(e)}]")
                        else:
                            logger.warning(f"⚠️ PDF processing not available - PyPDF2 not installed")
                            content_parts.append(f"[PDF processing not available - {file.filename}]")
                        
                    elif file.content_type and file.content_type.startswith('text/'):
                        # Process text files
                        logger.info(f"📝 Processing as text: {file.filename}")
                        text_content = file_content.decode('utf-8')
                        content_parts.append(f"File: {file.filename}\nContent:\n{text_content}")
                        logger.info(f"✅ Text content added, length: {len(text_content)}")
                        
                    else:
                        # Unsupported file type
                        logger.warning(f"❌ Unsupported file type: {file.filename} - {file.content_type}")
                        content_parts.append(f"[Unsupported file type: {file.filename} - {file.content_type}]")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Error processing file {file.filename}: {e}")
                    content_parts.append(f"[Error processing file: {file.filename}]")
            
            # Generate response using Gemini
            logger.info(f"🚀 Sending request to Gemini with {len(content_parts)} content parts")
            logger.info(f"📝 Content parts: {[type(part).__name__ for part in content_parts]}")
            
            try:
                response = processing_model.generate_content(content_parts)
                logger.info(f"✅ Gemini response received successfully")
                
                return {
                    "model_used": model,
                    "prompt": prompt,
                    "files_info": file_info,
                    "raw_response": response.text,
                    "processing_method": "gemini_universal",
                    "status": "success"
                }
            except Exception as e:
                logger.error(f"❌ Gemini API error: {e}")
                logger.error(f"❌ Error type: {type(e).__name__}")
                import traceback
                logger.error(f"❌ Full traceback: {traceback.format_exc()}")
                raise
            
        except Exception as e:
            logger.error(f"Error in universal processing: {e}")
            return {
                "model_used": model,
                "prompt": prompt,
                "error": str(e),
                "status": "error"
            }
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get service status and configuration"""
        return {
            "service": "Gemini AI Service",
            "status": "active" if self.api_key else "mock_mode",
            "available_models": [
                "gemini-2.0-flash-exp",
                "gemini-1.5-flash",
                "gemini-1.5-pro", 
                "gemini-2.5-pro",
                "gemini-2.5-flash",
                "gemini-pro",
                "gemini-pro-vision"
            ],
            "api_configured": bool(self.api_key),
            "capabilities": [
                "universal_ai_processing",
                "image_analysis",
                "text_processing",
                "multi_modal_understanding",
                "custom_prompts"
            ]
        }
    
    def test_model_initialization(self) -> Dict[str, Any]:
        """Test if different models can be initialized"""
        if not self.api_key:
            return {"status": "mock_mode", "message": "No API key configured"}
        
        test_results = {}
        test_models = ['gemini-2.5-pro', 'gemini-2.0-pro', 'gemini-1.5-pro']
        
        for test_model in test_models:
            try:
                test_gen_model = genai.GenerativeModel(test_model)
                test_results[test_model] = "success"
            except Exception as e:
                test_results[test_model] = f"failed: {str(e)}"
        
        return {
            "status": "tested",
            "results": test_results
        }
    
    def _generate_mock_response(self, prompt: str, files: List[Any]) -> Dict[str, Any]:
        """Generate mock response for demo purposes when API key is not configured"""
        logger.info("Generating mock response for demonstration")
        
        # Check if the prompt is asking for bill entries extraction
        if "bill entries" in prompt.lower() or "extract" in prompt.lower():
            mock_response = """
            [
                {
                    "si_no": 1,
                    "bill_cash_memo": "DEMO001",
                    "bill_date": "1/15/24",
                    "classification": "HOSPITAL CONSULTATION",
                    "type_of_treatment": "Allopathic",
                    "account_code": "550",
                    "description": "MEDICAL REIMBURSEMENT SPECIAL DESEASES",
                    "amount": 1500.00,
                    "med_pass_amount": 1500.00,
                    "fin_pass_amount_taxable": 1500.00,
                    "fin_pass_non_taxable": null
                },
                {
                    "si_no": 2,
                    "bill_cash_memo": "DEMO002", 
                    "bill_date": "1/16/24",
                    "classification": "MEDICINES",
                    "type_of_treatment": "Allopathic",
                    "account_code": "550",
                    "description": "MEDICAL REIMBURSEMENT SPECIAL DESEASES",
                    "amount": 2300.50,
                    "med_pass_amount": 2300.50,
                    "fin_pass_amount_taxable": 2300.50,
                    "fin_pass_non_taxable": null
                },
                {
                    "si_no": 3,
                    "bill_cash_memo": "DEMO003",
                    "bill_date": "1/17/24",
                    "classification": "PATHOLOGICAL TEST",
                    "type_of_treatment": "Allopathic",
                    "account_code": "550",
                    "description": "MEDICAL REIMBURSEMENT SPECIAL DESEASES",
                    "amount": 850.75,
                    "med_pass_amount": 850.75,
                    "fin_pass_amount_taxable": 850.75,
                    "fin_pass_non_taxable": null
                }
            ]
            """
        elif "document" in prompt.lower() and "extract" in prompt.lower():
            mock_response = """
            {
                "bill_number": "DEMO001",
                "amount": 1500.00,
                "patient_name": "John Doe",
                "date": "1/15/24",
                "hospital_name": "City Hospital",
                "document_type": "bill",
                "confidence_score": 0.95,
                "extracted_text": "MEDICAL BILL - City Hospital - Patient: John Doe - Bill #: DEMO001 - Amount: ₹1,500.00 - Date: 15/01/2024"
            }
            """
        else:
            mock_response = """
            {
                "analysis": "This is a mock AI response for demonstration purposes.",
                "confidence": 0.85,
                "status": "demo_mode"
            }
            """
        
        return {
            "model_used": "mock-gemini",
            "prompt": prompt,
            "files_info": [{"filename": f.filename, "size": "mock"} for f in files if hasattr(f, 'filename')],
            "raw_response": mock_response,
            "processing_method": "mock_demo",
            "status": "success"
        }
