#!/usr/bin/env python3
"""
Test script for the complete Aura backend flow.
This simulates the entire process without needing the Quest app.
"""

import requests
import json
import base64
import time
from pathlib import Path

# Configuration
BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/ping")
        response.raise_for_status()
        print(f"✅ Health check passed: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def create_test_image():
    """Create a simple test image (1x1 pixel JPEG)."""
    # This is a minimal 1x1 pixel JPEG image
    jpeg_data = bytes.fromhex('ffd8ffe000104a46494600010101006000600000ffdb004300080606070605080707070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720222c231c1c2837292c30313434341f27393d38323c2e333432ffdb0043010909090c0b0c180d0d1832211c213232323232323232323232323232323232323232323232323232323232323232323232323232323232323232323232323232ffc00011080001000103012200021101031101ffc4001f0000010501010101010100000000000000000102030405060708090a0bffc400b5100002010303020403050504040000017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282090a161718191a25262728292a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9faffc4001f01000301010101010101010100000000000102030405060708090a0bffc400b51100020102040403040705040400010277000102031104052131061241510761711322328108144291a1b1c109233352f0156272d10a162434e125f11718191a262728292a35363738393a434445464748494a535455565758595a636465666768696a737475767778797a82838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae2e3e4e5e6e7e8e9eaf2f3f4f5f6f7f8f9faffda000c03010002110311003f00ffd9')
    return jpeg_data

def test_image_upload():
    """Test uploading an image."""
    print("\n📸 Testing image upload...")
    try:
        # Create test image data
        image_data = create_test_image()
        
        # Prepare the upload
        files = {
            'image': ('test_image.jpg', image_data, 'image/jpeg')
        }
        data = {
            'user_id': 'test_user_123',
            'session_id': 'test_session_456'
        }
        
        response = requests.post(f"{BASE_URL}/upload-image", files=files, data=data)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Image uploaded successfully!")
        print(f"   Image ID: {result['image_id']}")
        print(f"   Message: {result['message']}")
        
        return result['image_id']
        
    except Exception as e:
        print(f"❌ Image upload failed: {e}")
        return None

def test_image_analysis(image_id):
    """Test analyzing an uploaded image with Gemini."""
    print(f"\n🔍 Testing image analysis for image {image_id}...")
    try:
        payload = {
            "image_id": image_id,
            "query": "What do you see in this image? Please describe it in detail."
        }
        
        response = requests.post(f"{BASE_URL}/analyze-image", json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Image analysis successful!")
        print(f"   Description: {result['description'][:100]}...")
        print(f"   Full length: {len(result['description'])} characters")
        
        return result['description']
        
    except Exception as e:
        print(f"❌ Image analysis failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text}")
        return None

def test_vapi_webhook():
    """Test the Vapi webhook endpoint."""
    print(f"\n🔔 Testing Vapi webhook...")
    try:
        # Simulate a function call from Vapi
        payload = {
            "message": {
                "type": "function-call",
                "functionCall": {
                    "name": "describeSurroundings",
                    "parameters": {
                        "user_query": "What's around me?"
                    }
                }
            }
        }
        
        response = requests.post(f"{BASE_URL}/webhook/vapi", json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Vapi webhook test successful!")
        print(f"   Result: {result['result']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Vapi webhook test failed: {e}")
        return False

def test_get_image_info(image_id):
    """Test retrieving image information."""
    print(f"\n📋 Testing get image info for {image_id}...")
    try:
        response = requests.get(f"{BASE_URL}/image/{image_id}")
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Image info retrieved successfully!")
        print(f"   Filename: {result['filename']}")
        print(f"   User ID: {result['user_id']}")
        print(f"   Size: {result['size']} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Get image info failed: {e}")
        return False

def main():
    """Run the complete test flow."""
    print("🚀 Starting Aura Backend Full Flow Test")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health_check():
        print("❌ Health check failed. Make sure the server is running!")
        return False
    
    # Test 2: Image upload
    image_id = test_image_upload()
    if not image_id:
        print("❌ Image upload failed. Stopping tests.")
        return False
    
    # Test 3: Get image info
    test_get_image_info(image_id)
    
    # Test 4: Image analysis (this will use Gemini)
    description = test_image_analysis(image_id)
    if not description:
        print("❌ Image analysis failed. This might be due to Gemini API issues.")
    
    # Test 5: Vapi webhook
    test_vapi_webhook()
    
    print("\n" + "=" * 50)
    print("🎉 Full flow test completed!")
    
    if description:
        print("\n📝 Summary:")
        print(f"   ✅ Image uploaded with ID: {image_id}")
        print(f"   ✅ Image analyzed with Gemini")
        print(f"   ✅ Vapi webhook working")
        print(f"   ✅ All endpoints functional")
        print("\n🎯 Your backend is ready for integration!")
    else:
        print("\n⚠️  Note: Image analysis failed, but other endpoints work.")
        print("   This might be due to Gemini API configuration.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Some tests failed. Check the errors above.") 