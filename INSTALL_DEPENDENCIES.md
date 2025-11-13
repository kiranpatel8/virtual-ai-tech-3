# Installing Python Dependencies

## Issue: Import errors in main.py

The linter warnings you're seeing (`Import "requests" could not be resolved from source`) occur because the required Python packages haven't been installed yet.

## Solution

### Step 1: Install pip (if not already installed)

If you get an error that pip is not found, install it:

```bash
# Download get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# Install pip
python get-pip.py
```

Or download manually from: https://bootstrap.pypa.io/get-pip.py

### Step 2: Install Required Packages

Choose one of these methods:

#### Option A: Using requirements.txt (Recommended)
```bash
python -m pip install -r requirements.txt
```

#### Option B: Install packages individually
```bash
python -m pip install fastapi==0.104.1
python -m pip install uvicorn==0.24.0
python -m pip install python-multipart==0.0.6
python -m pip install requests==2.31.0
python -m pip install Pillow==10.1.0
python -m pip install python-dotenv==1.0.0
```

#### Option C: Using a Virtual Environment (Best Practice)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install packages
python -m pip install -r requirements.txt
```

### Step 3: Configure VS Code (if using VS Code)

1. Open Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose the Python interpreter where packages are installed
   - If using venv: Select `.\venv\Scripts\python.exe`
   - Otherwise: Select your global Python installation

### Step 4: Verify Installation

```bash
# Check if packages are installed
python -m pip list

# Test the imports
python -c "import fastapi, requests, PIL; print('All imports successful!')"
```

## After Installation

Once dependencies are installed:
1. The linter warnings should disappear
2. You can run the API: `python main.py`
3. Or use the startup script: `python start_api.py`

## Troubleshooting

### "pip is not recognized"
- Make sure Python is in your PATH
- Use `python -m pip` instead of just `pip`
- Reinstall Python with "Add to PATH" option checked

### "Permission denied" errors
- Run terminal as Administrator (Windows)
- Use `--user` flag: `python -m pip install --user -r requirements.txt`
- Or use a virtual environment (recommended)

### Packages install but imports still not resolved
- Restart VS Code
- Check Python interpreter selection
- Make sure you're using the same Python where packages were installed

## Quick Setup Script

For Windows, you can also run:
```bash
python start_api.py
```

This script checks dependencies and provides guidance if anything is missing.
