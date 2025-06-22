#!/usr/bin/env python3
"""
Aura Backend - FastAPI Server

How to run:
$ uvicorn main:app --reload

Visit http://127.0.0.1:8000/ping to check if the server is running.
Visit http://127.0.0.1:8000/ to use the web interface.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
import uuid
import base64
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Aura Backend", description="Conversational Vision Assistant Backend", version="0.1")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models for request/response
class VapiWebhookRequest(BaseModel):
    message: Dict[str, Any]

class VapiWebhookResponse(BaseModel):
    result: str

class ImageUploadResponse(BaseModel):
    image_id: str
    message: str

class AnalyzeImageRequest(BaseModel):
    image_id: str
    query: str

class AnalyzeImageResponse(BaseModel):
    description: str
    image_id: str

# In-memory storage for images (in production, use a database)
image_storage = {}

# Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

async def analyze_image_with_gemini(image_data: bytes, query: str) -> str:
    """
    Send image and query to Google Gemini API for analysis.
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
                            "text": f"Please describe what you see in this image. The user is asking: '{query}'. Provide a detailed, helpful description that would be useful for someone who is visually impaired."
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
                "maxOutputTokens": 2048,
            }
        }
        
        headers = {
            "Content-Type": "application/json",
        }
        
        params = {
            "key": GEMINI_API_KEY
        }
        
        print(f"🔍 Sending image to Gemini API...")
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"⚠️  Gemini API returned status {response.status_code}: {response.text}")
            # Return a helpful fallback response
            return f"I can see you're asking about your surroundings. The image analysis service is currently having some issues, but I can help you with other questions. Your query was: '{query}'"
        
        data = response.json()
        
        # Extract the description from Gemini's response
        if 'candidates' in data and len(data['candidates']) > 0:
            candidate = data['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                parts = candidate['content']['parts']
                if len(parts) > 0 and 'text' in parts[0]:
                    description = parts[0]['text']
                    print(f"✅ Gemini analysis complete: {len(description)} characters")
                    return description
        
        # Fallback if response structure is unexpected
        print(f"⚠️  Unexpected Gemini response structure: {data}")
        return "I can see the image, but I'm having trouble providing a detailed description right now."
        
    except Exception as e:
        print(f"❌ Error analyzing image with Gemini: {e}")
        # Return a helpful fallback response instead of raising an exception
        return f"I can see you're asking about your surroundings. There was a temporary issue with the image analysis service. Your query was: '{query}'. Please try again in a moment."

@app.get("/ping")
def ping():
    """Health check endpoint."""
    return JSONResponse(content={"message": "pong"})

@app.post("/webhook/vapi", response_model=VapiWebhookResponse)
async def vapi_webhook(request: VapiWebhookRequest):
    """
    Webhook endpoint for Vapi function calls.
    This receives function calls from Vapi when users ask about their surroundings.
    """
    try:
        message = request.message
        
        # Check if this is a function call
        if message.get("type") == "function-call":
            function_call = message.get("functionCall", {})
            function_name = function_call.get("name")
            
            print(f"🔔 Received function call: {function_name}")
            
            if function_name == "describeSurroundings":
                # This is where we'll handle the describeSurroundings function
                # For now, we'll return a placeholder response
                result = "I can see you're asking about your surroundings. I'll need an image to provide a detailed description."
                
                print(f"📸 Function call handled: {function_name}")
                return VapiWebhookResponse(result=result)
            
            else:
                # Unknown function
                raise HTTPException(status_code=400, detail=f"Unknown function: {function_name}")
        
        else:
            # Not a function call, just acknowledge receipt
            print(f"📨 Received message type: {message.get('type', 'unknown')}")
            return VapiWebhookResponse(result="Message received")
            
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-image", response_model=ImageUploadResponse)
async def upload_image(
    image: UploadFile = File(...),
    user_id: str = Form(...),
    session_id: Optional[str] = Form(None)
):
    """
    Upload an image from the Quest app.
    This endpoint receives images when users ask about their surroundings.
    """
    try:
        # Validate file type
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Generate unique image ID
        image_id = str(uuid.uuid4())
        
        # Read image data
        image_data = await image.read()
        
        # Store image data (in production, save to disk/database)
        image_storage[image_id] = {
            "data": image_data,
            "filename": image.filename,
            "content_type": image.content_type,
            "user_id": user_id,
            "session_id": session_id,
            "size": len(image_data)
        }
        
        print(f"📸 Image uploaded: {image_id} ({len(image_data)} bytes) from user {user_id}")
        
        return ImageUploadResponse(
            image_id=image_id,
            message=f"Image uploaded successfully. Size: {len(image_data)} bytes"
        )
        
    except Exception as e:
        print(f"❌ Error uploading image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-image", response_model=AnalyzeImageResponse)
async def analyze_image(request: AnalyzeImageRequest):
    """
    Analyze an uploaded image with Google Gemini.
    This endpoint takes an image ID and query, then returns a description.
    """
    try:
        image_id = request.image_id
        query = request.query
        
        if image_id not in image_storage:
            raise HTTPException(status_code=404, detail="Image not found")
        
        image_info = image_storage[image_id]
        image_data = image_info["data"]
        
        print(f"🔍 Analyzing image {image_id} with query: '{query}'")
        
        # Send to Gemini for analysis
        description = await analyze_image_with_gemini(image_data, query)
        
        return AnalyzeImageResponse(
            description=description,
            image_id=image_id
        )
        
    except Exception as e:
        print(f"❌ Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/image/{image_id}")
async def get_image(image_id: str):
    """
    Retrieve an uploaded image by ID.
    """
    if image_id not in image_storage:
        raise HTTPException(status_code=404, detail="Image not found")
    
    image_info = image_storage[image_id]
    return {
        "image_id": image_id,
        "filename": image_info["filename"],
        "content_type": image_info["content_type"],
        "user_id": image_info["user_id"],
        "session_id": image_info["session_id"],
        "size": image_info["size"]
    }

@app.get("/", response_class=HTMLResponse)
async def web_interface():
    """Serve the web interface."""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
            <body>
                <h1>Aura Backend</h1>
                <p>Web interface not found. Please check that static/index.html exists.</p>
                <p><a href="/docs">API Documentation</a></p>
            </body>
        </html>
        """)

@app.get("/api-info")
def api_info():
    """Root endpoint with basic info."""
    return {
        "message": "Aura Backend is running!",
        "endpoints": {
            "web_interface": "/",
            "health_check": "/ping",
            "vapi_webhook": "/webhook/vapi",
            "upload_image": "/upload-image",
            "analyze_image": "/analyze-image",
            "get_image": "/image/{image_id}",
            "docs": "/docs"
        }
    }
