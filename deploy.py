"""
Quick deployment script using ngrok for instant sharing
"""
import subprocess
import os
import sys
import time
import webbrowser

def check_ngrok():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ ngrok is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ ngrok not found. Please install ngrok:")
    print("1. Go to https://ngrok.com/download")
    print("2. Download and install ngrok")
    print("3. Sign up for a free account")
    print("4. Run: ngrok config add-authtoken YOUR_TOKEN")
    return False

def start_ngrok_tunnel():
    """Start ngrok tunnel"""
    if not check_ngrok():
        return None
    
    print("🚇 Starting ngrok tunnel...")
    
    # Start ngrok in background
    ngrok_process = subprocess.Popen(
        ['ngrok', 'http', '8000', '--log=stdout'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait a bit for ngrok to start
    time.sleep(3)
    
    # Get the public URL
    try:
        result = subprocess.run(['ngrok', 'api', 'tunnels'], capture_output=True, text=True)
        if 'public_url' in result.stdout:
            import json
            data = json.loads(result.stdout)
            if data.get('tunnels'):
                public_url = data['tunnels'][0]['public_url']
                return public_url, ngrok_process
    except:
        pass
    
    print("⏳ Ngrok is starting... Check http://localhost:4040 for the public URL")
    return "http://localhost:4040", ngrok_process

def main():
    """Main function"""
    print("🚀 FastAPI Notes API - Quick Deployment")
    print("=" * 50)
    
    print("\n📋 Deployment Options:")
    print("1. 🚇 ngrok (Instant tunnel - 2 minutes)")
    print("2. ☁️  Railway (Free cloud hosting - 5 minutes)")
    print("3. 🌐 Render (Free cloud hosting - 5 minutes)")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        print("\n🚇 Setting up ngrok tunnel...")
        result = start_ngrok_tunnel()
        if result:
            public_url, process = result
            print(f"\n✅ Your API is now accessible at: {public_url}")
            print(f"📖 API Documentation: {public_url}/docs")
            print(f"💚 Health Check: {public_url}/health")
            print("\n📋 Share these links with your interviewer!")
            print("\nPress Ctrl+C to stop the tunnel")
            
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n👋 Stopping tunnel...")
                process.terminate()
    
    elif choice == "2":
        print("\n☁️  Railway Deployment Instructions:")
        print("1. Go to https://railway.app")
        print("2. Sign up with GitHub")
        print("3. Click 'New Project' → 'Deploy from GitHub repo'")
        print("4. Select your repository")
        print("5. Railway will auto-deploy!")
        print("\n📁 Make sure to push these files to GitHub first:")
        print("   - Procfile")
        print("   - requirements.txt")
        print("   - runtime.txt")
        
    elif choice == "3":
        print("\n🌐 Render Deployment Instructions:")
        print("1. Go to https://render.com")
        print("2. Sign up with GitHub")
        print("3. Click 'New' → 'Web Service'")
        print("4. Connect your GitHub repository")
        print("5. Set build command: `pip install -r requirements.txt`")
        print("6. Set start command: `python main.py`")
        print("7. Deploy!")
    
    else:
        print("❌ Invalid option")

if __name__ == "__main__":
    main()
