#!/usr/bin/env python3
"""
Aura Vision Assistant - Voice-First Version (Simplified for Deployment)

A FastAPI server for image analysis with voice integration using Vapi and Google Gemini AI.
This version avoids Pydantic to prevent Rust compilation issues on Render.

Smart Architecture:
1. Voice Input via Vapi - Users speak questions about images
2. Image Analysis via Gemini - AI analyzes uploaded images
3. Voice Output via Vapi TTS - Results spoken back to user
4. Session Management - Track user sessions and images
5. Real-time Processing - Handle voice queries seamlessly

How to run:
$ uvicorn main_voice_simple:app --reload

Visit http://127.0.0.1:8000/ping to check if the server is running.
Visit http://127.0.0.1:8000/ to use the web interface.
"""

import os
import uuid
import base64
import requests
from datetime import datetime
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

# Import our custom modules
from voice_manager import voice_manager
from session_manager import session_manager

# Initialize FastAPI app
app = FastAPI(title="Aura Voice-First Vision Assistant", version="2.0.0")

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Environment variables
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
GEMINI_API_KEY = os.getenv("GOOGLE_CLOUD_TTS_API_KEY")

# Initialize Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro-vision')
else:
    model = None

async def process_query_with_gemini(query: str, image_id: Optional[str] = None) -> str:
    """Process a query with Gemini AI."""
    try:
        if not model:
            return "Gemini AI is not configured. Please set GOOGLE_CLOUD_TTS_API_KEY."
        
        if not image_id:
            # Text-only query
            text_model = genai.GenerativeModel('gemini-pro')
            response = text_model.generate_content(query)
            return response.text
        
        # Image analysis query
        image_path = f"static/images/{image_id}.jpg"
        if not os.path.exists(image_path):
            return "Image not found. Please upload an image first."
        
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()
        
        response = model.generate_content([query, image_data])
        return response.text
        
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return f"Error processing query: {str(e)}"

@app.get("/ping")
def ping():
    """Health check endpoint."""
    return JSONResponse(content={
        "message": "pong", 
        "voice_enabled": voice_manager.is_voice_enabled(),
        "gemini_enabled": bool(GEMINI_API_KEY)
    })

@app.post("/voice/query")
async def voice_query(session_id: str = Form(...), query: str = Form(...), image_id: Optional[str] = Form(None)):
    """Process voice query and return response with TTS."""
    try:
        print(f"🎤 Processing voice query: {query}")
        
        # Get response from Gemini
        response_text = await process_query_with_gemini(query, image_id)
        
        # Try to generate TTS audio
        audio_url = None
        if voice_manager.is_voice_enabled():
            audio_url = await voice_manager.generate_tts(response_text)
            
        # If main TTS fails, try fallback
        if not audio_url:
            print("🔄 Trying fallback TTS...")
            audio_url = await voice_manager.generate_tts_fallback(response_text)
        
        return JSONResponse(content={
            "response": response_text,
            "audio_url": audio_url,
            "session_id": session_id
        })
        
    except Exception as e:
        print(f"❌ Error processing voice query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/session/create")
async def create_voice_session(user_id: str = Form(...)):
    """Create a new voice-enabled session."""
    try:
        session_id = session_manager.create_session(user_id, voice_enabled=True)
        return JSONResponse(content={
            "session_id": session_id,
            "message": "Voice session created successfully",
            "voice_enabled": True
        })
    except Exception as e:
        print(f"❌ Error creating voice session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/voice/session/{session_id}")
