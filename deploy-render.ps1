# Render Deployment Helper Script for Aura Voice Backend
# This script helps you deploy to Render from the terminal

Write-Host "🚀 Aura Voice Backend - Render Deployment Helper" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

Write-Host ""
Write-Host "📋 Prerequisites Check:" -ForegroundColor Yellow
Write-Host "1. Make sure you have a GitHub account" -ForegroundColor White
Write-Host "2. Ensure your code is committed to a Git repository" -ForegroundColor White
Write-Host "3. Have your API keys ready" -ForegroundColor White

Write-Host ""
Write-Host "🔑 Your API Keys (already provided):" -ForegroundColor Yellow
Write-Host "GEMINI_API_KEY=AIzaSyAWBueMJ-xHJT0rdnOkB_0shALr6tcyxu4" -ForegroundColor Cyan
Write-Host "VAPI_API_KEY=a021cf71-05a0-43a0-a5cb-9f34ec24974c" -ForegroundColor Cyan
Write-Host "GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json" -ForegroundColor Cyan

Write-Host ""
Write-Host "🎯 Deployment Steps:" -ForegroundColor Yellow
Write-Host "1. Visit: https://render.com" -ForegroundColor White
Write-Host "2. Sign up with GitHub" -ForegroundColor White
Write-Host "3. Click 'New +' → 'Web Service'" -ForegroundColor White
Write-Host "4. Connect your GitHub repository (aura-backend)" -ForegroundColor White
Write-Host "5. Configure the service:" -ForegroundColor White
Write-Host "   - Name: aura-voice-backend" -ForegroundColor White
Write-Host "   - Environment: Python 3" -ForegroundColor White
Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor White
Write-Host "   - Start Command: uvicorn main_voice:app --host 0.0.0.0 --port `$PORT" -ForegroundColor White
Write-Host "6. Add Environment Variables in Render dashboard:" -ForegroundColor White
Write-Host "   - GEMINI_API_KEY=AIzaSyAWBueMJ-xHJT0rdnOkB_0shALr6tcyxu4" -ForegroundColor White
Write-Host "   - VAPI_API_KEY=a021cf71-05a0-43a0-a5cb-9f34ec24974c" -ForegroundColor White
Write-Host "   - GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json" -ForegroundColor White
Write-Host "7. Deploy!" -ForegroundColor White

Write-Host ""
Write-Host "📊 After Deployment:" -ForegroundColor Yellow
Write-Host "- Your app will be available at: https://your-app-name.onrender.com" -ForegroundColor White
Write-Host "- Update Vapi webhook to: https://your-app-name.onrender.com/webhook/vapi" -ForegroundColor White
Write-Host "- Test endpoints: /ping, /api-info, /" -ForegroundColor White

Write-Host ""
Write-Host "🔧 Alternative: Deploy via Render CLI" -ForegroundColor Yellow
Write-Host "If you prefer command line deployment:" -ForegroundColor White
Write-Host "1. Install Render CLI: npm install -g @render/cli" -ForegroundColor White
Write-Host "2. Login: render login" -ForegroundColor White
Write-Host "3. Deploy: render deploy" -ForegroundColor White

Write-Host ""
Write-Host "🎉 Ready to deploy!" -ForegroundColor Green
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 