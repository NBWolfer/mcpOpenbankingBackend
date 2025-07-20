# PowerShell script to start the MCP OpenBanking Backend Server
Write-Host "Starting MCP OpenBanking Backend Server..." -ForegroundColor Green
Write-Host ""

# Activate conda environment
Write-Host "Activating conda environment..." -ForegroundColor Yellow
conda activate openbanking-backend

# Install/update requirements if needed
Write-Host "Installing/updating dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Start the FastAPI server
Write-Host ""
Write-Host "Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
