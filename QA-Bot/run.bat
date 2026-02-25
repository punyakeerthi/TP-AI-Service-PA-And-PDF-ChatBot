@echo off
echo 🤖 Starting PDF QA Bot...
echo ================================

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found!
    echo Please copy .env.example to .env and add your Google API key
    echo.
    echo Steps:
    echo 1. copy .env.example .env
    echo 2. Edit .env and add your GOOGLE_API_KEY
    echo 3. Run this script again
    pause
    exit /b 1
)

REM Check if virtual environment should be created
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Start the application
echo 🚀 Starting Streamlit application...
echo The app will open in your browser at http://localhost:8501
echo.
streamlit run app.py

pause