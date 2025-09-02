import pandas as pd
import numpy as np
import pickle
import json
import time
from typing import Dict, List, Tuple, Any
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import warnings
warnings.filterwarnings('ignore')

class AlgorithmComparison:
    """
    Random Forest vs SVM Kapsamlı Karşılaştırma Sistemi
    """
    
    def __init__(self):
        self.df = None
        self.features = []
        self.results = {
            'random_forest': {},
            'svm_linear': {},
            'svm_rbf': {},
            'svm_poly': {}
        }
        
        # Algoritma konfigürasyonları
        self.algorithms = {
            'random_forest': {
                'name': 'Random Forest Regressor',
                'model_class': RandomForestRegressor,
                'params': {
                    'n_estimators': 100,
                    'max_depth': 15,
                    'min_samples_split': 5,
                    'min_samples_leaf': 2,
                    'random_state': 42,
                    'n_jobs': -1
                },
                'needs_scaling': False,
                'color': '#2E8B57',
                'advantages': ['Hızlı eğitim', 'Overfitting direnci', 'Feature importance']
            },
            'svm_linear': {
                'name': 'Linear SVM',
                'model_class': SVR,
                'params': {
                    'kernel': 'linear',
                    'C': 1.0,
                    'epsilon': 0.1
                },
                'needs_scaling': True,
                'color': '#FF6347',
                'advantages': ['Basit ve yorumlanabilir', 'Az parametre', 'Hızlı tahmin']
            },
            'svm_rbf': {
                'name': 'RBF SVM',
                'model_class': SVR,
                'params': {
                    'kernel': 'rbf',
                    'C': 100,
                    'gamma': 'scale',
                    'epsilon': 0.1
                },
                'needs_scaling': True,
                'color': '#4169E1',
                'advantages': ['Non-linear patterns', 'Flexible', 'Robust']
            },
            'svm_poly': {
                'name': 'Polynomial SVM',
                'model_class': SVR,
                'params': {
                    'kernel': 'poly',
                    'degree': 3,
                    'C': 1.0,
                    'epsilon': 0.1
                },
                'needs_scaling': True,
                'color': '#9932CC',
                'advantages': ['Polynomial relationships', 'Interpretable', 'Smooth curves']
            }
        }
        
        print("🔬 AllerMind: Random Forest vs SVM Karşılaştırması")
        print("=" * 60)
        
    def load_data(self):
        """Veriyi yükle ve hazırla"""
        print("\n📊 Veri yükleniyor...")
        
        data_path = '/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/cleaned_combined_data.csv'
        self.df = pd.read_csv(data_path)
        print(f"✅ {len(self.df)} satır, {len(self.df.columns)} kolon yüklendi")
        
        # Özellikleri seç
        self.features = [
            'temperature_2m', 'relative_humidity_2m', 'precipitation',
            'wind_speed_10m', 'pm10', 'pm2_5', 'upi_value', 'plant_upi_value'
        ]
        
        # Kategorik encoding
        if 'pollen_code' in self.df.columns:
            le = LabelEncoder()
            self.df['pollen_encoded'] = le.fit_transform(self.df['pollen_code'].fillna('UNKNOWN'))
            self.features.append('pollen_encoded')
        
        # NaN temizleme
        for feature in self.features:
            if feature in self.df.columns:
                self.df[feature] = self.df[feature].fillna(self.df[feature].median())
        
        print(f"🔧 {len(self.features)} özellik hazırlandı")
        
        # Hedef grupları oluştur
        self._create_target_groups()
        
    def _create_target_groups(self):
        """5 allerji grubu için hedef değişkenleri oluştur"""
        print("🎯 Allerji grupları oluşturuluyor...")
        
        # Normalize edilmiş faktörler
        temp_norm = (self.df['temperature_2m'] - self.df['temperature_2m'].min()) / \
                   (self.df['temperature_2m'].max() - self.df['temperature_2m'].min())
        humidity_norm = self.df['relative_humidity_2m'] / 100
        pm10_norm = self.df['pm10'] / self.df['pm10'].max()
        pm25_norm = self.df['pm2_5'] / self.df['pm2_5'].max()
        upi_norm = self.df['upi_value'] / self.df['upi_value'].max()
        plant_upi_norm = self.df['plant_upi_value'] / self.df['plant_upi_value'].max()
        
        # 5 allerji grubu tanımla
        group_definitions = {
            1: {'weights': [0.4, 0.3, 0.2, 0.1], 'features': [upi_norm, plant_upi_norm, pm25_norm, temp_norm]},
            2: {'weights': [0.35, 0.25, 0.25, 0.15], 'features': [pm10_norm, pm25_norm, upi_norm, humidity_norm]},
            3: {'weights': [0.35, 0.25, 0.25, 0.15], 'features': [upi_norm, temp_norm, humidity_norm, pm10_norm]},
            4: {'weights': [0.25, 0.25, 0.25, 0.25], 'features': [upi_norm, pm10_norm, pm25_norm, temp_norm]},
            5: {'weights': [0.3, 0.3, 0.2, 0.2], 'features': [temp_norm, humidity_norm, pm10_norm, upi_norm]}
        }
        
        for group_id, definition in group_definitions.items():
            weights = definition['weights']
            features = definition['features']
            
            group_score = sum(w * f for w, f in zip(weights, features))
            self.df[f'group_{group_id}'] = np.clip(group_score * 10, 0, 10)
        
        print("✅ 5 allerji grubu oluşturuldu")
        
    def train_and_evaluate_algorithm(self, algorithm_name: str, group_id: int, 
                                   test_size: float = 0.2, cv_folds: int = 5) -> Dict:
        """Belirli algoritma ve grup için eğitim ve değerlendirme"""
        
        config = self.algorithms[algorithm_name]
        group_name = f"group_{group_id}"
        
        # Veri hazırlama
        X = self.df[self.features].copy()
        y = self.df[group_name].copy()
        
        # NaN temizleme
        mask = ~(X.isnull().any(axis=1) | y.isnull())
        X_clean = X[mask]
        y_clean = y[mask]
        
        if len(X_clean) == 0:
            return {'error': 'No valid data'}
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_clean, y_clean, test_size=test_size, random_state=42
        )
        
        start_time = time.time()
        
        # Scaling (SVM için)
        if config['needs_scaling']:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            train_data, test_data = X_train_scaled, X_test_scaled
        else:
            train_data, test_data = X_train, X_test
            scaler = None
        
        # Model eğitimi
        model = config['model_class'](**config['params'])
        model.fit(train_data, y_train)
        
        # Tahmin
        y_pred = model.predict(test_data)
        training_time = time.time() - start_time
        
        # Cross-validation
        cv_start = time.time()
        if config['needs_scaling']:
            # CV için pipeline gerekli olabilir, basit yaklaşım kullanalım
            cv_scores = []
            for fold in range(cv_folds):
                X_cv_train, X_cv_test, y_cv_train, y_cv_test = train_test_split(
                    X_clean, y_clean, test_size=0.2, random_state=fold
                )
                if config['needs_scaling']:
                    scaler_cv = StandardScaler()
                    X_cv_train = scaler_cv.fit_transform(X_cv_train)
                    X_cv_test = scaler_cv.transform(X_cv_test)
                
                model_cv = config['model_class'](**config['params'])
                model_cv.fit(X_cv_train, y_cv_train)
                score = r2_score(y_cv_test, model_cv.predict(X_cv_test))
                cv_scores.append(score)
        else:
            cv_scores = cross_val_score(model, X_clean, y_clean, cv=cv_folds, scoring='r2')
        
        cv_time = time.time() - cv_start
        
        # Metrikler
        metrics = {
            'model_name': config['name'],
            'algorithm': algorithm_name,
            'group_id': group_id,
            'r2_score': r2_score(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'mae': mean_absolute_error(y_test, y_pred),
            'training_time': training_time,
            'cv_mean': np.mean(cv_scores),
            'cv_std': np.std(cv_scores),
            'cv_time': cv_time,
            'data_points': len(X_clean),
            'test_points': len(X_test),
            'advantages': config['advantages']
        }
        
        return metrics
    
    def compare_all_algorithms(self, sample_size: int = 10000):
        """Tüm algoritmaları karşılaştır"""
        print(f"\n🆚 Kapsamlı Algoritma Karşılaştırması")
        print(f"📊 Örnek boyutu: {sample_size}")
        
        # Veriyi yükle
        self.load_data()
        
        # Büyük veri seti için sampling
        if len(self.df) > sample_size:
            self.df = self.df.sample(n=sample_size, random_state=42)
            print(f"📉 Veri örneklendi: {len(self.df)} satır")
        
        # Her algoritma ve grup kombinasyonu için test
        total_tests = len(self.algorithms) * 5  # 5 grup
        current_test = 0
        
        print(f"\n🚀 {total_tests} test başlıyor...")
        
        for algorithm_name in self.algorithms.keys():
            self.results[algorithm_name] = {}
            
            for group_id in range(1, 6):
                current_test += 1
                print(f"\n[{current_test}/{total_tests}] {self.algorithms[algorithm_name]['name']} - Grup {group_id}")
                
                metrics = self.train_and_evaluate_algorithm(algorithm_name, group_id)
                
                if 'error' not in metrics:
                    self.results[algorithm_name][group_id] = metrics
                    print(f"  ✅ R²: {metrics['r2_score']:.4f}, MSE: {metrics['mse']:.4f}, Süre: {metrics['training_time']:.2f}s")
                else:
                    print(f"  ❌ Hata: {metrics['error']}")
        
        print(f"\n✅ Tüm testler tamamlandı!")
        
        # Sonuçları göster
        self._display_comprehensive_results()
        
        # Grafikler oluştur
        self._create_comparison_charts()
        
        # Sonuçları kaydet
        self._save_results()
        
        return self.results
    
    def _display_comprehensive_results(self):
        """Kapsamlı sonuçları göster"""
        print(f"\n" + "="*80)
        print(f"🏆 KAPSAMLI ALGORITMA KARŞILAŞTIRMA SONUÇLARI")
        print(f"="*80)
        
        # Grup bazında karşılaştırma
        for group_id in range(1, 6):
            print(f"\n📊 GRUP {group_id} KARŞILAŞTIRMASI:")
            print("-" * 60)
            
            group_results = []
            for alg_name, alg_results in self.results.items():
                if group_id in alg_results:
                    metrics = alg_results[group_id]
                    group_results.append({
                        'Algorithm': metrics['model_name'],
                        'R² Score': metrics['r2_score'],
                        'MSE': metrics['mse'],
                        'MAE': metrics['mae'],
                        'CV Mean±Std': f"{metrics['cv_mean']:.3f}±{metrics['cv_std']:.3f}",
                        'Training Time': f"{metrics['training_time']:.2f}s",
                        'Advantages': ', '.join(metrics['advantages'][:2])
                    })
            
            if group_results:
                # En iyi R² skoru
                best_r2 = max(group_results, key=lambda x: x['R² Score'])
                # En hızlı eğitim
                fastest = min(group_results, key=lambda x: float(x['Training Time'].replace('s', '')))
                
                for result in group_results:
                    symbol = "🥇" if result == best_r2 else "⚡" if result == fastest else "  "
                    print(f"  {symbol} {result['Algorithm']:<20} | "
                          f"R²: {result['R² Score']:.4f} | "
                          f"MSE: {result['MSE']:.4f} | "
                          f"CV: {result['CV Mean±Std']:<12} | "
                          f"Süre: {result['Training Time']:<8}")
                
                print(f"\n  🎯 En İyi Performans: {best_r2['Algorithm']} (R²: {best_r2['R² Score']:.4f})")
                print(f"  ⚡ En Hızlı Eğitim: {fastest['Algorithm']} ({fastest['Training Time']})")
        
        # Genel özet
        self._display_overall_summary()
    
    def _display_overall_summary(self):
        """Genel özet istatistikleri"""
        print(f"\n" + "="*60)
        print(f"📈 GENEL ÖZET İSTATİSTİKLERİ")
        print(f"="*60)
        
        algorithm_stats = {}
        
        for alg_name, alg_results in self.results.items():
            if alg_results:
                r2_scores = [metrics['r2_score'] for metrics in alg_results.values()]
                training_times = [metrics['training_time'] for metrics in alg_results.values()]
                cv_means = [metrics['cv_mean'] for metrics in alg_results.values()]
                
                algorithm_stats[alg_name] = {
                    'name': self.algorithms[alg_name]['name'],
                    'avg_r2': np.mean(r2_scores),
                    'std_r2': np.std(r2_scores),
                    'avg_time': np.mean(training_times),
                    'avg_cv': np.mean(cv_means),
                    'wins': 0,
                    'groups_tested': len(alg_results)
                }
        
        # Her grupta en iyi olanı say
        for group_id in range(1, 6):
            group_r2_scores = {}
            for alg_name, alg_results in self.results.items():
                if group_id in alg_results:
                    group_r2_scores[alg_name] = alg_results[group_id]['r2_score']
            
            if group_r2_scores:
                winner = max(group_r2_scores, key=group_r2_scores.get)
                algorithm_stats[winner]['wins'] += 1
        
        # Sonuçları göster
        print(f"\n🏅 Algoritma Performans Sıralaması:")
        sorted_algorithms = sorted(algorithm_stats.items(), 
                                 key=lambda x: x[1]['avg_r2'], reverse=True)
        
        for rank, (alg_name, stats) in enumerate(sorted_algorithms, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
            print(f"  {medal} {rank}. {stats['name']:<20}")
            print(f"      📊 Ortalama R²: {stats['avg_r2']:.4f} ± {stats['std_r2']:.4f}")
            print(f"      ⏱️  Ortalama Süre: {stats['avg_time']:.2f}s")
            print(f"      🏆 Kazanılan Gruplar: {stats['wins']}/{stats['groups_tested']}")
            print(f"      🎯 CV Ortalama: {stats['avg_cv']:.4f}")
            print()
        
        # Genel tavsiye
        best_overall = sorted_algorithms[0][1]['name']
        fastest_alg = min(algorithm_stats.items(), key=lambda x: x[1]['avg_time'])[1]['name']
        most_wins = max(algorithm_stats.items(), key=lambda x: x[1]['wins'])[1]['name']
        
        print(f"💡 TAVSİYELER:")
        print(f"  🎯 En İyi Genel Performans: {best_overall}")
        print(f"  ⚡ En Hızlı Algorithm: {fastest_alg}")
        print(f"  🏆 En Çok Kazanan: {most_wins}")
        print(f"  🔬 Üretim Ortamı İçin: Random Forest (Robust ve yorumlanabilir)")
        print(f"  🧪 Araştırma İçin: RBF SVM (Karmaşık pattern detection)")
    
    def _create_comparison_charts(self):
        """Karşılaştırma grafiklerini oluştur"""
        print(f"\n📊 Karşılaştırma grafikleri oluşturuluyor...")
        
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('AllerMind: Random Forest vs SVM Karşılaştırması', fontsize=16, fontweight='bold')
        
        # 1. R² Scores by Group
        ax1 = axes[0, 0]
        group_data = {alg: [] for alg in self.algorithms.keys()}
        groups = []
        
        for group_id in range(1, 6):
            groups.append(f'Grup {group_id}')
            for alg_name in self.algorithms.keys():
                if group_id in self.results[alg_name]:
                    group_data[alg_name].append(self.results[alg_name][group_id]['r2_score'])
                else:
                    group_data[alg_name].append(0)
        
        x = np.arange(len(groups))
        width = 0.2
        
        for i, (alg_name, scores) in enumerate(group_data.items()):
            color = self.algorithms[alg_name]['color']
            label = self.algorithms[alg_name]['name']
            ax1.bar(x + i*width, scores, width, label=label, color=color, alpha=0.8)
        
        ax1.set_xlabel('Allerji Grupları')
        ax1.set_ylabel('R² Score')
        ax1.set_title('Grup Bazında R² Score Karşılaştırması')
        ax1.set_xticks(x + width*1.5)
        ax1.set_xticklabels(groups)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Training Time Comparison
        ax2 = axes[0, 1]
        avg_times = {}
        for alg_name, alg_results in self.results.items():
            if alg_results:
                times = [metrics['training_time'] for metrics in alg_results.values()]
                avg_times[alg_name] = np.mean(times)
        
        algorithms = list(avg_times.keys())
        times = list(avg_times.values())
        colors = [self.algorithms[alg]['color'] for alg in algorithms]
        names = [self.algorithms[alg]['name'] for alg in algorithms]
        
        bars = ax2.bar(names, times, color=colors, alpha=0.8)
        ax2.set_ylabel('Ortalama Eğitim Süresi (saniye)')
        ax2.set_title('Algoritma Eğitim Süresi Karşılaştırması')
        ax2.grid(True, alpha=0.3)
        
        # Değerleri bars üzerine yaz
        for bar, time_val in zip(bars, times):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{time_val:.2f}s', ha='center', va='bottom', fontweight='bold')
        
        # 3. Cross-Validation Scores
        ax3 = axes[1, 0]
        cv_data = {alg: [] for alg in self.algorithms.keys()}
        
        for group_id in range(1, 6):
            for alg_name in self.algorithms.keys():
                if group_id in self.results[alg_name]:
                    cv_data[alg_name].append(self.results[alg_name][group_id]['cv_mean'])
                else:
                    cv_data[alg_name].append(0)
        
        for i, (alg_name, scores) in enumerate(cv_data.items()):
            color = self.algorithms[alg_name]['color']
            label = self.algorithms[alg_name]['name']
            ax3.bar(x + i*width, scores, width, label=label, color=color, alpha=0.8)
        
        ax3.set_xlabel('Allerji Grupları')
        ax3.set_ylabel('Cross-Validation R² Score')
        ax3.set_title('Cross-Validation Performans Karşılaştırması')
        ax3.set_xticks(x + width*1.5)
        ax3.set_xticklabels(groups)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Algorithm Wins Distribution
        ax4 = axes[1, 1]
        win_counts = {alg: 0 for alg in self.algorithms.keys()}
        
        for group_id in range(1, 6):
            group_r2_scores = {}
            for alg_name, alg_results in self.results.items():
                if group_id in alg_results:
                    group_r2_scores[alg_name] = alg_results[group_id]['r2_score']
            
            if group_r2_scores:
                winner = max(group_r2_scores, key=group_r2_scores.get)
                win_counts[winner] += 1
        
        algorithms = list(win_counts.keys())
        wins = list(win_counts.values())
        colors = [self.algorithms[alg]['color'] for alg in algorithms]
        names = [self.algorithms[alg]['name'] for alg in algorithms]
        
        wedges, texts, autotexts = ax4.pie(wins, labels=names, colors=colors, autopct='%1.0f%%',
                                          startangle=90, textprops={'fontsize': 10})
        ax4.set_title('Algoritma Galibiyetleri Dağılımı')
        
        plt.tight_layout()
        
        # Grafikleri kaydet
        chart_path = '/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/comparison/algorithm_comparison_charts.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        print(f"📊 Grafikler kaydedildi: {chart_path}")
        
        plt.show()
    
    def _save_results(self):
        """Sonuçları JSON formatında kaydet"""
        results_path = '/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/comparison/comparison_results.json'
        
        # JSON serializable hale getir
        serializable_results = {}
        for alg_name, alg_results in self.results.items():
            serializable_results[alg_name] = {}
            for group_id, metrics in alg_results.items():
                serializable_results[alg_name][group_id] = {
                    k: float(v) if isinstance(v, (np.float64, np.float32)) else v
                    for k, v in metrics.items()
                    if k != 'advantages'  # advantages'ı ayrı olarak ekle
                }
                serializable_results[alg_name][group_id]['advantages'] = metrics.get('advantages', [])
        
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Sonuçlar kaydedildi: {results_path}")

def main():
    """Ana karşılaştırma fonksiyonu"""
    print("🔬 AllerMind: Kapsamlı Random Forest vs SVM Karşılaştırması")
    print("=" * 70)
    
    # Karşılaştırma sistemi
    comparison = AlgorithmComparison()
    
    # Karşılaştırmayı çalıştır
    results = comparison.compare_all_algorithms(sample_size=8000)
    
    print(f"\n✅ Karşılaştırma tamamlandı!")
    print(f"📁 Sonuçlar '/comparison' klasörüne kaydedildi")
    print(f"📊 Grafikler ve JSON raporu oluşturuldu")

if __name__ == "__main__":
    main()
