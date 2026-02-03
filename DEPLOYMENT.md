# Agentic Honey-Pot Deployment Guide

## 🚀 Quick Deploy to Railway (5 minutes)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Click "Login" → Sign up with GitHub
3. Authorize Railway

### Step 2: Deploy Your Project

#### Option A: Deploy from GitHub (Recommended)
1. Push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/honeypot-api.git
   git push -u origin main
   ```

2. In Railway:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Dockerfile and deploy

#### Option B: Deploy from Local (Faster)
1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Initialize and deploy:
   ```bash
   railway init
   railway up
   ```

### Step 3: Add Environment Variables

In Railway dashboard:
1. Go to your project → Variables
2. Add these variables:
   ```
   API_KEY=honeypot_secret_key_2026
   LLM_PROVIDER=gemini
   GOOGLE_API_KEY=your_gemini_api_key_here
   GUVI_CALLBACK_URL=https://hackathon.guvi.in/api/updateHoneyPotFinalResult
   MAX_CONVERSATION_TURNS=20
   SCAM_THRESHOLD=0.7
   ```

### Step 4: Get Your Public URL

1. Railway will generate a URL like: `https://honeypot-api-production-xxxx.up.railway.app`
2. Click "Settings" → "Generate Domain" if not auto-generated
3. Your endpoint will be: `https://your-app.railway.app/api/honeypot`

---

## 🧪 Test Your Deployed API

### Using GUVI Endpoint Tester

1. **Endpoint URL**: `https://your-app.railway.app/api/honeypot`
2. **API Key**: `honeypot_secret_key_2026`
3. **Header**: `x-api-key: honeypot_secret_key_2026`

### Using cURL

```bash
curl -X POST https://your-app.railway.app/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: honeypot_secret_key_2026" \
  -d '{
    "sessionId": "test-session-001",
    "message": {
      "sender": "scammer",
      "text": "Your bank account will be blocked. Verify immediately.",
      "timestamp": 1770005528731
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English",
      "locale": "IN"
    }
  }'
```

Expected Response:
```json
{
  "status": "success",
  "reply": "I'm very worried. What should I do exactly? Please guide me."
}
```

---

## 🔧 Alternative: Deploy to Render

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: honeypot-api
   - **Environment**: Docker
   - **Plan**: Free

### Step 3: Add Environment Variables
Same as Railway (see above)

### Step 4: Deploy
- Render will build and deploy automatically
- URL: `https://honeypot-api.onrender.com`

---

## 📝 Deployment Checklist

- [x] Dockerfile created
- [x] railway.json created
- [x] Procfile created
- [ ] Push code to GitHub (optional)
- [ ] Create Railway/Render account
- [ ] Deploy project
- [ ] Add environment variables
- [ ] Get public URL
- [ ] Test with GUVI endpoint tester

---

## ⚠️ Important Notes

1. **Environment Variables**: Make sure to add your Gemini API key in the deployment platform
2. **API Key**: Use the same API key (`honeypot_secret_key_2026`) or create a new one
3. **Free Tier Limits**: 
   - Railway: 500 hours/month
   - Render: May sleep after inactivity (takes 30s to wake up)

---

## 🆘 Troubleshooting

### Deployment fails
- Check logs in Railway/Render dashboard
- Verify all environment variables are set
- Ensure Dockerfile is correct

### API not responding
- Check if service is running in dashboard
- Verify the URL is correct
- Test health endpoint: `https://your-app.railway.app/`

### Authentication errors
- Verify `x-api-key` header is set correctly
- Check API_KEY environment variable matches

---

## 📞 Support

If you encounter issues:
1. Check deployment logs
2. Verify environment variables
3. Test locally first
4. Check Railway/Render status page
