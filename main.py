#!/usr/bin/env python3
"""
Aura Backend - Voice-First Vision Assistant

Smart Architecture:
1. Voice Input via Vapi - Users speak questions about images
2. Image Analysis via Gemini - AI analyzes uploaded images
3. Voice Output via Vapi TTS - Results spoken back to user
4. Session Management - Track user sessions and images
5. Real-time Processing - Handle voice queries seamlessly

How to run:
$ uvicorn main:app --reload

Visit http://127.0.0.1:8000/ping to check if the server is running.
Visit http://127.0.0.1:8000/ to use the web interface.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import os
import uuid
import base64
import requests
import json
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our custom modules
from session_manager import SessionManager
from voice_manager import GoogleCloudTTSManager

app = FastAPI(title="Aura Voice-First Vision Assistant", description="Voice-powered image analysis with Vapi integration", version="2.0")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models for request/response
class VapiWebhookRequest(BaseModel):
    message: Dict[str, Any]

class VapiWebhookResponse(BaseModel):
    result: str

class VoiceQueryRequest(BaseModel):
    session_id: str
    query: str
    image_id: Optional[str] = None

class VoiceQueryResponse(BaseModel):
    response: str
    audio_url: Optional[str] = None
    session_id: str

class ImageUploadResponse(BaseModel):
    image_id: str
    message: str
    session_id: str

class AnalyzeImageRequest(BaseModel):
    image_id: str
    query: str
    session_id: Optional[str] = None

class AnalyzeImageResponse(BaseModel):
    description: str
    image_id: str
    audio_url: Optional[str] = None

class SessionInfo(BaseModel):
    session_id: str
    user_id: str
    created_at: datetime
    last_activity: datetime
    images: List[str]
    voice_enabled: bool

# Global storage (in production, use Redis/database)
image_storage = {}
session_storage = {}
active_websockets = []

# API Keys from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
VAPI_API_KEY = os.getenv('VAPI_API_KEY')

if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY not found in environment variables or .env file")

VAPI_API_URL = "https://api.vapi.ai"

class SessionManager:
    """Manages user sessions and voice interactions."""
    
    @staticmethod
    def create_session(user_id: str, voice_enabled: bool = True) -> str:
        """Create a new user session."""
        session_id = str(uuid.uuid4())
        session_storage[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "images": [],
            "voice_enabled": voice_enabled,
            "current_image": None
        }
        print(f"📱 Created session {session_id} for user {user_id}")
        return session_id
    
    @staticmethod
    def get_session(session_id: str) -> Optional[Dict]:
        """Get session information."""
        return session_storage.get(session_id)
    
    @staticmethod
    def update_session_activity(session_id: str):
        """Update session last activity."""
        if session_id in session_storage:
            session_storage[session_id]["last_activity"] = datetime.now()
    
    @staticmethod
    def add_image_to_session(session_id: str, image_id: str):
        """Add image to session."""
        if session_id in session_storage:
            session_storage[session_id]["images"].append(image_id)
            session_storage[session_id]["current_image"] = image_id
            print(f"📸 Added image {image_id} to session {session_id}")
    
    @staticmethod
    def get_current_image(session_id: str) -> Optional[str]:
        """Get current image for session."""
        session = session_storage.get(session_id)
        return session.get("current_image") if session else None

class VapiVoiceManager:
    """Manages Vapi voice interactions."""
    
    def __init__(self):
        self.api_key = VAPI_API_KEY
        self.base_url = VAPI_API_URL
    
    async def text_to_speech(self, text: str, voice: str = "alloy") -> Optional[str]:
        """Convert text to speech using Vapi TTS."""
        try:
            if not self.api_key:
                print("⚠️  VAPI_API_KEY not set, skipping TTS")
                return None
            
            # Vapi TTS endpoint
            url = f"{self.base_url}/audio/speech"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "tts-1",
                "input": text,
                "voice": voice,
                "response_format": "mp3"
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                # Save audio file and return URL
                audio_id = str(uuid.uuid4())
                audio_filename = f"static/audio/{audio_id}.mp3"
                os.makedirs("static/audio", exist_ok=True)
                
                with open(audio_filename, "wb") as f:
                    f.write(response.content)
                
                audio_url = f"/static/audio/{audio_id}.mp3"
                print(f"🎵 Generated TTS audio: {audio_url}")
                return audio_url
            else:
                print(f"❌ TTS failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ TTS error: {e}")
            return None
    
    async def process_voice_query(self, session_id: str, query: str) -> Dict[str, Any]:
        """Process a voice query and return response with audio."""
        try:
            # Get current image for session
            current_image = SessionManager.get_current_image(session_id)
            
            if not current_image:
                response_text = "I don't see any image in your current session. Please upload an image first, then ask me about it."
            else:
                # Analyze image with the voice query
                image_data = image_storage.get(current_image, {}).get("data")
                if image_data:
                    response_text = await analyze_image_with_gemini(image_data, query)
                else:
                    response_text = "I'm sorry, I couldn't find the image you're referring to. Please upload a new image."
            
            # Generate audio response
            audio_url = await self.text_to_speech(response_text)
            
            return {
                "response": response_text,
                "audio_url": audio_url,
                "session_id": session_id,
                "image_id": current_image
            }
            
        except Exception as e:
            print(f"❌ Voice query processing error: {e}")
            return {
                "response": "I'm sorry, I encountered an error processing your voice query. Please try again.",
                "audio_url": None,
                "session_id": session_id,
                "image_id": None
            }

# Initialize voice manager
voice_manager = VapiVoiceManager()

async def analyze_image_with_gemini(image_data: bytes, query: str) -> str:
    """
    Send image and query to Google Gemini API for analysis.
    Optimized for voice responses.
    """
    try:
        if not GEMINI_API_KEY:
            raise Exception("GEMINI_API_KEY not found in environment variables")
        
        # Encode image to base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Prepare the request payload for Gemini
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Please describe what you see in this image. The user is asking: '{query}'. Provide a clear, conversational description that would be helpful when spoken aloud. Keep it concise but informative, as this will be converted to speech."
                        },
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "topK": 32,
                "topP": 1,
                "maxOutputTokens": 1024,  # Shorter for voice
            }
        }
        
        headers = {
            "Content-Type": "application/json",
        }
        
        params = {
            "key": GEMINI_API_KEY
        }
        
        print(f"🔍 Analyzing image with voice query: '{query}'")
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
            headers=headers, params=params, json=payload, timeout=30
        )
        
        if response.status_code != 200:
            print(f"⚠️  Gemini API returned status {response.status_code}: {response.text}")
            return f"I can see you're asking about your surroundings. The image analysis service is currently having some issues, but I can help you with other questions. Your query was: '{query}'"
        
        data = response.json()
        
        # Extract the description from Gemini's response
        if 'candidates' in data and len(data['candidates']) > 0:
            candidate = data['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                parts = candidate['content']['parts']
                if len(parts) > 0 and 'text' in parts[0]:
                    description = parts[0]['text']
                    print(f"✅ Voice-optimized analysis complete: {len(description)} characters")
                    return description
        
        # Fallback if response structure is unexpected
        print(f"⚠️  Unexpected Gemini response structure: {data}")
        return "I can see the image, but I'm having trouble providing a detailed description right now."
        
    except Exception as e:
        print(f"❌ Error analyzing image with Gemini: {e}")
        return f"I can see you're asking about your surroundings. There was a temporary issue with the image analysis service. Your query was: '{query}'. Please try again in a moment."

@app.get("/ping")
def ping():
    """Health check endpoint."""
    return JSONResponse(content={"message": "pong", "voice_enabled": bool(VAPI_API_KEY)})

@app.post("/voice/query", response_model=VoiceQueryResponse)
async def process_voice_query(request: VoiceQueryRequest):
    """
    Process a voice query about an image.
    This is the main endpoint for voice interactions.
    """
    try:
        # Update session activity
        SessionManager.update_session_activity(request.session_id)
        
        # Process the voice query
        result = await voice_manager.process_voice_query(request.session_id, request.query)
        
        return VoiceQueryResponse(**result)
        
    except Exception as e:
        print(f"❌ Error processing voice query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/session/create")
async def create_voice_session(user_id: str = Form(...)):
    """Create a new voice-enabled session."""
    try:
        session_id = SessionManager.create_session(user_id, voice_enabled=True)
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
    try:
        session = SessionManager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return JSONResponse(content={
            "session_id": session_id,
            "user_id": session["user_id"],
            "created_at": session["created_at"].isoformat(),
            "last_activity": session["last_activity"].isoformat(),
            "images": session["images"],
            "current_image": session["current_image"],
            "voice_enabled": session["voice_enabled"]
        })
    except Exception as e:
        print(f"❌ Error getting voice session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook/vapi", response_model=VapiWebhookResponse)
async def vapi_webhook(request: VapiWebhookRequest):
    """
    Enhanced webhook endpoint for Vapi function calls.
    Handles voice interactions and image analysis requests.
    """
    try:
        message = request.message
        
        # Check if this is a function call
        if message.get("type") == "function-call":
            function_call = message.get("functionCall", {})
            function_name = function_call.get("name")
            arguments = function_call.get("arguments", {})
            
            print(f"🔔 Received Vapi function call: {function_name}")
            
            if function_name == "describeSurroundings":
                # Handle voice request to describe surroundings
                session_id = arguments.get("session_id")
                query = arguments.get("query", "What do you see in this image?")
                
                if not session_id:
                    result = "I need a session ID to help you with image analysis. Please start a new session first."
                else:
                    # Process the voice query
                    voice_result = await voice_manager.process_voice_query(session_id, query)
                    result = voice_result["response"]
                
                print(f"🎤 Voice function call handled: {function_name}")
                return VapiWebhookResponse(result=result)
            
            elif function_name == "uploadImage":
                # Handle voice request to upload image
                session_id = arguments.get("session_id")
                image_data = arguments.get("image_data")
                
                if session_id and image_data:
                    # Process image upload
                    image_id = str(uuid.uuid4())
                    image_storage[image_id] = {
                        "data": base64.b64decode(image_data),
                        "session_id": session_id,
                        "uploaded_at": datetime.now()
                    }
                    SessionManager.add_image_to_session(session_id, image_id)
                    result = f"Image uploaded successfully. You can now ask me questions about what you see."
                else:
                    result = "I need both a session ID and image data to upload an image."
                
                print(f"📸 Image upload function call handled: {function_name}")
                return VapiWebhookResponse(result=result)
            
            else:
                # Unknown function
                raise HTTPException(status_code=400, detail=f"Unknown function: {function_name}")
        
        else:
            # Not a function call, just acknowledge receipt
            print(f"📨 Received Vapi message type: {message.get('type', 'unknown')}")
            return VapiWebhookResponse(result="Message received")
            
    except Exception as e:
        print(f"❌ Error processing Vapi webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-image", response_model=ImageUploadResponse)
async def upload_image(
    image: UploadFile = File(...),
    user_id: str = Form(...),
    session_id: Optional[str] = Form(None)
):
    """
    Upload an image from the Quest app or voice interface.
    Enhanced to work with voice sessions.
    """
    try:
        # Validate file type
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Generate unique image ID
        image_id = str(uuid.uuid4())
        
        # Read image data
        image_data = await image.read()
        
        # Create session if not provided
        if not session_id:
            session_id = SessionManager.create_session(user_id, voice_enabled=True)
        
        # Store image data
        image_storage[image_id] = {
            "data": image_data,
            "filename": image.filename,
            "content_type": image.content_type,
            "user_id": user_id,
            "session_id": session_id,
            "size": len(image_data),
            "uploaded_at": datetime.now()
        }
        
        # Add image to session
        SessionManager.add_image_to_session(session_id, image_id)
        
        print(f"📸 Image uploaded: {image_id} ({len(image_data)} bytes) from user {user_id} in session {session_id}")
        
        return ImageUploadResponse(
            image_id=image_id,
            message="Image uploaded successfully. You can now ask questions about it via voice or text.",
            session_id=session_id
        )
        
    except Exception as e:
        print(f"❌ Error uploading image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-image", response_model=AnalyzeImageResponse)
async def analyze_image(request: AnalyzeImageRequest):
    """
    Analyze an image with a query.
    Enhanced to support voice output.
    """
    try:
        # Get image data
        image_info = image_storage.get(request.image_id)
        if not image_info:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Update session activity if provided
        if request.session_id:
            SessionManager.update_session_activity(request.session_id)
        
        # Analyze image
        description = await analyze_image_with_gemini(image_info["data"], request.query)
        
        # Generate audio if session is voice-enabled
        audio_url = None
        if request.session_id:
            session = SessionManager.get_session(request.session_id)
            if session and session.get("voice_enabled"):
                audio_url = await voice_manager.text_to_speech(description)
        
        return AnalyzeImageResponse(
            description=description,
            image_id=request.image_id,
            audio_url=audio_url
        )
        
    except Exception as e:
        print(f"❌ Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/image/{image_id}")
async def get_image(image_id: str):
    """Get image information."""
    try:
        image_info = image_storage.get(image_id)
        if not image_info:
            raise HTTPException(status_code=404, detail="Image not found")
    
        return JSONResponse(content={
            "image_id": image_id,
            "filename": image_info["filename"],
            "content_type": image_info["content_type"],
            "size": image_info["size"],
            "user_id": image_info["user_id"],
            "session_id": image_info["session_id"],
            "uploaded_at": image_info["uploaded_at"].isoformat()
        })
        
    except Exception as e:
        print(f"❌ Error getting image info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def web_interface():
    """Enhanced web interface with voice capabilities."""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Aura Voice-First Vision Assistant</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
                .voice-section { background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0; }
                .upload-section { background: #f3e5f5; padding: 15px; border-radius: 8px; margin: 20px 0; }
                button { background: #2196f3; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
                button:hover { background: #1976d2; }
                input, textarea { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px; }
                .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
                .success { background: #d4edda; color: #155724; }
                .error { background: #f8d7da; color: #721c24; }
            </style>
        </head>
            <body>
            <div class="container">
                <h1>🎤 Aura Voice-First Vision Assistant</h1>
                <p>Upload images and ask questions via voice or text!</p>
                
                <div class="voice-section">
                    <h2>🎙️ Voice Session</h2>
                    <button onclick="createVoiceSession()">Create Voice Session</button>
                    <div id="voiceStatus"></div>
                </div>
                
                <div class="upload-section">
                    <h2>📸 Upload Image</h2>
                    <input type="file" id="imageFile" accept="image/*">
                    <input type="text" id="userId" placeholder="User ID">
                    <input type="text" id="sessionId" placeholder="Session ID (optional)">
                    <button onclick="uploadImage()">Upload Image</button>
                    <div id="uploadStatus"></div>
                </div>
                
                <div class="upload-section">
                    <h2>🔍 Ask Questions</h2>
                    <input type="text" id="imageId" placeholder="Image ID">
                    <input type="text" id="sessionIdQuery" placeholder="Session ID (for voice)">
                    <textarea id="query" placeholder="Ask about the image..."></textarea>
                    <button onclick="analyzeImage()">Analyze Image</button>
                    <div id="analysisStatus"></div>
                </div>
            </div>
            
            <script>
                async function createVoiceSession() {
                    const userId = document.getElementById('userId').value || 'web_user_' + Date.now();
                    try {
                        const response = await fetch('/voice/session/create', {
                            method: 'POST',
                            body: new FormData([['user_id', userId]])
                        });
                        const data = await response.json();
                        document.getElementById('voiceStatus').innerHTML = 
                            `<div class="status success">Voice session created: ${data.session_id}</div>`;
                        document.getElementById('sessionId').value = data.session_id;
                    } catch (error) {
                        document.getElementById('voiceStatus').innerHTML = 
                            `<div class="status error">Error: ${error.message}</div>`;
                    }
                }
                
                async function uploadImage() {
                    const file = document.getElementById('imageFile').files[0];
                    const userId = document.getElementById('userId').value;
                    const sessionId = document.getElementById('sessionId').value;
                    
                    if (!file || !userId) {
                        document.getElementById('uploadStatus').innerHTML = 
                            `<div class="status error">Please select a file and enter user ID</div>`;
                        return;
                    }
                    
                    const formData = new FormData();
                    formData.append('image', file);
                    formData.append('user_id', userId);
                    if (sessionId) formData.append('session_id', sessionId);
                    
                    try {
                        const response = await fetch('/upload-image', {
                            method: 'POST',
                            body: formData
                        });
                        const data = await response.json();
                        document.getElementById('uploadStatus').innerHTML = 
                            `<div class="status success">Image uploaded: ${data.image_id}</div>`;
                        document.getElementById('imageId').value = data.image_id;
                        if (data.session_id) document.getElementById('sessionIdQuery').value = data.session_id;
                    } catch (error) {
                        document.getElementById('uploadStatus').innerHTML = 
                            `<div class="status error">Error: ${error.message}</div>`;
                    }
                }
                
                async function analyzeImage() {
                    const imageId = document.getElementById('imageId').value;
                    const sessionId = document.getElementById('sessionIdQuery').value;
                    const query = document.getElementById('query').value;
                    
                    if (!imageId || !query) {
                        document.getElementById('analysisStatus').innerHTML = 
                            `<div class="status error">Please enter image ID and query</div>`;
                        return;
                    }
                    
                    try {
                        const response = await fetch('/analyze-image', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({image_id: imageId, query: query, session_id: sessionId})
                        });
                        const data = await response.json();
                        let result = `<div class="status success"><strong>Analysis:</strong> ${data.description}</div>`;
                        if (data.audio_url) {
                            result += `<audio controls><source src="${data.audio_url}" type="audio/mpeg">Your browser does not support audio.</audio>`;
                        }
                        document.getElementById('analysisStatus').innerHTML = result;
                    } catch (error) {
                        document.getElementById('analysisStatus').innerHTML = 
                            `<div class="status error">Error: ${error.message}</div>`;
                    }
                }
            </script>
            </body>
        </html>
        """)

@app.get("/api-info")
def api_info():
    """Get API information including voice capabilities."""
    return JSONResponse(content={
        "name": "Aura Voice-First Vision Assistant",
        "version": "2.0",
        "description": "Voice-powered image analysis with Vapi integration",
        "features": {
            "voice_input": bool(VAPI_API_KEY),
            "voice_output": bool(VAPI_API_KEY),
            "image_analysis": bool(GEMINI_API_KEY),
            "session_management": True,
            "real_time_processing": True
        },
        "endpoints": {
            "voice": [
                "POST /voice/query - Process voice queries",
                "POST /voice/session/create - Create voice session",
                "GET /voice/session/{session_id} - Get session info"
            ],
            "images": [
                "POST /upload-image - Upload image",
                "POST /analyze-image - Analyze image",
                "GET /image/{image_id} - Get image info"
            ],
            "webhook": [
                "POST /webhook/vapi - Vapi webhook handler"
            ],
            "web": [
                "GET / - Web interface",
                "GET /ping - Health check",
                "GET /api-info - This endpoint"
            ]
        },
        "voice_enabled": bool(VAPI_API_KEY),
        "gemini_enabled": bool(GEMINI_API_KEY)
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
