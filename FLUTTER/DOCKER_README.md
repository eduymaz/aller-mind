# AllerMind Flutter Web Application

Bu, AllerMind projesi için Flutter ile geliştirilmiş web tabanlı kullanıcı arayüzüdür.

## Özellikler

- 🌐 Responsive web arayüzü
- 📍 Konum bazlı allerji risk tahmini
- 👤 Kullanıcı profili yönetimi
- 📊 Allerji sınıflandırma ve risk analizi
- 🎨 Modern ve kullanıcı dostu tasarım

## Teknolojiler

- Flutter Web
- Provider (State Management)
- HTTP (API İletişimi)
- Geolocator (Konum Servisleri)

## Docker ile Çalıştırma

### Tek Başına Çalıştırma

```bash
# Docker image oluştur
docker build -t allermind-flutter-web .

# Container'ı çalıştır
docker run -p 3000:80 allermind-flutter-web
```

Uygulama http://localhost:3000 adresinde çalışacaktır.

### Docker Compose ile Çalıştırma

Tüm mikroservislerle birlikte çalıştırmak için ana dizinden:

```bash
# Tüm servisleri başlat
docker-compose up -d

# Sadece Flutter web uygulamasını başlat
docker-compose up -d flutter-web

# Logları takip et
docker-compose logs -f flutter-web
```

## Lokal Geliştirme

### Gereksinimler

- Flutter SDK (>=3.0.0)
- Dart SDK
- Chrome veya başka bir modern tarayıcı

### Kurulum

```bash
# Bağımlılıkları yükle
flutter pub get

# Web için derle ve çalıştır
flutter run -d chrome

# Veya production build
flutter build web --release
```

### Geliştirme Modu

```bash
# Hot reload ile çalıştır
flutter run -d web-server --web-port=8080
```

## API Yapılandırması

Uygulama, Docker ortamında nginx reverse proxy üzerinden aşağıdaki servislere bağlanır:

- **Model Service**: `/api/v1/model/*` → `http://model-service:8484`
- **User Preference Service**: `/api/v1/allergy-classification/*` → `http://userpreference-service:9191`

Lokal geliştirmede, servisleri ayrı ayrı çalıştırmanız ve API URL'lerini `lib/services/` altındaki dosyalarda güncellemeniz gerekebilir.

## Proje Yapısı

```
FLUTTER/
├── lib/
│   ├── main.dart                  # Ana uygulama giriş noktası
│   ├── models/                    # Veri modelleri
│   ├── providers/                 # State management
│   ├── screens/                   # UI ekranları
│   ├── services/                  # API servisleri
│   ├── utils/                     # Yardımcı fonksiyonlar
│   └── widgets/                   # Tekrar kullanılabilir bileşenler
├── IMAGE/                         # Görsel varlıklar
├── web/                          # Web özel dosyalar
├── Dockerfile                     # Docker imaj tanımı
├── nginx.conf                     # Nginx yapılandırması
└── pubspec.yaml                  # Flutter bağımlılıkları
```

## Önemli Notlar

- Uygulama web için optimize edilmiştir
- Nginx, tüm API isteklerini ilgili mikroservislere yönlendirir
- Flutter web uygulaması, statik dosyalar olarak build edilir ve nginx tarafından servis edilir
- CORS sorunları nginx reverse proxy ile çözülmüştür

## Sorun Giderme

### Container başlamıyor

```bash
# Container loglarını kontrol et
docker logs allermind-flutter-web

# Health check durumunu kontrol et
docker inspect allermind-flutter-web
```

### API bağlantı hataları

1. Backend servislerin çalıştığından emin olun:
```bash
docker-compose ps
```

2. Network bağlantısını kontrol edin:
```bash
docker network inspect allermind-network
```

3. Nginx loglarını kontrol edin:
```bash
docker exec allermind-flutter-web cat /var/log/nginx/error.log
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
