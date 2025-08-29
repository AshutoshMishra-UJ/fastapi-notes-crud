#!/usr/bin/env bash
# Build script for Render

set -e  # Exit on any error

echo "🔧 Build script starting..."
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "📊 Testing imports..."
python -c "import fastapi; import sqlalchemy; import uvicorn; print('✅ All imports successful')"

echo "📊 Setting up database..."
python -c "from database import create_tables; create_tables(); print('✅ Database tables created')"

echo "✅ Build completed successfully!"
