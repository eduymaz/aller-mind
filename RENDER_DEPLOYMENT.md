# 🚀 AllerMind Production Deployment Guide (Render.com)

This guide walks you through deploying AllerMind's microservices architecture to production using Render.com and Google Cloud Run.

---

## 📋 Table of Contents

1. [Deployment Architecture](#-deployment-architecture)
2. [Prerequisites](#-prerequisites)
3. [Database Setup (PostgreSQL)](#-database-setup-postgresql)
4. [Render.com Deployment](#-rendercom-deployment)
5. [Google Cloud Run Deployment](#-google-cloud-run-deployment)
6. [Environment Configuration](#-environment-configuration)
7. [Service Health Checks](#-service-health-checks)
8. [Monitoring & Logging](#-monitoring--logging)
9. [Scaling Configuration](#-scaling-configuration)
10. [Troubleshooting](#-troubleshooting)

---

## 🏗️ Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION DEPLOYMENT                     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Render.com (Free Tier / Starter)                  │    │
│  │                                                     │    │
│  │  ├─ PostgreSQL Database (Managed)                  │    │
│  │  ├─ User Preference Service (Web Service)          │    │
│  │  ├─ Pollen Service (Web Service)                   │    │
│  │  └─ Weather/AirQuality Service (Web Service)       │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Google Cloud Run (Serverless)                     │    │
│  │                                                     │    │
│  │  ├─ Model Orchestration Service                    │    │
│  │  └─ ML Model Service (Python/Flask)                │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  External APIs                                      │    │
│  │  ├─ Google Pollen API                              │    │
│  │  ├─ Google Air Quality API                         │    │
│  │  └─ Open-Meteo API                                 │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ Prerequisites

### Required Accounts

1. **Render.com Account** ([Sign up](https://render.com))
   - Free tier available
   - Credit card required for verification (not charged on free tier)

2. **Google Cloud Platform Account** ([Sign up](https://cloud.google.com))
   - $300 free credit for new users
   - Billing account required

3. **GitHub Account**
   - Repository must be public or connected to Render

### Required Tools

```bash
# Install Google Cloud SDK
brew install google-cloud-sdk  # macOS
# OR download from https://cloud.google.com/sdk/docs/install

# Install Render CLI (optional)
brew tap render-oss/render
brew install render

# Verify installations
gcloud --version
render --version
```

### API Keys

- **Google API Key** with enabled APIs:
  - Pollen API
  - Air Quality API
  - Maps JavaScript API (optional, for geocoding)

---

## 🗄️ Database Setup (PostgreSQL)

### Step 1: Create PostgreSQL Database on Render

1. **Log in to Render Dashboard**: https://dashboard.render.com

2. **Create New PostgreSQL Database**:
   - Click **"New +"** → **"PostgreSQL"**
   - **Name**: `allermind-db`
   - **Database**: `allermind`
   - **User**: `allermind_user` (auto-generated)
   - **Region**: Choose closest to your users (e.g., `Oregon (US West)`)
   - **Plan**: `Free` (500MB, shared CPU) or `Starter` ($7/month, 1GB)

3. **Save Connection Details**:
   - **Internal Database URL**: `postgresql://user:pass@host:5432/allermind`
   - **External Database URL**: For external connections
   - **Connection String**: Will be used in services

### Step 2: Initialize Database Schema

**Option A: Using Render Shell**

```bash
# Connect to database via Render Dashboard
# Dashboard → allermind-db → Connect → Shell

# Run initialization script
\i /path/to/init-db.sql
```

**Option B: Using psql locally**

```bash
# Copy external connection string from Render dashboard
psql "postgresql://allermind_user:PASSWORD@HOST/allermind"

# Create tables
CREATE TABLE user_preferences (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER CHECK (age > 0 AND age < 150),
    allergy_types TEXT[],
    sensitivity_level INTEGER CHECK (sensitivity_level BETWEEN 1 AND 5),
    medical_conditions TEXT[],
    activity_level VARCHAR(50),
    personal_weights JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE prediction_history (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES user_preferences(user_id),
    location_lat DOUBLE PRECISION,
    location_lng DOUBLE PRECISION,
    city_name VARCHAR(255),
    predicted_safe_time INTEGER,
    risk_level VARCHAR(50),
    environmental_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE city_cache (
    id BIGSERIAL PRIMARY KEY,
    city_name VARCHAR(255) UNIQUE,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    country_code VARCHAR(10),
    timezone VARCHAR(100),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);
CREATE INDEX idx_prediction_history_user_id ON prediction_history(user_id);
CREATE INDEX idx_prediction_history_created_at ON prediction_history(created_at);
CREATE INDEX idx_city_cache_name ON city_cache(city_name);
```

### Step 3: Verify Database

```bash
# List tables
\dt

# Check user_preferences table
SELECT COUNT(*) FROM user_preferences;
```

---

## 🌐 Render.com Deployment

### Using render.yaml (Recommended)

**Step 1: Prepare render.yaml**

Create `render.yaml` in project root:

```yaml
services:
  # User Preference Service
  - type: web
    name: userpreference-service
    runtime: docker
    dockerfilePath: ./userpreference-microservice/Dockerfile
    dockerContext: ./userpreference-microservice
    region: oregon
    plan: free
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: allermind-db
          property: connectionString
      - key: SPRING_PROFILES_ACTIVE
        value: prod
      - key: SERVER_PORT
        value: 10000
    healthCheckPath: /actuator/health

  # Pollen Service
  - type: web
    name: pollen-service
    runtime: docker
    dockerfilePath: ./pollen-microservice/Dockerfile
    dockerContext: ./pollen-microservice
    region: oregon
    plan: free
    envVars:
      - key: GOOGLE_API_KEY
        sync: false  # Set via Render dashboard
      - key: SPRING_PROFILES_ACTIVE
        value: prod
      - key: SERVER_PORT
        value: 10000
    healthCheckPath: /actuator/health

  # Weather & Air Quality Service
  - type: web
    name: weather-airpollution-service
    runtime: docker
    dockerfilePath: ./weather-airpollution-microservice/Dockerfile
    dockerContext: ./weather-airpollution-microservice
    region: oregon
    plan: free
    envVars:
      - key: GOOGLE_API_KEY
        sync: false
      - key: SPRING_PROFILES_ACTIVE
        value: prod
      - key: SERVER_PORT
        value: 10000
    healthCheckPath: /actuator/health

databases:
  - name: allermind-db
    databaseName: allermind
    user: allermind_user
    region: oregon
    plan: free
```

**Step 2: Deploy to Render**

```bash
# Option 1: Connect GitHub repository
# 1. Go to Render Dashboard
# 2. Click "New +" → "Blueprint"
# 3. Connect your GitHub repository
# 4. Render will auto-detect render.yaml and deploy

# Option 2: Deploy via Render CLI
render deploy
```

**Step 3: Configure Environment Variables**

For sensitive values (API keys), set via Render Dashboard:

1. Go to each service in Render Dashboard
2. Navigate to **Environment** tab
3. Add environment variables:
   - `GOOGLE_API_KEY`: Your Google API key
   - `DATABASE_URL`: Auto-populated from database

**Step 4: Verify Deployments**

```bash
# Check service URLs (provided by Render)
curl https://userpreference-service.onrender.com/actuator/health
curl https://pollen-service.onrender.com/actuator/health
curl https://weather-airpollution-service.onrender.com/actuator/health
```

---

## ☁️ Google Cloud Run Deployment

### Step 1: Setup Google Cloud Project

```bash
# Authenticate
gcloud auth login

# Create new project
gcloud projects create allermind-prod --name="AllerMind Production"

# Set project
gcloud config set project allermind-prod

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Deploy Model Orchestration Service

```bash
cd model-microservice

# Build and push Docker image
gcloud builds submit --tag gcr.io/allermind-prod/model-service

# Deploy to Cloud Run
gcloud run deploy model-service \
  --image gcr.io/allermind-prod/model-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars "ML_MODEL_URL=https://ml-model-service-XXXXXX.run.app,POLLEN_URL=https://pollen-service.onrender.com,WEATHER_URL=https://weather-airpollution-service.onrender.com,USER_PREF_URL=https://userpreference-service.onrender.com"

# Get service URL
gcloud run services describe model-service --region us-central1 --format 'value(status.url)'
```

### Step 3: Deploy ML Model Service

```bash
cd ../ml-model-microservice

# Build and push
gcloud builds submit --tag gcr.io/allermind-prod/ml-model-service

# Deploy with larger memory (models are heavy)
gcloud run deploy ml-model-service \
  --image gcr.io/allermind-prod/ml-model-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 5 \
  --timeout 300

# Get service URL
gcloud run services describe ml-model-service --region us-central1 --format 'value(status.url)'
```

### Step 4: Update Model Service with ML URL

```bash
# Update model-service with actual ML service URL
gcloud run services update model-service \
  --region us-central1 \
  --update-env-vars "ML_MODEL_URL=https://ml-model-service-XXXXXX-uc.a.run.app"
```

### Step 5: Verify Cloud Run Deployments

```bash
# Test Model Orchestration Service
curl https://model-service-XXXXXX-uc.a.run.app/api/health

# Test ML Model Service
curl https://ml-model-service-XXXXXX-uc.a.run.app/health
```

---

## ⚙️ Environment Configuration

### Complete Environment Variables Matrix

| Service | Variable | Source | Example |
|---------|----------|--------|---------|
| **Model Service** | ML_MODEL_URL | Cloud Run URL | https://ml-model-service-xxx.run.app |
| | POLLEN_URL | Render URL | https://pollen-service.onrender.com |
| | WEATHER_URL | Render URL | https://weather-service.onrender.com |
| | USER_PREF_URL | Render URL | https://userpreference-service.onrender.com |
| **ML Model Service** | N/A | N/A | N/A |
| **Pollen Service** | GOOGLE_API_KEY | Google Cloud Console | AIzaSyXXXXXXXXXXXXXXXXXX |
| **Weather Service** | GOOGLE_API_KEY | Google Cloud Console | AIzaSyXXXXXXXXXXXXXXXXXX |
| **User Preference** | DATABASE_URL | Render Database | postgresql://user:pass@host/db |
| | SPRING_PROFILES_ACTIVE | Static | prod |

### Production application.yml Template

```yaml
# application-prod.yml (for Spring Boot services)
spring:
  application:
    name: ${SERVICE_NAME}
  
  datasource:
    url: ${DATABASE_URL}
    hikari:
      maximum-pool-size: 5
      minimum-idle: 2
      connection-timeout: 30000
  
  jpa:
    hibernate:
      ddl-auto: validate  # NEVER use 'update' in production
    show-sql: false
    properties:
      hibernate:
        format_sql: false

server:
  port: ${PORT:10000}  # Render uses PORT env variable
  
logging:
  level:
    root: INFO
    com.allermind: INFO
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} - %msg%n"

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: when-authorized
```

---

## 🏥 Service Health Checks

### Configure Health Endpoints

**Spring Boot Services** (Auto-configured):

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info
  endpoint:
    health:
      show-details: always
```

**Python Flask Service**:

```python
# app.py
@app.route('/health')
def health():
    return jsonify({
        'status': 'UP',
        'service': 'ml-model-service',
        'models_loaded': len(models),
        'timestamp': datetime.utcnow().isoformat()
    })
```

### Test All Health Endpoints

```bash
#!/bin/bash
echo "🏥 Checking Production Service Health..."

SERVICES=(
  "https://model-service-XXXXX-uc.a.run.app/api/health"
  "https://ml-model-service-XXXXX-uc.a.run.app/health"
  "https://pollen-service.onrender.com/actuator/health"
  "https://weather-airpollution-service.onrender.com/actuator/health"
  "https://userpreference-service.onrender.com/actuator/health"
)

for service in "${SERVICES[@]}"; do
  echo "Testing $service..."
  curl -s "$service" | jq .
done
```

---

## 📊 Monitoring & Logging

### Google Cloud Run Monitoring

```bash
# View logs
gcloud run logs read model-service --limit 50 --region us-central1

# Real-time logs
gcloud run logs tail model-service --region us-central1

# Check metrics
gcloud run services describe model-service --region us-central1
```

### Render.com Monitoring

1. **Dashboard**: https://dashboard.render.com
2. Navigate to each service
3. View **Logs** tab for real-time logs
4. View **Metrics** tab for CPU/Memory usage

### Setup Alerts (Google Cloud)

```bash
# Create alert policy for high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High Error Rate - Model Service" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=60s
```

---

## 📈 Scaling Configuration

### Google Cloud Run Auto-scaling

```bash
# Update scaling settings
gcloud run services update model-service \
  --region us-central1 \
  --min-instances 1 \
  --max-instances 20 \
  --cpu 2 \
  --memory 1Gi \
  --concurrency 80
```

**Scaling Strategy**:
- **Min instances**: 1 (keep warm, avoid cold starts)
- **Max instances**: 20 (prevent runaway costs)
- **Concurrency**: 80 requests per instance
- **CPU**: 2 vCPU for faster processing
- **Memory**: 1-2Gi depending on service

### Render.com Scaling

**Free Tier Limitations**:
- Services spin down after 15 minutes of inactivity
- 750 hours/month free (enough for 1 service)
- Cold start: ~30 seconds

**Upgrade to Starter/Standard**:
- Always-on instances
- Horizontal auto-scaling
- More memory and CPU

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Service Timeout on Render

**Problem**: Service returns 502/504 errors

**Solution**:
```yaml
# render.yaml - increase health check timeout
healthCheckPath: /actuator/health
healthCheckTimeout: 30  # seconds
```

#### 2. Database Connection Failures

**Problem**: Services can't connect to PostgreSQL

**Solution**:
```bash
# Check DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql://user:pass@host:5432/dbname

# Test connection
psql "$DATABASE_URL"

# Verify service has environment variable
# Render Dashboard → Service → Environment → Check DATABASE_URL
```

#### 3. Cold Starts on Cloud Run

**Problem**: First request takes 10+ seconds

**Solution**:
```bash
# Set minimum instances to 1
gcloud run services update model-service \
  --region us-central1 \
  --min-instances 1
```

#### 4. Out of Memory (Cloud Run)

**Problem**: Service crashes with OOM error

**Solution**:
```bash
# Increase memory allocation
gcloud run services update ml-model-service \
  --region us-central1 \
  --memory 4Gi
```

#### 5. CORS Errors from Flutter App

**Problem**: Browser blocks API requests

**Solution**:
```java
// Add CORS configuration to Spring Boot
@Configuration
public class CorsConfig {
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/**")
                    .allowedOrigins("*")
                    .allowedMethods("GET", "POST", "PUT", "DELETE");
            }
        };
    }
}
```

---

## ✅ Deployment Checklist

- [ ] Create Render.com account
- [ ] Create Google Cloud account
- [ ] Obtain Google API key
- [ ] Create PostgreSQL database on Render
- [ ] Initialize database schema
- [ ] Deploy User Preference Service to Render
- [ ] Deploy Pollen Service to Render
- [ ] Deploy Weather Service to Render
- [ ] Deploy Model Orchestration Service to Cloud Run
- [ ] Deploy ML Model Service to Cloud Run
- [ ] Configure all environment variables
- [ ] Test all health endpoints
- [ ] Test end-to-end prediction flow
- [ ] Setup monitoring and alerts
- [ ] Configure auto-scaling
- [ ] Update Flutter app with production URLs
- [ ] Test mobile app with production backend

---

## 🔐 Security Best Practices

1. **API Keys**: Never commit to Git
   - Use Render environment variables
   - Use Google Secret Manager for Cloud Run

2. **Database**: 
   - Use internal connection strings when possible
   - Restrict IP access if needed
   - Enable SSL connections

3. **HTTPS**: 
   - Enforced by default on Render and Cloud Run
   - Use `https://` in all service URLs

4. **Authentication**:
   - Implement JWT/OAuth for user endpoints
   - Use API keys for service-to-service communication

---

## 💰 Cost Estimation

### Free Tier (Render + Google Cloud)

| Service | Provider | Plan | Cost |
|---------|----------|------|------|
| PostgreSQL | Render | Free | $0 |
| User Service | Render | Free | $0 |
| Pollen Service | Render | Free | $0 |
| Weather Service | Render | Free | $0 |
| Model Service | Google Cloud Run | Free tier | $0* |
| ML Service | Google Cloud Run | Free tier | $0* |
| **Total** | | | **$0-5/month** |

\* Google Cloud Run free tier: 2M requests/month, 360k GB-seconds

### Production (Recommended)

| Service | Provider | Plan | Cost/Month |
|---------|----------|------|------------|
| PostgreSQL | Render | Starter | $7 |
| 3x Java Services | Render | Starter | $21 |
| Model Service | Cloud Run | Pay-as-you-go | $10-30 |
| ML Service | Cloud Run | Pay-as-you-go | $20-50 |
| **Total** | | | **$58-108/month** |

---

## 📚 Next Steps

1. **Monitor Performance**: Setup dashboards for response times
2. **Optimize Costs**: Review usage and downgrade unused services
3. **Setup CI/CD**: Automate deployments with GitHub Actions
4. **Add Caching**: Implement Redis for frequently accessed data
5. **Load Testing**: Use tools like k6 or Locust to test capacity

---

## 🆘 Support

- **Render Docs**: https://render.com/docs
- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **Project Issues**: https://github.com/eduymaz/allermind/issues

---

**🎉 Congratulations! Your AllerMind production deployment is complete.**
