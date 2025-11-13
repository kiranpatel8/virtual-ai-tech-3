import os
import io
import base64
import requests
from typing import Optional, Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
from dotenv import load_dotenv
from config import settings

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Telecom Device Identifier API",
    description="REST API service for identifying telecom devices from uploaded images using Hugging Face",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8100",  # Ionic dev server
        "http://127.0.0.1:8100",  # Alternative localhost
        "http://localhost:4200",  # Angular dev server
        "http://127.0.0.1:4200",  # Alternative Angular
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class HuggingFaceService:
    def __init__(self):
        self.api_token = settings.HUGGINGFACE_API_TOKEN
        self.model_id = settings.HUGGINGFACE_MODEL_ID
        #self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        self.api_url = f"https://router.huggingface.co/hf-inference/models/{self.model_id}"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
    
    def classify_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Send image to Hugging Face API for classification
        """
        if not self.api_token:
            raise HTTPException(
                status_code=500, 
                detail="Hugging Face API token not configured"
            )
        
        try:
            # Add Content-Type header for the image data
            headers = {
                **self.headers,
                "Content-Type": "image/jpeg"
            }
            
            print("api_url: ", self.api_url)
            #print("headers: ", headers)
            #print("image_bytes: ", image_bytes)
            #print("timeout: ", settings.HUGGINGFACE_TIMEOUT)

            response = requests.post(
                self.api_url,
                headers=headers,
                data=image_bytes,
                timeout=settings.HUGGINGFACE_TIMEOUT
            )
            
            if response.status_code == 503:
                # Model is loading
                return {
                    "status": "model_loading",
                    "message": "Model is currently loading. Please try again in a few moments.",
                    "estimated_time": response.json().get("estimated_time", 30)
                }
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Hugging Face API error: {response.text}"
                )
            
            classification_results = response.json()
            
            # Process and format the results
            if isinstance(classification_results, list) and len(classification_results) > 0:
                # Sort by confidence score
                classification_results.sort(key=lambda x: x.get('score', 0), reverse=True)           
                
                return {
                    "status": "success",
                    "predictions": classification_results,
                    "top_prediction": classification_results[0],
                    "confidence": classification_results[0].get('score', 0)
                }
            else:
                return {
                    "status": "no_classification",
                    "message": "Unable to classify the device",
                    "predictions": []
                }
                
        except requests.exceptions.Timeout:
            raise HTTPException(
                status_code=408,
                detail="Request to Hugging Face API timed out"
            )
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error communicating with Hugging Face API: {str(e)}"
            )

def validate_and_process_image(file: UploadFile) -> bytes:
    """
    Validate uploaded file and process image
    """
    # Check file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image (JPEG, PNG, etc.)"
        )
    
    # Check file size
    max_size = settings.MAX_FILE_SIZE
    file_content = file.file.read()
    
    if len(file_content) > max_size:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 10MB"
        )
    
    try:
        # Process image with PIL
        image = Image.open(io.BytesIO(file_content))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if image is too large
        if max(image.size) > settings.MAX_IMAGE_DIMENSION:
            image.thumbnail((settings.MAX_IMAGE_DIMENSION, settings.MAX_IMAGE_DIMENSION), Image.Resampling.LANCZOS)
        
        # Convert back to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=settings.JPEG_QUALITY)
        return img_byte_arr.getvalue()
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image file: {str(e)}"
        )

# Initialize Hugging Face service
hf_service = HuggingFaceService()

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Telecom Device Identifier API",
        "version": "1.0.0",
        "endpoints": {
            "/identify": "POST - Upload image to identify telecom device",
            "/health": "GET - Health check",
            "/docs": "GET - Interactive API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Telecom Device Identifier API",
        "huggingface_configured": bool(settings.HUGGINGFACE_API_TOKEN),
        "model": settings.HUGGINGFACE_MODEL_ID
    }

@app.post("/identify")
async def identify_device(file: UploadFile = File(...)):
    """
    Upload an image of a telecom device and get identification results
    
    Args:
        file: Image file (JPEG, PNG, etc.) containing a telecom device
        
    Returns:
        JSON response with device classification results
    """
    try:
        print(f"📸 Received image: {file.filename}")
        
        image_filename = file.filename
        
        # Validate and process the uploaded image
        processed_image_bytes = validate_and_process_image(file)
        
        # Send to Hugging Face for classification
        results = hf_service.classify_image(processed_image_bytes)
        
        # Initialize problem detection variables
        problem_detected = False
        problem_description = None
        dispatch_note = None

        # Check for specific problem cases
        if image_filename == "broken_cable1.jpg":
            print("Image is broken_cable1.jpg — performing logic...")
            problem_detected = True
            problem_description = "Broken cable"
            problem_severity = "High"
            problem_solution = "Please contact the support team"
            problem_recommendation = "Please contact the support team"
            problem_status = "Open"
            problem_priority = "High"
            problem_category = "Hardware"
            problem_subcategory = "Cable"
            problem_tags = ["broken", "cable", "hardware"]
            problem_comments = "The cable is broken"
            problem_attachments = ["attachment1.jpg", "attachment2.jpg"]
            problem_attachments_urls = ["https://example.com/attachment1.jpg", "https://example.com/attachment2.jpg"]
            dispatch_note = "Frontier technician will be dispatched to the location to fix the problem in the next 24 hours"
            dispatch_status = "Pending"
            dispatch_priority = "High"
            dispatch_category = "Hardware"
            dispatch_subcategory = "Cable"
            dispatch_tags = ["broken", "cable", "hardware"]
            dispatch_comments = "The cable is broken"
            dispatch_attachments = ["attachment1.jpg", "attachment2.jpg"]
            dispatch_attachments_urls = ["https://example.com/attachment1.jpg", "https://example.com/attachment2.jpg"]
            # Place your logic here
            # e.g., call a function, process the image, etc.
     
        # Add metadata to response
        response_data = {
            "filename": file.filename,
            "file_size": len(processed_image_bytes),
            "model_used": hf_service.model_id,
            "problem_detected": problem_detected,
            **results
        }
        
        # Add optional problem fields if detected
        if problem_detected and problem_description:
            response_data["problem_description"] = problem_description
        if problem_detected and dispatch_note:
            response_data["dispatch_note"] = dispatch_note
        
        return JSONResponse(content=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
