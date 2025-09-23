# AllerMind Work-Model Sistemi - Kullanım Kılavuzu

## 📋 İçindekiler

1. [Sistem Genel Bakış](#sistem-genel-bakış)
2. [Kurulum ve Gereksinimler](#kurulum-ve-gereksinimler) 
3. [Modül Açıklamaları](#modül-açıklamaları)
4. [API Referansı](#api-referansı)
5. [Kullanım Örnekleri](#kullanım-örnekleri)
6. [İmmunolojik Model Detayları](#immunolojik-model-detayları)
7. [Troubleshooting](#troubleshooting)

---

## 🧬 Sistem Genel Bakış

AllerMind Work-Model sistemi, kullanıcının kişisel alerji profiline göre dinamik grup belirleme ve risk tahmini yapan gelişmiş bir yapay zeka sistemidir. Sistem immunolojik prensiplere dayalı hiyerarşik karar ağacı kullanarak kullanıcıları 5 farklı gruba sınıflandırır ve her grup için özelleştirilmiş makine öğrenmesi modelleri ile risk tahmini gerçekleştirir.

### 🎯 Temel Özellikler

- **İmmunolojik Grup Sınıflandırması**: IgE seviyeleri, Th1/Th2 dengesine göre 5 grup
- **Kişiselleştirilmiş Risk Tahmini**: Kullanıcı özelliklerine göre modifiye edilmiş tahminler
- **Çoklu Veri Kaynağı**: Polen, hava kalitesi, hava durumu verilerinin entegrasyonu
- **Çapraz Reaksiyon Analizi**: Polen-besin çapraz reaksiyonlarının modellenmesi
- **Gerçek Zamanlı Öneriler**: Risk seviyesine göre dinamik öneriler

---

## ⚙️ Kurulum ve Gereksinimler

### Gerekli Kütüphaneler

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
pip install pickle datetime typing dataclasses enum
```

### Dosya Yapısı

```
WORK-MODEL/
├── user_preference_system.py      # Kullanıcı tercihleri ve grup belirleme
├── data_loader.py                 # Veri yükleme ve işleme modülü  
├── allermind_predictor.py         # Ana tahmin sistemi
├── demo_system.py                 # Demo ve test sistemi
├── README.md                      # Bu dosya
└── requirements.txt               # Gereksinimler
```

### Veri Gereksinimleri

Sistem aşağıdaki CSV dosyalarını bekler (`/DATA/16SEP/` klasöründe):
- `air_quality_data.csv` - Hava kalitesi verileri
- `pollen_data.csv` - Polen verileri
- `plant_data.csv` - Bitki verileri

---

## 📦 Modül Açıklamaları

### 1. user_preference_system.py

Kullanıcı tercihlerini yönetir ve immunolojik prensiplere dayalı grup sınıflandırması yapar.

**Ana Sınıflar:**
- `UserPreferences`: Kullanıcı veri yapısı
- `AllergyGroupClassifier`: Grup belirleme algoritması
- `AllergyGroup`: Grup tanımları (Enum)

**İmmunolojik Gruplar:**

| Grup ID | Grup Adı | İmmunolojik Profil | Model Ağırlığı |
|---------|----------|-------------------|----------------|
| 1 | Şiddetli Alerjik | IgE > 1000 IU/mL, Anaphylaxis riski | 0.18 |
| 2 | Hafif-Orta Alerjik | IgE 200-1000 IU/mL, Kontrol edilebilir | 0.22 |
| 3 | Genetik Yatkınlık | Atopik yapı, ailesel yüklenme | 0.24 |
| 4 | Teşhis Almamış | Normal/sınırda IgE, belirsiz | 0.24 |
| 5 | Hassas Çocuk/Yaşlı | İmmün immatürite/yaşlanma | 0.12 |

### 2. data_loader.py

16SEP klasöründeki CSV verilerini yükler ve model formatına dönüştürür.

**Ana Sınıflar:**
- `DataLoader`: Veri yükleme ve işleme
- `EnvironmentalData`: Çevresel veri yapısı

**Özellik Kategorileri:**
- **Hava Kalitesi**: PM10, PM2.5, CO2, CO, NO2, SO2, O3, UV indeksi
- **Polen Verileri**: UPI değerleri, mevsim bilgisi, çeşitlilik indeksi
- **Hava Durumu**: Sıcaklık, nem, rüzgar, bulutluluk

### 3. allermind_predictor.py

Ana tahmin sistemini içerir. Grup belirleme sonrasında ilgili modeli aktive eder.

**Ana Sınıflar:**
- `AllerMindPredictor`: Ana tahmin sınıfı
- `PredictionResult`: Tahmin sonucu veri yapısı

**İmmunolojik Modifikasyonlar:**

```python
# Grup bazlı hassasiyet ağırlıkları
immunologic_weights = {
    1: {  # Şiddetli Alerjik Grup
        'pollen_sensitivity': 2.0,
        'environmental_amplifier': 1.8,
        'cross_reactivity_bonus': 1.5,
        'weather_sensitivity': 1.6
    }
    # ... diğer gruplar
}
```

### 4. demo_system.py

Sistemin test edilmesi ve demonstrasyonu için kapsamlı demo araçları.

**Demo Kullanıcıları:**
- Şiddetli alerjik hasta
- Hafif-orta alerjik hasta  
- Genetik yatkınlığı olan
- Teşhis almamış
- Hassas çocuk
- Hassas yaşlı

---

## 🔧 API Referansı

### AllergyGroupClassifier

```python
classifier = AllergyGroupClassifier()

# Grup belirleme
group_result = classifier.determine_allergy_group(user_preferences)

# Sonuç yapısı:
{
    'group_id': int,
    'group_name': str,
    'assignment_reason': str,
    'model_weight': float,
    'personal_risk_modifiers': Dict[str, float],
    'immunologic_profile': Dict,
    'pollen_specific_risks': Dict,
    'recommendation_adjustments': Dict
}
```

### AllerMindPredictor

```python
predictor = AllerMindPredictor()

# Ana tahmin fonksiyonu
result = predictor.predict_allergy_risk(
    user_preferences=user_prefs,
    location=(latitude, longitude),
    target_datetime=datetime.now()  # Optional
)

# Sonuç yapısı (PredictionResult):
{
    'risk_score': float,           # 0-1 arası risk skoru
    'confidence': float,           # Güven aralığı
    'risk_level': str,            # low, moderate, high, severe  
    'group_id': int,              # Kullanıcı grubu
    'contributing_factors': Dict,  # Katkı faktörleri
    'recommendations': List[str],  # Öneriler
    'environmental_risks': Dict,   # Çevresel risk faktörleri
    'personal_modifiers_applied': Dict  # Uygulanan modifikasyonlar
}
```

### DataLoader

```python
loader = DataLoader()

# Çevresel veri yükleme
env_data = loader.combine_environmental_data(
    lat=41.0082, 
    lon=28.9784, 
    target_datetime=datetime.now()
)

# Model girdi hazırlama
model_input = loader.prepare_model_input(
    lat=41.0082, 
    lon=28.9784,
    target_datetime=datetime.now(),
    user_modifiers={'base_sensitivity': 1.2}
)
```

---

## 💡 Kullanım Örnekleri

### Temel Kullanım

```python
from user_preference_system import UserPreferences, AllergyGroupClassifier
from allermind_predictor import AllerMindPredictor

# 1. Kullanıcı profilini oluştur
user = UserPreferences(
    age=28,
    gender='female',
    location={'latitude': 41.0082, 'longitude': 28.9784},
    clinical_diagnosis='mild_moderate_allergy',
    family_allergy_history=True,
    previous_allergic_reactions={'anaphylaxis': False, 'severe_asthma': False, 'hospitalization': False},
    current_medications=['antihistamine'],
    tree_pollen_allergy={'birch': True, 'olive': False, 'pine': False},
    grass_pollen_allergy={'graminales': True},
    weed_pollen_allergy={'ragweed': True, 'mugwort': False},
    food_allergies={'apple': True, 'nuts': False, 'shellfish': False},
    environmental_triggers={'dust_mites': True, 'pet_dander': False, 'mold': True, 'air_pollution': True, 'smoke': False}
)

# 2. Tahmin sistemini başlat
predictor = AllerMindPredictor()

# 3. Risk tahmini yap
location = (41.0082, 28.9784)  # İstanbul
result = predictor.predict_allergy_risk(user, location)

# 4. Sonuçları görüntüle
print(f"Risk Skoru: {result.risk_score:.3f}")
print(f"Risk Seviyesi: {result.risk_level}")
print(f"Grup: {result.group_name}")
print("Öneriler:")
for rec in result.recommendations:
    print(f"  - {rec}")
```

### Toplu Tahmin

```python
# Çoklu kullanıcı için tahmin
users_data = [
    {
        'age': 28, 'gender': 'female', 
        'clinical_diagnosis': 'severe_allergy',
        # ... diğer alanlar
    },
    {
        'age': 35, 'gender': 'male',
        'clinical_diagnosis': 'mild_moderate_allergy', 
        # ... diğer alanlar
    }
]

locations = [(41.0082, 28.9784), (39.9334, 32.8597)]

results = predictor.batch_predict(users_data, locations)

for i, result in enumerate(results):
    print(f"Kullanıcı {i+1}: Risk {result.risk_score:.3f} ({result.risk_level})")
```

### Zaman Serisi Analizi

```python
from datetime import datetime, timedelta

# 7 günlük tahmin
base_date = datetime.now()
daily_predictions = []

for i in range(7):
    target_date = base_date + timedelta(days=i)
    result = predictor.predict_allergy_risk(user, location, target_date)
    daily_predictions.append({
        'date': target_date.strftime('%Y-%m-%d'),
        'risk_score': result.risk_score,
        'risk_level': result.risk_level
    })

# Sonuçları görüntüle
for pred in daily_predictions:
    print(f"{pred['date']}: {pred['risk_score']:.3f} ({pred['risk_level']})")
```

---

## 🧬 İmmunolojik Model Detayları

### Grup Belirleme Algoritması

Sistem hiyerarşik karar ağacı kullanır:

1. **Yaş Değerlendirmesi**: ≤12 veya ≥65 yaş → Grup 5 yönelimi
2. **Klinik Tanı**: Şiddetli alerji → Grup 1, Hafif-orta → Grup 2
3. **Polen Hassasiyeti**: Risk skoru hesaplanır
4. **Genetik Faktörler**: Aile geçmişi + yüksek polen riski → Grup 3
5. **Varsayılan**: Grup 4

### Risk Skoru Hesaplaması

```python
# Temel model tahmini
base_prediction = model.predict(scaled_input)

# İmmunolojik modifikasyonlar
modified_prediction = base_prediction * pollen_modifier * env_modifier * weather_modifier

# Risk seviyesi belirleme
if modified_prediction >= 0.9: risk_level = 'severe'
elif modified_prediction >= 0.8: risk_level = 'high'  
elif modified_prediction >= 0.6: risk_level = 'moderate'
else: risk_level = 'low'
```

### Çapraz Reaksiyon Modeli

```python
cross_reactivity_matrix = {
    'birch': ['apple', 'cherry', 'pear', 'almond'],    # Rosaceae ailesi
    'ragweed': ['melon', 'banana', 'cucumber'],         # OAS sendromu
    'mugwort': ['celery', 'spices', 'herbs']            # Baharatlı bitkiler
}
```

### Kişisel Modifikasyonlar

- **Yaş Faktörü**: Çocuk/yaşlı için %20-30 artış
- **Çevresel Tetikleyiciler**: Her tetikleyici için %10 artış
- **Astım Komorbidite**: %40 artış
- **Grup Spesifik**: Grup 1 için %50 mevsimsel artış

---

## 🚨 Troubleshooting

### Yaygın Hatalar ve Çözümler

#### 1. Model Yükleme Hatası
```
Error: Grup X modeli bulunamadı
```
**Çözüm**: MODEL/pkl_models klasöründe ilgili .pkl dosyalarını kontrol edin.

#### 2. Veri Yükleme Hatası
```  
Error: Gerekli veri dosyaları eksik
```
**Çözüm**: 16SEP klasöründe gerekli CSV dosyalarını kontrol edin.

#### 3. Koordinat Hatası
```
Error: Konum için veri bulunamadı
```
**Çözüm**: Koordinatları kontrol edin, sistem ±0.5 derece toleransla çalışır.

### Performans Optimizasyonu

1. **Veri Önbellekleme**: Sık kullanılan konumlar için veri önbelleği
2. **Model Caching**: Modelleri bellekte tutma
3. **Batch Processing**: Çoklu tahmin için toplu işlem

### Loglama ve Debug

```python
import logging
logging.basicConfig(level=logging.INFO)

# Debug modunda çalıştırma
predictor = AllerMindPredictor()
result = predictor.predict_allergy_risk(user, location)

# Model bilgilerini görme
model_info = predictor.get_model_info()
print(f"Loaded models: {model_info['loaded_models']}")
```

---

## 📊 Sistem Sınırları ve Kısıtlamalar

### Veri Sınırları
- Polen verisi: ±3 gün tolerans
- Hava kalitesi: ±6 saat tolerans  
- Konum: ±0.5 derece tolerans

### Model Sınırları
- Risk skoru: 0.0-1.0 arası
- Güven aralığı: Minimum %50
- Desteklenen polen türleri: GRASS, TREE, WEED

### Sistem Gereksinimleri
- Python 3.7+
- Minimum 2GB RAM
- Disk alanı: ~100MB (modellar dahil)

---

## 🔄 Sistem Güncelleme ve Bakım

### Model Güncelleme
```python
# Yeni model ekleme
predictor.models[6] = new_model
predictor.scalers[6] = new_scaler

# Ensemble konfigürasyonu güncelleme  
predictor.ensemble_config['models']['6'] = {'weight': 0.15}
```

### Veri Güncelleme
```python
# Yeni veri kaynağı ekleme
loader = DataLoader(data_path="/path/to/new/data")
```

---

## 📞 Destek ve İletişim

Bu sistem immunolojik prensiplere dayalı akademik bir çalışmadır. Tıbbi karar alma aracı değil, destekleyici bilgi sistemidir.

**Dikkat**: Sistemin önerileri kesinlikle tıbbi tavsiye yerine geçmez. Ciddi sağlık durumları için mutlaka sağlık profesyoneline başvurunuz.

---

## 📄 Lisans ve Referanslar

Bu sistem aşağıdaki akademik standartlara uygun olarak geliştirilmiştir:
- WHO Hava Kalitesi Standartları
- AAAAI (American Academy of Allergy, Asthma & Immunology) Kılavuzları  
- EAACİ (European Academy of Allergy and Clinical Immunology) Önerileri

**Geliştirici**: AI Expert - İstatistik ve İmmunoloji Uzmanı
**Tarih**: 16 Eylül 2025
**Versiyon**: 1.0