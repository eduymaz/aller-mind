#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALLERMIND V2.0 - EXPERT PREDICTION SYSTEM
Kişisel ağırlık parametreli gelişmiş tahmin sistemi
"""

import os
import pickle
import json
import numpy as np
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ExpertAllermindPredictor:
    """Expert-level Allermind prediction system with personal weighting"""
    
    def __init__(self, model_path=None):
        # Eğer model_path belirtilmemişse, bu dosyanın bulunduğu dizini kullan
        if model_path is None:
            model_path = os.path.dirname(os.path.abspath(__file__))
        self.model_path = model_path
        self.models = {}
        self.ensemble_config = None
        self.load_models()
    
    def load_models(self):
        """Tüm grup modellerini yükle"""
        
        print("🚀 ALLERMIND V2.0 EXPERT PREDICTION SYSTEM")
        print("=" * 60)
        print("📦 Gelişmiş modeller yükleniyor...")
        
        # Ensemble config yükle
        try:
            config_path = f"{self.model_path}/ensemble_config_v2.json"
            with open(config_path, 'r') as f:
                self.ensemble_config = json.load(f)
            print("✅ Ensemble configuration yüklendi")
        except Exception as e:
            print(f"❌ Ensemble config yüklenemedi: {e}")
            return False
        
        # Her grup modelini yükle
        success_count = 0
        for group_id in range(1, 6):
            try:
                model_path = f"{self.model_path}/Grup{group_id}_advanced_model_v2.pkl"
                with open(model_path, 'rb') as f:
                    self.models[group_id] = pickle.load(f)
                
                # Model info
                model_info = self.models[group_id]
                algorithm = model_info['algorithm_used']
                performance = model_info['performance']
                
                print(f"✅ Grup {group_id}: {algorithm}")
                print(f"   📊 Test R²: {performance['test_r2']:.4f}, MAE: {performance['test_mae']:.4f}")
                
                success_count += 1
                
            except Exception as e:
                print(f"❌ Grup {group_id} modeli yüklenemedi: {e}")
        
        print(f"\n🎉 {success_count}/5 model başarıyla yüklendi!")
        return success_count == 5
    
    def validate_input(self, environmental_data):
        """Input verilerini validate et"""
        
        required_features = [
            'temperature_2m', 'relative_humidity_2m', 'precipitation', 
            'wind_speed_10m', 'pm10', 'pm2_5', 'ozone', 'nitrogen_dioxide', 
            'uv_index', 'surface_pressure'
        ]
        
        missing_features = []
        validated_data = {}
        
        # Default değerler
        defaults = {
            'temperature_2m': 22.0, 'relative_humidity_2m': 55.0, 'precipitation': 0.0,
            'snowfall': 0.0, 'rain': 0.0, 'cloud_cover': 30.0, 'surface_pressure': 1013.0,
            'wind_speed_10m': 5.0, 'wind_direction_10m': 180.0, 'sunshine_duration': 8.0,
            'pm10': 20.0, 'pm2_5': 12.0, 'carbon_dioxide': 400.0, 'carbon_monoxide': 1.0,
            'nitrogen_dioxide': 20.0, 'sulphur_dioxide': 10.0, 'ozone': 100.0,
            'aerosol_optical_depth': 0.2, 'methane': 1900.0, 'uv_index': 5.0,
            'uv_index_clear_sky': 6.0, 'dust': 50.0, 'pollen_code': 0,
            'in_season': 0, 'upi_value': 0, 'plant_code': 0,
            'plant_in_season': 0, 'plant_upi_value': 0
        }
        
        # Feature validation ve default assignment
        for feature in required_features:
            if feature in environmental_data:
                validated_data[feature] = float(environmental_data[feature])
            else:
                missing_features.append(feature)
                validated_data[feature] = defaults.get(feature, 0.0)
        
        # Tüm diğer özellikleri de ekle
        for feature, default_val in defaults.items():
            if feature not in validated_data:
                validated_data[feature] = environmental_data.get(feature, default_val)
        
        return validated_data, missing_features
    
    def create_engineered_features(self, data):
        """Engineered features oluştur"""
        
        engineered = data.copy()
        
        # Time-based features (şu an için sabit değerler)
        engineered['hour'] = 12  # Varsayılan öğle saati
        engineered['day_of_week'] = 2  # Varsayılan çarşamba
        engineered['lat'] = 39.9334  # Varsayılan Ankara koordinatı
        engineered['lon'] = 32.8597
        
        # AQI Combined
        try:
            engineered['aqi_combined'] = (
                data['pm10'] * 0.3 + 
                data['pm2_5'] * 0.4 + 
                data['ozone'] * 0.2 + 
                data['nitrogen_dioxide'] * 0.1
            )
        except:
            engineered['aqi_combined'] = 50.0
        
        # Pollen risk index
        try:
            engineered['pollen_risk_index'] = (
                data['upi_value'] * 0.5 + 
                data['plant_upi_value'] * 0.3 + 
                (data['wind_speed_10m'] / 20) * 0.2
            )
        except:
            engineered['pollen_risk_index'] = 0.0
        
        # Comfort index
        try:
            temp = data['temperature_2m']
            humidity = data['relative_humidity_2m']
            wind = data['wind_speed_10m']
            engineered['comfort_index'] = (
                temp - (0.55 - 0.0055 * humidity) * (temp - 14.5) - wind * 0.16
            )
        except:
            engineered['comfort_index'] = 20.0
        
        # UV danger level
        try:
            uv = data['uv_index']
            if uv <= 2:
                engineered['uv_danger_level'] = 0
            elif uv <= 5:
                engineered['uv_danger_level'] = 1
            elif uv <= 7:
                engineered['uv_danger_level'] = 2
            elif uv <= 10:
                engineered['uv_danger_level'] = 3
            else:
                engineered['uv_danger_level'] = 4
        except:
            engineered['uv_danger_level'] = 2
        
        # Time-based features
        engineered['is_peak_pollen_hour'] = 1 if 6 <= engineered['hour'] <= 10 else 0
        engineered['is_weekend'] = 1 if engineered['day_of_week'] >= 5 else 0
        
        return engineered
    
    def predict_group(self, environmental_data, group_id, personal_params=None):
        """Belirli bir grup için tahmin yap"""
        
        if group_id not in self.models:
            return None
        
        model_package = self.models[group_id]
        model = model_package['model']
        scaler = model_package['scaler']
        features = model_package['features']
        algorithm = model_package['algorithm_used']
        
        # Veriyi validate et ve engineered features oluştur
        validated_data, missing_features = self.validate_input(environmental_data)
        engineered_data = self.create_engineered_features(validated_data)
        
        # Feature vector oluştur
        feature_vector = []
        for feature in features:
            feature_vector.append(engineered_data.get(feature, 0.0))
        
        feature_array = np.array(feature_vector).reshape(1, -1)
        
        # Scaling (SVR ve Neural Network için)
        if 'SVR' in algorithm or 'Neural' in algorithm:
            feature_array = scaler.transform(feature_array)
        
        # Base prediction
        base_prediction = model.predict(feature_array)[0]
        
        # Kişisel ağırlık uygula
        if personal_params:
            personal_multiplier = self.calculate_personal_multiplier(group_id, personal_params)
            adjusted_prediction = base_prediction / personal_multiplier
            adjusted_prediction = max(0.5, min(8.5, adjusted_prediction))
        else:
            adjusted_prediction = base_prediction
            personal_multiplier = 1.0
        
        # Risk score hesapla (inverse relationship)
        risk_score = max(0, min(1, (8.5 - adjusted_prediction) / 8.0))
        
        # Risk level
        if risk_score < 0.3:
            risk_level = 'Düşük'
            recommendation = "Dışarıda rahatça vakit geçirebilirsiniz."
        elif risk_score < 0.6:
            risk_level = 'Orta'
            recommendation = "Dikkatli olun, kısa-orta süreli dışarıda kalabilirsiniz."
        else:
            risk_level = 'Yüksek'
            recommendation = "İç mekan tercih edin, dışarıda kısa süre kalın."
        
        return {
            'group_id': group_id,
            'group_name': model_package['group_info']['name'],
            'algorithm': algorithm,
            'base_safe_hours': float(base_prediction),
            'personal_safe_hours': float(adjusted_prediction),
            'personal_multiplier': float(personal_multiplier),
            'risk_score': float(risk_score),
            'risk_level': risk_level,
            'recommendation': recommendation,
            'performance': model_package['performance'],
            'missing_features': missing_features,
            'prediction_timestamp': datetime.now().isoformat()
        }
    
    def calculate_personal_multiplier(self, group_id, personal_params):
        """Risk seviyesi temelli kişisel ağırlık multiplier'ı hesapla
        
        Grup 1: Yüksek Alerjen Grup (tanılı, şiddetli)
        Grup 2: Hafif-Orta Alerjen Grup 
        Grup 3: Genetik Yatkınlık Grubu (aile geçmişi)
        Grup 4: Sağlıklı Birey Grubu 
        Grup 5: Hassas Grup (çocuk/yaşlı/kronik)
        """
        
        if group_id not in self.models:
            return 1.0
        
        # Profil bilgilerini al
        profile = personal_params.get('profile', {})
        
        # 1. ÖNCE GRUP RİSK SEVİYESİNİ BELİRLE
        base_risk_multiplier = self.determine_user_risk_group(profile)
        
        # 2. SONRA ALERJİ TÜRÜ UYUMLULUĞUNU KONTROL ET
        allergy_relevance_multiplier = self.calculate_allergy_relevance(group_id, profile)
        
        # 3. KİŞİSEL YAŞAM TARZI FAKTÖRLERİNİ EKLE
        lifestyle_multiplier = self.calculate_lifestyle_factors(personal_params)
        
        # 4. TOPLAM MULTİPLİER HESAPLA
        total_multiplier = base_risk_multiplier * allergy_relevance_multiplier * lifestyle_multiplier
        
        # Sınırları uygula
        total_multiplier = max(0.3, min(5.0, total_multiplier))
        
        return total_multiplier
    
    def determine_user_risk_group(self, profile):
        """Kullanıcının hangi risk grubunda olduğunu belirle"""
        
        # Klinik tanı kontrolü
        clinical = profile.get('clinical_diagnosis', 'none')
        
        # Önceki reaksiyonlar
        reactions = profile.get('previous_reactions', {})
        severe_reactions = any(reactions.values())
        
        # Aile geçmişi
        family_history = profile.get('family_allergy_history', False)
        
        # Yaş kontrolü (çocuk/yaşlı)
        age = profile.get('age', 25)
        is_child_elderly = age < 12 or age > 65
        
        # Risk grubu belirleme
        if clinical == 'severe_allergy' or reactions.get('anaphylaxis', False):
            return 3.5  # Grup 1: Yüksek Risk
        elif clinical == 'asthma' or reactions.get('severe_asthma', False):
            return 3.0  # Grup 1: Yüksek Risk (astım)
        elif clinical == 'mild_moderate_allergy' or reactions.get('hospitalization', False):
            return 2.2  # Grup 2: Orta Risk
        elif family_history and clinical == 'none':
            return 1.8  # Grup 3: Genetik Yatkınlık
        elif is_child_elderly:
            return 2.5  # Grup 5: Hassas Grup
        else:
            return 1.0  # Grup 4: Sağlıklı Birey
    
    def calculate_allergy_relevance(self, group_id, profile):
        """Belirli model grubu için alerji türü uyumluluğu"""
        
        relevance_multiplier = 1.0
        
        # Grup 1: Polen Hassasiyeti Modeli
        if group_id == 1:
            polen_count = 0
            if profile.get('tree_pollen', {}).get('birch', False): polen_count += 1
            if profile.get('tree_pollen', {}).get('pine', False): polen_count += 1
            if profile.get('tree_pollen', {}).get('olive', False): polen_count += 1
            if profile.get('grass_pollen', {}).get('graminales', False): polen_count += 1
            if profile.get('weed_pollen', {}).get('mugwort', False): polen_count += 1
            if profile.get('weed_pollen', {}).get('ragweed', False): polen_count += 1
            
            if polen_count >= 4:
                relevance_multiplier = 2.8  # Çok yüksek polen hassasiyeti
            elif polen_count >= 2:
                relevance_multiplier = 2.0
            elif polen_count >= 1:
                relevance_multiplier = 1.5
            else:
                relevance_multiplier = 0.7  # Polen alerjisi yok, daha güvenli
        
        # Grup 2: Hava Kirliliği Modeli
        elif group_id == 2:
            air_sensitivity = profile.get('environmental_triggers', {}).get('air_pollution', False)
            smoke_sensitivity = profile.get('environmental_triggers', {}).get('smoke', False)
            
            if air_sensitivity and smoke_sensitivity:
                relevance_multiplier = 2.5
            elif air_sensitivity or smoke_sensitivity:
                relevance_multiplier = 1.8
            else:
                relevance_multiplier = 0.8
        
        # Grup 3: UV & Güneş Modeli
        elif group_id == 3:
            # UV hassasiyeti genellikle cilt tipi ve yaşla ilgili
            age = profile.get('age', 25)
            clinical = profile.get('clinical_diagnosis', 'none')
            
            if age < 5 or age > 70:  # Çok genç veya yaşlı
                relevance_multiplier = 2.0
            elif clinical in ['severe_allergy', 'asthma']:  # İmmün sistem zayıf
                relevance_multiplier = 1.6
            else:
                relevance_multiplier = 1.0  # Standart UV hassasiyeti
        
        # Grup 4: Meteorolojik Faktörler
        elif group_id == 4:
            # Basınç, nem, rüzgar hassasiyeti
            clinical = profile.get('clinical_diagnosis', 'none')
            
            if clinical == 'asthma':  # Astım hastaları hava değişimlerine çok hassas
                relevance_multiplier = 2.2
            elif clinical in ['severe_allergy', 'mild_moderate_allergy']:
                relevance_multiplier = 1.5
            else:
                relevance_multiplier = 1.0
        
        # Grup 5: Hassas Grup (Çok faktörlü)
        elif group_id == 5:
            # Çocuk/yaşlı/kronik hasta için tüm faktörler önemli
            age = profile.get('age', 25)
            clinical = profile.get('clinical_diagnosis', 'none')
            
            risk_factors = 0
            
            # Yaş faktörü
            if age < 12 or age > 65:
                risk_factors += 2
            
            # Klinik durum
            if clinical in ['severe_allergy', 'asthma']:
                risk_factors += 2
            elif clinical == 'mild_moderate_allergy':
                risk_factors += 1
            
            # Çevresel hassasiyetler
            env_triggers = profile.get('environmental_triggers', {})
            sensitive_count = sum(1 for trigger in env_triggers.values() if trigger)
            if sensitive_count >= 3:
                risk_factors += 2
            elif sensitive_count >= 1:
                risk_factors += 1
            
            # Risk faktörüne göre multiplier
            if risk_factors >= 5:
                relevance_multiplier = 3.0
            elif risk_factors >= 3:
                relevance_multiplier = 2.0
            elif risk_factors >= 1:
                relevance_multiplier = 1.5
            else:
                relevance_multiplier = 1.0
        
        return relevance_multiplier
    
    def calculate_lifestyle_factors(self, personal_params):
        """Yaşam tarzı faktörlerini hesapla"""        
        multiplier = 1.0
        
        # Temel kişisel faktörler
        hassasiyet = personal_params.get('kisisel_hassasiyet', 3)
        dis_aktivite = personal_params.get('dis_aktivite_suresi', 120)
        egzersiz = personal_params.get('egzersiz_yogunlugu', 3)
        ilac_kullanimi = personal_params.get('ilaç_kullanimi', 0)
        stres = personal_params.get('stres_seviyesi', 3)
        uyku = personal_params.get('uyku_kalitesi', 3)
        beslenme = personal_params.get('beslenme_kalitesi', 3)
        
        # Hassasiyet faktörü (1-5 arası, yüksek hassasiyet = daha riskli)
        if hassasiyet >= 4:
            multiplier *= 1.4  # Çok hassas kişiler
        elif hassasiyet >= 3:
            multiplier *= 1.2
        elif hassasiyet <= 2:
            multiplier *= 0.9
        
        # Dış aktivite süresi (uzun süre dışarıda = daha riskli)
        if dis_aktivite > 240:
            multiplier *= 1.3
        elif dis_aktivite > 120:
            multiplier *= 1.1
        elif dis_aktivite < 60:
            multiplier *= 0.95
        
        # İlaç kullanımı (ilaç var = biraz daha güvenli)
        if ilac_kullanimi == 1:
            multiplier *= 0.85
        
        # Stres seviyesi (yüksek stres = bağışıklık zayıf = daha riskli)
        if stres >= 4:
            multiplier *= 1.2
        elif stres <= 2:
            multiplier *= 0.95
        
        # Uyku kalitesi (kötü uyku = bağışıklık zayıf = daha riskli)
        if uyku <= 2:
            multiplier *= 1.3
        elif uyku >= 4:
            multiplier *= 0.9
        
        # Beslenme kalitesi (kötü beslenme = bağışıklık zayıf = daha riskli)
        if beslenme <= 2:
            multiplier *= 1.2
        elif beslenme >= 4:
            multiplier *= 0.95
        
        return multiplier
    
    def predict_ensemble(self, environmental_data, personal_params=None):
        """Ensemble tahmin - tüm grupların ağırlıklı ortalaması"""
        
        print(f"🔮 Ensemble tahmin başlatılıyor...")
        
        # Her grup için tahmin yap
        group_predictions = {}
        valid_predictions = []
        
        for group_id in range(1, 6):
            prediction = self.predict_group(environmental_data, group_id, personal_params)
            if prediction:
                group_predictions[group_id] = prediction
                
                # Sadece yüksek performanslı modelleri ensemble'da kullan
                if prediction['performance']['test_r2'] > 0.95:
                    valid_predictions.append(prediction)
                
                print(f"  Grup {group_id}: {prediction['personal_safe_hours']:.1f} saat (Risk: {prediction['risk_level']})")
        
        if not valid_predictions:
            print("  ⚠️ Güvenilir tahmin bulunamadı")
            return None
        
        # Ağırlıklı ortalama (performance-based)
        total_weight = 0
        weighted_hours = 0
        
        for pred in valid_predictions:
            weight = pred['performance']['test_r2']  # R² değeri ağırlık olarak
            weighted_hours += weight * pred['personal_safe_hours']
            total_weight += weight
        
        final_hours = weighted_hours / total_weight if total_weight > 0 else 4.0
        final_risk = max(0, min(1, (8.5 - final_hours) / 8.0))
        
        # Final risk level
        if final_risk < 0.3:
            final_risk_level = 'Düşük'
            final_recommendation = "Dışarıda güvenle vakit geçirebilirsiniz."
        elif final_risk < 0.6:
            final_risk_level = 'Orta'
            final_recommendation = "Dikkatli olun, kısa-orta süreli dışarıda kalabilirsiniz."
        else:
            final_risk_level = 'Yüksek'
            final_recommendation = "İç mekan tercih edin, kısa süre dışarıda kalın."
        
        return {
            'ensemble_prediction': {
                'safe_outdoor_hours': float(final_hours),
                'risk_score': float(final_risk),
                'risk_level': final_risk_level,
                'recommendation': final_recommendation,
                'confidence': len(valid_predictions) / 5.0,
                'models_used': [p['group_id'] for p in valid_predictions],
                'prediction_timestamp': datetime.now().isoformat()
            },
            'individual_predictions': group_predictions,
            'personal_parameters': personal_params or {},
            'input_validation': {
                'missing_features': group_predictions[1]['missing_features'] if group_predictions else [],
                'total_features': len(environmental_data)
            },
            'ensemble_info': {
                'total_models': 5,
                'reliable_models': len(valid_predictions),
                'weighting_method': 'performance_based_r2'
            }
        }
    
    def get_model_info(self):
        """Model bilgilerini döndür"""
        
        model_info = {}
        
        for group_id, model_package in self.models.items():
            model_info[group_id] = {
                'group_name': model_package['group_info']['name'],
                'algorithm': model_package['algorithm_used'],
                'performance': model_package['performance'],
                'features_count': len(model_package['features']),
                'target_type': model_package['target_info']['target_type'],
                'created_at': model_package['created_at']
            }
        
        return model_info

def demo_expert_system():
    """Expert sistem demo"""
    
    print("🎯 ALLERMIND V2.0 EXPERT SYSTEM DEMO")
    print("=" * 50)
    
    # Predictor oluştur
    predictor = ExpertAllermindPredictor()
    
    # Test scenarios
    scenarios = {
        'İdeal Hava Koşulları': {
            'environmental_data': {
                'temperature_2m': 23.0, 'relative_humidity_2m': 55.0,
                'precipitation': 0.0, 'wind_speed_10m': 8.0,
                'pm10': 15.0, 'pm2_5': 8.0, 'ozone': 80.0,
                'nitrogen_dioxide': 15.0, 'uv_index': 5.0, 'surface_pressure': 1015.0
            },
            'personal_params': {
                'age_group': 'adult',
                'medical_condition': 'healthy',
                'activity_level': 'moderate',
                'sensitivity_level': 'moderate'
            }
        },
        'Hassas Birey - Kirli Hava': {
            'environmental_data': {
                'temperature_2m': 32.0, 'relative_humidity_2m': 40.0,
                'precipitation': 0.0, 'wind_speed_10m': 3.0,
                'pm10': 75.0, 'pm2_5': 45.0, 'ozone': 160.0,
                'nitrogen_dioxide': 40.0, 'uv_index': 9.0, 'surface_pressure': 1008.0
            },
            'personal_params': {
                'age_group': 'elderly',
                'medical_condition': 'asthma',
                'activity_level': 'high',
                'sensitivity_level': 'very_high'
            }
        }
    }
    
    for scenario_name, scenario_data in scenarios.items():
        print(f"\n{'='*20} {scenario_name.upper()} {'='*20}")
        
        result = predictor.predict_ensemble(
            scenario_data['environmental_data'],
            scenario_data['personal_params']
        )
        
        if result:
            ensemble = result['ensemble_prediction']
            print(f"🎯 ENSEMBLE SONUCU:")
            print(f"   Güvenli Dış Mekan: {ensemble['safe_outdoor_hours']:.1f} saat")
            print(f"   Risk Seviyesi: {ensemble['risk_level']}")
            print(f"   Güven: {ensemble['confidence']:.1%}")
            print(f"   Kullanılan Modeller: {ensemble['models_used']}")
            print(f"   Öneri: {ensemble['recommendation']}")
            
            # En iyi ve en kötü model
            predictions = result['individual_predictions']
            if predictions:
                best = max(predictions.items(), key=lambda x: x[1]['performance']['test_r2'])
                worst = min(predictions.items(), key=lambda x: x[1]['performance']['test_r2'])
                
                print(f"\n   🏆 En İyi Model: Grup {best[0]} ({best[1]['algorithm']}) - R²: {best[1]['performance']['test_r2']:.4f}")
                print(f"   🔻 En Zayıf Model: Grup {worst[0]} ({worst[1]['algorithm']}) - R²: {worst[1]['performance']['test_r2']:.4f}")

if __name__ == "__main__":
    demo_expert_system()