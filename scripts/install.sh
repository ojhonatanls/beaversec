#!/bin/bash
# BeaverSec Installation Script for Unix-like systems

set -e

echo "BeaverSec Installation"
echo "======================"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3.8+ is required but not found"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if (( $(echo "$PYTHON_VERSION < 3.8" | bc -l) )); then
    echo "Error: Python 3.8+ required (found $PYTHON_VERSION)"
    exit 1
fi

echo "Found Python $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies if requested
if [ "$1" = "--dev" ]; then
    echo "Installing development dependencies..."
    pip install -r requirements-dev.txt
fi

# Install BeaverSec in development mode
echo "Installing BeaverSec..."
pip install -e .

# Create configuration directory
mkdir -p ~/.beaversec
mkdir -p ~/.beaversec/logs
mkdir -p ~/.beaversec/credentials

# Create default configuration
if [ ! -f ~/.beaversec/config.yaml ]; then
    echo "Creating default configuration..."
    cp beaversec/config/templates/config.yaml.template ~/.beaversec/config.yaml
fi

# Set permissions
chmod 755 ~/.beaversec
chmod 700 ~/.beaversec/credentials

echo ""
echo "Installation complete!"
echo ""
echo "To start using BeaverSec:"
echo "  source venv/bin/activate"
echo "  beaversec --help"
echo ""
echo "Or run directly:"
echo "  venv/bin/beaversec --help"