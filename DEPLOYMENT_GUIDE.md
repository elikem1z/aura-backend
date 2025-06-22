# Scripture Finder - HTTPS Deployment Guide

## 🚀 Free HTTPS Hosting on Render.com

This guide will help you deploy Scripture Finder with free HTTPS hosting on Render.com.

### Prerequisites
1. **GitHub Account**: To host your code
2. **Google AI Studio Account**: For Gemini API key
3. **Render.com Account**: For free hosting

## 📋 Step-by-Step Deployment

### Step 1: Get Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key (you'll need this later)

### Step 2: Push to GitHub
1. Create a new repository on GitHub
2. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit - Scripture Finder"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 3: Deploy on Render.com
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your GitHub account if not already connected
4. Select your repository
5. Configure the service:
   - **Name**: `scripture-finder`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python app.py`
6. Click "Create Web Service"

### Step 4: Set Environment Variables
1. In your Render dashboard, go to your service
2. Click "Environment" tab
3. Add these environment variables:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Your Gemini API key from Step 1
   - **Key**: `BIBLE_API_KEY`
   - **Value**: `a1692756d99fab00256e70dbda406cc7`
   - **Key**: `FLASK_ENV`
   - **Value**: `production`

### Step 5: Deploy and Test
1. Render will automatically deploy your app
2. Wait for the build to complete (usually 2-3 minutes)
3. Your app will be available at: `https://your-app-name.onrender.com`
4. Test the microphone feature - it should work with HTTPS!

## 🔧 Alternative Free HTTPS Hosting

### Railway.app
1. Go to [railway.app](https://railway.app)
2. Connect GitHub and select your repository
3. Railway automatically detects Python and deploys
4. Set environment variables in Railway dashboard
5. Get HTTPS URL automatically

### Vercel
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Configure as Python project
4. Set environment variables
5. Deploy with automatic HTTPS

## 🎯 Testing Your Deployment

### Test These Features:
1. **Basic Search**: Try searching for "John 3:16"
2. **Voice Input**: Click the MIC button and speak
3. **AI Analysis**: Ask complex questions (requires Gemini API key)
4. **Mobile Responsive**: Test on your phone

### Common Issues & Solutions:

**Microphone not working:**
- Ensure you're on HTTPS (should work automatically on Render)
- Check browser permissions
- Try refreshing the page

**"AI analysis not available":**
- Verify your Gemini API key is set correctly
- Check the environment variables in Render dashboard
- Restart the service if needed

**Build fails:**
- Check that all files are pushed to GitHub
- Verify `requirements.txt` is in the backend folder
- Check Render logs for specific errors

## 🔒 Security Notes

- Your API keys are stored securely in Render's environment variables
- HTTPS is automatically enabled on Render
- No sensitive data is stored in your code
- The Bible API key is public and safe to include

## 📱 Mobile Testing

Your app will work perfectly on mobile devices:
- Responsive design adapts to screen size
- Touch-friendly interface
- Voice recognition works on mobile browsers
- HTTPS ensures microphone access

## 🎉 Success!

Once deployed, you'll have:
- ✅ Free HTTPS hosting
- ✅ Working microphone features
- ✅ AI-powered Bible search
- ✅ Mobile-responsive design
- ✅ No server maintenance required

Your Scripture Finder is now live and ready to use! 🚀

---

**Need help?** Check the main README.md for troubleshooting tips. 