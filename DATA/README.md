# 🧠 AllerMind V2.0 - Expert Model System

## � Genel Bakış

AllerMind V2.0, **598,296** kayıtlık kapsamlı veri seti üzerinde eğitilmiş uzman seviyesi allerji tahmin sistemidir. 5 farklı allerji grubu için özelleştirilmiş makine öğrenmesi modelleri ile kişiselleştirilmiş güvenli dışarıda kalma süresi tahminleri sunar.

**NOT:** İşlemler MODEL/version2_pkl_models içerisindeki modeller ile yapılmıştır ancak dosya büyüklüğü nedeniyle drive'da saklanmaktadır. Aşağıda link üzerinden ulaşılabilir. Diğer kullanımda duran tüm modeller eski versiyona aittir.

## 🎯 Temel Özellikler

- ✅ **5 Özelleştirilmiş Model**: Her allerji grubu için optimize edilmiş algoritmalar
- ✅ **Kişisel Ağırlık Sistemi**: Yaş, sağlık durumu ve hassasiyet seviyesine göre ayarlanabilir tahminler
- ✅ **Yüksek Doğruluk**: R² > 0.5, MAE < 0.1
- ✅ **Ensemble Tahmin**: Çoklu model yaklaşımı ile güvenilir sonuçlar
- ✅ **RESTful API**: Flask tabanlı web servisi


## 👥 Allerji Grupları

1. **Polen Hassasiyeti** - Ağaç, çimen ve yabani ot alerjileri
2. **Hava Kirliliği** - PM2.5, PM10, NO2, Ozon hassasiyeti
3. **UV & Güneş** - UV indeksi ve güneş maruziyeti hassasiyeti
4. **Meteorolojik** - Basınç, nem, rüzgar hassasiyeti
5. **Hassas Grup** - Çocuk/yaşlı, çoklu faktör hassasiyeti

## 📋 Örnek Veri Formatı

### Giriş Verileri

| Parametre | Örnek Değer | Birim | Açıklama |
|-----------|-------------|-------|----------|
| `temperature_2m` | 25.0 | °C | Hava sıcaklığı |
| `relative_humidity_2m` | 60.0 | % | Bağıl nem |
| `pm10` | 30.0 | µg/m³ | Partikül madde (10µm) |
| `pm2_5` | 18.0 | µg/m³ | Partikül madde (2.5µm) |
| `uv_index` | 7.0 | - | UV indeksi |
| `nitrogen_dioxide` | 25.0 | µg/m³ | Azot dioksit |
| `ozone` | 80.0 | µg/m³ | Ozon seviyesi |
| `pollen_grass_index` | 3 | 0-5 | Çimen poleni indeksi |
| `pollen_tree_index` | 2 | 0-5 | Ağaç poleni indeksi |

### Kişisel Parametreler

| Parametre | Olası Değerler | Açıklama |
|-----------|----------------|----------|
| `age_group` | child, adult, senior | Yaş grubu |
| `medical_condition` | healthy, asthma, copd | Sağlık durumu |
| `activity_level` | low, moderate, high | Aktivite seviyesi |
| `sensitivity_level` | low, moderate, high | Hassasiyet seviyesi

| `sensitivity_level` | low, moderate, high | Hassasiyet seviyesi |


### Kurulum

```bash
pip install -r requirements.txt
```

### Python Kullanımı

```python
from expert_predictor import ExpertAllermindPredictor

# Predictor oluştur
predictor = ExpertAllermindPredictor()

# Çevresel veriler
env_data = {
    'temperature_2m': 25.0,
    'relative_humidity_2m': 60.0,
    'pm10': 30.0,
    'pm2_5': 18.0,
    'uv_index': 7.0
}

# Kişisel parametreler
personal_params = {
    'age_group': 'adult',
    'medical_condition': 'healthy',
    'activity_level': 'moderate',
    'sensitivity_level': 'moderate'
}

# Tahmin yap
result = predictor.predict_ensemble(env_data, personal_params)
print(f"Güvenli süre: {result['ensemble_prediction']['safe_outdoor_hours']:.1f} saat")
```

### API Kullanımı

```bash
# API'yi başlat
python expert_api_service.py

# Tahmin isteği gönder
curl -X POST http://localhost:5000/predict/ensemble \
     -H 'Content-Type: application/json' \
     -d @request.json
```

