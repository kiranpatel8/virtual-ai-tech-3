# OCR Device Information Extraction Feature

## Overview
The API now includes automatic OCR (Optical Character Recognition) to extract device information from router, modem, and ONT images using EasyOCR.

## What It Extracts
- **Model Number**: Device model identifier (e.g., AC1900, WRT54G)
- **Serial Number**: Unique device serial number
- **Product Type**: Device category (Router, Modem, ONT, or Unknown)
- **Raw Text**: All text detected in the image
- **Confidence Score**: OCR accuracy confidence

## Installation

### 1. Install the new dependencies:
```bash
pip install -r requirements.txt
```

This will install:
- `easyocr==1.7.0` (OCR library)
- Additional dependencies: `numpy`, `torch`, `opencv-python-headless`

**Note**: First-time initialization of EasyOCR will download language models (~100MB for English).

### 2. Start the API:
```bash
python start_api.py
```

## API Response Format

When you POST an image to `/identify`, the response now includes a `device_info` field:

```json
{
  "filename": "router_image.jpg",
  "file_size": 123456,
  "model_used": "your-model-id",
  "status": "success",
  "predictions": [...],
  "device_info": {
    "model_number": "AC1900",
    "serial_number": "SN123456789",
    "product_type": "Router",
    "raw_text": ["MODEL", "AC1900", "S/N", "123456789", ...],
    "confidence": 0.95,
    "text_detections": 15
  }
}
```

## How It Works

### The `extract_device_info_from_image()` Function

```python
def extract_device_info_from_image(image_bytes: bytes) -> Dict[str, Any]
```

**Process:**
1. Converts image bytes to numpy array
2. Uses EasyOCR to detect and extract all text from the image
3. Analyzes extracted text to identify:
   - Product type (by keywords: "ONT", "MODEM", "ROUTER", etc.)
   - Model number (using regex patterns for common formats)
   - Serial number (looking for "S/N", "Serial", etc.)
4. Returns structured data with confidence scores

### Detection Patterns

**Product Type Detection:**
- ONT: Keywords like "ONT", "OPTICAL NETWORK TERMINAL", "FIBER"
- Modem: Keywords like "MODEM", "CABLE MODEM", "DSL"
- Router: Keywords like "ROUTER", "WIRELESS", "WI-FI", "WIFI"

**Model Number Patterns:**
- `MODEL: XXX` or `Model #: XXX`
- `P/N: XXX` (Part Number)
- Alphanumeric codes like `AC1900`, `WRT54G`, etc.

**Serial Number Patterns:**
- `S/N: XXX`
- `Serial: XXX` or `Serial #: XXX`
- `SN: XXX`

## Example Usage

### Using curl:
```bash
curl -X POST "http://localhost:8000/identify" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@router_label.jpg"
```

### Using Python requests:
```python
import requests

with open('router_image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/identify',
        files={'file': f}
    )
    
data = response.json()
device_info = data['device_info']

print(f"Model: {device_info['model_number']}")
print(f"Serial: {device_info['serial_number']}")
print(f"Type: {device_info['product_type']}")
```

### From the Ionic App:
The existing image upload functionality will automatically receive the new `device_info` field in the response.

## Performance Notes

- **First Call**: Takes longer (~5-10 seconds) due to EasyOCR model initialization
- **Subsequent Calls**: Much faster (~1-3 seconds) as the model is cached in memory
- **GPU Support**: Set `gpu=True` in the code if CUDA is available for better performance

## Troubleshooting

### EasyOCR Installation Issues:
If you encounter issues installing EasyOCR, try:
```bash
pip install --upgrade pip
pip install torch torchvision
pip install easyocr
```

### Memory Issues:
EasyOCR requires ~500MB of RAM. If running on limited resources, consider:
- Using a smaller image size
- Running on a machine with more RAM
- Using cloud-based OCR APIs as an alternative

## Customization

### Adding More Patterns:
Edit the `model_patterns` or `serial_patterns` lists in `extract_device_info_from_image()` to recognize additional formats.

### Supporting More Languages:
Change the EasyOCR reader initialization:
```python
_ocr_reader = easyocr.Reader(['en', 'es'], gpu=False)  # Add Spanish
```

### Adjusting Confidence Threshold:
Filter low-confidence results:
```python
if confidence > 0.7:  # Only accept high-confidence detections
    extracted_texts.append(text)
```

