# AllerMind PostgreSQL Database

Custom PostgreSQL image with pre-configured schemas for AllerMind microservices.

## Özellikler

- **PostgreSQL 15 Alpine**: Hafif ve güvenli base image
- **Otomatik Şema Oluşturma**: Container ilk başlatıldığında şemalar otomatik oluşturulur
- **Kalıcı Veri**: Named volume ile veriler container yeniden başlatıldığında korunur
- **Health Check**: Container sağlık durumu sürekli kontrol edilir

## Şemalar

AllerMind uygulaması iki ayrı şema kullanır:

- **WEATHER**: Hava durumu ve hava kalitesi verileri
- **POLLEN**: Polen verileri

## Veritabanı Bilgileri

```
Database: allermind
User: postgres
Password: 123456
Port: 5433 (Host) -> 5432 (Container)
```

## Kullanım

### Docker Compose ile Başlatma

```bash
# Ana dizinden
docker-compose up -d postgres

# Logları kontrol et
docker-compose logs -f postgres
```

### Manuel Build ve Run

```bash
# Image build
cd postgres
docker build -t allermind-postgres .

# Container çalıştır
docker run -d \
  --name allermind-postgres \
  -e POSTGRES_PASSWORD=123456 \
  -p 5433:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  allermind-postgres
```

## Veritabanına Bağlanma

### psql ile

```bash
# Container içinden
docker exec -it allermind-postgres psql -U postgres -d allermind

# Host'tan (psql kurulu ise)
psql -h localhost -p 5433 -U postgres -d allermind
```

### Şemaları Kontrol Etme

```sql
-- Mevcut şemaları listele
\dn+

-- WEATHER şemasındaki tabloları listele
\dt WEATHER.*

-- POLLEN şemasındaki tabloları listele
\dt POLLEN.*
```

## Veri Kalıcılığı

### Named Volume Kullanımı

Docker Compose `postgres_data` named volume kullanır. Bu volume:

- Container yeniden başlatıldığında veriler korunur
- Container silinse bile veriler kalır
- Yeni container aynı volume'u kullanırsa verilere erişebilir

### Volume İşlemleri

```bash
# Volume'ları listele
docker volume ls

# postgres_data volume'unu incele
docker volume inspect aller-mind_postgres_data

# Volume'u tamamen silme (DİKKAT: Tüm veriler silinir!)
docker volume rm aller-mind_postgres_data
```

### Veritabanını Sıfırlama

Eğer veritabanını baştan oluşturmak isterseniz:

```bash
# Container'ı durdur ve sil
docker-compose down postgres

# Volume'u sil (veriler kaybolur!)
docker volume rm aller-mind_postgres_data

# Yeniden başlat (init-db.sql otomatik çalışır)
docker-compose up -d postgres
```

## Init Script (init-db.sql)

`init-db.sql` dosyası sadece container **ilk kez** oluşturulduğunda çalışır. 

⚠️ **Önemli**: Volume mevcut olduğu sürece init script bir daha çalışmaz!

### Init Script Çalışma Koşulları

Init script çalışması için:
1. Volume tamamen boş olmalı (ilk kez oluşturulmuş)
2. `/var/lib/postgresql/data` dizini boş olmalı

### Script İçeriği

- `WEATHER` şeması oluşturur
- `POLLEN` şeması oluşturur  
- Gerekli izinleri verir
- Gelecekte oluşturulacak tablolar için default izinler ayarlar

## Mikroservislere Bağlantı

### Spring Boot Configuration

**Weather Service:**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://postgres:5432/allermind?currentSchema=WEATHER
    username: postgres
    password: 123456
```

**Pollen Service:**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://postgres:5432/allermind?currentSchema=POLLEN
    username: postgres
    password: 123456
```

## Troubleshooting

### Container Başlamıyor

```bash
# Logları kontrol et
docker logs allermind-postgres

# Init script hatalarını gör
docker logs allermind-postgres 2>&1 | grep -i error
```

### Şemalar Oluşmamış

Init script sadece ilk başlatmada çalışır. Eğer şemalar eksikse:

```bash
# Manuel olarak şemaları oluştur
docker exec -it allermind-postgres psql -U postgres -d allermind -f /docker-entrypoint-initdb.d/init-db.sql
```

### Bağlantı Sorunları

```bash
# PostgreSQL hazır mı kontrol et
docker exec allermind-postgres pg_isready -U postgres -d allermind

# Port dinlemesi kontrol et
docker exec allermind-postgres netstat -tuln | grep 5432
```

### Permission Denied Hataları

```bash
# Volume sahiplik bilgilerini kontrol et
docker exec allermind-postgres ls -la /var/lib/postgresql/data

# PostgreSQL kullanıcısını kontrol et
docker exec allermind-postgres whoami
```

## Backup ve Restore

### Manuel Backup

```bash
# Tüm veritabanını yedekle
docker exec allermind-postgres pg_dump -U postgres allermind > backup.sql

# Sadece WEATHER şemasını yedekle
docker exec allermind-postgres pg_dump -U postgres -n WEATHER allermind > weather_backup.sql

# Sadece POLLEN şemasını yedekle
docker exec allermind-postgres pg_dump -U postgres -n POLLEN allermind > pollen_backup.sql
```

### Restore

```bash
# Backup'tan geri yükle
docker exec -i allermind-postgres psql -U postgres allermind < backup.sql
```

## Performance

- **Startup Time**: ~5-10 saniye
- **Init Script Time**: ~1-2 saniye (sadece ilk başlatma)
- **Memory Usage**: ~50-100MB (Alpine base image sayesinde)
- **Disk Usage**: Verilere bağlı olarak değişir

## Security

⚠️ **Production Notları:**

1. Varsayılan şifre (`123456`) **sadece development** içindir
2. Production'da güçlü şifreler kullanın
3. PostgreSQL şifresini environment variable veya secrets ile yönetin
4. Network güvenliği için firewall kuralları ekleyin

```yaml
# Production için örnek
environment:
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}  # .env dosyasından al
```
