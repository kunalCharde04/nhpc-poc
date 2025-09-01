"""
AI-Powered Medical Bill Validator with Color-Coded Results - FIXED VERSION
Handles extraction, processing, and validation with proper JSON structure
"""
import aiohttp
import json
import logging
import time
from typing import List, Dict, Any, Optional, Tuple
from fastapi import UploadFile
from models import (
    BillEntry, SupportingDocument, ValidationResult, 
    MatchStatus, ValidationSummary, ValidationResponse
)
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BillValidator:
    """Advanced bill validator with color-coded results"""
    
    def __init__(self):
        self.ai_service_url = os.getenv('AI_SERVICE_URL', 'http://localhost:8001')
        self.timeout = aiohttp.ClientTimeout(total=300)
        self.amount_tolerance = 0.05  # 5% tolerance for amount matching
        logger.info("Bill Validator initialized with color-coded validation")
    
    async def extract_bill_entries(self, file: UploadFile) -> List[BillEntry]:
        """
        Extract bill entries from PDF or image table and convert to structured JSON
        """
        logger.info(f"🔍 Extracting bill entries from {file.filename}")
        start_time = time.time()
        
        prompt = """
        Extract all bill entries from this medical bill PDF table. The table contains medical expense entries with the following columns:
        
        - SI No (Serial Number)
        - Bill/Cash Memo
        - Bill Date (in MM/DD/YY format)
        - Classification (e.g., HOSPITAL CONSULTATION, MEDICINES, PATHOLOGICAL TEST)
        - Type Of Treatment (e.g., Allopathic)
        - Account Code (e.g., 550)
        - Description (e.g., MEDICAL REIMBURSEMENT SPECIAL DESEASES)
        - Amount (numerical value only)
        - Med Pass Amount (numerical value only)
        - Fin Pass Amount Taxable (numerical value only)
        - Fin Pass Non Taxable (numerical value only, may be empty)
        
        Return ONLY a JSON array like this:
        [
            {
                "si_no": 1,
                "bill_cash_memo": "vacs2822451",
                "bill_date": "3/23/24",
                "classification": "HOSPITAL CONSULTATION",
                "type_of_treatment": "Allopathic",
                "account_code": "550",
                "description": "MEDICAL REIMBURSEMENT SPECIAL DESEASES",
                "amount": 500.0,
                "med_pass_amount": 500.0,
                "fin_pass_amount_taxable": 500.0,
                "fin_pass_non_taxable": null
            }
        ]
        
        Important: 
        - Extract exact amounts as numbers (no currency symbols)
        - Preserve the exact format of bill numbers and dates
        - Handle empty fields with null
        - Ensure all numerical values are properly parsed
        """
        
        try:
            # Reset file pointer to beginning
            if hasattr(file, 'seek'):
                await file.seek(0)
            
            # Log file details
            logger.info(f"📁 File details: {file.filename}, type: {file.content_type}")
            logger.info(f"📁 File size: {getattr(file, 'size', 'unknown')}")
            logger.info(f"📁 File headers: {getattr(file, 'headers', 'unknown')}")
            
            # Validate file object
            if not file.filename:
                logger.error("❌ File has no filename")
                raise Exception("File has no filename")
            
            if not file.content_type:
                logger.error("❌ File has no content type")
                raise Exception("File has no content type")
            
            # Read file content
            file_content = await file.read()
            if not file_content:
                logger.error("❌ File is empty")
                return []
            
            logger.info(f"📄 File content length: {len(file_content)} bytes")
            logger.info(f"📄 File content type: {type(file_content)}")
            logger.info(f"📄 File content first 100 bytes: {file_content[:100]}")
            
            # Test AI service connectivity with proper error handling
            try:
                logger.info(f"🔍 Testing AI service connectivity to: {self.ai_service_url}")
                connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=300), 
                    connector=connector
                ) as session:
                    async with session.get(f"{self.ai_service_url}/") as response:
                        logger.info(f"🔍 AI service health check response: {response.status}")
                        if response.status == 200:
                            logger.info(f"✅ AI service health check passed")
                        else:
                            logger.warning(f"⚠️ AI service returned {response.status}")
                            response_text = await response.text()
                            logger.warning(f"⚠️ AI service response: {response_text[:200]}...")
            except asyncio.TimeoutError:
                logger.error("❌ AI service timeout during health check")
                raise Exception("AI service timeout - please check if the service is running")
            except aiohttp.ClientConnectorError as e:
                logger.error(f"❌ Cannot connect to AI service: {e}")
                raise Exception(f"Cannot connect to AI service at {self.ai_service_url}")
            except Exception as e:
                logger.error(f"❌ AI service connectivity test failed: {e}")
                raise Exception(f"AI service error: {e}")
            
            # Prepare form data with proper content type handling
            data = aiohttp.FormData()
            data.add_field('model', 'gemini-2.5-pro')  # Use gemini-2.5-pro as requested
            data.add_field('prompt', prompt)
            
            # Handle file content properly
            content_type = getattr(file, 'content_type', 'application/octet-stream')
            if not content_type or content_type == 'application/octet-stream':
                # Try to infer content type from filename
                if file.filename.lower().endswith('.pdf'):
                    content_type = 'application/pdf'
                elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    content_type = 'image/jpeg'
            
            data.add_field('files', file_content, 
                          filename=file.filename, 
                          content_type=content_type)
            
            logger.info(f"🚀 Sending request to AI service: {self.ai_service_url}/process")
            logger.info(f"📤 Request data: model=gemini-2.5-pro, filename={file.filename}")
            logger.info(f"📤 Form data structure: {type(data)}")
            logger.info(f"📤 Form data fields count: {len(data._fields) if hasattr(data, '_fields') else 'No _fields attribute'}")
            
            # Make API call with proper error handling
            connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=300),  # 2 minutes for large image processing
                connector=connector
            ) as session:
                try:
                    async with session.post(f"{self.ai_service_url}/process", data=data) as response:
                        logger.info(f"📡 AI service response status: {response.status}")
                        
                        if response.status == 200:
                            try:
                                result = await response.json()
                                logger.info(f"📥 AI service response received")
                                logger.info(f"📥 Response keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                                logger.info(f"📥 Full response structure: {result}")
                                
                                extracted_data = self._parse_json_from_response(result)
                                if not extracted_data:
                                    logger.warning("⚠️ No data extracted from response")
                                    logger.warning(f"⚠️ Raw response: {result}")
                                    return []
                                
                                logger.info(f"🔍 Parsed {len(extracted_data)} entries")
                                
                                # Convert to BillEntry objects with validation
                                bill_entries = []
                                for i, item in enumerate(extracted_data):
                                    try:
                                        # Validate required fields
                                        if not self._validate_bill_entry_data(item):
                                            logger.warning(f"⚠️ Skipping invalid entry {i+1}: missing required fields")
                                            continue
                                        
                                        # Clean and convert data types
                                        cleaned_item = self._clean_bill_entry_data(item)
                                        bill_entry = BillEntry(**cleaned_item)
                                        bill_entries.append(bill_entry)
                                        logger.info(f"✅ Created bill entry {i+1}: {bill_entry.bill_cash_memo}")
                                    except Exception as e:
                                        logger.warning(f"⚠️ Skipping invalid bill entry {i+1}: {e}")
                                        continue
                                
                                extraction_time = time.time() - start_time
                                logger.info(f"✅ Extracted {len(bill_entries)} bill entries in {extraction_time:.2f}s")
                                return bill_entries
                                
                            except Exception as e:
                                logger.error(f"❌ Error processing response: {e}")
                                raise Exception(f"Response processing error: {e}")
                        else:
                            error_text = await response.text()
                            logger.error(f"❌ AI service failed: {response.status}")
                            logger.error(f"❌ Error response: {error_text[:200]}...")
                            raise Exception(f"AI service error: {response.status} - {error_text[:100]}")
                            
                except asyncio.TimeoutError:
                    logger.error("❌ Request timeout")
                    raise Exception("Request timeout - file may be too large or service overloaded")
                except aiohttp.ClientError as e:
                    logger.error(f"❌ Client error: {e}")
                    raise Exception(f"Network error: {e}")
                        
        except Exception as e:
            logger.error(f"❌ Error extracting bills: {str(e)}")
            import traceback
            logger.error(f"❌ Full traceback: {traceback.format_exc()}")
            raise Exception(f"Extraction failed: {str(e)}")
    
    def _validate_bill_entry_data(self, item: Dict[str, Any]) -> bool:
        """Validate that bill entry data has required fields"""
        required_fields = ['si_no', 'bill_cash_memo', 'amount']
        for field in required_fields:
            if field not in item or item[field] is None:
                return False
        return True
    
    def _clean_bill_entry_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and convert bill entry data types"""
        cleaned = {}
        
        # Handle each field with proper type conversion
        cleaned['si_no'] = int(item.get('si_no', 0))
        cleaned['bill_cash_memo'] = str(item.get('bill_cash_memo', ''))
        cleaned['bill_date'] = str(item.get('bill_date', ''))
        cleaned['classification'] = str(item.get('classification', ''))
        cleaned['type_of_treatment'] = str(item.get('type_of_treatment', ''))
        cleaned['account_code'] = str(item.get('account_code', ''))
        cleaned['description'] = str(item.get('description', ''))
        
        # Handle numerical fields with proper conversion
        for field in ['amount', 'med_pass_amount', 'fin_pass_amount_taxable', 'fin_pass_non_taxable']:
            value = item.get(field)
            if value is None or value == '' or value == 'null':
                cleaned[field] = None if field == 'fin_pass_non_taxable' else 0.0
            else:
                try:
                    # Remove currency symbols and convert to float
                    if isinstance(value, str):
                        value = value.replace(',', '').replace('$', '').replace('₹', '').strip()
                    cleaned[field] = float(value)
                except (ValueError, TypeError):
                    cleaned[field] = None if field == 'fin_pass_non_taxable' else 0.0
        
        return cleaned
    
    async def process_supporting_documents(self, documents: List[UploadFile]) -> List[SupportingDocument]:
        """
        Process supporting documents to extract bill information
        """
        logger.info(f"📄 Processing {len(documents)} supporting documents")
        start_time = time.time()
        
        if not documents:
            logger.warning("⚠️ No supporting documents provided")
            return []
        
        prompt = """
        Extract bill information from this medical document (prescription/invoice/bill):
        
        - Bill Number/Invoice Number (look for invoice numbers, bill numbers, reference numbers, any alphanumeric codes)
        - Total Amount (numerical value only, look for total, amount, sum, please pay, final amount)
        - Patient Name (if available)
        - Date (if available, in any format - extract exactly as shown)
        - Hospital/Clinic Name (if available)
        
        Return ONLY JSON like this:
        {
            "bill_number": "extracted bill number or null if not found",
            "amount": 1234.56,
            "patient_name": "patient name or null if not found",
            "date": "date or null if not found",
            "hospital_name": "hospital name or null if not found",
            "confidence_score": 0.95,
            "document_type": "bill or prescription or invoice"
        }
        
        Important: 
        - Look carefully for bill numbers in various formats (VACS2822451, 5060834, etc.)
        - Extract amounts from fields like "PLEASE PAY", "TOTAL", "AMOUNT", "SUM"
        - Extract dates exactly as they appear (e.g., "23-03-2024", "3/23/24")
        - Return valid JSON only, no additional text
        """
        
        processed_docs = []
        
        for doc in documents:
            try:
                logger.info(f"Processing {doc.filename}")
                
                # Reset file pointer
                if hasattr(doc, 'seek'):
                    await doc.seek(0)
                
                file_content = await doc.read()
                if not file_content:
                    logger.warning(f"⚠️ {doc.filename} is empty")
                    continue
                
                # Prepare form data
                data = aiohttp.FormData()
                data.add_field('model', 'gemini-2.5-pro')  # Use gemini-2.5-pro as requested
                data.add_field('prompt', prompt)
                
                # Handle content type
                content_type = getattr(doc, 'content_type', 'application/octet-stream')
                if not content_type or content_type == 'application/octet-stream':
                    if doc.filename.lower().endswith('.pdf'):
                        content_type = 'application/pdf'
                    elif doc.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        content_type = 'image/jpeg'
                
                data.add_field('files', file_content, 
                              filename=doc.filename, 
                              content_type=content_type)
                
                # Make API call
                connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
                async with aiohttp.ClientSession(
                    timeout=self.timeout,
                    connector=connector
                ) as session:
                    try:
                        async with session.post(f"{self.ai_service_url}/process", data=data) as response:
                            if response.status == 200:
                                result = await response.json()
                                doc_data = self._parse_json_from_response(result, expect_dict=True)
                                
                                if doc_data:
                                    # Add metadata and create supporting document
                                    doc_data['filename'] = doc.filename
                                    doc_data['extracted_text'] = str(result.get('result', {}).get('raw_response', ''))[:500]
                                    
                                    # Set defaults for missing fields
                                    doc_data.setdefault('confidence_score', 0.9)
                                    doc_data.setdefault('document_type', 'document')
                                    
                                    try:
                                        supporting_doc = SupportingDocument(**doc_data)
                                        processed_docs.append(supporting_doc)
                                        logger.info(f"✅ Processed {doc.filename}")
                                    except Exception as e:
                                        logger.warning(f"⚠️ Invalid document data for {doc.filename}: {e}")
                                else:
                                    logger.warning(f"⚠️ No data extracted from {doc.filename}")
                            else:
                                error_text = await response.text()
                                logger.error(f"❌ Failed to process {doc.filename}: {response.status} - {error_text[:100]}")
                    except asyncio.TimeoutError:
                        logger.error(f"❌ Timeout processing {doc.filename}")
                    except Exception as e:
                        logger.error(f"❌ Error processing {doc.filename}: {e}")
                        
            except Exception as e:
                logger.error(f"❌ Error processing {doc.filename}: {str(e)}")
                continue
        
        processing_time = time.time() - start_time
        logger.info(f"✅ Successfully processed {len(processed_docs)}/{len(documents)} documents in {processing_time:.2f}s")
        return processed_docs
    
    async def validate_bills_with_documents(self, bill_entries: List[BillEntry], 
                                          supporting_docs: List[SupportingDocument]) -> ValidationResponse:
        """
        Validate bills against supporting documents and return color-coded results
        """
        logger.info("🔍 Validating bills against supporting documents")
        start_time = time.time()
        
        if not bill_entries:
            raise ValueError("No bill entries to validate")
        
        validation_results = []
        matched_count = 0
        partial_count = 0
        unmatched_count = 0
        
        for bill_entry in bill_entries:
            try:
                # Try to find matching document
                matched_doc, match_score = self._find_best_matching_document(bill_entry, supporting_docs)
                
                if matched_doc and match_score >= 0.8:  # High confidence match
                    # Check for perfect match vs partial match
                    is_perfect_match = self._is_perfect_match(bill_entry, matched_doc)
                    
                    if is_perfect_match:
                        match_status = MatchStatus.MATCHED
                        color = "green"
                        matched_count += 1
                        notes = "Perfect match with supporting document"
                    else:
                        match_status = MatchStatus.PARTIAL_MATCH
                        color = "orange"  # Changed from red to orange for partial matches
                        partial_count += 1
                        notes = "Partial match - some fields don't match"
                    
                    # Create validation result with proper error handling
                    validation_result = ValidationResult(
                        bill_entry=bill_entry,
                        match_status=match_status,
                        matched_document=matched_doc,
                        color=color,
                        bill_number_match=self._compare_bill_numbers(
                            bill_entry.bill_cash_memo, 
                            matched_doc.bill_number
                        ),
                        amount_match=self._compare_amounts(
                            bill_entry.amount, 
                            matched_doc.amount
                        ),
                        date_match=self._compare_dates(
                            bill_entry.bill_date, 
                            matched_doc.date
                        ),
                        mismatches=self._get_mismatch_details(bill_entry, matched_doc),
                        notes=notes
                    )
                    
                else:
                    # No matching document found
                    match_status = MatchStatus.NOT_MATCHED
                    color = "red"  # Changed to red for unmatched
                    unmatched_count += 1
                    
                    validation_result = ValidationResult(
                        bill_entry=bill_entry,
                        match_status=match_status,
                        matched_document=None,
                        color=color,
                        bill_number_match=False,
                        amount_match=False,
                        date_match=False,
                        mismatches=["No supporting document found"],
                        notes="No supporting document found for this bill"
                    )
                
                validation_results.append(validation_result)
                
            except Exception as e:
                logger.error(f"❌ Error validating bill entry {bill_entry.si_no}: {e}")
                # Create error validation result
                error_result = ValidationResult(
                    bill_entry=bill_entry,
                    match_status=MatchStatus.NOT_MATCHED,
                    matched_document=None,
                    color="red",
                    bill_number_match=False,
                    amount_match=False,
                    date_match=False,
                    mismatches=[f"Validation error: {str(e)}"],
                    notes=f"Error during validation: {str(e)}"
                )
                validation_results.append(error_result)
                unmatched_count += 1
        
        # Create summary
        processing_time = time.time() - start_time
        summary = ValidationSummary(
            total_bills=len(bill_entries),
            matched_bills=matched_count,
            partial_matches=partial_count,
            unmatched_bills=unmatched_count,
            processing_time=processing_time
        )
        
        # Create complete response
        response = ValidationResponse(
            summary=summary,
            bill_entries=bill_entries,
            validation_results=validation_results,
            supporting_documents=supporting_docs
        )
        
        logger.info(f"✅ Validation complete: {matched_count} green, {partial_count} orange, {unmatched_count} red")
        return response
    
    def _find_best_matching_document(self, bill_entry: BillEntry, 
                                   supporting_docs: List[SupportingDocument]) -> Tuple[Optional[SupportingDocument], float]:
        """Find the best matching supporting document for a bill entry"""
        if not supporting_docs:
            return None, 0.0
        
        best_match = None
        best_score = 0.0
        
        for doc in supporting_docs:
            try:
                # Skip documents without bill numbers
                if not doc.bill_number:
                    continue
                
                # Calculate match score based on multiple criteria
                bill_number_score = self._calculate_bill_number_similarity(
                    bill_entry.bill_cash_memo, 
                    doc.bill_number
                )
                amount_score = self._calculate_amount_similarity(
                    bill_entry.amount, 
                    doc.amount
                )
                date_score = self._calculate_date_similarity(
                    bill_entry.bill_date, 
                    doc.date
                )
                
                # Weighted average score (prioritize bill number matching)
                total_score = (bill_number_score * 0.6 + amount_score * 0.3 + date_score * 0.1)
                
                if total_score > best_score:
                    best_score = total_score
                    best_match = doc
                    
            except Exception as e:
                logger.warning(f"⚠️ Error matching document {doc.filename}: {e}")
                continue
        
        return best_match, best_score
    
    def _is_perfect_match(self, bill_entry: BillEntry, supporting_doc: SupportingDocument) -> bool:
        """Check if bill entry perfectly matches supporting document"""
        try:
            bill_number_match = self._compare_bill_numbers(
                bill_entry.bill_cash_memo, 
                supporting_doc.bill_number
            )
            
            # For perfect match, use stricter amount comparison (1% tolerance instead of 5%)
            if supporting_doc.amount is None:
                amount_match = False
            else:
                difference = abs(bill_entry.amount - supporting_doc.amount)
                strict_tolerance = max(bill_entry.amount * 0.01, 1.0)  # At least 1 rupee tolerance
                amount_match = difference <= strict_tolerance
            
            return bill_number_match and amount_match
            
        except Exception as e:
            logger.warning(f"⚠️ Error checking perfect match: {e}")
            return False
    
    def _compare_bill_numbers(self, bill_number1: str, bill_number2: Optional[str]) -> bool:
        """Compare bill numbers for exact or fuzzy match with improved logic"""
        if not bill_number2:
            return False
        
        try:
            # Normalize bill numbers
            norm1 = self._normalize_bill_number(bill_number1)
            norm2 = self._normalize_bill_number(bill_number2)
            
            if not norm1 or not norm2:
                return False
            
            # Exact match
            if norm1 == norm2:
                return True
            
            # Fuzzy match (one contains the other, minimum length 3)
            if len(norm1) >= 3 and len(norm2) >= 3:
                if norm1 in norm2 or norm2 in norm1:
                    return True
            
            # Handle common variations (e.g., "VACS2822451" vs "vacs2822451")
            if norm1.lower() == norm2.lower():
                return True
            
            # Handle cases where one might have extra characters
            if len(norm1) > 5 and len(norm2) > 5:
                # Check if they share a significant portion
                common_length = min(len(norm1), len(norm2))
                if common_length >= 5:
                    if norm1[:common_length] == norm2[:common_length]:
                        return True
            
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Error comparing bill numbers: {e}")
            return False
    
    def _compare_amounts(self, amount1: float, amount2: Optional[float]) -> bool:
        """Compare amounts with tolerance and improved logic"""
        if amount2 is None:
            return False
        
        try:
            difference = abs(amount1 - amount2)
            tolerance = max(amount1 * self.amount_tolerance, 1.0)  # At least 1 rupee tolerance
            
            # Exact match
            if difference == 0:
                return True
            
            # Within tolerance
            if difference <= tolerance:
                return True
            
            # Handle rounding differences (e.g., 1970.0 vs 1970.44)
            if difference <= 1.0:
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Error comparing amounts: {e}")
            return False
    
    def _compare_dates(self, date1: str, date2: Optional[str]) -> bool:
        """Compare dates for similarity with flexible format handling"""
        if not date2:
            return False
        
        try:
            # Normalize dates for comparison
            norm1 = self._normalize_date(date1)
            norm2 = self._normalize_date(date2)
            
            if not norm1 or not norm2:
                return False
            
            # Exact match after normalization
            if norm1 == norm2:
                return True
            
            # Check if dates are within reasonable range (same month/year)
            if self._dates_are_similar(norm1, norm2):
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Error comparing dates: {e}")
            return False
    
    def _normalize_date(self, date_str: str) -> Optional[str]:
        """Normalize date string to a standard format for comparison"""
        if not date_str:
            return None
        
        try:
            # Remove common separators and normalize
            date_str = str(date_str).strip().lower()
            
            # Handle common date formats
            if '/' in date_str:
                # Format: MM/DD/YY or MM/DD/YYYY
                parts = date_str.split('/')
                if len(parts) == 3:
                    month, day, year = parts
                    # Normalize year to 4 digits
                    if len(year) == 2:
                        year = '20' + year if int(year) < 50 else '19' + year
                    return f"{month.zfill(2)}/{day.zfill(2)}/{year}"
            
            elif '-' in date_str:
                # Format: DD-MM-YYYY or MM-DD-YYYY
                parts = date_str.split('-')
                if len(parts) == 3:
                    # Assume DD-MM-YYYY format (common in Indian documents)
                    day, month, year = parts
                    return f"{month.zfill(2)}/{day.zfill(2)}/{year}"
            
            return date_str
            
        except Exception as e:
            logger.warning(f"⚠️ Error normalizing date '{date_str}': {e}")
            return date_str
    
    def _dates_are_similar(self, date1: str, date2: str) -> bool:
        """Check if two dates are similar (same month/year)"""
        try:
            # Simple check: if both dates contain the same month and year
            # This handles cases like "3/23/24" vs "23/03/2024"
            if '/' in date1 and '/' in date2:
                parts1 = date1.split('/')
                parts2 = date2.split('/')
                
                if len(parts1) >= 2 and len(parts2) >= 2:
                    # Check if month and year are the same (allowing for different day)
                    month1, year1 = parts1[0], parts1[-1]
                    month2, year2 = parts2[0], parts2[-1]
                    
                    # Normalize years
                    if len(year1) == 2:
                        year1 = '20' + year1 if int(year1) < 50 else '19' + year1
                    if len(year2) == 2:
                        year2 = '20' + year2 if int(year2) < 50 else '19' + year2
                    
                    return month1 == month2 and year1 == year2
            
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Error checking date similarity: {e}")
            return False
    
    def _get_mismatch_details(self, bill_entry: BillEntry, supporting_doc: SupportingDocument) -> List[str]:
        """Get detailed list of mismatches between bill and document"""
        mismatches = []
        
        try:
            if not self._compare_bill_numbers(bill_entry.bill_cash_memo, supporting_doc.bill_number):
                mismatches.append(f"Bill number: '{bill_entry.bill_cash_memo}' ≠ '{supporting_doc.bill_number}'")
            
            if not self._compare_amounts(bill_entry.amount, supporting_doc.amount):
                mismatches.append(f"Amount: ₹{bill_entry.amount} ≠ ₹{supporting_doc.amount}")
            
            if not self._compare_dates(bill_entry.bill_date, supporting_doc.date):
                mismatches.append(f"Date: '{bill_entry.bill_date}' ≠ '{supporting_doc.date}'")
            
            return mismatches
            
        except Exception as e:
            logger.warning(f"⚠️ Error getting mismatch details: {e}")
            return [f"Error comparing fields: {str(e)}"]
    
    def _calculate_bill_number_similarity(self, bill_number1: str, bill_number2: str) -> float:
        """Calculate similarity score between two bill numbers"""
        if not bill_number2:
            return 0.0
        
        try:
            norm1 = self._normalize_bill_number(bill_number1)
            norm2 = self._normalize_bill_number(bill_number2)
            
            if not norm1 or not norm2:
                return 0.0
            
            if norm1 == norm2:
                return 1.0
            
            if norm1 in norm2 or norm2 in norm1:
                return 0.8
            
            # Calculate Levenshtein distance similarity
            distance = self._levenshtein_distance(norm1, norm2)
            max_len = max(len(norm1), len(norm2))
            
            if max_len == 0:
                return 0.0
            
            similarity = 1.0 - (distance / max_len)
            return max(0.0, similarity)
            
        except Exception as e:
            logger.warning(f"⚠️ Error calculating bill number similarity: {e}")
            return 0.0
    
    def _calculate_amount_similarity(self, amount1: float, amount2: Optional[float]) -> float:
        """Calculate similarity score between two amounts"""
        if amount2 is None:
            return 0.0
        
        try:
            difference = abs(amount1 - amount2)
            tolerance = max(amount1 * self.amount_tolerance, 1.0)
            
            if difference <= tolerance:
                return 1.0
            
            # Linear decrease based on difference
            max_difference = amount1 * 0.5  # 50% difference
            if difference >= max_difference:
                return 0.0
            
            similarity = 1.0 - (difference / max_difference)
            return max(0.0, similarity)
            
        except Exception as e:
            logger.warning(f"⚠️ Error calculating amount similarity: {e}")
            return 0.0
    
    def _calculate_date_similarity(self, date1: str, date2: Optional[str]) -> float:
        """Calculate similarity score between two dates"""
        if not date2:
            return 0.0
        
        try:
            if date1.lower().strip() == date2.lower().strip():
                return 1.0
            
            return 0.5  # Partial credit for different dates
            
        except Exception as e:
            logger.warning(f"⚠️ Error calculating date similarity: {e}")
            return 0.0
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        try:
            previous_row = list(range(len(s2) + 1))
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            
            return previous_row[-1]
            
        except Exception as e:
            logger.warning(f"⚠️ Error calculating Levenshtein distance: {e}")
            return max(len(s1), len(s2))  # Return max length on error
    
    def _normalize_bill_number(self, bill_number: str) -> str:
        """Normalize bill number for comparison"""
        if not bill_number:
            return ""
        
        try:
            # Remove common separators and convert to uppercase
            normalized = str(bill_number).upper()
            normalized = normalized.replace(" ", "").replace("-", "").replace("_", "").replace("/", "")
            return normalized.strip()
            
        except Exception as e:
            logger.warning(f"⚠️ Error normalizing bill number '{bill_number}': {e}")
            return str(bill_number).upper()
    
    def _parse_json_from_response(self, ai_response: Dict[str, Any], expect_dict: bool = False) -> Any:
        """Parse JSON from AI response with better error handling"""
        try:
            # Get the raw response
            raw_response = ai_response.get('result', {}).get('raw_response', '')
            if not raw_response:
                logger.warning("⚠️ No raw response from AI service")
                return [] if not expect_dict else {}
            
            logger.info(f"🔍 Parsing response: {raw_response[:200]}...")
            
            # Clean the response - remove markdown formatting
            cleaned_response = raw_response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            
            cleaned_response = cleaned_response.strip()
            
            # Try to find JSON in the response
            if expect_dict:
                # Look for object
                json_start = cleaned_response.find('{')
                json_end = cleaned_response.rfind('}') + 1
            else:
                # Look for array
                json_start = cleaned_response.find('[')
                json_end = cleaned_response.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = cleaned_response[json_start:json_end]
                logger.info(f"🔍 Extracted JSON: {json_str[:100]}...")
                
                try:
                    parsed_data = json.loads(json_str)
                    logger.info(f"✅ Successfully parsed JSON")
                    return parsed_data
                except json.JSONDecodeError as e:
                    logger.error(f"❌ JSON decode error: {e}")
                    logger.error(f"❌ Failed JSON: {json_str[:200]}...")
            
            # Fallback: try to parse the entire cleaned response
            try:
                parsed_data = json.loads(cleaned_response)
                logger.info(f"✅ Successfully parsed entire response as JSON")
                return parsed_data
            except json.JSONDecodeError:
                logger.error(f"❌ Could not parse response as JSON")
                logger.error(f"❌ Response: {cleaned_response[:200]}...")
            
            return [] if not expect_dict else {}
            
        except Exception as e:
            logger.error(f"❌ Error parsing JSON response: {e}")
            logger.error(f"❌ Raw response: {str(ai_response)[:200]}...")
            return [] if not expect_dict else {}
    
    async def complete_validation_workflow(self, bill_file: UploadFile, 
                                         supporting_docs: List[UploadFile]) -> ValidationResponse:
        """
        Complete workflow: Extract → Process → Validate with color-coded results
        """
        logger.info("🚀 Starting complete bill validation workflow with color coding")
        
        try:
            # Step 1: Extract bill entries
            logger.info("📋 Step 1: Extracting bill entries...")
            bill_entries = await self.extract_bill_entries(bill_file)
            
            if not bill_entries:
                raise ValueError('No bill entries found in file - please check file format and content')
            
            logger.info(f"✅ Found {len(bill_entries)} bill entries")
            
            # Step 2: Process supporting documents
            logger.info("📄 Step 2: Processing supporting documents...")
            processed_docs = await self.process_supporting_documents(supporting_docs)
            
            logger.info(f"✅ Processed {len(processed_docs)} supporting documents")
            
            # Step 3: Validate and get color-coded results
            logger.info("🔍 Step 3: Validating bills against documents...")
            validation_response = await self.validate_bills_with_documents(bill_entries, processed_docs)
            
            logger.info("✅ Validation workflow completed successfully")
            return validation_response
            
        except Exception as e:
            logger.error(f"❌ Validation workflow failed: {e}")
            raise Exception(f"Validation workflow error: {str(e)}")

# Additional helper functions for better error handling and debugging

def create_sample_response_on_error(bill_entries: List[BillEntry]) -> ValidationResponse:
    """Create a sample response when validation fails"""
    validation_results = []
    
    for entry in bill_entries:
        result = ValidationResult(
            bill_entry=entry,
            match_status=MatchStatus.NOT_MATCHED,
            matched_document=None,
            color="red",
            bill_number_match=False,
            amount_match=False,
            date_match=False,
            mismatches=["Validation service unavailable"],
            notes="System error during validation"
        )
        validation_results.append(result)
    
    summary = ValidationSummary(
        total_bills=len(bill_entries),
        matched_bills=0,
        partial_matches=0,
        unmatched_bills=len(bill_entries),
        processing_time=0.0
    )
    
    return ValidationResponse(
        summary=summary,
        bill_entries=bill_entries,
        validation_results=validation_results,
        supporting_documents=[]
    )

def validate_environment() -> Dict[str, Any]:
    """Validate environment setup and return status"""
    status = {
        "ai_service_url": os.getenv('AI_SERVICE_URL', 'http://localhost:8001'),
        "environment_loaded": True,
        "required_modules": [],
        "missing_modules": []
    }
    
    # Check required modules
    required_modules = ['aiohttp', 'fastapi', 'pydantic', 'python-dotenv']
    
    for module in required_modules:
        try:
            __import__(module.replace('-', '_'))
            status["required_modules"].append(module)
        except ImportError:
            status["missing_modules"].append(module)
    
    return status

# Usage example:
"""
# Initialize the validator
validator = BillValidator()

# Validate environment
env_status = validate_environment()
if env_status["missing_modules"]:
    print(f"Missing modules: {env_status['missing_modules']}")

# Note: Using gemini-2.5-pro model as requested
# Make sure your AI service supports this model

# Run the validation workflow
try:
    result = await validator.complete_validation_workflow(bill_file, supporting_docs)
    
    # Process results
    print(f"Validation Summary:")
    print(f"Total bills: {result.summary.total_bills}")
    print(f"Matched (Green): {result.summary.matched_bills}")
    print(f"Partial (Orange): {result.summary.partial_matches}")
    print(f"Unmatched (Red): {result.summary.unmatched_bills}")
    
    # Color-coded results
    for validation_result in result.validation_results:
        color_emoji = {"green": "🟢", "orange": "🟠", "red": "🔴"}.get(validation_result.color, "⚪")
        print(f"{color_emoji} {validation_result.bill_entry.bill_cash_memo}: {validation_result.notes}")
        
except Exception as e:
    print(f"Validation failed: {e}")
    # Use fallback response
    fallback_response = create_sample_response_on_error(bill_entries)
"""