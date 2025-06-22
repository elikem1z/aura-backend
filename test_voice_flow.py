#!/usr/bin/env python3
"""
Test Voice-First Architecture for Aura Vision Assistant

This script tests the complete voice-first flow:
1. Create voice session
2. Upload image
3. Process voice queries
4. Verify voice responses
"""

import os
import sys
import requests
import json
import base64
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_IMAGE_PATH = "test_image.jpg"  # Create a test image or use existing one

def create_test_image():
    """Create a simple test image if it doesn't exist."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple test image
        img = Image.new('RGB', (400, 300), color='white')
        draw = ImageDraw.Draw(img)
        
        # Add some text
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 50), "Test Image for Aura", fill='black', font=font)
        draw.text((50, 100), "This is a test image", fill='blue', font=font)
        draw.text((50, 150), "for voice analysis", fill='red', font=font)
        
        # Save the image
        img.save(TEST_IMAGE_PATH, "JPEG")
        print(f"✅ Created test image: {TEST_IMAGE_PATH}")
        return True
        
    except ImportError:
        print("⚠️  PIL not available, using existing test image")
        return False
    except Exception as e:
        print(f"❌ Error creating test image: {e}")
        return False

def test_server_health():
    """Test if the server is running and healthy."""
    try:
        response = requests.get(f"{BASE_URL}/ping", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server health check passed")
            print(f"   Voice enabled: {data.get('voice_enabled', False)}")
            print(f"   Gemini enabled: {data.get('gemini_enabled', False)}")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server health check error: {e}")
        return False

def test_create_voice_session():
    """Test creating a voice session."""
    try:
        user_id = f"test_user_{int(os.getpid())}"
        response = requests.post(
            f"{BASE_URL}/voice/session/create",
            data={"user_id": user_id},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            session_id = data.get("session_id")
            print(f"✅ Voice session created: {session_id}")
            return session_id
        else:
            print(f"❌ Failed to create voice session: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating voice session: {e}")
        return None

def test_upload_image(session_id: str):
    """Test uploading an image."""
    try:
        # Check if test image exists
        if not os.path.exists(TEST_IMAGE_PATH):
            if not create_test_image():
                print("⚠️  Using dummy image data for test")
                # Create dummy image data
                dummy_data = b"dummy_image_data"
                with open(TEST_IMAGE_PATH, "wb") as f:
                    f.write(dummy_data)
        
        # Upload the image
        with open(TEST_IMAGE_PATH, "rb") as f:
            files = {"image": f}
            data = {
                "user_id": f"test_user_{int(os.getpid())}",
                "session_id": session_id
            }
            
            response = requests.post(
                f"{BASE_URL}/upload-image",
                files=files,
                data=data,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            image_id = data.get("image_id")
            print(f"✅ Image uploaded: {image_id}")
            return image_id
        else:
            print(f"❌ Failed to upload image: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error uploading image: {e}")
        return None

def test_voice_query(session_id: str, query: str):
    """Test processing a voice query."""
    try:
        payload = {
            "session_id": session_id,
            "query": query
        }
        
        response = requests.post(
            f"{BASE_URL}/voice/query",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get("response")
            audio_url = data.get("audio_url")
            
            print(f"✅ Voice query processed: '{query}'")
            print(f"   Response: {response_text[:100]}...")
            if audio_url:
                print(f"   Audio URL: {audio_url}")
            else:
                print(f"   No audio generated (voice may be disabled)")
            
            return data
        else:
            print(f"❌ Failed to process voice query: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error processing voice query: {e}")
        return None

def test_analyze_image(image_id: str, session_id: str, query: str):
    """Test analyzing an image with voice output."""
    try:
        payload = {
            "image_id": image_id,
            "query": query,
            "session_id": session_id
        }
        
        response = requests.post(
            f"{BASE_URL}/analyze-image",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            description = data.get("description")
            audio_url = data.get("audio_url")
            
            print(f"✅ Image analysis completed")
            print(f"   Description: {description[:100]}...")
            if audio_url:
                print(f"   Audio URL: {audio_url}")
            else:
                print(f"   No audio generated")
            
            return data
        else:
            print(f"❌ Failed to analyze image: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error analyzing image: {e}")
        return None

def test_vapi_webhook():
    """Test Vapi webhook functionality."""
    try:
        # Test webhook with a function call
        payload = {
            "message": {
                "type": "function-call",
                "functionCall": {
                    "name": "describeSurroundings",
                    "arguments": {
                        "session_id": "test_session",
                        "query": "What do you see in this image?"
                    }
                }
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/webhook/vapi",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data.get("result")
            print(f"✅ Vapi webhook test passed")
            print(f"   Result: {result[:100]}...")
            return True
        else:
            print(f"❌ Vapi webhook test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Vapi webhook: {e}")
        return False

def test_session_management(session_id: str):
    """Test session management functionality."""
    try:
        response = requests.get(
            f"{BASE_URL}/voice/session/{session_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Session management test passed")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Images: {len(data.get('images', []))}")
            print(f"   Voice enabled: {data.get('voice_enabled')}")
            return True
        else:
            print(f"❌ Session management test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing session management: {e}")
        return False

def main():
    """Run the complete voice-first architecture test."""
    print("🚀 Testing Aura Voice-First Architecture")
    print("=" * 50)
    
    # Test 1: Server Health
    print("\n📋 Test 1: Server Health Check")
    if not test_server_health():
        print("❌ Server is not running. Please start the server first.")
        return False
    
    # Test 2: Create Voice Session
    print("\n📋 Test 2: Create Voice Session")
    session_id = test_create_voice_session()
    if not session_id:
        print("❌ Failed to create voice session")
        return False
    
    # Test 3: Upload Image
    print("\n📋 Test 3: Upload Image")
    image_id = test_upload_image(session_id)
    if not image_id:
        print("❌ Failed to upload image")
        return False
    
    # Test 4: Voice Query Processing
    print("\n📋 Test 4: Voice Query Processing")
    voice_queries = [
        "What do you see in this image?",
        "Describe the colors and objects",
        "Is there any text in the image?"
    ]
    
    for query in voice_queries:
        result = test_voice_query(session_id, query)
        if not result:
            print(f"❌ Failed to process voice query: {query}")
    
    # Test 5: Image Analysis with Voice
    print("\n📋 Test 5: Image Analysis with Voice Output")
    test_analyze_image(image_id, session_id, "What is the main content of this image?")
    
    # Test 6: Session Management
    print("\n📋 Test 6: Session Management")
    test_session_management(session_id)
    
    # Test 7: Vapi Webhook
    print("\n📋 Test 7: Vapi Webhook")
    test_vapi_webhook()
    
    print("\n" + "=" * 50)
    print("🎉 Voice-First Architecture Test Complete!")
    print("\nNext Steps:")
    print("1. Set up your VAPI_API_KEY and GEMINI_API_KEY in .env file")
    print("2. Configure Vapi assistant using vapi_config.json")
    print("3. Test with real voice interactions")
    print("4. Integrate with Quest app for mobile voice experience")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 