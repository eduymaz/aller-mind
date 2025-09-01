import pandas as pd
import numpy as np
import pickle
import json
import sys
import os
from typing import Dict, Any, List

# Mevcut dizini Python path'ine ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from allergy_predictor import AllergyGroupPredictor

class AllergyPredictionDemo:
    """
    Allerji tahmin sistemi demo ve test sınıfı
    """
    
    def __init__(self, model_path: str = '/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/models'):
        self.model_path = model_path
        self.predictor = AllergyGroupPredictor()
        self.load_trained_models()
    
    def load_trained_models(self):
        """Eğitilmiş modelleri yükle"""
        print("📂 Eğitilmiş modeller yükleniyor...")
        
        # Grup ağırlıklarını yükle
        with open(f"{self.model_path}/group_weights.json", 'r') as f:
            self.predictor.group_weights = json.load(f)
            # JSON'dan gelen string key'leri int'e çevir
            self.predictor.group_weights = {
                int(k): v for k, v in self.predictor.group_weights.items()
            }
        
        # Label encoder'ları yükle
        with open(f"{self.model_path}/label_encoders.pkl", 'rb') as f:
            self.predictor.label_encoders = pickle.load(f)
        
        # Her grup için model ve scaler yükle
        for group_id in range(1, 6):
            with open(f"{self.model_path}/group_{group_id}_model.pkl", 'rb') as f:
                self.predictor.models[group_id] = pickle.load(f)
            with open(f"{self.model_path}/group_{group_id}_scaler.pkl", 'rb') as f:
                self.predictor.scalers[group_id] = pickle.load(f)
        
        print("✅ Tüm modeller başarıyla yüklendi!")
    
    def create_sample_scenarios(self) -> List[Dict[str, Any]]:
        """Test senaryoları oluştur"""
        scenarios = [
            {
                'name': 'İdeal Hava Koşulları',
                'data': {
                    'temperature_2m': 22,
                    'relative_humidity_2m': 55,
                    'precipitation': 0.1,  # Hafif yağış
                    'wind_speed_10m': 3,
                    'wind_direction_10m': 180,
                    'uv_index': 3,
                    'pm10': 15,
                    'pm2_5': 8,
                    'nitrogen_dioxide': 20,
                    'sulphur_dioxide': 10,
                    'ozone': 60,
                    'carbon_monoxide': 500,
                    'methane': 1400,
                    'upi_value': 1,
                    'plant_upi_value': 1,
                    'pollen_code': 'GRASS',
                    'plant_code': 'GRAMINALES',
                    'in_season': False,
                    'plant_in_season': False,
                    'hour': 14,
                    'day_of_year': 244
                }
            },
            {
                'name': 'Yüksek Polen Sezonu',
                'data': {
                    'temperature_2m': 28,
                    'relative_humidity_2m': 35,
                    'precipitation': 0,  # Yağış yok
                    'wind_speed_10m': 15,  # Yüksek rüzgar
                    'wind_direction_10m': 90,
                    'uv_index': 8,
                    'pm10': 20,
                    'pm2_5': 12,
                    'nitrogen_dioxide': 25,
                    'sulphur_dioxide': 15,
                    'ozone': 85,
                    'carbon_monoxide': 800,
                    'methane': 1450,
                    'upi_value': 4,  # Yüksek polen
                    'plant_upi_value': 4,
                    'pollen_code': 'WEED',
                    'plant_code': 'RAGWEED',  # En alerjik bitki
                    'in_season': True,
                    'plant_in_season': True,
                    'hour': 11,
                    'day_of_year': 240
                }
            },
            {
                'name': 'Kötü Hava Kalitesi',
                'data': {
                    'temperature_2m': 32,
                    'relative_humidity_2m': 80,
                    'precipitation': 0,
                    'wind_speed_10m': 2,  # Düşük rüzgar
                    'wind_direction_10m': 45,
                    'uv_index': 10,
                    'pm10': 60,  # Yüksek PM10
                    'pm2_5': 40,  # Yüksek PM2.5
                    'nitrogen_dioxide': 60,
                    'sulphur_dioxide': 30,
                    'ozone': 120,
                    'carbon_monoxide': 2000,
                    'methane': 1600,
                    'upi_value': 2,
                    'plant_upi_value': 2,
                    'pollen_code': 'TREE',
                    'plant_code': 'OLIVE',
                    'in_season': False,
                    'plant_in_season': False,
                    'hour': 15,
                    'day_of_year': 245
                }
            },
            {
                'name': 'Karma Risk Durumu',
                'data': {
                    'temperature_2m': 26,
                    'relative_humidity_2m': 65,
                    'precipitation': 0,
                    'wind_speed_10m': 8,
                    'wind_direction_10m': 200,
                    'uv_index': 6,
                    'pm10': 35,
                    'pm2_5': 20,
                    'nitrogen_dioxide': 40,
                    'sulphur_dioxide': 20,
                    'ozone': 95,
                    'carbon_monoxide': 1200,
                    'methane': 1500,
                    'upi_value': 3,
                    'plant_upi_value': 3,
                    'pollen_code': 'WEED',
                    'plant_code': 'MUGWORT',
                    'in_season': True,
                    'plant_in_season': True,
                    'hour': 16,
                    'day_of_year': 242
                }
            }
        ]
        return scenarios
    
    def run_comprehensive_test(self):
        """Kapsamlı test çalıştır"""
        print("🧪 Kapsamlı test başlıyor...\n")
        
        scenarios = self.create_sample_scenarios()
        
        for scenario in scenarios:
            print(f"📋 Senaryo: {scenario['name']}")
            print("=" * 50)
            
            for group_id in range(1, 6):
                try:
                    result = self.predictor.predict_safe_time(scenario['data'], group_id)
                    
                    print(f"👥 {result['group_name']}:")
                    print(f"   ⏰ Güvenli süre: {result['predicted_safe_hours']} saat")
                    print(f"   🎯 Risk skoru: {result['risk_score']} ({result['risk_level']})")
                    print(f"   💡 Öneri: {result['recommendation']}")
                    print()
                    
                except Exception as e:
                    print(f"❌ Grup {group_id} için hata: {e}")
            
            print("-" * 70)
            print()
    
    def interactive_prediction(self):
        """Interaktif tahmin"""
        print("🎮 İnteraktif Tahmin Modu")
        print("Hava durumu bilgilerini girin:")
        
        try:
            # Temel hava durumu bilgileri
            temperature = float(input("🌡️  Sıcaklık (°C): "))
            humidity = float(input("💧 Nem oranı (%): "))
            wind_speed = float(input("💨 Rüzgar hızı (m/s): "))
            uv_index = float(input("☀️ UV indeksi (0-11): "))
            
            # Hava kalitesi
            pm10 = float(input("🏭 PM10 (µg/m³): "))
            pm25 = float(input("🏭 PM2.5 (µg/m³): "))
            
            # Polen bilgileri
            print("\n🌿 Polen türü seçin:")
            print("1 - GRASS (Çim)")
            print("2 - TREE (Ağaç)")
            print("3 - WEED (Yabani ot)")
            pollen_choice = int(input("Seçim (1-3): "))
            pollen_map = {1: 'GRASS', 2: 'TREE', 3: 'WEED'}
            pollen_code = pollen_map.get(pollen_choice, 'GRASS')
            
            upi_value = float(input("🌸 Polen yoğunluğu (1-5): "))
            
            in_season = input("🗓️  Mevsiminde mi? (e/h): ").lower().startswith('e')
            
            # Grup seçimi
            print(f"\n👥 Allerji grubunuzu seçin:")
            for group_id, group_name in self.predictor.groups.items():
                print(f"{group_id} - {group_name}")
            
            selected_group = int(input("Grup seçimi (1-5): "))
            
            # Veri hazırla
            input_data = {
                'temperature_2m': temperature,
                'relative_humidity_2m': humidity,
                'precipitation': 0,
                'wind_speed_10m': wind_speed,
                'wind_direction_10m': 180,
                'uv_index': uv_index,
                'pm10': pm10,
                'pm2_5': pm25,
                'nitrogen_dioxide': 25,
                'sulphur_dioxide': 15,
                'ozone': 80,
                'carbon_monoxide': 800,
                'methane': 1400,
                'upi_value': upi_value,
                'plant_upi_value': upi_value,
                'pollen_code': pollen_code,
                'plant_code': 'GRAMINALES',
                'in_season': in_season,
                'plant_in_season': in_season,
                'hour': 14,
                'day_of_year': 244
            }
            
            # Tahmin yap
            result = self.predictor.predict_safe_time(input_data, selected_group)
            
            print("\n🎯 TAHMIN SONUCU")
            print("=" * 40)
            print(f"👥 Grup: {result['group_name']}")
            print(f"⏰ Güvenli süre: {result['predicted_safe_hours']} saat")
            print(f"🎯 Risk skoru: {result['risk_score']} ({result['risk_level']})")
            print(f"💡 Öneri: {result['recommendation']}")
            
        except KeyboardInterrupt:
            print("\n👋 Çıkış yapılıyor...")
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    def compare_all_groups(self, data: Dict[str, Any]):
        """Tüm gruplar için karşılaştırma"""
        print("🔄 Tüm gruplar için karşılaştırma:")
        print("=" * 60)
        
        results = []
        for group_id in range(1, 6):
            result = self.predictor.predict_safe_time(data, group_id)
            results.append(result)
        
        # Sonuçları sırala (güvenli süreye göre)
        results.sort(key=lambda x: x['predicted_safe_hours'], reverse=True)
        
        for i, result in enumerate(results, 1):
            emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
            print(f"{emoji} {result['group_name']}")
            print(f"   ⏰ {result['predicted_safe_hours']} saat")
            print(f"   🎯 Risk: {result['risk_level']} ({result['risk_score']})")
            print()
    
    def analyze_feature_importance(self):
        """Özellik önemini analiz et"""
        print("📊 Özellik Önem Analizi")
        print("=" * 40)
        
        for group_id in range(1, 6):
            model = self.predictor.models[group_id]
            feature_names = [
                'temperature_2m', 'relative_humidity_2m', 'precipitation',
                'wind_speed_10m', 'wind_direction_10m', 'uv_index',
                'pm10', 'pm2_5', 'nitrogen_dioxide', 'sulphur_dioxide', 'ozone',
                'carbon_monoxide', 'methane', 'upi_value', 'plant_upi_value',
                'pollen_code_encoded', 'plant_code_encoded',
                'in_season_encoded', 'plant_in_season_encoded',
                'hour', 'day_of_year'
            ]
            
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                
                # En önemli 5 özelliği al
                feature_importance = list(zip(feature_names[:len(importances)], importances))
                feature_importance.sort(key=lambda x: x[1], reverse=True)
                
                print(f"\n👥 {self.predictor.groups[group_id]} - En Önemli Özellikler:")
                for i, (feature, importance) in enumerate(feature_importance[:5], 1):
                    print(f"   {i}. {feature}: {importance:.3f}")

