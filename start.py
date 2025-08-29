#!/usr/bin/env python3
"""
Production startup script for Render deployment
"""
import os
import sys

def main():
    """Main startup function for production"""
    print("🚀 Starting FastAPI Notes CRUD API...")
    
    # Set default environment variables
    if not os.getenv("SECRET_KEY"):
        print("⚠️  No SECRET_KEY found in environment variables")
        sys.exit(1)
    
    # Import and create tables
    try:
        from database import create_tables
        print("📊 Creating database tables...")
        create_tables()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        sys.exit(1)
    
    # Start the application
    try:
        import uvicorn
        from main import app
        
        port = int(os.environ.get("PORT", 8000))
        print(f"🌐 Starting server on port {port}...")
        
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
