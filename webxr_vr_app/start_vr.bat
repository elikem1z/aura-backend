@echo off
title Aura VR WebXR Server
color 0A

echo.
echo ========================================
echo    🎮 Aura VR WebXR Server
echo ========================================
echo.
echo 📋 Instructions:
echo 1. Make sure your FastAPI backend is running on port 8001
echo 2. Open your Meta Quest browser
echo 3. Navigate to: http://localhost:8080
echo 4. Click "Enter VR" to start the experience
echo.
echo 🛑 Press Ctrl+C to stop the server
echo.

python server.py

echo.
echo Server stopped. Press any key to exit...
pause >nul 