#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALLERMIND V2.0 - EXPERT-LEVEL MODEL CREATOR
İstatistiksel olarak optimize edilmiş 5-grup alerji tahmin sistemi
Kişisel ağırlık parametresi dahil gelişmiş makine öğrenmesi yaklaşımı
"""

import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from sklearn.preprocessing import LabelEncoder, StandardScaler, RobustScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, TimeSeriesSplit, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import ElasticNet, Ridge, Lasso, BayesianRidge
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class ExpertAllermindModelCreator:
    """Expert-level istatistiksel model creator"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.processed_data = None
        self.label_encoders = {}
        self.scalers = {}
        self.models = {}
        self.feature_importance = {}
        
        # 5 Alerji Grubu Tanımları (İstatistiksel Ağırlıklar ile)
        self.allergy_groups = {
            1: {
                'name': 'Polen Hassasiyeti Grubu',
                'description': 'Ağaç, çimen ve yabani ot poleni hassasiyeti',
                'primary_features': ['pollen_code', 'plant_code', 'upi_value', 'plant_upi_value', 
                                   'wind_speed_10m', 'wind_direction_10m', 'relative_humidity_2m'],
                'target_weight_factors': {
                    'upi_value': 0.4, 'plant_upi_value': 0.3, 'wind_speed_10m': 0.15,
                    'relative_humidity_2m': 0.1, 'temperature_2m': 0.05
                },
                'algorithm': 'RandomForest',
                'algorithm_params': {'n_estimators': 200, 'max_depth': 15, 'min_samples_split': 5}
            },
            2: {
                'name': 'Hava Kirliliği Hassasiyeti Grubu',
                'description': 'PM, NO2, Ozon hassasiyeti',
                'primary_features': ['pm10', 'pm2_5', 'nitrogen_dioxide', 'ozone', 'carbon_monoxide',
                                   'sulphur_dioxide', 'aerosol_optical_depth'],
                'target_weight_factors': {
                    'pm10': 0.25, 'pm2_5': 0.25, 'nitrogen_dioxide': 0.2, 'ozone': 0.15,
                    'carbon_monoxide': 0.1, 'sulphur_dioxide': 0.05
                },
                'algorithm': 'GradientBoosting',
                'algorithm_params': {'n_estimators': 150, 'learning_rate': 0.05, 'max_depth': 8}
            },
            3: {
                'name': 'UV ve Güneş Hassasiyeti Grubu',
                'description': 'UV indeksi ve güneş ışığı hassasiyeti',
                'primary_features': ['uv_index', 'uv_index_clear_sky', 'sunshine_duration', 
                                   'cloud_cover', 'temperature_2m'],
                'target_weight_factors': {
                    'uv_index': 0.4, 'uv_index_clear_sky': 0.25, 'sunshine_duration': 0.2,
                    'cloud_cover': 0.1, 'temperature_2m': 0.05
                },
                'algorithm': 'SVR',
                'algorithm_params': {'C': 100, 'gamma': 'scale', 'kernel': 'rbf'}
            },
            4: {
                'name': 'Meteorolojik Hassasiyet Grubu',
                'description': 'Basınç, nem, rüzgar değişimleri hassasiyeti',
                'primary_features': ['surface_pressure', 'relative_humidity_2m', 'wind_speed_10m',
                                   'precipitation', 'rain', 'cloud_cover'],
                'target_weight_factors': {
                    'surface_pressure': 0.3, 'relative_humidity_2m': 0.25, 'wind_speed_10m': 0.2,
                    'precipitation': 0.15, 'cloud_cover': 0.1
                },
                'algorithm': 'ExtraTrees',
                'algorithm_params': {'n_estimators': 180, 'max_depth': 12, 'min_samples_split': 4}
            },
            5: {
                'name': 'Hassas Grup (Çocuk/Yaşlı)',
                'description': 'Tüm çevresel faktörlere yüksek hassasiyet',
                'primary_features': ['pm10', 'pm2_5', 'uv_index', 'temperature_2m', 'ozone',
                                   'upi_value', 'relative_humidity_2m', 'wind_speed_10m'],
                'target_weight_factors': {
                    'pm10': 0.2, 'pm2_5': 0.2, 'uv_index': 0.15, 'temperature_2m': 0.15,
                    'ozone': 0.1, 'upi_value': 0.1, 'relative_humidity_2m': 0.05, 'wind_speed_10m': 0.05
                },
                'algorithm': 'NeuralNetwork',
                'algorithm_params': {'hidden_layer_sizes': (100, 50, 25), 'max_iter': 500, 'alpha': 0.001}
            }
        }
    
    def load_and_preprocess_data(self):
        """Veriyi yükle ve ön işleme"""
        
        print("📊 VERİ YÜKLEME VE ÖN İŞLEME")
        print("=" * 50)
        
        # Veri yükleme
        print("📁 Veri yükleniyor...")
        self.df = pd.read_csv(self.data_path)
        print(f"✅ Veri yüklendi: {self.df.shape[0]:,} satır, {self.df.shape[1]} kolon")
        
        # Tarih parsing
        self.df['time'] = pd.to_datetime(self.df['time'])
        self.df['hour'] = self.df['time'].dt.hour
        self.df['day_of_week'] = self.df['time'].dt.dayofweek
        
        # Eksik değer analizi
        print("\n🔍 Eksik değer işleme...")
        missing_before = self.df.isnull().sum().sum()
        
        # Kritik hava kalitesi verilerini interpolate et
        air_quality_cols = ['pm10', 'pm2_5', 'nitrogen_dioxide', 'ozone', 'carbon_monoxide']
        for col in air_quality_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].interpolate(method='linear')
                self.df[col] = self.df[col].fillna(self.df[col].median())
        
        # Polen verilerini forward fill
        pollen_cols = ['pollen_code', 'in_season', 'upi_value', 'plant_code', 'plant_in_season', 'plant_upi_value']
        for col in pollen_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(method='ffill')
                self.df[col] = self.df[col].fillna(method='bfill')
        
        # Kategorik encoding
        print("\n🏷️ Kategorik değişken encoding...")
        categorical_cols = ['pollen_code', 'plant_code']
        for col in categorical_cols:
            if col in self.df.columns:
                le = LabelEncoder()
                self.df[col] = self.df[col].astype(str)
                self.df[col] = le.fit_transform(self.df[col])
                self.label_encoders[col] = le
        
        # Boolean kolonları numeric'e çevir
        bool_cols = ['in_season', 'plant_in_season']
        for col in bool_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(int)
        
        missing_after = self.df.isnull().sum().sum()
        print(f"✅ Eksik değer azaltıldı: {missing_before:,} → {missing_after:,}")
        
        # Feature engineering
        print("\n⚙️ Feature engineering...")
        self.create_engineered_features()
        
        print(f"✅ İşlenmiş veri boyutu: {self.df.shape}")
        
    def create_engineered_features(self):
        """Gelişmiş feature engineering"""
        
        # Air Quality Index (AQI) calculation
        if all(col in self.df.columns for col in ['pm10', 'pm2_5', 'ozone', 'nitrogen_dioxide']):
            pm10_filled = self.df['pm10'].fillna(self.df['pm10'].median())
            pm25_filled = self.df['pm2_5'].fillna(self.df['pm2_5'].median())
            ozone_filled = self.df['ozone'].fillna(self.df['ozone'].median())
            no2_filled = self.df['nitrogen_dioxide'].fillna(self.df['nitrogen_dioxide'].median())
            self.df['aqi_combined'] = (
                pm10_filled * 0.3 + 
                pm25_filled * 0.4 + 
                ozone_filled * 0.2 + 
                no2_filled * 0.1
            )
        
        # Pollen risk index
        if all(col in self.df.columns for col in ['upi_value', 'plant_upi_value', 'wind_speed_10m']):
            upi_filled = self.df['upi_value'].fillna(0)
            plant_upi_filled = self.df['plant_upi_value'].fillna(0)
            wind_filled = self.df['wind_speed_10m'].fillna(0)
            self.df['pollen_risk_index'] = (
                upi_filled * 0.5 + 
                plant_upi_filled * 0.3 + 
                (wind_filled / 20) * 0.2  # Normalize wind
            )
        
        # Comfort index
        if all(col in self.df.columns for col in ['temperature_2m', 'relative_humidity_2m', 'wind_speed_10m']):
            # Heat index approximation
            temp_c = self.df['temperature_2m'].fillna(20)  # Default 20°C
            humidity = self.df['relative_humidity_2m'].fillna(50)  # Default 50%
            wind = self.df['wind_speed_10m'].fillna(5)  # Default 5 m/s
            self.df['comfort_index'] = (
                temp_c - 
                (0.55 - 0.0055 * humidity) * (temp_c - 14.5) - 
                wind * 0.16
            )
        
        # UV danger level
        if 'uv_index' in self.df.columns:
            uv_filled = self.df['uv_index'].fillna(0)
            self.df['uv_danger_level'] = pd.cut(
                uv_filled, 
                bins=[-1, 2, 5, 7, 10, 15], 
                labels=[0, 1, 2, 3, 4]
            ).astype(int)
        
        # Time-based features
        self.df['is_peak_pollen_hour'] = ((self.df['hour'] >= 6) & (self.df['hour'] <= 10)).astype(int)
        self.df['is_weekend'] = (self.df['day_of_week'] >= 5).astype(int)
        
        print(f"✅ {len([c for c in self.df.columns if c.endswith('_index') or c.startswith('is_')])} yeni feature oluşturuldu")
    
    def create_group_targets(self, group_id):
        """Grup-spesifik hedef değişken oluştur"""
        
        group_info = self.allergy_groups[group_id]
        target_factors = group_info['target_weight_factors']
        
        # Weighted target calculation
        target_components = []
        weights = []
        
        for feature, weight in target_factors.items():
            if feature in self.df.columns:
                # Normalize feature to 0-1 range
                feature_data = self.df[feature].fillna(self.df[feature].median())
                normalized = (feature_data - feature_data.min()) / (feature_data.max() - feature_data.min() + 1e-8)
                target_components.append(normalized * weight)
                weights.append(weight)
        
        if target_components:
            # Create composite target (0-1 risk score)
            target = sum(target_components) / sum(weights)
            
            # Convert to "safe outdoor hours" (inverse relationship)
            # High risk = fewer safe hours
            safe_hours = 8 * (1 - target.clip(0, 1)) + 0.5  # 0.5-8.5 hours range
            
            return target.clip(0, 1), safe_hours.clip(0.5, 8.5)
        else:
            print(f"⚠️ Grup {group_id} için yeterli feature bulunamadı")
            return None, None
    
    def create_model_for_group(self, group_id):
        """Grup-spesifik model oluştur"""
        
        print(f"\n🤖 GRUP {group_id} MODEL OLUŞTURULUYOR")
        print(f"📋 {self.allergy_groups[group_id]['name']}")
        print("-" * 50)
        
        group_info = self.allergy_groups[group_id]
        
        # Target değişken oluştur
        risk_target, hours_target = self.create_group_targets(group_id)
        
        if risk_target is None:
            print(f"❌ Grup {group_id} için target oluşturulamadı")
            return None
        
        # Features seç
        primary_features = group_info['primary_features']
        available_features = [f for f in primary_features if f in self.df.columns]
        
        # Engineered features da ekle
        engineered_cols = [c for c in self.df.columns if c.endswith('_index') or c.startswith('is_') or c == 'aqi_combined']
        available_features.extend(engineered_cols)
        
        # Location ve time features
        available_features.extend(['lat', 'lon', 'hour', 'day_of_week'])
        
        # Duplicate removal
        available_features = list(set(available_features))
        available_features = [f for f in available_features if f in self.df.columns]
        
        print(f"✅ {len(available_features)} feature seçildi")
        
        # Data preparation
        X = self.df[available_features].fillna(self.df[available_features].median())
        y = hours_target  # Safe hours as target
        
        # Train-test split (time-aware)
        split_date = self.df['time'].quantile(0.8)
        train_mask = self.df['time'] <= split_date
        
        X_train, X_test = X[train_mask], X[~train_mask]
        y_train, y_test = y[train_mask], y[~train_mask]
        
        print(f"📊 Train: {len(X_train):,}, Test: {len(X_test):,}")
        
        # Feature scaling
        scaler = RobustScaler()  # Robust to outliers
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Model seçimi ve eğitimi
        algorithm = group_info['algorithm']
        params = group_info['algorithm_params']
        
        print(f"🔧 Algoritma: {algorithm}")
        
        if algorithm == 'RandomForest':
            model = RandomForestRegressor(**params, random_state=42, n_jobs=-1)
        elif algorithm == 'GradientBoosting':
            model = GradientBoostingRegressor(**params, random_state=42)
        elif algorithm == 'SVR':
            model = SVR(**params)
        elif algorithm == 'ExtraTrees':
            model = ExtraTreesRegressor(**params, random_state=42, n_jobs=-1)
        elif algorithm == 'NeuralNetwork':
            model = MLPRegressor(**params, random_state=42)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # Model training
        print("🎯 Model eğitiliyor...")
        if algorithm == 'SVR' or algorithm == 'NeuralNetwork':
            model.fit(X_train_scaled, y_train)
            y_pred_train = model.predict(X_train_scaled)
            y_pred_test = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
        
        # Performance evaluation
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        
        print(f"📈 PERFORMANS SONUÇLARI:")
        print(f"   Train R²: {train_r2:.4f}")
        print(f"   Test R²: {test_r2:.4f}")
        print(f"   Train MAE: {train_mae:.4f}")
        print(f"   Test MAE: {test_mae:.4f}")
        print(f"   Overfitting Gap: {abs(train_r2 - test_r2):.4f}")
        
        # Feature importance
        if hasattr(model, 'feature_importances_'):
            feature_imp = dict(zip(available_features, model.feature_importances_))
            top_features = sorted(feature_imp.items(), key=lambda x: x[1], reverse=True)[:10]
            print(f"🔝 En önemli 5 feature:")
            for i, (feat, imp) in enumerate(top_features[:5], 1):
                print(f"   {i}. {feat}: {imp:.4f}")
        
        # Model package oluştur
        model_package = {
            'model': model,
            'scaler': scaler,
            'features': available_features,
            'group_info': group_info,
            'performance': {
                'train_r2': train_r2,
                'test_r2': test_r2,
                'train_mae': train_mae,
                'test_mae': test_mae,
                'overfitting_gap': abs(train_r2 - test_r2)
            },
            'target_info': {
                'target_type': 'safe_outdoor_hours',
                'min_hours': y.min(),
                'max_hours': y.max(),
                'mean_hours': y.mean()
            },
            'feature_importance': feature_imp if hasattr(model, 'feature_importances_') else None,
            'created_at': datetime.now().isoformat(),
            'algorithm_used': algorithm,
            'scaling_method': 'RobustScaler'
        }
        
        # Kişisel ağırlık sistemi ekle
        model_package['personal_weight_system'] = self.create_personal_weight_system(group_id)
        
        return model_package
    
    def create_personal_weight_system(self, group_id):
        """Kişisel ağırlık parametresi sistemi"""
        
        return {
            'weight_factors': {
                'age_factor': {
                    'child': {'multiplier': 1.5, 'description': 'Çocuklar için arttırılmış hassasiyet'},
                    'adult': {'multiplier': 1.0, 'description': 'Standart yetişkin hassasiyeti'},
                    'elderly': {'multiplier': 1.3, 'description': 'Yaşlılar için arttırılmış hassasiyet'}
                },
                'medical_condition': {
                    'asthma': {'multiplier': 1.4, 'description': 'Astım hastası ekstra hassasiyet'},
                    'allergy': {'multiplier': 1.2, 'description': 'Alerji hastası ekstra hassasiyet'},
                    'healthy': {'multiplier': 1.0, 'description': 'Sağlıklı birey standart hassasiyet'}
                },
                'activity_level': {
                    'high': {'multiplier': 1.2, 'description': 'Yüksek aktivite - daha fazla soluma'},
                    'moderate': {'multiplier': 1.0, 'description': 'Orta aktivite - standart'},
                    'low': {'multiplier': 0.9, 'description': 'Düşük aktivite - daha az etki'}
                },
                'sensitivity_level': {
                    'very_high': {'multiplier': 1.6, 'description': 'Çok yüksek hassasiyet'},
                    'high': {'multiplier': 1.3, 'description': 'Yüksek hassasiyet'},
                    'moderate': {'multiplier': 1.0, 'description': 'Orta hassasiyet'},
                    'low': {'multiplier': 0.8, 'description': 'Düşük hassasiyet'}
                }
            },
            'calculation_formula': 'base_prediction * age_factor * medical_condition * activity_level * sensitivity_level',
            'group_specific_adjustments': self.allergy_groups[group_id]['target_weight_factors']
        }
    
    def save_model(self, model_package, group_id):
        """Model ve tüm bilgileri kaydet"""
        
        filename = f"Grup{group_id}_advanced_model_v2.pkl"
        filepath = f"/Users/elifdy/Desktop/allermind/aller-mind/DATA/MODEL/version2_pkl_models/{filename}"
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_package, f)
        
        print(f"✅ Model kaydedildi: {filename}")
        return filepath
    
    def create_all_models(self):
        """Tüm 5 grup için model oluştur"""
        
        print("🚀 ALLERMIND V2.0 - EXPERT MODEL CREATION")
        print("=" * 60)
        
        # Veri hazırlama
        self.load_and_preprocess_data()
        
        # Her grup için model oluştur
        created_models = {}
        
        for group_id in range(1, 6):
            try:
                model_package = self.create_model_for_group(group_id)
                if model_package:
                    filepath = self.save_model(model_package, group_id)
                    created_models[group_id] = filepath
                    print(f"✅ Grup {group_id} başarıyla oluşturuldu")
                else:
                    print(f"❌ Grup {group_id} oluşturulamadı")
            except Exception as e:
                print(f"❌ Grup {group_id} hatası: {str(e)}")
        
        # Ensemble config oluştur
        ensemble_config = {
            'version': '2.0',
            'created_at': datetime.now().isoformat(),
            'models': created_models,
            'groups': self.allergy_groups,
            'data_info': {
                'total_samples': len(self.df),
                'feature_count': len([c for c in self.df.columns if c not in ['time', 'lat', 'lon']]),
                'date_range': f"{self.df['time'].min()} - {self.df['time'].max()}"
            }
        }
        
        config_path = "/Users/elifdy/Desktop/allermind/aller-mind/DATA/MODEL/version2_pkl_models/ensemble_config_v2.json"
        with open(config_path, 'w') as f:
            json.dump(ensemble_config, f, indent=2, default=str)
        
        print(f"\n🎉 TÜM MODELLER OLUŞTURULDU!")
        print(f"   Başarılı: {len(created_models)}/5")
        print(f"   Ensemble config: ensemble_config_v2.json")
        
        return created_models, ensemble_config

def main():
    """Ana fonksiyon"""
    
    data_path = "/Users/elifdy/Desktop/allermind/aller-mind/DATA/11SEP/20250911_combined_all_data.csv"
    
    creator = ExpertAllermindModelCreator(data_path)
    created_models, config = creator.create_all_models()
    
    print(f"\n📊 MODEL ÖZET RAPORU:")
    print(f"   Oluşturulan model sayısı: {len(created_models)}")
    print(f"   Veri boyutu: {creator.df.shape if creator.df is not None else 'N/A'}")
    print(f"   Oluşturma tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()