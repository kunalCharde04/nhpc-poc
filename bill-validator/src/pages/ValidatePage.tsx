import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, FileText, Eye, EyeOff } from 'lucide-react'
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

interface ExtractionWithDocumentsResponse {
  message: string;
  bill_entries: BillEntry[];
  bill_entries_count: number;
  extraction_time: number;
  processed_documents: SupportingDocument[];
  documents_count: number;
  documents_processing_time: number;
}

const ValidatePage = () => {
  const [validationResults, setValidationResults] = useState<ValidationResponse | null>(null)
  const [extractedEntries, setExtractedEntries] = useState<ExtractionWithDocumentsResponse | null>(null)
  const [billEntriesFile, setBillEntriesFile] = useState<File | null>(null)
  const [supportingDocs, setSupportingDocs] = useState<File[]>([])
  const [currentStep, setCurrentStep] = useState<'upload' | 'preview' | 'results'>('upload')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showDocs, setShowDocs] = useState(true)

  const handleInitialUpload = async (billEntriesPdf: File, supportingDocuments: File[]) => {
    setIsLoading(true)
    setError(null)
    setBillEntriesFile(billEntriesPdf)
    setSupportingDocs(supportingDocuments)

    try {
      // First extract bill entries and (optionally) process supporting docs in one call
      const formData = new FormData()
      formData.append('bill_entries_file', billEntriesPdf)
      for (const doc of supportingDocuments) {
        formData.append('supporting_documents', doc)
      }
      
      // Log what we're sending for debugging
      console.log('File being sent:', billEntriesPdf)
      console.log('File name:', billEntriesPdf.name)
      console.log('File type:', billEntriesPdf.type)
      console.log('File size:', billEntriesPdf.size)
      console.log('FormData entries:', Array.from(formData.entries()))

      const token = localStorage.getItem('auth_token')
      const response = await fetch('/api/extract-bills', {
        method: 'POST',
        body: formData,
        headers: token ? { 'Authorization': `Bearer ${token}` } : undefined,
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
    if (!extractedEntries) return

    setIsLoading(true)
    setError(null)

    try {
      // New JSON-only validation flow: send preprocessed arrays
      const payload = {
        bill_entries: extractedEntries.bill_entries,
        processed_documents: extractedEntries.processed_documents,
      }

      const token = localStorage.getItem('auth_token')
      const response = await fetch('/api/validate-bills', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(token ? { 'Authorization': `Bearer ${token}` } : {}) },
        body: JSON.stringify(payload),
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
          <>
            <BillEntriesPreview
              entries={extractedEntries.bill_entries}
              count={extractedEntries.bill_entries_count}
              extractionMethod="AI-powered extraction"
              onProceedToValidation={handleProceedToValidation}
              isLoading={isLoading}
            />

            {/* Supporting Documents Preview */}
            <div className="max-w-6xl mx-auto space-y-6 mt-6">
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <FileText className="h-6 w-6 text-emerald-600" />
                    <h2 className="text-xl font-semibold text-gray-900">Extracted Supporting Documents</h2>
                    <span className="px-3 py-1 rounded-full text-sm font-medium bg-emerald-50 text-emerald-800">
                      {extractedEntries.documents_count} found
                    </span>
                  </div>
                  <button
                    onClick={() => setShowDocs(!showDocs)}
                    className="inline-flex items-center px-3 py-1 text-gray-600 hover:text-gray-900 transition-colors"
                  >
                    {showDocs ? (<><EyeOff className="h-4 w-4 mr-2" />Hide</>) : (<><Eye className="h-4 w-4 mr-2" />Show</>)}
                  </button>
                </div>

                {showDocs && (
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Bill Number</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Hospital</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Confidence</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Filename</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {extractedEntries.processed_documents.map((doc, idx) => (
                          <tr key={idx} className="hover:bg-gray-50">
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">{doc.bill_number || '-'}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{doc.amount !== undefined ? `₹${doc.amount.toLocaleString()}` : '-'}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{doc.date || '-'}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{doc.hospital_name || '-'}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{doc.confidence_score !== undefined ? (doc.confidence_score * 100).toFixed(0) + '%' : '-'}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{doc.filename}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          </>
        )}

        {/* Step 3: Validation Results */}
        {currentStep === 'results' && validationResults && (
          <ValidationResults 
            results={validationResults}
            onReset={handleReset}
            onBackToPreview={() => setCurrentStep('preview')}
          />
        )}
      </main>
    </div>
  )
}

export default ValidatePage
