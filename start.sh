#!/bin/bash

echo "🚀 Starting MedNexa - Multi-Agent AI Pharma Research Assistant"
echo "=============================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo ""
echo "📦 Setting up Backend..."
echo "------------------------"

# Navigate to backend directory
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your API keys"
fi

# Start backend server in background
echo "Starting FastAPI backend server..."
python main.py &
BACKEND_PID=$!

echo "✅ Backend started on http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"

# Wait for backend to start
sleep 5

cd ..

echo ""
echo "📦 Setting up Frontend..."
echo "-------------------------"

# Navigate to frontend directory
cd frontend

# Install npm dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Start frontend development server
echo "Starting React frontend..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Frontend started on http://localhost:3000"

echo ""
echo "=============================================================="
echo "🎉 MedNexa is running!"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=============================================================="

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
