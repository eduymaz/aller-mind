# AllerMind Flutter Uygulaması

AllerMind allerji risk tahmin sisteminin mobil uygulamasıdır. Hava kalitesi, polen yoğunluğu ve meteorolojik verileri analiz ederek kişisel allerji risk tahmini yapar.

## 🚀 Özellikler

- **Kişiselleştirilmiş Risk Analizi**: 5 farklı kullanıcı grubu için özelleştirilmiş tahminler
- **Gerçek Zamanlı Veriler**: Hava durumu, hava kalitesi ve polen verilerinin canlı analizi
- **Görsel Risk Göstergesi**: Risk seviyesine göre renklendirilen ve görsel olarak desteklenen sonuçlar
- **Konum Tabanlı Tahmin**: GPS konumunuza göre otomatik veri toplama
- **Detaylı Öneriler**: Risk seviyesine göre kişiselleştirilmiş tavsiyeler

## 📱 Ekranlar

1. **Ana Sayfa (HomeScreen)**: Uygulamaya giriş ve genel bilgiler
2. **Kullanıcı Seçimi (UserSelectionScreen)**: Allerji grup seçimi ve kullanıcı bilgileri
3. **Yükleme Sayfası (LoadingScreen)**: Konum alma ve tahmin işlemi
4. **Sonuç Sayfası (ResultScreen)**: Risk analizi ve detaylı sonuçlar

## 🏗️ Proje Yapısı

```
lib/
├── main.dart                     # Uygulama giriş noktası
├── models/                       # Veri modelleri
│   ├── allermind_response.dart   # API yanıt modeli
│   └── user_settings.dart        # Kullanıcı ayarları modeli
├── providers/                    # State yönetimi
│   └── allermind_provider.dart   # Ana uygulama state'i
├── screens/                      # Ekranlar
│   ├── home_screen.dart          # Ana sayfa
│   ├── user_selection_screen.dart # Kullanıcı seçim sayfası
│   ├── loading_screen.dart       # Yükleme sayfası
│   └── result_screen.dart        # Sonuç sayfası
└── services/                     # API servisleri
    └── allermind_api_service.dart # REST API iletişimi
```

## 🔧 Kurulum

1. **Gereksinimler**:
   - Flutter SDK (3.0+)
   - Dart SDK
   - Android Studio / Xcode (mobil geliştirme için)

2. **Bağımlılıkları yükleyin**:
   ```bash
   cd FLUTTER
   flutter pub get
   ```

3. **Microservice'i başlatın**:
   - Model microservice'in 8484 portunda çalıştığından emin olun
   - `http://localhost:8484/api/v1/model/health` endpoint'inin erişilebilir olduğunu kontrol edin

4. **Uygulamayı çalıştırın**:
   ```bash
   flutter run
   ```

## 🌐 API Entegrasyonu

Uygulama `http://localhost:8484` adresinde çalışan model microservice ile iletişim kurar:

### Endpoint:
- `POST /api/v1/model/prediction?lat={lat}&lon={lon}`

### İstek Formatı:
```json
{
  "userId": "string",
  "userGroup": {
    "groupId": 1,
    "groupName": "Şiddetli Alerjik Grup",
    "description": "Ciddi alerjik reaksiyonları olan kişiler"
  }
}
```

### Yanıt Formatı:
```json
{
  "success": true,
  "overallRiskLevel": "ORTA",
  "overallRiskEmoji": "🟡",
  "overallRiskScore": 6.5,
  "modelPrediction": {
    "location": {
      "latitude": 41.0082,
      "longitude": 28.9784,
      "city_name": "İstanbul"
    },
    "predictions": [...],
    "environmental_data": {
      "temperature": 25.5,
      "humidity": 60,
      "pollen_index": 3,
      "pm10": 45,
      "pm2_5": 20,
      "wind_speed": 15,
      "precipitation": 0,
      "cloud_cover": 30
    }
  }
}
```

## 👥 Kullanıcı Grupları

1. **Şiddetli Alerjik Grup**: Ciddi alerjik reaksiyonları olan kişiler
2. **Hafif-Orta Grup**: Hafif ve orta düzeyde alerjisi olan kişiler
3. **Olası Alerjik/Genetik**: Genetik yatkınlığı olan kişiler
4. **Teşhis Almamış**: Henüz alerjik teşhis almamış kişiler
5. **Hassas Grup (Çocuk/Yaşlı/Kronik)**: Çocuk, yaşlı veya kronik hastalığı olan kişiler

## 🎨 Görsel Kaynaklar

IMAGE/ klasöründe bulunan görseller:
- `first.png`: Ana sayfa görseli
- `iyi.png`: Düşük risk seviyesi görseli
- `orta.png`: Orta risk seviyesi görseli  
- `risk.png`: Yüksek risk seviyesi görseli

## 📋 İzinler

### Android İzinleri:
- `ACCESS_FINE_LOCATION`: Hassas konum verisi
- `ACCESS_COARSE_LOCATION`: Yaklaşık konum verisi
- `INTERNET`: İnternet erişimi
- `ACCESS_NETWORK_STATE`: Ağ durumu kontrolü

### iOS İzinleri (Info.plist):
- `NSLocationWhenInUseUsageDescription`: Konum kullanım izni açıklaması

## 🔍 Hata Ayıklama

1. **Konum alınamıyor**: 
   - Cihaz ayarlarından konum servislerinin açık olduğunu kontrol edin
   - Uygulama izinlerini kontrol edin

2. **API bağlantı hatası**:
   - Model microservice'in çalıştığından emin olun
   - `baseUrl` ayarını kontrol edin (localhost yerine IP adresi gerekebilir)

3. **Görsel yükleme hatası**:
   - `pubspec.yaml`'daki asset yapılandırmasını kontrol edin
   - IMAGE/ klasöründe görsellerin bulunduğundan emin olun

## 🚀 Derleme

### Android APK:
```bash
flutter build apk --release
```

### iOS:
```bash
flutter build ios --release
```

## 📝 Notlar

- Uygulama şu anda localhost'ta çalışan microservice ile test edilmek üzere yapılandırılmıştır
- Production ortamında `AllerMindApiService.baseUrl` değiştirilmelidir
- Görsel kaynaklar uygulamayla birlikte paketlenir
- State yönetimi Provider pattern ile gerçekleştirilmiştir