#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALLERMIND V2.0 - EXPERT WEB API SERVICE
Flask-based RESTful API with personal weighting system
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from expert_predictor import ExpertAllermindPredictor
import traceback
from datetime import datetime
import logging

# Flask app setup
app = Flask(__name__)
CORS(app)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global predictor instance
predictor = None

def initialize_predictor():
    """Expert predictor'ı başlat"""
    global predictor
    try:
        predictor = ExpertAllermindPredictor()
        logger.info("✅ Expert AllermindPredictor başarıyla yüklendi")
        return True
    except Exception as e:
        logger.error(f"❌ Expert Predictor yüklenemedi: {str(e)}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """API sağlık kontrolü"""
    
    return jsonify({
        'status': 'healthy',
        'service': 'AllermindV2 Expert API',
        'version': '2.0',
        'system': 'Expert-level machine learning system',
        'timestamp': datetime.now().isoformat(),
        'predictor_loaded': predictor is not None,
        'models_loaded': len(predictor.models) if predictor else 0
    })

@app.route('/predict/group/<int:group_id>', methods=['POST'])
def predict_single_group(group_id):
    """Tek grup için expert tahmin"""
    
    try:
        if not predictor:
            return jsonify({
                'error': 'Expert Predictor not initialized',
                'message': 'Service not ready'
            }), 503
        
        if group_id not in [1, 2, 3, 4, 5]:
            return jsonify({
                'error': 'Invalid group_id',
                'message': 'group_id must be between 1-5',
                'available_groups': list(range(1, 6))
            }), 400
        
        # Input data
        data = request.json
        if not data:
            return jsonify({
                'error': 'No input data provided',
                'message': 'Request body must contain environmental_data and optional personal_params'
            }), 400
        
        environmental_data = data.get('environmental_data', {})
        personal_params = data.get('personal_params', None)
        
        if not environmental_data:
            return jsonify({
                'error': 'Missing environmental_data',
                'required_fields': ['temperature_2m', 'relative_humidity_2m', 'pm10', 'pm2_5', 'uv_index']
            }), 400
        
        # Prediction
        result = predictor.predict_group(environmental_data, group_id, personal_params)
        
        if not result:
            return jsonify({
                'error': 'Prediction failed',
                'message': f'Could not generate prediction for group {group_id}'
            }), 500
        
        return jsonify({
            'success': True,
            'data': result,
            'api_info': {
                'version': '2.0',
                'system': 'Expert-level prediction',
                'request_timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Single group prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc() if app.debug else None
        }), 500

@app.route('/predict/ensemble', methods=['POST'])
def predict_ensemble():
    """Expert ensemble tahmin - ana endpoint"""
    
    try:
        if not predictor:
            return jsonify({
                'error': 'Expert Predictor not initialized',
                'message': 'Service not ready'
            }), 503
        
        # Input data
        data = request.json
        if not data:
            return jsonify({
                'error': 'No input data provided',
                'message': 'Request body must contain environmental_data and optional personal_params',
                'example': {
                    'environmental_data': {
                        'temperature_2m': 25.0,
                        'relative_humidity_2m': 60.0,
                        'pm10': 30.0,
                        'pm2_5': 18.0,
                        'uv_index': 7.0
                    },
                    'personal_params': {
                        'age_group': 'adult',
                        'medical_condition': 'healthy',
                        'activity_level': 'moderate',
                        'sensitivity_level': 'moderate'
                    }
                }
            }), 400
        
        environmental_data = data.get('environmental_data', {})
        personal_params = data.get('personal_params', None)
        
        if not environmental_data:
            return jsonify({
                'error': 'Missing environmental_data',
                'required_fields': ['temperature_2m', 'relative_humidity_2m', 'pm10', 'pm2_5', 'uv_index']
            }), 400
        
        # Ensemble prediction
        result = predictor.predict_ensemble(environmental_data, personal_params)
        
        if not result:
            return jsonify({
                'error': 'Ensemble prediction failed',
                'message': 'Could not generate reliable ensemble prediction'
            }), 500
        
        # Response
        response = {
            'success': True,
            'ensemble_prediction': result['ensemble_prediction'],
            'individual_predictions': result['individual_predictions'],
            'personal_parameters': result['personal_parameters'],
            'input_validation': result['input_validation'],
            'ensemble_info': result['ensemble_info'],
            'api_info': {
                'version': '2.0',
                'system': 'Expert Ensemble Prediction',
                'features': 'Personal weighting, Performance-based ensemble, Expert algorithms',
                'request_timestamp': datetime.now().isoformat()
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Ensemble prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc() if app.debug else None
        }), 500

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """Batch tahmin - çoklu lokasyon ve kişi"""
    
    try:
        if not predictor:
            return jsonify({
                'error': 'Expert Predictor not initialized'
            }), 503
        
        data = request.json
        batch_requests = data.get('requests', [])
        
        if not batch_requests:
            return jsonify({
                'error': 'No batch requests provided',
                'message': 'Request must contain "requests" array',
                'example': {
                    'requests': [
                        {
                            'name': 'Location 1',
                            'environmental_data': {...},
                            'personal_params': {...}
                        }
                    ]
                }
            }), 400
        
        if len(batch_requests) > 10:  # Rate limiting
            return jsonify({
                'error': 'Too many requests',
                'message': f'Maximum 10 requests per batch, received {len(batch_requests)}'
            }), 400
        
        # Her request için ensemble tahmin
        batch_results = []
        
        for idx, req in enumerate(batch_requests):
            try:
                req_name = req.get('name', f'Request_{idx+1}')
                env_data = req.get('environmental_data', {})
                personal_data = req.get('personal_params', None)
                
                result = predictor.predict_ensemble(env_data, personal_data)
                
                if result:
                    batch_results.append({
                        'request_name': req_name,
                        'request_index': idx,
                        'success': True,
                        'prediction': result['ensemble_prediction'],
                        'confidence': result['ensemble_info']['reliable_models'] / 5.0
                    })
                else:
                    batch_results.append({
                        'request_name': req_name,
                        'request_index': idx,
                        'success': False,
                        'error': 'Prediction failed'
                    })
                
            except Exception as req_error:
                batch_results.append({
                    'request_name': req.get('name', f'Request_{idx+1}'),
                    'request_index': idx,
                    'success': False,
                    'error': str(req_error)
                })
        
        # Summary
        successful = sum(1 for r in batch_results if r['success'])
        avg_confidence = sum(r.get('confidence', 0) for r in batch_results if r['success']) / max(successful, 1)
        
        return jsonify({
            'success': True,
            'batch_summary': {
                'total_requests': len(batch_requests),
                'successful_predictions': successful,
                'failed_predictions': len(batch_requests) - successful,
                'success_rate': successful / len(batch_requests),
                'average_confidence': avg_confidence
            },
            'results': batch_results,
            'api_info': {
                'version': '2.0',
                'system': 'Expert Batch Prediction',
                'request_timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/models/info', methods=['GET'])
def models_info():
    """Expert model bilgileri"""
    
    try:
        if not predictor:
            return jsonify({
                'error': 'Expert Predictor not initialized'
            }), 503
        
        model_info = predictor.get_model_info()
        
        return jsonify({
            'success': True,
            'system_info': {
                'version': '2.0',
                'system_type': 'Expert Machine Learning System',
                'total_models': len(model_info),
                'data_size': '598,296 records',
                'training_period': '2025-08-30 to 2025-09-11',
                'features': 'Personal weighting, Performance-based ensemble, Advanced algorithms'
            },
            'models': model_info,
            'allergy_groups': {
                1: 'Polen Hassasiyeti Grubu',
                2: 'Hava Kirliliği Hassasiyeti Grubu',
                3: 'UV ve Güneş Hassasiyeti Grubu',
                4: 'Meteorolojik Hassasiyet Grubu',
                5: 'Hassas Grup (Çocuk/Yaşlı)'
            },
            'personal_parameters': {
                'age_group': ['child', 'adult', 'elderly'],
                'medical_condition': ['healthy', 'allergy', 'asthma'],
                'activity_level': ['low', 'moderate', 'high'],
                'sensitivity_level': ['low', 'moderate', 'high', 'very_high']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/predict/demo', methods=['GET'])
def demo_prediction():
    """Demo tahmin - test amaçlı"""
    
    try:
        if not predictor:
            return jsonify({
                'error': 'Expert Predictor not initialized'
            }), 503
        
        # Demo scenarios
        scenarios = {
            'ideal_conditions': {
                'environmental_data': {
                    'temperature_2m': 25.0, 'relative_humidity_2m': 60.0,
                    'precipitation': 0.0, 'wind_speed_10m': 8.0,
                    'pm10': 20.0, 'pm2_5': 12.0, 'ozone': 90.0,
                    'nitrogen_dioxide': 18.0, 'uv_index': 6.0, 'surface_pressure': 1015.0
                },
                'personal_params': {
                    'age_group': 'adult',
                    'medical_condition': 'healthy',
                    'activity_level': 'moderate',
                    'sensitivity_level': 'moderate'
                }
            },
            'high_pollution': {
                'environmental_data': {
                    'temperature_2m': 32.0, 'relative_humidity_2m': 45.0,
                    'precipitation': 0.0, 'wind_speed_10m': 3.0,
                    'pm10': 85.0, 'pm2_5': 55.0, 'ozone': 180.0,
                    'nitrogen_dioxide': 45.0, 'uv_index': 9.0, 'surface_pressure': 1008.0
                },
                'personal_params': {
                    'age_group': 'elderly',
                    'medical_condition': 'asthma',
                    'activity_level': 'low',
                    'sensitivity_level': 'very_high'
                }
            }
        }
        
        demo_results = {}
        
        for scenario_name, scenario_data in scenarios.items():
            result = predictor.predict_ensemble(
                scenario_data['environmental_data'],
                scenario_data['personal_params']
            )
            
            if result:
                demo_results[scenario_name] = {
                    'input': scenario_data,
                    'prediction': result['ensemble_prediction'],
                    'summary': f"{result['ensemble_prediction']['safe_outdoor_hours']:.1f} hours, {result['ensemble_prediction']['risk_level']} risk"
                }
        
        return jsonify({
            'success': True,
            'demo_results': demo_results,
            'message': 'Expert system demo predictions with different scenarios',
            'api_version': '2.0'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'GET /health - System health check',
            'POST /predict/ensemble - Main prediction endpoint',
            'POST /predict/group/<id> - Single group prediction',
            'POST /predict/batch - Batch predictions',
            'GET /predict/demo - Demo predictions',
            'GET /models/info - Model information'
        ],
        'api_version': '2.0'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Expert system encountered an error',
        'api_version': '2.0'
    }), 500

if __name__ == '__main__':
    print("🚀 ALLERMIND V2.0 EXPERT WEB API SERVICE")
    print("=" * 60)
    print("🧠 Expert-level machine learning system")
    print("⚙️ Personal weighting & Performance-based ensemble")
    
    # Expert predictor initialize
    if initialize_predictor():
        print("✅ Expert Predictor başarıyla yüklendi")
        print("📊 Model performansları:")
        
        model_info = predictor.get_model_info()
        for gid, info in model_info.items():
            print(f"   Grup {gid}: {info['algorithm']} (R²: {info['performance']['test_r2']:.4f})")
        
        print(f"\n📖 API KULLANIM ÖRNEKLERİ:")
        print(f"\n1. Expert Ensemble Prediction:")
        print(f"   curl -X POST http://localhost:5000/predict/ensemble \\")
        print(f"        -H 'Content-Type: application/json' \\")
        print(f"        -d '{{")
        print(f"          \"environmental_data\": {{")
        print(f"            \"temperature_2m\": 25.0,")
        print(f"            \"relative_humidity_2m\": 60.0,")
        print(f"            \"pm10\": 30.0,")
        print(f"            \"pm2_5\": 18.0,")
        print(f"            \"uv_index\": 7.0")
        print(f"          }},")
        print(f"          \"personal_params\": {{")
        print(f"            \"age_group\": \"adult\",")
        print(f"            \"medical_condition\": \"healthy\",")
        print(f"            \"activity_level\": \"moderate\",")
        print(f"            \"sensitivity_level\": \"moderate\"")
        print(f"          }}")
        print(f"        }}'")
        
        print(f"\n2. System Health:")
        print(f"   curl http://localhost:5000/health")
        
        print(f"\n3. Demo Predictions:")
        print(f"   curl http://localhost:5000/predict/demo")
        
        print(f"\n🌐 Expert Server başlatılıyor - http://localhost:5000")
        print(f"   🔬 Expert algorithms: RandomForest, GradientBoosting, SVR, ExtraTrees, NeuralNetwork")
        print(f"   🎯 Personal weighting system: Aktif")
        print(f"   📊 Performance-based ensemble: Aktif")
        print(f"   🛡️ CORS: Etkin")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Expert Predictor yüklenemedi - Server başlatılamıyor")
        sys.exit(1)