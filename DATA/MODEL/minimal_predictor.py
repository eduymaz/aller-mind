#!/usr/bin/env python3
"""
AllerMind Minimal Tahmin Sistemi
===============================

Bu sistem hiçbir dış kütüphane kullanmadan, pkl modellerini analiz eder
ve basit risk hesaplamaları yapar.

Kullanım: python minimal_predictor.py
"""

import pickle
import random
import math
from datetime import datetime
from pathlib import Path

class MinimalAllerMindPredictor:
    """Minimal AllerMind tahmin sistemi"""
    
    def __init__(self):
        self.models_dir = Path("pkl_models")
        
        # Grup bilgileri
        self.groups = {
            1: {
                'name': 'Şiddetli Alerjik Grup',
                'description': 'Yoğun polen alerjisi, astım',
                'risk_threshold': 30,
                'polen_weight': 3.5,
                'pollution_weight': 2.0,
                'weather_weight': 1.8
            },
            2: {
                'name': 'Hafif-Orta Grup',
                'description': 'Hafif alerjik reaksiyonlar',
                'risk_threshold': 40,
                'polen_weight': 1.6,
                'pollution_weight': 3.5,
                'weather_weight': 1.8
            },
            3: {
                'name': 'Genetik Yatkınlığı Olan Grup',
                'description': 'Aile geçmişi olan bireyler',
                'risk_threshold': 35,
                'polen_weight': 2.2,
                'pollution_weight': 2.2,
                'weather_weight': 2.0
            },
            4: {
                'name': 'Kaliteli Yaşam Tercih Eden Grup',
                'description': 'Konfor odaklı yaşam',
                'risk_threshold': 45,
                'polen_weight': 2.8,
                'pollution_weight': 3.0,
                'weather_weight': 2.2
            },
            5: {
                'name': 'Hassas Grup (Çocuk/Yaşlı)',
                'description': 'Yaşlılar ve çocuklar',
                'risk_threshold': 25,
                'polen_weight': 1.4,
                'pollution_weight': 1.2,
                'weather_weight': 1.4
            }
        }
        
        # Şehir koordinatları
        self.cities = {
            'ankara': (39.9334, 32.8597, 1.2),  # lat, lon, city_factor
            'istanbul': (41.0082, 28.9784, 1.5),
            'izmir': (38.4237, 27.1428, 1.3),
            'bursa': (40.1826, 29.0665, 1.2),
            'antalya': (36.8969, 30.7133, 1.1),
            'adana': (37.0000, 35.3213, 1.3),
            'konya': (37.8667, 32.4833, 1.0),
            'gaziantep': (37.0662, 37.3833, 1.2),
            'kayseri': (38.7312, 35.4787, 1.1),
            'mersin': (36.8000, 34.6333, 1.2)
        }
    
    def analyze_models(self):
        """Model dosyalarını analiz et"""
        print("🔍 MODEL DOSYALARI ANALİZİ")
        print("="*50)
        
        pkl_files = list(self.models_dir.glob("*.pkl"))
        
        if not pkl_files:
            print("❌ Hiç .pkl dosyası bulunamadı!")
            return False
        
        print(f"📦 Bulunan {len(pkl_files)} model dosyası:")
        
        successful_loads = 0
        
        for i, pkl_file in enumerate(pkl_files, 1):
            try:
                file_size = pkl_file.stat().st_size / (1024 * 1024)
                print(f"\n{i:2d}. {pkl_file.name}")
                print(f"    📏 Boyut: {file_size:.1f} MB")
                
                # Modeli yüklemeyi dene
                with open(pkl_file, 'rb') as f:
                    model_package = pickle.load(f)
                
                print(f"    ✅ Başarıyla yüklendi")
                print(f"    📋 İçerik:")
                
                for key, value in model_package.items():
                    print(f"       📌 {key}: {type(value).__name__}")
                    
                    if key == 'features' and hasattr(value, '__len__'):
                        print(f"          └─ {len(value)} özellik")
                    elif key == 'model':
                        model_type = str(type(value)).split('.')[-1].replace("'>", "")
                        print(f"          └─ {model_type}")
                
                successful_loads += 1
                
            except Exception as e:
                print(f"    ❌ Yükleme hatası: {str(e)[:50]}...")
        
        print(f"\n📊 ÖZET: {successful_loads}/{len(pkl_files)} model başarıyla analiz edildi")
        return successful_loads > 0
    
    def get_city_info(self, city_name):
        """Şehir bilgisini al"""
        city_key = city_name.lower()
        
        # Türkçe karakter temizliği
        replacements = {'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c'}
        for tr_char, en_char in replacements.items():
            city_key = city_key.replace(tr_char, en_char)
        
        if city_key in self.cities:
            return self.cities[city_key]
        else:
            # Varsayılan: Ankara
            print(f"⚠️ '{city_name}' bulunamadı, Ankara kullanılıyor")
            return self.cities['ankara']
    
    def generate_environmental_data(self, city_name, date_str):
        """Çevresel veri simüle et"""
        lat, lon, city_factor = self.get_city_info(city_name)
        
        # Tarih işleme
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            month = date_obj.month
        except:
            month = datetime.now().month
        
        # Mevsimsel faktörler
        season_factors = {
            'polen_spring': 1.8 if month in [3, 4, 5] else 1.0,
            'summer_heat': 1.3 if month in [6, 7, 8] else 1.0,
            'autumn_mild': 1.1 if month in [9, 10, 11] else 1.0,
            'winter_low': 0.6 if month in [12, 1, 2] else 1.0
        }
        
        # Rastgele çevresel veriler üret
        data = {
            # Polen verileri
            'tree_pollen': random.uniform(5, 80) * season_factors['polen_spring'],
            'grass_pollen': random.uniform(3, 60) * season_factors['polen_spring'],
            'weed_pollen': random.uniform(2, 40) * season_factors['autumn_mild'],
            
            # Hava kalitesi
            'pm25': random.uniform(8, 60) * city_factor,
            'pm10': random.uniform(15, 100) * city_factor,
            'no2': random.uniform(10, 70) * city_factor,
            'ozone': random.uniform(40, 160) * season_factors['summer_heat'],
            'so2': random.uniform(2, 35) * city_factor,
            'co': random.uniform(0.5, 4.0) * city_factor,
            
            # Meteoroloji
            'temperature': random.uniform(0, 40) + (month - 6) * 2,
            'humidity': random.uniform(25, 90),
            'wind_speed': random.uniform(1, 25),
            'pressure': random.uniform(995, 1025),
            'uv_index': max(0, random.uniform(0, 11) * season_factors['summer_heat']),
            'visibility': random.uniform(2, 30),
            'cloud_cover': random.uniform(0, 100),
            'precipitation': max(0, random.uniform(0, 15))
        }
        
        return data
    
    def calculate_risk_score(self, env_data, group_id):
        """Grup özelinde risk skoru hesapla"""
        group = self.groups[group_id]
        
        # Polen bileşeni
        polen_score = (
            env_data['tree_pollen'] * 1.2 +
            env_data['grass_pollen'] * 1.0 +
            env_data['weed_pollen'] * 0.8
        ) / 3
        
        # Kirlilik bileşeni
        pollution_score = (
            env_data['pm25'] * 1.5 +
            env_data['pm10'] * 1.2 +
            env_data['no2'] * 1.3 +
            env_data['ozone'] / 2 +
            env_data['so2'] * 1.1 +
            env_data['co'] * 20
        ) / 6
        
        # Hava durumu bileşeni
        temp_comfort = abs(env_data['temperature'] - 22)  # 22°C ideal
        humidity_discomfort = abs(env_data['humidity'] - 55)  # 55% ideal
        
        weather_score = (
            temp_comfort * 2 +
            humidity_discomfort / 2 +
            env_data['wind_speed'] / 3 +
            (100 - env_data['visibility']) +
            env_data['precipitation'] * 3
        ) / 5
        
        # Grup ağırlıklı toplam
        total_score = (
            polen_score * group['polen_weight'] +
            pollution_score * group['pollution_weight'] +
            weather_score * group['weather_weight']
        ) / (group['polen_weight'] + group['pollution_weight'] + group['weather_weight'])
        
        # 0-100 arası normalize et
        risk_score = min(100, max(0, total_score))
        
        return risk_score
    
    def evaluate_risk_level(self, risk_score, group_id):
        """Risk seviyesini değerlendir"""
        threshold = self.groups[group_id]['risk_threshold']
        
        if risk_score <= threshold * 0.6:
            return "Düşük Risk 🟢", "Outdoor aktiviteler güvenli", "green"
        elif risk_score <= threshold * 0.8:
            return "Düşük-Orta Risk 🟡", "Kısa süreli outdoor aktivite", "yellow"
        elif risk_score <= threshold:
            return "Orta Risk 🟠", "Dikkatli outdoor aktivite", "orange"
        elif risk_score <= threshold * 1.2:
            return "Yüksek Risk 🔴", "Indoor kalmanız önerilir", "red"
        else:
            return "Çok Yüksek Risk 🚨", "Kesinlikle indoor kalın", "darkred"
    
    def calculate_safe_hours(self, risk_score):
        """Güvenli outdoor saat hesapla"""
        if risk_score <= 20:
            return 24
        elif risk_score <= 40:
            return 18
        elif risk_score <= 60:
            return 12
        elif risk_score <= 80:
            return 6
        else:
            return 2
    
    def predict_for_group(self, group_id, city_name, date_str):
        """Grup için tahmin yap"""
        if group_id not in self.groups:
            return {'error': f'Geçersiz grup ID: {group_id}'}
        
        # Çevresel veri üret
        env_data = self.generate_environmental_data(city_name, date_str)
        
        # Risk hesapla
        risk_score = self.calculate_risk_score(env_data, group_id)
        
        # Risk seviyesi
        risk_level, recommendation, color = self.evaluate_risk_level(risk_score, group_id)
        
        # Güvenli saatler
        safe_hours = self.calculate_safe_hours(risk_score)
        
        return {
            'group_id': group_id,
            'group_name': self.groups[group_id]['name'],
            'city': city_name,
            'date': date_str,
            'risk_score': round(risk_score, 1),
            'risk_level': risk_level,
            'recommendation': recommendation,
            'safe_hours': safe_hours,
            'color': color,
            'env_data': {k: round(v, 1) for k, v in env_data.items()}
        }
    
    def predict_all_groups(self, city_name, date_str):
        """Tüm gruplar için tahmin"""
        results = {}
        
        for group_id in range(1, 6):
            results[group_id] = self.predict_for_group(group_id, city_name, date_str)
        
        return results
    
    def print_report(self, results):
        """Rapor yazdır"""
        if isinstance(results, dict) and 'group_id' in results:
            # Tek grup
            self._print_single_result(results)
        else:
            # Çoklu grup
            self._print_multi_results(results)
    
    def _print_single_result(self, result):
        """Tek grup raporu"""
        print(f"\n{'='*60}")
        print(f"🌿 ALLERMIND ALERJİ RİSK RAPORU")
        print(f"{'='*60}")
        print(f"👥 Grup: {result['group_name']} (#{result['group_id']})")
        print(f"📍 Şehir: {result['city'].title()}")
        print(f"📅 Tarih: {result['date']}")
        print(f"⏰ Analiz Zamanı: {datetime.now().strftime('%H:%M:%S')}")
        
        print(f"\n🎯 TAHMİN SONUÇLARI:")
        print(f"{'-'*30}")
        print(f"Risk Skoru: {result['risk_score']}/100")
        print(f"Risk Seviyesi: {result['risk_level']}")
        print(f"Güvenli Outdoor Saat: {result['safe_hours']} saat/gün")
        print(f"Öneri: {result['recommendation']}")
        
        print(f"\n🌡️ ÇEVRESEL KOŞULLAR (Simülasyon):")
        print(f"{'-'*40}")
        env = result['env_data']
        print(f"🌸 Polen - Ağaç: {env['tree_pollen']} grains/m³")
        print(f"🌾 Polen - Çimen: {env['grass_pollen']} grains/m³")
        print(f"🌿 Polen - Ot: {env['weed_pollen']} grains/m³")
        print(f"💨 PM2.5: {env['pm25']} μg/m³")
        print(f"💨 PM10: {env['pm10']} μg/m³")
        print(f"🌡️ Sıcaklık: {env['temperature']}°C")
        print(f"💧 Nem: {env['humidity']}%")
        print(f"🌬️ Rüzgar: {env['wind_speed']} km/h")
        print(f"☀️ UV İndeks: {env['uv_index']}")
    
    def _print_multi_results(self, results):
        """Çoklu grup raporu"""
        first_result = list(results.values())[0]
        
        print(f"\n{'='*70}")
        print(f"🌿 ALLERMIND - TÜM GRUPLAR RİSK RAPORU")
        print(f"{'='*70}")
        print(f"📍 Şehir: {first_result['city'].title()}")
        print(f"📅 Tarih: {first_result['date']}")
        print(f"⏰ Analiz: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n📊 GRUP BAZLI SONUÇLAR:")
        print(f"{'-'*70}")
        
        for group_id in sorted(results.keys()):
            result = results[group_id]
            if 'error' not in result:
                print(f"\n{group_id}. {result['group_name']}")
                print(f"   Risk: {result['risk_score']}/100 | {result['risk_level']}")
                print(f"   Güvenli: {result['safe_hours']}h | {result['recommendation']}")
        
        # En güvenli ve en riskli grupları bul
        safe_groups = []
        risky_groups = []
        
        for group_id, result in results.items():
            if 'error' not in result:
                if result['risk_score'] <= 30:
                    safe_groups.append(f"Grup {group_id}")
                elif result['risk_score'] >= 60:
                    risky_groups.append(f"Grup {group_id}")
        
        if safe_groups or risky_groups:
            print(f"\n💡 HIZLI ÖZET:")
            print(f"{'-'*30}")
            if safe_groups:
                print(f"🟢 Güvenli Gruplar: {', '.join(safe_groups)}")
            if risky_groups:
                print(f"🔴 Riskli Gruplar: {', '.join(risky_groups)}")
    
    def interactive_prediction(self):
        """İnteraktif tahmin"""
        print(f"\n{'='*60}")
        print("🌿 ALLERMIND MİNİMAL TAHMİN SİSTEMİ")
        print(f"{'='*60}")
        print("Bu sistem hiçbir dış kütüphane kullanmadan çalışır!")
        
        # Model analizi
        print(f"\n🔍 Model dosyaları kontrol ediliyor...")
        self.analyze_models()
        
        while True:
            # Grup seçimi
            print(f"\n👥 GRUP SEÇİMİ:")
            for gid, ginfo in self.groups.items():
                print(f"{gid}. {ginfo['name']}")
            print("0. Tüm gruplar")
            
            try:
                choice = input("Grup seçin (0-5): ").strip()
                if choice == '0':
                    selected_group = None
                elif choice in ['1', '2', '3', '4', '5']:
                    selected_group = int(choice)
                else:
                    print("❌ Geçersiz seçim!")
                    continue
            except:
                print("❌ Geçersiz giriş!")
                continue
            
            # Şehir seçimi
            print(f"\n🏙️ ŞEHİR SEÇİMİ:")
            city_list = list(self.cities.keys())
            for i, city in enumerate(city_list[:5], 1):
                print(f"{i}. {city.title()}")
            
            city_input = input("Şehir adı girin (veya Enter=Ankara): ").strip()
            city_name = city_input if city_input else "Ankara"
            
            # Tarih
            date_str = input("Tarih (YYYY-MM-DD) veya Enter=bugün: ").strip()
            if not date_str:
                date_str = datetime.now().strftime('%Y-%m-%d')
            
            # Tahmin yap
            print(f"\n🔄 Hesaplama yapılıyor...")
            
            if selected_group:
                result = self.predict_for_group(selected_group, city_name, date_str)
                self.print_report(result)
            else:
                results = self.predict_all_groups(city_name, date_str)
                self.print_report(results)
            
            # Devam
            print(f"\n{'='*60}")
            again = input("Başka bir tahmin yapmak ister misiniz? (e/h): ")
            if again.lower() not in ['e', 'evet', 'y', 'yes']:
                break
        
        print(f"\n👋 AllerMind Minimal Predictor'ı kullandığınız için teşekkürler!")

def main():
    """Ana fonksiyon"""
    print("🌿 AllerMind Minimal Tahmin Sistemi")
    print("="*50)
    print("✅ Hiçbir dış kütüphane gerektirmez!")
    print("📦 Model dosyalarını analiz eder")
    print("🧮 Basit risk hesaplamaları yapar")
    
    # Dizin kontrolü
    models_dir = Path("pkl_models")
    if not models_dir.exists():
        print(f"\n❌ '{models_dir}' klasörü bulunamadı!")
        print("Lütfen bu scripti MODEL klasörü içinde çalıştırın.")
        return
    
    predictor = MinimalAllerMindPredictor()
    predictor.interactive_prediction()

if __name__ == "__main__":
    main()
