#!/bin/bash
# Setup script for Hugging Face Spaces deployment

set -e  # Exit on any error

echo "Setting up Humanoid Robotics RAG Agent for Hugging Face Spaces..."

# Create necessary directories if they don't exist
mkdir -p src/api src/storage src/embeddings src/extraction src/services src/utils src/models

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete!"