import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Application settings and configuration
    """
    # Hugging Face Configuration
    HUGGINGFACE_API_TOKEN: Optional[str] = os.getenv("HUGGINGFACE_API_TOKEN")
    
    # Default model for image classification
    # Options for better telecom device classification:
    # - google/vit-base-patch16-224 (Vision Transformer - general purpose)
    # - microsoft/DiT-base-distilled-patch16-224 (Data-efficient Image Transformer)
    # - facebook/convnext-base-224 (ConvNeXt model)
    # - microsoft/swin-base-patch4-window7-224 (Swin Transformer)
    HUGGINGFACE_MODEL_ID: str = os.getenv("HUGGINGFACE_MODEL_ID", "google/vit-base-patch16-224")
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Image processing settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_IMAGE_DIMENSION: int = 1024
    JPEG_QUALITY: int = 85
    
    # API timeout settings
    HUGGINGFACE_TIMEOUT: int = 30

settings = Settings()
