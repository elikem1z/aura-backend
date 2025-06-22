# 🚀 RENDER DEPLOYMENT CHECKLIST

## Your API Keys (Copy these exactly):
```
GEMINI_API_KEY=AIzaSyAWBueMJ-xHJT0rdnOkB_0shALr6tcyxu4
VAPI_API_KEY=a021cf71-05a0-43a0-a5cb-9f34ec24974c
GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json
```

## Step-by-Step Deployment Instructions:

### 1. Sign Up/Login to Render
- ✅ Render website should be open in your browser
- Click "Get Started" or "Sign Up"
- Choose "Continue with GitHub"
- Authorize Render to access your GitHub account

### 2. Create New Web Service
- Click the **"New +"** button (top right)
- Select **"Web Service"**
- Click **"Connect a repository"**
- Find and select: **`elikem1z/aura-backend`**
- Click **"Connect"**

### 3. Configure the Service
Fill in these exact settings:

**Basic Settings:**
- **Name:** `aura-voice-backend`
- **Region:** Choose closest to you (US East recommended)
- **Branch:** `main`
- **Root Directory:** Leave empty (default)

**Build & Deploy Settings:**
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main_voice:app --host 0.0.0.0 --port $PORT`

### 4. Add Environment Variables
Click on **"Environment"** tab and add these variables:

| Variable Name | Value |
|---------------|-------|
| `GEMINI_API_KEY` | `AIzaSyAWBueMJ-xHJT0rdnOkB_0shALr6tcyxu4` |
| `VAPI_API_KEY` | `a021cf71-05a0-43a0-a5cb-9f34ec24974c` |
| `GOOGLE_APPLICATION_CREDENTIALS` | `google-credentials.json` |

### 5. Deploy
- Click **"Create Web Service"**
- Wait for deployment to complete (usually 2-3 minutes)
- You'll see build logs in real-time

### 6. Get Your App URL
After successful deployment, you'll get a URL like:
`https://aura-voice-backend.onrender.com`

## Testing Your Deployment

Once deployed, test these endpoints:

1. **Health Check:** `https://your-app-url/ping`
2. **API Info:** `https://your-app-url/api-info`
3. **Web Interface:** `https://your-app-url/`

## Update Vapi Webhook

After deployment, update your Vapi webhook URL to:
`https://your-app-url/webhook/vapi`

## Troubleshooting

If deployment fails:
1. Check the build logs for errors
2. Verify all environment variables are set correctly
3. Make sure the repository is public or you've authorized Render access

## Success Indicators

✅ Build completes without errors
✅ Health check returns: `{"message":"pong","voice_enabled":true,"gemini_enabled":true}`
✅ Web interface loads properly
✅ All API endpoints respond correctly

---

**Your app is ready for deployment! Follow the steps above and let me know if you encounter any issues.** 