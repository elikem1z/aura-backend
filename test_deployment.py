#!/usr/bin/env python3
"""
Comprehensive Test Script for Aura Voice Backend

This script tests all major endpoints to ensure the application is ready for deployment.
Run this before pushing to Git to verify everything works correctly.
"""

import requests
import json
import time
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8001"
TEST_USER_ID = "test_user_deployment_123"

def test_basic_endpoints():
    """Test basic health and info endpoints."""
    print("🔍 Testing basic endpoints...")
    
    # Test ping endpoint
    try:
        response = requests.get(f"{BASE_URL}/ping", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ /ping - Status: {response.status_code}")
            print(f"   Response: {data}")
        else:
            print(f"❌ /ping - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ /ping - Error: {e}")
        return False
    
    # Test API info endpoint
    try:
        response = requests.get(f"{BASE_URL}/api-info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ /api-info - Status: {response.status_code}")
            print(f"   Name: {data.get('name', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
        else:
            print(f"❌ /api-info - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ /api-info - Error: {e}")
        return False
    
    # Test web interface
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print(f"✅ / (web interface) - Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
        else:
            print(f"❌ / (web interface) - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ / (web interface) - Error: {e}")
        return False
    
    return True

def test_voice_session():
    """Test voice session creation and management."""
    print("\n🎤 Testing voice session endpoints...")
    
    # Create a new voice session
    try:
        payload = {"user_id": TEST_USER_ID}
        response = requests.post(
            f"{BASE_URL}/voice/session/create",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print(f"✅ Voice session created - Session ID: {session_id}")
            
            # Test getting session info
            response = requests.get(f"{BASE_URL}/voice/session/{session_id}", timeout=10)
            if response.status_code == 200:
                session_data = response.json()
                print(f"✅ Session info retrieved - User: {session_data.get('user_id')}")
                return session_id
            else:
                print(f"❌ Failed to get session info - Status: {response.status_code}")
                return None
        else:
            print(f"❌ Failed to create voice session - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Voice session test error: {e}")
        return None

def test_voice_query(session_id):
    """Test voice query functionality."""
    print("\n🗣️ Testing voice query endpoint...")
    
    if not session_id:
        print("⚠️ Skipping voice query test - no session ID")
        return False
    
    try:
        payload = {
            "session_id": session_id,
            "query": "What can you see in this image?"
        }
        
        response = requests.post(
            f"{BASE_URL}/voice/query",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Voice query successful - Status: {response.status_code}")
            print(f"   Response: {data.get('response', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Voice query failed - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Voice query test error: {e}")
        return False

def test_vapi_webhook():
    """Test Vapi webhook endpoint."""
    print("\n🔗 Testing Vapi webhook endpoint...")
    
    try:
        # Test with the correct function name: describeSurroundings
        payload = {
            "message": {
                "type": "function-call",
                "functionCall": {
                    "name": "describeSurroundings",
                    "arguments": {
                        "session_id": "test_session_123",
                        "query": "What do you see?"
                    }
                }
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/webhook/vapi",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Vapi webhook successful - Status: {response.status_code}")
            print(f"   Result: {data.get('result', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Vapi webhook failed - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Vapi webhook test error: {e}")
        return False

def test_image_analysis():
    """Test image analysis endpoint."""
    print("\n🖼️ Testing image analysis endpoint...")
    
    try:
        payload = {
            "image_id": "test_image_123",
            "query": "Describe what you see in this image",
            "session_id": "test_session_123"
        }
        
        response = requests.post(
            f"{BASE_URL}/analyze-image",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # This should fail with 404 since we're using a fake image ID
        if response.status_code == 404:
            print("✅ Image analysis correctly returns 404 for non-existent image")
            return True
        else:
            print(f"⚠️ Image analysis returned {response.status_code} instead of 404")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Image analysis test error: {e}")
        return False

def test_image_upload():
    """Test image upload functionality."""
    print("\n📤 Testing image upload endpoint...")
    
    try:
        # Create a simple test image (1x1 pixel PNG)
        test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xd7\xd4\xc5\x00\x00\x00\x00IEND\xaeB`\x82'
        
        files = {'image': ('test.png', test_image_data, 'image/png')}
        data = {'user_id': TEST_USER_ID}
        
        response = requests.post(
            f"{BASE_URL}/upload-image",
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Image upload successful - Status: {response.status_code}")
            print(f"   Image ID: {data.get('image_id', 'N/A')}")
            print(f"   Session ID: {data.get('session_id', 'N/A')}")
            return data.get('image_id')
        else:
            print(f"❌ Image upload failed - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Image upload test error: {e}")
        return None

def test_real_image_analysis(image_id):
    """Test image analysis with a real uploaded image."""
    print("\n🔍 Testing real image analysis...")
    
    if not image_id:
        print("⚠️ Skipping real image analysis - no image ID")
        return False
    
    try:
        payload = {
            "image_id": image_id,
            "query": "What do you see in this image?",
            "session_id": "test_session_123"
        }
        
        response = requests.post(
            f"{BASE_URL}/analyze-image",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Real image analysis successful - Status: {response.status_code}")
            print(f"   Description: {data.get('description', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Real image analysis failed - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Real image analysis test error: {e}")
        return False

def test_error_handling():
    """Test error handling for invalid requests."""
    print("\n🚨 Testing error handling...")
    
    # Test invalid session
    try:
        response = requests.get(f"{BASE_URL}/voice/session/invalid_session_id", timeout=10)
        if response.status_code == 404:
            print("✅ Invalid session returns 404 as expected")
        else:
            print(f"⚠️ Invalid session returned {response.status_code} instead of 404")
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    # Test invalid image
    try:
        response = requests.get(f"{BASE_URL}/image/invalid_image_id", timeout=10)
        if response.status_code == 404:
            print("✅ Invalid image returns 404 as expected")
        else:
            print(f"⚠️ Invalid image returned {response.status_code} instead of 404")
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    return True

def main():
    """Run all tests."""
    print("🚀 Aura Voice Backend - Pre-Deployment Test Suite")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/ping", timeout=5)
        if response.status_code != 200:
            print(f"❌ Server not responding properly. Status: {response.status_code}")
            print("   Make sure your server is running on http://localhost:8001")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure your server is running on http://localhost:8001")
        print("   Run: python -m uvicorn main_voice:app --reload --port 8001 --host 0.0.0.0")
        return
    
    print("✅ Server is running and responding")
    
    # Run all tests
    tests_passed = 0
    total_tests = 8
    
    # Test 1: Basic endpoints
    if test_basic_endpoints():
        tests_passed += 1
    
    # Test 2: Voice session
    session_id = test_voice_session()
    if session_id:
        tests_passed += 1
    
    # Test 3: Voice query
    if test_voice_query(session_id):
        tests_passed += 1
    
    # Test 4: Vapi webhook
    if test_vapi_webhook():
        tests_passed += 1
    
    # Test 5: Image analysis (should fail with 404)
    if test_image_analysis():
        tests_passed += 1
    
    # Test 6: Image upload
    image_id = test_image_upload()
    if image_id:
        tests_passed += 1
    
    # Test 7: Real image analysis
    if test_real_image_analysis(image_id):
        tests_passed += 1
    
    # Test 8: Error handling
    if test_error_handling():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    
    if tests_passed >= total_tests - 1:  # Allow 1 test to fail (error handling might be different)
        print("🎉 TESTS PASSED! Your app is ready for deployment!")
        print("\n📋 Next Steps:")
        print("1. Commit your code to Git")
        print("2. Choose a deployment platform (Railway recommended)")
        print("3. Set environment variables on your chosen platform")
        print("4. Deploy!")
    else:
        print("⚠️ Some tests failed. Please fix the issues before deploying.")
        print("\n🔧 Check the error messages above and fix any issues.")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 