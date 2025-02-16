#!/bin/bash
# final.sh - Creates a virtual environment, installs dependencies, and runs the simulation.

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the virtual environment directory name.
VENV_DIR="venv"

echo "-------------------------------------"
echo "Creating virtual environment..."
echo "-------------------------------------"

# Create virtual environment (if it doesn't exist).
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created in '$VENV_DIR'."
else
    echo "Virtual environment '$VENV_DIR' already exists."
fi

# Activate the virtual environment.
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip.
echo "Upgrading pip..."
pip install --upgrade pip

# Install required packages.
echo "Installing required packages (rich and matplotlib)..."
pip install rich matplotlib

echo "-------------------------------------"
echo "Running the simulation..."
echo "-------------------------------------"

# Run the main simulation script.
python3 main.py

# Optionally, deactivate the virtual environment after the run.
echo "Simulation complete."

echo "-------------------------------------"
echo "Deactivating virtual environment...."
echo "-------------------------------------"
deactivate
