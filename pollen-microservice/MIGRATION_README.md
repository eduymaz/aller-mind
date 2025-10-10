# Pollen Microservice - Migration Tamamlandı ✅

## 📋 Özet

Python tabanlı `pollen-service` başarıyla Java Spring Boot mikroservisine migrate edilmiştir.

## 🔄 Yapılan Değişiklikler

### 1. Yeni Entity'ler
- ✅ `ProcessingStatus` - Günlük işlem takibi için

### 2. Yeni Repository'ler
- ✅ `ProcessingStatusRepository`

### 3. Yeni DTO'lar
- ✅ `GooglePollenApiResponse` - Google Pollen API response mapping
  - DailyInfo
  - PollenTypeInfo
  - PlantInfo
  - DateInfo
  - IndexInfo
  - PlantDescription

### 4. Yeni Servisler
- ✅ `GooglePollenExternalService` - Google Pollen API'den veri çekme
- ✅ `PollenDataMapper` - API response'larını entity'lere dönüştürme
- ✅ `PollenDataProcessingService` - Ana veri işleme servisi
- ✅ `DailyPollenDataFetchJob` - Her gün 00:00'da çalışan scheduled job

### 5. Yeni Controller
- ✅ `PollenDataProcessingController` - Manuel tetikleme için admin endpoint

### 6. Konfigürasyon
- ✅ `RestTemplateConfig` - HTTP client konfigürasyonu
- ✅ `@EnableScheduling` - Scheduling aktif edildi
- ✅ Google Pollen API key application.properties'e eklendi
- ✅ Scheduling properties eklendi

## 🚀 Çalışma Mantığı

### Otomatik Çalışma
Uygulama her gün **00:00**'da otomatik olarak:
1. Tüm şehirleri veritabanından çeker
2. Her şehir için Google Pollen API'den veri çeker
3. Pollen ve Plant verilerini veritabanına kaydeder (cascade ile birlikte)
4. İşlem tamamlandığında günü "processed" olarak işaretler
5. Aynı gün tekrar çalışmayı engeller

### Manuel Tetikleme
Test veya acil durumlarda:
```bash
POST http://localhost:8282/api/v1/admin/pollen-processing/trigger
```

## 📊 Veritabanı Şeması

### Yeni Tablo: processing_status
```sql
CREATE TABLE "POLLEN"."processing_status" (
    date DATE PRIMARY KEY,
    isprocessed BOOLEAN NOT NULL
);
```

### Mevcut Tablolar
- `pollen_data` - Polen verileri (id PK)
- `plant_data` - Bitki verileri (id PK, pollen_data_id FK)
- `city` - Şehir bilgileri (plaka PK)

## 🔧 Teknik Detaylar

### API Endpoints
Mevcut endpoint'ler korundu:
- `GET /api/v1/pollen?lat={lat}&lon={lon}` - Veri sorgulama

Yeni endpoint:
- `POST /api/v1/admin/pollen-processing/trigger` - Manuel tetikleme

### Google Pollen API
- **URL**: https://pollen.googleapis.com/v1/forecast:lookup
- **API Key**: AIzaSyBBu4qaSpo8kTpJlRYZNKjZIqo-JLdMmIc
- **Parameters**: 
  - location.latitude
  - location.longitude
  - days=1
  
### Response Yapısı
```json
{
  "regionCode": "TR",
  "dailyInfo": [{
    "date": {"year": 2025, "month": 10, "day": 9},
    "pollenTypeInfo": [{
      "code": "GRASS",
      "inSeason": true,
      "indexInfo": {"value": 2.5},
      "healthRecommendations": ["Stay indoors"]
    }],
    "plantInfo": [{
      "code": "POA_PRATENSIS",
      "plantDescription": {
        "type": "GRASS",
        "picture": "url",
        "pictureCloseup": "url"
      }
    }]
  }]
}
```

### Bağımlılıklar
- Spring Boot 4.0.0-M2
- Spring Data JPA
- Spring Web
- PostgreSQL Driver
- Lombok
- Spring Task Scheduler

