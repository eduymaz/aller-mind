FROM python:3.11-slim

LABEL maintainer="AllerMind Team"
LABEL description="AllerMind ML Model Microservice - Expert Prediction System"

WORKDIR /app

# Install system dependencies and gdown for Google Drive downloads
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install gdown for reliable Google Drive downloads
RUN pip install --no-cache-dir gdown

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY real_model_test.py .

# Create model directory structure
RUN mkdir -p ./DATA/MODEL/version2_pkl_models

# Copy model files and expert predictor
# Python files and config
COPY DATA/MODEL/version2_pkl_models/*.py ./DATA/MODEL/version2_pkl_models/
COPY DATA/MODEL/version2_pkl_models/*.json ./DATA/MODEL/version2_pkl_models/

# Copy all pkl models from local (Grup1 excluded via .dockerignore, will be downloaded)
COPY DATA/MODEL/version2_pkl_models/ ./DATA/MODEL/version2_pkl_models/

# Download Grup1 model from Google Drive during build
RUN echo "📥 Downloading Grup1 model from Google Drive..." && \
    gdown --id 1RJHb7nNaRXmTm8Vkdkp4E2Zx-fkXgT9K \
          -O ./DATA/MODEL/version2_pkl_models/Grup1_advanced_model_v2.pkl && \
    echo "✅ Grup1 model downloaded successfully" && \
    ls -lh ./DATA/MODEL/version2_pkl_models/Grup1_advanced_model_v2.pkl

# Create necessary directories
RUN mkdir -p /app/logs

# Expose the port
EXPOSE 8585

# Environment variables
ENV FLASK_APP=real_model_test.py
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8585/health || exit 1

# Run the application
CMD ["python", "real_model_test.py"]