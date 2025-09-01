# Medical Bill Validation System

A comprehensive AI-powered system for validating medical bills by cross-checking bill entries against supporting documents.

## 🏥 Features

- **PDF Processing**: Extract bill entries from PDF tables automatically
- **OCR Technology**: Read text from scanned documents and images
- **Smart Validation**: Cross-check bill numbers and amounts with fuzzy matching
- **Detailed Reports**: Generate comprehensive validation reports with mismatch details
- **Modern UI**: Clean, responsive web interface built with React and Tailwind CSS
- **Export Functionality**: Export validation results to CSV
- **Multi-language Support**: English and Hindi language support

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PyPDF2**: PDF text extraction
- **Tesseract OCR**: Optical character recognition
- **OpenCV**: Image preprocessing
- **Pillow**: Image processing
- **Pydantic**: Data validation

### Frontend
- **React 18**: Modern JavaScript library
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icons
- **React Dropzone**: File upload functionality

## 📋 Prerequisites

Before running this application, make sure you have:

1. **Python 3.9+** installed
2. **Node.js 16+** and npm installed
3. **Tesseract OCR** installed:
   - **macOS**: `brew install tesseract`
   - **Ubuntu**: `sudo apt-get install tesseract-ocr`
   - **Windows**: Download from [Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki)

## 🚀 Installation & Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd bill-validator-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   python start.py
   ```

   The backend will be available at: `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd bill-validator
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at: `http://localhost:5173`

## 📖 Usage Guide

### Step 1: Prepare Your Documents

1. **Bill Entries PDF**: A PDF containing a table with bill numbers, amounts, and other details
2. **Supporting Documents**: Scanned bills, prescriptions, receipts (PDF or image formats)

### Step 2: Upload Files

1. Open the web application in your browser
2. Upload the Bill Entries PDF in the first section
3. Upload supporting documents in the second section
4. Click "Validate Bills" to start the process

### Step 3: Review Results

The system will provide:
- **Summary Statistics**: Total bills, valid bills, mismatched bills, success rate
- **Detailed Results**: Row-by-row validation with specific mismatch information
- **Export Options**: Download results as CSV

## 🔍 Validation Process

The system performs the following checks:

1. **Bill Number Matching**:
   - Exact matches
   - Fuzzy matching with similarity threshold
   - Format normalization (removing separators)

2. **Amount Matching**:
   - Exact amount comparison
   - Tolerance-based matching (5% default)
   - Currency format handling

3. **Document Association**:
   - Attempts to match each bill entry with supporting documents
   - Uses combination of bill number and amount for verification
   - Provides confidence scores for matches

## 📊 Validation Results

### Status Types
- **✅ Valid**: Perfect match found
- **⚠️ Partial**: Some fields match, others don't
- **❌ Invalid**: Significant mismatches found
- **🔍 Not Found**: No supporting document found

### Mismatch Types
- **Bill Number Mismatch**: Bill numbers don't match
- **Amount Mismatch**: Amounts don't match within tolerance
- **Document Not Found**: No supporting document available

## 🔧 Configuration

### Backend Configuration
- Modify tolerance settings in `bill_validator.py`
- Adjust OCR parameters in `pdf_processor.py`
- Update file size limits in `main.py`

### Frontend Configuration
- Update API endpoint in `App.tsx` if backend runs on different port
- Modify UI themes in `tailwind.config.js`

## 📁 Project Structure

```
NHPC/
├── bill-validator/                 # Frontend React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── FileUploader.tsx
│   │   │   └── ValidationResults.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── tailwind.config.js
├── bill-validator-backend/         # Backend FastAPI application
│   ├── main.py                    # Main application file
│   ├── models.py                  # Pydantic data models
│   ├── pdf_processor.py           # PDF and OCR processing
│   ├── bill_validator.py          # Validation logic
│   ├── requirements.txt           # Python dependencies
│   └── start.py                   # Startup script
└── README.md
```

## 🐛 Troubleshooting

### Common Issues

1. **Tesseract not found error**:
   - Ensure Tesseract is installed and in PATH
   - Update `tesseract_cmd` path if needed

2. **CORS errors**:
   - Check that frontend and backend URLs are correctly configured
   - Ensure CORS middleware is properly set up

3. **File upload errors**:
   - Check file size limits
   - Verify file formats are supported

4. **OCR accuracy issues**:
   - Ensure documents are high quality and well-scanned
   - Adjust OCR parameters for your document type

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the API documentation at `/docs`

## 🔮 Future Enhancements

- **Database Integration**: Store validation history
- **Batch Processing**: Handle large volumes of bills
- **Advanced OCR**: Improve accuracy with machine learning
- **Multi-language OCR**: Support for regional languages
- **API Authentication**: Secure API endpoints
- **Real-time Processing**: WebSocket integration for live updates

# nhpc-poc
