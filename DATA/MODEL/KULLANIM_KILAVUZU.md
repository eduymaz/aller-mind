# AllerMind Makine Öğrenmesi Modeli Kullanım Kılavuzu

## 📖 Genel Bakış

AllerMind, çevresel faktörler ve polen verilerini kullanarak alerji hastalığı olan kişilerin güvenli dış mekan sürelerini tahmin eden gelişmiş bir makine öğrenmesi sistemidir. Sistem, beş farklı hasta grubu için optimize edilmiş algoritmalar kullanır.

### 🎯 Sistem Performansı

| Grup | Algoritma | Doğruluk (R²) | Ortalama Hata (MSE) | Mutlak Hata (MAE) |
|------|-----------|---------------|---------------------|-------------------|
| Grup 1 | Random Forest | %99.56 | 0.0052 | 0.0096 |
| Grup 2 | RBF SVM | %99.62 | 0.0021 | 0.0385 |
| Grup 3 | RBF SVM | %99.75 | 0.0016 | 0.0343 |
| Grup 4 | RBF SVM | %99.80 | 0.0009 | 0.0245 |
| Grup 5 | RBF SVM | %99.55 | 0.0022 | 0.0401 |

## 🏥 Hasta Grupları

### Grup 1: Şiddetli Alerjik Hastalar
- **Özellikler**: Yoğun alerji belirtileri, çoklu alerjen hassasiyeti
- **Algoritma**: Random Forest Regressor
- **Güvenlik Faktörü**: En yüksek (konservatif tahminler)

### Grup 2: Hafif-Orta Düzey Alerjik Hastalar  
- **Özellikler**: Mevsimsel alerjiler, kontrol edilebilir belirtiler
- **Algoritma**: RBF SVM
- **Güvenlik Faktörü**: Dengeli yaklaşım

### Grup 3: Genetik Yatkınlık Olan Hastalar
- **Özellikler**: Aile öyküsü mevcut, potansiyel risk altında
- **Algoritma**: RBF SVM  
- **Güvenlik Faktörü**: Proaktif koruma

### Grup 4: Kaliteli Yaşam Arayan Hastalar
- **Özellikler**: Yaşam kalitesi odaklı, aktif yaşam tarzı
- **Algoritma**: RBF SVM
- **Güvenlik Faktörü**: Optimum süre tahmini

### Grup 5: Hassas Çocuk ve Yaşlı Hastalar
- **Özellikler**: İmmün sistem zayıflığı, ek sağlık riskleri
- **Algoritma**: RBF SVM
- **Güvenlik Faktörü**: Maksimum koruma

## 💻 Teknik Kullanım

### Hızlı Başlangıç

```python
import pickle
import numpy as np
from datetime import datetime

class AllerMindPredictor:
    def __init__(self):
        self.models = {}
        self.load_all_models()
    
    def load_all_models(self):

        grup_isimleri = [
            'Grup1_Siddetli_Alerjik',
            'Grup2_Hafif_Orta', 
            'Grup3_Genetik_Yatkinlik',
            'Grup4_Kaliteli_Yasam',
            'Grup5_Hassas_Cocuk_Yasli'
        ]
        
        for grup_ismi in grup_isimleri:
            try:
                with open(f'pkl_models/{grup_ismi}_model.pkl', 'rb') as f:
                    self.models[grup_ismi] = pickle.load(f)
                print(f"✅ {grup_ismi} modeli yüklendi")
            except Exception as e:
                print(f"❌ {grup_ismi} modeli yüklenemedi: {e}")
    
    def predict_safe_hours(self, grup_ismi, cevre_verileri):

        if grup_ismi not in self.models:
            raise ValueError(f"Geçersiz grup ismi: {grup_ismi}")
        
        model_paketi = self.models[grup_ismi]
        model = model_paketi['model']
        scaler = model_paketi['scaler'] 
        ozellikler = model_paketi['features']
        
        # Veri hazırlama
        X = []
        for ozellik in ozellikler:
            deger = cevre_verileri.get(ozellik, 0)
            X.append(deger)
        
        X = np.array(X).reshape(1, -1)
        X_scaled = scaler.transform(X)
        
        # Tahmin
        tahmin = model.predict(X_scaled)[0]
        
        # Güvenlik kontrolü (0-24 saat arası)
        tahmin = max(0, min(24, tahmin))
        
        return round(tahmin, 1)
    
    def get_risk_level(self, tahmin_saat):
    
        if tahmin_saat >= 6:
            return "DÜŞÜK", "Uzun süreli dış mekan etkinlikleri güvenli"
        elif tahmin_saat >= 3:
            return "ORTA", "Kısa süreli dış mekan etkinlikleri önerilir"
        elif tahmin_saat >= 1:
            return "YÜKSEK", "Sınırlı dış mekan etkinlikleri, koruyucu önlemler"
        else:
            return "KRİTİK", "Dış mekan etkinlikleri önerilmez"

# Kullanım örneği
predictor = AllerMindPredictor()

# Çevresel veri örneği
cevre_verileri = {
    'upi_value': 3.5,                    # Polen indeksi
    'plant_upi_value': 2.8,              # Bitki spesifik polen
    'in_season': 1,                      # Mevsim durumu (1: evet, 0: hayır)
    'plant_in_season': 1,                # Bitki mevsimi
    'pm2_5': 25.0,                       # İnce partikül madde (µg/m³)
    'pm10': 40.0,                        # Kaba partikül madde (µg/m³)
    'ozone': 85.0,                       # Ozon seviyesi (µg/m³)
    'nitrogen_dioxide': 35.0,            # Azot dioksit (µg/m³)
    'sulphur_dioxide': 15.0,             # Kükürt dioksit (µg/m³)
    'carbon_monoxide': 1.2,              # Karbon monoksit (mg/m³)
    'temperature_2m': 22.5,              # Sıcaklık (°C)
    'relative_humidity_2m': 65.0,        # Bağıl nem (%)
    'precipitation': 0.0,                # Yağış (mm)
    'wind_speed_10m': 12.0,              # Rüzgar hızı (km/h)
    'uv_index': 7.0                      # UV indeksi
}

# Her grup için tahmin
for grup in predictor.models.keys():
    saatlik_tahmin = predictor.predict_safe_hours(grup, cevre_verileri)
    risk_seviyesi, oneri = predictor.get_risk_level(saatlik_tahmin)
    
    print(f"\n{grup}:")
    print(f"  Güvenli süre: {saatlik_tahmin} saat")
    print(f"  Risk seviyesi: {risk_seviyesi}")
    print(f"  Öneri: {oneri}")
```

