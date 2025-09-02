"""
Pydantic models for Medical Bill Validation System with Color-Coded Results
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MatchStatus(str, Enum):
    """Status of bill matching with supporting documents"""
    MATCHED = "matched"           # Green - Perfect match
    PARTIAL_MATCH = "partial"     # Red - Partial match (some fields don't match)
    NOT_MATCHED = "not_matched"   # Yellow - No supporting document found

class BillEntry(BaseModel):
    """Model for bill entry from the main PDF table"""
    si_no: int = Field(..., description="Serial number from the table")
    bill_cash_memo: str = Field(..., description="Bill/Cash Memo number")
    bill_date: str = Field(..., description="Bill date in MM/DD/YY format")
    classification: str = Field(..., description="Medical expense classification")
    type_of_treatment: str = Field(..., description="Type of treatment (e.g., Allopathic)")
    account_code: str = Field(..., description="Account code (e.g., 550)")
    description: str = Field(..., description="Description of the medical expense")
    amount: float = Field(..., description="Original bill amount")
    med_pass_amount: float = Field(..., description="Medical passed amount")
    fin_pass_amount_taxable: float = Field(..., description="Financial passed amount (taxable)")
    fin_pass_non_taxable: Optional[float] = Field(None, description="Financial passed amount (non-taxable)")

class SupportingDocument(BaseModel):
    """Model for supporting document data extracted via AI"""
    filename: str = Field(..., description="Original filename")
    bill_number: Optional[str] = Field(None, description="Bill number extracted from document")
    amount: Optional[float] = Field(None, description="Amount extracted from document")
    patient_name: Optional[str] = Field(None, description="Patient name if available")
    date: Optional[str] = Field(None, description="Date if available")
    hospital_name: Optional[str] = Field(None, description="Hospital/clinic name if available")
    extracted_text: str = Field(..., description="Full OCR extracted text")
    confidence_score: Optional[float] = Field(None, description="OCR confidence score")
    document_type: Optional[str] = Field(None, description="Type of document (bill, prescription, etc.)")

class ValidationResult(BaseModel):
    """Model for individual bill validation result with color coding"""
    bill_entry: BillEntry = Field(..., description="Original bill entry from table")
    match_status: MatchStatus = Field(..., description="Match status for color coding")
    matched_document: Optional[SupportingDocument] = Field(None, description="Matching supporting document if found")
    
    # Color coding information
    color: str = Field(..., description="Color code: green=matched, red=partial, yellow=not_matched")
    
    # Validation details
    bill_number_match: bool = Field(..., description="Whether bill numbers match")
    amount_match: bool = Field(..., description="Whether amounts match (within tolerance)")
    date_match: bool = Field(False, description="Whether dates match (if available)")
    
    # Mismatch details
    mismatches: List[str] = Field(default_factory=list, description="List of mismatch descriptions")
    notes: Optional[str] = Field(None, description="Additional validation notes")

class ValidationSummary(BaseModel):
    """Summary of validation results"""
    total_bills: int = Field(..., description="Total number of bills processed")
    matched_bills: int = Field(..., description="Number of perfectly matched bills (green)")
    partial_matches: int = Field(..., description="Number of partially matched bills (red)")
    unmatched_bills: int = Field(..., description="Number of unmatched bills (yellow)")
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="Validation timestamp")

class ValidationResponse(BaseModel):
    """Complete validation response with color-coded results"""
    summary: ValidationSummary = Field(..., description="Validation summary")
    bill_entries: List[BillEntry] = Field(..., description="All extracted bill entries")
    validation_results: List[ValidationResult] = Field(..., description="Detailed validation results with color coding")
    supporting_documents: List[SupportingDocument] = Field(..., description="Processed supporting documents")
    
    # Color coding legend
    color_legend: Dict[str, str] = Field(
        default_factory=lambda: {
            "green": "Perfect match - Bill and supporting document match completely",
            "red": "Partial match - Some fields don't match or have discrepancies",
            "yellow": "No match - No supporting document found for this bill"
        }
    )

class BillExtractionResponse(BaseModel):
    """Response for bill extraction endpoint"""
    message: str = Field(..., description="Success/error message")
    bill_entries: List[BillEntry] = Field(..., description="Extracted bill entries")
    count: int = Field(..., description="Number of bills extracted")
    extraction_time: float = Field(..., description="Extraction time in seconds")

class DocumentProcessingResponse(BaseModel):
    """Response for document processing endpoint"""
    message: str = Field(..., description="Success/error message")
    processed_documents: List[SupportingDocument] = Field(..., description="Processed supporting documents")
    count: int = Field(..., description="Number of documents processed")
    processing_time: float = Field(..., description="Processing time in seconds")

class ExtractionWithDocumentsResponse(BaseModel):
    """Combined response for initial extraction flow (bill entries + optional supporting docs)."""
    message: str = Field(..., description="Success message")
    bill_entries: List[BillEntry] = Field(..., description="Extracted bill entries")
    bill_entries_count: int = Field(..., description="Number of bills extracted")
    extraction_time: float = Field(..., description="Extraction time in seconds")
    processed_documents: List[SupportingDocument] = Field(default_factory=list, description="Processed supporting documents")
    documents_count: int = Field(0, description="Number of supporting documents processed")
    documents_processing_time: float = Field(0.0, description="Time taken to process supporting documents")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
