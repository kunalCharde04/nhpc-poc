  import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, AlertCircle, Loader2, CheckCircle2, Shield, FileImage } from 'lucide-react'

interface FileUploaderProps {
  onValidate: (billEntriesPdf: File, supportingDocs: File[]) => void
  isLoading: boolean
}

const FileUploader = ({ onValidate, isLoading }: FileUploaderProps) => {
  const [billEntriesFile, setBillEntriesFile] = useState<File | null>(null)
  const [supportingDocs, setSupportingDocs] = useState<File[]>([])
  const [errors, setErrors] = useState<string[]>([])  

  const onBillEntriesDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file && (file.type === 'application/pdf' || file.type.startsWith('image/'))) {
      setBillEntriesFile(file)
      setErrors(prev => prev.filter(error => !error.includes('bill entries')))
    } else {
      setErrors(prev => [...prev.filter(error => !error.includes('bill entries')), 
        'Bill entries file must be a PDF or image (JPG, PNG, BMP, TIFF)'])
    }
  }, [])

  const onSupportingDocsDrop = useCallback((acceptedFiles: File[]) => {
    const validFiles = acceptedFiles.filter(file => 
      file.type === 'application/pdf' || file.type.startsWith('image/')
    )
    
    if (validFiles.length !== acceptedFiles.length) {
      setErrors(prev => [...prev.filter(error => !error.includes('supporting documents')), 
        'Supporting documents must be PDFs or images (JPG, PNG, BMP, TIFF)'])
    } else {
      setErrors(prev => prev.filter(error => !error.includes('supporting documents')))
    }
    
    setSupportingDocs(prev => [...prev, ...validFiles])
  }, [])

  const billEntriesDropzone = useDropzone({
    onDrop: onBillEntriesDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    },
    maxFiles: 1,
    multiple: false
  })

  const supportingDocsDropzone = useDropzone({
    onDrop: onSupportingDocsDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    },
    multiple: true
  })

  const handleValidate = () => {
    const newErrors: string[] = []
    
    if (!billEntriesFile) {
      newErrors.push('Please upload the bill entries file (PDF or image)')
    }
    
    if (supportingDocs.length === 0) {
      newErrors.push('Please upload at least one supporting document')
    }
    
    setErrors(newErrors)
    
    if (newErrors.length === 0 && billEntriesFile) {
      onValidate(billEntriesFile, supportingDocs)
    }
  }

  const removeSupportingDoc = (index: number) => {
    setSupportingDocs(prev => prev.filter((_, i) => i !== index))
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (file: File) => {
    if (file.type === 'application/pdf') {
      return <FileText className="h-5 w-5 text-red-600" />
    } else if (file.type.startsWith('image/')) {
      return <FileImage className="h-5 w-5 text-green-600" />
    }
    return <FileText className="h-5 w-5 text-blue-600" />
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-blue-900 mb-3">How to Use</h2>
        <div className="space-y-2 text-blue-800">
          <p>1. Upload your <strong>Bill Entries</strong> (PDF or image) containing the table with bill numbers and amounts</p>
          <p>2. Upload <strong>Supporting Documents</strong> (scanned bills, prescriptions, receipts, images)</p>
          <p>3. Click <strong>Validate Bills</strong> to cross-check the information</p>
          <p>4. Review the validation results showing any mismatches found</p>
        </div>
        
        {/* Supported File Types */}
        <div className="mt-4 pt-4 border-t border-blue-200">
          <h3 className="text-sm font-medium text-blue-900 mb-2">Supported File Types:</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <FileText className="h-4 w-4 text-blue-600" />
              <span className="text-blue-700">Bill Entries: PDF or Images</span>
            </div>
            <div className="flex items-center space-x-2">
              <FileText className="h-4 w-4 text-red-600" />
              <span className="text-blue-700">Supporting Docs: PDF files</span>
            </div>
            <div className="flex items-center space-x-2">
              <FileImage className="h-4 w-4 text-green-600" />
              <span className="text-blue-700">Supporting Docs: Images (JPG, PNG, BMP, TIFF)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Errors */}
      {errors.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start">
            <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3" />
            <div>
              <h3 className="text-red-800 font-medium">Please fix the following errors:</h3>
              <ul className="mt-2 list-disc list-inside text-red-700 text-sm">
                {errors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-8">
        {/* Bill Entries Upload */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <FileText className="h-5 w-5 text-blue-600 mr-2" />
            1. Bill Entries (PDF or Image)
          </h3>
          
          <div
            {...billEntriesDropzone.getRootProps()}
            className={`
              border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer
              ${billEntriesDropzone.isDragActive 
                ? 'border-blue-400 bg-blue-50' 
                : billEntriesFile 
                  ? 'border-green-400 bg-green-50' 
                  : 'border-gray-300 bg-gray-50 hover:border-gray-400'
              }
            `}
          >
            <input {...billEntriesDropzone.getInputProps()} />
            <div className="space-y-3">
              {billEntriesFile ? (
                <>
                  <CheckCircle2 className="h-8 w-8 text-green-600 mx-auto" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{billEntriesFile.name}</p>
                    <p className="text-xs text-gray-500">{formatFileSize(billEntriesFile.size)}</p>
                  </div>
                </>
              ) : (
                <>
                  <Upload className="h-8 w-8 text-gray-400 mx-auto" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {billEntriesDropzone.isDragActive ? 'Drop PDF here' : 'Click to upload or drag PDF'}
                    </p>
                    <p className="text-xs text-gray-500">PDF files only</p>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Supporting Documents Upload */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <FileText className="h-5 w-5 text-blue-600 mr-2" />
            2. Supporting Documents
          </h3>
          
          <div
            {...supportingDocsDropzone.getRootProps()}
            className={`
              border-2 border-dashed rounded-lg p-6 text-center transition-colors cursor-pointer
              ${supportingDocsDropzone.isDragActive 
                ? 'border-blue-400 bg-blue-50' 
                : 'border-gray-300 bg-gray-50 hover:border-gray-400'
              }
            `}
          >
            <input {...supportingDocsDropzone.getInputProps()} />
            <div className="space-y-3">
              <Upload className="h-6 w-6 text-gray-400 mx-auto" />
              <div>
                <p className="text-sm font-medium text-gray-900">
                  {supportingDocsDropzone.isDragActive ? 'Drop files here' : 'Click to upload or drag files'}
                </p>
                <p className="text-xs text-gray-500">PDFs, Images (JPG, PNG, BMP, TIFF)</p>
              </div>
            </div>
          </div>

          {/* Uploaded Supporting Documents */}
          {supportingDocs.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-sm font-medium text-gray-700">Uploaded Documents:</h4>
              {supportingDocs.map((doc, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-2">
                    {getFileIcon(doc)}
                    <div>
                      <p className="text-sm font-medium text-gray-900">{doc.name}</p>
                      <p className="text-xs text-gray-500">{formatFileSize(doc.size)}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => removeSupportingDoc(index)}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Validation Button */}
      <div className="text-center">
        <button
          onClick={handleValidate}
          disabled={isLoading || !billEntriesFile || supportingDocs.length === 0}
          className={`
            inline-flex items-center px-8 py-3 rounded-lg font-semibold text-lg transition-all duration-200
            ${isLoading || !billEntriesFile || supportingDocs.length === 0
              ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-xl transform hover:-translate-y-1'
            }
          `}
        >
          {isLoading ? (
            <>
              <Loader2 className="h-5 w-5 mr-2 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <Shield className="h-5 w-5 mr-2" />
              Validate Bills
            </>
          )}
        </button>
        
        {(!billEntriesFile || supportingDocs.length === 0) && (
          <p className="text-sm text-gray-500 mt-2">
            Please upload both a bill entries PDF and at least one supporting document
          </p>
        )}
      </div>
    </div>
  )
}

export default FileUploader

