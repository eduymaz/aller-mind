#!/usr/bin/env python3
"""
AllerMind Alerji Risk Tahmin Sistemi
====================================

Bu sistem, pkl modellerini kullanarak farklı şehir, grup ve tarihlere göre
alerji risk tahminleri yapar.

Kullanım:
    python allermind_predictor.py --grup 1 --sehir "Ankara" --tarih "2025-09-11"
    
Grup Bilgileri:
    1: Şiddetli Alerjik Grup
    2: Hafif-Orta Grup  
    3: Genetik Yatkınlığı Olan Grup
    4: Kaliteli Yaşam Tercih Eden Grup
    5: Hassas Grup (Çocuk/Yaşlı)
"""

import argparse
import pickle
import warnings
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os
import math
import random

warnings.filterwarnings('ignore')

class AllerMindPredictor:
       
    def __init__(self, models_dir="pkl_models"):
        
        self.models_dir = Path(models_dir)
        self.models = {}
        self.group_info = {
            1: {
                'name': 'Şiddetli Alerjik Grup',
                'description': 'Yoğun polen alerjisi, astım vb.',
                'risk_threshold': 30,
                'safe_threshold': 20
            },
            2: {
                'name': 'Hafif-Orta Grup',
                'description': 'Hafif alerjik reaksiyonlar',
                'risk_threshold': 40,
                'safe_threshold': 25
            },
            3: {
                'name': 'Genetik Yatkınlığı Olan Grup',
                'description': 'Aile geçmişi olan bireyler',
                'risk_threshold': 35,
                'safe_threshold': 22
            },
            4: {
                'name': 'Kaliteli Yaşam Tercih Eden Grup',
                'description': 'Konfor odaklı yaşam tarzı',
                'risk_threshold': 45,
                'safe_threshold': 30
            },
            5: {
                'name': 'Hassas Grup (Çocuk/Yaşlı)',
                'description': 'Yaşlılar ve çocuklar',
                'risk_threshold': 25,
                'safe_threshold': 15
            }
        }
        
        # Temel feature listesi (notebook'tan alınmıştır)
        self.feature_list = [
            'tree_pollen_index', 'grass_pollen_index', 'weed_pollen_index',
            'pm2_5', 'pm10', 'no2', 'ozone', 'so2', 'co',
            'temperature_2m', 'relative_humidity_2m', 'wind_speed_10m',
            'surface_pressure', 'uv_index', 'visibility', 
            'cloud_cover', 'dew_point_2m', 'precipitation'
        ]
        
        # Interaction features (notebook'tan)
        self.interaction_features = [
            'polen_weather_interaction',  # tree_pollen × humidity × wind_speed
            'pollution_pressure_interaction',  # pm2_5 × surface_pressure  
            'ozone_temp_interaction',  # ozone × temperature
            'complete_env_interaction'  # pm10 × humidity × wind_speed
        ]
        
        self.all_features = self.feature_list + self.interaction_features
        
        # Şehir koordinatları (Türkiye'nin başlıca şehirleri)
        self.city_coordinates = {
            'ankara': (39.9334, 32.8597),
            'istanbul': (41.0082, 28.9784),
            'izmir': (38.4237, 27.1428),
            'bursa': (40.1826, 29.0665),
            'antalya': (36.8969, 30.7133),
            'adana': (37.0000, 35.3213),
            'konya': (37.8667, 32.4833),
            'gaziantep': (37.0662, 37.3833),
            'kayseri': (38.7312, 35.4787),
            'mersin': (36.8000, 34.6333),
            'diyarbakir': (37.9144, 40.2306),
            'eskisehir': (39.7767, 30.5206),
            'samsun': (41.2928, 36.3313),
            'denizli': (37.7765, 29.0864),
            'malatya': (38.3552, 38.3095),
            'trabzon': (41.0015, 39.7178),
            'van': (38.4891, 43.4089),
            'erzurum': (39.9334, 41.2678),
            'batman': (37.8812, 41.1351),
            'elazig': (38.6810, 39.2264)
        }
    
    def load_models(self):
        """Tüm grup modellerini yükle"""
        print("🔄 Modeller yükleniyor...")
        
        for group_id in range(1, 6):
            try:
                # Önce .pkl formatını dene
                pkl_path = self.models_dir / f"Grup{group_id}_*.pkl"
                pkl_files = list(self.models_dir.glob(f"Grup{group_id}_*model.pkl"))
                
                if pkl_files:
                    model_path = pkl_files[0]
                    print(f"📦 Grup {group_id} modeli yükleniyor: {model_path.name}")
                    
                    with open(model_path, 'rb') as f:
                        model_package = pickle.load(f)
                    
                    self.models[group_id] = model_package
                    print(f"✅ Grup {group_id} başarıyla yüklendi")
                    
                else:
                    print(f"❌ Grup {group_id} için model dosyası bulunamadı")
                    
            except Exception as e:
                print(f"❌ Grup {group_id} model yükleme hatası: {e}")
        
        print(f"📊 Toplam {len(self.models)} model yüklendi")
    
    def get_city_coordinates(self, city_name):
        """Şehir koordinatlarını al"""
        city_lower = city_name.lower().replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
        
        if city_lower in self.city_coordinates:
            return self.city_coordinates[city_lower]
        else:
            # Ankara'yı varsayılan olarak döndür
            print(f"⚠️ '{city_name}' şehri bulunamadı, Ankara koordinatları kullanılıyor")
            return self.city_coordinates['ankara']
    
    def generate_environmental_data(self, city, date_str):
        """
        Şehir ve tarih için örnek çevresel veri üret
        (Gerçek bir API'den veri çekilebilir)
        """
        lat, lon = self.get_city_coordinates(city)
        
        # Tarih işleme
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        except:
            date_obj = datetime.now()
        
        # Mevsim faktörü
        month = date_obj.month
        season_factor = {
            'spring': 1.5 if month in [3, 4, 5] else 1.0,  # Polen yoğun
            'summer': 1.3 if month in [6, 7, 8] else 1.0,  # Sıcaklık yüksek
            'autumn': 1.1 if month in [9, 10, 11] else 1.0,
            'winter': 0.8 if month in [12, 1, 2] else 1.0   # Polen düşük
        }
        
        # Şehir faktörü (büyük şehirlerde kirlilik daha yüksek)
        big_cities = ['istanbul', 'ankara', 'izmir', 'bursa', 'antalya']
        city_factor = 1.4 if city.lower() in big_cities else 1.0
        
        # Basit normal dağılım simülasyonu
        def simple_normal(mean, std):
            """Basit normal dağılım simülasyonu"""
            return random.gauss(mean, std)
        
        # Örnek veri üretimi (gerçek değerler için API entegrasyonu gerekli)
        base_data = {
            'tree_pollen_index': simple_normal(25, 15) * season_factor.get('spring', 1.0),
            'grass_pollen_index': simple_normal(20, 10) * season_factor.get('spring', 1.0),
            'weed_pollen_index': simple_normal(15, 8) * season_factor.get('autumn', 1.0),
            'pm2_5': simple_normal(20, 8) * city_factor,
            'pm10': simple_normal(35, 12) * city_factor,
            'no2': simple_normal(30, 10) * city_factor,
            'ozone': simple_normal(80, 20) * season_factor.get('summer', 1.0),
            'so2': simple_normal(15, 5) * city_factor,
            'co': simple_normal(1.2, 0.4) * city_factor,
            'temperature_2m': simple_normal(20, 8) + (month - 6) * 3,  # Mevsimsel
            'relative_humidity_2m': simple_normal(60, 15),
            'wind_speed_10m': simple_normal(8, 3),
            'surface_pressure': simple_normal(1013, 10),
            'uv_index': max(0, simple_normal(5, 2) * season_factor.get('summer', 1.0)),
            'visibility': simple_normal(15, 5),
            'cloud_cover': simple_normal(40, 20),
            'dew_point_2m': simple_normal(10, 5),
            'precipitation': max(0, simple_normal(2, 3))
        }
        
        # Negatif değerleri düzelt
        for key in base_data:
            if base_data[key] < 0:
                base_data[key] = abs(base_data[key])
        
        return base_data
    
    def calculate_interaction_features(self, data):
        """Interaction features hesapla"""
        interactions = {}
        
        # Polen-meteoroloji etkileşimi
        interactions['polen_weather_interaction'] = (
            data['tree_pollen_index'] * data['relative_humidity_2m'] * data['wind_speed_10m'] / 1000
        )
        
        # Kirlilik-basınç etkileşimi
        interactions['pollution_pressure_interaction'] = (
            data['pm2_5'] * data['surface_pressure'] / 1000
        )
        
        # Ozon-sıcaklık etkileşimi  
        interactions['ozone_temp_interaction'] = (
            data['ozone'] * data['temperature_2m'] / 100
        )
        
        # Komple çevresel etkileşim
        interactions['complete_env_interaction'] = (
            data['pm10'] * data['relative_humidity_2m'] * data['wind_speed_10m'] / 10000
        )
        
        return interactions
    
    def predict_for_group(self, group_id, city, date_str, custom_data=None):
        """
        Belirli bir grup için tahmin yap
        
        Args:
            group_id (int): Grup numarası (1-5)
            city (str): Şehir adı
            date_str (str): Tarih (YYYY-MM-DD)
            custom_data (dict, optional): Özel çevresel veriler
        
        Returns:
            dict: Tahmin sonuçları
        """
        if group_id not in self.models:
            return {'error': f'Grup {group_id} modeli yüklenmemiş'}
        
        # Çevresel veri al
        if custom_data:
            env_data = custom_data
        else:
            env_data = self.generate_environmental_data(city, date_str)
        
        # Interaction features ekle
        interactions = self.calculate_interaction_features(env_data)
        env_data.update(interactions)
        
        # Model paketi al
        model_package = self.models[group_id]
        model = model_package['model']
        scaler = model_package.get('scaler')
        features = model_package.get('features', self.all_features)
        
        # Feature vektörü hazırla
        try:
            # Basit liste olarak hazırla (numpy yerine)
            X_list = [[env_data.get(feat, 0) for feat in features]]
            
            # Model predict için uygun format
            if hasattr(model, 'predict'):
                # Scaling uygula
                if scaler and hasattr(scaler, 'transform'):
                    try:
                        X_scaled = scaler.transform(X_list)
                    except:
                        X_scaled = X_list
                        print("⚠️ Scaler uygulanamadı, ham veri kullanılıyor")
                else:
                    X_scaled = X_list
            
            # Tahmin yap
            prediction = model.predict(X_scaled)[0]
            
            # Risk seviyesi belirle
            group_info = self.group_info[group_id]
            
            if prediction <= group_info['safe_threshold']:
                risk_level = "Düşük Risk"
                recommendation = "🟢 Outdoor aktiviteler güvenli"
            elif prediction <= group_info['risk_threshold']:
                risk_level = "Orta Risk"  
                recommendation = "🟡 Dikkatli outdoor aktivite"
            else:
                risk_level = "Yüksek Risk"
                recommendation = "🔴 Indoor kalmanız öneriliyor"
            
            # Güvenli saat tahmini
            safe_hours = max(0, min(24, 24 - (prediction / 4)))
            
            result = {
                'grup_id': group_id,
                'grup_adi': group_info['name'],
                'sehir': city,
                'tarih': date_str,
                'risk_skoru': round(prediction, 1),
                'risk_seviyesi': risk_level,
                'guvenli_saat_tahmini': round(safe_hours, 1),
                'oneri': recommendation,
                'cevresel_veriler': {k: round(v, 2) for k, v in env_data.items()},
                'model_info': {
                    'feature_count': len(features),
                    'model_type': str(type(model).__name__)
                }
            }
            
            return result
            
        except Exception as e:
            return {'error': f'Tahmin hatası: {str(e)}'}
    
    def predict_all_groups(self, city, date_str, custom_data=None):
        """Tüm gruplar için tahmin yap"""
        results = {}
        
        for group_id in range(1, 6):
            if group_id in self.models:
                results[group_id] = self.predict_for_group(group_id, city, date_str, custom_data)
        
        return results
    
    def print_prediction_report(self, results):
        """Tahmin raporunu yazdır"""
        if isinstance(results, dict) and 'error' in results:
            print(f"❌ Hata: {results['error']}")
            return
        
        if isinstance(results, dict) and 'grup_id' in results:
            # Tek grup sonucu
            self._print_single_result(results)
        else:
            # Çoklu grup sonuçları
            print(f"\n{'='*80}")
            print(f"🌿 ALLERMIND ALERJİ RİSK RAPORU")
            print(f"{'='*80}")
            print(f"📍 Şehir: {list(results.values())[0]['sehir']}")
            print(f"📅 Tarih: {list(results.values())[0]['tarih']}")
            print(f"\n🎯 GRUP BAZLI TAHMİNLER:")
            print(f"{'-'*60}")
            
            for group_id in sorted(results.keys()):
                result = results[group_id]
                if 'error' not in result:
                    print(f"\n{group_id}. {result['grup_adi']}")
                    print(f"   Risk Skoru: {result['risk_skoru']}")
                    print(f"   Risk Seviyesi: {result['risk_seviyesi']}")
                    print(f"   Güvenli Saat: {result['guvenli_saat_tahmini']} saat/gün")
                    print(f"   Öneri: {result['oneri']}")
    
    def _print_single_result(self, result):
        """Tek grup sonucunu yazdır"""
        print(f"\n{'='*60}")
        print(f"🌿 ALLERMIND TAHMİN RAPORU")
        print(f"{'='*60}")
        print(f"👥 Grup: {result['grup_adi']} (#{result['grup_id']})")
        print(f"📍 Şehir: {result['sehir']}")
        print(f"📅 Tarih: {result['tarih']}")
        print(f"\n📊 TAHMİN SONUÇLARI:")
        print(f"{'-'*30}")
        print(f"Risk Skoru: {result['risk_skoru']}/100")
        print(f"Risk Seviyesi: {result['risk_seviyesi']}")
        print(f"Güvenli Saat Tahmini: {result['guvenli_saat_tahmini']} saat/gün")
        print(f"Öneri: {result['oneri']}")
        
        print(f"\n🌡️ ÇEVRESEL KOŞULLAR:")
        print(f"{'-'*30}")
        env = result['cevresel_veriler']
        print(f"Polen (Ağaç/Çimen/Ot): {env['tree_pollen_index']:.1f}/{env['grass_pollen_index']:.1f}/{env['weed_pollen_index']:.1f}")
        print(f"Hava Kalitesi (PM2.5/PM10): {env['pm2_5']:.1f}/{env['pm10']:.1f}")
        print(f"Sıcaklık: {env['temperature_2m']:.1f}°C")
        print(f"Nem: {env['relative_humidity_2m']:.1f}%")
        print(f"Rüzgar: {env['wind_speed_10m']:.1f} km/h")

