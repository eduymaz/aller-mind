# 🌟 AllerMind - Allerji Tahmin Sistemi

## 📊 Proje Özeti

AllerMind, 5 farklı allerji profiline sahip bireyler için özelleştirilmiş bir tahmin sistemidir. Hava durumu, hava kalitesi ve polen verilerini analiz ederek, kullanıcılara güvenli vakit geçirme süresi önerisi sunar.

## 🎯 Temel Özellikler

- **5 Özelleştirilmiş Allerji Grubu** için ayrı modeller
- **Yüksek Doğruluk**: R² > 0.99, RMSE < 0.081
- **Kapsamlı Veri Analizi**: 175,872 satır veri
- **Bilimsel Parametre Ağırlıklandırma**
- **Real-time Tahmin Sistemi**

## 📁 Dosya Yapısı

```
DATA/ML/
├── data_processor.py          # Veri işleme ve temizleme
├── allergy_predictor.py       # Ana tahmin sistemi
├── demo.py                    # Demo ve test uygulaması
├── analysis_report.py         # Detaylı analiz raporu
├── KULLANIM_KILAVUZU.md      # Kullanım kılavuzu
├── README.md                  # Bu dosya
├── cleaned_combined_data.csv  # Temizlenmiş veri
├── allergy_analysis_report.md # Detaylı analiz raporu
└── models/                    # Eğitilmiş modeller
    ├── group_1_model.pkl
    ├── group_1_scaler.pkl
    ├── ...
    └── group_weights.json
```

## 👥 Allerji Grupları

### Grup 1: Şiddetli Alerjik Grup
- **Polen Odağı**: %40 ağırlık
- **Ortalama Güvenli Süre**: 1.48 saat
- **Hassasiyet Eşiği**: 0.2

### Grup 2: Hafif-Orta Grup
- **Dengeli Yaklaşım**: Polen %30, Hava Kalitesi %30, Hava Durumu %40
- **Ortalama Güvenli Süre**: 4.21 saat
- **Hassasiyet Eşiği**: 0.4

### Grup 3: Olası Alerjik/Genetik
- **Polen Odağı**: %35 ağırlık
- **Ortalama Güvenli Süre**: 2.38 saat
- **Hassasiyet Eşiği**: 0.3

### Grup 4: Teşhis Almamış
- **Temkinli Yaklaşım**: Hava kalitesi %35 ağırlık
- **Ortalama Güvenli Süre**: 5.71 saat
- **Hassasiyet Eşiği**: 0.5

### Grup 5: Hassas Grup (Çocuk/Yaşlı)
- **Hava Kalitesi Odağı**: %45 ağırlık
- **Ortalama Güvenli Süre**: 6.23 saat
- **Hassasiyet Eşiği**: 0.6

## 🚀 Hızlı Başlangıç

### 1. Bağımlılıkları Yükle
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

### 2. Demo Çalıştır
```bash
cd DATA/ML
python demo.py
```

### 3. Temel Kullanım
```python
from allergy_predictor import AllergyGroupPredictor

# Predictor oluştur ve modelleri yükle
predictor = AllergyGroupPredictor()

# Giriş verisi hazırla
input_data = {
    'temperature_2m': 25,
    'relative_humidity_2m': 60,
    'pm10': 20,
    'pm2_5': 12,
    'upi_value': 2,
    'pollen_code': 'GRASS',
    'in_season': True,
    # ... diğer parametreler
}

# Tahmin yap (Grup 1 için)
result = predictor.predict_safe_time(input_data, group_id=1)
print(f"Güvenli süre: {result['predicted_safe_hours']} saat")
print(f"Öneri: {result['recommendation']}")
```

## 📊 Model Performansı

