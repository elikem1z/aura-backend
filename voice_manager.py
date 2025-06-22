#!/usr/bin/env python3
"""
Voice Manager for Aura Vision Assistant

Handles:
- Text-to-Speech via Vapi
- Voice query processing
- Session management for voice interactions
"""

import os
import uuid
import requests
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

# Set API keys directly to avoid .env file encoding issues
os.environ['VAPI_API_KEY'] = 'a021cf71-05a0-43a0-a5cb-9f34ec24974c'
os.environ['GEMINI_API_KEY'] = 'AIzaSyAWBueMJ-xHJT0rdnOkB_0shALr6tcyxu4'

class VapiVoiceManager:
    """Manages Vapi voice interactions and TTS."""
    
    def __init__(self):
        self.api_key = os.getenv('VAPI_API_KEY')
        self.base_url = "https://api.vapi.ai"
        self.voice_enabled = bool(self.api_key)
    
    async def text_to_speech(self, text: str, voice: str = "alloy") -> Optional[str]:
        """Convert text to speech using Vapi TTS."""
        try:
            if not self.voice_enabled:
                print("⚠️  VAPI_API_KEY not set, skipping TTS")
                return None
            
            # Use Vapi's TTS endpoint - try different endpoints
            url = f"{self.base_url}/tts"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text,
                "voice": voice
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
    
    async def process_voice_query(self, session_id: str, query: str, image_analyzer_func) -> Dict[str, Any]:
        """Process a voice query and return response with audio."""
        try:
            # This will be called with the image analyzer function from main.py
            # For now, return a placeholder
            response_text = f"I received your voice query: '{query}' for session {session_id}. Image analysis will be integrated."
            
            # Generate audio response
            audio_url = await self.text_to_speech(response_text)
            
            return {
                "response": response_text,
                "audio_url": audio_url,
                "session_id": session_id,
                "image_id": None
            }
            
        except Exception as e:
            print(f"❌ Voice query processing error: {e}")
            return {
                "response": "I'm sorry, I encountered an error processing your voice query. Please try again.",
                "audio_url": None,
                "session_id": session_id,
                "image_id": None
            }
    
    def is_voice_enabled(self) -> bool:
        """Check if voice features are enabled."""
        return self.voice_enabled

# Global voice manager instance
voice_manager = VapiVoiceManager() 