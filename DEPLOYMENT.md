# 🚀 Deployment Guide for Aura Voice Backend

This guide will help you deploy your FastAPI application to various cloud platforms.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ All API keys ready (GEMINI_API_KEY, VAPI_API_KEY, GOOGLE_CLOUD_TTS_API_KEY)
- ✅ Your code committed to a Git repository
- ✅ A GitHub account (for most platforms)

## 🎯 Quick Deploy Options

### Option 1: Railway (Recommended - Fastest)

**Railway** is the fastest way to deploy with automatic HTTPS, custom domains, and a generous free tier.

#### Steps:
1. **Visit** [railway.app](https://railway.app) and sign up with GitHub
2. **Create New Project** → "Deploy from GitHub repo"
3. **Select your repository** (aura-backend)
4. **Add Environment Variables**:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   VAPI_API_KEY=your_vapi_api_key
   GOOGLE_CLOUD_TTS_API_KEY=your_google_cloud_tts_api_key
   ```
5. **Deploy** - Railway will automatically detect the `railway.json` config
6. **Get your URL** - Railway provides a URL like `https://your-app.railway.app`

#### Benefits:
- ⚡ Automatic deployment on git push
- 🔒 Free SSL certificates
- 🌍 Global CDN
- 📊 Built-in monitoring
- 💰 Generous free tier (500 hours/month)

---

### Option 2: Render

**Render** offers easy deployment with automatic HTTPS and custom domains.

#### Steps:
1. **Visit** [render.com](https://render.com) and sign up
2. **Create New** → "Web Service"
3. **Connect your GitHub repository**
4. **Configure**:
   - **Name**: `aura-voice-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main_voice:app --host 0.0.0.0 --port $PORT`
5. **Add Environment Variables**:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   VAPI_API_KEY=your_vapi_api_key
   GOOGLE_CLOUD_TTS_API_KEY=your_google_cloud_tts_api_key
   ```
6. **Deploy** - Render will use the `render.yaml` config

#### Benefits:
- 🆓 Free tier available
- 🔒 Automatic HTTPS
- 🚀 Easy scaling
- 📱 Good mobile app

---

### Option 3: Heroku

**Heroku** is a classic choice with good Python support.

#### Steps:
1. **Install Heroku CLI**:
   ```bash
   # Windows (with Chocolatey)
   choco install heroku
   
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Heroku app**:
   ```bash
   heroku create your-aura-app-name
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set GEMINI_API_KEY=your_gemini_api_key
   heroku config:set VAPI_API_KEY=your_vapi_api_key
   heroku config:set GOOGLE_CLOUD_TTS_API_KEY=your_google_cloud_tts_api_key
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

6. **Open your app**:
   ```bash
   heroku open
   ```

#### Benefits:
- 🏛️ Mature platform
- 🔧 Extensive add-ons
- 📚 Great documentation
- 🎯 Good for production

---

## 🔧 Environment Variables Setup

All platforms require these environment variables:

```bash
# Required for image analysis
GEMINI_API_KEY=your_gemini_api_key_here

# Required for voice integration
VAPI_API_KEY=your_vapi_api_key_here

# Optional: Google Cloud TTS (fallback)
GOOGLE_CLOUD_TTS_API_KEY=your_google_cloud_tts_api_key_here
```

## 🧪 Post-Deployment Testing

After deployment, test your endpoints:

1. **Health Check**: `https://your-app-url/ping`
2. **API Info**: `https://your-app-url/api-info`
3. **Web Interface**: `https://your-app-url/`

## 🔗 Update Vapi Webhook

Once deployed, update your Vapi webhook URL to:
```
https://your-app-url/webhook/vapi
```

## 📊 Monitoring Your Deployment

### Railway
- Dashboard: [railway.app/dashboard](https://railway.app/dashboard)
- Logs: Available in the Railway dashboard
- Metrics: Built-in monitoring

### Render
- Dashboard: [render.com/dashboard](https://render.com/dashboard)
- Logs: Available in the Render dashboard
- Health checks: Automatic monitoring

### Heroku
- Dashboard: [dashboard.heroku.com](https://dashboard.heroku.com)
- Logs: `heroku logs --tail`
- Monitoring: `heroku addons:create papertrail`

## 🚨 Troubleshooting

### Common Issues:

**"Application Error"**
- Check environment variables are set correctly
- Verify all API keys are valid
- Check logs for specific error messages

**"Build Failed"**
- Ensure `requirements.txt` is in the root directory
- Check Python version compatibility
- Verify all dependencies are listed

**"Port Issues"**
- Make sure your app uses `$PORT` environment variable
- Check the Procfile is correct

**"API Key Errors"**
- Verify all environment variables are set
- Test API keys locally first
- Check for typos in variable names

## 🔄 Continuous Deployment

### Railway & Render
- Automatic deployment on git push to main branch
- No additional setup required

### Heroku
```bash
# Enable automatic deploys
heroku pipelines:create
heroku pipelines:add your-pipeline-name
```

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans |
|----------|-----------|------------|
| Railway  | 500 hours/month | $5/month |
| Render   | 750 hours/month | $7/month |
| Heroku   | 550 hours/month | $7/month |

## 🎉 Next Steps

After successful deployment:

1. **Test all endpoints** with your deployed URL
2. **Update your Quest app** to use the new backend URL
3. **Configure Vapi webhook** to point to your deployed URL
4. **Set up monitoring** to track performance
5. **Consider custom domain** for production use

## 📞 Support

If you encounter issues:
- Check the platform's documentation
- Review the logs for error messages
- Test locally first to isolate issues
- Consider the troubleshooting section above

---

**Happy Deploying! 🚀** 