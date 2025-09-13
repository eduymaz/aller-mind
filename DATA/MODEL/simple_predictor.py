#!/usr/bin/env python3
"""
AllerMind Basit Alerji Risk Tahmin Sistemi
==========================================

Bu sistem, pkl modellerini kullanarak farklı şehir, grup ve tarihlere göre
alerji risk tahminleri yapar. (Sadece pickle modülü kullanır)

Kullanım:
    python simple_predictor.py
    
Grup Bilgileri:
    1: Şiddetli Alerjik Grup
    2: Hafif-Orta Grup  
    3: Genetik Yatkınlığı Olan Grup
    4: Kaliteli Yaşam Tercih Eden Grup
    5: Hassas Grup (Çocuk/Yaşlı)
"""

import pickle
import numpy as np
from datetime import datetime
from pathlib import Path
import os

class SimpleAllerMindPredictor:
    """Basit AllerMind tahmin sınıfı"""
    
    def __init__(self, models_dir="pkl_models"):
        self.models_dir = Path(models_dir)
        self.models = {}
        
        # Grup bilgileri
        self.group_info = {
            1: {'name': 'Şiddetli Alerjik Grup', 'threshold': 30},
            2: {'name': 'Hafif-Orta Grup', 'threshold': 40},
            3: {'name': 'Genetik Yatkınlığı Olan Grup', 'threshold': 35},
            4: {'name': 'Kaliteli Yaşam Tercih Eden Grup', 'threshold': 45},
            5: {'name': 'Hassas Grup (Çocuk/Yaşlı)', 'threshold': 25}
        }
        
        # Şehir koordinatları
        self.cities = {
            'ankara': (39.9334, 32.8597),
            'istanbul': (41.0082, 28.9784),
            'izmir': (38.4237, 27.1428),
            'bursa': (40.1826, 29.0665),
            'antalya': (36.8969, 30.7133),
            'adana': (37.0000, 35.3213),
            'konya': (37.8667, 32.4833)
        }
    
    def list_available_models(self):
        """Mevcut modelleri listele"""
        print("📦 Mevcut Model Dosyaları:")
        print("-" * 40)
        
        pkl_files = list(self.models_dir.glob("*.pkl"))
        
        if not pkl_files:
            print("❌ Hiç .pkl model dosyası bulunamadı!")
            return False
        
        for i, pkl_file in enumerate(pkl_files, 1):
            file_size = pkl_file.stat().st_size / (1024 * 1024)  # MB
            print(f"{i}. {pkl_file.name} ({file_size:.1f} MB)")
        
        return True
    
    def load_single_model(self, model_path):
        """Tek bir model yükle ve test et"""
        try:
            print(f"\n🔄 Model yükleniyor: {model_path.name}")
            
            with open(model_path, 'rb') as f:
                model_package = pickle.load(f)
            
            print("✅ Model başarıyla yüklendi!")
            
            # Model içeriğini incele
            print(f"\n📋 Model İçeriği:")
            for key in model_package.keys():
                value = model_package[key]
                print(f"  {key}: {type(value).__name__}")
            
            # Features varsa göster
            if 'features' in model_package:
                features = model_package['features']
                print(f"\n🎯 Özellik Sayısı: {len(features)}")
                print(f"📝 İlk 5 Özellik: {features[:5]}")
            
            return model_package
            
        except Exception as e:
            print(f"❌ Model yükleme hatası: {str(e)}")
            return None
    
    def generate_sample_data(self, city_name, group_id):
        """Örnek veri üret"""
        # Şehir faktörü
        city_lower = city_name.lower()
        big_cities = ['istanbul', 'ankara', 'izmir']
        city_factor = 1.3 if city_lower in big_cities else 1.0
        
        # Grup faktörü
        group_factor = {1: 1.5, 2: 1.0, 3: 1.2, 4: 0.8, 5: 1.4}.get(group_id, 1.0)
        
        # Temel çevresel veriler (örnek)
        base_data = {
            'tree_pollen_index': np.random.uniform(10, 80) * group_factor,
            'grass_pollen_index': np.random.uniform(5, 60) * group_factor,
            'weed_pollen_index': np.random.uniform(3, 40) * group_factor,
            'pm2_5': np.random.uniform(5, 50) * city_factor,
            'pm10': np.random.uniform(10, 80) * city_factor,
            'no2': np.random.uniform(10, 60) * city_factor,
            'ozone': np.random.uniform(50, 150),
            'so2': np.random.uniform(5, 30) * city_factor,
            'co': np.random.uniform(0.5, 3.0) * city_factor,
            'temperature_2m': np.random.uniform(5, 35),
            'relative_humidity_2m': np.random.uniform(30, 90),
            'wind_speed_10m': np.random.uniform(2, 20),
            'surface_pressure': np.random.uniform(1000, 1020),
            'uv_index': np.random.uniform(1, 10),
            'visibility': np.random.uniform(5, 25),
            'cloud_cover': np.random.uniform(0, 100),
            'dew_point_2m': np.random.uniform(-5, 25),
            'precipitation': np.random.uniform(0, 10)
        }
        
        # Interaction features hesapla
        base_data.update({
            'polen_weather_interaction': (base_data['tree_pollen_index'] * 
                                        base_data['relative_humidity_2m'] * 
                                        base_data['wind_speed_10m']) / 1000,
            'pollution_pressure_interaction': (base_data['pm2_5'] * 
                                             base_data['surface_pressure']) / 1000,
            'ozone_temp_interaction': (base_data['ozone'] * 
                                     base_data['temperature_2m']) / 100,
            'complete_env_interaction': (base_data['pm10'] * 
                                       base_data['relative_humidity_2m'] * 
                                       base_data['wind_speed_10m']) / 10000
        })
        
        return base_data
    
    def make_prediction(self, model_package, sample_data, group_id):
        """Tahmin yap"""
        try:
            model = model_package['model']
            scaler = model_package.get('scaler')
            features = model_package.get('features', list(sample_data.keys()))
            
            # Veri hazırla
            X = np.array([[sample_data.get(feat, 0) for feat in features]])
            
            # Scaling varsa uygula
            if scaler is not None:
                try:
                    X_scaled = scaler.transform(X)
                except:
                    X_scaled = X
                    print("⚠️ Scaler uygulanamadı, ham veri kullanılıyor")
            else:
                X_scaled = X
            
            # Tahmin
            prediction = model.predict(X_scaled)[0]
            
            # Risk değerlendirme
            threshold = self.group_info[group_id]['threshold']
            
            if prediction <= threshold * 0.7:
                risk_level = "Düşük Risk 🟢"
                recommendation = "Outdoor aktiviteler güvenli"
            elif prediction <= threshold:
                risk_level = "Orta Risk 🟡"
                recommendation = "Dikkatli outdoor aktivite"
            else:
                risk_level = "Yüksek Risk 🔴"
                recommendation = "Indoor kalmanız önerilir"
            
            # Güvenli saat tahmini
            safe_hours = max(0, min(24, 24 - (prediction / 4)))
            
            return {
                'risk_score': round(prediction, 1),
                'risk_level': risk_level,
                'safe_hours': round(safe_hours, 1),
                'recommendation': recommendation,
                'success': True
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def interactive_prediction(self):
        """İnteraktif tahmin sistemi"""
        print(f"\n{'='*60}")
        print("🌿 ALLERMIND İNTERAKTİF TAHMİN SİSTEMİ")
        print(f"{'='*60}")
        
        # Modelleri listele
        if not self.list_available_models():
            return
        
        # Model seç
        pkl_files = list(self.models_dir.glob("*.pkl"))
        
        while True:
            try:
                choice = input(f"\nModel numarası seçin (1-{len(pkl_files)}) veya 'q' çıkış: ")
                if choice.lower() == 'q':
                    return
                
                model_index = int(choice) - 1
                if 0 <= model_index < len(pkl_files):
                    selected_model = pkl_files[model_index]
                    break
                else:
                    print("❌ Geçersiz numara!")
            except ValueError:
                print("❌ Lütfen geçerli bir sayı girin!")
        
        # Modeli yükle
        model_package = self.load_single_model(selected_model)
        if not model_package:
            return
        
        # Grup seç
        print(f"\n👥 Grup Seçimi:")
        for gid, ginfo in self.group_info.items():
            print(f"{gid}. {ginfo['name']}")
        
        while True:
            try:
                group_id = int(input("Grup numarası (1-5): "))
                if 1 <= group_id <= 5:
                    break
                else:
                    print("❌ Grup numarası 1-5 arası olmalı!")
            except ValueError:
                print("❌ Lütfen geçerli bir sayı girin!")
        
        # Şehir seç
        print(f"\n🏙️ Mevcut Şehirler: {', '.join(self.cities.keys()).title()}")
        city_name = input("Şehir adı girin: ").strip()
        
        if not city_name:
            city_name = "Ankara"
            print(f"Varsayılan şehir kullanılıyor: {city_name}")
        
        # Veri üret ve tahmin yap
        print(f"\n🔄 Tahmin hesaplanıyor...")
        sample_data = self.generate_sample_data(city_name, group_id)
        result = self.make_prediction(model_package, sample_data, group_id)
        
        # Sonuçları göster
        if result['success']:
            print(f"\n{'='*50}")
            print(f"📊 TAHMİN SONUÇLARI")
            print(f"{'='*50}")
            print(f"👥 Grup: {self.group_info[group_id]['name']}")
            print(f"📍 Şehir: {city_name.title()}")
            print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d')}")
            print(f"\n🎯 Risk Skoru: {result['risk_score']}/100")
            print(f"📊 Risk Seviyesi: {result['risk_level']}")
            print(f"⏰ Güvenli Saat Tahmini: {result['safe_hours']} saat/gün")
            print(f"💡 Öneri: {result['recommendation']}")
            
            # Çevresel koşullar özeti
            print(f"\n🌡️ Günün Çevresel Koşulları (Örnek):")
            print(f"   Polen (Ağaç/Çimen): {sample_data['tree_pollen_index']:.0f}/{sample_data['grass_pollen_index']:.0f}")
            print(f"   Hava Kalitesi (PM2.5): {sample_data['pm2_5']:.1f} μg/m³")
            print(f"   Sıcaklık: {sample_data['temperature_2m']:.1f}°C")
            print(f"   Nem: {sample_data['relative_humidity_2m']:.0f}%")
            
        else:
            print(f"❌ Tahmin hatası: {result['error']}")
        
        # Tekrar soru
        again = input(f"\nBaşka tahmin yapmak ister misiniz? (e/h): ")
        if again.lower() in ['e', 'evet', 'y', 'yes']:
            self.interactive_prediction()

def main():
    """Ana fonksiyon"""
    print("🌿 AllerMind Basit Tahmin Sistemi")
    print("="*40)
    
    # Çalışma dizinini kontrol et
    models_dir = Path("pkl_models")
    if not models_dir.exists():
        print(f"❌ '{models_dir}' klasörü bulunamadı!")
        print("Lütfen script'i MODEL klasörü içinde çalıştırın.")
        return
    
    # Predictor başlat
    predictor = SimpleAllerMindPredictor()
    predictor.interactive_prediction()
    
    print(f"\n{'='*40}")
    print("👋 Görüşürüz!")

if __name__ == "__main__":
    main()
