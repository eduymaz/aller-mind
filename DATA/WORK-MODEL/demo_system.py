"""
AllerMind Demo ve Test Sistemi
Farklı kullanıcı senaryolarını test eden kapsamlı demo
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Kendi modüllerimizi import et
from user_preference_system import UserPreferences, AllergyGroupClassifier, create_sample_user_preferences
from allermind_predictor import AllerMindPredictor, create_test_user
from data_loader import DataLoader

warnings.filterwarnings('ignore')


class AllerMindDemo:
    """
    AllerMind sistem demo sınıfı
    Farklı senaryoları test eder ve sonuçları görselleştirir
    """
    
    def __init__(self):
        try:
            self.predictor = AllerMindPredictor()
            self.group_classifier = AllergyGroupClassifier()
            self.data_loader = DataLoader()
            self.demo_users = self._create_demo_users()
            
            print("✅ AllerMind Demo sistemi başarıyla başlatıldı")
        except Exception as e:
            print(f"❌ Demo sistemi başlatılamadı: {e}")
            print("⚠️  Fallback modu aktif - sınırlı özellikler")
    
    def _create_demo_users(self) -> Dict[str, UserPreferences]:
        """Demo için farklı kullanıcı profilleri oluştur"""
        
        users = {}
        
        # 1. Şiddetli Alerjik Hasta (Grup 1)
        users['severe_patient'] = UserPreferences(
            age=28,
            gender='female',
            location={'latitude': 41.0082, 'longitude': 28.9784},
            clinical_diagnosis='severe_allergy',
            family_allergy_history=True,
            previous_allergic_reactions={
                'anaphylaxis': True,
                'severe_asthma': True,
                'hospitalization': True
            },
            current_medications=['antihistamine', 'bronchodilator', 'epinephrine', 'immunotherapy'],
            tree_pollen_allergy={
                'birch': True,
                'olive': True,
                'pine': True
            },
            grass_pollen_allergy={
                'graminales': True
            },
            weed_pollen_allergy={
                'ragweed': True,
                'mugwort': True
            },
            food_allergies={
                'apple': True,
                'nuts': True,
                'shellfish': True
            },
            environmental_triggers={
                'dust_mites': True,
                'pet_dander': True,
                'mold': True,
                'air_pollution': True,
                'smoke': True
            }
        )
        
        # 2. Hafif-Orta Alerjik Hasta (Grup 2)
        users['moderate_patient'] = UserPreferences(
            age=35,
            gender='male',
            location={'latitude': 39.9334, 'longitude': 32.8597},  # Ankara
            clinical_diagnosis='mild_moderate_allergy',
            family_allergy_history=True,
            previous_allergic_reactions={
                'anaphylaxis': False,
                'severe_asthma': False,
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
                'ragweed': False,
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
                'mold': False,
                'air_pollution': True,
                'smoke': False
            }
        )
        
        # 3. Genetik Yatkınlığı Olan (Grup 3)
        users['genetic_risk'] = UserPreferences(
            age=22,
            gender='female',
            location={'latitude': 38.4192, 'longitude': 27.1287},  # İzmir
            clinical_diagnosis='none',
            family_allergy_history=True,
            previous_allergic_reactions={
                'anaphylaxis': False,
                'severe_asthma': False,
                'hospitalization': False
            },
            current_medications=[],
            tree_pollen_allergy={
                'birch': False,
                'olive': True,
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
                'apple': False,
                'nuts': False,
                'shellfish': False
            },
            environmental_triggers={
                'dust_mites': False,
                'pet_dander': False,
                'mold': True,
                'air_pollution': False,
                'smoke': False
            }
        )
        
        # 4. Teşhis Almamış (Grup 4)
        users['undiagnosed'] = UserPreferences(
            age=45,
            gender='male',
            location={'latitude': 36.2194, 'longitude': 36.1611},  # Hatay
            clinical_diagnosis='none',
            family_allergy_history=False,
            previous_allergic_reactions={
                'anaphylaxis': False,
                'severe_asthma': False,
                'hospitalization': False
            },
            current_medications=[],
            tree_pollen_allergy={
                'birch': False,
                'olive': False,
                'pine': False
            },
            grass_pollen_allergy={
                'graminales': False
            },
            weed_pollen_allergy={
                'ragweed': False,
                'mugwort': False
            },
            food_allergies={
                'apple': False,
                'nuts': False,
                'shellfish': False
            },
            environmental_triggers={
                'dust_mites': False,
                'pet_dander': False,
                'mold': False,
                'air_pollution': True,
                'smoke': False
            }
        )
        
        # 5. Hassas Çocuk (Grup 5)
        users['vulnerable_child'] = UserPreferences(
            age=8,
            gender='male',
            location={'latitude': 37.0662, 'longitude': 37.3833},  # Şanlıurfa
            clinical_diagnosis='none',
            family_allergy_history=True,
            previous_allergic_reactions={
                'anaphylaxis': False,
                'severe_asthma': False,
                'hospitalization': False
            },
            current_medications=[],
            tree_pollen_allergy={
                'birch': False,
                'olive': True,
                'pine': False
            },
            grass_pollen_allergy={
                'graminales': True
            },
            weed_pollen_allergy={
                'ragweed': False,
                'mugwort': False
            },
            food_allergies={
                'apple': False,
                'nuts': True,
                'shellfish': False
            },
            environmental_triggers={
                'dust_mites': True,
                'pet_dander': False,
                'mold': False,
                'air_pollution': True,
                'smoke': True
            }
        )
        
        # 6. Hassas Yaşlı (Grup 5)
        users['vulnerable_elderly'] = UserPreferences(
            age=72,
            gender='female',
            location={'latitude': 41.0039, 'longitude': 39.7168},  # Trabzon
            clinical_diagnosis='none',
            family_allergy_history=False,
            previous_allergic_reactions={
                'anaphylaxis': False,
                'severe_asthma': False,
                'hospitalization': False
            },
            current_medications=['bronchodilator'],
            tree_pollen_allergy={
                'birch': False,
                'olive': False,
                'pine': True
            },
            grass_pollen_allergy={
                'graminales': False
            },
            weed_pollen_allergy={
                'ragweed': False,
                'mugwort': True
            },
            food_allergies={
                'apple': False,
                'nuts': False,
                'shellfish': False
            },
            environmental_triggers={
                'dust_mites': True,
                'pet_dander': True,
                'mold': True,
                'air_pollution': True,
                'smoke': True
            }
        )
        
        return users
    
    def run_comprehensive_demo(self):
        """Kapsamlı demo çalıştır"""
        print("\\n" + "="*60)
        print("🧬 ALLERMİND KAPSAMLI DEMONSTRASyon")
        print("="*60)
        
        # 1. Grup Sınıflandırma Testi
        self.test_group_classification()
        
        # 2. Risk Tahmin Testi
        self.test_risk_prediction()
        
        # 3. Farklı Şehirler için Karşılaştırma
        self.test_city_comparison()
        
        # 4. Zaman Serisi Analizi
        self.test_time_series_analysis()
        
        # 5. Performans Analizi
        self.test_performance_analysis()
        
        print("\\n✅ Demo tamamlandı!")
    
    def test_group_classification(self):
        """Grup sınıflandırma testleri"""
        print("\\n📊 GRUP SINIFLANDIRMA TESTLERİ")
        print("-" * 40)
        
        for user_type, user_prefs in self.demo_users.items():
            result = self.group_classifier.determine_allergy_group(user_prefs)
            
            print(f"\\n👤 {user_type.upper()}:")
            print(f"  Yaş: {user_prefs.age}, Cinsiyet: {user_prefs.gender}")
            print(f"  Klinik Tanı: {user_prefs.clinical_diagnosis}")
            print(f"  ➜ GRUP {result['group_id']}: {result['group_name']}")
            print(f"  Neden: {result['assignment_reason']}")
            print(f"  Model Ağırlığı: {result['model_weight']}")
            
            # Kişisel modifikasyonlar
            modifiers = result['personal_risk_modifiers']
            if any(v != 1.0 for v in modifiers.values()):
                print("  🔧 Kişisel Modifikasyonlar:")
                for key, value in modifiers.items():
                    if value != 1.0:
                        print(f"    {key}: {value:.2f}")
    
    def test_risk_prediction(self):
        """Risk tahmin testleri"""
        print("\\n🎯 RİSK TAHMİN TESTLERİ")
        print("-" * 40)
        
        # Her kullanıcı için tahmin yap
        for user_type, user_prefs in self.demo_users.items():
            location = (user_prefs.location['latitude'], user_prefs.location['longitude'])
            
            try:
                result = self.predictor.predict_allergy_risk(user_prefs, location)
                
                print(f"\\n🏥 {user_type.upper()} TAHMİNİ:")
                print(f"  Risk Skoru: {result.risk_score:.3f}")
                print(f"  Risk Seviyesi: {result.risk_level.upper()}")
                print(f"  Güven Aralığı: {result.confidence:.2f}")
                print(f"  Veri Kalitesi: {result.data_quality_score:.2f}")
                
                # En önemli faktörler
                factors = result.contributing_factors
                max_factor = max(factors.items(), key=lambda x: abs(x[1]))
                print(f"  En Önemli Faktör: {max_factor[0]} ({max_factor[1]:.3f})")
                
                # Öneriler (ilk 2 tanesi)
                print("  💡 Öneriler:")
                for rec in result.recommendations[:2]:
                    print(f"    • {rec}")
                
            except Exception as e:
                print(f"  ❌ Tahmin hatası: {e}")
    
    def test_city_comparison(self):
        """Şehir karşılaştırma testleri"""
        print("\\n🏙️ ŞEHİR KARŞILAŞTIRMA ANALİZİ")
        print("-" * 40)
        
        # Test için bir kullanıcı seç
        test_user = self.demo_users['moderate_patient']
        
        # Türkiye'nin farklı şehirleri
        cities = {
            'İstanbul': (41.0082, 28.9784),
            'Ankara': (39.9334, 32.8597),
            'İzmir': (38.4192, 27.1287),
            'Antalya': (36.8969, 30.7133),
            'Trabzon': (41.0039, 39.7168)
        }
        
        results = {}
        
        for city_name, location in cities.items():
            try:
                result = self.predictor.predict_allergy_risk(test_user, location)
                results[city_name] = {
                    'risk_score': result.risk_score,
                    'risk_level': result.risk_level,
                    'confidence': result.confidence
                }
            except Exception as e:
                print(f"  ❌ {city_name} için tahmin hatası: {e}")
                continue
        
        # Sonuçları görüntüle
        if results:
            print("\\n📈 Şehirler arası risk karşılaştırması:")
            sorted_cities = sorted(results.items(), key=lambda x: x[1]['risk_score'], reverse=True)
            
            for i, (city, data) in enumerate(sorted_cities, 1):
                print(f"  {i}. {city}: {data['risk_score']:.3f} ({data['risk_level'].upper()})")
    
    def test_time_series_analysis(self):
        """Zaman serisi analizi"""
        print("\\n⏰ ZAMAN SERİSİ ANALİZİ")
        print("-" * 40)
        
        # Test kullanıcısı ve konumu
        test_user = self.demo_users['moderate_patient']
        test_location = (test_user.location['latitude'], test_user.location['longitude'])
        
        # 7 gün için tahmin
        base_date = datetime.now()
        predictions = []
        
        for i in range(7):
            target_date = base_date + timedelta(days=i)
            
            try:
                result = self.predictor.predict_allergy_risk(test_user, test_location, target_date)
                predictions.append({
                    'date': target_date.strftime('%Y-%m-%d'),
                    'day': target_date.strftime('%A'),
                    'risk_score': result.risk_score,
                    'risk_level': result.risk_level
                })
            except Exception as e:
                print(f"  ❌ {target_date.strftime('%Y-%m-%d')} için tahmin hatası: {e}")
                continue
        
        if predictions:
            print("\\n📅 7 Günlük Risk Tahmini:")
            for pred in predictions:
                risk_emoji = self._get_risk_emoji(pred['risk_level'])
                print(f"  {pred['date']} ({pred['day'][:3]}): {pred['risk_score']:.3f} {risk_emoji}")
    
    def test_performance_analysis(self):
        """Performans analizi"""
        print("\\n⚡ PERFORMANS ANALİZİ")
        print("-" * 40)
        
        # Model bilgilerini göster
        try:
            model_info = self.predictor.get_model_info()
            
            print(f"  Yüklü Modeller: {model_info['loaded_models']}")
            print(f"  Özellik Sayısı: {len(model_info['data_loader_features'])}")
            print(f"  Ensemble Versiyonu: {model_info['ensemble_config'].get('version', 'N/A')}")
            
            # Risk eşikleri
            print("  Risk Eşikleri:")
            for level, threshold in model_info['risk_thresholds'].items():
                print(f"    {level.capitalize()}: {threshold:.1f}")
                
        except Exception as e:
            print(f"  ❌ Performans bilgisi alınamadı: {e}")
        
        # Hız testi
        import time
        test_user = self.demo_users['moderate_patient']
        test_location = (test_user.location['latitude'], test_user.location['longitude'])
        
        start_time = time.time()
        try:
            result = self.predictor.predict_allergy_risk(test_user, test_location)
            end_time = time.time()
            
            prediction_time = (end_time - start_time) * 1000  # milisaniye
            print(f"\\n  ⏱️ Tahmin Süresi: {prediction_time:.1f} ms")
            
        except Exception as e:
            print(f"  ❌ Hız testi başarısız: {e}")
    
    def _get_risk_emoji(self, risk_level: str) -> str:
        """Risk seviyesine göre emoji döndür"""
        emojis = {
            'low': '🟢',
            'moderate': '🟡',
            'high': '🟠',
            'severe': '🔴'
        }
        return emojis.get(risk_level, '⚪')
    
    def run_interactive_demo(self):
        """İnteraktif demo"""
        print("\\n" + "="*50)
        print("🎮 İNTERAKTİF ALLERMİND DEMOSu")
        print("="*50)
        
        while True:
            print("\\n📋 Mevcut Demo Kullanıcıları:")
            for i, (user_type, user_prefs) in enumerate(self.demo_users.items(), 1):
                print(f"  {i}. {user_type} (Yaş: {user_prefs.age}, Şehir: Türkiye)")
            
            print("\\n  0. Çıkış")
            
            try:
                choice = input("\\nBir kullanıcı seçin (0-6): ").strip()
                
                if choice == '0':
                    print("👋 Demo sonlandırıldı!")
                    break
                
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(self.demo_users):
                    user_types = list(self.demo_users.keys())
                    selected_user_type = user_types[choice_idx]
                    selected_user = self.demo_users[selected_user_type]
                    
                    self._run_single_user_demo(selected_user_type, selected_user)
                else:
                    print("❌ Geçersiz seçim!")
                    
            except (ValueError, IndexError):
                print("❌ Lütfen geçerli bir sayı girin!")
            except KeyboardInterrupt:
                print("\\n👋 Demo sonlandırıldı!")
                break
    
    def _run_single_user_demo(self, user_type: str, user_prefs: UserPreferences):
        """Tek kullanıcı için detaylı demo"""
        print(f"\\n🔍 {user_type.upper()} DETAYLI ANALİZİ")
        print("-" * 40)
        
        # Grup sınıflandırması
        group_result = self.group_classifier.determine_allergy_group(user_prefs)
        print(f"\\n👥 GRUP SINIFLANDIRMASI:")
        print(f"  Grup: {group_result['group_name']} (ID: {group_result['group_id']})")
        print(f"  Neden: {group_result['assignment_reason']}")
        
        # Risk tahmini
        location = (user_prefs.location['latitude'], user_prefs.location['longitude'])
        
        try:
            result = self.predictor.predict_allergy_risk(user_prefs, location)
            
            print(f"\\n🎯 RİSK TAHMİNİ:")
            print(f"  Risk Skoru: {result.risk_score:.3f}")
            print(f"  Risk Seviyesi: {result.risk_level.upper()} {self._get_risk_emoji(result.risk_level)}")
            print(f"  Güven Aralığı: {result.confidence:.2f}")
            
            print(f"\\n🧬 KATKIDA BULUNAN FAKTÖRLER:")
            for factor, value in result.contributing_factors.items():
                if abs(value) > 0.1:  # Önemli faktörleri göster
                    print(f"  {factor}: {value:.3f}")
            
            print(f"\\n💡 ÖNERİLER:")
            for i, rec in enumerate(result.recommendations, 1):
                print(f"  {i}. {rec}")
                
            print(f"\\n🌡️ ÇEVRESEL DURUM:")
            for risk, value in result.environmental_risks.items():
                if value > 0:
                    print(f"  {risk}: {value:.1f}")
        
        except Exception as e:
            print(f"❌ Tahmin hatası: {e}")
        
        input("\\nDevam etmek için Enter'a basın...")


def generate_demo_report():
    """Demo raporu oluştur"""
    print("\\n📄 DEMO RAPORU OLUŞTURULUYOR...")
    
    demo = AllerMindDemo()
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'system_info': {
            'models_loaded': len(demo.predictor.models),
            'demo_users': len(demo.demo_users)
        },
        'test_results': {},
        'recommendations': []
    }
    
    # Her kullanıcı için test
    for user_type, user_prefs in demo.demo_users.items():
        try:
            # Grup sınıflandırması
            group_result = demo.group_classifier.determine_allergy_group(user_prefs)
            
            # Risk tahmini
            location = (user_prefs.location['latitude'], user_prefs.location['longitude'])
            prediction_result = demo.predictor.predict_allergy_risk(user_prefs, location)
            
            report['test_results'][user_type] = {
                'group_id': group_result['group_id'],
                'group_name': group_result['group_name'],
                'risk_score': prediction_result.risk_score,
                'risk_level': prediction_result.risk_level,
                'confidence': prediction_result.confidence
            }
            
        except Exception as e:
            report['test_results'][user_type] = {'error': str(e)}
    
    # Raporu kaydet
    report_file = f"/Users/elifdy/Desktop/allermind/aller-mind/DATA/WORK-MODEL/demo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Demo raporu kaydedildi: {report_file}")
    return report


if __name__ == "__main__":
    # Ana demo menüsü
    print("🧬 ALLERMİND DEMO SİSTEMİ")
    print("=" * 30)
    print("1. Kapsamlı Demo Çalıştır")
    print("2. İnteraktif Demo")
    print("3. Demo Raporu Oluştur")
    print("0. Çıkış")
    
    while True:
        try:
            choice = input("\\nSeçiminizi yapın (0-3): ").strip()
            
            if choice == '0':
                print("👋 Çıkış yapılıyor...")
                break
            elif choice == '1':
                demo = AllerMindDemo()
                demo.run_comprehensive_demo()
            elif choice == '2':
                demo = AllerMindDemo()
                demo.run_interactive_demo()
            elif choice == '3':
                generate_demo_report()
            else:
                print("❌ Geçersiz seçim!")
                
        except KeyboardInterrupt:
            print("\\n👋 Demo sonlandırıldı!")
            break
        except Exception as e:
            print(f"❌ Hata oluştu: {e}")