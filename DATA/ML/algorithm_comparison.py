import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import time
import warnings
warnings.filterwarnings('ignore')

class ProgressBar:
    """İlerleme takibi için progress bar"""
    
    def __init__(self, total_steps, task_name="İşlem"):
        self.total_steps = total_steps
        self.current_step = 0
        self.task_name = task_name
        self.start_time = time.time()
        print(f"\n🚀 {self.task_name} başladı...")
    
    def update(self, step_name=""):
        """Bir adım ilerle"""
        self.current_step += 1
        progress_percent = (self.current_step / self.total_steps) * 100
        
        # Kalan süre tahmini
        elapsed_time = time.time() - self.start_time
        if self.current_step > 0:
            eta = (elapsed_time / self.current_step) * (self.total_steps - self.current_step)
            eta_str = f" (Kalan: {eta:.1f}s)"
        else:
            eta_str = ""
        
        # Progress bar çizimi
        bar_length = 30
        filled_length = int(bar_length * self.current_step / self.total_steps)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        print(f"\r[{bar}] {progress_percent:.1f}% {step_name}{eta_str}", end='', flush=True)
    
    def finish(self):
        """İşlem tamamlandı"""
        elapsed_time = time.time() - self.start_time
        print(f"\n✅ {self.task_name} tamamlandı! ({elapsed_time:.2f}s)")

