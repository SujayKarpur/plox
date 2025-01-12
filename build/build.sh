#!/bin/bash

# Exit on any error
set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python 3."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip is not installed. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# Set the project directory
PROJECT_DIR="$(pwd)"

# Create the virtual environment inside the build folder if it doesn't exist
VENV_DIR="$PROJECT_DIR/build/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Install dependencies from requirements.txt
if [ -f "$PROJECT_DIR/build/requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r "$PROJECT_DIR/build/requirements.txt"
else
    echo "No requirements.txt found. Skipping dependency installation."
fi

# Install the project in editable mode
echo "Installing the project in editable mode..."
pip install -e "$PROJECT_DIR/build/."

# Make the plox executable available globally by linking it
echo "Creating executable for plox..."
ln -s "$PROJECT_DIR/build/plox" /usr/local/bin/plox

# Add build to the PATH permanently by modifying the bashrc
echo "export PATH=\$PATH:$PROJECT_DIR/build" >> ~/.bashrc
source ~/.bashrc

# Success message
echo "Setup complete! You can now run 'plox' from anywhere."
