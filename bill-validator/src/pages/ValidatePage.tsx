import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import FileUploader from '../components/FileUploader'
import ValidationResults from '../components/ValidationResults'
import BillEntriesPreview from '../components/BillEntriesPreview'

// Updated interfaces to match the new backend API
interface BillEntry {
  si_no: number;
  bill_cash_memo: string;
  bill_date: string;
  classification: string;
  type_of_treatment: string;
  account_code: string;
  description: string;
  amount: number;
  med_pass_amount: number;
  fin_pass_amount_taxable: number;
  fin_pass_non_taxable?: number;
}

interface SupportingDocument {
  filename: string;
  bill_number?: string;
  amount?: number;
  patient_name?: string;
  date?: string;
  hospital_name?: string;
  extracted_text: string;
  confidence_score?: number;
  document_type?: string;
}

interface ValidationResult {
  bill_entry: BillEntry;
  match_status: 'matched' | 'partial' | 'not_matched';
  matched_document?: SupportingDocument;
  color: 'green' | 'red' | 'yellow';
  bill_number_match: boolean;
  amount_match: boolean;
  date_match: boolean;
  mismatches: string[];
  notes?: string;
}

interface ValidationSummary {
  total_bills: number;
  matched_bills: number;
  partial_matches: number;
  unmatched_bills: number;
  processing_time: number;
  timestamp: string;
}

interface ValidationResponse {
  summary: ValidationSummary;
  bill_entries: BillEntry[];
  validation_results: ValidationResult[];
  supporting_documents: SupportingDocument[];
  color_legend: {
    green: string;
    red: string;
    yellow: string;
  };
}

interface BillExtractionResponse {
  message: string;
  bill_entries: BillEntry[];
  count: number;
  extraction_time: number;
}

const ValidatePage = () => {
  const [validationResults, setValidationResults] = useState<ValidationResponse | null>(null)
  const [extractedEntries, setExtractedEntries] = useState<BillExtractionResponse | null>(null)
  const [billEntriesFile, setBillEntriesFile] = useState<File | null>(null)
  const [supportingDocs, setSupportingDocs] = useState<File[]>([])
  const [currentStep, setCurrentStep] = useState<'upload' | 'preview' | 'results'>('upload')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleInitialUpload = async (billEntriesPdf: File, supportingDocuments: File[]) => {
    setIsLoading(true)
    setError(null)
    setBillEntriesFile(billEntriesPdf)
    setSupportingDocs(supportingDocuments)

    try {
      // First extract bill entries for preview using the new endpoint
      const formData = new FormData()
      formData.append('bill_entries_file', billEntriesPdf)
      
      // Log what we're sending for debugging
      console.log('File being sent:', billEntriesPdf)
      console.log('File name:', billEntriesPdf.name)
      console.log('File type:', billEntriesPdf.type)
      console.log('File size:', billEntriesPdf.size)
      console.log('FormData entries:', Array.from(formData.entries()))

      const response = await fetch('http://localhost:8000/extract-bills', {
        method: 'POST',
        body: formData,
      })  

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Bill extraction failed')
      }

      const extractionResult = await response.json()
      setExtractedEntries(extractionResult)
      setCurrentStep('preview')
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An unknown error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  const handleProceedToValidation = async () => {
    if (!extractedEntries || !billEntriesFile || supportingDocs.length === 0) return

    setIsLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      
      // Include the original bill entries file 
      formData.append('bill_entries_file', billEntriesFile)
      
      // Include all supporting documents
      for (const doc of supportingDocs) {
        formData.append('supporting_documents', doc)
      }

      const response = await fetch('http://localhost:8000/validate-bills', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Validation failed')
      }

      const results = await response.json()
      setValidationResults(results)
      setCurrentStep('results')
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An unknown error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setValidationResults(null)
    setExtractedEntries(null)
    setBillEntriesFile(null)
    setSupportingDocs([])
    setCurrentStep('upload')
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center space-x-4">
            <Link 
              to="/" 
              className="inline-flex items-center text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeft className="h-5 w-5 mr-2" />
              Back to Home
            </Link>
            <div className="h-6 w-px bg-gray-300"></div>
            <h1 className="text-2xl font-bold text-gray-900">Bill Validation</h1>
          </div>
        </div>
      </div>
      
      <main className="container mx-auto px-4 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <div className="text-red-800">
                <h3 className="font-medium">Validation Error</h3>
                <p className="text-sm mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Step 1: Upload Documents */}
        {currentStep === 'upload' && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">Upload Your Documents</h2>
                <p className="text-lg text-gray-600">
                  Upload your bill entries (PDF or image) and supporting documents for validation
                </p>
              </div>
              
              <FileUploader 
                onValidate={handleInitialUpload}
                isLoading={isLoading}
              />
            </div>
            
            {/* Instructions Card */}
            <div className="bg-blue-50 rounded-xl p-6 border border-blue-200">
              <h3 className="text-lg font-semibold text-blue-900 mb-3">Instructions:</h3>
              <ul className="space-y-2 text-blue-800">
                <li className="flex items-start">
                  <span className="flex-shrink-0 w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3"></span>
                  Upload a PDF or image containing your bill entries with bill numbers and amounts
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3"></span>
                  Upload supporting documents (PDFs, images) that contain the actual bills
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3"></span>
                  Our AI will extract and cross-reference the data for validation
                </li>
              </ul>
            </div>
          </div>
        )}

        {/* Step 2: Preview Extracted Entries */}
        {currentStep === 'preview' && extractedEntries && (
          <BillEntriesPreview
            entries={extractedEntries.bill_entries}
            count={extractedEntries.count}
            extractionMethod="AI-powered extraction"
            onProceedToValidation={handleProceedToValidation}
            isLoading={isLoading}
          />
        )}

        {/* Step 3: Validation Results */}
        {currentStep === 'results' && validationResults && (
          <ValidationResults 
            results={validationResults}
            onReset={handleReset}
          />
        )}
      </main>
    </div>
  )
}

export default ValidatePage
