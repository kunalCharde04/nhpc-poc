#!/bin/bash

# Start script for NHPC Medical Bill Validation System

echo "Starting NHPC Medical Bill Validation System..."
echo "================================================="

# Function to check if a command was successful
check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed to start"
        exit 1
    fi
}

# Check if required directories exist
if [ ! -d "ai-service" ] || [ ! -d "bill-validator-backend" ] || [ ! -d "bill-validator" ]; then
    echo "Error: Required directories not found. Please run this script from the NHPC root directory."
    exit 1
fi

echo "1. Starting AI Service (Port 8001)..."
cd ai-service
source venv/bin/activate && python3 start.py &
AI_PID=$!
cd ..

echo "2. Starting Backend Service (Port 8000)..."
cd bill-validator-backend
source venv/bin/activate && python3 start.py &
BACKEND_PID=$!
cd ..

echo "3. Starting Frontend Development Server (Port 5173)..."
cd bill-validator
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "Services started successfully!"
echo "=============================="
echo "AI Service:      http://localhost:8001"
echo "Backend API:     http://localhost:8000"
echo "Frontend:        http://localhost:5173"
echo ""
echo "Process IDs:"
echo "AI Service:      $AI_PID"
echo "Backend:         $BACKEND_PID"
echo "Frontend:        $FRONTEND_PID"
echo ""
echo "To stop all services, press Ctrl+C or run:"
echo "kill $AI_PID $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Waiting for services to initialize..."
sleep 5

# Test if services are responding
echo "Testing service health..."
curl -s http://localhost:8001/ > /dev/null && echo "✓ AI Service is responding" || echo "✗ AI Service not responding"
curl -s http://localhost:8000/ > /dev/null && echo "✓ Backend Service is responding" || echo "✗ Backend Service not responding"

echo ""
echo "All services are running! Open http://localhost:5173 in your browser."

# Wait for user to stop services
wait
