# Complete Setup Guide - Telecom Device Identifier System

This guide walks you through setting up both the **Python REST API** and the **Ionic Mobile App** for identifying telecom devices using camera photos.

## System Overview

The complete system consists of:

1. **Python REST API** - Backend service that processes images using Hugging Face AI models
2. **Ionic Mobile App** - Cross-platform mobile app with camera integration

```
[Mobile App] ---> [Python API] ---> [Hugging Face API] ---> [Device Classification]
```

## Prerequisites

### For Python API:
- Python 3.8 or later
- pip (Python package installer)

### For Mobile App:
- Node.js 16 or later
- npm or yarn
- Ionic CLI
- (Optional) Android Studio for Android development
- (Optional) Xcode for iOS development (macOS only)

## Step 1: Set Up Python API

### 1.1 Install Python Dependencies

```bash
# Navigate to project root
cd telecom-device-identifier

# Install Python dependencies
pip install -r requirements.txt
```

### 1.2 Configure Environment

Create a `.env` file in the project root:

```bash
# Copy the template
cp env_template.txt .env
```

Edit the `.env` file and add your Hugging Face API token:

```env
HUGGINGFACE_API_TOKEN=your_actual_token_here
HUGGINGFACE_MODEL_ID=google/vit-base-patch16-224
API_HOST=0.0.0.0
API_PORT=8000
```

**Getting a Hugging Face Token:**
1. Sign up at [huggingface.co](https://huggingface.co)
2. Go to Settings > Access Tokens
3. Create a new token with "Read" permissions
4. Copy the token to your `.env` file

### 1.3 Test Python API

```bash
# Start the API server
python start_api.py

# Or directly
python main.py
```

The API should be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

Test with curl:
```bash
curl http://localhost:8000/health
```

## Step 2: Set Up Ionic Mobile App

### 2.1 Install Node.js Dependencies

```bash
# Navigate to ionic app directory
cd ionic-app

# Run setup script (Linux/macOS)
chmod +x setup.sh
./setup.sh

# Or on Windows
setup.bat

# Or manually
npm install
npm install -g @ionic/cli @capacitor/cli
```

### 2.2 Configure API Endpoint

For development, edit `ionic-app/src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'  // For browser testing
};
```

**Important for Mobile Devices:**
Replace `localhost` with your computer's IP address:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://192.168.1.100:8000'  // Use your actual IP
};
```

Find your IP:
- **Windows**: `ipconfig`
- **macOS/Linux**: `ifconfig` or `ip addr`

### 2.3 Test in Browser

```bash
# Start development server
ionic serve
```

The app will open at http://localhost:8100

## Step 3: Test the Complete System

### 3.1 Browser Testing

1. **Start Python API**: `python start_api.py`
2. **Start Ionic App**: `ionic serve`
3. **Test in browser**: Upload an image to test the integration

### 3.2 Mobile Device Testing

#### Android Setup

```bash
# Add Android platform
ionic capacitor add android

# Build and sync
ionic capacitor build android

# Open in Android Studio
ionic capacitor open android

# Or run directly on device
ionic capacitor run android
```

#### iOS Setup (macOS only)

```bash
# Add iOS platform
ionic capacitor add ios

# Build and sync
ionic capacitor build ios

# Open in Xcode
ionic capacitor open ios

# Or run directly on device/simulator
ionic capacitor run ios
```

## Step 4: Usage Instructions

### Using the Mobile App

1. **Open the app** on your device
2. **Check API status** - The app shows if the API is connected (green pulse icon)
3. **Take a photo** or **select from gallery**
4. **View results** - The app automatically sends the image for identification
5. **Interpret results**:
   - **Green badges**: High confidence (80%+)
   - **Yellow badges**: Medium confidence (60-80%)
   - **Red badges**: Low confidence (<60%)

### API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /identify` - Upload image for identification
- `GET /docs` - Interactive API documentation

## Troubleshooting

### Common Issues

#### 1. "API Service Unavailable"
- **Check**: Python API is running on correct port
- **Check**: Firewall allows connections on port 8000
- **Fix**: Restart Python API with `python start_api.py`

#### 2. "Cannot connect to API" (Mobile)
- **Check**: Using computer's IP address, not localhost
- **Check**: Mobile device on same network as computer
- **Fix**: Update environment.ts with correct IP address

#### 3. "Hugging Face API token not configured"
- **Check**: `.env` file exists with valid token
- **Check**: Token has correct permissions
- **Fix**: Get new token from huggingface.co/settings/tokens

#### 4. "Model is loading"
- **Wait**: Hugging Face models need to warm up on first use
- **Try**: Wait 30-60 seconds and try again

#### 5. Camera not working
- **Check**: App has camera permissions
- **Check**: Testing on real device (not simulator)
- **Fix**: Grant camera permissions in device settings

### Network Configuration

For mobile devices to connect to your local API:

1. **Find your computer's IP address**
2. **Update environment files** with the correct IP
3. **Ensure firewall allows connections** on port 8000
4. **Test connectivity** from mobile browser: `http://YOUR_IP:8000/health`

### Development Tips

1. **Use live reload** for faster development:
   ```bash
   ionic capacitor run android -l --external
   ```

2. **Debug on device** using Chrome DevTools:
   - Enable USB debugging on Android
   - Open `chrome://inspect` in Chrome

3. **Monitor API logs** while testing:
   ```bash
   python main.py  # Shows request logs
   ```

## Advanced Configuration

### Custom AI Models

To use different Hugging Face models for better telecom device recognition:

```env
# In .env file
HUGGINGFACE_MODEL_ID=microsoft/DiT-base-distilled-patch16-224
```

Recommended models:
- `google/vit-base-patch16-224` (default)
- `microsoft/DiT-base-distilled-patch16-224`
- `facebook/convnext-base-224`

### Production Deployment

#### Python API
- Use a production WSGI server (Gunicorn, uWSGI)
- Set up proper environment variables
- Configure HTTPS
- Set up monitoring and logging

#### Mobile App
- Build production apps for app stores
- Configure production API endpoints
- Test thoroughly on multiple devices
- Follow platform store guidelines

## File Structure

```
telecom-device-identifier/
├── main.py                    # Python API main file
├── config.py                  # API configuration
├── requirements.txt           # Python dependencies
├── start_api.py              # API startup script
├── test_api.py               # API test script
├── .env                      # Environment variables (create this)
├── ionic-app/                # Mobile app directory
│   ├── src/
│   │   ├── app/
│   │   │   ├── home/         # Main page
│   │   │   └── services/     # API service
│   │   └── environments/     # Environment configs
│   ├── setup.sh              # Setup script (Linux/macOS)
│   ├── setup.bat             # Setup script (Windows)
│   └── package.json          # Node dependencies
└── COMPLETE_SETUP_GUIDE.md   # This file
```

## Support

If you encounter issues:

1. **Check this guide** for common solutions
2. **Verify API connectivity** using the health endpoint
3. **Check browser console** for error messages
4. **Test on multiple devices** to isolate issues
5. **Review logs** from both API and mobile app

## Next Steps

Once everything is working:

1. **Customize the AI model** for better telecom device recognition
2. **Add more device types** to the classification
3. **Implement user authentication** if needed
4. **Add offline support** for the mobile app
5. **Deploy to production** environments

Enjoy using your Telecom Device Identifier system! 🚀📱
