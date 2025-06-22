#!/usr/bin/env python3
"""
Test script to check if the provided API key works with Google TTS.
"""

import requests
import base64
import os
import json
import uuid
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
TEST_API_KEY = os.getenv('GOOGLE_CLOUD_TTS_API_KEY')

if not TEST_API_KEY:
    print("❌ GOOGLE_CLOUD_TTS_API_KEY not found in environment variables")
    print("📝 Please add GOOGLE_CLOUD_TTS_API_KEY to your .env file")
    exit(1)

def test_tts_api():
    """Test the TTS API with the provided key."""
    print("🧪 Testing Google Cloud TTS API with provided key")
    print("=" * 50)
    
    url = "https://texttospeech.googleapis.com/v1/text:synthesize"
    
    # API key as query parameter (not Bearer token)
    params = {
        "key": TEST_API_KEY
    }
    
    # Request body according to Google Cloud TTS API schema
    data = {
        "input": {
            "text": "Hello, this is a test of the Google Cloud Text-to-Speech API."
        },
        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Standard-A",
            "ssmlGender": "NEUTRAL"
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": 1.0,
            "pitch": 0.0,
            "volumeGainDb": 0.0
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("📡 Making request to Google Cloud TTS API...")
        response = requests.post(url, headers=headers, params=params, json=data)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! API key works with TTS")
            
            # Try to save the audio
            try:
                audio_content = base64.b64decode(response.json()["audioContent"])
                
                # Ensure directory exists
                os.makedirs("static/audio", exist_ok=True)
                
                # Save test audio
                with open("static/audio/test_tts.mp3", "wb") as f:
                    f.write(audio_content)
                
                print("🎵 Test audio saved as: static/audio/test_tts.mp3")
                print("🎉 Your API key works! TTS is ready to use.")
                
            except Exception as e:
                print(f"⚠️  Could not save audio: {e}")
                
        elif response.status_code == 401:
            print("❌ UNAUTHORIZED: API key is invalid")
            print("💡 Check if the API key is correct")
            
        elif response.status_code == 403:
            print("❌ FORBIDDEN: API key doesn't have access to Text-to-Speech API")
            print("💡 You need to enable Text-to-Speech API in your Google Cloud project")
            
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_tts_api() 