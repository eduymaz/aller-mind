#!/usr/bin/env python3
"""
AllerMind Ultra Basit Tahmin Sistemi
====================================

Bu sistem sadece Python standart kütüphaneleri kullanarak
pkl modellerini test eder ve basit tahminler yapar.

Hiçbir dış kütüphane gerektirmez!
"""

import pickle
import random
import math
from datetime import datetime
from pathlib import Path

class UltraSimplePredictor:
    """En basit AllerMind tahmin sınıfı"""
    
    def __init__(self):
        self.models_dir = Path("pkl_models")
        
        # Grup bilgileri
        self.groups = {
            1: "Şiddetli Alerjik Grup",
            2: "Hafif-Orta Grup", 
            3: "Genetik Yatkınlığı Olan Grup",
            4: "Kaliteli Yaşam Tercih Eden Grup",
            5: "Hassas Grup (Çocuk/Yaşlı)"
        }
        
        # Şehirler
        self.cities = [
            "Ankara", "Istanbul", "Izmir", "Bursa", "Antalya", 
            "Adana", "Konya", "Gaziantep", "Kayseri", "Mersin"
        ]
    
    def list_models(self):
        """Model dosyalarını listele"""
        print("📦 MEVCUT MODEL DOSYALARI:")
        print("="*50)
        
        pkl_files = list(self.models_dir.glob("*.pkl"))
        
        if not pkl_files:
            print("❌ Hiç .pkl dosyası bulunamadı!")
            return []
        
        for i, pkl_file in enumerate(pkl_files, 1):
            try:
                file_size = pkl_file.stat().st_size / (1024 * 1024)
                print(f"{i:2d}. {pkl_file.name:<40} ({file_size:.1f} MB)")
            except:
                print(f"{i:2d}. {pkl_file.name}")
        
        return pkl_files
    
    def test_model_loading(self, model_path):
        """Modeli yüklemeyi test et"""
        try:
            print(f"\n🔄 Test ediliyor: {model_path.name}")
            
            with open(model_path, 'rb') as f:
                model_package = pickle.load(f)
            
            print("✅ Model başarıyla yüklendi!")
            
            # İçeriği incele
            print(f"\n📋 Model İçeriği:")
            for key, value in model_package.items():
                print(f"  📌 {key}: {type(value).__name__}")
                
                # Özel bilgiler
                if key == 'features' and hasattr(value, '__len__'):
                    print(f"     └─ {len(value)} özellik")
                elif key == 'model':
                    print(f"     └─ {type(value).__name__}")
            
            return model_package
            
        except Exception as e:
            print(f"❌ Yükleme hatası: {e}")
            return None
    
    def generate_fake_data(self, group_id, city_name):
        """Sahte çevresel veri üret"""
        # Grup faktörü (1=en hassas, 5=en az hassas)
        group_sensitivity = {1: 1.5, 2: 1.0, 3: 1.2, 4: 0.8, 5: 1.4}
        sensitivity = group_sensitivity.get(group_id, 1.0)
        
        # Şehir faktörü (büyük şehirlerde kirlilik yüksek)
        big_cities = ["Istanbul", "Ankara", "Izmir", "Bursa"]
        city_factor = 1.3 if city_name in big_cities else 1.0
        
        # Rastgele çevresel veriler
        data = {
            'tree_pollen_index': random.uniform(5, 80) * sensitivity,
            'grass_pollen_index': random.uniform(3, 60) * sensitivity,
            'weed_pollen_index': random.uniform(2, 40) * sensitivity,
            'pm2_5': random.uniform(8, 60) * city_factor,
            'pm10': random.uniform(15, 100) * city_factor,
            'no2': random.uniform(10, 70) * city_factor,
            'ozone': random.uniform(40, 160),
            'so2': random.uniform(2, 35) * city_factor,
            'co': random.uniform(0.5, 4.0) * city_factor,
            'temperature_2m': random.uniform(0, 40),
            'relative_humidity_2m': random.uniform(25, 90),
            'wind_speed_10m': random.uniform(1, 25),
            'surface_pressure': random.uniform(995, 1025),
            'uv_index': random.uniform(0, 11),
            'visibility': random.uniform(2, 30),
            'cloud_cover': random.uniform(0, 100),
            'dew_point_2m': random.uniform(-10, 30),
            'precipitation': random.uniform(0, 15)
        }
        
        # Basit interaction features
        data['polen_weather_interaction'] = (data['tree_pollen_index'] * 
                                           data['relative_humidity_2m'] * 
                                           data['wind_speed_10m']) / 1000
        
        data['pollution_pressure_interaction'] = (data['pm2_5'] * 
                                                data['surface_pressure']) / 1000
        
        data['ozone_temp_interaction'] = (data['ozone'] * 
                                        data['temperature_2m']) / 100
        
        data['complete_env_interaction'] = (data['pm10'] * 
                                          data['relative_humidity_2m'] * 
                                          data['wind_speed_10m']) / 10000
        
        return data
    
    def simple_risk_calculation(self, data, group_id):
        """Basit risk hesaplama (model olmadan)"""
        # Grup ağırlıkları
        weights = {
            1: {'polen': 3.0, 'pollution': 2.0, 'weather': 1.5},  # Polen hassas
            2: {'polen': 1.5, 'pollution': 3.5, 'weather': 1.8},  # Kirlilik hassas
            3: {'polen': 2.2, 'pollution': 2.2, 'weather': 2.0},  # Genel
            4: {'polen': 2.8, 'pollution': 3.0, 'weather': 2.2},  # Çoklu hassas
            5: {'polen': 1.2, 'pollution': 1.2, 'weather': 1.3}   # Düşük hassas
        }
        
        w = weights[group_id]
        
        # Bileşen skorları
        polen_score = (data['tree_pollen_index'] + 
                      data['grass_pollen_index'] + 
                      data['weed_pollen_index']) / 3
        
        pollution_score = (data['pm2_5'] + data['pm10'] + data['no2']) / 3
        
        weather_score = abs(data['temperature_2m'] - 22) + data['relative_humidity_2m']
        
        # Ağırlıklı toplam
        risk_score = (polen_score * w['polen'] + 
                     pollution_score * w['pollution'] + 
                     weather_score * w['weather']) / 10
        
        return min(100, max(0, risk_score))
    
    def evaluate_risk(self, risk_score, group_id):
        """Risk seviyesini değerlendir"""
        thresholds = {1: 25, 2: 35, 3: 30, 4: 40, 5: 20}
        threshold = thresholds[group_id]
        
        if risk_score <= threshold * 0.7:
            return "Düşük Risk 🟢", "Outdoor aktiviteler güvenli"
        elif risk_score <= threshold:
            return "Orta Risk 🟡", "Dikkatli outdoor aktivite"
        else:
            return "Yüksek Risk 🔴", "Indoor kalmanız önerilir"
    
    def interactive_demo(self):
        """İnteraktif demo"""
        print(f"\n{'='*60}")
        print("🌿 ALLERMIND ULTRA BASİT DEMO SİSTEMİ")
        print(f"{'='*60}")
        print("Bu sistem pkl modellerini test eder ve basit hesaplamalar yapar.")
        
        # Modelleri listele
        pkl_files = self.list_models()
        
        if pkl_files:
            print(f"\n🧪 İlk modeli test edelim:")
            first_model = pkl_files[0]
            model_package = self.test_model_loading(first_model)
            
            if model_package:
                print(f"🎉 Model başarıyla analiz edildi!")
        
        # Grup seçimi
        print(f"\n👥 GRUP SEÇİMİ:")
        for gid, gname in self.groups.items():
            print(f"{gid}. {gname}")
        
        while True:
            try:
                group_id = input("Grup seçin (1-5): ").strip()
                if group_id.isdigit() and 1 <= int(group_id) <= 5:
                    group_id = int(group_id)
                    break
                else:
                    print("❌ Lütfen 1-5 arası bir sayı girin!")
            except:
                print("❌ Geçersiz giriş!")
        
        # Şehir seçimi
        print(f"\n🏙️ ŞEHİR SEÇİMİ:")
        for i, city in enumerate(self.cities[:5], 1):
            print(f"{i}. {city}")
        
        city_name = input("Şehir adı girin (veya Enter=Ankara): ").strip()
        if not city_name:
            city_name = "Ankara"
        
        # Hesaplama
        print(f"\n🔄 Hesaplama yapılıyor...")
        
        data = self.generate_fake_data(group_id, city_name)
        risk_score = self.simple_risk_calculation(data, group_id)
        risk_level, recommendation = self.evaluate_risk(risk_score, group_id)
        
        safe_hours = max(0, 24 - (risk_score / 4))
        
        # Sonuçları göster
        print(f"\n{'='*50}")
        print(f"📊 TAHMİN RAPORU")
        print(f"{'='*50}")
        print(f"👥 Grup: {self.groups[group_id]}")
        print(f"📍 Şehir: {city_name}")
        print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        print(f"\n🎯 SONUÇLAR:")
        print(f"   Risk Skoru: {risk_score:.1f}/100")
        print(f"   Risk Seviyesi: {risk_level}")
        print(f"   Güvenli Saat: {safe_hours:.1f} saat/gün")
        print(f"   Öneri: {recommendation}")
        
        print(f"\n🌡️ ÇEVRESEL KOŞULLAR (Simülasyon):")
        print(f"   🌸 Polen (Ağaç): {data['tree_pollen_index']:.1f}")
        print(f"   🌾 Polen (Çimen): {data['grass_pollen_index']:.1f}")
        print(f"   💨 PM2.5: {data['pm2_5']:.1f} μg/m³")
        print(f"   🌡️ Sıcaklık: {data['temperature_2m']:.1f}°C")
        print(f"   💧 Nem: {data['relative_humidity_2m']:.0f}%")
        print(f"   🌬️ Rüzgar: {data['wind_speed_10m']:.1f} km/h")
        
        # Tekrar
        print(f"\n{'='*50}")
        again = input("Başka bir tahmin yapmak ister misiniz? (e/h): ")
        if again.lower() in ['e', 'evet', 'y', 'yes']:
            self.interactive_demo()

def main():
    """Ana fonksiyon"""
    print("🌿 AllerMind Ultra Basit Test Sistemi")
    print("="*50)
    print("Python standart kütüphaneleri ile çalışır!")
    
    # Dizin kontrolü
    if not Path("pkl_models").exists():
        print("❌ 'pkl_models' klasörü bulunamadı!")
        print("Lütfen bu scripti MODEL klasörü içinde çalıştırın.")
        return
    
    predictor = UltraSimplePredictor()
    predictor.interactive_demo()
    
    print(f"\n👋 Demo tamamlandı!")

if __name__ == "__main__":
    main()
