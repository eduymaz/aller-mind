#!/bin/bash
# ML Model Microservice - Build ve Test Script

set -e

echo "=================================="
echo "ML Model Microservice Build Test"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}❌ Dockerfile bulunamadı!${NC}"
    echo "Bu script'i ml-model-microservice dizininde çalıştırın:"
    echo "  cd ml-model-microservice"
    echo "  ./test-build.sh"
    exit 1
fi

echo -e "${YELLOW}📦 Step 1: Docker Image Build${NC}"
echo "Building allermind-ml-model:test..."
echo ""

docker build -t allermind-ml-model:test . || {
    echo -e "${RED}❌ Docker build başarısız!${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}✅ Build başarılı!${NC}"
echo ""

echo -e "${YELLOW}🔍 Step 2: Model Dosyalarını Kontrol Et${NC}"
echo ""

# Create temporary container to check files
CONTAINER_ID=$(docker create allermind-ml-model:test)

echo "Model dosyaları:"
docker cp $CONTAINER_ID:/app/DATA/MODEL/version2_pkl_models /tmp/model_check 2>/dev/null || {
    echo -e "${RED}❌ Model dizini kopyalanamadı!${NC}"
    docker rm $CONTAINER_ID
    exit 1
}

# List pkl files
echo ""
echo "PKL Model Dosyaları:"
ls -lh /tmp/model_check/*.pkl 2>/dev/null | awk '{print "  " $9 " - " $5}'

# Count models
MODEL_COUNT=$(ls -1 /tmp/model_check/Grup*.pkl 2>/dev/null | wc -l | tr -d ' ')

echo ""
if [ "$MODEL_COUNT" -eq 5 ]; then
    echo -e "${GREEN}✅ Tüm 5 model dosyası mevcut!${NC}"
else
    echo -e "${RED}❌ Model sayısı: $MODEL_COUNT (beklenen: 5)${NC}"
    docker rm $CONTAINER_ID
    rm -rf /tmp/model_check
    exit 1
fi

# Check Grup1 specifically
if [ -f "/tmp/model_check/Grup1_advanced_model_v2.pkl" ]; then
    GRUP1_SIZE=$(ls -lh /tmp/model_check/Grup1_advanced_model_v2.pkl | awk '{print $5}')
    echo -e "${GREEN}✅ Grup1 model başarıyla indirildi (${GRUP1_SIZE})${NC}"
else
    echo -e "${RED}❌ Grup1 model bulunamadı!${NC}"
    docker rm $CONTAINER_ID
    rm -rf /tmp/model_check
    exit 1
fi

# Cleanup
docker rm $CONTAINER_ID > /dev/null
rm -rf /tmp/model_check

echo ""
echo -e "${YELLOW}🚀 Step 3: Container Çalıştır ve Test Et${NC}"
echo ""

# Run container
echo "Container başlatılıyor..."
CONTAINER_RUN_ID=$(docker run -d -p 8585:8585 allermind-ml-model:test)

echo "Container ID: $CONTAINER_RUN_ID"
echo "Servis başlatılması bekleniyor (30 saniye)..."
sleep 30

# Test health endpoint
echo ""
echo "Health check testi..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8585/health)

if [ "$HTTP_STATUS" -eq 200 ]; then
    echo -e "${GREEN}✅ Health check başarılı (HTTP $HTTP_STATUS)${NC}"
else
    echo -e "${RED}❌ Health check başarısız (HTTP $HTTP_STATUS)${NC}"
    echo ""
    echo "Container logs:"
    docker logs $CONTAINER_RUN_ID
    docker stop $CONTAINER_RUN_ID > /dev/null
    docker rm $CONTAINER_RUN_ID > /dev/null
    exit 1
fi

# Get health response
echo ""
echo "Health endpoint response:"
curl -s http://localhost:8585/health | python3 -m json.tool || curl -s http://localhost:8585/health

# Check logs for model loading
echo ""
echo "Model yükleme logları:"
docker logs $CONTAINER_RUN_ID 2>&1 | grep -E "(Grup|model|yüklendi|EXPERT)" | head -10

echo ""
echo -e "${YELLOW}🧹 Step 4: Cleanup${NC}"
echo ""

docker stop $CONTAINER_RUN_ID > /dev/null
docker rm $CONTAINER_RUN_ID > /dev/null

echo "Container durduruldu ve temizlendi"

echo ""
echo "=================================="
echo -e "${GREEN}✅ TÜM TESTLER BAŞARILI!${NC}"
echo "=================================="
echo ""
echo "Image hazır: allermind-ml-model:test"
echo ""
echo "Manuel test için:"
echo "  docker run -p 8585:8585 allermind-ml-model:test"
echo "  curl http://localhost:8585/health"
echo ""
echo "Image'i silmek için:"
echo "  docker rmi allermind-ml-model:test"
echo ""
