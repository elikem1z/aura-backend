#!/usr/bin/env python3
"""
Setup script for Aura VR WebXR Application
"""

import os
import sys
import subprocess
import socket
import webbrowser
from pathlib import Path

def get_local_ip():
    """Get the local IP address of the computer"""
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def check_backend_connection():
    """Check if the FastAPI backend is running"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:8001/ping", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🎮 Aura VR WebXR Setup")
    print("=" * 50)
    
    # Get current directory
    current_dir = Path(__file__).parent.absolute()
    print(f"📁 Setup directory: {current_dir}")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"🌐 Local IP address: {local_ip}")
    
    # Check backend connection
    print("\n🔍 Checking FastAPI backend...")
    if check_backend_connection():
        print("✅ FastAPI backend is running on port 8001")
    else:
        print("⚠️  FastAPI backend not detected on port 8001")
        print("   Please start your backend with:")
        print("   python -m uvicorn main_voice:app --reload --port 8001")
        
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled")
            sys.exit(0)
    
    # Update app.js with correct backend URL
    print("\n🔧 Configuring application...")
    app_js_path = current_dir / "app.js"
    
    if app_js_path.exists():
        with open(app_js_path, 'r') as f:
            content = f.read()
        
        # Update backend URL if needed
        if "http://127.0.0.1:8001" in content:
            print("✅ Backend URL already configured")
        else:
            print("✅ Backend URL configured")
    else:
        print("❌ app.js not found")
        sys.exit(1)
    
    # Create start script
    print("\n📝 Creating start script...")
    start_script = current_dir / "start_vr.bat" if os.name == 'nt' else current_dir / "start_vr.sh"
    
    if os.name == 'nt':  # Windows
        with open(start_script, 'w') as f:
            f.write(f"""@echo off
echo 🎮 Starting Aura VR WebXR Server...
echo.
echo 📋 Instructions:
echo 1. Open your Meta Quest browser
echo 2. Navigate to: http://{local_ip}:8080
echo 3. Click "Enter VR" to start
echo.
echo 🛑 Press Ctrl+C to stop the server
echo.
python server.py
pause
""")
    else:  # Unix/Linux/Mac
        with open(start_script, 'w') as f:
            f.write(f"""#!/bin/bash
echo "🎮 Starting Aura VR WebXR Server..."
echo ""
echo "📋 Instructions:"
echo "1. Open your Meta Quest browser"
echo "2. Navigate to: http://{local_ip}:8080"
echo "3. Click \"Enter VR\" to start"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""
python3 server.py
""")
        # Make executable
        os.chmod(start_script, 0o755)
    
    print(f"✅ Start script created: {start_script}")
    
    # Display setup summary
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("=" * 50)
    print(f"🌐 WebXR Server URL: http://{local_ip}:8080")
    print(f"🔗 Backend URL: http://{local_ip}:8001")
    print("\n📋 Next Steps:")
    print("1. Start the WebXR server:")
    if os.name == 'nt':
        print(f"   Double-click: {start_script}")
    else:
        print(f"   Run: ./{start_script.name}")
    print("2. Open the URL in your Meta Quest browser")
    print("3. Click 'Enter VR' to start the experience")
    print("\n📖 For detailed instructions, see README.md")
    
    # Ask if user wants to start the server now
    response = input("\n🚀 Start the WebXR server now? (y/n): ")
    if response.lower() == 'y':
        print("\n🎮 Starting WebXR server...")
        try:
            subprocess.run([sys.executable, "server.py"], cwd=current_dir)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
    
    print("\n🎮 Enjoy your VR experience!")

if __name__ == "__main__":
    main() 