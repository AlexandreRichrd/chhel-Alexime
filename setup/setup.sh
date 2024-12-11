#!/bin/bash

# Define the Python version and virtual environment directory
PYTHON_VERSION="3.11.1"
VENV_DIR="../venv"

# Check if the specified Python version is installed
if ! command -v python3.11 &> /dev/null
then
    echo "Python $PYTHON_VERSION is not installed. Please install Python $PYTHON_VERSION first."
    exit
fi

# Create the virtual environment with the specified Python version
python3.11 -m venv $VENV_DIR

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the required packages
pip install -r requirements.txt

echo "Setup complete. Virtual environment created and dependencies installed."