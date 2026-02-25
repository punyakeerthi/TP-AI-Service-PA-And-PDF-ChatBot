#!/bin/bash

# PDF QA Bot Startup Script

echo "🤖 Starting PDF QA Bot..."
echo "================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Please copy .env.example to .env and add your Google API key"
    echo ""
    echo "Steps:"
    echo "1. cp .env.example .env"
    echo "2. Edit .env and add your GOOGLE_API_KEY"
    echo "3. Run this script again"
    exit 1
fi

# Check if virtual environment should be created
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo "🚀 Starting Streamlit application..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
streamlit run app.py