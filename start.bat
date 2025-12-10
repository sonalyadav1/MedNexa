@echo off
echo Starting MedNexa - Multi-Agent AI Pharma Research Assistant
echo ==============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 3 is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)

echo.
echo Setting up Backend...
echo ------------------------

cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt --quiet

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit backend\.env with your API keys
)

REM Start backend server
echo Starting FastAPI backend server...
start "MedNexa Backend" python main.py

timeout /t 5 /nobreak >nul

cd ..

echo.
echo Setting up Frontend...
echo -------------------------

cd frontend

REM Install npm dependencies if needed
if not exist "node_modules" (
    echo Installing npm dependencies...
    call npm install
)

REM Start frontend development server
echo Starting React frontend...
start "MedNexa Frontend" npm run dev

echo.
echo ==============================================================
echo MedNexa is running!
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the services
echo ==============================================================

pause
