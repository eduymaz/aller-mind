# 🚀 AllerMind Quick Start Guide

Get AllerMind up and running in 5 minutes! This guide provides the fastest path to a working development environment.

---

## ⚡ Prerequisites

Before you begin, ensure you have:

- **Docker Desktop** installed ([Download](https://www.docker.com/products/docker-desktop))
- **Git** installed
- **Google API Key** for Pollen and Air Quality APIs ([Get API Key](https://console.cloud.google.com/))
- **8GB RAM** minimum
- **10GB disk space** available

---

## 📦 Quick Setup (5 Minutes)

### Step 1: Clone Repository (30 seconds)

```bash
git clone https://github.com/eduymaz/allermind.git
cd aller-mind
```

### Step 2: Configure Environment (1 minute)

Create a `.env` file in the project root:

```bash
cat > .env << EOF
# Google API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Database Configuration
DATABASE_URL=jdbc:postgresql://postgres:5432/allermind
DATABASE_USER=postgres
DATABASE_PASSWORD=password

# Service URLs (for local development)
ML_MODEL_URL=http://ml-model-service:8585
POLLEN_URL=http://pollen-service:8282
WEATHER_URL=http://weather-service:8383
USER_PREF_URL=http://userpreference-service:9191
EOF
```

**Important**: Replace `your_google_api_key_here` with your actual Google API key.

### Step 3: Start All Services (3 minutes)

```bash
docker-compose up --build
```

This will:
- Build all 5 microservices
- Start PostgreSQL database
- Initialize database schema
- Start all services on their respective ports

**First build takes 2-3 minutes**. Subsequent starts are much faster.

### Step 4: Verify Services (30 seconds)

Check that all services are running:

```bash
# Check service health
curl http://localhost:8484/api/health   # Model Orchestration Service
curl http://localhost:8585/health       # ML Model Service
curl http://localhost:8282/actuator/health  # Pollen Service
curl http://localhost:8383/actuator/health  # Weather Service
curl http://localhost:9191/actuator/health  # User Preference Service
```

All should return `{"status": "UP"}` or similar.

---

## 🎯 Quick Test

### Test the Prediction API

```bash
curl -X POST http://localhost:8484/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 41.0082,
    "longitude": 28.9784,
    "userId": "test_user_123"
  }'
```

**Expected Response**:
```json
{
  "safeMinutes": 240,
  "riskLevel": "MODERATE",
  "confidence": 0.95,
  "recommendations": [
    "Wear sunglasses outdoors",
    "Monitor pollen levels"
  ],
  "environmentalData": {
    "temperature": 25.5,
    "humidity": 60,
    "pollenIndex": 3.2,
    "airQualityIndex": 45
  }
}
```

---

## 🌐 Access Points

Once running, access these URLs:

| Service | URL | Description |
|---------|-----|-------------|
| **Model Orchestration** | http://localhost:8484 | Main API endpoint |
| **Swagger UI** | http://localhost:8484/swagger-ui/index.html | API Documentation |
| **ML Model Service** | http://localhost:8585 | Machine Learning predictions |
| **Pollen Service** | http://localhost:8282 | Pollen data API |
| **Weather Service** | http://localhost:8383 | Weather & air quality API |
| **User Preference** | http://localhost:9191 | User management API |
| **PostgreSQL** | localhost:5432 | Database (use pgAdmin or psql) |

---

## 🛠️ Common Commands

### Start Services
```bash
docker-compose up
```

### Start in Background
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f
```

### Stop Services
```bash
docker-compose down
```

### Rebuild Services
```bash
docker-compose up --build
```

### Clean Everything
```bash
docker-compose down -v  # Remove volumes too
```

---

## 📱 Flutter Mobile App (Optional)

### Setup Flutter App

```bash
cd FLUTTER
flutter pub get
flutter run
```

### Update API Endpoint

Edit `lib/utils/constants.dart`:

```dart
class Constants {
  static const String apiBaseUrl = 'http://localhost:8484';  // For iOS emulator
  // static const String apiBaseUrl = 'http://10.0.2.2:8484'; // For Android emulator
  // static const String apiBaseUrl = 'http://YOUR-IP:8484';  // For physical device
}
```

---

## 🐛 Troubleshooting

### Port Already in Use

If ports are occupied:

```bash
# Find process using port
lsof -ti:8484

# Kill process
kill -9 $(lsof -ti:8484)
```

### Docker Build Fails

```bash
# Clean Docker cache
docker system prune -a

# Rebuild
docker-compose build --no-cache
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps

# Access PostgreSQL directly
docker-compose exec postgres psql -U postgres -d allermind

# Check tables
\dt
```

### Service Not Starting

```bash
# Check logs for specific service
docker-compose logs model-service
docker-compose logs ml-model-service
docker-compose logs postgres
```

### Out of Memory

Increase Docker memory allocation:
- Docker Desktop → Settings → Resources → Memory → Set to 4GB+

---

## 📊 Verify Installation

Run this test script to verify all components:

```bash
#!/bin/bash
echo "🧪 Testing AllerMind Services..."

echo "1. Testing Model Orchestration Service..."
curl -s http://localhost:8484/api/health | grep -q "UP" && echo "✅ Model Service OK" || echo "❌ Model Service FAILED"

echo "2. Testing ML Model Service..."
curl -s http://localhost:8585/health | grep -q "status" && echo "✅ ML Service OK" || echo "❌ ML Service FAILED"

echo "3. Testing Pollen Service..."
curl -s http://localhost:8282/actuator/health | grep -q "UP" && echo "✅ Pollen Service OK" || echo "❌ Pollen Service FAILED"

echo "4. Testing Weather Service..."
curl -s http://localhost:8383/actuator/health | grep -q "UP" && echo "✅ Weather Service OK" || echo "❌ Weather Service FAILED"

echo "5. Testing User Preference Service..."
curl -s http://localhost:9191/actuator/health | grep -q "UP" && echo "✅ User Service OK" || echo "❌ User Service FAILED"

echo "6. Testing Database..."
docker-compose exec -T postgres psql -U postgres -d allermind -c "SELECT 1;" > /dev/null 2>&1 && echo "✅ Database OK" || echo "❌ Database FAILED"

echo ""
echo "🎉 All tests complete!"
```

Save as `test-services.sh`, make executable, and run:

```bash
chmod +x test-services.sh
./test-services.sh
```

---

## 🎓 Next Steps

Now that you have AllerMind running:

1. **Explore the API** - Open Swagger UI at http://localhost:8484/swagger-ui/index.html
2. **Read the Tutorial** - Check `TUTORIAL.md` for in-depth technical documentation
3. **Test predictions** - Try different locations and user profiles
4. **Mobile app** - Run the Flutter app to see the complete user experience
5. **Deploy to cloud** - See `RENDER_DEPLOYMENT.md` for production deployment

---

## 📚 Additional Resources

- **Full Documentation**: `TUTORIAL.md`
- **Docker Details**: `DOCKER_README.md`
- **Production Deployment**: `RENDER_DEPLOYMENT.md`
- **Contributing**: `CONTRIBUTING.md`
- **Project Overview**: `README.md`

---

## 💡 Tips

- **First run**: Takes 2-3 minutes to download images and build
- **Subsequent runs**: Start in ~30 seconds
- **Development**: Use `docker-compose up` (without `-d`) to see logs in real-time
- **Production**: Never commit `.env` file to git (it's in `.gitignore`)
- **API Key**: Free tier Google API key has rate limits - consider upgrading for production

---

## 🆘 Need Help?

- **Issues**: Check `TROUBLESHOOTING.md` (if available) or open a GitHub issue
- **Questions**: Reach out to the team or check existing documentation
- **Logs**: Always check `docker-compose logs` for error details

---

**🎉 Congratulations! You now have AllerMind running locally.**

Happy coding! 🌿
