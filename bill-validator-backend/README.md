# Simple Medical Bill Validation System

A simplified AI-powered system to validate medical bills against supporting documents.

## What it does

1. **Extract bill entries from PDF** → Shows extracted values to user
2. **Analyze supporting documents** (prescriptions/invoices) → Extract bill information  
3. **Find mismatches** → Tell you mismatched bill numbers and amounts

## Files (Simplified!)

- `main.py` - FastAPI backend with 3 simple endpoints
- `simple_bill_validator.py` - Single file that does everything
- `models.py` - Data models
- `start.py` - Startup script

## API Endpoints

### 1. Extract Bill Entries
```bash
curl -X POST "http://localhost:8000/extract-bill-entries" \
  -F "bill_entries_pdf=@bills.pdf"
```

### 2. Process Supporting Documents  
```bash
curl -X POST "http://localhost:8000/process-documents" \
  -F "supporting_documents=@doc1.pdf" \
  -F "supporting_documents=@doc2.pdf"
```

### 3. Complete Validation (Does Everything)
```bash
curl -X POST "http://localhost:8000/validate-bills" \
  -F "bill_entries_pdf=@bills.pdf" \
  -F "supporting_documents=@doc1.pdf" \
  -F "supporting_documents=@doc2.pdf"
```

## Setup

1. **Start AI Service** (in separate terminal):
```bash
cd ../ai-service
python start.py
```

2. **Start Backend**:
```bash
python start.py
```

## How it works

1. Uses **Gemini 2.0 Pro** model for document analysis
2. Extracts bill numbers, amounts, patient names, dates
3. Compares bills with supporting documents
4. Reports mismatches and missing documents
5. Simple JSON responses - no complex validation objects

## Response Format

```json
{
  "bill_entries": [
    {
      "bill_number": "INV-001",
      "bill_amount": 1500.50,
      "patient_name": "John Doe",
      "date": "2024-01-15",
      "hospital_name": "City Hospital"
    }
  ],
  "supporting_documents": [
    {
      "filename": "receipt1.pdf", 
      "bill_number": "INV-001",
      "amount": 1500.50
    }
  ],
  "analysis": {
    "summary": {
      "total_bills": 1,
      "matched_bills": 1,
      "mismatched_bills": 0,
      "unmatched_bills": 0
    },
    "matched_bills": [...],
    "mismatches": [...],
    "unmatched_bills": [...]
  }
}
```

That's it! Much simpler than before.
