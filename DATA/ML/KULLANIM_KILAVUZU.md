# 🌟 AllerMind - Allerji Tahmin Sistemi Kullanım Kılavuzu

## 📋 İçindekiler
1. [Sistem Genel Bakış](#sistem-genel-bakış)
2. [Kurulum ve Kullanım](#kurulum-ve-kullanım)
3. [API Kullanımı](#api-kullanımı)
4. [Allerji Grupları](#allerji-grupları)
5. [Örnek Kullanımlar](#örnek-kullanımlar)
6. [Parametre Açıklamaları](#parametre-açıklamaları)
7. [Sık Sorulan Sorular](#sık-sorulan-sorular)

---

## 🎯 Sistem Genel Bakış

AllerMind, 5 farklı allerji profili için özelleştirilmiş tahmin sistemidir. Hava durumu, hava kalitesi ve polen verilerini analiz ederek, kullanıcılara güvenli vakit geçirme süresi önerisi sunar.

### ✨ Temel Özellikler:
- **5 farklı allerji grubu** için özelleştirilmiş modeller
- **Real-time** hava durumu ve polen analizi
- **Bilimsel veriye dayalı** tahminler
- **Kullanıcı dostu** öneri sistemi
- **Yüksek doğruluk** oranı (R² > 0.99)

---

## 🔧 Kurulum ve Kullanım

### Gereksinimler:
```bash
pandas>=1.5.0
numpy>=1.20.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
seaborn>=0.11.0
```

### Temel Kullanım:

```python
from allergy_predictor import AllergyGroupPredictor

# Predictor oluştur
predictor = AllergyGroupPredictor()

# Veri ile model eğit
predictor.train_group_models(df)

# Tahmin yap
input_data = {
    'temperature_2m': 25,
    'relative_humidity_2m': 60,
    'pm10': 20,
    'upi_value': 2,
    # ... diğer parametreler
}

result = predictor.predict_safe_time(input_data, group_id=1)
print(f"Güvenli süre: {result['predicted_safe_hours']} saat")
```

---

## 🚀 API Kullanımı

### Tahmin İşlemi:

```python
def predict_safe_time(input_data: Dict, group_id: int) -> Dict:
    """
    Belirtilen grup için güvenli vakit tahmin et
    
    Args:
        input_data: Çevresel parametreler
        group_id: Allerji grubu (1-5)
        
    Returns:
        {
            'group_id': int,
            'group_name': str,
            'predicted_safe_hours': float,
            'risk_score': float,
            'recommendation': str,
            'risk_level': str
        }
    """
```

### Demo Çalıştırma:

```bash
cd DATA/ML
python demo.py
```

---

## 👥 Allerji Grupları

### 🔴 Grup 1: Şiddetli Alerjik Grup
- **Hedef Kitle**: Doktor tanısı ile şiddetli allerji
- **Hassasiyet**: En yüksek (Eşik: 0.2)
- **Polen Odağı**: %40 ağırlık
- **Ortalama Güvenli Süre**: 1.48 saat
- **Özellik**: Polen mevsiminde ciddi kısıtlamalar

### 🟡 Grup 2: Hafif-Orta Grup  
- **Hedef Kitle**: Hafif/orta seviye allerji
- **Hassasiyet**: Orta (Eşik: 0.4)
- **Dengeli Yaklaşım**: Polen %30, Hava Kalitesi %30, Hava Durumu %40
- **Ortalama Güvenli Süre**: 4.21 saat
- **Özellik**: Esnek günlük aktivite planlaması

### 🟠 Grup 3: Olası Alerjik/Genetik
- **Hedef Kitle**: Genetik yatkınlık, teşhis öncesi
- **Hassasiyet**: Yüksek (Eşik: 0.3)
- **Polen Odağı**: %35 ağırlık
- **Ortalama Güvenli Süre**: 2.38 saat
- **Özellik**: Proaktif önlem odaklı

### 🔵 Grup 4: Teşhis Almamış
- **Hedef Kitle**: Belirsiz allerji durumu
- **Hassasiyet**: Orta-Düşük (Eşik: 0.5)
- **Temkinli Yaklaşım**: Hava kalitesi %35 ağırlık
- **Ortalama Güvenli Süre**: 5.71 saat
- **Özellik**: Belirsizlik yönetimi

### 🟢 Grup 5: Hassas Grup (Çocuk/Yaşlı)
- **Hedef Kitle**: Çocuklar, yaşlılar, kronik hastalık
- **Hassasiyet**: Düşük allerji, yüksek genel hassasiyet (Eşik: 0.6)
- **Hava Kalitesi Odağı**: %45 ağırlık
- **Ortalama Güvenli Süre**: 6.23 saat
- **Özellik**: Genel sağlık odaklı

---

## 🧪 Örnek Kullanımlar

### Senaryo 1: İdeal Koşullarda Tahmin

```python
ideal_conditions = {
    'temperature_2m': 22,
    'relative_humidity_2m': 55,
    'precipitation': 0.1,  # Hafif yağış
    'wind_speed_10m': 3,
    'uv_index': 3,
    'pm10': 15,
    'pm2_5': 8,
    'upi_value': 1,  # Düşük polen
    'pollen_code': 'GRASS',
    'in_season': False
}

# Tüm gruplar için tahmin
for group_id in range(1, 6):
    result = predictor.predict_safe_time(ideal_conditions, group_id)
    print(f"Grup {group_id}: {result['predicted_safe_hours']} saat")
```

**Beklenen Sonuçlar:**
- Grup 1: ~6 saat
- Grup 2: ~7.3 saat  
- Grup 3: ~7.2 saat
- Grup 4: ~7.4 saat
- Grup 5: ~7.4 saat

### Senaryo 2: Yüksek Polen Sezonu

```python
high_pollen = {
    'temperature_2m': 28,
    'relative_humidity_2m': 35,
    'precipitation': 0,  # Kuru hava
    'wind_speed_10m': 15,  # Yüksek rüzgar
    'uv_index': 8,
    'pm10': 20,
    'pm2_5': 12,
    'upi_value': 4,  # Yüksek polen
    'pollen_code': 'WEED',
    'plant_code': 'RAGWEED',  # En alerjik bitki
    'in_season': True,
    'plant_in_season': True
}
```

**Beklenen Sonuçlar:**
- Grup 1: 0 saat (Dışarı çıkma)
- Grup 2: ~2.5 saat
- Grup 3: ~0.1 saat  
- Grup 4: ~5.8 saat
- Grup 5: ~5.5 saat

---

## 📊 Parametre Açıklamaları

### 🌤️ Hava Durumu Parametreleri:
- **temperature_2m**: Sıcaklık (°C)
- **relative_humidity_2m**: Nem oranı (%)
- **precipitation**: Yağış miktarı (mm)
- **wind_speed_10m**: Rüzgar hızı (m/s)
- **wind_direction_10m**: Rüzgar yönü (derece)
- **uv_index**: UV indeksi (0-11)
- **sunshine_duration**: Güneşlenme süresi (saat)

### 🏭 Hava Kalitesi Parametreleri:
- **pm10**: PM10 partikül madde (µg/m³)
- **pm2_5**: PM2.5 partikül madde (µg/m³)
- **nitrogen_dioxide**: Azot dioksit (µg/m³)
- **sulphur_dioxide**: Kükürt dioksit (µg/m³)
- **ozone**: Ozon (µg/m³)
- **carbon_monoxide**: Karbon monoksit (µg/m³)
- **methane**: Metan (ppb)

### 🌿 Polen Parametreleri:
- **pollen_code**: Polen türü (GRASS, TREE, WEED)
- **plant_code**: Bitki türü (GRAMINALES, OLIVE, RAGWEED, MUGWORT, BIRCH)
- **upi_value**: Universal Polen İndeksi (1-5)
- **plant_upi_value**: Bitki özel UPI değeri (1-5)
- **in_season**: Polen mevsiminde mi? (True/False)
- **plant_in_season**: Bitki mevsiminde mi? (True/False)

---

## 🎯 Risk Seviyeleri ve Öneriler

### 🟢 Düşük Risk (0.0 - Eşik)
- **Öneri**: "Harika! X saat güvenle dışarıda vakit geçirebilirsiniz."
- **Aktivite**: Normal açık hava aktiviteleri
- **Süre**: 6-8 saat

### 🟡 Orta Risk (Eşik - 1.5x Eşik)  
- **Öneri**: "X saat kadar dışarıda olabilirsiniz. Dikkatli olun."
- **Aktivite**: Kısa süreli aktiviteler
- **Süre**: 3-6 saat

### 🟠 Yüksek Risk (1.5x - 2x Eşik)
- **Öneri**: "Sadece X saat kısa süreli dışarı çıkış önerilir."
- **Aktivite**: Zorunlu çıkışlar
- **Süre**: 1-3 saat

### 🔴 Çok Yüksek Risk (>2x Eşik)
- **Öneri**: "Dışarı çıkma önerilmez. İç mekanda kalın."
- **Aktivite**: İç mekan aktiviteleri
- **Süre**: 0 saat

---

## ❓ Sık Sorulan Sorular

### Q: Hangi grupa dahil olduğumu nasıl anlarım?
**A**: Doktor teşhisinize göre:
- Tanılı şiddetli allerji → Grup 1
- Tanılı hafif/orta allerji → Grup 2  
- Aile geçmişi var, belirti yok → Grup 3
- Emin değilim → Grup 4
- Allerji yok ama hassasım → Grup 5

### Q: Tahminler ne kadar güvenilir?
**A**: Model doğruluğu %99+ (R² > 0.99), ancak bireysel farklılıklar olabilir.

### Q: Günlük kaç kez kontrol etmeliyim?
**A**: Sabah ve öğlen olmak üzere günde 2 kez kontrol önerilir.

### Q: Önerilerden farklı hissedersem ne yapmalıyım?
**A**: Kişisel deneyiminizi önceleyerek daha temkinli davranın.

### Q: Başka şehirler için kullanabilir miyim?
**A**: Evet, coğrafi koordinat (lat, lon) girişi ile kullanabilirsiniz.

---

## 🔧 Sorun Giderme

### Hata: "Model bulunamadı"
```bash
# Modeli yeniden eğitin
python allergy_predictor.py
```

### Hata: "Özellik uyumsuzluğu"
```python
# Gerekli tüm parametreleri kontrol edin
required_features = [
    'temperature_2m', 'relative_humidity_2m', 'precipitation',
    'wind_speed_10m', 'uv_index', 'pm10', 'pm2_5', 
    'upi_value', 'pollen_code', 'in_season', 'hour'
]
```

### Performans Optimizasyonu:
```python
# Model cache kullanın
predictor.save_models('cache/')
predictor.load_models('cache/')
```

---

## 📞 Destek ve İletişim

- **Dokümantasyon**: [GitHub Repository]
- **İssue Raporu**: [GitHub Issues]
- **E-posta**: support@allermind.com
- **Versiyon**: v1.0.0
- **Son Güncelleme**: 1 Eylül 2025

---

*🌟 AllerMind - Allerji Tahmin Sistemi ile sağlıklı günler!*
