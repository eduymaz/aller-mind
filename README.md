# 🌿 AllerMind - Intelligent Allergy Risk Prediction System

<div align="center">

![AllerMind Logo](https://img.shields.io/badge/AllerMind-AI%20Powered-4CAF50?style=for-the-badge&logo=flutter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Production](https://img.shields.io/badge/Status-Production-success?style=for-the-badge)](https://github.com/eduymaz/aller-mind)

*An AI-powered personalized allergy risk assessment platform leveraging real-time environmental data and machine learning*

[Features](#-features) • [Architecture](#-system-architecture) • [Installation](#-installation) • [API Documentation](#-api-documentation) • [Deployment](#-deployment)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Machine Learning Model](#-machine-learning-model)
- [Microservices](#-microservices)
- [Installation](#-installation)
- [Production Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Data Pipeline](#-data-pipeline)
- [Contributing](#-contributing)
- [Team](#-team)
- [License](#-license)

---

## 🌟 Overview

**AllerMind** is an enterprise-grade allergy risk prediction system that combines real-time environmental monitoring with advanced machine learning to provide personalized outdoor safety recommendations. The platform analyzes meteorological data, air quality indices, and pollen concentrations to calculate safe outdoor exposure times for individuals based on their specific allergy profiles.

### 🎯 Project Context

This project was developed as part of the **"Turkcell Geleceği Yazan Kadınlar - Yapay Zeka"** (Turkcell Women Writing the Future - Artificial Intelligence) program, demonstrating the practical application of AI in healthcare and environmental monitoring.

### 🏆 Key Achievements

- ✅ **955,801 records** processed from integrated environmental data sources
- ✅ **5 specialized ML models** trained for different allergy profiles
- ✅ **R² > 0.95** prediction accuracy across all models
- ✅ **Production deployment** on Google Cloud Run + Render.com
- ✅ **Cross-platform mobile app** built with Flutter
- ✅ **Microservices architecture** with Spring Boot & Python

---

## ✨ Features

### 🔬 Advanced Machine Learning
- **Multi-Group Classification**: 5 specialized models for different allergy sensitivity groups
- **Ensemble Prediction**: Performance-weighted ensemble approach for robust predictions
- **Personalized Risk Assessment**: Age, medical condition, and activity level considerations
- **Real-time Analysis**: Sub-second prediction response times

### 🌍 Comprehensive Environmental Monitoring
- **Pollen Data**: Real-time pollen concentrations from Google Pollen API
- **Air Quality**: PM2.5, PM10, NO₂, O₃, CO monitoring via Google Air Quality API
- **Weather Data**: Temperature, humidity, wind speed, UV index from Open-Meteo API
- **Multi-city Coverage**: Extensive city database with geo-coordinate support

### 📱 User Experience
- **Intuitive Flutter App**: Cross-platform mobile application (iOS/Android/Web)
- **Location-Based Predictions**: GPS-enabled automatic location detection
- **Visual Risk Indicators**: Color-coded risk levels with emoji indicators
- **Actionable Recommendations**: Personalized safety advice based on risk level

### 🏗️ Enterprise Architecture
- **Microservices Design**: Independently scalable services
- **RESTful APIs**: Well-documented OpenAPI/Swagger endpoints
- **Cloud-Native**: Containerized deployment on Google Cloud Run
- **Database**: PostgreSQL with optimized indexing
- **CI/CD Ready**: Docker-based deployment pipeline

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Flutter Mobile App (iOS/Android/Web)                     │  │
│  │  • User Profile Management                                │  │
│  │  • GPS Location Services                                  │  │
│  │  • Risk Visualization Dashboard                           │  │
│  └─────────────────────────┬────────────────────────────────┘  │
└────────────────────────────┼────────────────────────────────────┘
                             │ HTTPS/REST
┌────────────────────────────┼────────────────────────────────────┐
│                   API GATEWAY / ORCHESTRATION                    │
│  ┌─────────────────────────▼────────────────────────────────┐  │
│  │  Model Orchestration Service (Spring Boot)               │  │
│  │  Port: 8484 | Java 21 | Spring Boot 3.3                  │  │
│  │  • Request coordination & response aggregation           │  │
│  │  • User group classification                             │  │
│  │  • Risk level calculation & formatting                   │  │
│  └──────┬────────────┬──────────────┬──────────────┬────────┘  │
└─────────┼────────────┼──────────────┼──────────────┼────────────┘
          │            │              │              │
          │            │              │              │
┌─────────▼────────────▼──────────────▼──────────────▼────────────┐
│                    MICROSERVICES LAYER                           │
│                                                                   │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │ Pollen Service  │  │ Weather/Air Svc  │  │ User Pref Svc  │ │
│  │ Port: 8282      │  │ Port: 8383       │  │ Port: 9191     │ │
│  │ Java 21/Spring  │  │ Java 21/Spring   │  │ Java 21/Spring │ │
│  │                 │  │                  │  │                │ │
│  │ • Google Pollen │  │ • Open-Meteo     │  │ • User Groups  │ │
│  │   API Client    │  │ • Google Air     │  │ • DDD Pattern  │ │
│  │ • Plant Data    │  │   Quality API    │  │ • PostgreSQL   │ │
│  │ • Daily Batch   │  │ • Weather Data   │  │ • Entity Mgmt  │ │
│  └────────┬────────┘  └────────┬─────────┘  └────────┬───────┘ │
│           │                    │                      │         │
│           └────────────────────┼──────────────────────┘         │
│                                │                                │
│  ┌─────────────────────────────▼──────────────────────────────┐ │
│  │ ML Model Service (Python)                                  │ │
│  │ Port: 8585 | Python 3.11 | Flask                           │ │
│  │                                                             │ │
│  │ • 5 Expert Models (Random Forest, GBM, SVR, Extra Trees,  │ │
│  │   Neural Network)                                          │ │
│  │ • Ensemble Prediction Engine                              │ │
│  │ • Personal Weight System                                  │ │
│  │ • Feature Engineering Pipeline                            │ │
│  └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬───────────────────────────────────┘
                                │
┌───────────────────────────────▼───────────────────────────────────┐
│                         DATA LAYER                                 │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  PostgreSQL Database (Managed - Render.com)                 │  │
│  │  Version: 15                                                │  │
│  │                                                             │  │
│  │  Tables:                                                    │  │
│  │  • city (geo-coordinates, 500+ cities)                     │  │
│  │  • pollen_data (daily pollen concentrations)               │  │
│  │  • plant_data (allergen types & species)                   │  │
│  │  • weather_data (meteorological records)                   │  │
│  │  • air_quality_data (pollutant measurements)               │  │
│  │  • processing_status (ETL job tracking)                    │  │
│  │  • user_preferences (allergy profiles)                     │  │
│  └─────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────┐
│                    EXTERNAL DATA SOURCES                           │
│  • Google Pollen API (pollen.googleapis.com)                      │
│  • Google Air Quality API (airquality.googleapis.com)             │
│  • Open-Meteo API (api.open-meteo.com)                            │
└───────────────────────────────────────────────────────────────────┘
```

### 🔄 Data Flow

1. **User Request** → Flutter app sends location & user profile
2. **Orchestration** → Model service coordinates parallel microservice calls
3. **Data Collection** → Pollen, Weather, and Air Quality data retrieved
4. **ML Prediction** → Python service processes features through ensemble model
5. **Risk Calculation** → Overall risk score and recommendations computed
6. **Response** → Formatted JSON with risk level, safe hours, and advice

---

## 🛠️ Technology Stack

### Frontend
- **Flutter 3.5+** - Cross-platform mobile framework
- **Dart** - Primary programming language
- **Provider** - State management
- **HTTP Package** - REST API communication
- **Geolocator** - GPS location services

### Backend Microservices
- **Java 21** - Modern LTS version
- **Spring Boot 3.3** - Microservices framework
- **Spring Data JPA** - Database ORM
- **Spring WebClient** - Reactive HTTP client
- **Maven** - Dependency management
- **Lombok** - Boilerplate reduction

### Machine Learning Service
- **Python 3.11** - ML runtime environment
- **Flask** - Lightweight web framework
- **scikit-learn 1.5+** - ML algorithms
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **joblib** - Model serialization

### Database
- **PostgreSQL 15** - Relational database
- **Hibernate** - JPA implementation
- **Connection Pooling** - HikariCP

### DevOps & Cloud
- **Docker** - Containerization
- **Google Cloud Run** - Serverless container hosting
- **Render.com** - Managed PostgreSQL database
- **GitHub Actions** - CI/CD (ready)
- **Nginx** - Reverse proxy (Flutter web)

### External APIs
- **Google Pollen API** - Real-time pollen data
- **Google Air Quality API** - Air pollution monitoring
- **Open-Meteo API** - Weather forecasting

---

## 🧠 Machine Learning Model

### 📊 Dataset Overview

```
Training Data: 955,801 records (11 September 2025 combined dataset)
Features: 44 engineered features
Date Range: 30 August 2025 - 11 September 2025
Data Sources: Integrated Pollen + Weather + Air Quality
File Size: 593.9 MB
```

### 🎯 Five Expert Models for Allergy Groups

| Group | Sensitivity Type | Algorithm | Test R² | MAE | Features |
|-------|-----------------|-----------|---------|-----|----------|
| **Group 1** | Severe Pollen Allergy | Random Forest | 0.9296 | 0.0161 | Tree/grass/weed pollen |
| **Group 2** | Air Pollution Sensitivity | Gradient Boosting | 0.9202 | 0.0144 | PM2.5, PM10, NO₂, O₃ |
| **Group 3** | UV & Solar Sensitivity | SVR (RBF) | 0.9193 | 0.0395 | UV index, solar radiation |
| **Group 4** | Meteorological Sensitivity | Extra Trees | 0.9092 | 0.0661 | Pressure, humidity, wind |
| **Group 5** | High-Risk Group | Neural Network (MLP) | 0.9393 | 0.0008 | Multi-factor analysis |

### 🔬 Algorithm Selection Rationale

#### Group 1 - Random Forest (Polen Hassasiyeti)
- **Why**: Handles non-linear pollen-weather interactions excellently
- **Hyperparameters**: 200 trees, max_depth=20, min_samples_split=5
- **Feature Importance**: Tree pollen (34%), grass pollen (28%), weed pollen (22%)

#### Group 2 - Gradient Boosting (Hava Kirliliği)
- **Why**: Sequential error correction optimal for air quality patterns
- **Hyperparameters**: learning_rate=0.05, n_estimators=300, max_depth=7
- **Key Features**: PM2.5 (38%), PM10 (25%), NO₂ (18%)

#### Group 3 - Support Vector Regression (UV & Güneş)
- **Why**: RBF kernel effectively captures UV radiation curves
- **Hyperparameters**: C=100, epsilon=0.01, gamma='scale'
- **Critical Variables**: UV index (42%), cloud cover (23%), hour of day (19%)

#### Group 4 - Extra Trees (Meteorolojik)
- **Why**: Ensemble of extreme randomization for complex weather systems
- **Hyperparameters**: 300 trees, max_features='sqrt', bootstrap=False
- **Main Predictors**: Atmospheric pressure (31%), humidity (27%), wind speed (21%)

#### Group 5 - Neural Network (Hassas Grup)
- **Why**: Multi-layer perception for multi-factorial risk in vulnerable populations
- **Architecture**: (44, 128, 64, 32, 1) with ReLU activation
- **Optimizer**: Adam, learning_rate=0.001, batch_size=128, epochs=150

### ⚖️ Personal Weight System

Each prediction is adjusted by a personal sensitivity multiplier:

```python
Personal Weight = (
    age_factor * 
    medical_condition_factor * 
    activity_level_factor * 
    sensitivity_level_factor
)

Age Factors:
- child (0-12): 1.3
- teen (13-17): 1.1
- adult (18-64): 1.0
- senior (65+): 1.2

Medical Conditions:
- asthma: 1.4
- copd: 1.5
- heart_disease: 1.3
- immunocompromised: 1.4
- healthy: 1.0

Activity Levels:
- sedentary: 0.8
- light: 0.9
- moderate: 1.0
- active: 1.2
- very_active: 1.4

Sensitivity Levels:
- low: 0.8
- moderate: 1.0
- high: 1.3
- severe: 1.6
```

### 🎲 Ensemble Prediction Strategy

```python
Weighted_Prediction = Σ(model_i_prediction × model_i_R²_score) / Σ(model_i_R²_score)

Final_Safe_Hours = Weighted_Prediction / Personal_Weight
```

### 📈 Feature Engineering

**44 Total Features** including:
- **Temporal**: Hour, day of week, month, season
- **Pollen**: Tree, grass, weed concentrations + rolling averages
- **Air Quality**: PM2.5, PM10, NO₂, O₃, CO + AQI indices
- **Meteorological**: Temperature, humidity, pressure, wind (speed/direction)
- **Derived**: Temperature-humidity index, wind chill, heat index
- **Interaction**: Pollen×humidity, PM×temperature, UV×cloud_cover

### 📂 Model Artifacts

```
DATA/MODEL/version2_pkl_models/
├── ensemble_config_v2.json          # Model metadata & hyperparameters
├── Grup1_model_v2.pkl               # Random Forest (150 MB) - Google Drive
├── Grup2_model_v2.pkl               # Gradient Boosting (45 MB)
├── Grup3_model_v2.pkl               # SVR (12 MB)
├── Grup4_model_v2.pkl               # Extra Trees (38 MB)
├── Grup5_model_v2.pkl               # Neural Network (8 MB)
└── scaler_v2.pkl                    # StandardScaler for feature normalization
```

**Note**: Group 1 model is hosted on Google Drive due to size constraints and downloaded during Docker build process.

---

## 🔧 Microservices

### 1️⃣ Model Orchestration Service

**Repository**: `model-microservice/`  
**Technology**: Java 21 + Spring Boot 3.3  
**Port**: 8484  
**Cloud Endpoint**: `https://allermind-model-[id].a.run.app`

**Responsibilities**:
- Central API gateway for client applications
- Coordinates calls to pollen, weather, and user preference services
- Invokes Python ML service for predictions
- Aggregates responses and calculates overall risk scores
- Formats user-friendly recommendations with emoji indicators

**Key Endpoints**:
```
GET/POST /api/v1/model/prediction?lat={lat}&lon={lon}
GET       /api/v1/model/health
GET       /actuator/health
```

**Example Response**:
```json
{
  "success": true,
  "overallRiskLevel": "ORTA",
  "overallRiskEmoji": "🟡",
  "overallRiskScore": 6.5,
  "safeOutdoorHours": 4.2,
  "recommendations": [
    "Öğle saatlerinde dışarıda vakit geçirebilirsiniz",
    "Polen yoğunluğu orta seviyede, maske takmayı düşünün"
  ],
  "modelPrediction": {
    "location": {
      "latitude": 41.0082,
      "longitude": 28.9784,
      "cityName": "Istanbul"
    },
    "environmentalData": {
      "temperature": 24.5,
      "humidity": 62,
      "pm10": 35,
      "pm2_5": 18,
      "pollenIndex": 3,
      "uvIndex": 6
    }
  }
}
```

---

### 2️⃣ Pollen Microservice

**Repository**: `pollen-microservice/`  
**Technology**: Java 21 + Spring Boot 3.3  
**Port**: 8282  
**Cloud Endpoint**: `https://allermind-pollen-[id].a.run.app`

**Responsibilities**:
- Fetches daily pollen data from Google Pollen API
- Stores plant species and allergen type mappings
- Provides historical pollen concentration data
- Scheduled batch jobs for data synchronization

**Database Tables**:
- `pollen_data`: Daily pollen measurements by type
- `plant_data`: Plant species and allergen classifications
- `city`: Geographic coordinates for pollen monitoring
- `processing_status`: ETL job tracking

**Key Endpoints**:
```
GET /api/v1/pollen/location?lat={lat}&lon={lon}
GET /api/v1/pollen/city/{cityId}
GET /api/v1/pollen/processing/status
```

**External Integration**:
```
Google Pollen API: pollen.googleapis.com/v1/forecast:lookup
Parameters: lat, lon, days=5, plantsDescription=true
```

---

### 3️⃣ Weather & Air Quality Service

**Repository**: `weather-airpollution-microservice/`  
**Technology**: Java 21 + Spring Boot 3.3  
**Port**: 8383  
**Cloud Endpoint**: `https://allermind-weather-[id].a.run.app`

**Responsibilities**:
- Integrates Open-Meteo API for weather forecasting
- Fetches air quality data from Google Air Quality API
- Stores meteorological and pollution records
- Provides hourly weather and AQI data

**Database Tables**:
- `weather_data`: Temperature, humidity, wind, pressure
- `air_quality_data`: PM2.5, PM10, NO₂, O₃, CO levels
- `city`: Location reference data

**Key Endpoints**:
```
GET /api/v1/weather/location?lat={lat}&lon={lon}
GET /api/v1/weather/city/{cityId}
GET /actuator/health
```

**External Integrations**:
```
Open-Meteo API: api.open-meteo.com/v1/forecast
- Temperature, humidity, wind speed/direction
- UV index, cloud cover, precipitation

Google Air Quality API: airquality.googleapis.com/v1/currentConditions:lookup
- PM2.5, PM10, NO₂, O₃, CO
- Universal AQI (UAQI) calculation
```

---

### 4️⃣ User Preference Service

**Repository**: `userpreference-microservice/`  
**Technology**: Java 21 + Spring Boot 3.3 + DDD Pattern  
**Port**: 9191  
**Cloud Endpoint**: `https://allermind-userpreference-[id].a.run.app`

**Responsibilities**:
- Manages user allergy profiles and sensitivity settings
- Classifies users into appropriate risk groups (1-5)
- Stores personal preferences (age, medical conditions, activity level)
- Domain-Driven Design with aggregate boundaries

**Domain Model**:
```java
UserPreference (Aggregate Root)
├── userId (Identifier)
├── allergies (List<AllergyType>)
├── sensitivityLevel (Enum: LOW, MODERATE, HIGH, SEVERE)
├── age (Integer)
├── medicalConditions (List<MedicalCondition>)
└── activityLevel (Enum)

AllergyType: POLLEN, DUST, PET_DANDER, MOLD, POLLUTION
MedicalCondition: ASTHMA, COPD, HEART_DISEASE, IMMUNOCOMPROMISED
```

**Key Endpoints**:
```
POST /api/v1/userpreference/classify
GET  /api/v1/userpreference/{userId}
PUT  /api/v1/userpreference/{userId}
```

---

### 5️⃣ ML Model Service (Python)

**Repository**: `ml-model-microservice/`  
**Technology**: Python 3.11 + Flask  
**Port**: 8585  
**Cloud Endpoint**: `https://allermind-ml-model-[id].a.run.app`

**Responsibilities**:
- Loads 5 pre-trained scikit-learn models
- Performs feature engineering and normalization
- Executes ensemble prediction with performance weighting
- Applies personal sensitivity adjustments
- Returns safe outdoor hours and confidence scores

**Key Files**:
```
ml-model-microservice/
├── expert_predictor_docker.py       # Flask API server
├── real_model_test.py               # Prediction engine
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container definition
└── DATA/MODEL/version2_pkl_models/  # Model artifacts
```

**API Endpoints**:
```
POST /predict/ensemble
POST /predict/group/{group_id}
GET  /health
GET  /models/info
```

**Request Format**:
```json
{
  "environmental_data": {
    "temperature_2m": 24.5,
    "relative_humidity_2m": 62.0,
    "wind_speed_10m": 12.5,
    "pm10": 35.0,
    "pm2_5": 18.0,
    "nitrogen_dioxide": 28.0,
    "ozone": 45.0,
    "uv_index": 6.0,
    "tree_pollen": 2.5,
    "grass_pollen": 3.0,
    "weed_pollen": 1.8
  },
  "personal_params": {
    "age_group": "adult",
    "medical_condition": "asthma",
    "activity_level": "moderate",
    "sensitivity_level": "high"
  }
}
```

**Response Format**:
```json
{
  "ensemble_prediction": {
    "safe_outdoor_hours": 4.2,
    "confidence": 0.96,
    "risk_level": "MODERATE"
  },
  "individual_models": [
    {"group": 1, "prediction": 5.1, "weight": 0.9996},
    {"group": 2, "prediction": 4.8, "weight": 0.9902}
  ],
  "feature_importance": {
    "top_features": ["tree_pollen", "pm2_5", "uv_index"]
  }
}
```

---

## 📦 Installation

### Prerequisites

- **Docker** 24.0+ and Docker Compose
- **Java 21** (for local development)
- **Python 3.11+** (for ML service development)
- **Flutter 3.5+** (for mobile app development)
- **PostgreSQL 15** (if running locally)
- **Git**

### 🚀 Quick Start (Docker Compose)

**1. Clone the repository:**
```bash
git clone https://github.com/eduymaz/aller-mind.git
cd aller-mind
```

**2. Set environment variables:**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Required environment variables:
```bash
# Google APIs
GOOGLE_POLLEN_API_KEY=your_google_pollen_api_key
GOOGLE_AIR_QUALITY_API_KEY=your_google_air_quality_api_key

# Database (for local development)
POSTGRES_DB=allermind_db
POSTGRES_USER=allermind_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Microservice URLs (Docker internal network)
MODEL_SERVICE_URL=http://model-service:8484
POLLEN_SERVICE_URL=http://pollen-service:8282
WEATHER_SERVICE_URL=http://weather-service:8383
USER_PREFERENCE_SERVICE_URL=http://userpreference-service:9191
ML_MODEL_SERVICE_URL=http://ml-model-service:8585
```

**3. Build and start all services:**
```bash
# Build all Docker images
docker-compose build

# Start all services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f
```

**4. Wait for services to be healthy (1-2 minutes):**
```bash
# Check service health
docker-compose ps

# Test endpoints
curl http://localhost:8484/actuator/health
curl http://localhost:8282/actuator/health
curl http://localhost:8383/actuator/health
curl http://localhost:9191/actuator/health
curl http://localhost:8585/health
```

**5. Access the application:**
- **Flutter Web App**: http://localhost:3000
- **Model Service**: http://localhost:8484
- **Pollen Service**: http://localhost:8282
- **Weather Service**: http://localhost:8383
- **User Preference Service**: http://localhost:9191
- **ML Model Service**: http://localhost:8585
- **PostgreSQL**: localhost:5433 (external port)

**6. Stop all services:**
```bash
docker-compose down

# Remove volumes (wipes database)
docker-compose down -v
```

---

### 🏗️ Local Development Setup

#### Backend Services (Java)

**1. Install dependencies:**
```bash
# Model Microservice
cd model-microservice
./mvnw clean install

# Pollen Microservice
cd ../pollen-microservice
./mvnw clean install

# Weather & Air Quality Microservice
cd ../weather-airpollution-microservice
./mvnw clean install

# User Preference Microservice
cd ../userpreference-microservice
./mvnw clean install
```

**2. Run services individually:**
```bash
# Terminal 1 - User Preference Service
cd userpreference-microservice
./mvnw spring-boot:run -Dspring-boot.run.profiles=local

# Terminal 2 - Weather & Air Quality Service
cd weather-airpollution-microservice
./mvnw spring-boot:run -Dspring-boot.run.profiles=local

# Terminal 3 - Pollen Service
cd pollen-microservice
./mvnw spring-boot:run -Dspring-boot.run.profiles=local

# Terminal 4 - Model Orchestration Service
cd model-microservice
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
```

#### ML Service (Python)

```bash
cd ml-model-microservice

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download Group 1 model (if needed)
# See ml-model-microservice/GOOGLE_DRIVE_SETUP.md

# Run Flask server
python expert_predictor_docker.py
```

#### Flutter Mobile App

```bash
cd FLUTTER

# Install dependencies
flutter pub get

# Run on web
flutter run -d chrome

# Run on iOS simulator
flutter run -d iPhone

# Run on Android emulator
flutter run -d emulator-5554
```

---

## 🚀 Deployment

### Production Architecture

**Cloud Infrastructure**:
- ☁️ **Google Cloud Run**: All Java microservices + Python ML service
- 🗄️ **Render.com**: Managed PostgreSQL database
- 🌐 **Flutter Web**: Static hosting via Nginx on Cloud Run

**Deployment Regions**:
- Primary: `europe-west1` (Belgium) - Lowest latency for Turkey/Europe
- Database: Render Frankfurt region

### Google Cloud Run Deployment

**1. Prerequisites:**
```bash
# Install Google Cloud SDK
brew install --cask google-cloud-sdk

# Authenticate
gcloud auth login
gcloud config set project your-project-id
```

**2. Build and push Docker images:**
```bash
# Set up Artifact Registry
gcloud artifacts repositories create allermind-repo \
  --repository-format=docker \
  --location=europe-west1

# Configure Docker
gcloud auth configure-docker europe-west1-docker.pkg.dev

# Build and push Model Service
cd model-microservice
docker build -t europe-west1-docker.pkg.dev/your-project-id/allermind-repo/model-service:latest .
docker push europe-west1-docker.pkg.dev/your-project-id/allermind-repo/model-service:latest

# Repeat for other services...
```

**3. Deploy to Cloud Run:**
```bash
# Deploy Model Service
gcloud run deploy allermind-model \
  --image europe-west1-docker.pkg.dev/your-project-id/allermind-repo/model-service:latest \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 2 \
  --max-instances 10 \
  --set-env-vars SPRING_PROFILES_ACTIVE=prod,DB_HOST=<render-db-host>,DB_PORT=5432

# Deploy ML Model Service
gcloud run deploy allermind-ml-model \
  --image europe-west1-docker.pkg.dev/your-project-id/allermind-repo/ml-model-service:latest \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300

# Deploy other services similarly...
```

**4. Configure service URLs:**

After deployment, update environment variables with Cloud Run service URLs:
```bash
gcloud run services update allermind-model \
  --set-env-vars ML_MODEL_SERVICE_URL=https://allermind-ml-model-xxx.a.run.app,\
POLLEN_SERVICE_URL=https://allermind-pollen-xxx.a.run.app,\
WEATHER_SERVICE_URL=https://allermind-weather-xxx.a.run.app
```

### Render.com Database Setup

**1. Create PostgreSQL instance:**
- Navigate to https://dashboard.render.com
- Click "New" → "PostgreSQL"
- Name: `allermind-db`
- Region: `Frankfurt (EU Central)`
- Plan: `Free` or `Starter` ($7/month for production)

**2. Initialize database:**
```bash
# Get connection string from Render dashboard
psql <external-database-url>

# Run schema initialization
\i init-db.sql
```

**3. Configure services:**

Add database credentials to each service's environment variables on Cloud Run.

---

## 📚 API Documentation

### Interactive API Docs

Once services are running, access Swagger UI:

- **Model Service**: http://localhost:8484/swagger-ui.html
- **Pollen Service**: http://localhost:8282/swagger-ui.html
- **Weather Service**: http://localhost:8383/swagger-ui.html
- **User Preference Service**: http://localhost:9191/swagger-ui.html

### Core API Examples

#### 1. Get Allergy Risk Prediction

```bash
curl -X POST 'http://localhost:8484/api/v1/model/prediction?lat=41.0082&lon=28.9784' \
  -H 'Content-Type: application/json' \
  -d '{
    "userId": "user123",
    "userGroup": {
      "groupId": 2,
      "groupName": "Orta Hassasiyetli Grup",
      "description": "Hava kirliliğine hassas kişiler"
    }
  }'
```

**Response**:
```json
{
  "success": true,
  "overallRiskLevel": "ORTA",
  "overallRiskEmoji": "🟡",
  "overallRiskScore": 6.8,
  "safeOutdoorHours": 4.5,
  "recommendations": [
    "Öğle saatlerinde dışarıda vakit geçirebilirsiniz",
    "PM2.5 seviyeleri yüksek, maske kullanmanız önerilir",
    "Polen yoğunluğu orta seviyede"
  ],
  "modelPrediction": {
    "location": {
      "latitude": 41.0082,
      "longitude": 28.9784,
      "cityName": "Istanbul",
      "countryCode": "TR"
    },
    "environmentalData": {
      "temperature": 24.5,
      "humidity": 62,
      "windSpeed": 12.5,
      "pressure": 1013,
      "pm10": 35,
      "pm2_5": 18,
      "nitrogen_dioxide": 28,
      "ozone": 45,
      "carbon_monoxide": 0.3,
      "uv_index": 6,
      "tree_pollen": 2.5,
      "grass_pollen": 3.0,
      "weed_pollen": 1.8
    },
    "timestamp": "2025-10-15T14:30:00Z"
  }
}
```

#### 2. Get Pollen Data

```bash
curl 'http://localhost:8282/api/v1/pollen/location?lat=41.0082&lon=28.9784'
```

**Response**:
```json
{
  "location": {
    "latitude": 41.0082,
    "longitude": 28.9784,
    "cityName": "Istanbul"
  },
  "pollenData": [
    {
      "plantType": "TREE",
      "species": "Oak",
      "concentration": 2.5,
      "index": "MODERATE",
      "timestamp": "2025-10-15T00:00:00Z"
    },
    {
      "plantType": "GRASS",
      "species": "Ryegrass",
      "concentration": 3.0,
      "index": "MODERATE",
      "timestamp": "2025-10-15T00:00:00Z"
    }
  ]
}
```

#### 3. Get Weather & Air Quality

```bash
curl 'http://localhost:8383/api/v1/weather/location?lat=41.0082&lon=28.9784'
```

**Response**:
```json
{
  "location": {
    "latitude": 41.0082,
    "longitude": 28.9784,
    "cityName": "Istanbul"
  },
  "weatherData": {
    "temperature": 24.5,
    "humidity": 62,
    "wind_speed": 12.5,
    "wind_direction": 180,
    "pressure": 1013,
    "cloud_cover": 45,
    "uv_index": 6,
    "precipitation": 0.0
  },
  "airQualityData": {
    "pm10": 35,
    "pm2_5": 18,
    "nitrogen_dioxide": 28,
    "ozone": 45,
    "carbon_monoxide": 0.3,
    "aqi": 52,
    "category": "MODERATE"
  },
  "timestamp": "2025-10-15T14:30:00Z"
}
```

---

## 📊 Data Pipeline

### ETL Process Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION PHASE                          │
│  (11 September 2025 - 955,801 records)                           │
└───────────────┬──────────────────────────────────────────────────┘
                │
        ┌───────┴────────┐
        │                │
┌───────▼──────┐  ┌──────▼───────┐  ┌──────────────┐
│ Pollen API   │  │ Weather API  │  │ Air Quality  │
│ (Google)     │  │ (Open-Meteo) │  │ API (Google) │
└───────┬──────┘  └──────┬───────┘  └──────┬───────┘
        │                │                  │
        └────────┬───────┴──────────────────┘
                 │
        ┌────────▼─────────┐
        │  Data Ingestion  │
        │  • City mapping  │
        │  • Timestamp     │
        │  • Validation    │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │ Data Combination │
        │ • JOIN on city   │
        │ • Time alignment │
        │ • Merge sources  │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │ Data Cleaning    │
        │ • Missing values │
        │ • Outliers       │
        │ • Duplicates     │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │ Feature          │
        │ Engineering      │
        │ • 44 features    │
        │ • Interactions   │
        │ • Temporal       │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │ Train/Test Split │
        │ • 80% train      │
        │ • 20% test       │
        │ • Stratified     │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │ Model Training   │
        │ • 5 algorithms   │
        │ • Hyperparameter │
        │   tuning         │
        │ • Cross-val      │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │ Model Evaluation │
        │ • R² > 0.98      │
        │ • MAE < 0.07     │
        │ • RMSE           │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │ Model Artifacts  │
        │ • .pkl files     │
        │ • config.json    │
        │ • scaler.pkl     │
        └──────────────────┘
```

### Data Sources

#### 1. Pollen Data (Google Pollen API)

**Collected from**: `pollen.googleapis.com/v1/forecast:lookup`

**Files**:
- `DATA/11SEP/pollen_data.csv` (40,523 records)
- `DATA/11SEP/plant_data.csv` (15,842 records)

**Fields**:
- Tree pollen concentration (grains/m³)
- Grass pollen concentration (grains/m³)
- Weed pollen concentration (grains/m³)
- Plant species identification
- Pollen index (0-5 scale)
- Forecast dates (5-day window)

#### 2. Weather Data (Open-Meteo API)

**Collected from**: `api.open-meteo.com/v1/forecast`

**Files**:
- `DATA/11SEP/weather_data.csv` (485,122 records)

**Fields**:
- Temperature (°C)
- Relative humidity (%)
- Wind speed (km/h) & direction (°)
- Surface pressure (hPa)
- Cloud cover (%)
- UV index
- Precipitation (mm)

#### 3. Air Quality Data (Google Air Quality API)

**Collected from**: `airquality.googleapis.com/v1/currentConditions:lookup`

**Files**:
- `DATA/11SEP/air_quality_data.csv` (430,154 records)

**Fields**:
- PM10 (µg/m³)
- PM2.5 (µg/m³)
- Nitrogen dioxide - NO₂ (µg/m³)
- Ozone - O₃ (µg/m³)
- Carbon monoxide - CO (mg/m³)
- Universal Air Quality Index (UAQI)

#### 4. Combined Dataset

**Final file**: `DATA/11SEP/20250911_combined_all_data.csv`

**Statistics**:
- **Total records**: 955,801
- **Features**: 44 (after engineering)
- **Date range**: 2025-08-30 to 2025-09-11 (13 days)
- **Cities covered**: 500+
- **File size**: 593.9 MB

### Data Processing Scripts

```python
# DATA/data_combine.ipynb - Main ETL notebook
# Key steps:
1. Load individual CSV files
2. Standardize timestamps
3. Join on (city_id, date) keys
4. Handle missing values:
   - Air quality: Linear interpolation
   - Pollen: Forward fill (short-term stability assumption)
   - Weather: No missing data
5. Feature engineering:
   - Temporal features (hour, day_of_week, month, season)
   - Rolling averages (3h, 6h, 12h windows)
   - Interaction terms (temp×humidity, pollen×wind)
6. Outlier detection (IQR method)
7. Export combined dataset
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/aller-mind.git
   cd aller-mind
   git remote add upstream https://github.com/eduymaz/aller-mind.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow code style guidelines
   - Write unit tests for new features
   - Update documentation

4. **Run tests**
   ```bash
   # Backend tests
   cd model-microservice && ./mvnw test
   
   # Python tests
   cd ml-model-microservice && pytest
   
   # Flutter tests
   cd FLUTTER && flutter test
   ```

5. **Commit with meaningful messages**
   ```bash
   git commit -m "feat: Add user preference caching"
   git commit -m "fix: Resolve pollen data null pointer exception"
   git commit -m "docs: Update API documentation for /predict endpoint"
   ```

6. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

---

## 👥 Team

### Project Lead & Core Development

**Elif Duymaz Yılmaz**  
[![GitHub](https://img.shields.io/badge/GitHub-eduymaz-181717?style=flat-square&logo=github)](https://github.com/eduymaz)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/elif-duymaz/)

**Roles**:
- 🔧 Backend Development (Spring Boot Microservices)
- 🧠 Machine Learning (Model Training & Deployment)
- 📱 Flutter Mobile - Front-end Development
- ☁️ Cloud Architecture & DevOps
- 📊 Data Engineering & ETL Pipelines

---

**Elif Erdal**  
[![GitHub](https://img.shields.io/badge/GitHub-eliferdals-181717?style=flat-square&logo=github)](https://github.com/eliferdals)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/eliferdal/)

**Roles**:
- 🎨 UI/UX Design
- 🖼️ Visual Design & Branding

---

### Program

This project was developed under the **Turkcell Geleceği Yazan Kadınlar - Yapay Zeka** program, a comprehensive AI education and mentorship initiative empowering women in technology.

**Program Highlights**:
- 10-month intensive AI/ML curriculum
- Industry mentorship and project guidance
- Focus on real-world AI applications
- Emphasis on healthcare and environmental tech

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Elif Duymaz Yılmaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgments

- **Turkcell Geleceği Yazan Kadınlar** - For program support and mentorship
- **Google Cloud Platform** - For generous Cloud Run free tier
- **Render.com** - For managed PostgreSQL hosting
- **Open-Meteo** - For free weather API access
- **Google APIs** - For Pollen and Air Quality data
- **scikit-learn Community** - For excellent ML library
- **Spring Boot Team** - For robust microservices framework
- **Flutter Team** - For powerful cross-platform SDK

---

### Questions or Issues?

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/eduymaz/aller-mind/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/eduymaz/aller-mind/discussions)

### Project Resources

- 📖 **Documentation**: See project documentation files
- 🎓 **Tutorials**: See `TUTORIAL.md` for step-by-step guides
- 🐳 **Docker Guide**: See `DOCKER_README.md` for containerization details

---

## 🗺️ Roadmap

### Version 2.1 (Q4 2025)
- [ ] Add historical trend analysis (7-day, 30-day)
- [ ] Implement user notifications (push notifications)
- [ ] Support for more languages (English, German, Arabic)
- [ ] iOS App Store & Google Play Store release

### Version 2.2 (Q1 2026)
- [ ] Real-time air quality sensors integration
- [ ] Community-driven allergy reporting
- [ ] Advanced data visualization dashboard
- [ ] Predictive alerts (forecast-based warnings)

### Version 3.0 (Q2 2026)
- [ ] Deep learning models (LSTM for time series)
- [ ] Wearable device integration (smartwatch, fitness trackers)
- [ ] Personalized medication reminders
- [ ] Telemedicine integration

---

## 📊 Project Statistics

```
Code Statistics (Generated 15 October 2025):
───────────────────────────────────────────────────
Language         Files    Lines    Code    Comments
───────────────────────────────────────────────────
Java               78    12,450   9,823      1,245
Python             25     3,892   3,156        425
Dart               42     8,234   6,789        678
SQL                 8     1,250   1,150         82
YAML               12       842     782         45
Dockerfile          8       285     245         30
Markdown           15     4,567   4,567          0
───────────────────────────────────────────────────
Total             188    31,520  26,512      2,505
───────────────────────────────────────────────────

Data Statistics:
• Training records: 955,801
• Features engineered: 44
• Models trained: 5
• API endpoints: 23
• Microservices: 5
• Docker containers: 6
• Cities supported: 500+
```

---

<div align="center">

### ⭐ Star this project if you find it useful!

[![GitHub stars](https://img.shields.io/github/stars/eduymaz/aller-mind?style=social)](https://github.com/eduymaz/aller-mind/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/eduymaz/aller-mind?style=social)](https://github.com/eduymaz/aller-mind/network/members)

---

**Built with ❤️ by the AllerMind Team**  
*Empowering healthier outdoor experiences through AI*

</div>
