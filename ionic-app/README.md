# Telecom Device Identifier - Mobile App

A mobile application built with Ionic and Angular that allows users to take photos of telecom devices and identify them using the Python REST API service.

## Features

- **Camera Integration**: Take photos or select from gallery
- **Real-time Identification**: Connect to Python API for device classification
- **Beautiful UI**: Modern, responsive design with Ionic components
- **Cross-platform**: Works on iOS, Android, and web browsers
- **Offline Detection**: Handles API connectivity issues gracefully

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 16 or later)
- **npm** or **yarn**
- **Ionic CLI**: `npm install -g @ionic/cli`
- **Capacitor CLI**: `npm install -g @capacitor/cli`

For mobile development:
- **Android Studio** (for Android)
- **Xcode** (for iOS - macOS only)

## Quick Start

### 1. Install Dependencies

```bash
cd ionic-app
npm install
```

### 2. Configure API Endpoint

Edit `src/environments/environment.ts` to point to your Python API:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'  // Update if your API runs elsewhere
};
```

**Important**: For mobile devices, you'll need to use your computer's IP address instead of `localhost`.

### 3. Run in Browser (Development)

```bash
ionic serve
```

The app will open at `http://localhost:8100`

### 4. Build for Mobile

#### Android

```bash
# Add Android platform
ionic capacitor add android

# Build and sync
ionic capacitor build android

# Open in Android Studio
ionic capacitor open android
```

#### iOS (macOS only)

```bash
# Add iOS platform
ionic capacitor add ios

# Build and sync
ionic capacitor build ios

# Open in Xcode
ionic capacitor open ios
```

## Project Structure

```
ionic-app/
├── src/
│   ├── app/
│   │   ├── home/                 # Main page component
│   │   ├── services/             # API service
│   │   ├── app.component.*       # Root component
│   │   ├── app.module.ts         # App module
│   │   └── app-routing.module.ts # Routing configuration
│   ├── environments/             # Environment configurations
│   ├── theme/                    # Ionic theme variables
│   └── global.scss              # Global styles
├── capacitor.config.ts          # Capacitor configuration
├── ionic.config.json            # Ionic configuration
└── package.json                 # Dependencies and scripts
```

## API Configuration

The app connects to the Python REST API service. Make sure:

1. **Python API is running**: The Python service should be running on `localhost:8000`
2. **CORS is enabled**: The API should accept requests from the mobile app
3. **Network accessibility**: For mobile devices, use your computer's IP address

### Environment Configuration

Development (`src/environments/environment.ts`):
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://192.168.1.100:8000'  // Use your computer's IP
};
```

Production (`src/environments/environment.prod.ts`):
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://your-api-domain.com'
};
```

## Features Overview

### Camera Integration

- **Take Photo**: Uses device camera to capture images
- **Select from Gallery**: Choose existing photos from device storage
- **Image Processing**: Automatic resizing and format conversion

### API Communication

- **Health Check**: Monitors Python API availability
- **Image Upload**: Sends captured images for identification
- **Real-time Results**: Displays classification results immediately
- **Error Handling**: Graceful handling of network and API errors

### User Interface

- **Material Design**: Modern, intuitive interface
- **Loading States**: Visual feedback during processing
- **Results Display**: Clear presentation of identification results
- **Confidence Scores**: Visual indicators for prediction confidence

## Testing

### Browser Testing

```bash
ionic serve
```

Test the app in your browser. Camera functionality will use device camera or file picker.

### Mobile Testing

#### Android Testing

```bash
# Build and run on connected device
ionic capacitor run android

# Build and run with live reload
ionic capacitor run android -l --external
```

#### iOS Testing

```bash
# Build and run on connected device/simulator
ionic capacitor run ios

# Build and run with live reload
ionic capacitor run ios -l --external
```

## Troubleshooting

### Common Issues

1. **Camera not working**
   - Ensure camera permissions are granted
   - Test on a real device (camera may not work in simulators)

2. **API connection failed**
   - Check if Python API is running
   - Verify the API URL in environment files
   - For mobile: use computer's IP address, not localhost

3. **Build errors**
   - Clear node modules: `rm -rf node_modules && npm install`
   - Update Ionic CLI: `npm install -g @ionic/cli@latest`

### Network Configuration

For mobile devices to connect to your local Python API:

1. **Find your computer's IP**:
   ```bash
   # Windows
   ipconfig
   
   # macOS/Linux
   ifconfig
   ```

2. **Update environment.ts**:
   ```typescript
   apiUrl: 'http://YOUR_COMPUTER_IP:8000'
   ```

3. **Allow network access**: Ensure your firewall allows connections on port 8000

### Permissions

The app requires the following permissions:

- **Camera**: To take photos
- **Photos/Storage**: To select images from gallery
- **Network**: To communicate with the API

These are automatically configured in the Capacitor configuration.

## Deployment

### Web Deployment

```bash
# Build for production
ionic build --prod

# Deploy the dist/ folder to your web server
```

### Mobile App Stores

1. **Build production app**
2. **Test thoroughly on devices**
3. **Follow platform-specific store guidelines**:
   - Google Play Store (Android)
   - Apple App Store (iOS)

## Development

### Adding New Features

1. **Generate new page**: `ionic generate page feature-name`
2. **Generate service**: `ionic generate service services/feature-name`
3. **Update routing**: Add routes in `app-routing.module.ts`

### Styling

- Edit `src/theme/variables.css` for theme customization
- Use Ionic CSS utilities for responsive design
- Follow Ionic design guidelines for consistency

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple devices/platforms
5. Submit a pull request

## Support

For issues:
1. Check the troubleshooting section
2. Verify API connectivity
3. Test on different devices
4. Check browser console for errors

## License

MIT License - see LICENSE file for details.
