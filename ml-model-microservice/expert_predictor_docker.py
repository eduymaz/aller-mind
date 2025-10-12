#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALLERMIND V2.0 - EXPERT PREDICTION SYSTEM (Docker Compatible Version)
Kişisel ağırlık parametreli gelişmiş tahmin sistemi
"""

import pickle
import json
import os
import numpy as np
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ExpertAllermindPredictor:
    """Expert-level Allermind prediction system with personal weighting"""
    
    def __init__(self, model_path=None):
        # Docker uyumlu dinamik path
        if model_path is None:
            # Önce environment variable kontrol et
            model_path = os.environ.get('MODEL_PATH')
            
            # Yoksa, script'in bulunduğu dizini kullan
            if model_path is None:
                model_path = os.path.dirname(os.path.abspath(__file__))
        
        self.model_path = model_path
        self.models = {}
        self.ensemble_config = None
        self.load_models()
    
    def load_models(self):
        """Tüm grup modellerini yükle"""
        
        print("🚀 ALLERMIND V2.0 EXPERT PREDICTION SYSTEM (Docker)")
        print("=" * 60)
        print(f"📂 Model path: {self.model_path}")
        print("📦 Gelişmiş modeller yükleniyor...")
        
        # Ensemble config yükle
        try:
            config_path = os.path.join(self.model_path, "ensemble_config_v2.json")
            print(f"🔍 Config path: {config_path}")
            
            if not os.path.exists(config_path):
                print(f"❌ Config dosyası bulunamadı: {config_path}")
                print(f"📁 Dizin içeriği: {os.listdir(self.model_path)}")
                return False
                
            with open(config_path, 'r') as f:
                self.ensemble_config = json.load(f)
            print("✅ Ensemble configuration yüklendi")
        except Exception as e:
            print(f"❌ Ensemble config yüklenemedi: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Her grup modelini yükle
        success_count = 0
        for group_id in range(1, 6):
            try:
                model_file = f"Grup{group_id}_advanced_model_v2.pkl"
                model_path = os.path.join(self.model_path, model_file)
                print(f"🔍 Loading: {model_path}")
                
                if not os.path.exists(model_path):
                    print(f"❌ Model dosyası bulunamadı: {model_path}")
                    continue
                
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
                import traceback
                traceback.print_exc()
        
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
            'plant_in_season': 0, 'plant_upi_value': 0, 'pollen_diversity_index': 0.0,
            'grass_pollen': 0, 'tree_pollen': 0, 'weed_pollen': 0
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
                validated_data[feature] = float(environmental_data.get(feature, default_val))
        
        if missing_features:
            print(f"⚠️  Eksik özellikler default değerlerle dolduruldu: {missing_features}")
        
        return validated_data, missing_features
    
    def calculate_personal_multiplier(self, personal_params, group_id, profile=None):
        """Kişisel çarpan hesapla"""
        
        base_multiplier = 1.0
        
        # Kişisel hassasiyet (1-5)
        kisisel_hassasiyet = personal_params.get('kisisel_hassasiyet', 3)
        hassasiyet_weight = (kisisel_hassasiyet - 3) * 0.15
        
        # İlaç kullanımı (0-5)
        ilac_kullanimi = personal_params.get('ilaç_kullanimi', 0)
        ilac_weight = ilac_kullanimi * -0.08
        
        # Grup bazlı ağırlıklar
        group_weights = {
            1: 0.8,
            2: 1.0,
            3: 1.2,
            4: 1.4,
            5: 1.6
        }
        
        group_weight = group_weights.get(group_id, 1.0)
        
        # Profil bazlı düzeltmeler
        profile_modifier = 1.0
        if profile:
            # Yaş faktörü
            age = profile.get('age', 30)
            if age < 18 or age > 65:
                profile_modifier *= 1.1
            
            # Aile geçmişi
            if profile.get('family_allergy_history', False):
                profile_modifier *= 1.1
            
            # Önceki ciddi reaksiyonlar
            prev_reactions = profile.get('previous_reactions', {})
            if prev_reactions.get('severe_asthma', False):
                profile_modifier *= 1.2
            if prev_reactions.get('hospitalization', False):
                profile_modifier *= 1.15
            if prev_reactions.get('anaphylaxis', False):
                profile_modifier *= 1.25
        
        # Toplam çarpan
        personal_multiplier = (base_multiplier + hassasiyet_weight + ilac_weight) * group_weight * profile_modifier
        
        # Aralık sınırlaması
        personal_multiplier = max(0.5, min(2.0, personal_multiplier))
        
        return personal_multiplier
    
    def calculate_safe_hours(self, risk_score, personal_multiplier):
        """Güvenli dış mekan saati hesapla"""
        
        # Base safe hours (8 saat)
        base_hours = 8.0
        
        # Risk skoru düzeltmesi
        risk_factor = max(0, 1 - risk_score)
        
        # Kişisel çarpan düzeltmesi
        personal_hours = base_hours * risk_factor / personal_multiplier
        
        # Minimum 0.5, maksimum 12 saat
        safe_hours = max(0.5, min(12.0, personal_hours))
        
        return safe_hours
    
    def determine_risk_level(self, risk_score):
        """Risk seviyesi belirle"""
        
        if risk_score >= 0.7:
            return "Yüksek"
        elif risk_score >= 0.4:
            return "Orta"
        else:
            return "Düşük"
    
    def predict_group(self, environmental_data, group_id, personal_params=None):
        """Belirli bir grup için tahmin yap"""
        
        if group_id not in self.models:
            print(f"❌ Grup {group_id} modeli bulunamadı")
            return None
        
        # Input validation
        validated_data, missing = self.validate_input(environmental_data)
        
        # Model bilgilerini al
        model_info = self.models[group_id]
        model = model_info['model']
        scaler = model_info['scaler']
        feature_names = model_info['feature_names']
        
        # DataFrame oluştur
        input_df = pd.DataFrame([validated_data])
        
        # Sadece modelin beklediği özellikleri al
        input_df = input_df[feature_names]
        
        # Scaling
        X_scaled = scaler.transform(input_df)
        
        # Base prediction
        base_risk = model.predict(X_scaled)[0]
        
        # Personal parameters
        if personal_params is None:
            personal_params = {'kisisel_hassasiyet': 3, 'ilaç_kullanimi': 0}
        
        profile = personal_params.get('profile', {})
        
        # Personal multiplier
        personal_multiplier = self.calculate_personal_multiplier(
            personal_params, group_id, profile
        )
        
        # Adjusted risk
        adjusted_risk = base_risk * personal_multiplier
        adjusted_risk = max(0.0, min(1.0, adjusted_risk))
        
        # Safe hours
        base_safe_hours = self.calculate_safe_hours(base_risk, 1.0)
        personal_safe_hours = self.calculate_safe_hours(adjusted_risk, personal_multiplier)
        
        # Risk level
        risk_level = self.determine_risk_level(adjusted_risk)
        
        # Group name
        group_names = {
            1: "Alerjik Olmayan Grup",
            2: "Hafif-Orta Alerjik Grup",
            3: "Orta-Şiddetli Alerjik Grup",
            4: "Şiddetli Alerjik Grup",
            5: "Çok Şiddetli Alerjik Grup"
        }
        
        return {
            'group_id': group_id,
            'group_name': group_names.get(group_id, f"Grup {group_id}"),
            'base_risk_score': float(base_risk),
            'risk_score': float(adjusted_risk),
            'risk_level': risk_level,
            'personal_multiplier': float(personal_multiplier),
            'base_safe_hours': float(base_safe_hours),
            'personal_safe_hours': float(personal_safe_hours),
            'model_algorithm': model_info['algorithm_used'],
            'missing_features': missing
        }
    
    def predict_ensemble(self, environmental_data, personal_params=None):
        """Tüm modelleri kullanarak ensemble tahmin yap"""
        
        if not self.ensemble_config:
            print("❌ Ensemble config yüklenmedi")
            return None
        
        predictions = []
        weights = []
        
        for group_id in range(1, 6):
            if group_id in self.models:
                result = self.predict_group(environmental_data, group_id, personal_params)
                
                if result:
                    predictions.append(result)
                    
                    # Ensemble ağırlığı
                    group_config = self.ensemble_config.get('group_weights', {}).get(str(group_id), {})
                    weight = group_config.get('weight', 0.2)
                    weights.append(weight)
        
        if not predictions:
            print("❌ Hiç tahmin yapılamadı")
            return None
        
        # Normalize weights
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        
        # Weighted ensemble
        ensemble_risk = sum(p['risk_score'] * w for p, w in zip(predictions, normalized_weights))
        ensemble_safe_hours = sum(p['personal_safe_hours'] * w for p, w in zip(predictions, normalized_weights))
        
        # Best performing group
        best_group = max(predictions, key=lambda x: x['risk_score'])
        
        return {
            'ensemble_prediction': {
                'risk_score': float(ensemble_risk),
                'risk_level': self.determine_risk_level(ensemble_risk),
                'safe_hours': float(ensemble_safe_hours),
                'confidence': float(1.0 - np.std([p['risk_score'] for p in predictions]))
            },
            'individual_predictions': predictions,
            'best_performing_group': best_group,
            'ensemble_weights': {str(i+1): float(w) for i, w in enumerate(normalized_weights)}
        }
    
    def get_model_info(self):
        """Model bilgilerini döndür"""
        
        return {
            'loaded_models': list(self.models.keys()),
            'total_models': len(self.models),
            'models_path': self.model_path,
            'ensemble_enabled': self.ensemble_config is not None
        }
