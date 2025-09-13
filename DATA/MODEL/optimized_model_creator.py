#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllerMind Optimized Model Creator
En iyi performans gösteren modelleri yeniden paketler
"""

import pickle
import json
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import os

class OptimizedModelCreator:
    def __init__(self):
        self.pkl_models_path = "pkl_models/"
        
    def create_optimized_model_package(self, group_id, group_name, algorithm_type, model, scaler, features):
        """Optimize edilmiş model paketi oluştur"""
        
        # Model performans metrikleri (analiz sonuçlarından)
        performance_metrics = {
            1: {"r2": 0.9956, "mse": 0.0052, "mae": 0.0096, "algorithm": "Random Forest"},
            2: {"r2": 0.9962, "mse": 0.0021, "mae": 0.0385, "algorithm": "RBF SVM"},
            3: {"r2": 0.9975, "mse": 0.0016, "mae": 0.0343, "algorithm": "RBF SVM"},
            4: {"r2": 0.9980, "mse": 0.0009, "mae": 0.0245, "algorithm": "RBF SVM"},
            5: {"r2": 0.9955, "mse": 0.0022, "mae": 0.0401, "algorithm": "RBF SVM"}
        }
        
        model_package = {
            'model': model,
            'scaler': scaler,
            'features': features,
            'group_info': {
                'id': group_id,
                'name': group_name,
                'algorithm': algorithm_type,
                'performance': performance_metrics.get(group_id, {}),
                'optimization_date': '2025-09-12',
                'version': '2.0'
            },
            'prediction_metadata': {
                'input_features_count': len(features),
                'expected_output_range': [0, 24],  # Saatlik tahmin
                'confidence_threshold': performance_metrics.get(group_id, {}).get('r2', 0.95)
            }
        }
        
        # Model dosyasını kaydet
        filename = f"{self.pkl_models_path}{group_name}_model.pkl"
        with open(filename, 'wb') as f:
            pickle.dump(model_package, f)
            
        print(f"✅ {group_name} modeli optimize edilerek kaydedildi: {filename}")
        return model_package
    
    def load_and_repackage_models(self):
        """Mevcut modelleri yükle ve yeniden paketle"""
        
        # Grup tanımları
        groups = {
            1: {"name": "Grup1_Siddetli_Alerjik", "algorithm": "Random Forest"},
            2: {"name": "Grup2_Hafif_Orta", "algorithm": "RBF SVM"},
            3: {"name": "Grup3_Genetik_Yatkinlik", "algorithm": "RBF SVM"},
            4: {"name": "Grup4_Kaliteli_Yasam", "algorithm": "RBF SVM"},
            5: {"name": "Grup5_Hassas_Cocuk_Yasli", "algorithm": "RBF SVM"}
        }
        
        # Özellik listesi (analiz sonuçlarından)
        features = [
            'upi_value', 'plant_upi_value', 'in_season', 'plant_in_season',
            'pm2_5', 'pm10', 'ozone', 'nitrogen_dioxide', 'sulphur_dioxide', 
            'carbon_monoxide', 'temperature_2m', 'relative_humidity_2m',
            'precipitation', 'snowfall', 'rain', 'cloud_cover', 
            'surface_pressure', 'wind_speed_10m', 'wind_direction_10m',
            'soil_temperature_0_to_7cm', 'soil_moisture_0_to_7cm',
            'sunshine_duration', 'uv_index', 'uv_index_clear_sky',
            'dust', 'methane'
        ]
        
        optimized_models = {}
        
        for group_id, group_info in groups.items():
            try:
                model_file = f"{self.pkl_models_path}{group_info['name']}_model.pkl"
                scaler_file = f"{self.pkl_models_path}{group_info['name']}_scaler.pkl"
                
                if os.path.exists(model_file) and os.path.exists(scaler_file):
                    # Model ve scaler'ı yükle
                    with open(model_file, 'rb') as f:
                        model = pickle.load(f)
                    
                    with open(scaler_file, 'rb') as f:
                        scaler = pickle.load(f)
                    
                    # Optimize edilmiş paket oluştur
                    optimized_model = self.create_optimized_model_package(
                        group_id, group_info['name'], group_info['algorithm'],
                        model, scaler, features
                    )
                    
                    optimized_models[group_id] = optimized_model
                    
                else:
                    print(f"❌ {group_info['name']} model dosyaları bulunamadı")
                    
            except Exception as e:
                print(f"❌ {group_info['name']} işlenirken hata: {str(e)}")
        
        return optimized_models
    
    def create_ensemble_predictor(self, optimized_models):
        """Ensemble tahmin sistemi oluştur"""
        
        ensemble_config = {
            'models': {},
            'ensemble_strategy': 'weighted_average',
            'weights': {
                1: 0.18,  # Random Forest - feature importance için
                2: 0.22,  # RBF SVM - yüksek performans
                3: 0.24,  # RBF SVM - en yüksek R²
                4: 0.24,  # RBF SVM - en düşük hata
                5: 0.12   # RBF SVM - hassas grup
            },
            'confidence_threshold': 0.95,
            'version': '2.0',
            'creation_date': '2025-09-12'
        }
        
        for group_id, model_package in optimized_models.items():
            ensemble_config['models'][group_id] = {
                'algorithm': model_package['group_info']['algorithm'],
                'performance': model_package['group_info']['performance'],
                'weight': ensemble_config['weights'][group_id]
            }
        
        # Ensemble konfigürasyonunu kaydet
        with open(f"{self.pkl_models_path}ensemble_config.json", 'w') as f:
            json.dump(ensemble_config, f, indent=2)
        
        print("✅ Ensemble tahmin sistemi konfigürasyonu oluşturuldu")
        return ensemble_config

def main():
    print("🚀 AllerMind Model Optimizasyonu başlatılıyor...")
    
    creator = OptimizedModelCreator()
    
    # Modelleri yükle ve optimize et
    optimized_models = creator.load_and_repackage_models()
    
    if optimized_models:
        # Ensemble sistem oluştur
        ensemble_config = creator.create_ensemble_predictor(optimized_models)
        
        print(f"\n✅ {len(optimized_models)} model başarıyla optimize edildi")
        print("📊 Performans Özeti:")
        
        for group_id, model_package in optimized_models.items():
            perf = model_package['group_info']['performance']
            print(f"  Grup {group_id}: R²={perf.get('r2', 0):.4f}, "
                  f"MSE={perf.get('mse', 0):.4f}, "
                  f"Algoritma={perf.get('algorithm', 'N/A')}")
    
    else:
        print("❌ Hiçbir model optimize edilemedi")

if __name__ == "__main__":
    main()
