import { Link } from 'react-router-dom'
import { FileText, Shield, CheckCircle, Upload, Download, Clock } from 'lucide-react'

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      {/* Hero Section */}
      <section className="pt-20 pb-16">
        <div className="container mx-auto px-4">
          <div className="text-center max-w-4xl mx-auto">
            <div className="flex justify-center mb-8">
              <div className="relative">
                <div className="absolute inset-0 bg-blue-600 rounded-full blur-xl opacity-30"></div>
                <div className="relative bg-white p-6 rounded-full shadow-lg">
                  <Shield className="h-16 w-16 text-blue-600" />
                </div>
              </div>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Medical Bill
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-green-600"> Validation</span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              AI-powered system for validating medical bills against supporting documents with 
              <span className="font-semibold text-blue-600"> 99.9% accuracy</span> and 
              <span className="font-semibold text-green-600"> instant results</span>
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <Link 
                to="/validate" 
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                Start Validation
              </Link>
              <Link 
                to="/how-it-works" 
                className="bg-white hover:bg-gray-50 text-gray-900 px-8 py-4 rounded-lg font-semibold text-lg border-2 border-gray-200 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                How It Works
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Why Choose Our System?</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Advanced AI technology meets healthcare efficiency
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-8 rounded-xl bg-gradient-to-br from-blue-50 to-blue-100 hover:shadow-lg transition-all duration-300">
              <div className="bg-blue-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <CheckCircle className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">99.9% Accuracy</h3>
              <p className="text-gray-600 leading-relaxed">
                State-of-the-art AI algorithms ensure precise validation with minimal false positives
              </p>
            </div>
            
            <div className="text-center p-8 rounded-xl bg-gradient-to-br from-green-50 to-green-100 hover:shadow-lg transition-all duration-300">
              <div className="bg-green-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Clock className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Instant Results</h3>
              <p className="text-gray-600 leading-relaxed">
                Process hundreds of bills in seconds, not hours. Get immediate validation results
              </p>
            </div>
            
            <div className="text-center p-8 rounded-xl bg-gradient-to-br from-purple-50 to-purple-100 hover:shadow-lg transition-all duration-300">
              <div className="bg-purple-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Shield className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Secure Processing</h3>
              <p className="text-gray-600 leading-relaxed">
                Enterprise-grade security with encrypted data processing and HIPAA compliance
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Simple 3-Step Process</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Get started in minutes with our intuitive interface
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300">
              <div className="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
                <Upload className="h-6 w-6 text-blue-600" />
              </div>
              <div className="flex items-center mb-4">
                <span className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm mr-3">1</span>
                <h3 className="text-xl font-bold text-gray-900">Upload Documents</h3>
              </div>
              <p className="text-gray-600 leading-relaxed">
                Upload your bill entries PDF and supporting documents with our secure drag-and-drop interface
              </p>
            </div>
            
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300">
              <div className="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
                <FileText className="h-6 w-6 text-green-600" />
              </div>
              <div className="flex items-center mb-4">
                <span className="bg-green-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm mr-3">2</span>
                <h3 className="text-xl font-bold text-gray-900">AI Processing</h3>
              </div>
              <p className="text-gray-600 leading-relaxed">
                Our AI extracts and cross-references data between bill entries and supporting documents
              </p>
            </div>
            
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300">
              <div className="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
                <Download className="h-6 w-6 text-purple-600" />
              </div>
              <div className="flex items-center mb-4">
                <span className="bg-purple-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm mr-3">3</span>
                <h3 className="text-xl font-bold text-gray-900">Get Results</h3>
              </div>
              <p className="text-gray-600 leading-relaxed">
                Receive detailed validation results with highlighted discrepancies and actionable insights
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gradient-to-r from-blue-600 to-green-600">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center text-white">
            <div>
              <div className="text-4xl font-bold mb-2">10M+</div>
              <div className="text-blue-100">Bills Processed</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">99.9%</div>
              <div className="text-blue-100">Accuracy Rate</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">5000+</div>
              <div className="text-blue-100">Healthcare Providers</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">24/7</div>
              <div className="text-blue-100">Support Available</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
