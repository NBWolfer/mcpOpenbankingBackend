#!/bin/bash
# Startup script for Unix-like systems

echo "🏦 Starting MCP Banking Backend with Database..."
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    exit 1
fi

# Install requirements if needed
echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

echo ""
echo "🚀 Starting FastAPI server..."
echo "Server will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Default test credentials:"
echo "Username: john_doe"
echo "Password: password123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
