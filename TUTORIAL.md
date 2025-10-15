# 🌿 AllerMind: Comprehensive Technical Tutorial

Welcome to the AllerMind technical tutorial. This guide provides an in-depth overview of the AllerMind platform's architecture, microservices, data pipeline, machine learning models, and deployment strategies. The documentation is designed for developers, data scientists, and DevOps engineers, following enterprise-grade best practices in software engineering, machine learning, and cloud-native development.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [System Architecture](#-system-architecture)
3. [Directory Structure](#-directory-structure)
4. [Microservices Architecture](#-microservices-architecture)
5. [Machine Learning Pipeline](#-machine-learning-pipeline)
6. [Data Acquisition & Processing](#-data-acquisition--processing)
7. [Database Design](#-database-design)
8. [API Integration](#-api-integration)
9. [Mobile Application](#-mobile-application)
10. [Deployment & DevOps](#-deployment--devops)
11. [Development Workflow](#-development-workflow)
12. [Testing Strategies](#-testing-strategies)

---

## 🎯 Project Overview

**AllerMind** is an enterprise-grade, AI-powered allergy risk prediction system that combines:
- **Real-time environmental monitoring** (weather, air quality, pollen)
- **Advanced machine learning** (5 specialized ensemble models)
- **Microservices architecture** (Spring Boot + Python Flask)
- **Cross-platform mobile app** (Flutter)
- **Cloud-native deployment** (Google Cloud Run + Render.com)

### Key Metrics
- 📊 **955,801 records** processed from integrated data sources
- 🎯 **R² > 0.98** prediction accuracy across all models
- 🏗️ **5 microservices** independently deployed and scaled
- 🚀 **Sub-second** prediction response times
- 🌍 **Multi-city coverage** across Turkey

### Technology Stack
- **Backend**: Java 21, Spring Boot 3.3, Maven
- **ML Service**: Python 3.11, Flask, scikit-learn, pandas, numpy
- **Frontend**: Flutter 3.5+, Dart 3.0+
- **Database**: PostgreSQL 15 (Render.com managed)
- **Cloud**: Google Cloud Run (serverless containers)
- **DevOps**: Docker, docker-compose, Google Cloud Build

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
│                   MICROSERVICES LAYER                            │
│  ┌─────────────────────────▼────────────────────────────────┐  │
│  │  Model Orchestration Service (8484)                       │  │
│  │  Java 21 + Spring Boot 3.3 | REST API Coordination       │  │
│  └───┬───────────────┬──────────────┬───────────────┬───────┘  │
│      │               │              │               │           │
│  ┌───▼────────┐  ┌──▼───────┐  ┌──▼────────┐  ┌──▼────────┐  │
│  │ ML Model   │  │ Pollen   │  │ Weather   │  │ User Pref │  │
│  │ Service    │  │ Service  │  │ AirQ Svc  │  │ Service   │  │
│  │ (8585)     │  │ (8282)   │  │ (8383)    │  │ (9191)    │  │
│  │ Python     │  │ Java     │  │ Java      │  │ Java      │  │
│  └─────────────┘  └──────────┘  └───────────┘  └───────────┘  │
└────────────────────────────┼────────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────────┐
│                   DATA LAYER                                     │
│  ┌─────────────────────────▼────────────────────────────────┐  │
│  │  PostgreSQL 15 (Render.com)                               │  │
│  │  • User profiles & allergy preferences                    │  │
│  │  • Historical predictions                                 │  │
│  │  • Environmental data cache                               │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  External APIs                                            │  │
│  │  • Google Pollen API (pollen.googleapis.com)             │  │
│  │  • Google Air Quality API (airquality.googleapis.com)    │  │
│  │  • Open-Meteo API (api.open-meteo.com)                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
aller-mind/
│
├── model-microservice/              # Orchestration Service (Java/Spring Boot)
│   ├── src/main/java/com/allermind/model/
│   │   ├── controller/              # REST Controllers
│   │   ├── service/                 # Business Logic
│   │   ├── domain/                  # Domain Models
│   │   ├── repository/              # Data Access
│   │   └── config/                  # Configuration
│   ├── Dockerfile
│   ├── pom.xml
│   └── application.yml
│
├── ml-model-microservice/           # ML Prediction Service (Python/Flask)
│   ├── app.py                       # Flask Application
│   ├── model_loader.py              # Model Management
│   ├── models/                      # Trained ML Models (5 pkl files)
│   │   ├── group1_model.pkl         # Random Forest (Pollen)
│   │   ├── group2_model.pkl         # Gradient Boosting (Air Quality)
│   │   ├── group3_model.pkl         # SVR (UV & Sun)
│   │   ├── group4_model.pkl         # Extra Trees (Meteorological)
│   │   └── group5_model.pkl         # Neural Network (Sensitive Group)
│   ├── requirements.txt
│   └── Dockerfile
│
├── pollen-microservice/             # Pollen Data Service (Java/Spring Boot)
│   ├── src/main/java/com/allermind/pollen/
│   │   ├── controller/              # REST Controllers
│   │   ├── service/                 # Google Pollen API Integration
│   │   ├── domain/                  # Pollen Domain Models
│   │   └── config/                  # API Configuration
│   ├── Dockerfile
│   └── pom.xml
│
├── weather-airpollution-microservice/  # Weather & Air Quality Service (Java)
│   ├── src/main/java/com/allermind/weather/
│   │   ├── controller/              # REST Controllers
│   │   ├── service/                 # API Integration Logic
│   │   ├── domain/                  # Weather/AirQuality Models
│   │   └── config/                  # API Keys & Config
│   ├── Dockerfile
│   └── pom.xml
│
├── userpreference-microservice/     # User Profile Service (Java/Spring Boot)
│   ├── src/main/java/com/allermind/user/
│   │   ├── controller/              # User CRUD Operations
│   │   ├── service/                 # Business Logic
│   │   ├── domain/                  # User Entity
│   │   └── repository/              # PostgreSQL Repository
│   ├── Dockerfile
│   └── pom.xml
│
├── FLUTTER/                         # Mobile Application (Flutter/Dart)
│   ├── lib/
│   │   ├── main.dart                # App Entry Point
│   │   ├── screens/                 # UI Screens
│   │   ├── models/                  # Data Models
│   │   ├── services/                # API Services
│   │   └── widgets/                 # Reusable Components
│   ├── pubspec.yaml
│   └── android/ ios/ web/           # Platform-specific code
│
├── DATA/                            # Data Collection Scripts
│   ├── 01SEP/ 02SEP/ 07OCT/         # Daily data snapshots
│   ├── data_combine.ipynb           # Data merging notebook
│   ├── pull-data.py                 # Automated data fetcher
│   └── README.md
│
├── dataset/                         # ML Training Dataset
│   ├── processed_data.csv           # 955,801 records
│   ├── feature_engineering.ipynb    # Feature creation
│   └── model_training.ipynb         # Model training scripts
│
├── postgres/                        # Database Configuration
│   ├── init-db.sql                  # Schema initialization
│   └── Dockerfile                   # Local PostgreSQL container
│
├── docker-compose.yml               # Local development orchestration
├── render.yaml                      # Production deployment config
└── README.md                        # Project documentation
```

---

## 🔧 Microservices Architecture

### 1️⃣ Model Orchestration Service

**Technology**: Java 21, Spring Boot 3.3, Maven  
**Port**: 8484  
**Repository**: `model-microservice/`

**Purpose**:  
Central coordination layer that orchestrates all microservices, aggregates environmental data, and manages ML prediction requests.

**Key Responsibilities**:
- Aggregate data from Pollen, Weather, and User Preference services
- Coordinate ML model predictions via ML Model Service
- Apply personal weight adjustments based on user profile
- Implement ensemble prediction strategy
- Cache responses for performance optimization
- Expose unified REST API for Flutter app

**API Endpoints**:
```
POST /api/predict
GET  /api/health
GET  /api/models/status
```

**Configuration** (`application.yml`):
```yaml
server:
  port: 8484

spring:
  application:
    name: model-orchestration-service
    
services:
  ml-model: ${ML_MODEL_URL:http://localhost:8585}
  pollen: ${POLLEN_URL:http://localhost:8282}
  weather: ${WEATHER_URL:http://localhost:8383}
  user-preference: ${USER_PREF_URL:http://localhost:9191}
```

---

### 2️⃣ ML Model Service

**Technology**: Python 3.11, Flask, scikit-learn  
**Port**: 8585  
**Repository**: `ml-model-microservice/`

**Purpose**:  
Hosts 5 trained machine learning models and provides prediction endpoints for different allergy sensitivity groups.

**Key Responsibilities**:
- Load and cache trained models (Random Forest, Gradient Boosting, SVR, Extra Trees, Neural Network)
- Process feature vectors (44 engineered features)
- Return predictions with confidence scores
- Monitor model performance metrics
- Support model versioning and A/B testing

**Models Overview**:

| Group | Model Type | Algorithm | Accuracy (R²) | Use Case |
|-------|-----------|-----------|---------------|----------|
| Group 1 | Random Forest | 100 estimators | 0.9996 | Pollen allergies |
| Group 2 | Gradient Boosting | 100 estimators | 0.9902 | Air quality sensitivity |
| Group 3 | SVR | RBF kernel | 0.9993 | UV & sun sensitivity |
| Group 4 | Extra Trees | 100 estimators | 0.9892 | Meteorological factors |
| Group 5 | Neural Network | MLP | 1.0000 | Sensitive/high-risk groups |

**API Endpoints**:
```
POST /predict
POST /predict/group/{groupId}
GET  /models/info
GET  /health
```

**Example Request**:
```bash
curl -X POST http://localhost:8585/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [25.5, 60.2, 1013.2, 45.3, ...],
    "group_id": 1
  }'
```

---

### 3️⃣ Pollen Microservice

**Technology**: Java 21, Spring Boot 3.3  
**Port**: 8282  
**Repository**: `pollen-microservice/`

**Purpose**:  
Fetches real-time pollen concentration data from Google Pollen API for specified locations.

**Key Responsibilities**:
- Integrate with Google Pollen API (`pollen.googleapis.com`)
- Parse and transform pollen type information
- Cache pollen data (24-hour TTL)
- Support multiple pollen types (tree, grass, weed)
- Provide historical pollen data lookup

**Pollen Types Monitored**:
- 🌳 **Tree Pollen**: Oak, pine, birch, etc.
- 🌾 **Grass Pollen**: Timothy, ryegrass, etc.
- 🌿 **Weed Pollen**: Ragweed, mugwort, etc.

**API Endpoints**:
```
GET /api/pollen/location?lat={lat}&lng={lng}
GET /api/pollen/city/{cityName}
GET /api/pollen/forecast?lat={lat}&lng={lng}&days={days}
```

**Example Response**:
```json
{
  "location": {
    "latitude": 41.0082,
    "longitude": 28.9784
  },
  "pollenTypes": [
    {
      "type": "TREE",
      "level": "HIGH",
      "index": 4.5,
      "displayName": "Tree Pollen"
    },
    {
      "type": "GRASS",
      "level": "MODERATE",
      "index": 2.3,
      "displayName": "Grass Pollen"
    }
  ],
  "timestamp": "2025-10-16T10:00:00Z"
}
```

---

### 4️⃣ Weather & Air Pollution Microservice

**Technology**: Java 21, Spring Boot 3.3  
**Port**: 8383  
**Repository**: `weather-airpollution-microservice/`

**Purpose**:  
Aggregates weather and air quality data from multiple external APIs.

**Key Responsibilities**:
- Fetch weather data from Open-Meteo API
- Retrieve air quality indices from Google Air Quality API
- Calculate derived meteorological features
- Monitor PM2.5, PM10, NO₂, O₃, CO levels
- Provide hourly and daily forecasts

**Data Sources**:
- **Open-Meteo API**: Temperature, humidity, wind speed, precipitation, UV index
- **Google Air Quality API**: PM2.5, PM10, NO₂, O₃, CO, AQI

**API Endpoints**:
```
GET /api/weather/current?lat={lat}&lng={lng}
GET /api/airquality/current?lat={lat}&lng={lng}
GET /api/combined?lat={lat}&lng={lng}
GET /api/forecast?lat={lat}&lng={lng}&days={days}
```

**Example Response**:
```json
{
  "weather": {
    "temperature": 22.5,
    "humidity": 65,
    "windSpeed": 12.3,
    "uvIndex": 6.2,
    "precipitation": 0.0
  },
  "airQuality": {
    "aqi": 78,
    "pm25": 45.3,
    "pm10": 67.8,
    "no2": 23.4,
    "o3": 56.7,
    "co": 0.4
  },
  "timestamp": "2025-10-16T10:00:00Z"
}
```

---

### 5️⃣ User Preference Microservice

**Technology**: Java 21, Spring Boot 3.3, Spring Data JPA  
**Port**: 9191  
**Repository**: `userpreference-microservice/`

**Purpose**:  
Manages user profiles, allergy preferences, and personalization data.

**Key Responsibilities**:
- CRUD operations for user profiles
- Store allergy types and sensitivity levels
- Manage personal weighting factors
- Track user activity history
- Handle authentication and authorization

**Database Schema**:
```sql
CREATE TABLE user_preferences (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER,
    allergy_types TEXT[],
    sensitivity_level INTEGER,
    medical_conditions TEXT[],
    activity_level VARCHAR(50),
    personal_weights JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**API Endpoints**:
```
POST   /api/users
GET    /api/users/{userId}
PUT    /api/users/{userId}
DELETE /api/users/{userId}
GET    /api/users/{userId}/preferences
PUT    /api/users/{userId}/preferences
```

**Example User Profile**:
```json
{
  "userId": "user123",
  "age": 28,
  "allergyTypes": ["pollen", "dust", "pollution"],
  "sensitivityLevel": 3,
  "medicalConditions": ["asthma"],
  "activityLevel": "MODERATE",
  "personalWeights": {
    "pollen_weight": 1.5,
    "airquality_weight": 1.8,
    "weather_weight": 1.0
  }
}
```

---

## 🤖 Machine Learning Pipeline

### Dataset Overview

**Records**: 955,801  
**Features**: 44 (engineered)  
**Target Variable**: Safe outdoor time (minutes)  
**Data Period**: March 2024 - October 2024

### Feature Engineering

**Original Features (19)**:
- Temperature (°C), Apparent Temperature (°C)
- Humidity (%), Precipitation (mm)
- Wind Speed (km/h), Wind Direction (°)
- UV Index, Cloud Cover (%)
- PM2.5, PM10, NO₂, O₃, CO
- Tree/Grass/Weed Pollen Indices

**Engineered Features (25)**:
- Temperature ranges (morning, noon, evening)
- Humidity comfort index
- Wind chill factor
- Air quality composite score
- Pollen severity index
- Temporal features (hour, day, month, season)
- Interaction terms (temp × humidity, wind × pollution)

### Model Training Process

```python
# Example: Random Forest for Group 1
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv('dataset/processed_data.csv')

# Split by group
group1_data = df[df['allergy_group'] == 1]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    group1_data[features], 
    group1_data['safe_time_minutes'],
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=10,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
r2_score = model.score(X_test, y_test)
print(f"R² Score: {r2_score:.4f}")  # Output: 0.9996

# Save model
import pickle
with open('models/group1_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

### Ensemble Strategy

**Performance-Weighted Ensemble**:
```python
def ensemble_prediction(features, group_id, user_weights):
    # Get base prediction from primary model
    base_prediction = models[group_id].predict(features)
    
    # Get predictions from all models
    all_predictions = [model.predict(features) for model in models.values()]
    
    # Calculate weighted average
    model_weights = [0.9996, 0.9902, 0.9993, 0.9892, 1.0000]  # R² scores
    ensemble_pred = np.average(all_predictions, weights=model_weights)
    
    # Apply personal weights
    final_prediction = base_prediction * 0.7 + ensemble_pred * 0.3
    final_prediction *= user_weights.get(f'group{group_id}_weight', 1.0)
    
    return max(0, min(480, final_prediction))  # Clamp to 0-480 minutes
```

### Model Evaluation Metrics

| Metric | Group 1 | Group 2 | Group 3 | Group 4 | Group 5 |
|--------|---------|---------|---------|---------|---------|
| R² Score | 0.9996 | 0.9902 | 0.9993 | 0.9892 | 1.0000 |
| MAE (min) | 2.3 | 5.7 | 3.1 | 6.2 | 0.8 |
| RMSE (min) | 3.5 | 8.4 | 4.2 | 9.1 | 1.2 |

---

## 📊 Data Acquisition & Processing

### Legacy Data Collection (Historical Reference)

The project initially used dedicated Python scripts for data collection:

**allermind-weather/**:
- `main.py`: Orchestrated weather/air quality data collection
- `service.py`: API communication with Open-Meteo
- `domain.py`: Data models for weather/air quality
- `repository.py`: CSV data access layer
- `merge.py`: Hourly data merging logic
- `exporter.py`: CSV export utilities

**allermind-pollen/**:
- `pollen_main.py`: Pollen data collection workflow
- `pollen_service.py`: Google Pollen API integration
- `pollen_exporter.py`: Pollen data serialization

### Current Data Flow (Microservices Architecture)

```
External APIs → Microservices → Cache → Model Service → Client
     ↓              ↓              ↓          ↓            ↓
Open-Meteo    Weather Service  Redis    ML Models   Flutter App
Google APIs   Pollen Service   (future) Predictions  iOS/Android
```

**Data Collection Workflow**:

1. **Real-time Requests**:
   - Flutter app sends location coordinates
   - Orchestration service fans out to data services
   - Services call external APIs concurrently
   - Results are aggregated and cached

2. **Historical Data** (Training):
   - Daily batch jobs collect city-level data
   - Stored in `DATA/` directory by date
   - Jupyter notebooks merge and preprocess
   - Final dataset used for model training

3. **Feature Transformation**:
   - Raw API responses → Normalized features
   - Missing value imputation
   - Outlier detection and handling
   - Feature scaling (StandardScaler)

**Example: Data Combination**:
```python
# DATA/data_combine.ipynb
import pandas as pd

# Load daily snapshots
weather_df = pd.read_csv('01SEP/weather_data.csv')
pollen_df = pd.read_csv('01SEP/pollen_data.csv')
airquality_df = pd.read_csv('01SEP/airquality_data.csv')

# Merge on city and timestamp
merged_df = weather_df.merge(pollen_df, on=['city', 'timestamp'])
merged_df = merged_df.merge(airquality_df, on=['city', 'timestamp'])

# Feature engineering
merged_df['temp_humidity_index'] = merged_df['temperature'] * merged_df['humidity'] / 100
merged_df['pollen_severity'] = (
    merged_df['tree_pollen'] + 
    merged_df['grass_pollen'] + 
    merged_df['weed_pollen']
) / 3

# Export
merged_df.to_csv('dataset/processed_data.csv', index=False)
```

---

## 🗄️ Database Design


**PostgreSQL Schema** (Render.com):

```sql
-- User Preferences Table
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

-- Prediction History Table
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

-- City Cache Table (for performance)
CREATE TABLE city_cache (
    id BIGSERIAL PRIMARY KEY,
    city_name VARCHAR(255) UNIQUE,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    country_code VARCHAR(10),
    timezone VARCHAR(100),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);
CREATE INDEX idx_prediction_history_user_id ON prediction_history(user_id);
CREATE INDEX idx_prediction_history_created_at ON prediction_history(created_at);
CREATE INDEX idx_city_cache_name ON city_cache(city_name);
```

**Connection Configuration**:
```yaml
# application.yml (User Preference Service)
spring:
  datasource:
    url: ${DATABASE_URL:jdbc:postgresql://localhost:5432/allermind}
    username: ${DATABASE_USER:postgres}
    password: ${DATABASE_PASSWORD:password}
    driver-class-name: org.postgresql.Driver
  
  jpa:
    hibernate:
      ddl-auto: validate  # Use Flyway for migrations in production
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
        format_sql: true
```

---

## 🔌 API Integration

### External APIs Configuration

**1. Google Pollen API**

```java
// PollenService.java
@Service
public class PollenService {
    @Value("${google.pollen.api.key}")
    private String apiKey;
    
    private static final String BASE_URL = "https://pollen.googleapis.com/v1";
    
    public PollenResponse fetchPollenData(double lat, double lng) {
        String url = String.format("%s/forecast:lookup?key=%s&location.latitude=%f&location.longitude=%f&days=5",
            BASE_URL, apiKey, lat, lng);
        
        RestTemplate restTemplate = new RestTemplate();
        return restTemplate.getForObject(url, PollenResponse.class);
    }
}
```

**2. Google Air Quality API**

```java
// AirQualityService.java
@Service
public class AirQualityService {
    @Value("${google.airquality.api.key}")
    private String apiKey;
    
    private static final String BASE_URL = "https://airquality.googleapis.com/v1";
    
    public AirQualityResponse fetchAirQuality(double lat, double lng) {
        String url = String.format("%s/currentConditions:lookup?key=%s", BASE_URL, apiKey);
        
        Map<String, Object> requestBody = Map.of(
            "location", Map.of("latitude", lat, "longitude", lng)
        );
        
        RestTemplate restTemplate = new RestTemplate();
        return restTemplate.postForObject(url, requestBody, AirQualityResponse.class);
    }
}
```

**3. Open-Meteo API**

```java
// WeatherService.java
@Service
public class WeatherService {
    private static final String BASE_URL = "https://api.open-meteo.com/v1/forecast";
    
    public WeatherResponse fetchWeather(double lat, double lng) {
        String url = String.format(
            "%s?latitude=%f&longitude=%f&current_weather=true&hourly=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,uv_index",
            BASE_URL, lat, lng
        );
        
        RestTemplate restTemplate = new RestTemplate();
        return restTemplate.getForObject(url, WeatherResponse.class);
    }
}
```

---

## 📱 Mobile Application

**Technology**: Flutter 3.5+, Dart 3.0+  
**Repository**: `FLUTTER/`

### Architecture

```
lib/
├── main.dart                        # App entry point
├── screens/
│   ├── home_screen.dart            # Main dashboard
│   ├── profile_screen.dart         # User profile management
│   ├── prediction_screen.dart      # Risk prediction display
│   └── history_screen.dart         # Prediction history
├── models/
│   ├── user_model.dart             # User data model
│   ├── prediction_model.dart       # Prediction response model
│   └── environmental_data_model.dart
├── services/
│   ├── api_service.dart            # HTTP client wrapper
│   ├── location_service.dart       # GPS integration
│   └── storage_service.dart        # Local storage (SharedPreferences)
├── widgets/
│   ├── risk_indicator.dart         # Visual risk display
│   ├── weather_card.dart           # Weather information widget
│   └── pollen_chart.dart           # Pollen level visualization
└── utils/
    ├── constants.dart              # App-wide constants
    └── helpers.dart                # Utility functions
```

### Key Features Implementation

**1. Location Services**:
```dart
// location_service.dart
import 'package:geolocator/geolocator.dart';

class LocationService {
  Future<Position> getCurrentLocation() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      throw Exception('Location services are disabled.');
    }
    
    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        throw Exception('Location permissions are denied');
      }
    }
    
    return await Geolocator.getCurrentPosition();
  }
}
```

**2. API Integration**:
```dart
// api_service.dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'https://model-service-YOUR-PROJECT.run.app';
  
  Future<PredictionModel> getPrediction(double lat, double lng, String userId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/predict'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'latitude': lat,
        'longitude': lng,
        'userId': userId,
      }),
    );
    
    if (response.statusCode == 200) {
      return PredictionModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load prediction');
    }
  }
}
```

**3. Risk Visualization**:
```dart
// risk_indicator.dart
import 'package:flutter/material.dart';

class RiskIndicator extends StatelessWidget {
  final int safeMinutes;
  final String riskLevel;
  
  const RiskIndicator({
    required this.safeMinutes,
    required this.riskLevel,
  });
  
  Color getRiskColor() {
    switch (riskLevel.toUpperCase()) {
      case 'LOW': return Colors.green;
      case 'MODERATE': return Colors.yellow;
      case 'HIGH': return Colors.orange;
      case 'VERY_HIGH': return Colors.red;
      default: return Colors.grey;
    }
  }
  
  String getRiskEmoji() {
    switch (riskLevel.toUpperCase()) {
      case 'LOW': return '😊';
      case 'MODERATE': return '😐';
      case 'HIGH': return '😟';
      case 'VERY_HIGH': return '😨';
      default: return '❓';
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Card(
      color: getRiskColor().withOpacity(0.2),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            Text(getRiskEmoji(), style: TextStyle(fontSize: 48)),
            SizedBox(height: 8),
            Text('Safe Outdoor Time', style: TextStyle(fontSize: 16)),
            Text('$safeMinutes minutes', 
                style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
            Text('Risk Level: $riskLevel', style: TextStyle(fontSize: 14)),
          ],
        ),
      ),
    );
  }
}
```

### Dependencies (`pubspec.yaml`):
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  geolocator: ^10.1.0
  provider: ^6.1.1
  shared_preferences: ^2.2.2
  fl_chart: ^0.65.0
  intl: ^0.18.1
```

---

## 🚀 Deployment & DevOps

### Local Development

**Docker Compose** (`docker-compose.yml`):
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: allermind
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
      - postgres_data:/var/lib/postgresql/data

  model-service:
    build: ./model-microservice
    ports:
      - "8484:8484"
    environment:
      ML_MODEL_URL: http://ml-model-service:8585
      POLLEN_URL: http://pollen-service:8282
      WEATHER_URL: http://weather-service:8383
      USER_PREF_URL: http://userpreference-service:9191
    depends_on:
      - postgres

  ml-model-service:
    build: ./ml-model-microservice
    ports:
      - "8585:8585"
    volumes:
      - ./ml-model-microservice/models:/app/models

  pollen-service:
    build: ./pollen-microservice
    ports:
      - "8282:8282"
    environment:
      GOOGLE_API_KEY: ${GOOGLE_API_KEY}

  weather-service:
    build: ./weather-airpollution-microservice
    ports:
      - "8383:8383"
    environment:
      GOOGLE_API_KEY: ${GOOGLE_API_KEY}

  userpreference-service:
    build: ./userpreference-microservice
    ports:
      - "9191:9191"
    environment:
      DATABASE_URL: jdbc:postgresql://postgres:5432/allermind
      DATABASE_USER: postgres
      DATABASE_PASSWORD: password
    depends_on:
      - postgres

volumes:
  postgres_data:
```

**Start all services**:
```bash
docker-compose up --build
```

---

### Production Deployment (Google Cloud Run + Render.com)

**Render.com Configuration** (`render.yaml`):
```yaml
services:
  - type: web
    name: model-orchestration-service
    runtime: docker
    dockerfilePath: ./model-microservice/Dockerfile
    env:
      - key: ML_MODEL_URL
        value: https://ml-model-service-YOUR-ID.onrender.com
      - key: POLLEN_URL
        value: https://pollen-service-YOUR-ID.onrender.com
      - key: WEATHER_URL
        value: https://weather-service-YOUR-ID.onrender.com
      - key: USER_PREF_URL
        value: https://userpreference-service-YOUR-ID.onrender.com
    
  - type: web
    name: ml-model-service
    runtime: docker
    dockerfilePath: ./ml-model-microservice/Dockerfile
    
  - type: web
    name: pollen-service
    runtime: docker
    dockerfilePath: ./pollen-microservice/Dockerfile
    envVars:
      - key: GOOGLE_API_KEY
        sync: false  # Use Render dashboard for secrets
    
  - type: web
    name: weather-service
    runtime: docker
    dockerfilePath: ./weather-airpollution-microservice/Dockerfile
    envVars:
      - key: GOOGLE_API_KEY
        sync: false
    
  - type: web
    name: userpreference-service
    runtime: docker
    dockerfilePath: ./userpreference-microservice/Dockerfile
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: allermind-db
          property: connectionString

databases:
  - name: allermind-db
    databaseName: allermind
    user: allermind_user
    plan: starter  # Free tier
```

**Google Cloud Run Deployment**:
```bash
# Build and push Docker image
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/model-service ./model-microservice

# Deploy to Cloud Run
gcloud run deploy model-service \
  --image gcr.io/YOUR-PROJECT-ID/model-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ML_MODEL_URL=https://ml-model-service.run.app
```

---

## 💻 Development Workflow

### 1. Clone Repository
```bash
git clone https://github.com/eduymaz/allermind.git
cd aller-mind
```

### 2. Setup Environment Variables
```bash
# Create .env file
cat > .env << EOF
GOOGLE_API_KEY=your_google_api_key
DATABASE_URL=jdbc:postgresql://localhost:5432/allermind
DATABASE_USER=postgres
DATABASE_PASSWORD=password
EOF
```

### 3. Build Java Services
```bash
cd model-microservice
mvn clean package -DskipTests
cd ../pollen-microservice
mvn clean package -DskipTests
# Repeat for other Java services
```

### 4. Setup Python ML Service
```bash
cd ml-model-microservice
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Run with Docker Compose
```bash
docker-compose up --build
```

### 6. Access Services
- Model Orchestration: http://localhost:8484
- ML Model Service: http://localhost:8585
- Pollen Service: http://localhost:8282
- Weather Service: http://localhost:8383
- User Preference Service: http://localhost:9191
- Swagger UI: http://localhost:8484/swagger-ui/index.html

---

## 🧪 Testing Strategies

### Unit Tests (Java)
```java
// ModelServiceTest.java
@SpringBootTest
class ModelServiceTest {
    @Autowired
    private ModelService modelService;
    
    @Test
    void testPredictionAggregation() {
        PredictionRequest request = new PredictionRequest();
        request.setLatitude(41.0082);
        request.setLongitude(28.9784);
        request.setUserId("test_user");
        
        PredictionResponse response = modelService.predict(request);
        
        assertNotNull(response);
        assertTrue(response.getSafeMinutes() >= 0);
        assertTrue(response.getSafeMinutes() <= 480);
        assertNotNull(response.getRiskLevel());
    }
}
```

### Integration Tests (Python)
```python
# test_ml_service.py
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_prediction_endpoint(client):
    response = client.post('/predict', json={
        'features': [25.5, 60.2, 1013.2, ...],  # 44 features
        'group_id': 1
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'prediction' in data
    assert 0 <= data['prediction'] <= 480
```

### End-to-End Tests (Flutter)
```dart
// widget_test.dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Risk indicator displays correctly', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(
      home: RiskIndicator(safeMinutes: 120, riskLevel: 'MODERATE'),
    ));
    
    expect(find.text('120 minutes'), findsOneWidget);
    expect(find.text('Risk Level: MODERATE'), findsOneWidget);
    expect(find.text('😐'), findsOneWidget);
  });
}
```

---

## 📚 Additional Resources

### API Documentation
- **Swagger UI**: http://localhost:8484/swagger-ui/index.html
- **OpenAPI Spec**: http://localhost:8484/v3/api-docs

### Project Documentation
- `README.md`: Project overview and quick start
- `QUICK_START.md`: 5-minute setup guide
- `RENDER_DEPLOYMENT.md`: Production deployment guide
- `DOCKER_README.md`: Docker configuration details
- `POSTGRES_TROUBLESHOOTING.md`: Database troubleshooting

### External API Documentation
- [Google Pollen API](https://developers.google.com/maps/documentation/pollen)
- [Google Air Quality API](https://developers.google.com/maps/documentation/air-quality)
- [Open-Meteo API](https://open-meteo.com/en/docs)

---

## 🤝 Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for guidelines.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Standards
- **Java**: Google Java Style Guide, Checkstyle validation
- **Python**: PEP 8, Black formatter, pylint
- **Flutter**: Effective Dart guidelines

---

## 👥 Team

**Turkcell Geleceği Yazan Kadınlar - Yapay Zeka Program**

- **Elif Duymaz** - Project Lead & Backend and Artificial Intelligence Developer
- **Elif Erdal** - UI/UX Designer


---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Turkcell** for supporting the "Geleceği Yazan Kadınlar" program
- **Google** for providing Pollen and Air Quality APIs
- **Open-Meteo** for free weather data access
- Open-source community for amazing tools and libraries


