@echo off
title Aura VR WebXR Server with Firewall Setup
color 0A

echo.
echo ========================================
echo    🎮 Aura VR WebXR Server Setup
echo ========================================
echo.

echo 🔧 Configuring Windows Firewall for port 8080...
netsh advfirewall firewall add rule name="Aura VR WebXR" dir=in action=allow protocol=TCP localport=8080

echo.
echo 🌐 Starting WebXR Server...
echo 📱 This will make the app accessible from other devices
echo.

cd /d "%~dp0"
python server.py

echo.
echo Server stopped. Press any key to exit...
pause >nul 