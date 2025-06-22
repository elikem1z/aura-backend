#!/usr/bin/env python3
"""
Deployment Helper Script for Aura Voice Backend

This script helps prepare your application for deployment by:
1. Validating environment variables
2. Testing API connections
3. Checking file structure
4. Providing deployment status
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

def check_environment():
    """Check if all required environment variables are set."""
    print("🔍 Checking environment variables...")
    
    load_dotenv()
    
    required_vars = [
        'GEMINI_API_KEY',
        'VAPI_API_KEY'
    ]
    
    optional_vars = [
        'GOOGLE_CLOUD_TTS_API_KEY'
    ]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        print("   Please set these in your .env file or deployment platform")
        return False
    
    if missing_optional:
        print(f"⚠️  Missing optional environment variables: {', '.join(missing_optional)}")
        print("   These are not required but recommended for full functionality")
    
    print("✅ All required environment variables are set")
    return True

def check_files():
    """Check if all required files exist for deployment."""
    print("\n📁 Checking deployment files...")
    
    required_files = [
        'main_voice.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt'
    ]
    
    optional_files = [
        'railway.json',
        'render.yaml'
    ]
    
    missing_required = []
    missing_optional = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_required.append(file)
    
    for file in optional_files:
        if not Path(file).exists():
            missing_optional.append(file)
    
    if missing_required:
        print(f"❌ Missing required files: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        print(f"⚠️  Missing optional files: {', '.join(missing_optional)}")
        print("   These are platform-specific deployment configs")
    
    print("✅ All required files are present")
    return True

def test_api_connections():
    """Test API connections to ensure keys are valid."""
    print("\n🔗 Testing API connections...")
    
    # Test Gemini API
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        try:
            # Simple test request to Gemini
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("✅ Gemini API connection successful")
            else:
                print(f"⚠️  Gemini API connection failed: {response.status_code}")
        except Exception as e:
            print(f"⚠️  Gemini API connection error: {e}")
    
    # Test Vapi API
    vapi_key = os.getenv('VAPI_API_KEY')
    if vapi_key:
        try:
            # Simple test request to Vapi
            url = "https://api.vapi.ai/assistant"
            headers = {"Authorization": f"Bearer {vapi_key}"}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code in [200, 401, 403]:  # 401/403 means key is valid but no access
                print("✅ Vapi API connection successful")
            else:
                print(f"⚠️  Vapi API connection failed: {response.status_code}")
        except Exception as e:
            print(f"⚠️  Vapi API connection error: {e}")

def check_dependencies():
    """Check if all dependencies are properly listed."""
    print("\n📦 Checking dependencies...")
    
    if not Path('requirements.txt').exists():
        print("❌ requirements.txt not found")
        return False
    
    # Read requirements and check for key dependencies
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    key_deps = [
        'fastapi',
        'uvicorn',
        'requests',
        'python-dotenv'
    ]
    
    missing_deps = []
    for dep in key_deps:
        if dep not in requirements:
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"⚠️  Missing key dependencies: {', '.join(missing_deps)}")
        print("   Consider adding these to requirements.txt")
    else:
        print("✅ Key dependencies are listed")
    
    return True

def deployment_status():
    """Show deployment readiness status."""
    print("\n" + "="*50)
    print("🚀 DEPLOYMENT READINESS CHECK")
    print("="*50)
    
    env_ok = check_environment()
    files_ok = check_files()
    deps_ok = check_dependencies()
    test_api_connections()
    
    print("\n" + "="*50)
    if env_ok and files_ok and deps_ok:
        print("✅ READY FOR DEPLOYMENT!")
        print("\n📋 Next Steps:")
        print("1. Commit your code to Git")
        print("2. Choose a deployment platform (Railway recommended)")
        print("3. Follow the instructions in DEPLOYMENT.md")
        print("4. Set environment variables on your chosen platform")
        print("5. Deploy!")
    else:
        print("❌ NOT READY FOR DEPLOYMENT")
        print("\n🔧 Please fix the issues above before deploying")
    
    print("="*50)

def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == '--check-only':
        deployment_status()
    else:
        print("Aura Voice Backend - Deployment Helper")
        print("Usage: python deploy.py [--check-only]")
        print("\nOptions:")
        print("  --check-only    Run deployment readiness check only")
        print("\nRunning full deployment check...")
        deployment_status()

if __name__ == "__main__":
    main() 