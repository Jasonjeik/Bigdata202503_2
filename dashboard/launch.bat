@echo off
REM Quick launch script for Windows
REM Double-click this file to start the application

echo ============================================================
echo Movie Sentiment Analytics Platform
echo Quick Launch
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Launch the application
echo.
echo Starting application...
echo The app will open in your browser automatically.
echo Press Ctrl+C to stop the server.
echo.

streamlit run app.py

pause
