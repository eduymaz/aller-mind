# 🐳 AllerMind Docker Configuration Guide

Comprehensive guide to Docker setup, configuration, and management for AllerMind's microservices architecture.

---

## 📋 Table of Contents

1. [Docker Architecture Overview](#-docker-architecture-overview)
2. [Docker Compose Configuration](#-docker-compose-configuration)
3. [Individual Service Dockerfiles](#-individual-service-dockerfiles)
4. [Networking & Communication](#-networking--communication)
5. [Volume Management](#-volume-management)
6. [Build Optimization](#-build-optimization)
7. [Development vs Production](#-development-vs-production)
8. [Docker Commands Reference](#-docker-commands-reference)
9. [Troubleshooting](#-troubleshooting)

---

## 🏗️ Docker Architecture Overview

### Container Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Docker Compose Network                      │
│                     (allermind_network)                      │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐ │
│  │   PostgreSQL   │  │  Model Service │  │  ML Service   │ │
│  │   Container    │  │   Container    │  │   Container   │ │
│  │   Port: 5432   │  │   Port: 8484   │  │  Port: 8585   │ │
│  └────────────────┘  └────────────────┘  └───────────────┘ │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐ │
│  │ Pollen Service │  │ Weather Service│  │  User Service │ │
│  │   Container    │  │   Container    │  │   Container   │ │
│  │   Port: 8282   │  │   Port: 8383   │  │  Port: 9191   │ │
│  └────────────────┘  └────────────────┘  └───────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Shared Volume: postgres_data               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Services Breakdown

| Service | Image | Base OS | Runtime | Port | Memory |
|---------|-------|---------|---------|------|--------|
| **postgres** | postgres:15 | Debian | PostgreSQL 15 | 5432 | 512MB |
| **model-service** | Custom (Java) | Eclipse Temurin 21 | Spring Boot | 8484 | 512MB |
| **ml-model-service** | Custom (Python) | Python 3.11-slim | Flask | 8585 | 1GB |
| **pollen-service** | Custom (Java) | Eclipse Temurin 21 | Spring Boot | 8282 | 512MB |
| **weather-service** | Custom (Java) | Eclipse Temurin 21 | Spring Boot | 8383 | 512MB |
| **userpreference-service** | Custom (Java) | Eclipse Temurin 21 | Spring Boot | 9191 | 512MB |

---

## 🔧 Docker Compose Configuration

### Complete docker-compose.yml

```yaml
version: '3.8'

# Define custom network for inter-service communication
networks:
  allermind_network:
    driver: bridge

# Persistent volumes
volumes:
  postgres_data:
    driver: local

services:
  # ============================================
  # PostgreSQL Database
  # ============================================
  postgres:
    image: postgres:15-alpine
    container_name: allermind-postgres
    restart: unless-stopped
    networks:
      - allermind_network
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: allermind
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD:-password}
      POSTGRES_INITDB_ARGS: "--encoding=UTF8"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/init-db.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ============================================
  # Model Orchestration Service (Java/Spring Boot)
  # ============================================
  model-service:
    build:
      context: ./model-microservice
      dockerfile: Dockerfile
      args:
        JAR_FILE: target/*.jar
    container_name: allermind-model-service
    restart: unless-stopped
    networks:
      - allermind_network
    ports:
      - "8484:8484"
    environment:
      SPRING_PROFILES_ACTIVE: docker
      SERVER_PORT: 8484
      ML_MODEL_URL: http://ml-model-service:8585
      POLLEN_URL: http://pollen-service:8282
      WEATHER_URL: http://weather-service:8383
      USER_PREF_URL: http://userpreference-service:9191
    depends_on:
      postgres:
        condition: service_healthy
      ml-model-service:
        condition: service_started
      pollen-service:
        condition: service_started
      weather-service:
        condition: service_started
      userpreference-service:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8484/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # ============================================
  # ML Model Service (Python/Flask)
  # ============================================
  ml-model-service:
    build:
      context: ./ml-model-microservice
      dockerfile: Dockerfile
    container_name: allermind-ml-service
    restart: unless-stopped
    networks:
      - allermind_network
    ports:
      - "8585:8585"
    environment:
      FLASK_ENV: production
      PORT: 8585
      MODEL_PATH: /app/models
    volumes:
      - ./ml-model-microservice/models:/app/models:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8585/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # ============================================
  # Pollen Service (Java/Spring Boot)
  # ============================================
  pollen-service:
    build:
      context: ./pollen-microservice
      dockerfile: Dockerfile
    container_name: allermind-pollen-service
    restart: unless-stopped
    networks:
      - allermind_network
    ports:
      - "8282:8282"
    environment:
      SPRING_PROFILES_ACTIVE: docker
      SERVER_PORT: 8282
      GOOGLE_API_KEY: ${GOOGLE_API_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8282/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # ============================================
  # Weather & Air Quality Service (Java/Spring Boot)
  # ============================================
  weather-service:
    build:
      context: ./weather-airpollution-microservice
      dockerfile: Dockerfile
    container_name: allermind-weather-service
    restart: unless-stopped
    networks:
      - allermind_network
    ports:
      - "8383:8383"
    environment:
      SPRING_PROFILES_ACTIVE: docker
      SERVER_PORT: 8383
      GOOGLE_API_KEY: ${GOOGLE_API_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8383/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # ============================================
  # User Preference Service (Java/Spring Boot)
  # ============================================
  userpreference-service:
    build:
      context: ./userpreference-microservice
      dockerfile: Dockerfile
    container_name: allermind-userpreference-service
    restart: unless-stopped
    networks:
      - allermind_network
    ports:
      - "9191:9191"
    environment:
      SPRING_PROFILES_ACTIVE: docker
      SERVER_PORT: 9191
      DATABASE_URL: jdbc:postgresql://postgres:5432/allermind
      DATABASE_USER: postgres
      DATABASE_PASSWORD: ${DB_PASSWORD:-password}
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9191/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
```

### Environment Variables (.env)

```bash
# .env file (root directory)
# DO NOT commit this file to git!

# Database Configuration
DB_PASSWORD=your_secure_password_here

# Google API Key
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Override service ports
# MODEL_SERVICE_PORT=8484
# ML_SERVICE_PORT=8585
# POLLEN_SERVICE_PORT=8282
# WEATHER_SERVICE_PORT=8383
# USER_SERVICE_PORT=9191

# Optional: Java Memory Settings
JAVA_OPTS=-Xmx512m -Xms256m

# Optional: Python Settings
PYTHONUNBUFFERED=1
```

---

## 📦 Individual Service Dockerfiles

### 1. Java Spring Boot Services (Multi-stage Build)

**Dockerfile for model-microservice, pollen-microservice, weather-airpollution-microservice, userpreference-microservice:**

```dockerfile
# ==========================================
# Stage 1: Build Stage
# ==========================================
FROM eclipse-temurin:21-jdk-alpine AS builder

# Set working directory
WORKDIR /app

# Copy Maven wrapper and pom.xml
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./

# Download dependencies (cached layer)
RUN ./mvnw dependency:go-offline -B

# Copy source code
COPY src ./src

# Build application (skip tests for faster builds)
RUN ./mvnw clean package -DskipTests

# ==========================================
# Stage 2: Runtime Stage
# ==========================================
FROM eclipse-temurin:21-jre-alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Create non-root user
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# Set working directory
WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Expose port (overridden by docker-compose)
EXPOSE 8484

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s \
  CMD curl -f http://localhost:8484/actuator/health || exit 1

# Run application
ENTRYPOINT ["java", \
  "-XX:+UseContainerSupport", \
  "-XX:MaxRAMPercentage=75.0", \
  "-Djava.security.egd=file:/dev/./urandom", \
  "-jar", "app.jar"]
```

**Optimizations**:
- **Multi-stage build**: Smaller final image (~200MB vs 600MB)
- **Dependency caching**: Faster rebuilds by caching Maven dependencies
- **JVM memory tuning**: `-XX:MaxRAMPercentage=75.0` for container environments
- **Non-root user**: Security best practice
- **Health check**: Automatic container health monitoring

### 2. Python Flask ML Service

**Dockerfile for ml-model-microservice:**

```dockerfile
# ==========================================
# Stage 1: Build Stage
# ==========================================
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies to /install
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==========================================
# Stage 2: Runtime Stage
# ==========================================
FROM python:3.11-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 flask
USER flask

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY --chown=flask:flask app.py model_loader.py ./
COPY --chown=flask:flask models/ ./models/

# Expose port
EXPOSE 8585

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD curl -f http://localhost:8585/health || exit 1

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8585 \
    MODEL_PATH=/app/models

# Run application with gunicorn (production-ready WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:8585", "--workers", "2", "--threads", "4", "--timeout", "120", "app:app"]
```

**requirements.txt:**

```txt
Flask==3.0.0
gunicorn==21.2.0
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.26.2
joblib==1.3.2
```

**Optimizations**:
- **Multi-stage build**: Removes build tools from final image
- **Gunicorn**: Production-grade WSGI server (2 workers, 4 threads)
- **Non-root user**: Security best practice
- **Model volume mount**: Models loaded from persistent volume

### 3. PostgreSQL (Using Official Image)

**postgres/init-db.sql:**

```sql
-- Initialize AllerMind Database Schema

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Preferences Table
CREATE TABLE IF NOT EXISTS user_preferences (
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

-- Prediction History Table
CREATE TABLE IF NOT EXISTS prediction_history (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES user_preferences(user_id) ON DELETE CASCADE,
    location_lat DOUBLE PRECISION NOT NULL,
    location_lng DOUBLE PRECISION NOT NULL,
    city_name VARCHAR(255),
    predicted_safe_time INTEGER NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    environmental_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- City Cache Table
CREATE TABLE IF NOT EXISTS city_cache (
    id BIGSERIAL PRIMARY KEY,
    city_name VARCHAR(255) UNIQUE NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    country_code VARCHAR(10),
    timezone VARCHAR(100),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_prediction_history_user_id ON prediction_history(user_id);
CREATE INDEX IF NOT EXISTS idx_prediction_history_created_at ON prediction_history(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_city_cache_name ON city_cache(city_name);

-- Insert sample data (optional)
INSERT INTO user_preferences (user_id, age, allergy_types, sensitivity_level, activity_level)
VALUES 
    ('test_user_1', 30, ARRAY['pollen', 'dust'], 3, 'moderate'),
    ('test_user_2', 45, ARRAY['pollution', 'uv'], 4, 'high')
ON CONFLICT (user_id) DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Display summary
DO $$
BEGIN
    RAISE NOTICE 'AllerMind database initialized successfully!';
    RAISE NOTICE 'Tables created: user_preferences, prediction_history, city_cache';
    RAISE NOTICE 'Sample users added: test_user_1, test_user_2';
END $$;
```

---

## 🌐 Networking & Communication

### Docker Network Configuration

```yaml
networks:
  allermind_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Service Discovery

Services communicate using **container names** as hostnames:

```java
// Java services use container names in URLs
@Value("${ML_MODEL_URL:http://ml-model-service:8585}")
private String mlModelUrl;

@Value("${POLLEN_URL:http://pollen-service:8282}")
private String pollenUrl;
```

**Example**: When `model-service` calls `ml-model-service`:
```
http://ml-model-service:8585/predict
```

Docker DNS resolves `ml-model-service` to container IP.

### Port Mapping

| Container Port | Host Port | Access From Host |
|----------------|-----------|------------------|
| postgres:5432 | 5432 | localhost:5432 |
| model-service:8484 | 8484 | localhost:8484 |
| ml-model-service:8585 | 8585 | localhost:8585 |
| pollen-service:8282 | 8282 | localhost:8282 |
| weather-service:8383 | 8383 | localhost:8383 |
| userpreference-service:9191 | 9191 | localhost:9191 |

---

## 💾 Volume Management

### Persistent Volumes

```yaml
volumes:
  postgres_data:
    driver: local
```

**Data Location** (macOS):
```
/var/lib/docker/volumes/aller-mind_postgres_data/_data
```

### Bind Mounts

```yaml
volumes:
  # Read-only model files
  - ./ml-model-microservice/models:/app/models:ro
  
  # Database initialization script
  - ./postgres/init-db.sql:/docker-entrypoint-initdb.d/init.sql:ro
```

### Volume Operations

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect aller-mind_postgres_data

# Backup database volume
docker run --rm -v aller-mind_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup-$(date +%Y%m%d).tar.gz /data

# Restore database volume
docker run --rm -v aller-mind_postgres_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/postgres-backup-20251018.tar.gz -C /

# Remove volume (dangerous!)
docker volume rm aller-mind_postgres_data
```

---

## ⚡ Build Optimization

### Layer Caching Strategy

**Before (inefficient)**:
```dockerfile
COPY . .
RUN mvn clean package
```

**After (optimized)**:
```dockerfile
# Dependencies layer (cached unless pom.xml changes)
COPY pom.xml .
RUN mvn dependency:go-offline

# Source code layer (frequently changes)
COPY src ./src
RUN mvn package -DskipTests
```

### .dockerignore Files

**Java services (.dockerignore)**:
```
# Build artifacts
target/
*.class
*.jar
*.war

# IDE files
.idea/
.vscode/
*.iml

# OS files
.DS_Store
Thumbs.db

# Git
.git/
.gitignore

# Docker
Dockerfile
docker-compose.yml

# Documentation
README.md
*.md
```

**Python service (.dockerignore)**:
```
# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage

# Documentation
README.md
*.md

# Models (if large, mount as volume instead)
# models/*.pkl
```

### Build Performance Tips

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker-compose build

# Build specific service
docker-compose build model-service

# Build without cache (clean build)
docker-compose build --no-cache

# Parallel builds
docker-compose build --parallel
```

---

## 🔄 Development vs Production

### Development Configuration

**docker-compose.dev.yml**:
```yaml
version: '3.8'

services:
  model-service:
    build:
      context: ./model-microservice
      target: builder  # Use builder stage for hot reload
    volumes:
      - ./model-microservice/src:/app/src
    environment:
      SPRING_DEVTOOLS_RESTART_ENABLED: "true"
      
  ml-model-service:
    volumes:
      - ./ml-model-microservice:/app
    environment:
      FLASK_ENV: development
      FLASK_DEBUG: "1"
    command: flask run --host=0.0.0.0 --port=8585
```

**Usage**:
```bash
# Development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production mode
docker-compose up
```

### Production Configuration

**docker-compose.prod.yml**:
```yaml
version: '3.8'

services:
  model-service:
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
          
  ml-model-service:
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

---

## 📝 Docker Commands Reference

### Starting Services

```bash
# Start all services
docker-compose up

# Start in background (detached mode)
docker-compose up -d

# Start specific service
docker-compose up model-service

# Force rebuild before starting
docker-compose up --build

# Scale specific service (if stateless)
docker-compose up --scale ml-model-service=3
```

### Stopping Services

```bash
# Stop all services (graceful shutdown)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v

# Stop specific service
docker-compose stop model-service
```

### Viewing Logs

```bash
# View all logs
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# Logs for specific service
docker-compose logs -f model-service

# Last 100 lines
docker-compose logs --tail=100

# Logs with timestamps
docker-compose logs -t
```

### Executing Commands

```bash
# Open bash in running container
docker-compose exec model-service bash

# Run command in container
docker-compose exec postgres psql -U postgres -d allermind

# Run one-off command (creates temporary container)
docker-compose run --rm model-service curl http://ml-model-service:8585/health
```

### Inspecting Services

```bash
# List running containers
docker-compose ps

# Show container details
docker-compose ps model-service

# Check resource usage
docker stats

# Inspect network
docker network inspect aller-mind_allermind_network
```

### Cleaning Up

```bash
# Remove stopped containers
docker-compose rm

# Remove all (containers, networks, images)
docker-compose down --rmi all

# Prune unused Docker resources
docker system prune

# Prune everything (including volumes)
docker system prune -a --volumes
```

---

## 🐛 Troubleshooting

### 1. Service Won't Start

**Check logs**:
```bash
docker-compose logs model-service
```

**Common issues**:
- Port already in use: `lsof -ti:8484 | xargs kill -9`
- Missing environment variables: Check `.env` file
- Database not ready: Wait for health check

### 2. Container Crashes Immediately

```bash
# Check exit code
docker-compose ps

# View full logs
docker-compose logs --tail=all model-service

# Check container events
docker events --since 1h
```

### 3. Network Issues Between Containers

```bash
# Verify network exists
docker network ls | grep allermind

# Check container network config
docker inspect allermind-model-service | jq '.[0].NetworkSettings'

# Test connectivity
docker-compose exec model-service ping ml-model-service
```

### 4. Database Connection Refused

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check health status
docker-compose exec postgres pg_isready -U postgres

# Connect to database
docker-compose exec postgres psql -U postgres -d allermind

# Check tables
docker-compose exec postgres psql -U postgres -d allermind -c "\dt"
```

### 5. Out of Disk Space

```bash
# Check Docker disk usage
docker system df

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Clean build cache
docker builder prune
```

### 6. Slow Builds

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Use build cache
docker-compose build --parallel

# Check .dockerignore is configured
```

### 7. Memory Issues

```bash
# Check memory limits
docker stats

# Increase Docker memory (Docker Desktop)
# Settings → Resources → Memory → 4GB+

# Set JVM memory limits
JAVA_OPTS="-Xmx512m -Xms256m"
```

---

## 📊 Monitoring & Metrics

### Container Health Monitoring

```bash
# Watch health status
watch docker-compose ps

# Health check logs
docker inspect --format='{{json .State.Health}}' allermind-model-service | jq
```

### Resource Monitoring

```bash
# Real-time stats
docker stats

# Export stats to CSV
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" > stats.csv
```

### Log Aggregation (Optional)

```yaml
# docker-compose.yml - add logging driver
services:
  model-service:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 🔐 Security Best Practices

1. **Non-root users**: All Dockerfiles use dedicated users
2. **Secret management**: Use `.env` file (never commit)
3. **Network isolation**: Services on private bridge network
4. **Read-only filesystems**: Mount sensitive files as `:ro`
5. **Resource limits**: Set CPU/memory limits in production
6. **Image scanning**: Use `docker scan` to check for vulnerabilities

```bash
# Scan image for vulnerabilities
docker scan allermind-model-service
```

---

## 📚 Additional Resources

- **Docker Documentation**: https://docs.docker.com
- **Docker Compose Reference**: https://docs.docker.com/compose/compose-file/
- **Spring Boot Docker Guide**: https://spring.io/guides/topicals/spring-boot-docker/
- **Python Docker Best Practices**: https://docs.docker.com/language/python/

---

## ✅ Quick Reference Checklist

- [ ] Install Docker Desktop
- [ ] Create `.env` file with credentials
- [ ] Build all services: `docker-compose build`
- [ ] Start services: `docker-compose up -d`
- [ ] Check health: `docker-compose ps`
- [ ] View logs: `docker-compose logs -f`
- [ ] Test endpoints: `curl http://localhost:8484/api/health`
- [ ] Stop services: `docker-compose down`

---

**🐳 Docker setup complete! Ready to run!**