| Grup | Model R² | RMSE | Ortalama Güvenli Süre |
|------|----------|------|----------------------|
| 1    | 1.000    | 0.047| 1.48 saat           |
| 2    | 0.997    | 0.081| 4.21 saat           |
| 3    | 1.000    | 0.049| 2.38 saat           |
| 4    | 0.992    | 0.051| 5.71 saat           |
| 5    | 0.994    | 0.020| 6.23 saat           |

## 🧪 Test Senaryoları

### İdeal Hava Koşulları
- **En İyi Performans**: Grup 4 (7.36 saat)
- **En Kısıtlı**: Grup 1 (5.93 saat)
- **Risk Seviyesi**: Tüm gruplar düşük

### Yüksek Polen Sezonu
- **En İyi Performans**: Grup 4 (5.84 saat)
- **En Kısıtlı**: Grup 1 (0.0 saat)
- **Risk Seviyesi**: Grup 1,3 kritik

### Kötü Hava Kalitesi
- **En İyi Performans**: Grup 5 (6.38 saat)
- **En Kısıtlı**: Grup 1 (0.0 saat)
- **Risk Seviyesi**: Yüksek

## 🛠️ Sistem Mimarisi

### Veri İşleme Katmanı
- **Veri Kaynaklarını Birleştirme**: 3 günlük veri (30-31 Ağustos, 1 Eylül)
- **Veri Temizleme**: Eksik değer işleme, outlier tespiti
- **Özellik Mühendisliği**: Kategorik encoding, zaman özellikleri

### Model Katmanı
- **Algoritma**: Random Forest Regressor
- **Grup Bazlı Modeller**: Her grup için ayrı model
- **Parametre Ağırlıklandırma**: Bilimsel temelli ağırlıklar

### Tahmin Katmanı
- **Risk Skoru Hesaplama**: Polen, hava kalitesi, hava durumu
- **Güvenli Süre Tahmini**: Grup hassasiyetine göre
- **Öneri Sistemi**: Risk seviyesine göre öneriler

## 📈 Analiz Sonuçları

### Önemli Bulgular
1. **Şiddetli alerjik grup** en kısıtlı yaşam koşullarına sahip
2. **Polen mevsimi** kritik risk faktörü
3. **Hava kalitesi** tüm gruplar için önemli
4. **Hassas grup** paradoksal olarak en toleranslı

### İstatistiksel Özetler
- **Ortalama Güvenli Süre**: 4.00 saat
- **Risk Skoru Aralığı**: 0.128 - 0.720
- **En Yüksek Varyasyon**: Grup 1 (0-7.36 saat)

## 🔧 Gelişmiş Özellikler

### Özellik Önem Analizi
```python
from demo import AllergyPredictionDemo
demo = AllergyPredictionDemo()
demo.analyze_feature_importance()
```

### Grup Karşılaştırması
```python
# Tüm gruplar için karşılaştırma
demo.compare_all_groups(input_data)
```

### İnteraktif Tahmin
```python
# Kullanıcı girişi ile tahmin
demo.interactive_prediction()
```

## 📚 Dokümantasyon

- **[Kullanım Kılavuzu](https://github.com/eduymaz/aller-mind/blob/main/DATA/ML/KULLANIM_KILAVUZU.md)**: Detaylı kullanım talimatları
- **[Analiz Raporu](https://github.com/eduymaz/aller-mind/blob/main/DATA/ML/allergy_analysis_report.md)**: Kapsamlı analiz sonuçları

## 🔮 Gelecek Geliştirmeler

- [ ] Coğrafi mikro-iklim analizi
- [ ] Wearable cihaz entegrasyonu

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Branch'i push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

- **Proje Sahibi**: Elif Duymaz Yilmaz
- **E-posta**: duyymazelif@gmail.com
- **GitHub**: [GitHub Repository](https://github.com/eduymaz/aller-mind/)

## 🙏 Teşekkürler

- OpenWeather API
- Google Pollen API
- Scikit-learn Topluluğu
- Pandas Geliştiricileri

---

*🌟 AllerMind ile daha sağlıklı, bilinçli ve güvenli günler!*
