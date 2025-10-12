#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALLERMIND V2.0 - VERİ ANALİZİ VE HAZıRLIK
Expert-level istatistiksel analiz ve model hazırlığı
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split, TimeSeriesSplit, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import ElasticNet, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

def analyze_data():
    """Kapsamlı veri analizi"""
    
    print("🔍 ALLERMIND V2.0 - VERİ ANALİZİ BAŞLATIYOR")
    print("=" * 60)
    
    # Veri yükleme
    data_path = "/Users/elifdy/Desktop/allermind/aller-mind/DATA/11SEP/20250911_combined_all_data.csv"
    
    try:
        print("📁 Veri yükleniyor...")
        df = pd.read_csv(data_path)
        print(f"✅ Veri yüklendi: {df.shape[0]:,} satır, {df.shape[1]} kolon")
        
        # Temel bilgiler
        print(f"\n📊 TEMEL İSTATİSTİKLER:")
        print(f"   Veri boyutu: {df.shape}")
        print(f"   Bellek kullanımı: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        print(f"   Tarih aralığı: {df['time'].min()} - {df['time'].max()}")
        
        # Kolonlar
        print(f"\n📋 KOLONLAR ({len(df.columns)}):")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        # Eksik değerler
        print(f"\n🔍 EKSİK DEĞER ANALİZİ:")
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        
        for col in missing[missing > 0].index:
            print(f"   {col}: {missing[col]:,} ({missing_pct[col]:.1f}%)")
        
        # Target kolonlarımızı belirleyelim
        important_cols = [
            'temperature_2m', 'relative_humidity_2m', 'precipitation', 'snowfall', 'rain',
            'cloud_cover', 'surface_pressure', 'wind_speed_10m', 'wind_direction_10m',
            'sunshine_duration', 'pm10', 'pm2_5', 'carbon_dioxide', 'carbon_monoxide',
            'nitrogen_dioxide', 'sulphur_dioxide', 'ozone', 'aerosol_optical_depth',
            'methane', 'uv_index', 'uv_index_clear_sky', 'dust', 'pollen_code',
            'in_season', 'upi_value', 'plant_code', 'plant_in_season', 'plant_upi_value'
        ]
        
        # Mevcut kolonları kontrol et
        available_cols = [col for col in important_cols if col in df.columns]
        missing_cols = [col for col in important_cols if col not in df.columns]
        
        print(f"\n✅ MEVCUT KOLONLAR ({len(available_cols)}):")
        for col in available_cols:
            print(f"   ✓ {col}")
        
        if missing_cols:
            print(f"\n❌ EKSİK KOLONLAR ({len(missing_cols)}):")
            for col in missing_cols:
                print(f"   ✗ {col}")
        
        # Kategorik kolonları analiz et
        categorical_cols = ['pollen_code', 'in_season', 'plant_code', 'plant_in_season']
        existing_categorical = [col for col in categorical_cols if col in df.columns]
        
        print(f"\n🏷️ KATEGORİK KOLON ANALİZİ:")
        for col in existing_categorical:
            unique_vals = df[col].nunique()
            print(f"   {col}: {unique_vals} benzersiz değer")
            print(f"      Değerler: {list(df[col].unique()[:10])}")  # İlk 10 değer
        
        # Numerik kolonların istatistikleri
        print(f"\n📈 NUMERİK KOLON İSTATİSTİKLERİ:")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols[:10]:  # İlk 10 numerik kolon
            if col in available_cols:
                stats = df[col].describe()
                print(f"   {col}:")
                print(f"      Mean: {stats['mean']:.2f}, Std: {stats['std']:.2f}")
                print(f"      Min: {stats['min']:.2f}, Max: {stats['max']:.2f}")
        
        # Aykırı değer analizi
        print(f"\n🎯 AYKIRI DEĞER ANALİZİ:")
        for col in ['pm10', 'pm2_5', 'ozone', 'uv_index'][:4]:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
                print(f"   {col}: {outliers:,} aykırı değer ({outliers/len(df)*100:.1f}%)")
        
        return df, available_cols, existing_categorical
        
    except Exception as e:
        print(f"❌ Veri yükleme hatası: {str(e)}")
        return None, None, None

if __name__ == "__main__":
    df, available_cols, categorical_cols = analyze_data()
    
    if df is not None:
        print(f"\n🎉 Analiz tamamlandı!")
        print(f"   Kullanılabilir kolon sayısı: {len(available_cols) if available_cols else 0}")
        print(f"   Kategorik kolon sayısı: {len(categorical_cols) if categorical_cols else 0}")
    else:
        print(f"❌ Analiz başarısız!")