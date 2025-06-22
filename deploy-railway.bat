@echo off
echo 🚀 Aura Voice Backend - Railway Deployment Helper
echo ================================================

echo.
echo 📋 Prerequisites Check:
echo 1. Make sure you have a GitHub account
echo 2. Ensure your code is committed to a Git repository
echo 3. Have your API keys ready

echo.
echo 🔑 Required API Keys:
echo - GEMINI_API_KEY
echo - VAPI_API_KEY
echo - GOOGLE_CLOUD_TTS_API_KEY (optional)

echo.
echo 🎯 Deployment Steps:
echo 1. Visit: https://railway.app
echo 2. Sign up with GitHub
echo 3. Click "New Project"
echo 4. Select "Deploy from GitHub repo"
echo 5. Choose your repository (aura-backend)
echo 6. Add environment variables in Railway dashboard
echo 7. Deploy!

echo.
echo 🔧 Environment Variables to Set in Railway:
echo GEMINI_API_KEY=your_gemini_api_key_here
echo VAPI_API_KEY=your_vapi_api_key_here
echo GOOGLE_CLOUD_TTS_API_KEY=your_google_cloud_tts_api_key_here

echo.
echo 📊 After Deployment:
echo - Your app will be available at: https://your-app-name.railway.app
echo - Update Vapi webhook to: https://your-app-name.railway.app/webhook/vapi
echo - Test endpoints: /ping, /api-info, /

echo.
echo 🎉 Happy Deploying!
pause 