#!/usr/bin/env python3
"""
Startup script for the Telecom Device Identifier API
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'requests',
        'Pillow',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_configuration():
    """Check if configuration is properly set up"""
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  No .env file found")
        print("Create a .env file with:")
        print("   HUGGINGFACE_API_TOKEN=your_token_here")
        print("   HUGGINGFACE_MODEL_ID=google/vit-base-patch16-224")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check Hugging Face token
    hf_token = os.getenv('HUGGINGFACE_API_TOKEN')
    if not hf_token:
        print("❌ HUGGINGFACE_API_TOKEN not set in .env file")
        return False
    
    if hf_token == "your_huggingface_api_token_here":
        print("❌ Please set a real Hugging Face API token in .env file")
        print("Get your token from: https://huggingface.co/settings/tokens")
        return False
    
    print("✅ Configuration looks good")
    return True

def start_server():
    """Start the API server"""
    print("Starting Telecom Device Identifier API...")
    
    try:
        from config import settings
        import uvicorn
        from main import app
        
        print(f"🚀 Starting server at http://{settings.API_HOST}:{settings.API_PORT}")
        print(f"📖 API documentation: http://{settings.API_HOST}:{settings.API_PORT}/docs")
        print(f"🔍 Model: {settings.HUGGINGFACE_MODEL_ID}")
        print("\nPress Ctrl+C to stop the server")
        
        uvicorn.run(
            app, 
            host=settings.API_HOST, 
            port=settings.API_PORT,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    print("=" * 60)
    print("Telecom Device Identifier API - Startup")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print()
    
    # Check configuration
    if not check_configuration():
        sys.exit(1)
    
    print()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
