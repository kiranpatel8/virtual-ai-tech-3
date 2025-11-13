#!/usr/bin/env python3
"""
Test script for the Telecom Device Identifier API
"""

import requests
import json
import os
from pathlib import Path

# API configuration
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Health check passed: {data}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Root endpoint working: {data['message']}")
        return True
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_image_classification(image_path: str):
    """Test image classification endpoint"""
    print(f"Testing image classification with: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_BASE_URL}/identify", files=files)
        
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Classification successful!")
        print(f"   File: {data.get('filename')}")
        print(f"   Status: {data.get('status')}")
        
        if data.get('status') == 'success':
            top_pred = data.get('top_prediction', {})
            print(f"   Top prediction: {top_pred.get('label')} ({top_pred.get('score', 0):.2%} confidence)")
            
            # Show top 3 predictions
            predictions = data.get('predictions', [])[:3]
            print(f"   Top 3 predictions:")
            for i, pred in enumerate(predictions, 1):
                print(f"     {i}. {pred.get('label')} ({pred.get('score', 0):.2%})")
        else:
            print(f"   Message: {data.get('message', 'No message')}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"   Error details: {error_data.get('detail', 'No details')}")
            except:
                print(f"   Response text: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_invalid_file():
    """Test with invalid file"""
    print("Testing invalid file upload...")
    
    # Create a temporary text file
    test_file_path = "test_invalid.txt"
    with open(test_file_path, 'w') as f:
        f.write("This is not an image file")
    
    try:
        with open(test_file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_BASE_URL}/identify", files=files)
        
        # Should return 400 error
        if response.status_code == 400:
            print("✅ Invalid file correctly rejected")
            error_data = response.json()
            print(f"   Error message: {error_data.get('detail')}")
            result = True
        else:
            print(f"❌ Expected 400 error, got {response.status_code}")
            result = False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        result = False
    finally:
        # Clean up
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
    
    return result

def main():
    """Run all tests"""
    print("=" * 60)
    print("Telecom Device Identifier API - Test Suite")
    print("=" * 60)
    
    # Check if API is running
    try:
        requests.get(f"{API_BASE_URL}/", timeout=5)
    except requests.exceptions.RequestException:
        print(f"❌ API is not running at {API_BASE_URL}")
        print("Please start the API with: python main.py")
        return
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Invalid File Upload", test_invalid_file),
    ]
    
    # Look for sample images to test
    sample_images = []
    for ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
        for pattern in [f'*.{ext}', f'*.{ext.upper()}']:
            sample_images.extend(Path('.').glob(pattern))
    
    if sample_images:
        print(f"Found {len(sample_images)} sample image(s) to test")
        for img in sample_images[:3]:  # Test up to 3 images
            tests.append((f"Image Classification ({img.name})", lambda img=img: test_image_classification(str(img))))
    else:
        print("No sample images found. Create a .jpg or .png file in this directory to test image classification.")
    
    # Run tests
    results = []
    for test_name, test_func in tests:
        print(f"\n{'-' * 40}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n{'=' * 60}")
    print("TEST RESULTS SUMMARY")
    print(f"{'=' * 60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<30} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")

if __name__ == "__main__":
    main()