class AlgorithmComparison:
    """Random Forest vs SVM karşılaştırma sınıfı"""
    
    def __init__(self, sample_size=5000):
        """Hızlı karşılaştırma için optimize edilmiş init"""
        self.sample_size = sample_size
        self.df = None
        self.features = []
        self.data_loaded = False
        
        # Basitleştirilmiş algoritma configs
        self.algorithms = {
            'random_forest': {
                'name': 'Random Forest Regressor',
                'model': RandomForestRegressor,
                'params': {
                    'n_estimators': 50,
                    'random_state': 42,
                    'n_jobs': -1
                },
                'needs_scaling': False
            },
            'svm_rbf': {
                'name': 'Support Vector Machine (RBF)',
                'model': SVR,
                'params': {
                    'kernel': 'rbf',
                    'C': 100,
                    'gamma': 'scale',
                    'epsilon': 0.1
                },
                'needs_scaling': True
            }
        }
        
    def load_data(self):
        """Veriyi hızlı yükle"""
        print("\n📊 Veri yükleniyor...")
        progress = ProgressBar(3, "Veri Yükleme")
        
        try:
            data_path = '/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/cleaned_combined_data.csv'
            progress.update("Dosya okunuyor...")
            
            self.df = pd.read_csv(data_path)
            progress.update("Veri işleniyor...")
            
            print(f"\n✅ Veri yüklendi: {self.df.shape[0]} satır, {self.df.shape[1]} kolon")
            self.data_loaded = True
            progress.update("Tamamlandı")
            progress.finish()
            
            return True
            
        except Exception as e:
            print(f"\n❌ Veri yükleme hatası: {e}")
            return False
    
    def prepare_features_fast(self):
        """Özellikleri hızlı hazırla"""
        print("\n🔧 Özellikler hazırlanıyor...")
        progress = ProgressBar(4, "Özellik Hazırlama")
        
        # En önemli numerik özellikler
        self.features = [
            'temperature_2m', 'relative_humidity_2m', 'wind_speed_10m',
            'pm10', 'pm2_5', 'upi_value', 'plant_upi_value'
        ]
        progress.update("Özellikler seçiliyor...")
        
        # Mevcut kolonları kontrol et
        available_features = [col for col in self.features if col in self.df.columns]
        progress.update("Kolonlar kontrol ediliyor...")
        
        # Kategorik encode (hızlı)
        if 'pollen_code' in self.df.columns:
            self.df['pollen_encoded'] = self.df['pollen_code'].map({
                'GRASS': 0, 'TREE': 1, 'WEED': 2
            }).fillna(0)
            available_features.append('pollen_encoded')
        progress.update("Encoding tamamlandı...")
        
        self.features = available_features
        print(f"\n✅ {len(self.features)} özellik hazırlandı")
        progress.update("Tamamlandı")
        progress.finish()
        
        return self.features
    
    def compare_algorithms(self, target_groups=['group_1', 'group_2', 'group_3', 'group_4', 'group_5']):
        """Algoritmaları karşılaştır"""
        print(f"\n🆚 Random Forest vs SVM Karşılaştırması")
        print(f"📊 Örnek boyutu: {self.sample_size}")
        print(f"🎯 Hedef gruplar: {len(target_groups)}")
        
        # Veri hazırlık
        if not self.data_loaded:
            if not self.load_data():
                return None
        
        self.prepare_features_fast()
        
        # Sample data for faster processing
        if len(self.df) > self.sample_size:
            sample_df = self.df.sample(n=self.sample_size, random_state=42)
            print(f"\n📉 Veri örneklendi: {len(sample_df)} satır")
        else:
            sample_df = self.df.copy()
        
        # Genel karşılaştırma
        total_steps = len(target_groups) * len(self.algorithms)
        main_progress = ProgressBar(total_steps, "Algoritma Karşılaştırması")
        
        results = {}
        
        for group in target_groups:
            if group not in sample_df.columns:
                print(f"\n⚠️ {group} kolonu bulunamadı, atlanıyor...")
                continue
            
            results[group] = {}
            
            # Veri hazırlama
            X = sample_df[self.features]
            y = sample_df[group]
            
            # NaN değerleri temizle
            mask = ~(X.isnull().any(axis=1) | y.isnull())
            X_clean = X[mask]
            y_clean = y[mask]
            
            if len(X_clean) == 0:
                print(f"\n⚠️ {group} için geçerli veri yok, atlanıyor...")
                continue
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X_clean, y_clean, test_size=0.2, random_state=42
            )
            
            # Her algoritma için test
            for alg_name, alg_config in self.algorithms.items():
                try:
                    start_time = time.time()
                    
                    # Model oluştur
                    model = alg_config['model'](**alg_config['params'])
                    
                    # Scaling gerekiyorsa
                    if alg_config['needs_scaling']:
                        scaler = StandardScaler()
                        X_train_scaled = scaler.fit_transform(X_train)
                        X_test_scaled = scaler.transform(X_test)
                        
                        model.fit(X_train_scaled, y_train)
                        y_pred = model.predict(X_test_scaled)
                    else:
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_test)
                    
                    # Metrikleri hesapla
                    mse = mean_squared_error(y_test, y_pred)
                    r2 = r2_score(y_test, y_pred)
                    mae = mean_absolute_error(y_test, y_pred)
                    training_time = time.time() - start_time
                    
                    results[group][alg_name] = {
                        'r2_score': r2,
                        'mse': mse,
                        'mae': mae,
                        'training_time': training_time,
                        'model_name': alg_config['name']
                    }
                    
                    main_progress.update(f"{group} - {alg_config['name']}")
                    
                except Exception as e:
                    print(f"\n❌ {group} - {alg_name} hatası: {e}")
                    main_progress.update(f"{group} - HATA")
        
        main_progress.finish()
        
        # Sonuçları göster
        self._display_comparison_results(results)
        
        return results
    
    def _display_comparison_results(self, results):
        """Karşılaştırma sonuçlarını göster"""
        print(f"\n" + "="*80)
        print(f"🏆 RANDOM FOREST vs SVM KARŞILAŞTIRMA SONUÇLARI")
        print(f"="*80)
        
        # Grup bazında sonuçlar
        for group, group_results in results.items():
            if not group_results:
                continue
                
            print(f"\n📊 {group.upper()} GRUBU:")
            print("-" * 50)
            
            best_r2 = -float('inf')
            best_algorithm = ""
            
            for alg_name, metrics in group_results.items():
                r2 = metrics['r2_score']
                mse = metrics['mse']
                mae = metrics['mae']
                time_taken = metrics['training_time']
                model_name = metrics['model_name']
                
                print(f"  {model_name}:")
                print(f"    R² Score: {r2:.4f}")
                print(f"    MSE: {mse:.4f}")
                print(f"    MAE: {mae:.4f}")
                print(f"    Eğitim Süresi: {time_taken:.2f}s")
                
                if r2 > best_r2:
                    best_r2 = r2
                    best_algorithm = model_name
                
                print()
            
            # En iyi algoritma
            if best_algorithm:
                print(f"  🥇 En İyi: {best_algorithm} (R²: {best_r2:.4f})")
        
        # Genel özet
        print(f"\n" + "="*50)
        print(f"📈 GENEL ÖZET")
        print(f"="*50)
        
        rf_wins = 0
        svm_wins = 0
        
        for group, group_results in results.items():
            if len(group_results) == 2:
                rf_r2 = group_results.get('random_forest', {}).get('r2_score', -1)
                svm_r2 = group_results.get('svm_rbf', {}).get('r2_score', -1)
                
                if rf_r2 > svm_r2:
                    rf_wins += 1
                elif svm_r2 > rf_r2:
                    svm_wins += 1
        
        print(f"🌲 Random Forest kazandığı gruplar: {rf_wins}")
        print(f"🤖 SVM kazandığı gruplar: {svm_wins}")
        
        if rf_wins > svm_wins:
            print(f"\n🏆 GENEL KAZANAN: Random Forest Regressor")
            print(f"💡 Random Forest, {rf_wins}/{rf_wins + svm_wins} grupta daha iyi performans gösterdi.")
        elif svm_wins > rf_wins:
            print(f"\n🏆 GENEL KAZANAN: Support Vector Machine")
            print(f"💡 SVM, {svm_wins}/{rf_wins + svm_wins} grupta daha iyi performans gösterdi.")
        else:
            print(f"\n🤝 BERABERE: Her iki algoritma da eşit performans gösterdi.")

def main():
    """Ana karşılaştırma fonksiyonu"""
    print("🔬 AllerMind Algoritma Karşılaştırması")
    print("=" * 50)
    
    # Karşılaştırma nesnesini oluştur
    comparison = AlgorithmComparison(sample_size=3000)  # Hızlı test için küçük sample
    
    # Karşılaştırmayı çalıştır
    results = comparison.compare_algorithms()
    
    if results:
        print(f"\n✅ Karşılaştırma tamamlandı!")
        print(f"📊 {len(results)} grup analiz edildi.")
    else:
        print(f"\n❌ Karşılaştırma başarısız!")

if __name__ == "__main__":
    main()