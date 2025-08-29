# 🚀 Deployment Guide - FastAPI Notes CRUD API

## Quick Options for Interview Demo

### 🚇 Option 1: ngrok (Fastest - 2 minutes)

**Best for**: Immediate sharing, no setup required

1. **Install ngrok** (if not installed):
   ```bash
   # Download from https://ngrok.com/download
   # Or using chocolatey: choco install ngrok
   ```

2. **Get free ngrok account**:
   - Sign up at https://ngrok.com
   - Get your authtoken: `ngrok config add-authtoken YOUR_TOKEN`

3. **Start your API**:
   ```bash
   python main.py
   ```

4. **In another terminal, start ngrok**:
   ```bash
   ngrok http 8000
   ```

5. **Share the public URL** (e.g., `https://abc123.ngrok.io`)

**✅ Result**: Instant public URL like `https://random-id.ngrok.io`

---

### ☁️ Option 2: Railway (Free Cloud - 5 minutes)

**Best for**: Professional deployment, stays online

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "FastAPI Notes CRUD API"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to https://railway.app
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects and deploys!

3. **Set Environment Variables** (in Railway dashboard):
   - `SECRET_KEY`: `your-production-secret-key-here`

**✅ Result**: Professional URL like `https://your-app.railway.app`

---

### 🌐 Option 3: Render (Free Cloud - 5 minutes)

**Best for**: Free tier with custom domains

1. **Push to GitHub** (same as Railway)

2. **Deploy on Render**:
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`
     - **Environment**: `Python 3`

**✅ Result**: URL like `https://your-app.onrender.com`

---

## 📋 What to Share with Interviewer

Once deployed, share these links:

```
🔗 API Base URL: https://your-deployed-url.com
📖 API Documentation: https://your-deployed-url.com/docs
🔄 Alternative Docs: https://your-deployed-url.com/redoc
💚 Health Check: https://your-deployed-url.com/health
```

## 🧪 Quick API Demo

1. **Health Check**:
   ```bash
   curl https://your-url.com/health
   ```

2. **Register User**:
   ```bash
   curl -X POST "https://your-url.com/auth/register" \
        -H "Content-Type: application/json" \
        -d '{"username": "demo", "email": "demo@example.com", "password": "demo123"}'
   ```

3. **Login**:
   ```bash
   curl -X POST "https://your-url.com/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "demo", "password": "demo123"}'
   ```

4. **Create Note** (use token from login):
   ```bash
   curl -X POST "https://your-url.com/notes" \
        -H "Authorization: Bearer YOUR_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"title": "Interview Demo", "content": "This is a demo note for the interview"}'
   ```

## ⚡ Recommended: Use ngrok for Immediate Demo

If you need to demo **right now**:

1. Run the deployment script:
   ```bash
   python deploy.py
   ```

2. Select option 1 (ngrok)

3. Share the generated URL immediately!

## 🔒 Security Notes

- The app uses SQLite (file-based database)
- JWT tokens expire in 30 minutes
- Passwords are hashed with bcrypt
- Each user only sees their own notes

## 📱 Testing with Swagger UI

Once deployed, visit `https://your-url.com/docs` for interactive API testing directly in the browser!
