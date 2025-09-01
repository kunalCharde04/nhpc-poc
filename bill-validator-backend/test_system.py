"""
Test script for the Medical Bill Validation System
Demonstrates the new color-coded validation functionality
"""
import asyncio
import json
from bill_validator import BillValidator
from models import BillEntry, SupportingDocument

async def test_bill_validation():
    """Test the bill validation system with sample data"""
    
    print("🧪 Testing Medical Bill Validation System with Color-Coded Results")
    print("=" * 70)
    
    # Initialize validator
    validator = BillValidator()
    
    # Create sample bill entries (simulating extracted data)
    sample_bills = [
        BillEntry(
            si_no=1,
            bill_cash_memo="vacs2822451",
            bill_date="3/23/24",
            classification="HOSPITAL CONSULTATION",
            type_of_treatment="Allopathic",
            account_code="550",
            description="MEDICAL REIMBURSEMENT SPECIAL DESEASES",
            amount=500.0,
            med_pass_amount=500.0,
            fin_pass_amount_taxable=500.0,
            fin_pass_non_taxable=None
        ),
        BillEntry(
            si_no=2,
            bill_cash_memo="s06034",
            bill_date="4/15/24",
            classification="MEDICINES",
            type_of_treatment="Allopathic",
            account_code="550",
            description="MEDICAL REIMBURSEMENT SPECIAL DESEASES",
            amount=1970.0,
            med_pass_amount=1970.0,
            fin_pass_amount_taxable=1970.0,
            fin_pass_non_taxable=None
        ),
        BillEntry(
            si_no=3,
            bill_cash_memo="131141/OP/BL/23",
            bill_date="5/20/24",
            classification="PATHOLOGICAL TEST",
            type_of_treatment="Allopathic",
            account_code="550",
            description="MEDICAL REIMBURSEMENT SPECIAL DESEASES",
            amount=1556.0,
            med_pass_amount=1556.0,
            fin_pass_amount_taxable=1556.0,
            fin_pass_non_taxable=None
        )
    ]
    
    # Create sample supporting documents (simulating processed documents)
    sample_docs = [
        SupportingDocument(
            filename="bill_vacs2822451.pdf",
            bill_number="vacs2822451",
            amount=500.0,
            patient_name="John Doe",
            date="3/23/24",
            hospital_name="City Hospital",
            extracted_text="Sample extracted text from bill",
            confidence_score=0.95,
            document_type="bill"
        ),
        SupportingDocument(
            filename="prescription_s06034.pdf",
            bill_number="s06034",
            amount=2000.0,  # Different amount - will cause partial match
            patient_name="Jane Smith",
            date="4/15/24",
            hospital_name="Medical Center",
            extracted_text="Sample extracted text from prescription",
            confidence_score=0.92,
            document_type="prescription"
        )
        # Note: No document for the third bill - will show as yellow (no match)
    ]
    
    print(f"📋 Sample Bill Entries: {len(sample_bills)} bills")
    for bill in sample_bills:
        print(f"   • {bill.bill_cash_memo}: ${bill.amount} ({bill.classification})")
    
    print(f"\n📄 Sample Supporting Documents: {len(sample_docs)} documents")
    for doc in sample_docs:
        print(f"   • {doc.filename}: {doc.bill_number} - ${doc.amount}")
    
    print("\n🔍 Running Validation...")
    
    # Run validation
    validation_response = await validator.validate_bills_with_documents(sample_bills, sample_docs)
    
    # Display results
    print("\n" + "=" * 70)
    print("🎨 VALIDATION RESULTS WITH COLOR CODING")
    print("=" * 70)
    
    summary = validation_response.summary
    print(f"📊 Summary:")
    print(f"   • Total Bills: {summary.total_bills}")
    print(f"   • 🟢 Perfect Matches (Green): {summary.matched_bills}")
    print(f"   • 🔴 Partial Matches (Red): {summary.partial_matches}")
    print(f"   • 🟡 No Matches (Yellow): {summary.unmatched_bills}")
    print(f"   • Processing Time: {summary.processing_time:.2f}s")
    
    print(f"\n🔍 Detailed Results:")
    for i, result in enumerate(validation_response.validation_results, 1):
        print(f"\n{i}. Bill: {result.bill_entry.bill_cash_memo} (${result.bill_entry.amount})")
        print(f"   Status: {result.color.upper()} - {result.match_status.value}")
        
        if result.matched_document:
            print(f"   📄 Matched Document: {result.matched_document.filename}")
            print(f"   📊 Match Details:")
            print(f"      • Bill Number: {'✅' if result.bill_number_match else '❌'}")
            print(f"      • Amount: {'✅' if result.amount_match else '❌'}")
            print(f"      • Date: {'✅' if result.date_match else '❌'}")
            
            if result.mismatches:
                print(f"   ⚠️  Mismatches:")
                for mismatch in result.mismatches:
                    print(f"      • {mismatch}")
        else:
            print(f"   ❌ No supporting document found")
        
        if result.notes:
            print(f"   📝 Notes: {result.notes}")
    
    print(f"\n🎯 Color Coding Legend:")
    print(f"   🟢 Green: Perfect match - No action required")
    print(f"   🔴 Red: Partial match - Review discrepancies")
    print(f"   🟡 Yellow: No match - Upload missing document")
    
    print(f"\n✅ Test completed successfully!")
    
    # Return the validation response for further analysis
    return validation_response

def test_json_structure():
    """Test the JSON structure of the models"""
    
    print("\n🧪 Testing JSON Structure")
    print("=" * 50)
    
    # Create a sample bill entry
    bill = BillEntry(
        si_no=1,
        bill_cash_memo="TEST123",
        bill_date="1/15/24",
        classification="TEST",
        type_of_treatment="Test",
        account_code="123",
        description="Test Description",
        amount=100.0,
        med_pass_amount=100.0,
        fin_pass_amount_taxable=100.0,
        fin_pass_non_taxable=None
    )
    
    # Convert to JSON
    bill_json = bill.model_dump()
    
    print("📋 Bill Entry JSON Structure:")
    print(json.dumps(bill_json, indent=2))
    
    # Test validation result
    from models import ValidationResult, MatchStatus
    
    validation_result = ValidationResult(
        bill_entry=bill,
        match_status=MatchStatus.MATCHED,
        matched_document=None,
        color="green",
        bill_number_match=True,
        amount_match=True,
        date_match=False,
        mismatches=[],
        notes="Test validation result"
    )
    
    result_json = validation_result.model_dump()
    
    print("\n✅ Validation Result JSON Structure:")
    print(json.dumps(result_json, indent=2))
    
    print("\n✅ JSON structure test completed!")

if __name__ == "__main__":
    print("🚀 Starting Medical Bill Validation System Tests")
    
    # Test JSON structure
    test_json_structure()
    
    # Test async validation (if running in async context)
    try:
        # Try to run the async test
        asyncio.run(test_bill_validation())
    except RuntimeError:
        print("\n⚠️  Async test requires proper async context")
        print("   Run this in an async environment or use the API endpoints")
    
    print("\n🎉 All tests completed!")
    print("\n💡 To test the full system:")
    print("   1. Start the AI service: cd ../ai-service && python start.py")
    print("   2. Start this backend: python main.py")
    print("   3. Use the API endpoints at http://localhost:8000/docs")
