@echo off
echo 🔧 Fixing dependency conflicts...
echo.

echo Installing compatible python-multipart version...
pip install "python-multipart>=0.0.9"

echo.
echo Installing remaining dependencies...
pip install -r requirements.txt

echo.
echo ✅ Dependencies installed successfully!
echo.
pause