def main():
    """Ana fonksiyon"""
    print("🌟 AllerMind - Allerji Tahmin Sistemi Demo")
    print("=" * 50)
    
    try:
        demo = AllergyPredictionDemo()
        
        while True:
            print("\n📋 Menü:")
            print("1 - Kapsamlı Test Çalıştır")
            print("2 - İnteraktif Tahmin")
            print("3 - Özellik Önem Analizi")
            print("4 - Örnek Senaryo Karşılaştırma")
            print("0 - Çıkış")
            
            choice = input("\nSeçiminiz (0-4): ")
            
            if choice == '1':
                demo.run_comprehensive_test()
            elif choice == '2':
                demo.interactive_prediction()
            elif choice == '3':
                demo.analyze_feature_importance()
            elif choice == '4':
                scenarios = demo.create_sample_scenarios()
                for i, scenario in enumerate(scenarios, 1):
                    print(f"\n{i}. {scenario['name']}")
                
                scenario_choice = int(input("Senaryo seçin (1-4): ")) - 1
                if 0 <= scenario_choice < len(scenarios):
                    demo.compare_all_groups(scenarios[scenario_choice]['data'])
            elif choice == '0':
                print("👋 Güle güle!")
                break
            else:
                print("❌ Geçersiz seçim!")
                
    except KeyboardInterrupt:
        print("\n👋 Çıkış yapılıyor...")
    except Exception as e:
        print(f"❌ Genel hata: {e}")

if __name__ == "__main__":
    main()
