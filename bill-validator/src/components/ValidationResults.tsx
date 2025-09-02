import { CheckCircle2, XCircle, AlertTriangle, FileText, RotateCcw, Download, ArrowLeft } from 'lucide-react'

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

interface ValidationResultsProps {
  results: ValidationResponse;
  onReset: () => void;
  onBackToPreview?: () => void;
}

const ValidationResults = ({ results, onReset, onBackToPreview }: ValidationResultsProps) => {
  const getStatusIcon = (result: ValidationResult) => {
    if (result.color === 'green') {
      return <CheckCircle2 className="h-5 w-5 text-green-600" />
    } else if (result.color === 'red') {
      return <AlertTriangle className="h-5 w-5 text-red-600" />
    } else {
      return <XCircle className="h-5 w-5 text-yellow-600" />
    }
  }

  const getStatusColor = (result: ValidationResult) => {
    if (result.color === 'green') return 'bg-green-50 border-green-200'
    if (result.color === 'red') return 'bg-red-50 border-red-200'
    return 'bg-yellow-50 border-yellow-200'
  }

  const getStatusText = (result: ValidationResult) => {
    if (result.color === 'green') return 'Perfect Match'
    if (result.color === 'red') return 'Partial Match'
    return 'No Match'
  }

  const getStatusDescription = (result: ValidationResult) => {
    if (result.color === 'green') return 'Bill and supporting document match completely'
    if (result.color === 'red') return 'Some fields don\'t match or have discrepancies'
    return 'No supporting document found for this bill'
  }

  const exportToCSV = () => {
    const headers = ['SI No', 'Bill/Cash Memo', 'Amount', 'Status', 'Matched Document', 'Mismatches', 'Notes']
    const rows = results.validation_results.map(result => [
      result.bill_entry.si_no,
      result.bill_entry.bill_cash_memo,
      `₹${result.bill_entry.amount}`,
      getStatusText(result),
      result.matched_document?.filename || 'None',
      result.mismatches.join('; ') || 'None',
      result.notes || 'None'
    ])

    const csvContent = [headers, ...rows]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `bill-validation-results-${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Summary */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Validation Results</h2>
          <div className="flex space-x-3">
            {onBackToPreview && (
              <button
                onClick={onBackToPreview}
                className="inline-flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Preview
              </button>
            )}
            <button
              onClick={exportToCSV}
              className="inline-flex items-center px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 transition-colors"
            >
              <Download className="h-4 w-4 mr-2" />
              Export CSV
            </button>
            <button
              onClick={onReset}
              className="inline-flex items-center px-4 py-2 bg-gray-600 text-white text-sm font-medium rounded-lg hover:bg-gray-700 transition-colors"
            >
              <RotateCcw className="h-4 w-4 mr-2" />
              Start Over
            </button>
          </div>
        </div>

        {/* Color Legend */}
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-sm font-medium text-gray-900 mb-3">Color Coding Legend</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-700">
                <strong>Green:</strong> Perfect match - No action required
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-red-500 rounded-full"></div>
              <span className="text-sm text-gray-700">
                <strong>Red:</strong> Partial match - Review discrepancies
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-yellow-500 rounded-full"></div>
              <span className="text-sm text-gray-700">
                <strong>Yellow:</strong> No match - Upload missing document
              </span>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-gray-900">{results.summary.total_bills}</div>
            <div className="text-gray-700 text-sm">Total Bills</div>
          </div>
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-green-900">{results.summary.matched_bills}</div>
            <div className="text-green-700 text-sm">Perfect Matches</div>
          </div>
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-red-900">{results.summary.partial_matches}</div>
            <div className="text-red-700 text-sm">Partial Matches</div>
          </div>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-yellow-900">{results.summary.unmatched_bills}</div>
            <div className="text-yellow-700 text-sm">No Matches</div>
          </div>
        </div>

        <div className="text-sm text-gray-600">
          Processing time: {results.summary.processing_time.toFixed(2)}s
        </div>
      </div>

      {/* Detailed Results */}
      <div className="space-y-4">
        {results.validation_results.map((result, index) => (
          <div key={index} className={`bg-white rounded-lg shadow-sm border p-6 ${getStatusColor(result)}`}>
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                {getStatusIcon(result)}
                <div>
                  <h3 className="text-lg font-medium text-gray-900">
                    Bill {result.bill_entry.si_no}: {result.bill_entry.bill_cash_memo}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {result.bill_entry.classification} - ₹{result.bill_entry.amount.toLocaleString()}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                  result.color === 'green' ? 'bg-green-100 text-green-800' :
                  result.color === 'red' ? 'bg-red-100 text-red-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {getStatusText(result)}
                </div>
              </div>
            </div>

            <div className="mb-4">
              <p className="text-sm text-gray-700">{getStatusDescription(result)}</p>
            </div>

            {/* Match Details */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium text-gray-700">Bill Number:</span>
                {result.bill_number_match ? (
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                ) : (
                  <XCircle className="h-4 w-4 text-red-600" />
                )}
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium text-gray-700">Amount:</span>
                {result.amount_match ? (
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                ) : (
                  <XCircle className="h-4 w-4 text-red-600" />
                )}
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium text-gray-700">Date:</span>
                {result.date_match ? (
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                ) : (
                  <XCircle className="h-4 w-4 text-red-600" />
                )}
              </div>
            </div>

            {/* Matched Document */}
            {result.matched_document && (
              <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <FileText className="h-4 w-4 text-blue-600" />
                  <span className="text-sm font-medium text-blue-900">Matched Document</span>
                </div>
                <div className="text-sm text-blue-800">
                  <p><strong>File:</strong> {result.matched_document.filename}</p>
                  {result.matched_document.bill_number && (
                    <p><strong>Bill Number:</strong> {result.matched_document.bill_number}</p>
                  )}
                  {result.matched_document.amount && (
                    <p><strong>Amount:</strong> ₹{result.matched_document.amount.toLocaleString()}</p>
                  )}
                  {result.matched_document.date && (
                    <p><strong>Date:</strong> {result.matched_document.date}</p>
                  )}
                </div>
              </div>
            )}

            {/* Mismatches */}
            {result.mismatches.length > 0 && (
              <div className="mb-4">
                <h4 className="text-sm font-medium text-gray-900 mb-2">Discrepancies Found:</h4>
                <ul className="space-y-1">
                  {result.mismatches.map((mismatch, idx) => (
                    <li key={idx} className="text-sm text-red-700 flex items-start">
                      <span className="flex-shrink-0 w-1.5 h-1.5 bg-red-500 rounded-full mt-2 mr-2"></span>
                      {mismatch}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Notes */}
            {result.notes && (
              <div className="text-sm text-gray-600 italic">
                Note: {result.notes}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default ValidationResults

