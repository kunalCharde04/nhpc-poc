import { FileText, Eye, EyeOff, CheckCircle2, Loader2 } from 'lucide-react'
import { useState } from 'react'

// Updated interface to match the new backend API
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

interface BillEntriesPreviewProps {
  entries: BillEntry[];
  count: number;
  extractionMethod: string;
  onProceedToValidation: () => void;
  isLoading?: boolean;
}

const BillEntriesPreview = ({ entries, count, extractionMethod, onProceedToValidation, isLoading = false }: BillEntriesPreviewProps) => {
  const [showDetails, setShowDetails] = useState(true)

  const totalAmount = entries.reduce((sum, entry) => sum + entry.amount, 0)

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Summary Header */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <FileText className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">Extracted Bill Entries</h2>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              extractionMethod.toLowerCase().includes('ai') 
                ? 'bg-green-100 text-green-800' 
                : 'bg-blue-100 text-blue-800'
            }`}>
              {extractionMethod}
            </span>
          </div>
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="inline-flex items-center px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            {showDetails ? (
              <>
                <EyeOff className="h-4 w-4 mr-2" />
                Hide Details
              </>
            ) : (
              <>
                <Eye className="h-4 w-4 mr-2" />
                Show Details
              </>
            )}
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-blue-900">{count}</div>
            <div className="text-blue-700 text-sm">Total Bills Found</div>
          </div>
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-green-900">₹{totalAmount.toLocaleString()}</div>
            <div className="text-green-700 text-sm">Total Amount</div>
          </div>
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-purple-900">
              ₹{(totalAmount / count).toLocaleString()}
            </div>
            <div className="text-purple-700 text-sm">Average Amount</div>
          </div>
        </div>

        <div className="text-center">
          <button
            onClick={onProceedToValidation}
            disabled={isLoading}
            className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                Processing Validation...
              </>
            ) : (
              <>
                <CheckCircle2 className="h-5 w-5 mr-2" />
                Proceed to Validation
              </>
            )}
          </button>
        </div>
      </div>

      {/* Detailed Bill Entries */}
      {showDetails && (
        <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
          <div className="px-6 py-4 bg-gray-50 border-b">
            <h3 className="text-lg font-medium text-gray-900">Bill Details</h3>
            <p className="text-sm text-gray-600">Showing all extracted bill entries with detailed information</p>
          </div>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    SI No
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Bill/Cash Memo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Classification
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {entries.map((entry, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {entry.si_no}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-mono">
                      {entry.bill_cash_memo}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {entry.bill_date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {entry.classification}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      ₹{entry.amount.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {entry.type_of_treatment}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default BillEntriesPreview
