@echo off
echo ====================================================
echo Telecom Device Identifier - Ionic App Setup
echo ====================================================

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js version:
node --version

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed. Please install npm.
    pause
    exit /b 1
)

echo ✅ npm version:
npm --version

REM Install dependencies
echo.
echo 📦 Installing dependencies...
npm install

REM Check if Ionic CLI is installed globally
ionic --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Ionic CLI is not installed globally.
    echo Installing Ionic CLI...
    npm install -g @ionic/cli
)

echo ✅ Ionic CLI version:
ionic --version

REM Check if Capacitor CLI is installed globally
cap --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Capacitor CLI is not installed globally.
    echo Installing Capacitor CLI...
    npm install -g @capacitor/cli
)

echo ✅ Capacitor CLI version:
cap --version

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Make sure the Python API is running:
echo    cd .. ^&^& python start_api.py
echo.
echo 2. Update the API URL in src/environments/environment.ts
echo    For mobile testing, use your computer's IP address instead of localhost
echo.
echo 3. Start the development server:
echo    ionic serve
echo.
echo 4. For mobile development:
echo    ionic capacitor add android    # For Android
echo    ionic capacitor add ios        # For iOS (macOS only)
echo.
echo 📖 Check README.md for detailed instructions
echo.
pause
