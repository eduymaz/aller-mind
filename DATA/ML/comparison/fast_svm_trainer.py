import pandas as pd
import numpy as np
import pickle
import json
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import time
import os
import warnings
warnings.filterwarnings('ignore')

class FastSVMTrainer:
    """
    Hızlı SVM eğitim sınıfı - sample data ile optimize edilmiş
    """
    
    def __init__(self, sample_size=5000):
        self.sample_size = sample_size
        self.groups = {
            1: "Şiddetli Alerjik Grup",
            2: "Hafif-Orta Grup", 
            3: "Olası Alerjik Grup/Genetiğinde Olan",
            4: "Henüz Teşhis Almamış/İhtimali Bilinmeyen Grup",
            5: "Alerjisi Olmayan + İhtimali Bilinmeyen Ama Hassas Grup"
        }
        
        # Basit SVM konfigürasyonları (GridSearch yok!)
        self.svm_configs = {
            'linear': {
                'name': 'Linear SVM',
                'model': SVR(kernel='linear', C=1.0, epsilon=0.1)
            },
            'rbf': {
                'name': 'RBF SVM', 
                'model': SVR(kernel='rbf', C=100, gamma='scale', epsilon=0.1)
            }
        }
        
        self.results = {}
        
    def load_data_fast(self):
        """Veriyi hızlı yükle ve sample al"""
        print(f"📊 Veri yükleniyor (sample size: {self.sample_size})...")
        
        try:
            # Ana veriyi yükle
            df = pd.read_csv('/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/cleaned_combined_data.csv')
            print(f"✅ Toplam veri: {len(df)} satır")
            
            # Sample al (hızlı test için)
            if len(df) > self.sample_size:
                df_sample = df.sample(n=self.sample_size, random_state=42)
                print(f"📉 Sample alındı: {len(df_sample)} satır")
            else:
                df_sample = df.copy()
            
            return df_sample
            
        except Exception as e:
            print(f"❌ Veri yükleme hatası: {e}")
            return None
    
    def prepare_features_fast(self, df):
        """Özellikleri hızlı hazırla"""
        print("🔧 Özellikler hazırlanıyor...")
        
        # Temel numerik özellikler
        numeric_features = [
            'temperature_2m', 'relative_humidity_2m', 'wind_speed_10m',
            'pm10', 'pm2_5', 'upi_value', 'plant_upi_value'
        ]
        
        # Mevcut olan özellikleri filtrele
        available_features = [col for col in numeric_features if col in df.columns]
        
        # Kategorik encoding (basit)
        if 'pollen_code' in df.columns:
            df['pollen_encoded'] = df['pollen_code'].map({
                'GRASS': 0, 'TREE': 1, 'WEED': 2
            }).fillna(0)
            available_features.append('pollen_encoded')
        
        print(f"✅ {len(available_features)} özellik hazırlandı")
        return available_features
    
    def train_svm_fast(self, df, features):
        """Her grup için hızlı SVM eğitimi"""
        print(f"\n🚀 Hızlı SVM Eğitimi Başlıyor...")
        print("=" * 50)
        
        results = {}
        
        for group_id in range(1, 6):
            group_col = f'group_{group_id}'
            
            if group_col not in df.columns:
                print(f"⚠️ {group_col} kolonu bulunamadı!")
                continue
                
            print(f"\n🎯 {self.groups[group_id]} eğitiliyor...")
            start_time = time.time()
            
            # Veriyi hazırla
            X = df[features].copy()
            y = df[group_col].copy()
            
            # NaN temizle
            mask = ~(X.isnull().any(axis=1) | y.isnull())
            X_clean = X[mask]
            y_clean = y[mask]
            
            if len(X_clean) == 0:
                print(f"❌ {group_col} için geçerli veri yok!")
                continue
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X_clean, y_clean, test_size=0.2, random_state=42
            )
            
            # Scaling
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            group_results = {}
            
            # Her SVM tipi için eğit (GridSearch YOK!)
            for svm_type, config in self.svm_configs.items():
                print(f"  📈 {config['name']} eğitiliyor...", end=' ')
                
                model_start = time.time()
                
                # Model eğit
                model = config['model']
                model.fit(X_train_scaled, y_train)
                
                # Tahmin et
                y_pred = model.predict(X_test_scaled)
                
                # Metrikleri hesapla
                r2 = r2_score(y_test, y_pred)
                mse = mean_squared_error(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                
                model_time = time.time() - model_start
                
                group_results[svm_type] = {
                    'r2_score': r2,
                    'mse': mse,
                    'mae': mae,
                    'training_time': model_time,
                    'model': model,
                    'scaler': scaler
                }
                
                print(f"R²: {r2:.4f} ({model_time:.1f}s)")
            
            # En iyi modeli seç
            best_svm = max(group_results.keys(), key=lambda x: group_results[x]['r2_score'])
            best_r2 = group_results[best_svm]['r2_score']
            
            results[group_id] = {
                'best_svm_type': best_svm,
                'best_r2': best_r2,
                'results': group_results,
                'group_name': self.groups[group_id]
            }
            
            total_time = time.time() - start_time
            print(f"  🏆 En iyi: {self.svm_configs[best_svm]['name']} (R²: {best_r2:.4f})")
            print(f"  ⏱️ Toplam süre: {total_time:.1f}s")
        
        return results
    
    def compare_with_rf(self, df, features):
        """Random Forest ile karşılaştır"""
        print(f"\n🌲 Random Forest ile Karşılaştırma")
        print("=" * 50)
        
        rf_results = {}
        
        for group_id in range(1, 6):
            group_col = f'group_{group_id}'
            
            if group_col not in df.columns:
                continue
                
            print(f"\n🎯 Grup {group_id} - Random Forest...")
            
            # Veriyi hazırla
            X = df[features].copy()
            y = df[group_col].copy()
            
            # NaN temizle
            mask = ~(X.isnull().any(axis=1) | y.isnull())
            X_clean = X[mask]
            y_clean = y[mask]
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X_clean, y_clean, test_size=0.2, random_state=42
            )
            
            # Random Forest eğit
            start_time = time.time()
            rf_model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
            rf_model.fit(X_train, y_train)
            
            # Tahmin et
            y_pred = rf_model.predict(X_test)
            
            # Metrikleri hesapla
            r2 = r2_score(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            training_time = time.time() - start_time
            
            rf_results[group_id] = {
                'r2_score': r2,
                'mse': mse,
                'mae': mae,
                'training_time': training_time
            }
            
            print(f"  📊 Random Forest: R² = {r2:.4f} ({training_time:.1f}s)")
        
        return rf_results
    
    def display_comparison_results(self, svm_results, rf_results):
        """Karşılaştırma sonuçlarını göster"""
        print(f"\n" + "="*80)
        print("🏆 SVM vs RANDOM FOREST KARŞILAŞTIRMA SONUÇLARI")
        print("="*80)
        
        svm_wins = 0
        rf_wins = 0
        
        for group_id in range(1, 6):
            if group_id not in svm_results or group_id not in rf_results:
                continue
                
            print(f"\n📊 GRUP {group_id}: {svm_results[group_id]['group_name']}")
            print("-" * 60)
            
            # SVM en iyi sonucu
            best_svm_type = svm_results[group_id]['best_svm_type']
            svm_r2 = svm_results[group_id]['best_r2']
            svm_name = self.svm_configs[best_svm_type]['name']
            
            # Random Forest sonucu
            rf_r2 = rf_results[group_id]['r2_score']
            
            print(f"  🤖 En İyi SVM ({svm_name}): R² = {svm_r2:.4f}")
            print(f"  🌲 Random Forest: R² = {rf_r2:.4f}")
            
            # Kazanan
            if svm_r2 > rf_r2:
                winner = "SVM"
                svm_wins += 1
                improvement = ((svm_r2 - rf_r2) / rf_r2) * 100
                print(f"  🏆 Kazanan: SVM (+{improvement:.1f}% daha iyi)")
            else:
                winner = "Random Forest"
                rf_wins += 1
                improvement = ((rf_r2 - svm_r2) / svm_r2) * 100
                print(f"  🏆 Kazanan: Random Forest (+{improvement:.1f}% daha iyi)")
        
        # Genel özet
        print(f"\n" + "="*50)
        print("📈 GENEL ÖZET")
        print("="*50)
        print(f"🤖 SVM kazandığı gruplar: {svm_wins}")
        print(f"🌲 Random Forest kazandığı gruplar: {rf_wins}")
        
        if svm_wins > rf_wins:
            print(f"\n🏆 GENEL KAZANAN: SVM")
            print(f"💡 SVM, {svm_wins}/{svm_wins + rf_wins} grupta daha iyi performans gösterdi.")
        elif rf_wins > svm_wins:
            print(f"\n🏆 GENEL KAZANAN: Random Forest")
            print(f"💡 Random Forest, {rf_wins}/{svm_wins + rf_wins} grupta daha iyi performans gösterdi.")
        else:
            print(f"\n🤝 BERABERE!")
    
    def save_best_svm_models(self, svm_results, features):
        """En iyi SVM modellerini kaydet"""
        print(f"\n💾 En iyi SVM modelleri kaydediliyor...")
        
        # SVM modelleri için klasörler oluştur
        os.makedirs('svm_linear_models', exist_ok=True)
        os.makedirs('svm_rbf_models', exist_ok=True)
        
        for group_id, result in svm_results.items():
            best_type = result['best_svm_type']
            best_model = result['results'][best_type]['model']
            best_scaler = result['results'][best_type]['scaler']
            
            # Model kaydet
            model_dir = f'svm_{best_type}_models'
            model_path = f'{model_dir}/group_{group_id}_svm_model.pkl'
            scaler_path = f'{model_dir}/group_{group_id}_svm_scaler.pkl'
            
            with open(model_path, 'wb') as f:
                pickle.dump(best_model, f)
            with open(scaler_path, 'wb') as f:
                pickle.dump(best_scaler, f)
            
            print(f"  ✅ Grup {group_id}: {self.svm_configs[best_type]['name']} kaydedildi")
        
        # Özellik listesini kaydet
        with open('svm_features.json', 'w') as f:
            json.dump(features, f)
        
        print("💾 Tüm SVM modelleri kaydedildi!")

def main():
    """Ana fonksiyon - Hızlı SVM eğitimi ve karşılaştırma"""
    print("🔬 AllerMind - Hızlı SVM vs Random Forest Karşılaştırması")
    print("=" * 60)
    
    # Trainer oluştur (küçük sample ile)
    trainer = FastSVMTrainer(sample_size=3000)  # Hızlı test için
    
    # Veriyi yükle
    df = trainer.load_data_fast()
    if df is None:
        return
    
    # Özellikleri hazırla
    features = trainer.prepare_features_fast(df)
    
    # SVM'leri eğit
    svm_results = trainer.train_svm_fast(df, features)
    
    # Random Forest ile karşılaştır
    rf_results = trainer.compare_with_rf(df, features)
    
    # Sonuçları göster
    trainer.display_comparison_results(svm_results, rf_results)
    
    # En iyi modelleri kaydet
    trainer.save_best_svm_models(svm_results, features)
    
    print(f"\n✅ Hızlı karşılaştırma tamamlandı!")

if __name__ == "__main__":
    main()
