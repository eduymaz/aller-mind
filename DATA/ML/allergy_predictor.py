import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import json

class AllergyGroupPredictor:
    """
    5 farklı allerji grubu için özelleştirilmiş tahmin modeli
    """
    
    def __init__(self):
        self.groups = {
            1: "Şiddetli Alerjik Grup",
            2: "Hafif-Orta Grup", 
            3: "Olası Alerjik Grup/Genetiğinde Olan",
            4: "Henüz Teşhis Almamış/İhtimali Bilinmeyen Grup",
            5: "Alerjisi Olmayan + İhtimali Bilinmeyen Ama Hassas Grup"
        }
        
        # Her grup için özellik ağırlıkları
        self.group_weights = self._define_group_weights()
        
        # Model ve scaler'lar her grup için
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        
    def _define_group_weights(self) -> Dict[int, Dict[str, float]]:
        """
        Her allerji grubu için parametrelerin önem ağırlıklarını tanımla
        """
        weights = {
            # Grup 1: Şiddetli Alerjik Grup - Polen ve hava kalitesine çok hassas
            1: {
                'pollen_importance': 0.40,      # En yüksek polen hassasiyeti
                'air_quality_importance': 0.35, # Yüksek hava kalitesi hassasiyeti
                'weather_importance': 0.25,     # Hava durumu da önemli
                'seasonal_factor': 2.0,         # Mevsimsel etkiler çok önemli
                'plant_proximity_factor': 2.5,  # Bitki yakınlığı kritik
                'sensitivity_threshold': 0.2    # Çok düşük tolerans
            },
            
            # Grup 2: Hafif-Orta Grup - Dengeli hassasiyet
            2: {
                'pollen_importance': 0.30,
                'air_quality_importance': 0.30,
                'weather_importance': 0.40,
                'seasonal_factor': 1.5,
                'plant_proximity_factor': 1.8,
                'sensitivity_threshold': 0.4
            },
            
            # Grup 3: Olası Alerjik Grup - Genetik yatkınlık, orta hassasiyet
            3: {
                'pollen_importance': 0.35,
                'air_quality_importance': 0.25,
                'weather_importance': 0.40,
                'seasonal_factor': 1.7,
                'plant_proximity_factor': 2.0,
                'sensitivity_threshold': 0.3
            },
            
            # Grup 4: Teşhis Almamış - Belirsizlik, temkinli yaklaşım
            4: {
                'pollen_importance': 0.25,
                'air_quality_importance': 0.35,
                'weather_importance': 0.40,
                'seasonal_factor': 1.3,
                'plant_proximity_factor': 1.5,
                'sensitivity_threshold': 0.5
            },
            
            # Grup 5: Hassas Grup (Çocuk/Yaşlı) - Genel hava kalitesi odaklı
            5: {
                'pollen_importance': 0.20,
                'air_quality_importance': 0.45,  # En yüksek hava kalitesi odağı
                'weather_importance': 0.35,
                'seasonal_factor': 1.2,
                'plant_proximity_factor': 1.0,
                'sensitivity_threshold': 0.6
            }
        }
        
        print("✅ Grup ağırlıkları tanımlandı:")
        for group_id, group_name in self.groups.items():
            print(f"   Grup {group_id}: {group_name}")
            w = weights[group_id]
            print(f"      📊 Polen: {w['pollen_importance']:.1%}, "
                  f"Hava Kalitesi: {w['air_quality_importance']:.1%}, "
                  f"Hava Durumu: {w['weather_importance']:.1%}")
        
        return weights
    
    def create_composite_risk_score(self, df: pd.DataFrame, group_id: int) -> np.ndarray:
        """
        Belirtilen grup için bileşik risk skoru oluştur
        """
        weights = self.group_weights[group_id]
        
        # Polen riski hesapla
        pollen_risk = self._calculate_pollen_risk(df, weights)
        
        # Hava kalitesi riski hesapla
        air_quality_risk = self._calculate_air_quality_risk(df, weights)
        
        # Hava durumu riski hesapla
        weather_risk = self._calculate_weather_risk(df, weights)
        
        # Bileşik risk skoru
        composite_risk = (
            pollen_risk * weights['pollen_importance'] +
            air_quality_risk * weights['air_quality_importance'] +
            weather_risk * weights['weather_importance']
        )
        
        return composite_risk
    
    def _calculate_pollen_risk(self, df: pd.DataFrame, weights: Dict[str, float]) -> np.ndarray:
        """Polen riski hesapla"""
        # UPI değeri normalize et (1-5 arası)
        upi_normalized = (df['upi_value'] - 1) / 4
        plant_upi_normalized = (df['plant_upi_value'] - 1) / 4
        
        # Mevsimsel etki
        seasonal_multiplier = np.where(
            (df['in_season'] == True) & (df['plant_in_season'] == True),
            weights['seasonal_factor'],
            1.0
        )
        
        # Polen türü ağırlığı
        pollen_type_weight = df['pollen_code'].map({
            'WEED': 1.2,    # Yabani ot poleni en zararlı
            'GRASS': 1.0,   # Çim poleni orta
            'TREE': 0.8     # Ağaç poleni nispeten daha az
        }).fillna(1.0)
        
        # Bitki türü ağırlığı
        plant_type_weight = df['plant_code'].map({
            'RAGWEED': 1.3,   # En alerjik bitki
            'MUGWORT': 1.2,   # Yüksek alerjik
            'GRAMINALES': 1.0, # Orta alerjik
            'BIRCH': 0.9,     # Düşük alerjik
            'OLIVE': 0.7      # En düşük alerjik
        }).fillna(1.0)
        
        # Final polen riski
        pollen_risk = (
            (upi_normalized * 0.6 + plant_upi_normalized * 0.4) *
            seasonal_multiplier *
            pollen_type_weight *
            plant_type_weight *
            weights['plant_proximity_factor']
        )
        
        return np.clip(pollen_risk, 0, 1)
    
    def _calculate_air_quality_risk(self, df: pd.DataFrame, weights: Dict[str, float]) -> np.ndarray:
        """Hava kalitesi riski hesapla"""
        # WHO standartlarına göre normalize et
        pm10_risk = np.clip(df['pm10'] / 50, 0, 2)  # WHO günlük limit 50
        pm25_risk = np.clip(df['pm2_5'] / 25, 0, 2)  # WHO günlük limit 25
        
        no2_risk = np.clip(df['nitrogen_dioxide'] / 40, 0, 2)  # WHO yıllık limit 40
        so2_risk = np.clip(df['sulphur_dioxide'] / 20, 0, 2)   # WHO günlük limit 20
        ozone_risk = np.clip(df['ozone'] / 100, 0, 2)          # WHO 8-saatlik limit 100
        
        co_risk = np.clip(df['carbon_monoxide'] / 10000, 0, 2) # WHO 8-saatlik limit 10mg/m3
        
        # Ağırlıklı ortalama
        air_quality_risk = (
            pm25_risk * 0.25 +    # PM2.5 en zararlı
            pm10_risk * 0.20 +    # PM10 ikinci sırada
            ozone_risk * 0.20 +   # Ozon önemli
            no2_risk * 0.15 +     # NO2 orta
            so2_risk * 0.10 +     # SO2 düşük
            co_risk * 0.10        # CO en düşük
        )
        
        return np.clip(air_quality_risk, 0, 1)
    
    def _calculate_weather_risk(self, df: pd.DataFrame, weights: Dict[str, float]) -> np.ndarray:
        """Hava durumu riski hesapla"""
        # Sıcaklık riski (25-30°C optimal, dışında artan risk)
        temp_risk = np.where(
            (df['temperature_2m'] < 15) | (df['temperature_2m'] > 35),
            0.8,
            np.where(
                (df['temperature_2m'] < 20) | (df['temperature_2m'] > 30),
                0.4,
                0.1
            )
        )
        
        # Nem riski (40-60% optimal)
        humidity_risk = np.where(
            (df['relative_humidity_2m'] < 30) | (df['relative_humidity_2m'] > 80),
            0.6,
            np.where(
                (df['relative_humidity_2m'] < 40) | (df['relative_humidity_2m'] > 70),
                0.3,
                0.0
            )
        )
        
        # Rüzgar hızı (yüksek rüzgar polen dağılımını artırır)
        wind_risk = np.clip(df['wind_speed_10m'] / 20, 0, 1)  # 20 m/s üzeri maksimum risk
        
        # UV indeksi riski
        uv_risk = np.where(
            df['uv_index'] > 8, 0.8,
            np.where(df['uv_index'] > 5, 0.4, 0.1)
        )
        
        # Yağış (düşük yağış polen konsantrasyonunu artırır)
        rain_benefit = np.where(df['precipitation'] > 0.1, -0.3, 0)  # Yağış riski azaltır
        
        weather_risk = (
            temp_risk * 0.3 +
            humidity_risk * 0.25 +
            wind_risk * 0.2 +
            uv_risk * 0.15 +
            rain_benefit * 0.1
        )
        
        return np.clip(weather_risk, 0, 1)
    
    def calculate_safe_time_hours(self, risk_score: float, group_id: int) -> float:
        """
        Risk skoruna ve gruba göre güvenli vakit geçirme süresi hesapla (saat cinsinden)
        """
        threshold = self.group_weights[group_id]['sensitivity_threshold']
        
        if risk_score <= threshold:
            # Düşük risk: 6-8 saat güvenli
            safe_hours = 8 - (risk_score / threshold) * 2
        elif risk_score <= threshold * 1.5:
            # Orta risk: 2-4 saat güvenli
            safe_hours = 4 - ((risk_score - threshold) / (threshold * 0.5)) * 2
        elif risk_score <= threshold * 2:
            # Yüksek risk: 0.5-1 saat güvenli
            safe_hours = 1 - ((risk_score - threshold * 1.5) / (threshold * 0.5)) * 0.5
        else:
            # Çok yüksek risk: Dışarı çıkma önerilmez
            safe_hours = 0.0
        
        return max(0.0, safe_hours)
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Model için özellikleri hazırla
        """
        feature_df = df.copy()
        
        # Kategorik değişkenleri encode et
        categorical_columns = ['pollen_code', 'plant_code', 'in_season', 'plant_in_season']
        
        for col in categorical_columns:
            if col in feature_df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    feature_df[f'{col}_encoded'] = self.label_encoders[col].fit_transform(
                        feature_df[col].astype(str)
                    )
                else:
                    feature_df[f'{col}_encoded'] = self.label_encoders[col].transform(
                        feature_df[col].astype(str)
                    )
        
        # Zaman özellikleri oluştur
        if 'time' in feature_df.columns:
            feature_df['time'] = pd.to_datetime(feature_df['time'])
            feature_df['hour'] = feature_df['time'].dt.hour
            feature_df['day_of_year'] = feature_df['time'].dt.dayofyear
        
        # Özellik kolonlarını seç
        feature_columns = [
            # Hava durumu
            'temperature_2m', 'relative_humidity_2m', 'precipitation',
            'wind_speed_10m', 'wind_direction_10m', 'uv_index',
            
            # Hava kalitesi
            'pm10', 'pm2_5', 'nitrogen_dioxide', 'sulphur_dioxide', 'ozone',
            'carbon_monoxide', 'methane',
            
            # Polen
            'upi_value', 'plant_upi_value',
            'pollen_code_encoded', 'plant_code_encoded',
            'in_season_encoded', 'plant_in_season_encoded',
            
            # Zaman
            'hour', 'day_of_year'
        ]
        
        # Sadece mevcut kolonları al
        available_features = [col for col in feature_columns if col in feature_df.columns]
        
        return feature_df[available_features], available_features
    
    def train_group_models(self, df: pd.DataFrame):
        """
        Her grup için ayrı model eğit
        """
        print("🤖 Grup modellerini eğitiyor...")
        
        # Özellikleri hazırla
        feature_df, feature_columns = self.prepare_features(df)
        
        for group_id in range(1, 6):
            print(f"\n📚 Grup {group_id} modeli eğitiliyor: {self.groups[group_id]}")
            
            # Bu grup için risk skoru hesapla
            risk_scores = self.create_composite_risk_score(df, group_id)
            
            # Güvenli vakit sürelerini hesapla
            safe_times = np.array([
                self.calculate_safe_time_hours(risk, group_id) for risk in risk_scores
            ])
            
            # Veriyi böl
            X_train, X_test, y_train, y_test = train_test_split(
                feature_df, safe_times, test_size=0.2, random_state=42
            )
            
            # Özellik ölçekleme
            self.scalers[group_id] = StandardScaler()
            X_train_scaled = self.scalers[group_id].fit_transform(X_train)
            X_test_scaled = self.scalers[group_id].transform(X_test)
            
            # Model eğitimi
            self.models[group_id] = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
            
            self.models[group_id].fit(X_train_scaled, y_train)
            
            # Model değerlendirmesi
            y_pred = self.models[group_id].predict(X_test_scaled)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            print(f"   ✅ RMSE: {rmse:.3f}, R²: {r2:.3f}")
            print(f"   📈 Ortalama güvenli süre: {safe_times.mean():.2f} saat")
            print(f"   📊 Risk skoru aralığı: {risk_scores.min():.3f} - {risk_scores.max():.3f}")
        
        print("\n🎯 Tüm grup modelleri eğitimi tamamlandı!")
    
    def predict_safe_time(self, input_data: Dict[str, Any], group_id: int) -> Dict[str, Any]:
        """
        Belirtilen grup için güvenli vakit tahmin et
        """
        if group_id not in self.models:
            raise ValueError(f"Grup {group_id} için model henüz eğitilmemiş!")
        
        # Input dataframe oluştur
        input_df = pd.DataFrame([input_data])
        
        # Özellikleri hazırla
        feature_df, _ = self.prepare_features(input_df)
        
        # Ölçekle
        feature_scaled = self.scalers[group_id].transform(feature_df)
        
        # Tahmin yap
        predicted_hours = self.models[group_id].predict(feature_scaled)[0]
        
        # Risk skoru hesapla
        risk_score = self.create_composite_risk_score(input_df, group_id)[0]
        
        # Öneri oluştur
        recommendation = self._generate_recommendation(predicted_hours, risk_score, group_id)
        
        return {
            'group_id': group_id,
            'group_name': self.groups[group_id],
            'predicted_safe_hours': round(predicted_hours, 2),
            'risk_score': round(risk_score, 3),
            'recommendation': recommendation,
            'risk_level': self._get_risk_level(risk_score, group_id)
        }
    
    def _generate_recommendation(self, hours: float, risk_score: float, group_id: int) -> str:
        """Tavsiye metni oluştur"""
        threshold = self.group_weights[group_id]['sensitivity_threshold']
        
        if hours >= 6:
            return f"🟢 Harika! {hours:.1f} saat güvenle dışarıda vakit geçirebilirsiniz."
        elif hours >= 3:
            return f"🟡 {hours:.1f} saat kadar dışarıda olabilirsiniz. Dikkatli olun."
        elif hours >= 1:
            return f"🟠 Sadece {hours:.1f} saat kısa süreli dışarı çıkış önerilir."
        else:
            return "🔴 Dışarı çıkma önerilmez. İç mekanda kalın."
    
    def _get_risk_level(self, risk_score: float, group_id: int) -> str:
        """Risk seviyesi belirle"""
        threshold = self.group_weights[group_id]['sensitivity_threshold']
        
        if risk_score <= threshold:
            return "Düşük"
        elif risk_score <= threshold * 1.5:
            return "Orta"
        elif risk_score <= threshold * 2:
            return "Yüksek"
        else:
            return "Çok Yüksek"
    
    def save_models(self, base_path: str):
        """Modelleri kaydet"""
        import os
        os.makedirs(base_path, exist_ok=True)
        
        # Modelleri kaydet
        for group_id in self.models:
            model_path = f"{base_path}/group_{group_id}_model.pkl"
            scaler_path = f"{base_path}/group_{group_id}_scaler.pkl"
            
            with open(model_path, 'wb') as f:
                pickle.dump(self.models[group_id], f)
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scalers[group_id], f)
        
        # Label encoder'ları kaydet
        encoder_path = f"{base_path}/label_encoders.pkl"
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoders, f)
        
        # Grup ağırlıklarını kaydet
        weights_path = f"{base_path}/group_weights.json"
        with open(weights_path, 'w') as f:
            json.dump(self.group_weights, f, indent=2)
        
        print(f"💾 Modeller kaydedildi: {base_path}")

if __name__ == "__main__":
    # Temizlenmiş veriyi yükle
    data_path = '/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/cleaned_combined_data.csv'
    df = pd.read_csv(data_path)
    
    # Predictor oluştur ve eğit
    predictor = AllergyGroupPredictor()
    predictor.train_group_models(df)
    
    # Modelleri kaydet
    predictor.save_models('/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/models')
