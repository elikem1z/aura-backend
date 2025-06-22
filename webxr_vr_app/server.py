#!/usr/bin/env python3
"""
Simple HTTP server for serving the WebXR VR application
"""

import http.server
import socketserver
import os
import sys
import socket
from pathlib import Path

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def get_local_ip():
    """Get the local IP address of the computer"""
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Set up the server
    PORT = 8080
    HOST = "0.0.0.0"  # Bind to all network interfaces
    local_ip = get_local_ip()
    
    with socketserver.TCPServer((HOST, PORT), CORSHTTPRequestHandler) as httpd:
        print(f"🌐 WebXR Server running at http://localhost:{PORT}")
        print(f"📁 Serving files from: {script_dir}")
        print(f"🎮 Open http://{local_ip}:{PORT} in your Meta Quest browser")
        print(f"🔗 Network accessible at: http://{local_ip}:{PORT}")
        print("\n📋 Instructions:")
        print("1. Make sure your FastAPI backend is running on port 8001")
        print("2. Open this URL in your Meta Quest browser")
        print("3. Click 'Enter VR' to start the VR experience")
        print("4. Use the UI to capture screenshots and analyze images")
        print("\n🛑 Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            httpd.shutdown()

if __name__ == "__main__":
    main() 