#!/usr/bin/env python3
"""
Startup script for the FastAPI Notes CRUD application.
"""
import os
import sys
import subprocess

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import passlib
        import jose
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def main():
    """Main startup function."""
    print("🚀 Starting FastAPI Notes CRUD Application")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Set environment variables if not set
    if not os.getenv("SECRET_KEY"):
        os.environ["SECRET_KEY"] = "dev-secret-key-change-in-production"
        print("⚠️  Using default SECRET_KEY for development")
    
    # Import and run the app
    try:
        import uvicorn
        from main import app
        
        print("\n📝 Notes CRUD API is starting...")
        print("📖 API Documentation: http://localhost:8000/docs")
        print("🔄 Alternative docs: http://localhost:8000/redoc")
        print("💚 Health check: http://localhost:8000/health")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 50)
        
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
