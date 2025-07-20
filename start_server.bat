@echo off
echo 🏦 Starting MCP Banking Backend with Database...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Fix dependency conflicts and install requirements
echo 📦 Installing/updating dependencies...
echo Fixing python-multipart compatibility...
pip install "python-multipart>=0.0.9" --upgrade

echo Installing other dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Dependency installation failed. Please run fix_dependencies.bat first.
    pause
    exit /b 1
)

echo.
echo 🚀 Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Default test credentials:
echo Username: john_doe
echo Password: password123
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