### Konfigürasyon
```properties
server.port=8282
spring.datasource.url=jdbc:postgresql://localhost:5432/allermind?currentSchema=POLLEN
google.pollen.api.key=AIzaSyBBu4qaSpo8kTpJlRYZNKjZIqo-JLdMmIc
spring.task.scheduling.pool.size=2
```

## 📝 Python Servisi ile Karşılaştırma

| Özellik | Python Servisi | Java Mikroservis |
|---------|----------------|------------------|
| Çalışma | Manuel run (`python main.py`) | Otomatik scheduled (00:00) |
| Framework | Raw Python + psycopg2 | Spring Boot + JPA |
| HTTP Client | requests | RestTemplate |
| Veritabanı | Direct SQL | JPA/Hibernate with Cascade |
| Logging | logging module | SLF4J + Logback |
| Deployment | Script çalıştırma | Microservice (REST API) |
| İlişkiler | Manuel FK yönetimi | JPA @OneToMany cascade |

## ✅ Test Adımları

1. **Veritabanı Hazırlığı**
```sql
-- City tablosunda veri olduğundan emin olun
SELECT COUNT(*) FROM "POLLEN"."city";
```

2. **Uygulama Başlatma**
```bash
cd pollen-microservice
./mvnw spring-boot:run
```

3. **Manuel Test**
```bash
curl -X POST http://localhost:8282/api/v1/admin/pollen-processing/trigger
```

4. **Log Kontrolü**
```
2025-10-09 00:00:00 - Starting daily pollen data fetch job
2025-10-09 00:00:01 - Fetching pollen data from: https://pollen.googleapis.com/...
2025-10-09 00:00:02 - Processed city Adana: Pollen records: 3, Plant records: 5
...
2025-10-09 00:05:00 - Daily pollen data fetch job completed successfully
```

5. **Veri Kontrolü**
```sql
-- Bugünün verileri kaydedildi mi?
SELECT COUNT(*) FROM "POLLEN"."pollen_data" 
WHERE date = CURRENT_DATE;

SELECT COUNT(*) FROM "POLLEN"."plant_data" pd
JOIN "POLLEN"."pollen_data" p ON pd.pollen_data_id = p.id
WHERE p.date = CURRENT_DATE;

-- Processing status kontrolü
SELECT * FROM "POLLEN"."processing_status" 
WHERE date = CURRENT_DATE;

-- Detaylı veri görüntüleme
SELECT p.*, 
       (SELECT COUNT(*) FROM "POLLEN"."plant_data" pd WHERE pd.pollen_data_id = p.id) as plant_count
FROM "POLLEN"."pollen_data" p
WHERE p.date = CURRENT_DATE
ORDER BY p.lat, p.lon, p.pollen_code;
```

## 🎯 Scheduled Job Detayları

### Cron Expression
```
0 0 0 * * *
│ │ │ │ │ │
│ │ │ │ │ └─ Day of week (0-7, Sunday=0 or 7)
│ │ │ │ └─── Month (1-12)
│ │ │ └───── Day of month (1-31)
│ │ └─────── Hour (0-23)
│ └───────── Minute (0-59)
└─────────── Second (0-59)
```

`0 0 0 * * *` = Her gün 00:00:00 (gece yarısı)

### Değiştirme Örnekleri
```java
@Scheduled(cron = "0 0 2 * * *")  // Her gün 02:00
@Scheduled(cron = "0 0 */12 * * *") // Her 12 saatte bir
@Scheduled(cron = "0 0 6 * * MON-FRI") // Hafta içi her gün 06:00
```

## 🔍 Önemli Notlar

### Cascade İlişkiler
PlantData, PollenData'ya `@OneToMany(cascade = CascadeType.ALL)` ile bağlı. Bu sayede:
- PollenData save edildiğinde PlantData otomatik kaydedilir
- PollenData silindiğinde PlantData otomatik silinir (orphanRemoval = true)
- Transaction içinde tüm işlemler atomic olarak yapılır

