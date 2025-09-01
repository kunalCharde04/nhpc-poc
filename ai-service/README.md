# Medical Bill AI Service

AI-powered medical bill validation service using Google Gemini API.

## Features

- **Bill Data Extraction**: Extract structured data from medical bill images using Gemini Vision
- **PDF Text Analysis**: Analyze PDF text to extract bill entries using Gemini
- **Bill Validation**: AI-powered validation to match bill entries with supporting documents
- **Batch Processing**: Process multiple files simultaneously
- **RESTful API**: Easy integration with FastAPI endpoints

## Setup

### 1. Install Dependencies

```bash
cd ai-service
pip install -r requirements.txt
```

### 2. Environment Configuration

1. Copy the environment template:
```bash
cp env.example .env
```

2. Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 3. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

## Running the Service

```bash
python main.py
```

The service will start on `http://localhost:8001`

## API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /status` - Detailed service status

### Universal AI Processing
- `POST /process` - Universal endpoint for AI processing with custom model, prompt, and files

## Usage Examples

### Basic Bill Data Extraction
```bash
curl -X POST "http://localhost:8001/process" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "model=gemini-2.0-pro" \
  -F "prompt=Extract bill number, amount, and patient name from this medical bill image" \
  -F "files=@bill_image.jpg"
```

### Custom Analysis with Multiple Files
```bash
curl -X POST "http://localhost:8001/process" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "model=gemini-2.0-pro" \
  -F "prompt=Compare these medical bills and identify any discrepancies or patterns" \
  -F "files=@bill1.jpg" \
  -F "files=@bill2.jpg" \
  -F "files=@bill3.jpg"
```

### Bill Validation
```bash
curl -X POST "http://localhost:8001/process" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "model=gemini-2.0-flash-exp" \
  -F "prompt=Validate if this bill matches the expected bill number: B12345 and amount: $250.00. Provide a confidence score." \
  -F "files=@scanned_bill.jpg"
```

## Integration

This AI service is designed to work with the main bill validation backend. The backend can call these AI endpoints for enhanced processing capabilities.

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `AI_SERVICE_PORT`: Port to run the service (default: 8001)
- `AI_SERVICE_HOST`: Host to bind the service (default: 0.0.0.0)
- `ENVIRONMENT`: Environment mode (development/production)

## Error Handling

The service includes comprehensive error handling and logging. Check the console output for detailed error messages and API responses.

## Security Notes

- Never commit your `.env` file with real API keys
- Use environment-specific configuration
- Implement proper authentication for production use
- Consider rate limiting for the Gemini API calls
