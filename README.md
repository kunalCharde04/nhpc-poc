# NHPC Medical Bill Validation System

A comprehensive AI-powered system for validating medical bills against supporting documents using Google Gemini AI. This system consists of three main components: an AI service, a backend API, and a React frontend.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │   AI Service    │
│   (React)       │◄──►│   (FastAPI)      │◄──►│   (Gemini AI)   │
│   Port: 5173    │    │   Port: 8000     │    │   Port: 8001    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
NHPC/
├── ai-service/                 # AI-powered document processing service
│   ├── gemini_service.py      # Google Gemini AI integration
│   ├── main.py                # FastAPI application
│   ├── start.py               # Service startup script
│   └── requirements.txt       # Python dependencies
├── bill-validator-backend/    # Main backend API service
│   ├── bill_validator.py      # Core validation logic
│   ├── main.py                # FastAPI application
│   ├── models.py              # Data models
│   ├── start.py               # Service startup script
│   └── requirements.txt       # Python dependencies
├── bill-validator/            # React frontend application
│   ├── src/                   # React source code
│   ├── package.json           # Node.js dependencies
│   └── vite.config.ts         # Vite configuration
├── start_services.sh          # Automated startup script
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** installed on your system
- **Node.js 18+** and npm installed
- **Google Gemini API Key** (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

### 1. Clone and Setup

```bash
# Navigate to the project directory
cd /Users/parchaa/Desktop/NHPC

# Make the startup script executable
chmod +x start_services.sh
```

### 2. Environment Configuration

#### AI Service Setup
```bash
cd ai-service
cp env.example .env
# Edit .env and add your Gemini API key:
# GEMINI_API_KEY=your_actual_gemini_api_key_here
```

#### Backend Setup
```bash
cd ../bill-validator-backend
cp env.example .env
# Configure any additional environment variables if needed
```

### 3. Install Dependencies

#### Python Dependencies
```bash
# Install AI service dependencies
cd ai-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install backend dependencies
cd ../bill-validator-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Frontend Dependencies
```bash
cd ../bill-validator
npm install
```

### 4. Start All Services

#### Option 1: Automated Startup (Recommended)
```bash
# From the root directory
./start_services.sh
```

This script will:
- Start the AI service on port 8001
- Start the backend API on port 8000
- Start the frontend development server on port 5173
- Perform health checks on all services
- Display service URLs and process IDs

#### Option 2: Manual Startup

**Terminal 1 - AI Service:**
```bash
cd ai-service
source venv/bin/activate
python3 start.py
```

**Terminal 2 - Backend API:**
```bash
cd bill-validator-backend
source venv/bin/activate
python3 start.py
```

**Terminal 3 - Frontend:**
```bash
cd bill-validator
npm run dev
```

## 🌐 Service URLs

Once all services are running, you can access:

- **Frontend Application**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **AI Service**: http://localhost:8001
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

## 🔧 API Endpoints

### Backend API (Port 8000)

- `POST /extract-bill-entries` - Extract bill entries from PDF
- `POST /process-documents` - Process supporting documents
- `POST /validate-bills` - Complete bill validation workflow

### AI Service (Port 8001)

- `POST /process` - Universal AI processing endpoint
- `GET /` - Health check
- `GET /status` - Service status

## 📋 Features

### Frontend (React + TypeScript)
- Modern, responsive UI built with React and Tailwind CSS
- File upload interface for bills and supporting documents
- Real-time validation results display
- Interactive bill preview and analysis
- Navigation between different pages (Home, Validate, How It Works)

### Backend API (FastAPI)
- RESTful API for bill validation workflows
- PDF text extraction and analysis
- Document comparison and mismatch detection
- Integration with AI service for enhanced processing
- Comprehensive error handling and validation

### AI Service (Gemini AI)
- Google Gemini 2.0 Pro integration for document analysis
- Image and PDF processing capabilities
- Intelligent bill data extraction
- Custom prompt-based analysis
- Batch processing support

## 🛠️ Development

### Frontend Development
```bash
cd bill-validator
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run preview      # Preview production build
```

### Backend Development
```bash
cd bill-validator-backend
source venv/bin/activate
python3 main.py      # Run with auto-reload
```

### AI Service Development
```bash
cd ai-service
source venv/bin/activate
python3 main.py      # Run with auto-reload
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find and kill processes using the ports
   lsof -ti:8000 | xargs kill -9
   lsof -ti:8001 | xargs kill -9
   lsof -ti:5173 | xargs kill -9
   ```

2. **Python Virtual Environment Issues**
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Node.js Dependencies Issues**
   ```bash
   cd bill-validator
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Gemini API Key Issues**
   - Ensure your API key is correctly set in `ai-service/.env`
   - Verify the key has proper permissions
   - Check API usage limits

### Service Health Checks

```bash
# Test AI Service
curl http://localhost:8001/

# Test Backend API
curl http://localhost:8000/

# Test Frontend (should return HTML)
curl http://localhost:5173/
```

## 📝 Environment Variables

### AI Service (.env)
```
GEMINI_API_KEY=your_gemini_api_key_here
AI_SERVICE_PORT=8001
AI_SERVICE_HOST=0.0.0.0
ENVIRONMENT=development
```

### Backend Service (.env)
```
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
AI_SERVICE_URL=http://localhost:8001
ENVIRONMENT=development
```

## 🚀 Production Deployment

For production deployment:

1. **Build Frontend:**
   ```bash
   cd bill-validator
   npm run build
   ```

2. **Configure Production Environment Variables**
   - Set `ENVIRONMENT=production`
   - Configure proper host and port settings
   - Set up reverse proxy (nginx/Apache)

3. **Use Production WSGI Server:**
   ```bash
   # For backend and AI service
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

## 📄 License

This project is part of the NHPC Medical Bill Validation System.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For technical support or questions about the NHPC Medical Bill Validation System, please contact the development team.

---

**Note**: Make sure to keep your API keys secure and never commit them to version control. Always use environment variables for sensitive configuration.
