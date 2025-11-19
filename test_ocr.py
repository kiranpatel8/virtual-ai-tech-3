"""
Test script for the OCR device information extraction function.
This script demonstrates how to use the extract_device_info_from_image function
directly without running the full API.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path to import from main.py
sys.path.insert(0, str(Path(__file__).parent))

def test_ocr_with_image(image_path: str):
    """
    Test the OCR function with a local image file
    
    Args:
        image_path: Path to the image file
    """
    from main import extract_device_info_from_image
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file not found: {image_path}")
        return
    
    print(f"📸 Testing OCR with image: {image_path}")
    print("=" * 60)
    
    # Read image file
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    # Extract device information
    result = extract_device_info_from_image(image_bytes)
    
    # Display results
    print("\n🔍 OCR Extraction Results:")
    print("-" * 60)
    print(f"Model Number:    {result['model_number'] or 'Not detected'}")
    print(f"Serial Number:   {result['serial_number'] or 'Not detected'}")
    print(f"Product Type:    {result['product_type']}")
    print(f"Confidence:      {result['confidence']:.1%}")
    print(f"Text Detections: {result['text_detections']}")
    
    if result.get('error'):
        print(f"\n⚠️  Error occurred: {result['error']}")
    
    if result['raw_text']:
        print("\n📝 All Detected Text:")
        print("-" * 60)
        for i, text in enumerate(result['raw_text'], 1):
            print(f"{i:2d}. {text}")
    else:
        print("\n⚠️  No text detected in the image")
    
    print("\n" + "=" * 60)

def main():
    """Main function to run OCR tests"""
    print("\n" + "=" * 60)
    print("OCR Device Information Extraction - Test Script")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUsage: python test_ocr.py <image_path>")
        print("\nExample:")
        print("  python test_ocr.py router_image.jpg")
        print("  python test_ocr.py ../test_images/modem.png")
        
        # Try to use one of the example images if available
        example_images = [
            "ionic-app/src/assets/images/frontier.jpg",
            "ionic-app/src/assets/images/technician_icon.jpg",
        ]
        
        found_example = None
        for img in example_images:
            if os.path.exists(img):
                found_example = img
                break
        
        if found_example:
            print(f"\n📸 Using example image: {found_example}")
            test_ocr_with_image(found_example)
        else:
            print("\n❌ No example images found. Please provide an image path.")
        
        return
    
    image_path = sys.argv[1]
    test_ocr_with_image(image_path)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

