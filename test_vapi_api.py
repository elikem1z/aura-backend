#!/usr/bin/env python3
"""
Test script for actual Vapi API calls.
This script makes real API calls to validate the connection works end-to-end.
"""

import os
import sys
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_list_assistants():
    """Test listing assistants - this should work with any valid API key."""
    try:
        from vapi import Vapi
        
        api_key = os.getenv('VAPI_API_KEY')
        if not api_key:
            print("❌ VAPI_API_KEY not found in environment variables")
            return False
        
        print("🔍 Testing: List Assistants API Call")
        print("-" * 40)
        
        vapi = Vapi(token=api_key)
        
        # This should return a list of your assistants (even if empty)
        response = vapi.assistants.list()
        
        print(f"✅ Successfully called Vapi API!")
        print(f"📊 Response type: {type(response)}")
        
        # Try to access the response data
        if hasattr(response, 'data'):
            assistants = response.data
            print(f"📋 Found {len(assistants)} assistant(s)")
            
            for i, assistant in enumerate(assistants):
                print(f"   {i+1}. {assistant.name} (ID: {assistant.id})")
        else:
            print("📋 Response structure: ", dir(response))
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to list assistants: {e}")
        return False

def test_list_phone_numbers():
    """Test listing phone numbers - another simple API call."""
    try:
        from vapi import Vapi
        
        api_key = os.getenv('VAPI_API_KEY')
        if not api_key:
            print("❌ VAPI_API_KEY not found in environment variables")
            return False
        
        print("\n🔍 Testing: List Phone Numbers API Call")
        print("-" * 40)
        
        vapi = Vapi(token=api_key)
        
        # This should return a list of your phone numbers
        response = vapi.phone_numbers.list()
        
        print(f"✅ Successfully called Phone Numbers API!")
        print(f"📊 Response type: {type(response)}")
        
        # Try to access the response data
        if hasattr(response, 'data'):
            phone_numbers = response.data
            print(f"📋 Found {len(phone_numbers)} phone number(s)")
            
            for i, phone in enumerate(phone_numbers):
                print(f"   {i+1}. {phone.phone_number} (ID: {phone.id})")
        else:
            print("📋 Response structure: ", dir(response))
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to list phone numbers: {e}")
        return False

def test_api_key_validation():
    """Test that the API key is valid by making a simple call."""
    try:
        from vapi import Vapi
        
        api_key = os.getenv('VAPI_API_KEY')
        if not api_key:
            print("❌ VAPI_API_KEY not found in environment variables")
            return False
        
        print("\n🔍 Testing: API Key Validation")
        print("-" * 40)
        
        vapi = Vapi(token=api_key)
        
        # Try to get account info or make a simple call
        # This will fail if the API key is invalid
        response = vapi.assistants.list()
        
        print("✅ API key is valid and working!")
        print(f"🔑 API key format: {api_key[:10]}...{api_key[-4:]}")
        
        return True
        
    except Exception as e:
        print(f"❌ API key validation failed: {e}")
        if "401" in str(e) or "unauthorized" in str(e).lower():
            print("   This suggests your API key might be invalid or expired.")
        elif "403" in str(e) or "forbidden" in str(e).lower():
            print("   This suggests your API key doesn't have the required permissions.")
        return False

def main():
    """Run all Vapi API call tests."""
    print("🚀 Starting Vapi API Call Tests")
    print("=" * 50)
    
    tests = [
        ("API Key Validation", test_api_key_validation),
        ("List Assistants", test_list_assistants),
        ("List Phone Numbers", test_list_phone_numbers),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API tests passed! Your Vapi integration is working perfectly.")
        print("\nNext steps:")
        print("1. Test Google Gemini API connection")
        print("2. Move to Phase II: Building the FastAPI server")
    elif passed >= 1:
        print("⚠️  Some tests passed, but there may be issues with your API key or permissions.")
        print("Check your Vapi dashboard for API key status and permissions.")
    else:
        print("❌ All API tests failed. Please check:")
        print("   - Your API key is correct and active")
        print("   - Your Vapi account has the necessary permissions")
        print("   - Your internet connection is working")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 