## Girdi Parametreleri

### Zorunlu Çevresel Veriler (26 parametre)

#### Polen Verileri
- `upi_value`: Genel polen indeksi (0-12 arası)
- `plant_upi_value`: Bitki spesifik polen değeri (0-12 arası)  
- `in_season`: Genel mevsim durumu (0 veya 1)
- `plant_in_season`: Bitki mevsimi durumu (0 veya 1)

#### Hava Kalitesi Verileri
- `pm2_5`: İnce partikül madde (0-500 µg/m³)
- `pm10`: Kaba partikül madde (0-600 µg/m³)
- `ozone`: Ozon seviyesi (0-400 µg/m³)
- `nitrogen_dioxide`: Azot dioksit (0-200 µg/m³)
- `sulphur_dioxide`: Kükürt dioksit (0-1000 µg/m³)
- `carbon_monoxide`: Karbon monoksit (0-30 mg/m³)

#### Meteorolojik Veriler
- `temperature_2m`: 2m yükseklikteki sıcaklık (-40°C ile 50°C arası)
- `relative_humidity_2m`: Bağıl nem (0-100%)
- `precipitation`: Yağış miktarı (0-200 mm)
- `snowfall`: Kar yağışı (0-100 mm)
- `rain`: Yağmur (0-200 mm)
- `cloud_cover`: Bulut örtüsü (0-100%)
- `surface_pressure`: Yüzey basıncı (900-1100 hPa)
- `wind_speed_10m`: 10m yükseklikteki rüzgar hızı (0-200 km/h)
- `wind_direction_10m`: Rüzgar yönü (0-360°)
- `soil_temperature_0_to_7cm`: Toprak sıcaklığı (-20°C ile 40°C arası)
- `soil_moisture_0_to_7cm`: Toprak nemi (0-1 arası)
- `sunshine_duration`: Güneşlenme süresi (0-24 saat)
- `uv_index`: UV indeksi (0-15 arası)
- `uv_index_clear_sky`: Açık hava UV indeksi (0-15 arası)
- `dust`: Toz seviyesi (0-500 µg/m³)
- `methane`: Metan seviyesi (1800-2000 ppb)

## ⚙️ Algoritma Detayları

### Random Forest (Grup 1)
- **Ağaç sayısı**: 100
- **Maksimum derinlik**: 15
- **Minimum örnek bölünme**: 5
- **Bootstrap örnekleme**: Aktif
- **Özellik rastgeleliği**: √n_features

### RBF SVM (Grup 2-5)
- **Kernel**: Radial Basis Function
- **C parametresi**: 100 (düzenleme gücü)
- **Gamma**: 'scale' (1/n_features)
- **Epsilon**: 0.1 (tolerans)

## 🔒 Güvenlik ve Doğrulama

### Model Güvenilirliği
- **Çapraz doğrulama**: 5-fold CV uygulandı
- **Test verisi**: %20 ayrılmış veri kümesi
- **Overfitting kontrolü**: Düzenleme teknikleri kullanıldı

### Çıktı Doğrulaması
- **Aralık kontrolü**: 0-24 saat arası sınırlandırma
- **Tutarlılık kontrolleri**: Çevresel koşullar arası mantıksal ilişkiler
- **Risk seviyesi eşlikleri**: Otomatik güvenlik önerileri

## 📈 Performans Metrikleri

### Başarı Göstergeleri
- **R² Score**: Model açıklama gücü (%99+ tüm gruplar)
- **MSE**: Ortalama kare hatası (< 0.01 tüm gruplar)
- **MAE**: Ortalama mutlak hata (< 0.05 tüm gruplar)
- **Cross-Validation**: Tutarlı performans doğrulaması

### Sistem Gereksinimleri
- **Python**: 3.8+
- **scikit-learn**: 1.0+
- **numpy**: 1.20+
- **pickle**: Standart kütüphane

## 🔧 Sorun Giderme

### Yaygın Hatalar

1. **Model yüklenemedi**: Dosya yolu kontrolü yapın
2. **Geçersiz parametre**: Veri tiplerini kontrol edin
3. **Eksik özellik**: 26 parametrenin tamamı gerekli
4. **Aralık dışı değer**: Parametre sınırlarını kontrol edin

### İletişim ve Destek
- **Sürüm**: 2.0 (Güncellenme: 12 Eylül 2025)
- **Geliştirici**: AllerMind ML Takımı
- **Son güncelleme**: Optimizasyon ve algoritma iyileştirmeleri

---

*Bu kılavuz, AllerMind makine öğrenmesi modelinin güvenli ve etkili kullanımı için hazırlanmıştır. Tıbbi karar alma süreçlerinde mutlaka uzman hekimin görüşü alınmalıdır.*
