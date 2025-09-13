# AllerMind Model Microservice

AllerMind Model Microservice, pollen ve hava durumu verilerini kullanarak alerji riskini tahmin eden makine öğrenmesi modelini yöneten servisdir.

## Özellikler

- **REST API**: Koordinat ve kullanıcı ayarları ile alerji riski tahmini
- **External Service Integration**: Pollen ve Weather Air Quality servislerini çağırır
- **Machine Learning Integration**: Python tabanlı ML modelini kullanır
- **User Grouping**: Kullanıcı ayarlarını risk gruplarına dönüştürür
- **Comprehensive Response**: Detaylı risk analizi ve öneriler sunar

## API Endpoints

### GET/POST /api/v1/model/prediction

Koordinat ve kullanıcı ayarlarına göre alerji riski tahmini yapar.

**Parameters:**
- `lat`: Enlem (latitude)
- `lon`: Boylam (longitude)

**Request Body:**
```json
{
  "userId": "user-123",
  "allergies": ["pollen", "dust"],
  "sensitivityLevel": "HIGH",
  "age": 30,
  "location": "Istanbul",
  "preferences": ["outdoor_activities"]
}
```

**Response:**
```json
{
  "predictionId": "uuid-generated",
  "userId": "user-123",
  "lat": "41.0082",
  "lon": "28.9784",
  "overallRiskScore": 0.75,
  "overallRiskLevel": "HIGH",
  "modelPrediction": {
    "predictionId": "ml-prediction-id",
    "riskScore": 0.75,
    "riskLevel": "HIGH",
    "recommendations": ["Stay indoors during peak hours", "Use air purifier"],
    "additionalMetrics": {},
    "modelVersion": "v1.0"
  },
  "userGroup": {
    "groupId": "GROUP_HIGH",
    "riskLevel": "HIGH",
    "riskScore": 0.75,
    "groupDescription": "Yüksek risk grubu - Yüksek alerji reaksiyonu beklenir"
  }
}
```

### GET /api/v1/model/health

Servis sağlık durumunu kontrol eder.

**Response:**
```
Model Service is healthy
```

## External Services

### Pollen Service (Port 8282)
- **URL**: http://localhost:8282/api/pollen
- **Purpose**: Pollen verilerini sağlar

### Weather Air Quality Service (Port 8383)
- **URL**: http://localhost:8383/api/v1/weather-air-quality
- **Purpose**: Hava durumu ve hava kalitesi verilerini sağlar

### Machine Learning Model (Port 8000)
- **URL**: http://localhost:8000/predict
- **Purpose**: Python tabanlı ML modeli (.pkl format)

## Configuration

### Application Properties

```properties
# Server Configuration
server.port=8484

# External Service URLs
pollen.service.base-url=http://localhost:8282
weather.service.base-url=http://localhost:8383
ml.model.service.base-url=http://localhost:8000

# Logging
logging.level.com.allermind.model=INFO
```

## User Grouping Algorithm

Kullanıcı ayarları aşağıdaki algoritma ile risk gruplarına dönüştürülür:

### Risk Puanı Hesaplama:
1. **Alerji Sayısı**: Her alerji için +10 puan
2. **Hassasiyet Seviyesi**:
   - HIGH: +30 puan
   - MEDIUM: +20 puan
   - LOW: +10 puan
3. **Yaş Faktörü**: 12 yaş altı veya 65 yaş üstü +15 puan

### Risk Seviyesi Belirleme:
- **CRITICAL**: ≥60 puan
- **HIGH**: 40-59 puan
- **MEDIUM**: 20-39 puan
- **LOW**: <20 puan

## Model Integration

Makine öğrenmesi modeli ile entegrasyon için aşağıdaki veriler gönderilir:

### Input Features:
- User Group bilgileri
- Pollen verileri (UPI değerleri, mevsimsellik)
- Hava durumu verileri (sıcaklık, nem, rüzgar)
- Hava kalitesi verileri (PM2.5, PM10, ozon, UV index)

### Output:
- Risk skoru (0.0-1.0)
- Risk seviyesi (LOW, MEDIUM, HIGH, CRITICAL)
- Öneriler listesi
- Model versiyonu

## Build & Run

### Prerequisites
- Java 21
- Maven 3.6+
- Pollen Service (8282)
- Weather Air Quality Service (8383)
- ML Model Service (8000)

### Build
```bash
mvn clean compile
```

### Run
```bash
mvn spring-boot:run
```

Servis http://localhost:8484 adresinde çalışacaktır.

## Testing

### Unit Tests
```bash
mvn test
```

### Integration Test
```bash
curl -X POST "http://localhost:8484/api/v1/model/prediction?lat=41.0082&lon=28.9784" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "test-user",
    "allergies": ["pollen"],
    "sensitivityLevel": "MEDIUM",
    "age": 25
  }'
```

## Architecture

```
ModelController
    ↓
AllerMindModelService
    ↓
┌─────────────────┬──────────────────┬─────────────────────┐
│ PollenClient    │ WeatherClient    │ UserGroupingService │
└─────────────────┴──────────────────┴─────────────────────┘
    ↓
MachineLearningModelClient
    ↓
AllerMindResponse
```

## Future Enhancements

1. **Advanced Grouping Algorithm**: ML tabanlı kullanıcı gruplaması
2. **Caching**: Redis ile response caching
3. **Async Processing**: Asenkron model çağrıları
4. **Monitoring**: Detailed metrics ve monitoring
5. **Rate Limiting**: API rate limiting
6. **Authentication**: JWT tabanlı authentication