def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(
        description='AllerMind Alerji Risk Tahmin Sistemi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python allermind_predictor.py --grup 1 --sehir "Ankara" --tarih "2025-09-11"
  python allermind_predictor.py --sehir "Istanbul" --tarih "2025-09-12"  # Tüm gruplar
  python allermind_predictor.py --grup 5 --sehir "Izmir"                # Bugün
        """
    )
    
    parser.add_argument('--grup', type=int, choices=[1,2,3,4,5],
                        help='Grup numarası (1-5). Belirtilmezse tüm gruplar için tahmin yapılır')
    parser.add_argument('--sehir', required=True,
                        help='Şehir adı (örn: Ankara, Istanbul, Izmir)')  
    parser.add_argument('--tarih', default=datetime.now().strftime('%Y-%m-%d'),
                        help='Tahmin tarihi (YYYY-MM-DD). Varsayılan: bugün')
    parser.add_argument('--models-dir', default='pkl_models',
                        help='Model dosyalarının bulunduğu klasör')
    
    args = parser.parse_args()
    
    # Predictor başlat
    predictor = AllerMindPredictor(args.models_dir)
    
    # Modelleri yükle
    predictor.load_models()
    
    if len(predictor.models) == 0:
        print("❌ Hiç model yüklenemedi. Model dosyalarını kontrol edin.")
        sys.exit(1)
    
    # Tahmin yap
    if args.grup:
        # Tek grup için tahmin
        result = predictor.predict_for_group(args.grup, args.sehir, args.tarih)
        predictor.print_prediction_report(result)
    else:
        # Tüm gruplar için tahmin
        results = predictor.predict_all_groups(args.sehir, args.tarih)
        predictor.print_prediction_report(results)
    
    print(f"\n{'='*60}")
    print("✅ Tahmin tamamlandı!")

if __name__ == "__main__":
    main()
