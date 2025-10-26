#!/bin/bash
# AI PM Resume Analyzer - Installation Script
# Installs Python dependencies and sets up the tool

set -e  # Exit on error

echo "🚀 AI PM Resume Analyzer - Installation"
echo "========================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Please install Python 3.7 or higher:"
    echo "  macOS: brew install python3"
    echo "  Linux: sudo apt install python3 python3-pip"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.7"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 3.7+ required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"
echo ""

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found!"
    echo "Installing pip..."
    python3 -m ensurepip --upgrade
fi

echo "📦 Installing Python dependencies..."
echo ""

# Install requirements
pip3 install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Run: ./bin/analyze --help"
echo "  2. On first run, the tool will create a .env file"
echo "  3. Add your API key to the .env file"
echo "  4. Start analyzing resumes!"
echo ""
echo "For detailed instructions, see README.md"