## 📁 Dosya Yapısı

```
[version2_pkl_models](https://drive.google.com/drive/folders/1rpT4Sf3uRztBUEqGKoubKgCXd14NcJ34?usp=sharing)/
├── expert_predictor.py          # Ana tahmin sistemi
├── expert_api_service.py        # Flask API servisi
├── expert_model_creator.py      # Model eğitim scripti
├── ensemble_config_v2.json      # Ensemble konfigürasyonu
├── Grup1_advanced_model_v2.pkl  # Grup 1 modeli
├── Grup2_advanced_model_v2.pkl  # Grup 2 modeli
├── Grup3_advanced_model_v2.pkl  # Grup 3 modeli
├── Grup4_advanced_model_v2.pkl  # Grup 4 modeli
├── Grup5_advanced_model_v2.pkl  # Grup 5 modeli
├── data_analysis.py             # Veri analiz araçları
└── requirements.txt             # Bağımlılıklar
```

## 🔬 Teknik Detaylar

- **Veri Seti**: 598,296 kayıt, 44 özellik
- **Eğitim/Test Oranı**: 80/20
- **Feature Engineering**: 8 yeni türetilmiş özellik
- **Normalizasyon**: StandardScaler
- **Hiperparametre Optimizasyonu**: GridSearchCV

## 📖 Dokümantasyon

- **[Detaylı Tutorial](EXPERT_MODEL_TUTORIAL.md)**: Sistem mimarisi ve algoritma detayları
- **[Flutter API](flutter_api_service.py)**: Mobil uygulama entegrasyonu

## 🤝 Destek

Sorularınız için: duyymazelif@gmail.com

---

*🌟 AllerMind V2.0 - Kişiselleştirilmiş allerji yönetimi için bilimsel yaklaşım*
curl http://localhost:5000/models/info
```

### 📋 API Endpoints

- `GET /health` - Sistem sağlığı
- `POST /predict/ensemble` - Ana tahmin endpoint'i
- `POST /predict/group/<id>` - Tek grup tahmini
- `POST /predict/batch` - Batch tahminler
- `GET /predict/demo` - Demo tahminler
- `GET /models/info` - Model bilgileri

### 🎛️ Kişisel Ağırlık Sistemi

#### Yaş Grupları
- `child` (1.5x) - Çocuklar için arttırılmış hassasiyet
- `adult` (1.0x) - Standart yetişkin hassasiyeti
- `elderly` (1.3x) - Yaşlılar için arttırılmış hassasiyet

#### Tıbbi Durum
- `healthy` (1.0x) - Sağlıklı birey
- `allergy` (1.2x) - Alerji hastası
- `asthma` (1.4x) - Astım hastası

#### Aktivite Seviyesi
- `low` (0.9x) - Düşük aktivite
- `moderate` (1.0x) - Orta aktivite
- `high` (1.2x) - Yüksek aktivite

#### Hassasiyet Seviyesi
- `low` (0.8x) - Düşük hassasiyet
- `moderate` (1.0x) - Orta hassasiyet
- `high` (1.3x) - Yüksek hassasiyet
- `very_high` (1.6x) - Çok yüksek hassasiyet

### 📚 Detaylı Dokümantasyon

Sistem hakkında detaylı bilgi için `EXPERT_MODEL_TUTORIAL.md` dosyasına bakınız.

### 🔬 Teknik Detaylar

- **Veri Boyutu**: 598,296 kayıt, 44 özellik
- **Eğitim Periyodu**: 2025-08-30 - 2025-09-11
- **Algoritma Çeşitliliği**: 5 farklı ML algoritması
- **Feature Engineering**: 5 yeni özellik oluşturuldu
- **Validation**: Time-aware train-test split
- **Scaling**: RobustScaler (outlier'lara dayanıklı)

### 🏆 Başarı Metrikleri

- ✅ Tüm modellerde R² > 0.90
- ✅ Düşük overfitting (gap < 0.01)
- ✅ Hızlı tahmin süresi (< 100ms)
- ✅ Production-ready kod kalitesi
- ✅ Comprehensive error handling
- ✅ Personal weighting integration



**ALLERMIND V2.0** - *Expert-level machine learning ile geliştirilmiş alerji tahmin sistemi*