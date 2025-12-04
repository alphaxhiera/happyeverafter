#!/bin/bash

# IHSG Analysis Application Startup Script

echo "🚀 Starting IHSG Analysis Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p ihsg_analysis/modules/{data_fetcher,technical_indicators,fundamental_analysis,recommendation_engine,ui_components}
mkdir -p logs

# Run the application
echo "🌐 Launching Streamlit application..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

echo "✅ Application started successfully!"
echo "📱 Open your browser and go to: http://localhost:8501"