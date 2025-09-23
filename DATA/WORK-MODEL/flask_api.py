"""
AllerMind Flask API Server
Flask tabanlı REST API servisi
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging
import traceback
from dataclasses import asdict

from user_preference_system import AllergyGroupClassifier, ALLERGY_GROUPS
from allermind_predictor import AllerMindPredictor
from data_loader import DataLoader

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Frontend'den gelen isteklere izin ver

# Global nesneler
predictor = None
data_loader = None

def initialize_services():
    """Servisleri başlat"""
    global predictor, data_loader
    try:
        logger.info("🚀 Servisleri başlatılıyor...")
        
        # Data loader'ı başlat
        data_loader = DataLoader()
        logger.info("✅ DataLoader başlatıldı")
        
        # Predictor'ı başlat
        predictor = AllerMindPredictor()
        logger.info("✅ AllerMindPredictor başlatıldı")
        
        return True
    except Exception as e:
        logger.error(f"❌ Servis başlatma hatası: {str(e)}")
        return False

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Sistem sağlığını kontrol et"""
    try:
        status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'predictor': predictor is not None,
                'data_loader': data_loader is not None
            }
        }
        return jsonify(status), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/v1/allergy-groups', methods=['GET'])
def get_allergy_groups():
    """Mevcut alerji gruplarını döndür"""
    try:
        groups = []
        for group_id, group_info in ALLERGY_GROUPS.items():
            groups.append({
                'groupId': group_id,
                'groupName': group_info['name'],
                'description': group_info['description']
            })
        
        return jsonify({
            'success': True,
            'groups': groups
        }), 200
    except Exception as e:
        logger.error(f"❌ Grupları getirirken hata: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/v1/classify-user', methods=['POST'])
def classify_user():
    """Kullanıcı özelliklerine göre grup belirle"""
    try:
        user_data = request.get_json()
        
        if not user_data:
            return jsonify({
                'success': False,
                'error': 'Kullanıcı verisi eksik'
            }), 400
        
        # Alerji grup sınıflandırıcısını başlat
        classifier = AllergyGroupClassifier()
        
        # Grubu belirle
        group_id = classifier.classify_user(user_data)
        group_info = ALLERGY_GROUPS[group_id]
        
        return jsonify({
            'success': True,
            'groupId': group_id,
            'groupName': group_info['name'],
            'description': group_info['description'],
            'userCharacteristics': user_data
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Kullanıcı sınıflandırma hatası: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/v1/prediction', methods=['POST'])
def get_prediction():
    """Ana tahmin endpoint'i - kullanıcı bilgilerini alıp risk tahmini üret"""
    try:
        if not predictor or not data_loader:
            return jsonify({
                'success': False,
                'error': 'Sistem servisleri hazır değil'
            }), 503
        
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({
                'success': False,
                'error': 'İstek verisi eksik'
            }), 400
        
        # Gerekli alanları kontrol et
        required_fields = ['lat', 'lon', 'userGroup']
        missing_fields = [field for field in required_fields if field not in request_data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Eksik alanlar: {missing_fields}'
            }), 400
        
        # Konum bilgileri
        lat = float(request_data['lat'])
        lon = float(request_data['lon'])
        
        # Kullanıcı grubu
        user_group_data = request_data['userGroup']
        group_id = user_group_data.get('groupId', 1)
        
        # Günün tarihini al
        today = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"🔍 Tahmin isteği - Lat: {lat}, Lon: {lon}, Grup: {group_id}")
        
        # Kullanıcı verisini hazırla
        user_characteristics = request_data.get('userCharacteristics', {})
        user_modifiers = {
            'age': user_characteristics.get('age', 30),
            'gender': user_characteristics.get('gender', 'male'),
            'has_chronic_disease': user_characteristics.get('hasChronicDisease', False),
            'allergy_history': user_characteristics.get('allergyHistory', []),
            'medication_usage': user_characteristics.get('medicationUsage', [])
        }
        
        # Tahmin yap
        prediction_result = predictor.predict(
            group_id=group_id,
            location=(lat, lon),
            user_modifiers=user_modifiers,
            date=today
        )
        
        # Sonucu formatla
        if prediction_result and hasattr(prediction_result, 'predictions') and prediction_result.predictions:
            # En yüksek riski bul
            max_risk = max(pred.risk_score for pred in prediction_result.predictions)
            risk_level = predictor._determine_risk_level(max_risk)
            
            # Model tahmin sonuçlarını formatla
            formatted_predictions = []
            for pred in prediction_result.predictions:
                formatted_predictions.append({
                    'allergenType': pred.allergen_type,
                    'predictionValue': pred.risk_score,
                    'riskLevel': predictor._determine_risk_level(pred.risk_score),
                    'confidence': pred.confidence,
                    'factors': pred.contributing_factors
                })
            
            response = {
                'success': True,
                'predictionId': f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'userId': request_data.get('userId', 'anonymous'),
                'lat': str(lat),
                'lon': str(lon),
                'timestamp': datetime.now().isoformat(),
                'overallRiskScore': max_risk,
                'overallRiskLevel': risk_level,
                'overallRiskEmoji': predictor._get_risk_emoji(risk_level),
                'overallRiskCode': predictor._get_risk_code(risk_level),
                'userGroup': {
                    'groupId': group_id,
                    'groupName': ALLERGY_GROUPS[group_id]['name'],
                    'description': ALLERGY_GROUPS[group_id]['description']
                },
                'modelPrediction': {
                    'success': True,
                    'message': 'Tahmin başarılı',
                    'predictions': formatted_predictions,
                    'environmentalData': {
                        'date': today,
                        'location': f"{lat},{lon}",
                        'dataSource': '16SEP dataset'
                    }
                },
                'recommendations': predictor._get_recommendations(risk_level, group_id),
                'crossReactivity': predictor._get_cross_reactivity_info(group_id)
            }
            
            logger.info(f"✅ Tahmin başarılı - Risk: {max_risk:.3f} ({risk_level})")
            return jsonify(response), 200
        
        else:
            # Fallback yanıt
            fallback_risk = 0.5
            fallback_level = "ORTA"
            
            response = {
                'success': True,
                'predictionId': f"fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'userId': request_data.get('userId', 'anonymous'),
                'lat': str(lat),
                'lon': str(lon),
                'timestamp': datetime.now().isoformat(),
                'overallRiskScore': fallback_risk,
                'overallRiskLevel': fallback_level,
                'overallRiskEmoji': '⚠️',
                'overallRiskCode': 2,
                'userGroup': {
                    'groupId': group_id,
                    'groupName': ALLERGY_GROUPS[group_id]['name'],
                    'description': ALLERGY_GROUPS[group_id]['description']
                },
                'modelPrediction': {
                    'success': False,
                    'message': 'Fallback tahmin kullanıldı',
                    'predictions': [
                        {
                            'allergenType': 'Genel',
                            'predictionValue': fallback_risk,
                            'riskLevel': fallback_level,
                            'confidence': 0.7,
                            'factors': ['Veri yetersizliği']
                        }
                    ]
                },
                'recommendations': ["Genel önlemler alın", "Hava durumunu takip edin"],
                'crossReactivity': []
            }
            
            logger.warning("⚠️ Fallback tahmin kullanıldı")
            return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"❌ Tahmin hatası: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/v1/daily-data', methods=['GET'])
def get_daily_data():
    """Günlük çevresel verileri getir"""
    try:
        if not data_loader:
            return jsonify({
                'success': False,
                'error': 'Data loader hazır değil'
            }), 503
        
        # Parametreleri al
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        if lat is None or lon is None:
            return jsonify({
                'success': False,
                'error': 'Konum bilgileri (lat, lon) gerekli'
            }), 400
        
        # Veriyi yükle
        daily_data = data_loader.get_location_data(lat, lon)
        
        if daily_data is not None and not daily_data.empty:
            # Veriyi JSON formatında döndür
            data_sample = daily_data.head(1).to_dict(orient='records')[0] if not daily_data.empty else {}
            
            response = {
                'success': True,
                'date': date,
                'location': {'lat': lat, 'lon': lon},
                'dataCount': len(daily_data),
                'environmentalData': {
                    'airQuality': {
                        'aqi': data_sample.get('aqi', 'N/A'),
                        'pm25': data_sample.get('pm25', 'N/A'),
                        'pm10': data_sample.get('pm10', 'N/A'),
                        'no2': data_sample.get('no2', 'N/A'),
                        'o3': data_sample.get('o3', 'N/A')
                    },
                    'weather': {
                        'temperature': data_sample.get('temperature', 'N/A'),
                        'humidity': data_sample.get('humidity', 'N/A'),
                        'wind_speed': data_sample.get('wind_speed', 'N/A'),
                        'pressure': data_sample.get('pressure', 'N/A')
                    },
                    'pollen': {
                        'tree_pollen': data_sample.get('tree_pollen', 'N/A'),
                        'grass_pollen': data_sample.get('grass_pollen', 'N/A'),
                        'weed_pollen': data_sample.get('weed_pollen', 'N/A'),
                        'total_pollen': data_sample.get('total_pollen', 'N/A')
                    }
                }
            }
            
            return jsonify(response), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Belirtilen konum için veri bulunamadı'
            }), 404
            
    except Exception as e:
        logger.error(f"❌ Günlük veri hatası: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    logger.info("🌟 AllerMind Flask API başlatılıyor...")
    
    # Servisleri başlat
    if initialize_services():
        logger.info("✅ Tüm servisler başarıyla başlatıldı")
        logger.info("🚀 API Server http://localhost:5000 adresinde çalışıyor")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        logger.error("❌ Servisler başlatılamadı, server kapatılıyor")
        exit(1)