#!/bin/bash

# Local Development Run Script
# Bu script Flutter uygulamasını local development modunda başlatır
# Production ortamını etkilemez

set -e

echo "🚀 Starting AllerMind Flutter App in LOCAL DEVELOPMENT mode..."
echo ""

# Varsayılan local servis URL'leri
MODEL_SERVICE_URL="${MODEL_SERVICE_URL:-http://localhost:8484}"
USER_PREFERENCE_SERVICE_URL="${USER_PREFERENCE_SERVICE_URL:-http://localhost:9191}"

echo "📡 Configuration:"
echo "   Model Service: $MODEL_SERVICE_URL"
echo "   User Preference Service: $USER_PREFERENCE_SERVICE_URL"
echo ""

# Local servislerin çalıştığını kontrol et
echo "🔍 Checking if local services are running..."

if curl -s -f "$MODEL_SERVICE_URL/health" > /dev/null 2>&1; then
    echo "   ✅ Model Service is running"
else
    echo "   ⚠️  WARNING: Model Service might not be running at $MODEL_SERVICE_URL"
    echo "      Please start it with: cd ml-model-microservice && python main.py"
fi

if curl -s -f "$USER_PREFERENCE_SERVICE_URL/health" > /dev/null 2>&1; then
    echo "   ✅ User Preference Service is running"
else
    echo "   ⚠️  WARNING: User Preference Service might not be running at $USER_PREFERENCE_SERVICE_URL"
    echo "      Please start it with: cd userpreference-microservice && python main.py"
fi

echo ""
echo "🎯 Running Flutter app with local services..."
echo ""

# Flutter uygulamasını local development modunda başlat
flutter run \
  --dart-define=MODEL_SERVICE_URL="$MODEL_SERVICE_URL" \
  --dart-define=USER_PREFERENCE_SERVICE_URL="$USER_PREFERENCE_SERVICE_URL" -d F150CB0A-F945-42AD-8982-231BFCF353BC
