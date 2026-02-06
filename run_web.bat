@echo off
echo [SYSTEM] Initializing Secure Access Web Server...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [SYSTEM] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo [SYSTEM] Installing web dependencies...
pip install -r requirements.txt >nul 2>&1

REM Run the server
echo [SYSTEM] Server launching on http://127.0.0.1:5000 ...
python src/web/app.py

pause
