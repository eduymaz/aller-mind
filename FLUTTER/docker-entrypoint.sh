#!/bin/sh
set -e

# Default values if environment variables are not set
export MODEL_SERVICE_URL=${MODEL_SERVICE_URL:-"http://localhost:8484"}
export USER_PREFERENCE_SERVICE_URL=${USER_PREFERENCE_SERVICE_URL:-"http://localhost:9191"}

echo "🔧 Configuring Nginx with environment variables..."
echo "MODEL_SERVICE_URL: ${MODEL_SERVICE_URL}"
echo "USER_PREFERENCE_SERVICE_URL: ${USER_PREFERENCE_SERVICE_URL}"

# Replace environment variables in nginx config
envsubst '${MODEL_SERVICE_URL} ${USER_PREFERENCE_SERVICE_URL}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

echo "✅ Nginx configuration complete"

# Execute the CMD
exec "$@"
