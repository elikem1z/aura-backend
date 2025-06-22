#!/usr/bin/env python3
"""
Test script that uploads a real image and tests voice features.
"""

import requests
import os
import base64

BASE_URL = "http://127.0.0.1:8000"

def create_test_image():
    """Create a simple test image for testing."""
    # Create a simple 100x100 test image (red square)
    from PIL import Image, ImageDraw
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 80, 80], fill='blue')
    
    # Save it temporarily
    test_image_path = "test_image.png"
    img.save(test_image_path)
    return test_image_path

def test_complete_voice_workflow():
    """Test the complete voice workflow with a real image."""
    print("🎤 Testing Complete Voice Workflow")
    print("=" * 50)
    
    # Step 1: Create voice session
    print("\n1️⃣ Creating voice session...")
    try:
        response = requests.post(
            f"{BASE_URL}/voice/session/create",
            data={"user_id": "test_user"}
        )
        
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data["session_id"]
            print(f"✅ Voice session created: {session_id}")
        else:
            print(f"❌ Failed to create session: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Error creating session: {e}")
        return
    
    # Step 2: Create and upload test image
    print("\n2️⃣ Creating and uploading test image...")
    try:
        test_image_path = create_test_image()
        
        with open(test_image_path, 'rb') as f:
            files = {'image': f}
            data = {
                'user_id': 'test_user',
                'session_id': session_id
            }
            
            response = requests.post(
                f"{BASE_URL}/upload-image",
                files=files,
                data=data
            )
        
        if response.status_code == 200:
            upload_data = response.json()
            image_id = upload_data["image_id"]
            print(f"✅ Image uploaded: {image_id}")
        else:
            print(f"❌ Failed to upload image: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Error uploading image: {e}")
        return
    finally:
        # Clean up test image
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
    
    # Step 3: Analyze image with voice output
    print("\n3️⃣ Analyzing image with voice output...")
    try:
        payload = {
            "image_id": image_id,
            "query": "What do you see in this image? Please describe the colors and shapes.",
            "session_id": session_id
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
    
    print("\n" + "=" * 50)
    print("🎯 Test completed!")
    print("If you see audio generated, the voice features are working!")

if __name__ == "__main__":
    test_complete_voice_workflow() 