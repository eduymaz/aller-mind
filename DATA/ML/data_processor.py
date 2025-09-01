import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class AllergyDataProcessor:
    """
    Allerji grupları için veri işleme ve temizleme sınıfı
    """
    
    def __init__(self):
        self.data_paths = {
            '30AUG': '/Users/elifdy/Desktop/allermind/aller-mind/DATA/30AUG/20250830_combined_all_data.csv',
            '31AUG': '/Users/elifdy/Desktop/allermind/aller-mind/DATA/31AUG/20250831_combined_all_data.csv',
            '01SEP': '/Users/elifdy/Desktop/allermind/aller-mind/DATA/01SEP/20250901_combined_all_data.csv'
        }
        self.combined_data = None
        
    def load_and_combine_data(self) -> pd.DataFrame:
        """
        Üç farklı tarihteki verileri yükle ve birleştir
        """
        print("📊 Verileri yüklüyor...")
        dataframes = []
        
        for date, path in self.data_paths.items():
            try:
                df = pd.read_csv(path)
                df['data_date'] = date
                dataframes.append(df)
                print(f"✅ {date} verisi yüklendi: {len(df)} satır")
            except FileNotFoundError:
                print(f"❌ {date} dosyası bulunamadı: {path}")
                continue
        
        if dataframes:
            self.combined_data = pd.concat(dataframes, ignore_index=True)
            print(f"🔗 Toplam birleştirilmiş veri: {len(self.combined_data)} satır")
        else:
            raise Exception("Hiçbir veri dosyası yüklenemedi!")
            
        return self.combined_data
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Veriyi temizle ve gereksiz kolonları kaldır
        """
        print("\n🧹 Veri temizleme işlemi başlıyor...")
        
        # 1. picture_url ve picture_closeup_url kolonlarını kaldır
        columns_to_remove = ['picture_url', 'picture_closeup_url']
        existing_columns = [col for col in columns_to_remove if col in df.columns]
        
        if existing_columns:
            df = df.drop(columns=existing_columns)
            print(f"🗑️  Kaldırılan kolonlar: {existing_columns}")
        
        # 2. Tamamen boş olan kolonları tespit et ve kaldır
        empty_columns = df.columns[df.isnull().all()].tolist()
        if empty_columns:
            df = df.drop(columns=empty_columns)
            print(f"🗑️  Boş kolonlar kaldırıldı: {empty_columns}")
        
        # 3. Eksik değerleri kontrol et
        missing_counts = df.isnull().sum()
        high_missing = missing_counts[missing_counts > len(df) * 0.7]
        
        if len(high_missing) > 0:
            print(f"⚠️  Yüksek eksik değer oranına sahip kolonlar:")
            for col, count in high_missing.items():
                print(f"   - {col}: {count}/{len(df)} ({count/len(df)*100:.1f}%)")
        
        # 4. Numerik kolonları tanımla ve eksik değerleri doldur
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if df[col].isnull().sum() > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                print(f"🔧 {col} eksik değerleri median ile dolduruldu: {median_val}")
        
        # 5. Kategorik kolonları doldur
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if df[col].isnull().sum() > 0:
                mode_val = df[col].mode().iloc[0] if len(df[col].mode()) > 0 else 'Unknown'
                df[col] = df[col].fillna(mode_val)
                print(f"🔧 {col} eksik değerleri mod ile dolduruldu: {mode_val}")
        
        print(f"✅ Temizleme tamamlandı. Final boyut: {df.shape}")
        return df
    
    def analyze_data_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Veri yapısını analiz et
        """
        print("\n📈 Veri yapısı analizi...")
        
        analysis = {
            'shape': df.shape,
            'columns': list(df.columns),
            'numeric_columns': list(df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': list(df.select_dtypes(include=['object']).columns),
            'unique_dates': df['date'].unique() if 'date' in df.columns else [],
            'pollen_types': df['pollen_code'].unique() if 'pollen_code' in df.columns else [],
            'plant_types': df['plant_code'].unique() if 'plant_code' in df.columns else []
        }
        
        print(f"📏 Boyut: {analysis['shape']}")
        print(f"🔢 Numerik kolonlar ({len(analysis['numeric_columns'])}): {analysis['numeric_columns'][:5]}...")
        print(f"📝 Kategorik kolonlar ({len(analysis['categorical_columns'])}): {analysis['categorical_columns']}")
        print(f"📅 Benzersiz tarihler: {len(analysis['unique_dates'])}")
        print(f"🌿 Polen türleri: {analysis['pollen_types']}")
        print(f"🌱 Bitki türleri: {analysis['plant_types']}")
        
        return analysis
    
    def get_weather_features(self, df: pd.DataFrame) -> List[str]:
        """Hava durumu özelliklerini al"""
        weather_features = [
            'temperature_2m', 'relative_humidity_2m', 'precipitation', 
            'snowfall', 'rain', 'cloud_cover', 'surface_pressure', 
            'wind_speed_10m', 'wind_direction_10m', 'soil_temperature_0_to_7cm',
            'soil_moisture_0_to_7cm', 'sunshine_duration', 'uv_index', 'uv_index_clear_sky'
        ]
        return [col for col in weather_features if col in df.columns]
    
    def get_air_quality_features(self, df: pd.DataFrame) -> List[str]:
        """Hava kalitesi özelliklerini al"""
        air_quality_features = [
            'pm10', 'pm2_5', 'carbon_dioxide', 'carbon_monoxide', 
            'nitrogen_dioxide', 'sulphur_dioxide', 'ozone', 
            'aerosol_optical_depth', 'methane', 'dust'
        ]
        return [col for col in air_quality_features if col in df.columns]
    
    def get_pollen_features(self, df: pd.DataFrame) -> List[str]:
        """Polen özelliklerini al"""
        pollen_features = [
            'pollen_code', 'in_season', 'upi_value', 
            'plant_code', 'plant_in_season', 'plant_upi_value'
        ]
        return [col for col in pollen_features if col in df.columns]
    
    def process_all_data(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Tüm veri işleme sürecini çalıştır
        """
        print("🚀 Veri işleme süreci başlıyor...\n")
        
        # Verileri yükle ve birleştir
        combined_df = self.load_and_combine_data()
        
        # Veriyi temizle
        cleaned_df = self.clean_data(combined_df)
        
        # Veri yapısını analiz et
        analysis = self.analyze_data_structure(cleaned_df)
        
        # Özellik gruplarını belirle
        analysis['weather_features'] = self.get_weather_features(cleaned_df)
        analysis['air_quality_features'] = self.get_air_quality_features(cleaned_df)
        analysis['pollen_features'] = self.get_pollen_features(cleaned_df)
        
        print(f"\n🌤️  Hava durumu özellikleri ({len(analysis['weather_features'])}): {analysis['weather_features']}")
        print(f"🏭 Hava kalitesi özellikleri ({len(analysis['air_quality_features'])}): {analysis['air_quality_features']}")
        print(f"🌿 Polen özellikleri ({len(analysis['pollen_features'])}): {analysis['pollen_features']}")
        
        # Temizlenmiş veriyi kaydet
        output_path = '/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/cleaned_combined_data.csv'
        cleaned_df.to_csv(output_path, index=False)
        print(f"\n💾 Temizlenmiş veri kaydedildi: {output_path}")
        
        return cleaned_df, analysis

if __name__ == "__main__":
    processor = AllergyDataProcessor()
    cleaned_data, data_analysis = processor.process_all_data()
