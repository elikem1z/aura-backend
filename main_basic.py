#!/usr/bin/env python3
"""
Aura Vision Assistant - Basic Version (Pure Python)

A FastAPI server for image analysis with basic functionality.
This version uses only pure Python packages to avoid Rust compilation issues.

Features:
1. Image upload and storage
2. Basic text responses
3. Web interface
4. Session management (simplified)

How to run:
$ uvicorn main_basic:app --reload

Visit http://127.0.0.1:8000/ping to check if the server is running.
Visit http://127.0.0.1:8000/ to use the web interface.
"""

import os
import uuid
import json
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Aura Basic Vision Assistant", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Simple in-memory storage (for demo purposes)
sessions = {}
images = {}

def create_session(user_id: str) -> str:
    """Create a new session."""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "user_id": user_id,
        "created_at": datetime.now().isoformat(),
        "last_activity": datetime.now().isoformat(),
        "images": []
    }
    return session_id

def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Get session information."""
    return sessions.get(session_id)

def add_image_to_session(session_id: str, image_id: str):
    """Add image to session."""
    if session_id in sessions:
        sessions[session_id]["images"].append(image_id)
        sessions[session_id]["last_activity"] = datetime.now().isoformat()

def analyze_image_basic(image_id: str, query: str) -> str:
    """Basic image analysis (placeholder)."""
    if image_id not in images:
        return "Image not found."
    
    # Simple response based on query
    responses = {
        "what": "I can see an image that was uploaded. This is a basic analysis.",
        "describe": "The image appears to be a standard uploaded file. For detailed analysis, please use the full version with AI integration.",
        "analyze": "Basic analysis: Image detected and stored successfully.",
        "see": "I can see that an image has been uploaded to the system."
    }
    
    query_lower = query.lower()
    for key, response in responses.items():
        if key in query_lower:
            return response
    
    return "I can see an uploaded image. For detailed AI analysis, please use the full version with Gemini integration."

@app.get("/ping")
def ping():
    """Health check endpoint."""
    return JSONResponse(content={
        "message": "pong",
        "version": "1.0.0",
        "status": "basic_mode"
    })

@app.post("/session/create")
async def create_session_endpoint(user_id: str = Form(...)):
    """Create a new session."""
    try:
        session_id = create_session(user_id)
        return JSONResponse(content={
            "session_id": session_id,
            "message": "Session created successfully",
            "user_id": user_id
        })
    except Exception as e:
        print(f"❌ Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{session_id}")
async def get_session_endpoint(session_id: str):
    """Get session information."""
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return JSONResponse(content=session)

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
        
        # Store image info
        images[image_id] = {
            "path": image_path,
            "uploaded_at": datetime.now().isoformat(),
            "size": len(content)
        }
        
        # Update session if provided
        if session_id:
            add_image_to_session(session_id, image_id)
        
        return JSONResponse(content={
            "image_id": image_id,
            "message": "Image uploaded successfully",
            "session_id": session_id or "no_session",
            "size_bytes": len(content)
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
        if image_id not in images:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Basic analysis
        description = analyze_image_basic(image_id, query)
        
        print(f"✅ ANALYSIS COMPLETE:")
        print(f"   - Description: {description}")
        
        return JSONResponse(content={
            "description": description,
            "image_id": image_id,
            "analysis_type": "basic"
        })
        
    except Exception as e:
        print(f"❌ ANALYZE ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def web_interface():
    """Basic web interface."""
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aura Basic Vision Assistant</title>
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
        .status {
            text-align: center;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .status.success { background: #c6f6d5; color: #22543d; }
        .status.error { background: #fed7d7; color: #742a2a; }
        .status.warning { background: #fef5e7; color: #744210; }
        .info-box {
            background: #e6f3ff;
            border: 2px solid #63b3ed;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Aura Basic Vision Assistant</h1>
        
        <div class="info-box">
            <h3>ℹ️ Basic Mode</h3>
            <p>This is a simplified version for deployment testing. For full AI-powered analysis with voice capabilities, use the complete version.</p>
        </div>
        
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
            <h2>👤 Session Management</h2>
            <form id="sessionForm">
                <div class="form-group">
                    <label for="userId">User ID:</label>
                    <input type="text" id="userId" name="user_id" placeholder="Enter user ID" required>
                </div>
                <button type="submit">Create Session</button>
            </form>
            <div id="sessionResult"></div>
        </div>
    </div>

    <script>
        // Check server status on load
        window.onload = async function() {
            try {
                const response = await fetch('/ping');
                const data = await response.json();
                showStatus('Server is running! Version: ' + data.version + ' (' + data.status + ')', 'success');
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
            element.innerHTML = `
                <h4>Response:</h4>
                <p>${JSON.stringify(data, null, 2)}</p>
            `;
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
                const response = await fetch('/session/create', { method: 'POST', body: formData });
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
    </script>
</body>
</html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 