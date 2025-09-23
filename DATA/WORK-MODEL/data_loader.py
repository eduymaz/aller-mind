"""
AllerMind Veri Yükleme ve İşleme Modülü
16SEP klasöründeki CSV verilerini model için uygun formata dönüştürür
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import os
import logging
from dataclasses import dataclass

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EnvironmentalData:
    """Çevresel veri yapısı"""
    timestamp: datetime
    location: Dict[str, float]  # lat, lon
    
    # Hava kalitesi verileri
    air_quality: Dict[str, float]
    
    # Hava durumu verileri  
    weather: Dict[str, float]
    
    # Polen verileri
    pollen: Dict[str, Any]
    
    # Bitki verileri
    plants: List[Dict[str, Any]]


class DataLoader:

    
    def __init__(self, data_path: str = "/Users/elifdy/Desktop/allermind/aller-mind/DATA/16SEP"):
        self.data_path = data_path
        self.required_files = [
            'air_quality_data.csv',
            'pollen_data.csv', 
            'plant_data.csv'
        ]
        
        # Model özellik eşlemeleri
        self.feature_mappings = {
            'air_quality_features': [
                'pm10', 'pm2_5', 'carbon_dioxide', 'carbon_monoxide',
                'nitrogen_dioxide', 'sulphur_dioxide', 'ozone',
                'aerosol_optical_depth', 'methane', 'uv_index', 'dust'
            ],
            'weather_features': [
                'temperature_2m', 'relative_humidity_2m', 'precipitation',
                'cloud_cover', 'surface_pressure', 'wind_speed_10m',
                'sunshine_duration'
            ],
            'pollen_features': [
                'upi_value', 'grass_pollen', 'tree_pollen', 'weed_pollen',
                'in_season_count', 'pollen_diversity_index'
            ]
        }
        
        # Polen kodu eşlemeleri
        self.pollen_type_mapping = {
            'GRASS': 'grass_pollen',
            'TREE': 'tree_pollen', 
            'WEED': 'weed_pollen'
        }
        
        # Bitki kodu eşlemeleri
        self.plant_mapping = {
            'GRAMINALES': {'type': 'grass', 'allergenicity': 1.0},
            'OLIVE': {'type': 'tree', 'allergenicity': 0.5},
            'RAGWEED': {'type': 'weed', 'allergenicity': 1.3},
            'MUGWORT': {'type': 'weed', 'allergenicity': 1.1},
            'BIRCH': {'type': 'tree', 'allergenicity': 0.9},
            'OAK': {'type': 'tree', 'allergenicity': 0.8}
        }
        
    def validate_data_files(self) -> bool:
        
        missing_files = []
        
        for file_name in self.required_files:
            file_path = os.path.join(self.data_path, file_name)
            if not os.path.exists(file_path):
                missing_files.append(file_name)
        
        if missing_files:
            logger.error(f"Eksik dosyalar: {missing_files}")
            return False
        
        logger.info("Tüm gerekli veri dosyları mevcut")
        return True
    
    def load_air_quality_data(self) -> pd.DataFrame:
        
        try:
            file_path = os.path.join(self.data_path, 'air_quality_data.csv')
            df = pd.read_csv(file_path)
            
            # Tarih sütununu datetime'a çevir
            df['time'] = pd.to_datetime(df['time'])
            
            logger.info(f"Hava kalitesi verisi yüklendi: {len(df)} kayıt")
            return df
            
        except Exception as e:
            logger.error(f"Hava kalitesi verisi yüklenemedi: {e}")
            return pd.DataFrame()
    
    def load_pollen_data(self) -> pd.DataFrame:
        """Polen verilerini yükle"""
        try:
            file_path = os.path.join(self.data_path, 'pollen_data.csv')
            df = pd.read_csv(file_path)
            
            # Tarih sütununu datetime'a çevir
            df['date'] = pd.to_datetime(df['date'])
            
            logger.info(f"Polen verisi yüklendi: {len(df)} kayıt")
            return df
            
        except Exception as e:
            logger.error(f"Polen verisi yüklenemedi: {e}")
            return pd.DataFrame()
    
    def load_plant_data(self) -> pd.DataFrame:
        """Bitki verilerini yükle"""
        try:
            file_path = os.path.join(self.data_path, 'plant_data.csv')
            df = pd.read_csv(file_path)
            
            logger.info(f"Bitki verisi yüklendi: {len(df)} kayıt")
            return df
            
        except Exception as e:
            logger.error(f"Bitki verisi yüklenemedi: {e}")
            return pd.DataFrame()
    
    def process_pollen_data_for_location(self, lat: float, lon: float, 
                                       target_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Belirtilen konum ve tarih için polen verilerini işle
        """
        pollen_df = self.load_pollen_data()
        plant_df = self.load_plant_data()
        
        if pollen_df.empty or plant_df.empty:
            return {}
        
        # Tarih filtresi
        if target_date is None:
            target_date = datetime.now()
        
        # Konum filtresi (±0.5 derece tolerans)
        location_mask = (
            (abs(pollen_df['lat'] - lat) <= 0.5) &
            (abs(pollen_df['lon'] - lon) <= 0.5)
        )
        
        # Tarih filtresi (±3 gün tolerans)
        target_datetime = pd.to_datetime(target_date)
        date_mask = abs((pollen_df['date'] - target_datetime).dt.days) <= 3
        
        filtered_pollen = pollen_df[location_mask & date_mask]
        
        if filtered_pollen.empty:
            logger.warning(f"Konum ({lat}, {lon}) ve tarih {target_date} için polen verisi bulunamadı")
            return self._get_default_pollen_data()
        
        # Polen tiplerini gruplandır
        pollen_summary = {
            'grass_pollen': 0.0,
            'tree_pollen': 0.0,
            'weed_pollen': 0.0,
            'total_upi': 0.0,
            'in_season_count': 0,
            'pollen_diversity_index': 0.0,
            'dominant_pollen_type': 'none',
            'high_risk_plants': []
        }
        
        # Polen verilerini topla
        pollen_type_values = {'GRASS': [], 'TREE': [], 'WEED': []}
        
        for _, row in filtered_pollen.iterrows():
            pollen_type = row['pollen_code']
            upi_value = row['upi_value']
            in_season = row['in_season']
            
            if pollen_type in pollen_type_values:
                pollen_type_values[pollen_type].append(upi_value)
                
                if in_season:
                    pollen_summary['in_season_count'] += 1
        
        # Ortalama UPI değerlerini hesapla
        for pollen_type, values in pollen_type_values.items():
            if values:
                avg_upi = np.mean(values)
                feature_name = self.pollen_type_mapping[pollen_type]
                pollen_summary[feature_name] = avg_upi
                pollen_summary['total_upi'] += avg_upi
        
        # Polen çeşitlilik indeksi
        active_types = sum(1 for values in pollen_type_values.values() if values)
        pollen_summary['pollen_diversity_index'] = active_types / 3.0
        
        # Dominant polen tipi
        max_upi = 0
        for pollen_type, values in pollen_type_values.items():
            if values and max(values) > max_upi:
                max_upi = max(values)
                pollen_summary['dominant_pollen_type'] = pollen_type.lower()
        
        # Yüksek riskli bitkileri belirle
        pollen_summary['high_risk_plants'] = self._identify_high_risk_plants(
            filtered_pollen, plant_df
        )
        
        return pollen_summary
    
    def _identify_high_risk_plants(self, pollen_data: pd.DataFrame, 
                                 plant_data: pd.DataFrame) -> List[str]:
       
        high_risk_plants = []
        
        # Pollen data ile plant data'yı birleştir
        for _, pollen_row in pollen_data.iterrows():
            pollen_id = pollen_row['id']
            upi_value = pollen_row['upi_value']
            
            # İlgili bitki verilerini bul
            related_plants = plant_data[plant_data['pollen_data_id'] == pollen_id]
            
            for _, plant_row in related_plants.iterrows():
                plant_code = plant_row['plant_code']
                plant_upi = plant_row['plant_upi_value']
                
                # Yüksek risk kriterleri
                if upi_value >= 3.0 or plant_upi >= 3.0:  # Yüksek UPI
                    if plant_code in self.plant_mapping:
                        allergenicity = self.plant_mapping[plant_code]['allergenicity']
                        if allergenicity >= 1.0:  # Yüksek alerjenik potansiyel
                            high_risk_plants.append(plant_code)
        
        return list(set(high_risk_plants))  # Tekrarları kaldır
    
    def _get_default_pollen_data(self) -> Dict[str, Any]:
       
        return {
            'grass_pollen': 1.0,
            'tree_pollen': 1.0,
            'weed_pollen': 1.0,
            'total_upi': 3.0,
            'in_season_count': 0,
            'pollen_diversity_index': 0.3,
            'dominant_pollen_type': 'mixed',
            'high_risk_plants': []
        }
    
    def process_air_quality_for_location(self, lat: float, lon: float,
                                       target_datetime: Optional[datetime] = None) -> Dict[str, float]:
     
        air_df = self.load_air_quality_data()
        
        if air_df.empty:
            return self._get_default_air_quality_data()
        
        if target_datetime is None:
            target_datetime = datetime.now()
        
        # Konum filtresi
        location_mask = (
            (abs(air_df['lat'] - lat) <= 0.5) &
            (abs(air_df['lon'] - lon) <= 0.5)
        )
        
        # Zaman filtresi (±6 saat tolerans)
        time_diff = abs((air_df['time'] - target_datetime).dt.total_seconds() / 3600)
        time_mask = time_diff <= 6
        
        filtered_air = air_df[location_mask & time_mask]
        
        if filtered_air.empty:
            logger.warning(f"Konum ({lat}, {lon}) ve zaman {target_datetime} için hava kalitesi verisi bulunamadı")
            return self._get_default_air_quality_data()
        
        # En yakın zamanı seç
        closest_record = filtered_air.loc[filtered_air['time'].sub(target_datetime).abs().idxmin()]
        
        # Hava kalitesi özelliklerini çıkar
        air_quality_features = {}
        for feature in self.feature_mappings['air_quality_features']:
            if feature in closest_record:
                air_quality_features[feature] = float(closest_record[feature])
            else:
                air_quality_features[feature] = 0.0
        
        return air_quality_features
    
    def _get_default_air_quality_data(self) -> Dict[str, float]:
        """Varsayılan hava kalitesi verisi"""
        return {
            'pm10': 20.0,
            'pm2_5': 10.0,
            'carbon_dioxide': 400.0,
            'carbon_monoxide': 100.0,
            'nitrogen_dioxide': 10.0,
            'sulphur_dioxide': 5.0,
            'ozone': 80.0,
            'aerosol_optical_depth': 0.3,
            'methane': 1500.0,
            'uv_index': 5.0,
            'dust': 1.0
        }
    
    def combine_environmental_data(self, lat: float, lon: float,
                                 target_datetime: Optional[datetime] = None) -> Dict[str, Any]:
    
        if target_datetime is None:
            target_datetime = datetime.now()
        
        # Hava kalitesi verisi
        air_quality = self.process_air_quality_for_location(lat, lon, target_datetime)
        
        # Polen verisi
        pollen_data = self.process_pollen_data_for_location(lat, lon, target_datetime.date())
        
        # Hava durumu verisi (şimdilik varsayılan)
        weather_data = self._get_default_weather_data()
        
        # Tüm verileri birleştir
        combined_data = {
            **air_quality,
            **pollen_data,
            **weather_data
        }
        
        # Metadata ekle
        combined_data['metadata'] = {
            'location': {'lat': lat, 'lon': lon},
            'timestamp': target_datetime.isoformat(),
            'data_quality_score': self._calculate_data_quality_score(air_quality, pollen_data),
            'missing_features': self._identify_missing_features(combined_data)
        }
        
        return combined_data
    
    def _get_default_weather_data(self) -> Dict[str, float]:
       
        return {
            'temperature_2m': 20.0,
            'relative_humidity_2m': 60.0,
            'precipitation': 0.0,
            'cloud_cover': 50.0,
            'surface_pressure': 1013.25,
            'wind_speed_10m': 10.0,
            'sunshine_duration': 3600.0
        }
    
    def _calculate_data_quality_score(self, air_quality: Dict, pollen_data: Dict) -> float:

        total_features = len(self.feature_mappings['air_quality_features']) + len(self.feature_mappings['pollen_features'])
        available_features = len([k for k in air_quality.keys() if air_quality[k] != 0.0])
        available_features += len([k for k in pollen_data.keys() if isinstance(pollen_data[k], (int, float)) and pollen_data[k] != 0.0])
        
        return available_features / total_features
    
    def _identify_missing_features(self, data: Dict) -> List[str]:
        """Eksik özellikleri belirle"""
        missing = []
        all_expected_features = (
            self.feature_mappings['air_quality_features'] +
            self.feature_mappings['pollen_features'] +
            self.feature_mappings['weather_features']
        )
        
        for feature in all_expected_features:
            if feature not in data or data[feature] == 0.0:
                missing.append(feature)
        
        return missing
    
    def prepare_model_input(self, lat: float, lon: float, 
                          target_datetime: Optional[datetime] = None,
                          user_modifiers: Optional[Dict] = None) -> np.ndarray:
        """
        Model için girdi dizisini hazırla
        Kullanıcı kişisel modifikasyonları dahil et
        """
        # Çevresel verileri al
        environmental_data = self.combine_environmental_data(lat, lon, target_datetime)
        
        # Temel özellik vektörünü oluştur
        feature_vector = []
        
        # Hava kalitesi özellikleri
        for feature in self.feature_mappings['air_quality_features']:
            value = environmental_data.get(feature, 0.0)
            feature_vector.append(value)
        
        # Polen özellikleri
        for feature in self.feature_mappings['pollen_features']:
            value = environmental_data.get(feature, 0.0)
            feature_vector.append(value)
        
        # Hava durumu özellikleri
        for feature in self.feature_mappings['weather_features']:
            value = environmental_data.get(feature, 0.0)
            feature_vector.append(value)
        
        # Kullanıcı modifikasyonları uygula
        if user_modifiers:
            feature_vector = self._apply_user_modifiers(feature_vector, user_modifiers)
        
        return np.array(feature_vector).reshape(1, -1)
    
    def _apply_user_modifiers(self, feature_vector: List[float], 
                            user_modifiers: Dict) -> List[float]:
     
        modified_vector = feature_vector.copy()
        
        # Temel hassasiyet modifikasyonu
        base_sensitivity = user_modifiers.get('base_sensitivity', 1.0)
        
        # Polen özelliklerini modifiye et (indeks 11-16 arası polen özellikleri)
        pollen_start_idx = len(self.feature_mappings['air_quality_features'])
        pollen_end_idx = pollen_start_idx + len(self.feature_mappings['pollen_features'])
        
        for i in range(pollen_start_idx, pollen_end_idx):
            if i < len(modified_vector):
                modified_vector[i] *= base_sensitivity
        
        # Çevresel amplifikatör
        env_amplifier = user_modifiers.get('environmental_amplifier', 1.0)
        
        # Hava kalitesi özelliklerini modifiye et
        air_quality_indices = list(range(len(self.feature_mappings['air_quality_features'])))
        for i in air_quality_indices:
            if i < len(modified_vector):
                modified_vector[i] *= env_amplifier
        
        # Mevsimsel modifikasyon
        seasonal_modifier = user_modifiers.get('seasonal_modifier', 1.0)
        
        # Polen UPI değerlerini modifiye et
        if pollen_start_idx < len(modified_vector):
            modified_vector[pollen_start_idx] *= seasonal_modifier  # upi_value
        
        return modified_vector
    
    def get_feature_names(self) -> List[str]:
        """Model özellik isimlerini döndür"""
        return (
            self.feature_mappings['air_quality_features'] +
            self.feature_mappings['pollen_features'] + 
            self.feature_mappings['weather_features']
        )


# Test fonksiyonları
def test_data_loader():
    """Veri yükleyicisini test et"""
    loader = DataLoader()
    
    print("=== VERİ YÜKLEYICI TEST ===")
    
    # Dosya validasyonu
    if not loader.validate_data_files():
        print("❌ Gerekli veri dosyaları eksik")
        return
    
    print("✅ Tüm veri dosyaları mevcut")
    
    # Test konumu (İstanbul)
    test_lat, test_lon = 41.0082, 28.9784
    test_datetime = datetime.now()
    
    # Çevresel veri test
    env_data = loader.combine_environmental_data(test_lat, test_lon, test_datetime)
    print(f"\n📊 Çevresel veri özeti:")
    print(f"  - Veri kalite skoru: {env_data['metadata']['data_quality_score']:.2f}")
    print(f"  - Eksik özellik sayısı: {len(env_data['metadata']['missing_features'])}")
    
    # Model girdi test
    model_input = loader.prepare_model_input(test_lat, test_lon, test_datetime)
    print(f"\n🔢 Model girdi boyutu: {model_input.shape}")
    print(f"  - Özellik sayısı: {len(loader.get_feature_names())}")
    
    return loader


if __name__ == "__main__":
    test_data_loader()