import pandas as pd
import numpy as np
import pickle
import json
from typing import Dict, List, Tuple, Any
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import time
import os
import warnings
warnings.filterwarnings('ignore')

class SVMAllergyPredictor:
    """
    SVM tabanlı allerji tahmin modeli - Random Forest ile karşılaştırma için
    """
    
    def __init__(self):
        self.groups = {
            1: "Şiddetli Alerjik Grup",
            2: "Hafif-Orta Grup", 
            3: "Olası Alerjik Grup/Genetiğinde Olan",
            4: "Henüz Teşhis Almamış/İhtimali Bilinmeyen Grup",
            5: "Alerjisi Olmayan + İhtimali Bilinmeyen Ama Hassas Grup"
        }
        
        # SVM modelleri ve scaler'lar
        self.svm_models = {}
        self.svm_scalers = {}
        self.svm_encoders = {}
        
        # Model konfigürasyonları
        self.svm_configs = {
            'linear': {
                'name': 'Linear SVM',
                'params': {'kernel': 'linear', 'C': 1.0, 'epsilon': 0.1},
                'best_for': 'Basit doğrusal ilişkiler'
            },
            'rbf': {
                'name': 'RBF SVM',
                'params': {'kernel': 'rbf', 'C': 100, 'gamma': 'scale', 'epsilon': 0.1},
                'best_for': 'Karmaşık non-linear ilişkiler'
            },
            'poly': {
                'name': 'Polynomial SVM',
                'params': {'kernel': 'poly', 'degree': 3, 'C': 1.0, 'epsilon': 0.1},
                'best_for': 'Polynomial ilişkiler'
            }
        }
        
        print("🤖 SVM Allerji Tahmin Modeli Oluşturuldu")
        print("=" * 50)
        for key, config in self.svm_configs.items():
            print(f"  {config['name']}: {config['best_for']}")
    
    def load_and_prepare_data(self):
        """Mevcut veriyi yükle ve hazırla"""
        print("\n📊 Veri yükleniyor...")
        
        # Veriyi yükle
        data_path = '/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/cleaned_combined_data.csv'
        self.df = pd.read_csv(data_path)
        print(f"✅ {len(self.df)} satır veri yüklendi")
        
        # Temel özellikleri seç
        self.features = [
            'temperature_2m', 'relative_humidity_2m', 'precipitation',
            'wind_speed_10m', 'pm10', 'pm2_5', 'upi_value', 'plant_upi_value'
        ]
        
        # Kategorik özellikler
        if 'pollen_code' in self.df.columns:
            le = LabelEncoder()
            self.df['pollen_encoded'] = le.fit_transform(self.df['pollen_code'].fillna('UNKNOWN'))
            self.features.append('pollen_encoded')
        
        # NaN değerleri temizle
        for feature in self.features:
            if feature in self.df.columns:
                self.df[feature] = self.df[feature].fillna(self.df[feature].median())
        
        print(f"🔧 {len(self.features)} özellik hazırlandı")
        return True
    
    def create_target_groups(self):
        """5 allerji grubu için hedef değişkenleri oluştur"""
        print("\n🎯 Hedef grupları oluşturuluyor...")
        
        # Normalize edilmiş faktörler
        temp_norm = (self.df['temperature_2m'] - self.df['temperature_2m'].min()) / \
                   (self.df['temperature_2m'].max() - self.df['temperature_2m'].min())
        humidity_norm = self.df['relative_humidity_2m'] / 100
        pm10_norm = self.df['pm10'] / self.df['pm10'].max()
        pm25_norm = self.df['pm2_5'] / self.df['pm2_5'].max()
        upi_norm = self.df['upi_value'] / self.df['upi_value'].max()
        plant_upi_norm = self.df['plant_upi_value'] / self.df['plant_upi_value'].max()
        
        # Grup 1: Şiddetli Alerjik - Polen ve hava kalitesine çok hassas
        self.df['group_1'] = np.clip(
            upi_norm * 0.4 + plant_upi_norm * 0.3 + pm25_norm * 0.2 + temp_norm * 0.1,
            0, 1
        ) * 10
        
        # Grup 2: Hafif-Orta - Dengeli hassasiyet
        self.df['group_2'] = np.clip(
            pm10_norm * 0.35 + pm25_norm * 0.25 + upi_norm * 0.25 + humidity_norm * 0.15,
            0, 1
        ) * 10
        
        # Grup 3: Olası Alerjik - Genetik predispozisyon
        self.df['group_3'] = np.clip(
            upi_norm * 0.35 + temp_norm * 0.25 + humidity_norm * 0.25 + pm10_norm * 0.15,
            0, 1
        ) * 10
        
        # Grup 4: Henüz Teşhis Almamış - Genel hassasiyet
        self.df['group_4'] = np.clip(
            (upi_norm + pm10_norm + pm25_norm + temp_norm) * 0.25,
            0, 1
        ) * 10
        
        # Grup 5: Alerjisi Olmayan ama Hassas - Düşük hassasiyet
        self.df['group_5'] = np.clip(
            temp_norm * 0.3 + humidity_norm * 0.3 + pm10_norm * 0.2 + upi_norm * 0.2,
            0, 1
        ) * 10
        
        print("✅ 5 allerji grubu oluşturuldu")
        
        # İstatistikler
        for i in range(1, 6):
            group_col = f'group_{i}'
            mean_val = self.df[group_col].mean()
            std_val = self.df[group_col].std()
            print(f"  Grup {i}: Ortalama {mean_val:.2f} ± {std_val:.2f}")
    
    def train_svm_models(self, kernel_type='rbf', test_size=0.2):
        """SVM modellerini eğit"""
        print(f"\n🤖 SVM Modelleri Eğitiliyor (Kernel: {kernel_type})...")
        
        config = self.svm_configs[kernel_type]
        results = {}
        
        for group_id in range(1, 6):
            group_name = f"group_{group_id}"
            print(f"\n🎯 Grup {group_id} ({self.groups[group_id]}) eğitiliyor...")
            
            start_time = time.time()
            
            # Veri hazırlama
            X = self.df[self.features].copy()
            y = self.df[group_name].copy()
            
            # NaN temizleme
            mask = ~(X.isnull().any(axis=1) | y.isnull())
            X_clean = X[mask]
            y_clean = y[mask]
            
            if len(X_clean) == 0:
                print(f"⚠️ Grup {group_id} için geçerli veri yok!")
                continue
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X_clean, y_clean, test_size=test_size, random_state=42
            )
            
            # Scaling (SVM için gerekli)
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # SVM modeli
            svm_model = SVR(**config['params'])
            svm_model.fit(X_train_scaled, y_train)
            
            # Tahmin ve metrikler
            y_pred = svm_model.predict(X_test_scaled)
            
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            training_time = time.time() - start_time
            
            # Sonuçları kaydet
            results[group_id] = {
                'model_name': config['name'],
                'r2_score': r2,
                'mse': mse,
                'mae': mae,
                'training_time': training_time,
                'data_points': len(X_clean),
                'test_points': len(X_test)
            }
            
            # Modeli kaydet
            self.svm_models[group_id] = svm_model
            self.svm_scalers[group_id] = scaler
            
            print(f"  ✅ R² Score: {r2:.4f}, MSE: {mse:.4f}, Süre: {training_time:.2f}s")
        
        return results
    
    def save_svm_models(self, kernel_type='rbf'):
        """SVM modellerini kaydet"""
        print(f"\n💾 SVM Modelleri kaydediliyor ({kernel_type})...")
        
        model_dir = f'/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/comparison/svm_{kernel_type}_models'
        os.makedirs(model_dir, exist_ok=True)
        
        for group_id in range(1, 6):
            if group_id in self.svm_models:
                # Model kaydet
                model_path = f'{model_dir}/group_{group_id}_svm_model.pkl'
                with open(model_path, 'wb') as f:
                    pickle.dump(self.svm_models[group_id], f)
                
                # Scaler kaydet
                scaler_path = f'{model_dir}/group_{group_id}_svm_scaler.pkl'
                with open(scaler_path, 'wb') as f:
                    pickle.dump(self.svm_scalers[group_id], f)
        
        print(f"✅ SVM modelleri {model_dir} klasörüne kaydedildi")
    
    def predict_group_risk(self, weather_data: Dict, group_id: int, kernel_type='rbf') -> float:
        """Belirli bir grup için risk tahmini yap"""
        if group_id not in self.svm_models:
            raise ValueError(f"Grup {group_id} için model bulunamadı!")
        
        # Veriyi hazırla
        input_data = []
        for feature in self.features:
            if feature in weather_data:
                input_data.append(weather_data[feature])
            else:
                # Varsayılan değerler
                defaults = {
                    'temperature_2m': 20.0,
                    'relative_humidity_2m': 50.0,
                    'precipitation': 0.0,
                    'wind_speed_10m': 10.0,
                    'pm10': 20.0,
                    'pm2_5': 10.0,
                    'upi_value': 3.0,
                    'plant_upi_value': 2.0,
                    'pollen_encoded': 0
                }
                input_data.append(defaults.get(feature, 0.0))
        
        # Scaling ve tahmin
        input_scaled = self.svm_scalers[group_id].transform([input_data])
        risk_score = self.svm_models[group_id].predict(input_scaled)[0]
        
        return max(0, min(10, risk_score))  # 0-10 arası sınırla

def main():
    """Ana test fonksiyonu"""
    print("🤖 SVM Allerji Tahmin Sistemi")
    print("=" * 50)
    
    # SVM modeli oluştur
    svm_predictor = SVMAllergyPredictor()
    
    # Veriyi yükle
    svm_predictor.load_and_prepare_data()
    
    # Hedef grupları oluştur
    svm_predictor.create_target_groups()
    
    # Her kernel türü için test
    for kernel in ['linear', 'rbf', 'poly']:
        print(f"\n{'='*60}")
        print(f"🧪 {kernel.upper()} KERNEL TEST")
        print(f"{'='*60}")
        
        # Modelleri eğit
        results = svm_predictor.train_svm_models(kernel_type=kernel)
        
        # Modelleri kaydet
        svm_predictor.save_svm_models(kernel_type=kernel)
        
        # Sonuçları göster
        print(f"\n📊 {kernel.upper()} Kernel Sonuçları:")
        for group_id, metrics in results.items():
            print(f"  Grup {group_id}: R²={metrics['r2_score']:.4f}, MSE={metrics['mse']:.4f}")

if __name__ == "__main__":
    main()
