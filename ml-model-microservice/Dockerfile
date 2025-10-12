FROM python:3.11-slim

LABEL maintainer="AllerMind Team"
LABEL description="AllerMind ML Model Microservice - Expert Prediction System"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY real_model_test.py .

# Copy model files and expert predictor
COPY DATA/MODEL/version2_pkl_models/ ./DATA/MODEL/version2_pkl_models/

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