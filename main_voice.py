#!/usr/bin/env python3
"""
Aura Vision Assistant - Voice-First Version

A FastAPI server for image analysis with voice integration using Vapi and Google Gemini AI.
This version prioritizes voice interactions and text-to-speech responses.

Smart Architecture:
1. Voice Input via Vapi - Users speak questions about images
2. Image Analysis via Gemini - AI analyzes uploaded images
3. Voice Output via Vapi TTS - Results spoken back to user
4. Session Management - Track user sessions and images
5. Real-time Processing - Handle voice queries seamlessly

How to run:
$ uvicorn main_voice:app --reload

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
from pydantic import BaseModel
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

class CreateSessionRequest(BaseModel):
    user_id: str

# Global storage (in production, use Redis/database)
image_storage = {}

# API Keys from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
VAPI_API_KEY = os.getenv('VAPI_API_KEY')

if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY not found in environment variables or .env file")

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

async def process_query_with_gemini(query: str, image_id: Optional[str] = None) -> str:
    """
    Process a voice query with Gemini AI.
    If image_id is provided, analyze that specific image.
    Otherwise, provide a general response.
    """
    try:
        if image_id and image_id in image_storage:
            # Analyze specific image
            image_info = image_storage[image_id]
            return await analyze_image_with_gemini(image_info["data"], query)
        else:
            # General response without image
            return f"I understand you're asking: '{query}'. To help you with image analysis, please upload an image first and then ask your question."
            
    except Exception as e:
        print(f"❌ Error processing query with Gemini: {e}")
        return f"I'm sorry, I encountered an error processing your query: '{query}'. Please try again."

async def process_voice_query(request: VoiceQueryRequest) -> VoiceQueryResponse:
    """
    Process a voice query request and return response with TTS.
    """
    try:
        print(f"🎤 Processing voice query: {request.query}")
        
        # Get response from Gemini
        response_text = await process_query_with_gemini(request.query, request.image_id)
        
        # Try to generate TTS audio
        audio_url = None
        if voice_manager.is_voice_enabled():
            audio_url = await voice_manager.generate_tts(response_text)
            
        # If main TTS fails, try fallback
        if not audio_url:
            print("🔄 Trying fallback TTS...")
            audio_url = await voice_manager.generate_tts_fallback(response_text)
        
        return VoiceQueryResponse(
            response=response_text,
            audio_url=audio_url,
            session_id=request.session_id
        )
        
    except Exception as e:
        print(f"❌ Error processing voice query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping")
def ping():
    """Health check endpoint."""
    return JSONResponse(content={
        "message": "pong", 
        "voice_enabled": voice_manager.is_voice_enabled(),
        "gemini_enabled": bool(GEMINI_API_KEY)
    })

@app.post("/voice/query", response_model=VoiceQueryResponse)
async def voice_query(request: VoiceQueryRequest):
    """Process voice query and return response with TTS."""
    try:
        print(f"🎤 Processing voice query: {request.query}")
        
        # Get response from Gemini
        response_text = await process_query_with_gemini(request.query, request.image_id)
        
        # Try to generate TTS audio
        audio_url = None
        if voice_manager.is_voice_enabled():
            audio_url = await voice_manager.generate_tts(response_text)
            
        # If main TTS fails, try fallback
        if not audio_url:
            print("🔄 Trying fallback TTS...")
            audio_url = await voice_manager.generate_tts_fallback(response_text)
        
        return VoiceQueryResponse(
            response=response_text,
            audio_url=audio_url,
            session_id=request.session_id
        )
        
    except Exception as e:
        print(f"❌ Error processing voice query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/session/create")
async def create_voice_session(request: CreateSessionRequest):
    """Create a new voice-enabled session."""
    try:
        session_id = session_manager.create_session(request.user_id, voice_enabled=True)
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
                    voice_result = await process_voice_query(VoiceQueryRequest(
                        session_id=session_id,
                        query=query
                    ))
                    result = voice_result.response
                
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
                    session_manager.add_image_to_session(session_id, image_id)
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
        print(f"📤 UPLOAD REQUEST RECEIVED:")
        print(f"   - Filename: {image.filename}")
        print(f"   - Content-Type: {image.content_type}")
        print(f"   - User ID: {user_id}")
        print(f"   - Session ID: {session_id}")
        
        # Validate file type
        if not image.content_type.startswith('image/'):
            print(f"❌ Invalid file type: {image.content_type}")
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Generate unique image ID
        image_id = str(uuid.uuid4())
        print(f"   - Generated Image ID: {image_id}")
        
        # Read image data
        image_data = await image.read()
        print(f"   - Image size: {len(image_data)} bytes")
        
        # Create session if not provided
        if not session_id:
            session_id = session_manager.create_session(user_id, voice_enabled=True)
            print(f"   - Created new session: {session_id}")
        else:
            print(f"   - Using existing session: {session_id}")
        
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
        session_manager.add_image_to_session(session_id, image_id)
        
        print(f"✅ IMAGE UPLOAD SUCCESSFUL:")
        print(f"   - Image ID: {image_id}")
        print(f"   - Session ID: {session_id}")
        print(f"   - Total images in storage: {len(image_storage)}")
        
        return ImageUploadResponse(
            image_id=image_id,
            message="Image uploaded successfully. You can now ask questions about it via voice or text.",
            session_id=session_id
        )
        
    except Exception as e:
        print(f"❌ UPLOAD ERROR: {e}")
        print(f"   - Error type: {type(e).__name__}")
        import traceback
        print(f"   - Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-image", response_model=AnalyzeImageResponse)
async def analyze_image(request: AnalyzeImageRequest):
    """
    Analyze an image with a query.
    Enhanced to support voice output.
    """
    try:
        print(f"🔍 ANALYZE REQUEST RECEIVED:")
        print(f"   - Image ID: {request.image_id}")
        print(f"   - Query: {request.query}")
        print(f"   - Session ID: {request.session_id}")
        print(f"   - Total images in storage: {len(image_storage)}")
        print(f"   - Available image IDs: {list(image_storage.keys())}")
        
        # Get image data
        image_info = image_storage.get(request.image_id)
        if not image_info:
            print(f"❌ IMAGE NOT FOUND: {request.image_id}")
            print(f"   - Available images: {list(image_storage.keys())}")
            raise HTTPException(status_code=404, detail="Image not found")
        
        print(f"✅ IMAGE FOUND:")
        print(f"   - Filename: {image_info['filename']}")
        print(f"   - Size: {image_info['size']} bytes")
        print(f"   - Session: {image_info['session_id']}")
        
        # Update session activity if provided
        if request.session_id:
            session_manager.update_session_activity(request.session_id)
        
        # Analyze image
        description = await analyze_image_with_gemini(image_info["data"], request.query)
        
        # Generate audio if session is voice-enabled
        audio_url = None
        if request.session_id:
            session = session_manager.get_session(request.session_id)
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
        
        return AnalyzeImageResponse(
            description=description,
            image_id=request.image_id,
            audio_url=audio_url
        )
        
    except Exception as e:
        print(f"❌ ANALYZE ERROR: {e}")
        print(f"   - Error type: {type(e).__name__}")
        import traceback
        print(f"   - Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/image/{image_id}")
async def get_image(image_id: str):
    """Get image information."""
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
                            body: JSON.stringify({user_id: userId})
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
            "voice_input": voice_manager.is_voice_enabled(),
            "voice_output": voice_manager.is_voice_enabled(),
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
        "voice_enabled": voice_manager.is_voice_enabled(),
        "gemini_enabled": bool(GEMINI_API_KEY)
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 