async def get_voice_session(session_id: str):
    """Get voice session information."""
    session_info = session_manager.get_session_info(session_id)
    if not session_info:
        raise HTTPException(status_code=404, detail="Session not found")
    return JSONResponse(content=session_info)

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...), session_id: Optional[str] = Form(None)):
    """Upload an image for analysis."""
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Generate unique image ID
        image_id = str(uuid.uuid4())
        image_path = f"static/images/{image_id}.jpg"
        
        # Ensure directory exists
        os.makedirs("static/images", exist_ok=True)
        
        # Save image
        with open(image_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Update session if provided
        if session_id:
            session_manager.add_image_to_session(session_id, image_id)
        
        return JSONResponse(content={
            "image_id": image_id,
            "message": "Image uploaded successfully",
            "session_id": session_id or "no_session"
        })
        
    except Exception as e:
        print(f"❌ Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-image")
async def analyze_image(image_id: str = Form(...), query: str = Form(...), session_id: Optional[str] = Form(None)):
    """Analyze an uploaded image with a query."""
    try:
        print(f"🔍 Analyzing image {image_id} with query: {query}")
        
        # Check if image exists
        image_path = f"static/images/{image_id}.jpg"
        if not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Analyze with Gemini
        description = await process_query_with_gemini(query, image_id)
        
        # Generate TTS if session has voice enabled
        audio_url = None
        if session_id:
            session = session_manager.get_session(session_id)
            if session and session.get("voice_enabled"):
                print("🎤 Generating TTS audio...")
                audio_url = await voice_manager.generate_tts(description)
                
                # If main TTS fails, try fallback
                if not audio_url:
                    print("🔄 Main TTS failed, trying fallback...")
                    audio_url = await voice_manager.generate_tts_fallback(description)
        
        print(f"✅ ANALYSIS COMPLETE:")
        print(f"   - Description length: {len(description)} characters")
        print(f"   - Audio URL: {audio_url}")
        
        return JSONResponse(content={
            "description": description,
            "image_id": image_id,
            "audio_url": audio_url
        })
        
    except Exception as e:
        print(f"❌ ANALYZE ERROR: {e}")
        print(f"   - Error type: {type(e).__name__}")
        import traceback
        print(f"   - Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def web_interface():
    """Enhanced web interface with voice capabilities."""
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aura Voice-First Vision Assistant</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #4a5568;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 2px solid #e2e8f0;
            border-radius: 15px;
            background: #f8fafc;
        }
        .section h2 {
            color: #2d3748;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #4a5568;
        }
        input[type="text"], input[type="file"], textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus, input[type="file"]:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #e6fffa;
            border: 2px solid #81e6d9;
            border-radius: 8px;
        }
        .error {
            background: #fed7d7;
            border-color: #fc8181;
        }
        .audio-player {
            margin-top: 10px;
        }
        .status {
            text-align: center;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .status.success { background: #c6f6d5; color: #22543d; }
        .status.error { background: #fed7d7; color: #742a2a; }
        .status.warning { background: #fef5e7; color: #744210; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎤 Aura Voice-First Vision Assistant</h1>
        
        <div id="status" class="status"></div>
        
        <div class="section">
            <h2>📸 Upload Image</h2>
            <form id="uploadForm">
                <div class="form-group">
                    <label for="imageFile">Select Image:</label>
                    <input type="file" id="imageFile" name="file" accept="image/*" required>
                </div>
                <div class="form-group">
                    <label for="sessionId">Session ID (optional):</label>
                    <input type="text" id="sessionId" name="session_id" placeholder="Enter session ID">
                </div>
                <button type="submit">Upload Image</button>
            </form>
            <div id="uploadResult"></div>
        </div>
        
        <div class="section">
            <h2>🔍 Analyze Image</h2>
            <form id="analyzeForm">
                <div class="form-group">
                    <label for="analyzeImageId">Image ID:</label>
                    <input type="text" id="analyzeImageId" name="image_id" placeholder="Enter image ID" required>
                </div>
                <div class="form-group">
                    <label for="analyzeQuery">Query:</label>
                    <textarea id="analyzeQuery" name="query" rows="3" placeholder="What would you like to know about this image?" required></textarea>
                </div>
                <div class="form-group">
                    <label for="analyzeSessionId">Session ID (optional):</label>
                    <input type="text" id="analyzeSessionId" name="session_id" placeholder="Enter session ID">
                </div>
                <button type="submit">Analyze Image</button>
            </form>
            <div id="analyzeResult"></div>
        </div>
        
        <div class="section">
            <h2>🎤 Voice Session</h2>
            <form id="sessionForm">
                <div class="form-group">
                    <label for="userId">User ID:</label>
                    <input type="text" id="userId" name="user_id" placeholder="Enter user ID" required>
                </div>
                <button type="submit">Create Voice Session</button>
            </form>
            <div id="sessionResult"></div>
        </div>
        
        <div class="section">
            <h2>🎵 Voice Query</h2>
            <form id="voiceForm">
                <div class="form-group">
                    <label for="voiceSessionId">Session ID:</label>
                    <input type="text" id="voiceSessionId" name="session_id" placeholder="Enter session ID" required>
                </div>
                <div class="form-group">
                    <label for="voiceQuery">Query:</label>
                    <textarea id="voiceQuery" name="query" rows="3" placeholder="What would you like to ask?" required></textarea>
                </div>
                <div class="form-group">
                    <label for="voiceImageId">Image ID (optional):</label>
                    <input type="text" id="voiceImageId" name="image_id" placeholder="Enter image ID">
                </div>
                <button type="submit">Process Voice Query</button>
            </form>
            <div id="voiceResult"></div>
        </div>
    </div>

    <script>
        // Check server status on load
        window.onload = async function() {
            try {
                const response = await fetch('/ping');
                const data = await response.json();
                showStatus('Server is running! Voice: ' + (data.voice_enabled ? 'Enabled' : 'Disabled') + ', Gemini: ' + (data.gemini_enabled ? 'Enabled' : 'Disabled'), 'success');
            } catch (error) {
                showStatus('Server connection failed: ' + error.message, 'error');
            }
        };

        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
        }

        function showResult(elementId, data, isError = false) {
            const element = document.getElementById(elementId);
            element.className = 'result' + (isError ? ' error' : '');
            
            if (data.audio_url) {
                element.innerHTML = `
                    <h4>Response:</h4>
                    <p>${data.response || data.description || JSON.stringify(data)}</p>
                    <div class="audio-player">
                        <audio controls>
                            <source src="${data.audio_url}" type="audio/mpeg">
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                `;
            } else {
                element.innerHTML = `
                    <h4>Response:</h4>
                    <p>${data.response || data.description || JSON.stringify(data)}</p>
                `;
            }
        }

        // Upload Image
        document.getElementById('uploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData();
            formData.append('file', document.getElementById('imageFile').files[0]);
            formData.append('session_id', document.getElementById('sessionId').value);
            
            try {
                const response = await fetch('/upload-image', { method: 'POST', body: formData });
                const data = await response.json();
                if (response.ok) {
                    showResult('uploadResult', data);
                } else {
                    showResult('uploadResult', data, true);
                }
            } catch (error) {
                showResult('uploadResult', { error: error.message }, true);
            }
        });

        // Analyze Image
        document.getElementById('analyzeForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData();
            formData.append('image_id', document.getElementById('analyzeImageId').value);
            formData.append('query', document.getElementById('analyzeQuery').value);
            formData.append('session_id', document.getElementById('analyzeSessionId').value);
            
            try {
                const response = await fetch('/analyze-image', { method: 'POST', body: formData });
                const data = await response.json();
                if (response.ok) {
                    showResult('analyzeResult', data);
                } else {
                    showResult('analyzeResult', data, true);
                }
            } catch (error) {
                showResult('analyzeResult', { error: error.message }, true);
            }
        });

        // Create Session
        document.getElementById('sessionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData();
            formData.append('user_id', document.getElementById('userId').value);
            
            try {
                const response = await fetch('/voice/session/create', { method: 'POST', body: formData });
                const data = await response.json();
                if (response.ok) {
                    showResult('sessionResult', data);
                } else {
                    showResult('sessionResult', data, true);
                }
            } catch (error) {
                showResult('sessionResult', { error: error.message }, true);
            }
        });

        // Voice Query
        document.getElementById('voiceForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData();
            formData.append('session_id', document.getElementById('voiceSessionId').value);
            formData.append('query', document.getElementById('voiceQuery').value);
            formData.append('image_id', document.getElementById('voiceImageId').value);
            
            try {
                const response = await fetch('/voice/query', { method: 'POST', body: formData });
                const data = await response.json();
                if (response.ok) {
                    showResult('voiceResult', data);
                } else {
                    showResult('voiceResult', data, true);
                }
            } catch (error) {
                showResult('voiceResult', { error: error.message }, true);
            }
        });
    </script>
</body>
</html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 