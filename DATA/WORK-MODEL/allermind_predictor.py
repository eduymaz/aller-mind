"""
AllerMind Ana Tahmin Sistemi
Grup tabanlı model aktivasyonu ve kişisel özellik entegrasyonu
"""

import pickle
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime
import os
import logging
from dataclasses import dataclass
import warnings

# Kendi modüllerimizi import et
from user_preference_system import AllergyGroupClassifier, UserPreferences
from data_loader import DataLoader

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PredictionResult:
    """Tahmin sonucu veri yapısı"""
    risk_score: float
    confidence: float
    risk_level: str  # low, moderate, high, severe
    group_id: int
    group_name: str
    
    # Detaylı bilgiler
    contributing_factors: Dict[str, float]
    recommendations: List[str]
    environmental_risks: Dict[str, float]
    personal_modifiers_applied: Dict[str, float]
    
    # Metadata
    prediction_timestamp: datetime
    data_quality_score: float
    model_version: str


class AllerMindPredictor:
    """
    Ana AllerMind tahmin sistemi
    Kullanıcı grubuna göre uygun modeli aktive eder ve kişisel özellikler ekler
    """
    
    def __init__(self, models_path: str = "/Users/elifdy/Desktop/allermind/aller-mind/DATA/MODEL/pkl_models"):
        self.models_path = models_path
        self.data_loader = DataLoader()
        self.group_classifier = AllergyGroupClassifier()
        
        # Model ve konfigürasyon yükleme
        self.models = {}
        self.scalers = {}
        self.ensemble_config = {}
        
        self._load_models()
        self._load_ensemble_config()
        
        # Risk seviye eşikleri
        self.risk_thresholds = {
            'low': 0.3,
            'moderate': 0.6,
            'high': 0.8,
            'severe': 0.9
        }
        
        # İmmunolojik faktör ağırlıkları
        self.immunologic_weights = {
            1: {  # Şiddetli Alerjik Grup
                'pollen_sensitivity': 2.0,
                'environmental_amplifier': 1.8,
                'cross_reactivity_bonus': 1.5,
                'weather_sensitivity': 1.6
            },
            2: {  # Hafif-Orta Alerjik Grup  
                'pollen_sensitivity': 1.3,
                'environmental_amplifier': 1.2,
                'cross_reactivity_bonus': 1.1,
                'weather_sensitivity': 1.2
            },
            3: {  # Genetik Yatkınlık Grubu
                'pollen_sensitivity': 1.5,
                'environmental_amplifier': 1.4,
                'cross_reactivity_bonus': 1.3,
                'weather_sensitivity': 1.1
            },
            4: {  # Teşhis Almamış Grup
                'pollen_sensitivity': 1.0,
                'environmental_amplifier': 1.0,
                'cross_reactivity_bonus': 1.0,
                'weather_sensitivity': 1.0
            },
            5: {  # Hassas Çocuk/Yaşlı Grubu
                'pollen_sensitivity': 1.8,
                'environmental_amplifier': 2.0,
                'cross_reactivity_bonus': 1.4,
                'weather_sensitivity': 1.7
            }
        }
    
    def _load_models(self):
        """Tüm grup modellerini yükle"""
        try:
            for group_id in range(1, 6):
                model_file = f"Grup{group_id}_model.pkl"
                scaler_file = f"Grup{group_id}_scaler.pkl"
                
                model_path = os.path.join(self.models_path, model_file)
                scaler_path = os.path.join(self.models_path, scaler_file)
                
                if os.path.exists(model_path) and os.path.exists(scaler_path):
                    with open(model_path, 'rb') as f:
                        self.models[group_id] = pickle.load(f)
                    
                    with open(scaler_path, 'rb') as f:
                        self.scalers[group_id] = pickle.load(f)
                    
                    logger.info(f"Grup {group_id} modeli yüklendi")
                else:
                    logger.warning(f"Grup {group_id} model dosyaları bulunamadı")
        
        except Exception as e:
            logger.error(f"Model yükleme hatası: {e}")
            self._create_fallback_models()
    
    def _load_ensemble_config(self):
        """Ensemble konfigürasyonunu yükle"""
        try:
            config_path = os.path.join(self.models_path, "ensemble_config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    self.ensemble_config = json.load(f)
                logger.info("Ensemble konfigürasyonu yüklendi")
            else:
                self._create_default_ensemble_config()
        except Exception as e:
            logger.error(f"Ensemble konfigürasyonu yükleme hatası: {e}")
            self._create_default_ensemble_config()
    
    def _create_fallback_models(self):
        """Modeller yüklenemediğinde basit fallback modeller oluştur"""
        logger.warning("Fallback modeller oluşturuluyor")
        
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler
        
        # Her grup için basit model oluştur
        for group_id in range(1, 6):
            # Basit Random Forest modeli
            model = RandomForestRegressor(n_estimators=10, random_state=42)
            scaler = StandardScaler()
            
            # Dummy veri ile fit et
            dummy_X = np.random.random((100, 25))  # 25 özellik
            dummy_y = np.random.random(100)
            
            scaler.fit(dummy_X)
            model.fit(scaler.transform(dummy_X), dummy_y)
            
            self.models[group_id] = model
            self.scalers[group_id] = scaler
    
    def _create_default_ensemble_config(self):
        """Varsayılan ensemble konfigürasyonu"""
        self.ensemble_config = {
            "models": {
                "1": {"weight": 0.18, "algorithm": "Random Forest"},
                "2": {"weight": 0.22, "algorithm": "RBF SVM"}, 
                "3": {"weight": 0.24, "algorithm": "RBF SVM"},
                "4": {"weight": 0.24, "algorithm": "RBF SVM"},
                "5": {"weight": 0.12, "algorithm": "RBF SVM"}
            },
            "confidence_threshold": 0.95,
            "version": "2.0"
        }
    
    def predict_allergy_risk(self, user_preferences: UserPreferences, 
                           location: Tuple[float, float],
                           target_datetime: Optional[datetime] = None) -> PredictionResult:
    
        
        if target_datetime is None:
            target_datetime = datetime.now()
        
        # 1. Grup belirleme
        group_result = self.group_classifier.determine_allergy_group(user_preferences)
        group_id = group_result['group_id']
        
        logger.info(f"Kullanıcı Grup {group_id} olarak sınıflandırıldı: {group_result['group_name']}")
        
        # 2. Model kontrolü
        if group_id not in self.models:
            logger.error(f"Grup {group_id} modeli bulunamadı")
            return self._create_error_result()
        
        # 3. Çevresel veri hazırlama
        lat, lon = location
        user_modifiers = group_result['personal_risk_modifiers']
        
        try:
            # Veri yükleme
            model_input = self.data_loader.prepare_model_input(
                lat, lon, target_datetime, user_modifiers
            )
            
            # Çevresel veri detayları
            environmental_data = self.data_loader.combine_environmental_data(lat, lon, target_datetime)
            
            # 4. Model tahmini
            prediction = self._execute_model_prediction(group_id, model_input)
            
            # 5. İmmunolojik modifikasyonlar uygula
            modified_prediction = self._apply_immunologic_modifiers(
                prediction, group_result, environmental_data
            )
            
            # 6. Risk seviyesi belirleme
            risk_level = self._determine_risk_level(modified_prediction)
            
            # 7. Güven aralığı hesaplama
            confidence = self._calculate_confidence(group_id, environmental_data)
            
            # 8. Katkı faktörlerini analiz et
            contributing_factors = self._analyze_contributing_factors(
                environmental_data, group_result
            )
            
            # 9. Önerileri oluştur
            recommendations = self._generate_recommendations(
                risk_level, group_result, environmental_data
            )
            
            # 10. Sonucu oluştur
            result = PredictionResult(
                risk_score=modified_prediction,
                confidence=confidence,
                risk_level=risk_level,
                group_id=group_id,
                group_name=group_result['group_name'],
                contributing_factors=contributing_factors,
                recommendations=recommendations,
                environmental_risks=self._extract_environmental_risks(environmental_data),
                personal_modifiers_applied=user_modifiers,
                prediction_timestamp=target_datetime,
                data_quality_score=environmental_data['metadata']['data_quality_score'],
                model_version=self.ensemble_config.get('version', '1.0')
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Tahmin hatası: {e}")
            return self._create_error_result()
    
    def _execute_model_prediction(self, group_id: int, model_input: np.ndarray) -> float:
        """Model tahminini çalıştır"""
        try:
            # Veriyi ölçekle
            scaled_input = self.scalers[group_id].transform(model_input)
            
            # Tahmin yap
            prediction = self.models[group_id].predict(scaled_input)[0]
            
            # 0-1 aralığında normalize et
            normalized_prediction = max(0.0, min(1.0, prediction))
            
            return normalized_prediction
            
        except Exception as e:
            logger.error(f"Model çalıştırma hatası: {e}")
            return 0.5  # Varsayılan orta risk
    
    def _apply_immunologic_modifiers(self, base_prediction: float, 
                                   group_result: Dict, 
                                   environmental_data: Dict) -> float:
        """İmmunolojik modifikasyonları uygula"""
        
        group_id = group_result['group_id']
        weights = self.immunologic_weights.get(group_id, self.immunologic_weights[4])
        
        modified_prediction = base_prediction
        
        # Polen hassasiyet modifikasyonu
        pollen_risk = self._calculate_pollen_risk_factor(environmental_data)
        if pollen_risk > 0.5:  # Yüksek polen riski
            pollen_modifier = 1.0 + (pollen_risk * weights['pollen_sensitivity'] - 1.0) * 0.3
            modified_prediction *= pollen_modifier
        
        # Çevresel amplifikatör
        env_risk = self._calculate_environmental_risk_factor(environmental_data)
        if env_risk > 0.6:  # Yüksek çevresel risk
            env_modifier = 1.0 + (env_risk * weights['environmental_amplifier'] - 1.0) * 0.2
            modified_prediction *= env_modifier
        
        # Çapraz reaksiyon bonusu
        cross_reactive_plants = group_result.get('pollen_specific_risks', {}).get('cross_reactive_foods', [])
        if cross_reactive_plants:
            cross_modifier = 1.0 + len(cross_reactive_plants) * 0.1 * weights['cross_reactivity_bonus']
            modified_prediction *= cross_modifier
        
        # Hava durumu hassasiyeti
        weather_severity = self._calculate_weather_severity(environmental_data)
        if weather_severity > 0.7:
            weather_modifier = 1.0 + (weather_severity * weights['weather_sensitivity'] - 1.0) * 0.15
            modified_prediction *= weather_modifier
        
        # Sonucu 0-1 aralığında tut
        return max(0.0, min(1.0, modified_prediction))
    
    def _calculate_pollen_risk_factor(self, environmental_data: Dict) -> float:
        """Polen risk faktörünü hesapla"""
        total_upi = environmental_data.get('total_upi', 0.0)
        in_season_count = environmental_data.get('in_season_count', 0)
        diversity_index = environmental_data.get('pollen_diversity_index', 0.0)
        
        # UPI tabanlı risk (0-5 arası UPI'ı 0-1'e normalize et)
        upi_risk = min(1.0, total_upi / 5.0)
        
        # Mevsim içi polen sayısı riski
        season_risk = min(1.0, in_season_count / 10.0)
        
        # Çeşitlilik riski
        diversity_risk = diversity_index
        
        # Ağırlıklı ortalama
        return (upi_risk * 0.5 + season_risk * 0.3 + diversity_risk * 0.2)
    
    def _calculate_environmental_risk_factor(self, environmental_data: Dict) -> float:
        """Çevresel risk faktörünü hesapla"""
        # Hava kalitesi parametreleri
        pm25 = environmental_data.get('pm2_5', 0.0)
        ozone = environmental_data.get('ozone', 0.0)
        no2 = environmental_data.get('nitrogen_dioxide', 0.0)
        
        # Risk skorları (WHO sınırlarına göre)
        pm25_risk = min(1.0, pm25 / 25.0)  # WHO günlük sınır: 15 µg/m³
        ozone_risk = min(1.0, ozone / 100.0)  # WHO 8-saatlik ortalama: 100 µg/m³
        no2_risk = min(1.0, no2 / 40.0)  # WHO yıllık ortalama: 40 µg/m³
        
        # Ağırlıklı ortalama
        return (pm25_risk * 0.4 + ozone_risk * 0.3 + no2_risk * 0.3)
    
    def _calculate_weather_severity(self, environmental_data: Dict) -> float:
        """Hava durumu şiddeti faktörünü hesapla"""
        # Alerjiyi tetikleyebilecek hava durumu koşulları
        humidity = environmental_data.get('relative_humidity_2m', 50.0)
        temperature = environmental_data.get('temperature_2m', 20.0)
        wind_speed = environmental_data.get('wind_speed_10m', 0.0)
        
        # Nem riski (çok yüksek veya çok düşük nem)
        humidity_risk = 0.0
        if humidity > 80 or humidity < 30:
            humidity_risk = min(1.0, abs(humidity - 55) / 45)
        
        # Sıcaklık riski (aşırı sıcaklık)
        temp_risk = 0.0
        if temperature > 30:
            temp_risk = min(1.0, (temperature - 30) / 20)
        
        # Rüzgar riski (polen taşıyıcı)
        wind_risk = min(1.0, wind_speed / 20.0)
        
        return (humidity_risk * 0.4 + temp_risk * 0.3 + wind_risk * 0.3)
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """Risk skoruna göre risk seviyesi belirle"""
        if risk_score >= self.risk_thresholds['severe']:
            return 'severe'
        elif risk_score >= self.risk_thresholds['high']:
            return 'high'
        elif risk_score >= self.risk_thresholds['moderate']:
            return 'moderate'
        else:
            return 'low'
    
    def _calculate_confidence(self, group_id: int, environmental_data: Dict) -> float:
        """Tahmin güven aralığını hesapla"""
        # Temel güven skoru (model performansına göre)
        model_performance = self.ensemble_config.get('models', {}).get(str(group_id), {})
        base_confidence = model_performance.get('performance', {}).get('r2', 0.8)
        
        # Veri kalitesi faktörü
        data_quality = environmental_data.get('metadata', {}).get('data_quality_score', 0.7)
        
        # Birleştirilmiş güven skoru
        combined_confidence = (base_confidence * 0.7 + data_quality * 0.3)
        
        return max(0.5, min(1.0, combined_confidence))
    
    def _analyze_contributing_factors(self, environmental_data: Dict, 
                                    group_result: Dict) -> Dict[str, float]:
        """Katkı faktörlerini analiz et"""
        factors = {}
        
        # Polen faktörleri
        factors['pollen_contribution'] = self._calculate_pollen_risk_factor(environmental_data)
        
        # Hava kalitesi faktörleri
        factors['air_quality_contribution'] = self._calculate_environmental_risk_factor(environmental_data)
        
        # Hava durumu faktörleri
        factors['weather_contribution'] = self._calculate_weather_severity(environmental_data)
        
        # Kişisel risk faktörleri
        personal_modifiers = group_result.get('personal_risk_modifiers', {})
        factors['personal_sensitivity'] = personal_modifiers.get('base_sensitivity', 1.0) - 1.0
        factors['environmental_amplification'] = personal_modifiers.get('environmental_amplifier', 1.0) - 1.0
        
        return factors
    
    def _generate_recommendations(self, risk_level: str, group_result: Dict, 
                                environmental_data: Dict) -> List[str]:
        """Risk seviyesi ve grup bilgisine göre öneriler üret"""
        recommendations = []
        
        # Risk seviyesi bazlı öneriler
        if risk_level == 'severe':
            recommendations.extend([
                "🚨 ACİL: Dışarı çıkmayın, ilaçlarınızı kontrol edin",
                "💊 Acil ilaç (epinefrin) yanınızda olsun",
                "🏥 Gerekirse sağlık kuruluşuna başvurun"
            ])
        elif risk_level == 'high':
            recommendations.extend([
                "⚠️ Dışarı çıkmadan önce maske takın",
                "💊 Antihistaminik alın",
                "🪟 Pencere ve kapıları kapalı tutun"
            ])
        elif risk_level == 'moderate':
            recommendations.extend([
                "😷 Dış ortamda maske kullanmayı düşünün",
                "⏰ Sabah erken veya akşam saatlerini tercih edin",
                "🚿 Eve döndüğünüzde duş alın"
            ])
        else:  # low
            recommendations.extend([
                "😊 Dış ortam aktiviteleri için uygun",
                "🌳 Park ve bahçe aktivitelerini güvenle yapabilirsiniz"
            ])
        
        # Polen özel öneriler
        high_risk_pollens = group_result.get('pollen_specific_risks', {}).get('high_risk_pollens', [])
        if high_risk_pollens:
            recommendations.append(f"🌿 Dikkat: {', '.join(high_risk_pollens)} polenlerine karşı ekstra tedbirli olun")
        
        # Çapraz reaktif besinler
        cross_foods = group_result.get('pollen_specific_risks', {}).get('cross_reactive_foods', [])
        if cross_foods:
            recommendations.append(f"🍎 Çapraz reaksiyon riski: {', '.join(cross_foods)} tüketiminde dikkatli olun")
        
        # Grup özel öneriler
        group_id = group_result['group_id']
        if group_id == 1:  # Şiddetli alerjik
            recommendations.append("⚕️ Düzenli hekim kontrolü ve immünoterapi değerlendirmesi")
        elif group_id == 5:  # Hassas grup
            recommendations.append("👶👴 Yaş grubunuz nedeniyle ekstra dikkatli olun")
        
        return recommendations
    
    def _extract_environmental_risks(self, environmental_data: Dict) -> Dict[str, float]:
        """Çevresel risk faktörlerini çıkar"""
        return {
            'pm2_5_level': environmental_data.get('pm2_5', 0.0),
            'ozone_level': environmental_data.get('ozone', 0.0),
            'pollen_upi': environmental_data.get('total_upi', 0.0),
            'humidity_level': environmental_data.get('relative_humidity_2m', 0.0),
            'temperature': environmental_data.get('temperature_2m', 0.0)
        }
    
    def _create_error_result(self) -> PredictionResult:
        """Hata durumunda varsayılan sonuç oluştur"""
        return PredictionResult(
            risk_score=0.5,
            confidence=0.3,
            risk_level='moderate',
            group_id=4,
            group_name='Teşhis Almamış Grup',
            contributing_factors={'error': 1.0},
            recommendations=["❌ Sistem hatası oluştu, lütfen tekrar deneyin"],
            environmental_risks={},
            personal_modifiers_applied={},
            prediction_timestamp=datetime.now(),
            data_quality_score=0.0,
            model_version='error'
        )
    
    def batch_predict(self, users_data: List[Dict], 
                     locations: List[Tuple[float, float]],
                     target_datetime: Optional[datetime] = None) -> List[PredictionResult]:
        """Çoklu kullanıcı için toplu tahmin"""
        results = []
        
        for user_data, location in zip(users_data, locations):
            try:
                # UserPreferences nesnesini oluştur
                user_prefs = UserPreferences(**user_data)
                
                # Tahmin yap
                result = self.predict_allergy_risk(user_prefs, location, target_datetime)
                results.append(result)
                
            except Exception as e:
                logger.error(f"Toplu tahmin hatası: {e}")
                results.append(self._create_error_result())
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """Model bilgilerini döndür"""
        return {
            'loaded_models': list(self.models.keys()),
            'ensemble_config': self.ensemble_config,
            'data_loader_features': self.data_loader.get_feature_names(),
            'risk_thresholds': self.risk_thresholds,
            'immunologic_weights': self.immunologic_weights
        }


# Test fonksiyonları
def create_test_user() -> UserPreferences:
    """Test kullanıcısı oluştur"""
    return UserPreferences(
        age=35,
        gender='female',
        location={'latitude': 41.0082, 'longitude': 28.9784},
        clinical_diagnosis='mild_moderate_allergy',
        family_allergy_history=True,
        previous_allergic_reactions={
            'anaphylaxis': False,
            'severe_asthma': True,
            'hospitalization': False
        },
        current_medications=['antihistamine', 'nasal_spray'],
        tree_pollen_allergy={
            'birch': True,
            'olive': False,
            'pine': False
        },
        grass_pollen_allergy={
            'graminales': True
        },
        weed_pollen_allergy={
            'ragweed': True,
            'mugwort': False
        },
        food_allergies={
            'apple': True,
            'nuts': False,
            'shellfish': False
        },
        environmental_triggers={
            'dust_mites': True,
            'pet_dander': False,
            'mold': True,
            'air_pollution': True,
            'smoke': True
        }
    )


def test_predictor():
    """Tahmin sistemini test et"""
    print("=== ALLERMİND TAHMİN SİSTEMİ TEST ===")
    
    # Predictor oluştur
    predictor = AllerMindPredictor()
    
    # Test kullanıcısı
    test_user = create_test_user()
    
    # Test konumu (İstanbul)
    test_location = (41.0082, 28.9784)
    
    # Tahmin yap
    result = predictor.predict_allergy_risk(test_user, test_location)
    
    # Sonuçları yazdır
    print(f"\n📊 TAHMİN SONUÇLARI:")
    print(f"Risk Skoru: {result.risk_score:.3f}")
    print(f"Risk Seviyesi: {result.risk_level.upper()}")
    print(f"Güven Aralığı: {result.confidence:.2f}")
    print(f"Grup: {result.group_name} (ID: {result.group_id})")
    
    print(f"\n🧬 KATKIDA BULUNAN FAKTÖRLER:")
    for factor, value in result.contributing_factors.items():
        print(f"  {factor}: {value:.3f}")
    
    print(f"\n💡 ÖNERİLER:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"  {i}. {rec}")
    
    print(f"\n🌡️ ÇEVRESEL RİSKLER:")
    for risk, value in result.environmental_risks.items():
        print(f"  {risk}: {value:.2f}")
    
    return predictor


if __name__ == "__main__":
    test_predictor()