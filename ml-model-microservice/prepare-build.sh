#!/bin/bash

# ML Model Microservice Build Script
# Prepares the Docker build context by copying necessary files

echo "🤖 Preparing ML Model Microservice for Docker..."

# Define paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ML_SERVICE_DIR="$SCRIPT_DIR"

# Copy Python application file
echo "📦 Copying application files..."
cp "$PROJECT_ROOT/real_model_test.py" "$ML_SERVICE_DIR/"

# Copy MODEL directory with expert predictor and pkl files
echo "📊 Copying model files..."
mkdir -p "$ML_SERVICE_DIR/DATA/MODEL"
cp -r "$PROJECT_ROOT/DATA/MODEL/version2_pkl_models" "$ML_SERVICE_DIR/DATA/MODEL/"

# Verify files
echo "✅ Verifying files..."
if [ -f "$ML_SERVICE_DIR/real_model_test.py" ]; then
    echo "  ✓ real_model_test.py copied"
else
    echo "  ✗ real_model_test.py missing!"
    exit 1
fi

if [ -d "$ML_SERVICE_DIR/DATA/MODEL/version2_pkl_models" ]; then
    echo "  ✓ Model files copied"
    echo "  📁 Model files:"
    ls -la "$ML_SERVICE_DIR/DATA/MODEL/version2_pkl_models/"*.pkl 2>/dev/null || echo "  No .pkl files found"
else
    echo "  ✗ Model directory missing!"
    exit 1
fi

echo "🎉 ML Model Microservice ready for Docker build!"
echo "💡 Run: docker build -t allermind-ml-model ."