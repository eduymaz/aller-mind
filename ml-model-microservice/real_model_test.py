#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllerMind Allergy Risk Prediction REST API
Modern production-ready REST API service for allergy risk prediction
Integrates with WORK-MODEL system components
"""

import os
import sys
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import asdict

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

# Expert Prediction Result Class
class ExpertPredictionResult:
    """Result class for Expert Prediction System"""
    def __init__(self, risk_score: float, confidence: float, risk_level: str, 
                 group_id: int, group_name: str, contributing_factors: Dict,
                 recommendations: List[str], environmental_risks: Dict,
                 personal_modifiers_applied: Dict, prediction_timestamp: datetime,
                 data_quality_score: float = 1.0, model_version: str = "Expert-v2.0"):
        self.risk_score = risk_score
        self.confidence = confidence
        self.risk_level = risk_level
        self.group_id = group_id
        self.group_name = group_name
        self.contributing_factors = contributing_factors
        self.recommendations = recommendations
        self.environmental_risks = environmental_risks
        self.personal_modifiers_applied = personal_modifiers_applied
        self.prediction_timestamp = prediction_timestamp
        self.data_quality_score = data_quality_score
        self.model_version = model_version

# Import AllerMind Expert Predictor (New Model System)
expert_model_path = os.path.join(os.path.dirname(__file__), 'DATA', 'MODEL', 'version2_pkl_models')
if expert_model_path not in sys.path:
    sys.path.insert(0, expert_model_path)

try:
    from expert_predictor import ExpertAllermindPredictor
except ImportError as e:
    print(f"❌ Expert predictor import hatası: {e}")
    print(f"Path: {expert_model_path}")
    print("Lütfen DATA/MODEL/version2_pkl_models klasöründeki dosyaların mevcut olduğundan emin olun.")
    
    # List available files for debugging
    if os.path.exists(expert_model_path):
        print(f"Expert model klasöründeki dosyalar: {os.listdir(expert_model_path)}")
    else:
        print(f"Expert model klasörü bulunamadı: {expert_model_path}")
    sys.exit(1)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("🚀 AllerMind REST API başlatılıyor...")

app = Flask(__name__)
CORS(app)

print("✅ Flask ve CORS başlatıldı")

class AllerMindRiskPredictor:
    """
    Production-ready allergy risk prediction service
    Integrates Expert Prediction System v2.0 for real-time risk assessment
    """
    
    def __init__(self):
        """Initialize prediction service with Expert Predictor"""
        logger.info("🤖 AllerMind Expert Risk Predictor başlatılıyor...")
        
        try:
            # Initialize Expert Predictor (new model system)
            self.predictor = ExpertAllermindPredictor()
            
            # Model grupları (Flutter uygulaması ile uyumlu)
            self.model_groups = {
                1: "Model 1",
                2: "Model 2", 
                3: "Model 3",
                4: "Model 4",
                5: "Model 5"
            }
            
            # Validate system readiness
            self._validate_system()
            
            logger.info("✅ Expert Prediction System başarıyla başlatıldı")
            
        except Exception as e:
            logger.error(f"❌ Expert sistem başlatma hatası: {e}")
            raise
    
    def _validate_system(self):
        """Validate Expert Predictor is ready"""
        # Check if models are loaded
        if not hasattr(self.predictor, 'models') or not self.predictor.models:
            raise Exception("Expert modeller yüklenmedi")
        
        loaded_models = list(self.predictor.models.keys())
        logger.info(f"📊 {len(loaded_models)} expert model hazır: {loaded_models}")
    

    
    def predict_allergy_risk(self, request_data: Dict) -> Dict[str, Any]:
        """
        Main prediction method that processes API request and returns risk assessment
        
        Args:
            request_data: API request containing user classification from microservice and environmental data
            
        Returns:
            Dict containing risk prediction results
        """
        try:
            logger.info("🔍 Risk tahmini başlatılıyor...")
            
            # Extract and validate required data
            user_classification = request_data.get('userClassification', {})
            environmental_data = request_data.get('environmentalData', {})
            
            # Validate required fields - userClassification from microservice
            if not user_classification:
                raise ValueError("Kullanıcı sınıflandırma bilgisi (userClassification) gerekli")
            
            # Get allergy group from classification response
            allergy_group = user_classification.get('groupId')
            if allergy_group is None:
                raise ValueError("userClassification içinde groupId gerekli")
            
            if not isinstance(allergy_group, int) or allergy_group < 1 or allergy_group > 5:
                raise ValueError("groupId 1-5 arasında bir sayı olmalı")
            
            # Environmental data is required for REST API
            if not environmental_data:
                raise ValueError("Çevresel veri (environmentalData) gerekli")
            
            logger.info(f"👤 Kullanıcı grubu: {allergy_group} - {user_classification.get('groupName', 'Unknown')}")
            logger.info(f"🏥 Mikroservisten gelen sınıflandırma: {user_classification.get('assignmentReason', 'No reason')}")
            logger.info(f"🌡️ Çevresel veri alındı: {len(environmental_data)} parametre")
            
            # Use provided environmental data for prediction
            prediction_result = self._predict_with_environmental_data(
                user_classification=user_classification,
                environmental_data=environmental_data
            )
            
            # Format response
            response = self._format_prediction_response(prediction_result, user_classification)
            
            logger.info(f"✅ Tahmin tamamlandı - Risk: {response['riskScore']:.3f}")
            return response
            
        except Exception as e:
            logger.error(f"❌ Risk tahmini hatası: {e}")
            logger.error(traceback.format_exc())
            raise
    
    def _format_prediction_response(self, prediction_result: ExpertPredictionResult, user_classification: Dict[str, Any]) -> Dict[str, Any]:
        """Format prediction result for API response"""
        try:
            return {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'riskScore': float(prediction_result.risk_score),
                'riskLevel': prediction_result.risk_level,
                'confidence': float(prediction_result.confidence),
                'userGroup': {
                    'groupId': prediction_result.group_id,
                    'groupName': prediction_result.group_name,
                    'description': user_classification.get('groupDescription', f'Group {prediction_result.group_id} characteristics'),
                    'assignmentReason': user_classification.get('assignmentReason', 'Microservice classification'),
                    'modelWeight': user_classification.get('modelWeight', 1.0)
                },
                'contributingFactors': prediction_result.contributing_factors,
                'recommendations': prediction_result.recommendations,
                'environmentalRisks': prediction_result.environmental_risks,
                'personalModifiers': prediction_result.personal_modifiers_applied,
                'immunologicProfile': user_classification.get('immunologicProfile', {}),
                'environmentalSensitivityFactors': user_classification.get('environmentalSensitivityFactors', {}),
                'pollenSpecificRisks': user_classification.get('pollenSpecificRisks', {}),
                'dataQualityScore': float(prediction_result.data_quality_score),
                'modelVersion': prediction_result.model_version,
                'predictionTimestamp': prediction_result.prediction_timestamp.isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Response formatlanma hatası: {e}")
            return {
                'success': False,
                'error': f"Response formatlanma hatası: {e}",
                'timestamp': datetime.now().isoformat()
            }
    
    def _predict_with_environmental_data(self, user_classification: Dict[str, Any], 
                                       environmental_data: Dict[str, Any]) -> ExpertPredictionResult:
        """
        REST API için özel tahmin metodu - mikroservisten gelen kullanıcı sınıflandırması ve çevresel veri kullanır
        
        Args:
            user_classification: Mikroservisten gelen AllergyClassificationResponse
            environmental_data: REST request'ten gelen çevresel veri
            
        Returns:
            PredictionResult: Tahmin sonucu
        """
        try:
            # 1. Grup bilgisini user classification'dan al
            group_id = user_classification.get('groupId')
            
            logger.info(f"👤 Kullanıcı Grup {group_id} - Mikroservisten alındı")
            
            # 2. Model kontrolü
            if group_id not in self.predictor.models:
                logger.warning(f"⚠️ Grup {group_id} için model bulunamadı, fallback kullanılıyor")
                group_id = 4  # Varsayılan grup
            
            # 3. Environmental data'yı Expert Predictor formatına dönüştür
            expert_environmental_data = self._convert_to_expert_environmental_data(environmental_data)
            
            # 4. User classification'dan personal parameters oluştur
            personal_params = self._convert_to_personal_params(user_classification)
            
            logger.info(f"📋 Expert model için grup {group_id} kullanılıyor")
            logger.info(f"🔧 Personal parameters hazırlandı")
            
            # 5. Expert Predictor ile tahmin yap
            group_result = self.predictor.predict_group(
                expert_environmental_data, 
                group_id, 
                personal_params
            )
            
            if not group_result:
                raise Exception(f"Grup {group_id} için tahmin yapılamadı")
            
            # 6. Ensemble tahmin de yap (güven için)
            ensemble_result = self.predictor.predict_ensemble(
                expert_environmental_data,
                personal_params
            )
            
            # 7. Risk faktörlerini çıkar
            contributing_factors = self._extract_contributing_factors(expert_environmental_data, user_classification)
            environmental_risks = self._extract_environmental_risks(expert_environmental_data)
            recommendations = self._generate_recommendations(group_result, user_classification)
            
            # 8. Expert sonucunu ExpertPredictionResult formatına dönüştür
            return ExpertPredictionResult(
                risk_score=float(group_result['risk_score']),
                confidence=float(ensemble_result['ensemble_prediction']['confidence']),
                risk_level=group_result['risk_level'],
                group_id=group_id,
                group_name=group_result['group_name'],
                contributing_factors=contributing_factors,
                recommendations=recommendations,
                environmental_risks=environmental_risks,
                personal_modifiers_applied={
                    'personal_multiplier': group_result['personal_multiplier'],
                    'base_safe_hours': group_result['base_safe_hours'],
                    'personal_safe_hours': group_result['personal_safe_hours']
                },
                prediction_timestamp=datetime.now(),
                data_quality_score=1.0,
                model_version="Expert-v2.0"
            )
            
        except Exception as e:
            logger.error(f"❌ Expert predictor ile tahmin hatası: {e}")
            raise
    
    def _convert_to_expert_environmental_data(self, environmental_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        REST API'den gelen environmental data'yı Expert Predictor formatına çevir
        
        Args:
            environmental_data: REST request'ten gelen çevresel veri
            
        Returns:
            Dict[str, Any]: Expert Predictor için uygun format
        """
        try:
            air_quality_data = environmental_data.get('airQuality', {})
            pollen_data = environmental_data.get('pollen', {})
            weather_data = environmental_data.get('weather', {})
            
            # Expert Predictor'in beklediği formatta çevresel veri oluştur
            expert_data = {
                # Hava kalitesi
                'pm10': float(air_quality_data.get('pm10', 20.0)),
                'pm2_5': float(air_quality_data.get('pm25', 12.0)),  # REST API'de pm25
                'ozone': float(air_quality_data.get('o3', 100.0)),   # REST API'de o3
                'nitrogen_dioxide': float(air_quality_data.get('no2', 20.0)),
                'sulphur_dioxide': float(air_quality_data.get('so2', 10.0)),
                'carbon_monoxide': float(air_quality_data.get('co', 1.0)),
                'carbon_dioxide': float(air_quality_data.get('co2', 400.0)),
                
                # Hava durumu
                'temperature_2m': float(weather_data.get('temperature', 22.0)),
                'relative_humidity_2m': float(weather_data.get('humidity', 55.0)),
                'precipitation': float(weather_data.get('precipitation', 0.0)),
                'wind_speed_10m': float(weather_data.get('windSpeed', 5.0)),
                'surface_pressure': float(weather_data.get('pressure', 1013.0)),
                'uv_index': float(air_quality_data.get('uvIndex', 5.0)),
                
                # Polen
                'upi_value': float(pollen_data.get('totalUpi', 0.0)),
                'grass_pollen': float(pollen_data.get('grassPollen', 0.0)),
                'tree_pollen': float(pollen_data.get('treePollen', 0.0)),
                'weed_pollen': float(pollen_data.get('weedPollen', 0.0)),
                
                # Diğer gerekli alanlar (varsayılan değerlerle)
                'cloud_cover': float(weather_data.get('cloudCover', 30.0)),
                'wind_direction_10m': float(weather_data.get('windDirection', 180.0)),
                'sunshine_duration': float(weather_data.get('sunshineDuration', 8.0)),
                'dust': float(air_quality_data.get('dust', 50.0)),
                'methane': float(air_quality_data.get('methane', 1900.0)),
                'aerosol_optical_depth': float(air_quality_data.get('aerosolOpticalDepth', 0.2)),
                'in_season': int(pollen_data.get('inSeasonCount', 0) > 0),
                'plant_in_season': int(pollen_data.get('inSeasonCount', 0)),
                'pollen_diversity_index': float(pollen_data.get('diversityIndex', 0.0))
            }
            
            logger.info(f"🌍 Expert environmental data hazırlandı: {len(expert_data)} parametre")
            return expert_data
            
        except Exception as e:
            logger.error(f"❌ Expert environmental data dönüşüm hatası: {e}")
            # Fallback varsayılan değerler
            return {
                'temperature_2m': 22.0, 'relative_humidity_2m': 55.0, 'precipitation': 0.0,
                'wind_speed_10m': 5.0, 'pm10': 20.0, 'pm2_5': 12.0, 'ozone': 100.0,
                'nitrogen_dioxide': 20.0, 'uv_index': 5.0, 'surface_pressure': 1013.0
            }
    
    def _convert_to_personal_params(self, user_classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        User classification'dan personal parameters oluştur (Gerçek request verilerini kullanarak)
        
        Args:
            user_classification: Mikroservisten gelen kullanıcı sınıflandırması
            
        Returns:
            Dict[str, Any]: Expert Predictor için personal parameters
        """
        try:
            # Extract actual values from userClassification
            age = user_classification.get('age', 30)
            clinical_diagnosis = user_classification.get('clinicalDiagnosis', 'none')  # String değer, enum value
            current_medications = user_classification.get('currentMedications', [])
            
            # Calculate personal sensitivity based on clinical data
            base_sensitivity = 0.5
            
            # Age factor: younger and older people tend to be more sensitive
            if age < 18:
                age_factor = 1.2
            elif age > 65:
                age_factor = 1.1
            else:
                age_factor = 1.0
            
            # Clinical diagnosis factor - enum değerlerine göre
            diagnosis_factor = 1.0
            if clinical_diagnosis == 'severe_allergy':
                diagnosis_factor += 0.4
            elif clinical_diagnosis == 'mild_moderate_allergy':
                diagnosis_factor += 0.2
            elif clinical_diagnosis == 'asthma':
                diagnosis_factor += 0.3
            # 'none' için ek faktör yok
            
            # Medication factor - more medications indicate higher severity
            medication_factor = 1.0 + (len(current_medications) * 0.05)
            
            # Calculate final sensitivity (scale to 1-5)
            kisisel_hassasiyet_raw = base_sensitivity * age_factor * diagnosis_factor * medication_factor
            kisisel_hassasiyet = max(1, min(5, int(kisisel_hassasiyet_raw * 5)))
            
            # Medication usage (0-5 scale based on number of medications)
            ilaç_kullanimi = min(5, len(current_medications))
            
            # Build parameters using actual request data
            params = {
                'kisisel_hassasiyet': kisisel_hassasiyet,
                'ilaç_kullanimi': ilaç_kullanimi
            }
            
            # Profil bilgilerini ekle (expert_predictor profil analizi için)
            params['profile'] = self._create_mock_profile_from_classification(user_classification)
            
            logger.info(f"👤 Personal params oluşturuldu - Yaş: {age}, Klinik: {clinical_diagnosis}, Hassasiyet: {kisisel_hassasiyet}, İlaç: {ilaç_kullanimi}")
            return params
            
        except Exception as e:
            logger.error(f"❌ Personal params dönüşüm hatası: {e}")
            # Fallback varsayılan değerler
            return {
                'kisisel_hassasiyet': 3,
                'dis_aktivite_suresi': 120,
                'egzersiz_yogunlugu': 3,
                'ilaç_kullanimi': 0,
                'stres_seviyesi': 3,
                'uyku_kalitesi': 3,
                'beslenme_kalitesi': 3,
                'profile': {}
            }
    
    def _create_mock_profile_from_classification(self, user_classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        User classification'dan gerçek profil oluştur (expert_predictor için)
        Request'ten gelen gerçek verileri kullanır
        """
        # Gerçek verileri çıkar
        age = user_classification.get('age', 30)
        gender = user_classification.get('gender', 'male')
        clinical_diagnosis = user_classification.get('clinicalDiagnosis', 'none')  # String değer, enum value
        current_medications = user_classification.get('currentMedications', [])
        family_allergy_history = user_classification.get('familyAllergyHistory', False)
        
        # Polen alerjilerini çıkar
        tree_pollen_allergies = user_classification.get('treePollenAllergies', {})
        grass_pollen_allergies = user_classification.get('grassPollenAllergies', {})
        weed_pollen_allergies = user_classification.get('weedPollenAllergies', {})
        food_allergies = user_classification.get('foodAllergies', {})
        
        # Previous reactions bilgilerini çıkar
        previous_reactions = user_classification.get('previousAllergicReactions', {})
        
        # Environmental factors
        env_sensitivity = user_classification.get('environmentalSensitivityFactors', {})
        
        # Profil oluştur - gerçek verilerle
        profile = {
            'age': age,
            'gender': gender,
            'clinical_diagnosis': clinical_diagnosis,  # Artık direkt string değer
            'family_allergy_history': family_allergy_history,
            'medications': current_medications,
            'tree_pollen': {},
            'grass_pollen': {},
            'weed_pollen': {},
            'food_allergies': {},
            'environmental_triggers': {},
            'previous_reactions': {}
        }
        
        # Polen alerjilerini profilde işaretle (True olanları)
        if tree_pollen_allergies:
            for tree_type, has_allergy in tree_pollen_allergies.items():
                if has_allergy:
                    profile['tree_pollen'][tree_type] = True
        
        if grass_pollen_allergies:
            for grass_type, has_allergy in grass_pollen_allergies.items():
                if has_allergy:
                    profile['grass_pollen'][grass_type] = True
        
        if weed_pollen_allergies:
            for weed_type, has_allergy in weed_pollen_allergies.items():
                if has_allergy:
                    profile['weed_pollen'][weed_type] = True
        
        # Gıda alerjilerini profilde işaretle
        if food_allergies:
            for food_type, has_allergy in food_allergies.items():
                if has_allergy:
                    profile['food_allergies'][food_type] = True
        
        # Previous reactions'ı profilde kaydet
        if previous_reactions:
            profile['previous_reactions'] = {
                'severe_asthma': previous_reactions.get('severe_asthma', False),
                'hospitalization': previous_reactions.get('hospitalization', False),
                'anaphylaxis': previous_reactions.get('anaphylaxis', False)
            }
        
        # Environmental triggers - gerçek verilerden
        profile['environmental_triggers'] = {
            'air_pollution': env_sensitivity.get('air_pollution_sensitive', False),
            'dust_mites': env_sensitivity.get('dust_mites_sensitive', False),
            'pet_dander': env_sensitivity.get('pet_dander_sensitive', False),
            'smoke': env_sensitivity.get('smoke_sensitive', False),
            'mold': env_sensitivity.get('mold_sensitive', False)
        }
        
        logger.info(f"👤 Profil oluşturuldu - Yaş: {age}, Cinsiyet: {gender}, Klinik: {clinical_diagnosis}, İlaç: {len(current_medications)}")
        return profile
    
    def _extract_contributing_factors(self, environmental_data: Dict[str, Any], user_classification: Dict[str, Any]) -> Dict[str, Any]:
        """Risk katkı faktörlerini çıkar"""
        factors = {}
        
        # Çevresel faktörler
        if environmental_data.get('pm10', 0) > 50:
            factors['high_pm10'] = environmental_data.get('pm10')
        if environmental_data.get('pm2_5', 0) > 25:
            factors['high_pm25'] = environmental_data.get('pm2_5')
        if environmental_data.get('ozone', 0) > 120:
            factors['high_ozone'] = environmental_data.get('ozone')
        if environmental_data.get('upi_value', 0) > 100:
            factors['high_pollen'] = environmental_data.get('upi_value')
        
        # Kullanıcı faktörleri
        group_id = user_classification.get('groupId')
        if group_id in [1, 5]:
            factors['high_risk_group'] = group_id
        
        return factors
    
    def _extract_environmental_risks(self, environmental_data: Dict[str, Any]) -> Dict[str, Any]:
        """Çevresel riskleri çıkar"""
        risks = {
            'air_quality_risk': 'low',
            'pollen_risk': 'low',
            'weather_risk': 'low'
        }
        
        # Hava kalitesi riski
        pm10 = environmental_data.get('pm10', 0)
        pm25 = environmental_data.get('pm2_5', 0)
        ozone = environmental_data.get('ozone', 0)
        
        if pm10 > 100 or pm25 > 50 or ozone > 180:
            risks['air_quality_risk'] = 'high'
        elif pm10 > 50 or pm25 > 25 or ozone > 120:
            risks['air_quality_risk'] = 'medium'
        
        # Polen riski
        upi = environmental_data.get('upi_value', 0)
        if upi > 200:
            risks['pollen_risk'] = 'high'
        elif upi > 100:
            risks['pollen_risk'] = 'medium'
        
        # Hava durumu riski
        temp = environmental_data.get('temperature_2m', 20)
        wind = environmental_data.get('wind_speed_10m', 5)
        
        if temp > 35 or temp < 0 or wind > 25:
            risks['weather_risk'] = 'high'
        elif temp > 30 or temp < 5 or wind > 15:
            risks['weather_risk'] = 'medium'
        
        return risks
    
    def _generate_recommendations(self, group_result: Dict[str, Any], user_classification: Dict[str, Any]) -> List[str]:
        """Önerileri oluştur"""
        recommendations = []
        
        risk_level = group_result.get('risk_level', 'Orta')
        safe_hours = group_result.get('personal_safe_hours', 4.0)
        
        if risk_level == 'Yüksek':
            recommendations.append("İç mekanda kalmanız önerilir")
            recommendations.append("Dışarı çıkmanız gerekiyorsa maske takın")
            recommendations.append("Pencerelerinizi kapalı tutun")
        elif risk_level == 'Orta':
            recommendations.append(f"Dışarıda en fazla {safe_hours:.1f} saat kalabilirsiniz")
            recommendations.append("Aktivitelerinizi sınırlayın")
        else:
            recommendations.append("Güvenli bir gün, rahatça dışarıda vakit geçirebilirsiniz")
        
        # Grup bazlı öneriler
        group_id = user_classification.get('groupId')
        if group_id == 1:
            recommendations.append("İlaçlarınızı yanınızda bulundurun")
        elif group_id == 5:
            recommendations.append("Ekstra dikkatli olun, hassas grubundasınız")
        
        return recommendations
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information and health status"""
        try:
            model_info = self.predictor.get_model_info()
            
            return {
                'service': 'AllerMind Risk Prediction API',
                'version': '2.0',
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'models': {
                    'loadedModels': model_info.get('loaded_models', []),
                    'totalModels': len(model_info.get('loaded_models', [])),
                    'modelPath': model_info.get('models_path', 'Unknown')
                },
                'availableGroups': list(self.model_groups.keys()),
                'components': {
                    'expertPredictor': True,
                    'modelGroups': len(self.model_groups)
                }
            }
        except Exception as e:
            logger.error(f"❌ Sistem bilgisi alınırken hata: {e}")
            return {
                'service': 'AllerMind Risk Prediction API',
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Global predictor instance
risk_predictor = None

def initialize_predictor():
    """Initialize the risk predictor"""
    global risk_predictor
    try:
        risk_predictor = AllerMindRiskPredictor()
        return True
    except Exception as e:
        logger.error(f"❌ Predictor başlatma hatası: {e}")
        return False

# API Endpoints

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        if risk_predictor is None:
            return jsonify({
                "status": "unhealthy",
                "error": "Predictor not initialized",
                "service": "AllerMind Risk Prediction API",
                "timestamp": datetime.now().isoformat()
            }), 503
        
        system_info = risk_predictor.get_system_info()
        return jsonify(system_info), 200
        
    except Exception as e:
        logger.error(f"❌ Health check hatası: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "service": "AllerMind Risk Prediction API",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/v1/allergy-groups', methods=['GET'])
def get_allergy_groups():
    """Get available expert model groups"""
    try:
        global risk_predictor
        if not risk_predictor:
            return jsonify({
                'success': False,
                'error': 'Risk predictor başlatılmamış',
                'timestamp': datetime.now().isoformat()
            }), 500
        
        groups = []
        for group_id, group_name in risk_predictor.model_groups.items():
            groups.append({
                'groupId': group_id,
                'groupName': group_name,
                'description': f'Expert Model {group_id} - {group_name}',
                'modelAvailable': group_id in risk_predictor.predictor.models,
                'algorithm': risk_predictor.predictor.models[group_id]['algorithm_used'] if group_id in risk_predictor.predictor.models else 'Unknown'
            })
        
        return jsonify({
            'success': True,
            'groups': groups,
            'totalGroups': len(groups),
            'expertSystem': True,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Grupları getirirken hata: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500



@app.route('/api/v1/predict', methods=['POST'])
def predict_allergy_risk():
    """
    Main prediction endpoint - predict allergy risk based on user classification from microservice and environmental data
    
    Expected JSON format:
    {
        "userClassification": {
            "age": 28,
            "assignmentReason": "Klinik tanı temelinde",
            "clinicalDiagnosis": "mild_moderate_allergy",
            "currentMedications": [
                "antihistamine",
                "nasal_spray"
            ],
            "environmentalSensitivityFactors": {
                "pet_dander_sensitivity": false,
                "mold_sensitivity": true,
                "air_pollution_sensitivity": true,
                "dust_mite_sensitivity": true,
                "smoke_sensitivity": true
            },
            "environmentalTriggers": {
                "air_pollution": true,
                "dust_mites": true,
                "smoke": true,
                "pet_dander": false,
                "mold": true
            },
            "familyAllergyHistory": true,
            "foodAllergies": {
                "apple": true,
                "shellfish": false,
                "nuts": false
            },
            "gender": "female",
            "grassPollenAllergies": {
                "graminales": true
            },
            "groupDescription": "IgE 200-1000 IU/mL, Kontrol edilebilir belirtiler",
            "groupId": 2,
            "groupName": "Hafif-Orta Alerjik Grup",
            "immunologicProfile": {
                "inflammatory_response": "local",
                "ige_level": "moderate_high",
                "antihistamine_response": "good",
                "seasonal_pattern": "rhinitis"
            },
            "latitude": 41.01,
            "longitude": 28.98,
            "modelWeight": 0.22,
            "personalRiskModifiers": {
                "seasonal_modifier": 1.2,
                "environmental_amplifier": 1.4,
                "comorbidity_factor": 1.0,
                "base_sensitivity": 1.0
            },
            "pollenSpecificRisks": {
                "high_risk_pollens": [
                    "ragweed"
                ],
                "cross_reactive_foods": [
                    "apple",
                    "cherry",
                    "pear",
                    "almond",
                    "melon",
                    "banana",
                    "cucumber"
                ],
                "moderate_risk_pollens": [
                    "birch",
                    "graminales"
                ]
            },
            "previousAllergicReactions": {
                "severe_asthma": false,
                "hospitalization": false,
                "anaphylaxis": false
            },
            "recommendationAdjustments": {
                "environmental_control_level": "moderate",
                "medication_priority": "moderate",
                "monitoring_frequency": "weekly",
                "emergency_preparedness": false
            },
            "treePollenAllergies": {
                "pine": false,
                "olive": false,
                "birch": true
            },
            "userPreferenceId": "8eb0d4c6-02c2-4d02-87ca-3fbecfee922f",
            "weedPollenAllergies": {
                "mugwort": false,
                "ragweed": true
            }
        },
        "environmentalData": {
            "airQuality": {
                "pm25": 15.5,
                "pm10": 28.3,
                "o3": 125.7,
                "no2": 45.2,
                "so2": 8.1,
                "co": 0.8,
                "dust": 12,
                "methane": 1875.5,
                "uvIndex": 6.8,
                "aerosolOpticalDepth": 0.35,
                "co2": 415
            },
            "pollen": {
                "totalUpi": 85.6,
                "treePollen": 32.4,
                "grassPollen": 28.7,
                "weedPollen": 24.5,
                "inSeasonCount": 7,
                "diversityIndex": 0.65
            },
            "weather": {
                "temperature": 22.5,
                "humidity": 68.0,
                "windSpeed": 12.3,
                "pressure": 1013.25,
                "precipitation": 0.0,
                "windDirection": 270,
                "sunshineDuration": 8.5,
                "cloudCover": 45
            }
        }
    }
    """
    try:
        if risk_predictor is None:
            return jsonify({
                'success': False,
                'error': 'Sistem henüz hazır değil',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({
                'success': False,
                'error': 'Request body boş olamaz',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Validate required fields for REST API - userClassification from microservice
        required_fields = ['userClassification', 'environmentalData']
        missing_fields = [field for field in required_fields if field not in request_data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Eksik alanlar: {", ".join(missing_fields)}',
                'requiredFields': required_fields,
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Validate user classification structure
        user_classification = request_data.get('userClassification', {})
        required_classification_fields = ['groupId', 'groupName']
        missing_classification_fields = [field for field in required_classification_fields if field not in user_classification]
        
        if missing_classification_fields:
            return jsonify({
                'success': False,
                'error': f'userClassification içinde eksik alanlar: {", ".join(missing_classification_fields)}',
                'requiredFields': required_classification_fields,
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Validate group ID
        group_id = user_classification.get('groupId')
        if not isinstance(group_id, int) or group_id < 1 or group_id > 5:
            return jsonify({
                'success': False,
                'error': 'userClassification.groupId 1-5 arasında bir sayı olmalı',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Validate environmental data structure
        env_data = request_data.get('environmentalData', {})
        required_env_sections = ['airQuality', 'pollen', 'weather']
        missing_env_sections = [section for section in required_env_sections if section not in env_data]
        
        if missing_env_sections:
            return jsonify({
                'success': False,
                'error': f'environmentalData içinde eksik bölümler: {", ".join(missing_env_sections)}',
                'requiredSections': required_env_sections,
                'providedSections': list(env_data.keys()),
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Perform prediction
        prediction_response = risk_predictor.predict_allergy_risk(request_data)
        
        return jsonify(prediction_response), 200
        
    except ValueError as ve:
        logger.error(f"❌ Validation hatası: {ve}")
        return jsonify({
            'success': False,
            'error': str(ve),
            'timestamp': datetime.now().isoformat()
        }), 400
        
    except Exception as e:
        logger.error(f"❌ Tahmin hatası: {e}")
        return jsonify({
            'success': False,
            'error': f'İç hata: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/v1/system-info', methods=['GET'])
def get_system_info():
    """Get detailed system information"""
    try:
        if risk_predictor is None:
            return jsonify({
                'success': False,
                'error': 'System not initialized'
            }), 503
        
        system_info = risk_predictor.get_system_info()
        return jsonify(system_info), 200
        
    except Exception as e:
        logger.error(f"❌ System info error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Legacy endpoints for backward compatibility
@app.route('/predict', methods=['POST'])
def legacy_predict():
    """Legacy prediction endpoint for backward compatibility"""
    return predict_allergy_risk()

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint"""
    return jsonify({
        "message": "AllerMind API is running!",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0"
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500

if __name__ == "__main__":
    print("🌟" + "="*60 + "🌟")
    print("     🧬 ALLERMIND RISK PREDICTION REST API 🏥")
    print("🌟" + "="*60 + "🌟")
    
    try:
        # Initialize the prediction service
        print("📥 Prediction service başlatılıyor...")
        if initialize_predictor():
            print("✅ Sistem başarıyla başlatıldı")
            print("🌐 API Endpoints:")
            print("   GET  /health                     - Health check")
            print("   GET  /api/v1/allergy-groups      - Available allergy groups")
            print("   POST /api/v1/classify-user       - Classify user into group")
            print("   POST /api/v1/predict             - Main prediction endpoint")
            print("   GET  /api/v1/system-info         - System information")
            print("   POST /predict                    - Legacy prediction endpoint")
            print("   GET  /test                       - Simple test endpoint")
            print("-" * 70)
            print("🚀 Server http://localhost:8585 adresinde çalışıyor...")
            print("📖 API documentation: README.md dosyasına bakınız")
            
            app.run(host='0.0.0.0', port=8585, debug=False, threaded=True)
        else:
            print("❌ Sistem başlatılamadı")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Server kapatılıyor...")
    except Exception as e:
        logger.error(f"❌ Genel hata: {e}")
        traceback.print_exc()
        sys.exit(1)
