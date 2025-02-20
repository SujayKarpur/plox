#!/bin/bash
set -e  # Exit on any error

# Determine the directory where the script resides (plox/build)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if required files exist in the SCRIPT_DIR
REQUIRED_FILES=("requirements.txt" "setup.py" "plox")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$SCRIPT_DIR/$file" ]; then
        echo "Error: $file not found in $SCRIPT_DIR. Please ensure you're in the correct directory."
        exit 1
    fi
done

# Check if a virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: No active virtual environment found. Please activate one before running this script."
    exit 1
fi

echo "Using virtual environment: $VIRTUAL_ENV"
echo "Project root: $PROJECT_ROOT"
echo "Build directory: $SCRIPT_DIR"

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r "$SCRIPT_DIR/requirements.txt"

# Build and install the package
echo "Building and installing the package via setup.py..."
cd "$SCRIPT_DIR"
python setup.py install

# Give execution permissions to the plox executable
echo "Setting executable permissions for plox..."
chmod +x "$SCRIPT_DIR/plox"

echo "Build complete. You can now run the executable with:"
echo "  $SCRIPT_DIR/plox"
echo "Or, if you're in the build directory, simply:"
echo "  ./plox"