### API Rate Limiting
Google Pollen API'nin rate limit'i olabilir. Production'da:
- Exponential backoff mekanizması ekleyin
- API call'ları batch olarak yapın
- Circuit breaker pattern kullanın

### Veri Tekrarı
Processing status kontrolü ile aynı gün tekrar veri çekilmesi engellenir. Ancak:
- Manuel trigger her zaman çalışır
- Test için bu faydalıdır
- Production'da admin endpoint'i güvence altına alın

## 🐛 Sorun Giderme

### Problem: Scheduled job çalışmıyor
**Çözüm:** `@EnableScheduling` annotasyonunun `PollenServiceApplication` class'ında olduğundan emin olun.

### Problem: API key geçersiz
**Çözüm:** `application.properties`'deki API key'i kontrol edin veya environment variable kullanın.

### Problem: Duplicate key error
**Çözüm:** Processing status kontrolü çalışıyor mu? `shouldProcessToday()` metodunu kontrol edin.

### Problem: PlantData kaydedilmiyor
**Çözüm:** Cascade konfigürasyonunu kontrol edin. `@OneToMany(cascade = CascadeType.ALL)` olmalı.

### Problem: Transaction timeout
**Çözüm:** Çok fazla şehir varsa timeout süresini artırın:
```properties
spring.transaction.default-timeout=600
```

## 📦 Deployment

### Local
```bash
./mvnw clean package
java -jar target/pollen-service-0.0.1-SNAPSHOT.jar
```

### Docker
```dockerfile
FROM eclipse-temurin:21-jre
COPY target/*.jar app.jar
ENV GOOGLE_POLLEN_API_KEY=your-api-key-here
ENTRYPOINT ["java","-jar","/app.jar"]
```

### Environment Variables
```bash
export GOOGLE_POLLEN_API_KEY=AIzaSyBBu4qaSpo8kTpJlRYZNKjZIqo-JLdMmIc
export SPRING_DATASOURCE_URL=jdbc:postgresql://db-host:5432/allermind?currentSchema=POLLEN
export SPRING_DATASOURCE_USERNAME=postgres
export SPRING_DATASOURCE_PASSWORD=secure-password
```

### Production Önerileri
1. `spring.jpa.show-sql=false` yapın
2. Admin endpoint'i Spring Security ile güvence altına alın
3. API key'i environment variable'dan okuyun
4. Database connection pool ayarlarını optimize edin
5. Logging level'ı `INFO` veya `WARN` yapın
6. Health check endpoint ekleyin
7. Metrics ve monitoring ekleyin (Actuator)
8. API rate limiting ekleyin
9. Retry mechanism ekleyin
10. Circuit breaker pattern kullanın

## 🔒 Güvenlik

### API Key Yönetimi
**Mevcut:** application.properties'de hardcoded
**Önerilen:** Environment variable veya secret manager

```properties
# application.properties
google.pollen.api.key=${GOOGLE_POLLEN_API_KEY:default-key}
```

### Admin Endpoint Güvenliği
```java
@PreAuthorize("hasRole('ADMIN')")
@PostMapping("/trigger")
public ResponseEntity<...> triggerPollenDataProcessing() {
    // ...
}
```

## 🎉 Sonuç

Migration başarıyla tamamlandı! Artık Python script'i çalıştırmanıza gerek yok. Java mikroservis her gün otomatik olarak Google Pollen API'den veri çekecek ve kaydedecek.

**Eski Python Servisi:** Artık kullanıma KAPALI ✅  
**Yeni Java Mikroservis:** Aktif ve çalışıyor ✅

### Avantajlar
- ✅ Otomatik scheduled execution
- ✅ REST API ile veri sorgulama
- ✅ Transaction yönetimi
- ✅ Cascade ile ilişki yönetimi
- ✅ Better error handling
- ✅ Logging ve monitoring
- ✅ Cloud-ready deployment
