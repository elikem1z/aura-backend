#!/usr/bin/env python3
"""
Test script for Google Gemini API connection.
This script makes a simple request to the Gemini API to validate your API key and connection.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Updated to use the correct Gemini API endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"


def test_gemini_api():
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found in environment variables or .env file.")
        return False

    print("🚀 Testing Google Gemini API connection...")
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [
            {"parts": [{"text": "Say hello from Gemini!"}]}
        ]
    }
    params = {
        "key": GEMINI_API_KEY
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        print("✅ Successfully connected to Gemini API!")
        print("Response snippet:")
        print(data)
        return True
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print("Response content:", e.response.text)
        return False

def main():
    success = test_gemini_api()
    if success:
        print("\n🎉 Gemini API connection test PASSED!")
    else:
        print("\n❌ Gemini API connection test FAILED. Check your API key and network connection.")
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 