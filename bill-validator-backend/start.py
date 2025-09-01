"""
Startup script for AI-Powered Medical Bill Validation Backend
"""
import uvicorn
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting AI-Powered Medical Bill Validation System Backend...")
    print("=" * 60)
    
    # Check environment configuration
    ai_service_url = os.getenv('AI_SERVICE_URL', 'http://localhost:8001')
    app_host = os.getenv('APP_HOST', '0.0.0.0')
    app_port = int(os.getenv('APP_PORT', 8000))
    
    print("📋 System Configuration:")
    print(f"   • Backend Server: http://{app_host}:{app_port}")
    print(f"   • AI Service URL: {ai_service_url}")
    print(f"   • API Documentation: http://localhost:{app_port}/docs")
    print(f"   • Health Check: http://localhost:{app_port}/")
    
    print("\n🔧 Setup Requirements:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Start AI Service (from ai-service directory):")
    print("      cd ../ai-service && python start.py")
    print("   3. Set environment variables (copy env.example to .env)")
    print("   4. Ensure GEMINI_API_KEY is configured in AI service")
    
    print("\n✨ AI Features Available:")
    print("   • AI-powered document extraction")
    print("   • Intelligent bill validation")
    print("   • Pattern and anomaly detection")
    print("   • Custom AI analysis prompts")
    print("   • OCR fallback for reliability")
    
    print("\n🔗 API Endpoints:")
    print("   • /validate-bills - Main validation (with AI)")
    print("   • /extract-bill-entries - Extract bills (with AI)")
    print("   • /ai/analyze-document - Custom AI analysis")
    print("   • /ai/advanced-validation - Advanced AI validation")
    print("   • /ai/service-status - AI service health check")
    
    print("\n" + "=" * 60)
    print("🎯 Starting server...")
    
    uvicorn.run(
        "main:app",
        host=app_host,
        port=app_port,
        reload=True,
        log_level=os.getenv('LOG_LEVEL', 'info').lower()
    )
