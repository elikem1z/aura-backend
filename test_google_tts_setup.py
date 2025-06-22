#!/usr/bin/env python3
"""
Test script for Google Cloud TTS setup and functionality.
"""

import asyncio
import os
from voice_manager import voice_manager

async def test_tts_setup():
    """Test the TTS setup and functionality."""
    print("🧪 Testing Google Cloud TTS Setup")
    print("=" * 50)
    
    # Test 1: Check if voice manager is initialized
    print("1. Voice Manager Status:")
    print(f"   Voice enabled: {voice_manager.is_voice_enabled()}")
    print(f"   Credentials path: {voice_manager.credentials_path}")
    print(f"   Project ID: {voice_manager.project_id}")
    
    # Test 2: Try TTS generation
    print("\n2. Testing TTS Generation:")
    test_text = "Hello! This is a test of the Google Cloud Text-to-Speech functionality."
    
    audio_url = await voice_manager.text_to_speech(test_text)
    
    if audio_url:
        print(f"   ✅ TTS generated successfully!")
        print(f"   📁 Audio file: {audio_url}")
        print(f"   📝 Check the file to see the TTS output")
    else:
        print("   ❌ TTS generation failed")
    
    # Test 3: Check if credentials file exists
    print("\n3. Credentials Check:")
    if os.path.exists(voice_manager.credentials_path):
        print(f"   ✅ Credentials file found: {voice_manager.credentials_path}")
        print("   🎉 You can now implement actual Google Cloud TTS!")
    else:
        print(f"   ⚠️  Credentials file not found: {voice_manager.credentials_path}")
        print("   📋 Follow the setup guide in GOOGLE_CLOUD_TTS_SETUP.md")
    
    # Test 4: Voice query processing
    print("\n4. Testing Voice Query Processing:")
    session_id = "test_session_123"
    query = "What do you see in this image?"
    
    result = await voice_manager.process_voice_query(session_id, query, None)
    
    print(f"   Session ID: {result['session_id']}")
    print(f"   Response: {result['response']}")
    print(f"   Audio URL: {result['audio_url']}")
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Follow GOOGLE_CLOUD_TTS_SETUP.md to set up Google Cloud TTS")
    print("2. Download your service account key as 'google-credentials.json'")
    print("3. Update the project_id in voice_manager.py")
    print("4. Replace the fallback TTS with actual Google Cloud TTS implementation")
    print("5. Test with your server: python -m uvicorn main_voice:app --reload")

if __name__ == "__main__":
    asyncio.run(test_tts_setup()) 