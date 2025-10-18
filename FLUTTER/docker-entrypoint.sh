#!/bin/sh
set -e

# Google Cloud Run provides the PORT environment variable
# Default to 8080 if not set (Cloud Run default)
export PORT=${PORT:-8080}

# Default values if environment variables are not set
# These defaults allow the app to start even if services are unavailable
export MODEL_SERVICE_URL=${MODEL_SERVICE_URL:-"http://localhost:8484"}
export USER_PREFERENCE_SERVICE_URL=${USER_PREFERENCE_SERVICE_URL:-"http://localhost:9191"}

echo "🔧 Configuring Nginx for Google Cloud Run..."
echo "📍 PORT: ${PORT}"
echo "📍 MODEL_SERVICE_URL: ${MODEL_SERVICE_URL}"
echo "📍 USER_PREFERENCE_SERVICE_URL: ${USER_PREFERENCE_SERVICE_URL}"

# Replace environment variables in nginx config
envsubst '${PORT} ${MODEL_SERVICE_URL} ${USER_PREFERENCE_SERVICE_URL}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Test nginx configuration
echo "🧪 Testing Nginx configuration..."
nginx -t

echo "✅ Nginx configuration complete and validated"
echo "🚀 Starting Nginx server on port ${PORT}..."

# Execute the CMD
exec "$@"
