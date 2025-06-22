#!/usr/bin/env python3
"""
Test script to check Vapi TTS functionality with different API keys and endpoints.
"""

import asyncio
import requests
import os
import json

# Test both Vapi API keys
VAPI_API_KEYS = [
    'a021cf71-05a0-43a0-a5cb-9f34ec24974c',
    '5e337d2d-685f-41ed-84cb-cb9f71eb043a'
]

BASE_URL = "https://api.vapi.ai"

async def test_assistant_voice():
    """Test using assistant's voice capabilities for TTS."""
    print("\n🎤 Testing Assistant Voice Capabilities")
    print("=" * 50)
    
    # Use the working API key
    api_key = 'a021cf71-05a0-43a0-a5cb-9f34ec24974c'
    
    try:
        # First, get the assistant details
        url = f"{BASE_URL}/assistant"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            assistants = response.json()
            print(f"✅ Found {len(assistants)} assistants")
            
            for assistant in assistants:
                assistant_id = assistant.get('id')
                assistant_name = assistant.get('name')
                voice_config = assistant.get('voice', {})
                
                print(f"\n🤖 Assistant: {assistant_name} (ID: {assistant_id})")
                print(f"   Voice: {voice_config}")
                
                # Try to create a call with this assistant
                await test_assistant_call(api_key, assistant_id, assistant_name)
                
        else:
            print(f"❌ Failed to get assistants: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing assistant voice: {e}")

async def test_assistant_call(api_key, assistant_id, assistant_name):
    """Test creating a call with the assistant to test voice."""
    try:
        url = f"{BASE_URL}/call"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "assistantId": assistant_id,
            "phoneNumberId": None,  # We'll try without phone
            "customer": {
                "number": "+1234567890"  # Dummy number
            }
        }
        
        print(f"  📞 Testing call creation for {assistant_name}...")
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            call_data = response.json()
            call_id = call_data.get('id')
            print(f"  ✅ Call created: {call_id}")
            
            # Try to get call details
            await get_call_details(api_key, call_id)
            
        else:
            print(f"  ❌ Call creation failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"  ❌ Error creating call: {e}")

async def get_call_details(api_key, call_id):
    """Get details of a call."""
    try:
        url = f"{BASE_URL}/call/{call_id}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            call_details = response.json()
            print(f"    📋 Call status: {call_details.get('status')}")
            print(f"    🎤 Voice provider: {call_details.get('voice', {}).get('provider')}")
        else:
            print(f"    ❌ Failed to get call details: {response.status_code}")
            
    except Exception as e:
        print(f"    ❌ Error getting call details: {e}")

async def test_tts_endpoints():
    """Test different TTS endpoints with both API keys."""
    print("🎤 Testing Vapi TTS Endpoints")
    print("=" * 50)
    
    test_text = "Hello, this is a test of the text to speech functionality."
    
    # Try different Vapi TTS endpoints
    endpoints = [
        "/assistant/tts",
        "/tts", 
        "/audio/speech",
        "/v1/audio/speech",
        "/assistant/audio/speech",
        "/api/tts"
    ]
    
    for i, api_key in enumerate(VAPI_API_KEYS):
        print(f"\n🔑 Testing API Key {i+1}: {api_key[:8]}...")
        
        for endpoint in endpoints:
            try:
                url = f"{BASE_URL}{endpoint}"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                # Try different payload formats
                payloads = [
                    {
                        "text": test_text,
                        "voice": "alloy",
                        "model": "tts-1"
                    },
                    {
                        "input": test_text,
                        "voice": "alloy", 
                        "model": "tts-1",
                        "response_format": "mp3"
                    },
                    {
                        "text": test_text,
                        "voice": "alloy"
                    }
                ]
                
                for j, payload in enumerate(payloads):
                    try:
                        print(f"  🎤 Testing {endpoint} with payload {j+1}...")
                        response = requests.post(url, headers=headers, json=payload, timeout=10)
                        
                        if response.status_code == 200:
                            print(f"  ✅ SUCCESS! {endpoint} with payload {j+1}")
                            print(f"     Response size: {len(response.content)} bytes")
                            print(f"     Content-Type: {response.headers.get('content-type', 'unknown')}")
                            
                            # Save the audio file
                            filename = f"test_audio_key{i+1}_{endpoint.replace('/', '_')}_payload{j+1}.mp3"
                            with open(filename, "wb") as f:
                                f.write(response.content)
                            print(f"     Saved as: {filename}")
                            return True
                            
                        else:
                            print(f"  ❌ Failed: {response.status_code} - {response.text[:100]}")
                            
                    except Exception as e:
                        print(f"  ❌ Error with payload {j+1}: {e}")
                        continue
                        
            except Exception as e:
                print(f"  ❌ Error with endpoint {endpoint}: {e}")
                continue
    
    print("\n❌ No working TTS endpoint found")
    return False

async def test_vapi_assistant_endpoints():
    """Test Vapi assistant-related endpoints."""
    print("\n🤖 Testing Vapi Assistant Endpoints")
    print("=" * 50)
    
    for i, api_key in enumerate(VAPI_API_KEYS):
        print(f"\n🔑 Testing API Key {i+1}: {api_key[:8]}...")
        
        # Test assistant endpoints
        assistant_endpoints = [
            "/assistant",
            "/assistants", 
            "/assistant/tts",
            "/assistant/audio"
        ]
        
        for endpoint in assistant_endpoints:
            try:
                url = f"{BASE_URL}{endpoint}"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                # Try GET request first
                response = requests.get(url, headers=headers, timeout=10)
                print(f"  📡 GET {endpoint}: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"     Response: {response.text[:200]}...")
                    
            except Exception as e:
                print(f"  ❌ Error with {endpoint}: {e}")

if __name__ == "__main__":
    print("🚀 Starting Vapi TTS Tests")
    print("=" * 50)
    
    # Test TTS endpoints
    success = asyncio.run(test_tts_endpoints())
    
    # Test assistant endpoints
    asyncio.run(test_vapi_assistant_endpoints())
    
    # Test assistant voice capabilities
    asyncio.run(test_assistant_voice())
    
    if success:
        print("\n🎉 TTS test completed successfully!")
    else:
        print("\n💡 TTS test failed. Check the logs above for details.") 