#!/usr/bin/env python3
"""
Simple demo to show how the voice-first system works.
This will help you understand the workflow.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def demo_voice_workflow():
    """Demonstrate the complete voice workflow."""
    print("🎤 Aura Voice-First Demo")
    print("=" * 50)
    
    # Step 1: Create a voice session
    print("\n1️⃣ Creating voice session...")
    try:
        response = requests.post(
            f"{BASE_URL}/voice/session/create",
            data={"user_id": "demo_user"}
        )
        
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data["session_id"]
            print(f"✅ Voice session created: {session_id}")
            print(f"   Voice enabled: {session_data['voice_enabled']}")
        else:
            print(f"❌ Failed to create session: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Error creating session: {e}")
        return
    
    # Step 2: Upload a test image (if you have one)
    print("\n2️⃣ Uploading test image...")
    print("   Note: You'll need to upload an image through the web interface")
    print("   or provide an image file path here.")
    
    # For demo purposes, we'll use a placeholder image ID
    # In real usage, you'd upload an actual image
    image_id = "demo_image_123"
    print(f"   Using demo image ID: {image_id}")
    
    # Step 3: Analyze image with voice output
    print("\n3️⃣ Analyzing image with voice output...")
    try:
        payload = {
            "image_id": image_id,
            "query": "What do you see in this image? Please describe it in detail.",
            "session_id": session_id  # This enables voice output!
        }
        
        response = requests.post(
            f"{BASE_URL}/analyze-image",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis completed!")
            print(f"   Description: {result['description'][:100]}...")
            
            if result.get('audio_url'):
                print(f"   🎵 Audio generated: {result['audio_url']}")
                print("   The audio should auto-play in the web interface!")
            else:
                print("   ⚠️  No audio generated - check VAPI_API_KEY")
                
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error analyzing image: {e}")
    
    # Step 4: Show session info
    print("\n4️⃣ Session information:")
    try:
        response = requests.get(f"{BASE_URL}/voice/session/{session_id}")
        if response.status_code == 200:
            session_info = response.json()
            print(f"   Session ID: {session_info['session_id']}")
            print(f"   User ID: {session_info['user_id']}")
            print(f"   Voice Enabled: {session_info['voice_enabled']}")
            print(f"   Created: {session_info['created_at']}")
        else:
            print(f"   Could not retrieve session info: {response.status_code}")
    except Exception as e:
        print(f"   Error getting session info: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Key Points:")
    print("• Voice session MUST be created first")
    print("• Session ID enables TTS (Text-to-Speech)")
    print("• Without session ID, you only get text responses")
    print("• VAPI_API_KEY is required for voice features")
    print("• Web interface auto-fills IDs for convenience")

if __name__ == "__main__":
    demo_voice_workflow() 