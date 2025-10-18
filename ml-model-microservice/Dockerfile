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

# Copy all pkl models from local (Grup1 excluded via .dockerignore, will be downloaded)
COPY DATA/MODEL/version2_pkl_models/ ./DATA/MODEL/version2_pkl_models/

# Create necessary directories
RUN mkdir -p /app/logs

# Environment variables
ENV FLASK_APP=real_model_test.py
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=production
ENV PORT=8585

# Expose port (Cloud Run will override this with its own PORT env var)
EXPOSE $PORT

# Run the application
CMD ["python", "real_model_test.py"]