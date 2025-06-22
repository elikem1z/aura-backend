#!/usr/bin/env python3
"""
Test script for Vapi SDK connection validation.
This script tests basic functionality to ensure we can connect to Vapi services.
"""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_vapi_import():
    """Test that we can import the Vapi SDK successfully."""
    try:
        from vapi import Vapi
        print("✅ Successfully imported Vapi SDK")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Vapi SDK: {e}")
        return False

def test_vapi_initialization():
    """Test that we can initialize a Vapi client (without making actual API calls)."""
    try:
        from vapi import Vapi
        
        # Check if API key is available (we'll need this for actual operations)
        api_key = os.getenv('VAPI_API_KEY')
        if not api_key:
            print("⚠️  VAPI_API_KEY environment variable not set")
            print("   This is expected for initial testing, but you'll need it for actual API calls")
        
        # Try to create a Vapi instance (this won't make API calls yet)
        vapi = Vapi(token=api_key) if api_key else Vapi(token="test")
        print("✅ Successfully created Vapi client instance")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize Vapi client: {e}")
        return False

def test_basic_functionality():
    """Test basic Vapi functionality that doesn't require API calls."""
    try:
        from vapi import Vapi
        
        # Test that we can access basic attributes and methods
        vapi = Vapi(token="test")
        
        # Check if we can access the client attribute
        if hasattr(vapi, 'client'):
            print("✅ Vapi client has expected 'client' attribute")
        
        # Check if we can access common methods (these won't be called, just checked)
        expected_methods = ['assistants', 'calls', 'functions']
        for method in expected_methods:
            if hasattr(vapi, method):
                print(f"✅ Vapi client has '{method}' method available")
            else:
                print(f"⚠️  Vapi client missing '{method}' method")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test basic functionality: {e}")
        return False

def main():
    """Run all Vapi connection tests."""
    print("🚀 Starting Vapi SDK Connection Tests")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_vapi_import),
        ("Initialization Test", test_vapi_initialization),
        ("Basic Functionality Test", test_basic_functionality),
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
        print("🎉 All tests passed! Vapi SDK is ready to use.")
        print("\nNext steps:")
        print("1. Set your VAPI_API_KEY environment variable")
        print("2. Test actual API calls (if you have an API key)")
        print("3. Move to Phase II: Building the FastAPI server")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("Make sure you have the correct Vapi SDK version installed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 