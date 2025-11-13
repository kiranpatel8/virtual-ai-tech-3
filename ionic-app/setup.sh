#!/bin/bash

# Telecom Device Identifier - Ionic App Setup Script
echo "===================================================="
echo "Telecom Device Identifier - Ionic App Setup"
echo "===================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

echo "✅ npm version: $(npm --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Check if Ionic CLI is installed globally
if ! command -v ionic &> /dev/null; then
    echo ""
    echo "⚠️  Ionic CLI is not installed globally."
    echo "Installing Ionic CLI..."
    npm install -g @ionic/cli
fi

echo "✅ Ionic CLI version: $(ionic --version)"

# Check if Capacitor CLI is installed globally
if ! command -v cap &> /dev/null; then
    echo ""
    echo "⚠️  Capacitor CLI is not installed globally."
    echo "Installing Capacitor CLI..."
    npm install -g @capacitor/cli
fi

echo "✅ Capacitor CLI version: $(cap --version)"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure the Python API is running:"
echo "   cd .. && python start_api.py"
echo ""
echo "2. Update the API URL in src/environments/environment.ts"
echo "   For mobile testing, use your computer's IP address instead of localhost"
echo ""
echo "3. Start the development server:"
echo "   ionic serve"
echo ""
echo "4. For mobile development:"
echo "   ionic capacitor add android    # For Android"
echo "   ionic capacitor add ios        # For iOS (macOS only)"
echo ""
echo "📖 Check README.md for detailed instructions"
echo ""
