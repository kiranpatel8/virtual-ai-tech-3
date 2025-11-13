# Telecom Device Identifier API

A REST API service built with Python and FastAPI that identifies telecom devices from uploaded images using Hugging Face's machine learning models.

## Features

- **Image Upload**: Accept various image formats (JPEG, PNG, etc.)
- **Device Classification**: Identify telecom devices using pre-trained ML models
- **Error Handling**: Comprehensive validation and error responses
- **Auto Documentation**: Interactive API documentation with Swagger UI
- **Health Monitoring**: Health check endpoints for monitoring

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd telecom-device-identifier

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```bash
# Required: Your Hugging Face API token
HUGGINGFACE_API_TOKEN=your_huggingface_api_token_here

# Optional: Custom model (default: google/vit-base-patch16-224)
HUGGINGFACE_MODEL_ID=google/vit-base-patch16-224

# Optional: API configuration
API_HOST=0.0.0.0
API_PORT=8000
```

**Getting a Hugging Face API Token:**
1. Sign up at [huggingface.co](https://huggingface.co)
2. Go to Settings > Access Tokens
3. Create a new token with "Read" permissions
4. Copy the token to your `.env` file

### 3. Run the Service

```bash
# Start the API server
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### POST /identify

Upload an image to identify the telecom device.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Image file (max 10MB)

**Response:**
```json
{
  "filename": "router.jpg",
  "file_size": 245760,
  "model_used": "google/vit-base-patch16-224",
  "status": "success",
  "predictions": [
    {
      "label": "router",
      "score": 0.8945
    },
    {
      "label": "modem",
      "score": 0.0823
    }
  ],
  "top_prediction": {
    "label": "router",
    "score": 0.8945
  },
  "confidence": 0.8945
}
```

### GET /health

Check service health and configuration.

**Response:**
```json
{
  "status": "healthy",
  "service": "Telecom Device Identifier API",
  "huggingface_configured": true
}
```

### GET /

Get API information and available endpoints.

## Usage Examples

### Python Example

```python
import requests

# Upload and classify an image
url = "http://localhost:8000/identify"
files = {"file": open("telecom_device.jpg", "rb")}

response = requests.post(url, files=files)
result = response.json()

if result["status"] == "success":
    device_type = result["top_prediction"]["label"]
    confidence = result["confidence"]
    print(f"Detected device: {device_type} (confidence: {confidence:.2%})")
else:
    print(f"Classification failed: {result.get('message', 'Unknown error')}")
```

### cURL Example

```bash
# Upload an image for classification
curl -X POST "http://localhost:8000/identify" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@telecom_device.jpg"

# Health check
curl -X GET "http://localhost:8000/health"
```

### JavaScript/Fetch Example

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/identify', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        console.log('Device detected:', data.top_prediction.label);
        console.log('Confidence:', data.confidence);
    }
});
```

## Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- BMP
- TIFF
- WebP

## Image Requirements

- **Maximum file size**: 10MB
- **Maximum dimensions**: 1024x1024 pixels (images are automatically resized)
- **Format**: Any common image format (automatically converted to JPEG)

## Error Handling

The API provides detailed error responses:

```json
{
  "detail": "File must be an image (JPEG, PNG, etc.)"
}
```

Common error codes:
- `400`: Invalid file format or size
- `408`: Request timeout
- `500`: Internal server error
- `503`: Model loading (temporary)

## Model Information

### Default Model
- **Model**: `google/vit-base-patch16-224`
- **Type**: Vision Transformer
- **Description**: General-purpose image classifier

### Alternative Models

For better telecom device classification, you can configure alternative models:

```bash
# In your .env file
HUGGINGFACE_MODEL_ID=microsoft/DiT-base-distilled-patch16-224
```

Recommended models:
- `microsoft/DiT-base-distilled-patch16-224` - Data-efficient Image Transformer
- `facebook/convnext-base-224` - ConvNeXt model
- `microsoft/swin-base-patch4-window7-224` - Swin Transformer

## Development

### Project Structure

```
telecom-device-identifier/
├── main.py              # Main FastAPI application
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .env                # Environment variables (not in repo)
```

### Running in Development Mode

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

You can test the API using the interactive documentation at http://localhost:8000/docs or with any HTTP client.

## Deployment

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t telecom-device-api .
docker run -p 8000:8000 --env-file .env telecom-device-api
```

### Production Considerations

1. **Environment Variables**: Use proper secret management for API tokens
2. **Rate Limiting**: Implement rate limiting for production use
3. **Monitoring**: Add logging and monitoring
4. **Security**: Implement authentication if needed
5. **Scaling**: Use multiple workers with Gunicorn

## Troubleshooting

### Common Issues

1. **"Hugging Face API token not configured"**
   - Make sure you have `HUGGINGFACE_API_TOKEN` in your `.env` file
   - Verify the token is valid and has proper permissions

2. **"Model is currently loading"**
   - Hugging Face models need to warm up on first use
   - Wait a few moments and try again

3. **"File must be an image"**
   - Ensure you're uploading a valid image file
   - Check the file extension and content type

4. **Timeout errors**
   - Increase the timeout value in `config.py`
   - Check your internet connection

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the interactive API docs at `/docs`
3. Open an issue on GitHub
