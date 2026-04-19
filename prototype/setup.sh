#!/bin/bash
# Setup script for Einstein AI Coding Agent Prototype

set -e  # Exit on error

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🤖 Einstein AI Coding Agent - Prototype Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# Check Python version
echo "1️⃣  Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"
echo

# Check if we're in a virtual environment (recommended)
echo "2️⃣  Checking virtual environment..."
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Not in a virtual environment"
    echo "   Recommendation: Create a venv first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo
    read -p "   Continue without venv? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Virtual environment: $VIRTUAL_ENV"
fi
echo

# Install system dependencies (macOS)
echo "3️⃣  Checking system dependencies..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   Detected macOS"
    
    if ! command -v brew &> /dev/null; then
        echo "⚠️  Homebrew not found. Install from https://brew.sh"
    else
        echo "   Installing portaudio via Homebrew..."
        brew install portaudio || echo "   (portaudio may already be installed)"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "   Detected Linux"
    echo "   You may need to install: sudo apt-get install portaudio19-dev python3-pyaudio"
else
    echo "   Detected: $OSTYPE"
    echo "   Please install portaudio manually if needed"
fi
echo

# Install Python dependencies
echo "4️⃣  Installing Python packages..."
pip install -r requirements.txt
echo "✅ Python packages installed"
echo

# Create projects directory
echo "5️⃣  Creating projects directory..."
mkdir -p ~/ai-projects
echo "✅ Created ~/ai-projects/"
echo

# Test installations
echo "6️⃣  Testing installations..."
echo

echo "   Testing SpeechRecognition..."
python3 -c "import speech_recognition as sr; print('   ✅ SpeechRecognition works')" || echo "   ❌ Failed"

echo "   Testing Whisper..."
python3 -c "import whisper; print('   ✅ Whisper works')" || echo "   ❌ Failed (will download on first use)"

echo "   Testing requests..."
python3 -c "import requests; print('   ✅ Requests works')" || echo "   ❌ Failed"

echo

# Check for LM Studio
echo "7️⃣  Checking LM Studio..."
if curl -s http://localhost:1234/v1/models > /dev/null 2>&1; then
    echo "✅ LM Studio is running on port 1234"
else
    echo "⚠️  LM Studio not detected on port 1234"
    echo "   Please:"
    echo "   1. Open LM Studio"
    echo "   2. Load Qwen Coder 32B model"
    echo "   3. Start the server (port 1234)"
fi
echo

# Make scripts executable
echo "8️⃣  Making scripts executable..."
chmod +x main.py
chmod +x tests/test_basic.py
chmod +x voice/listener.py
chmod +x llm/coder.py
chmod +x executor/runner.py
chmod +x storage/manager.py
echo "✅ Scripts are executable"
echo

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
echo "Next steps:"
echo
echo "1. Make sure LM Studio is running with Qwen Coder 32B"
echo "2. Run tests: python3 tests/test_basic.py"
echo "3. Start the agent: python3 main.py"
echo
echo "Happy coding! 🚀"
echo
