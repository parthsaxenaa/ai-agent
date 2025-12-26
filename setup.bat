@echo off
echo ========================================
echo Vellicate Agent Setup
echo ========================================
echo.

echo [1/2] Installing Python dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to install dependencies.
    echo Please make sure Python and pip are installed.
    pause
    exit /b 1
)

echo.
echo [2/2] Setup complete!
echo.
echo Next steps:
echo 1. Edit the .env file and add your Gemini API key
echo 2. Run: streamlit run app.py
echo.
pause

