import { Link } from 'react-router-dom'
import { ArrowLeft, Upload, Brain, CheckCircle, FileText, Search, AlertTriangle, Download } from 'lucide-react'

const HowItWorksPage = () => {
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
            <h1 className="text-2xl font-bold text-gray-900">How It Works</h1>
          </div>
        </div>
      </div>

      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Advanced AI Bill Validation Process
          </h2>
          <p className="text-xl text-gray-600 leading-relaxed">
            Our system uses cutting-edge artificial intelligence to extract, analyze, and validate 
            medical bill data with unprecedented accuracy and speed.
          </p>
        </div>

        {/* Process Steps */}
        <div className="space-y-16">
          {/* Step 1 */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="flex-shrink-0">
                <div className="bg-blue-100 w-24 h-24 rounded-full flex items-center justify-center">
                  <Upload className="h-12 w-12 text-blue-600" />
                </div>
              </div>
              <div className="flex-1">
                <div className="flex items-center mb-4">
                  <span className="bg-blue-600 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold mr-4">1</span>
                  <h3 className="text-2xl font-bold text-gray-900">Document Upload</h3>
                </div>
                <p className="text-gray-600 text-lg leading-relaxed mb-4">
                  Upload your bill entries PDF containing the list of bills to validate, along with 
                  supporting documents (actual bills, receipts, invoices) in PDF or image format.
                </p>
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">Supported Formats:</h4>
                  <ul className="text-blue-800 space-y-1">
                    <li>• PDF documents (bill entries and supporting documents)</li>
                    <li>• Image files (JPG, PNG, TIFF) for scanned bills</li>
                    <li>• Batch upload for multiple supporting documents</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Step 2 */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="flex-shrink-0">
                <div className="bg-green-100 w-24 h-24 rounded-full flex items-center justify-center">
                  <Search className="h-12 w-12 text-green-600" />
                </div>
              </div>
              <div className="flex-1">
                <div className="flex items-center mb-4">
                  <span className="bg-green-600 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold mr-4">2</span>
                  <h3 className="text-2xl font-bold text-gray-900">Data Extraction</h3>
                </div>
                <p className="text-gray-600 text-lg leading-relaxed mb-4">
                  Our advanced OCR and AI algorithms extract key information from both the bill entries 
                  and supporting documents, including bill numbers, amounts, dates, and patient information.
                </p>
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-green-900 mb-2">From Bill Entries:</h4>
                    <ul className="text-green-800 space-y-1 text-sm">
                      <li>• Bill numbers</li>
                      <li>• Bill amounts</li>
                      <li>• Patient names</li>
                      <li>• Dates and references</li>
                    </ul>
                  </div>
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-green-900 mb-2">From Supporting Docs:</h4>
                    <ul className="text-green-800 space-y-1 text-sm">
                      <li>• Invoice numbers</li>
                      <li>• Total amounts</li>
                      <li>• Service details</li>
                      <li>• Hospital information</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Step 3 */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="flex-shrink-0">
                <div className="bg-purple-100 w-24 h-24 rounded-full flex items-center justify-center">
                  <Brain className="h-12 w-12 text-purple-600" />
                </div>
              </div>
              <div className="flex-1">
                <div className="flex items-center mb-4">
                  <span className="bg-purple-600 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold mr-4">3</span>
                  <h3 className="text-2xl font-bold text-gray-900">AI Analysis & Matching</h3>
                </div>
                <p className="text-gray-600 text-lg leading-relaxed mb-4">
                  Our AI engine performs intelligent matching between bill entries and supporting documents, 
                  using fuzzy matching algorithms to account for variations in formatting and data entry.
                </p>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-purple-900 mb-2">AI Capabilities:</h4>
                  <ul className="text-purple-800 space-y-1">
                    <li>• Fuzzy string matching for bill numbers and names</li>
                    <li>• Amount validation with tolerance for minor discrepancies</li>
                    <li>• Date parsing and validation across different formats</li>
                    <li>• Context-aware document matching</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Step 4 */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="flex-shrink-0">
                <div className="bg-orange-100 w-24 h-24 rounded-full flex items-center justify-center">
                  <CheckCircle className="h-12 w-12 text-orange-600" />
                </div>
              </div>
              <div className="flex-1">
                <div className="flex items-center mb-4">
                  <span className="bg-orange-600 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold mr-4">4</span>
                  <h3 className="text-2xl font-bold text-gray-900">Validation & Results</h3>
                </div>
                <p className="text-gray-600 text-lg leading-relaxed mb-4">
                  The system generates comprehensive validation results, highlighting matches, discrepancies, 
                  and providing detailed explanations for any issues found.
                </p>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="bg-green-50 p-4 rounded-lg text-center">
                    <CheckCircle className="h-8 w-8 text-green-600 mx-auto mb-2" />
                    <h5 className="font-semibold text-green-900">Valid Bills</h5>
                    <p className="text-green-800 text-sm">Perfect matches found</p>
                  </div>
                  <div className="bg-yellow-50 p-4 rounded-lg text-center">
                    <AlertTriangle className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                    <h5 className="font-semibold text-yellow-900">Discrepancies</h5>
                    <p className="text-yellow-800 text-sm">Issues requiring review</p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg text-center">
                    <FileText className="h-8 w-8 text-gray-600 mx-auto mb-2" />
                    <h5 className="font-semibold text-gray-900">No Match</h5>
                    <p className="text-gray-800 text-sm">Missing documents</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Technical Details */}
        <div className="mt-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-8 text-white">
          <h3 className="text-2xl font-bold mb-6 text-center">Technical Specifications</h3>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h4 className="text-lg font-semibold mb-3">AI & Machine Learning</h4>
              <ul className="space-y-2 text-blue-100">
                <li>• Advanced OCR with 99.9% accuracy</li>
                <li>• Natural Language Processing for text analysis</li>
                <li>• Machine learning models for pattern recognition</li>
                <li>• Continuous learning from validation patterns</li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-3">Security & Compliance</h4>
              <ul className="space-y-2 text-blue-100">
                <li>• HIPAA compliant data processing</li>
                <li>• End-to-end encryption</li>
                <li>• Secure cloud infrastructure</li>
                <li>• Data retention policies</li>
              </ul>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-16 text-center">
          <h3 className="text-3xl font-bold text-gray-900 mb-4">Ready to Get Started?</h3>
          <p className="text-xl text-gray-600 mb-8">
            Experience the power of AI-driven bill validation today
          </p>
          <Link 
            to="/validate" 
            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1 inline-block"
          >
            Start Validating Bills
          </Link>
        </div>
      </main>
    </div>
  )
}

export default HowItWorksPage
