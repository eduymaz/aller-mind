#!/usr/bin/env python3
"""
AllerMind Work-Model Ana Çalışma Dosyası
Kişiselleştirilmiş Alerji Risk Tahmini Sistemi

Bu dosya AllerMind sisteminin tüm bileşenlerini bir araya getirir ve
kullanıcıların kolayca sistemi çalıştırabilmesi için ana arayüzü sağlar.

Kullanım:
    python main.py

Date: 16 Eylül 2025
Version: 1.0
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Kendi modüllerimizi import et
try:
    from user_preference_system import UserPreferences, AllergyGroupClassifier, create_sample_user_preferences
    from allermind_predictor import AllerMindPredictor, create_test_user
    from data_loader import DataLoader
    from demo_system import AllerMindDemo, generate_demo_report
except ImportError as e:
    print(f"❌ Modül import hatası: {e}")
    print("Lütfen tüm gerekli dosyaların WORK-MODEL klasöründe olduğundan emin olun.")
    sys.exit(1)


class AllerMindApp:
    """
    AllerMind ana uygulama sınıfı
    Kullanıcı arayüzü ve sistem yönetimi
    """
    
    def __init__(self):
        self.predictor = None
        self.classifier = None
        self.data_loader = None
        self.initialize_system()
    
    def initialize_system(self):
        """Sistemi başlat"""
        print("🧬 AllerMind Sistem Başlatılıyor...")
        print("=" * 50)
        
        try:
            # Bileşenleri yükle
            self.predictor = AllerMindPredictor()
            self.classifier = AllergyGroupClassifier()
            self.data_loader = DataLoader()
            
            # Veri dosyalarını kontrol et
            if self.data_loader.validate_data_files():
                print("✅ Veri dosyları doğrulandı")
            else:
                print("⚠️  Bazı veri dosyaları eksik - sınırlı mod aktif")
            
            # Model durumunu kontrol et
            model_info = self.predictor.get_model_info()
            loaded_models = model_info['loaded_models']
            print(f"✅ {len(loaded_models)} grup modeli yüklendi: {loaded_models}")
            
            print("🎉 Sistem başarıyla başlatıldı!")
            
        except Exception as e:
            print(f"❌ Sistem başlatma hatası: {e}")
            print("🔧 Lütfen kurulum kılavuzunu kontrol edin")
            sys.exit(1)
    
    def show_main_menu(self):
        """Ana menüyü göster"""
        print("\\n" + "=" * 60)
        print("🧬 ALLERMİND - Kişiselleştirilmiş Alerji Risk Tahmini")
        print("=" * 60)
        print("1. 🎯 Hızlı Risk Tahmini")
        print("2. 👤 Detaylı Kullanıcı Profili Oluştur")
        print("3. 📊 Grup Sınıflandırma Testi")
        print("4. 🏙️ Şehir Karşılaştırması")
        print("5. 📅 Zaman Serisi Analizi")
        print("6. 🎮 Demo Sistemi")
        print("7. 📄 Rapor Oluştur")
        print("8. ℹ️  Sistem Bilgileri")
        print("9. 📖 Kullanım Kılavuzu")
        print("0. 🚪 Çıkış")
        print("-" * 60)
    
    def run(self):
        """Ana döngü"""
        while True:
            self.show_main_menu()
            
            try:
                choice = input("\\nSeçiminizi yapın (0-9): ").strip()
                
                if choice == '0':
                    print("👋 AllerMind kapatılıyor...")
                    break
                elif choice == '1':
                    self.quick_prediction()
                elif choice == '2':
                    self.create_detailed_profile()
                elif choice == '3':
                    self.test_group_classification()
                elif choice == '4':
                    self.city_comparison()
                elif choice == '5':
                    self.time_series_analysis()
                elif choice == '6':
                    self.run_demo_system()
                elif choice == '7':
                    self.generate_report()
                elif choice == '8':
                    self.show_system_info()
                elif choice == '9':
                    self.show_user_guide()
                else:
                    print("❌ Geçersiz seçim! Lütfen 0-9 arası bir sayı girin.")
                    
            except KeyboardInterrupt:
                print("\\n👋 Program sonlandırıldı!")
                break
            except Exception as e:
                print(f"❌ Beklenmeyen hata: {e}")
                input("Devam etmek için Enter'a basın...")
    
    def quick_prediction(self):
        """Hızlı risk tahmini"""
        print("\\n🎯 HIZLI RİSK TAHMİNİ")
        print("-" * 30)
        
        # Örnek kullanıcı profilleri
        print("Hazır profiller:")
        print("1. Hafif alerjik hasta (28 yaş, kadın)")
        print("2. Şiddetli alerjik hasta (35 yaş, erkek)")  
        print("3. Çocuk hasta (8 yaş)")
        print("4. Yaşlı hasta (72 yaş)")
        
        try:
            profile_choice = input("Profil seçin (1-4): ").strip()
            
            # Profil oluştur
            if profile_choice == '1':
                user = create_sample_user_preferences()
                user.clinical_diagnosis = 'mild_moderate_allergy'
            elif profile_choice == '2':
                user = create_test_user()
                user.clinical_diagnosis = 'severe_allergy'
            elif profile_choice == '3':
                user = create_sample_user_preferences()
                user.age = 8
            elif profile_choice == '4':
                user = create_sample_user_preferences()
                user.age = 72
            else:
                print("❌ Geçersiz profil seçimi!")
                return
            
            # Konum al
            print("\\nKonum seçin:")
            print("1. İstanbul (41.0082, 28.9784)")
            print("2. Ankara (39.9334, 32.8597)")
            print("3. İzmir (38.4192, 27.1287)")
            print("4. Manuel konum gir")
            
            location_choice = input("Konum seçin (1-4): ").strip()
            
            if location_choice == '1':
                location = (41.0082, 28.9784)
                city_name = "İstanbul"
            elif location_choice == '2':
                location = (39.9334, 32.8597)
                city_name = "Ankara"
            elif location_choice == '3':
                location = (38.4192, 27.1287)
                city_name = "İzmir"
            elif location_choice == '4':
                lat = float(input("Enlem girin: "))
                lon = float(input("Boylam girin: "))
                location = (lat, lon)
                city_name = f"({lat}, {lon})"
            else:
                print("❌ Geçersiz konum seçimi!")
                return
            
            # Tahmin yap
            print(f"\\n🔄 {city_name} için risk tahmini yapılıyor...")
            result = self.predictor.predict_allergy_risk(user, location)
            
            # Sonuçları göster
            self.display_prediction_result(result, city_name)
            
        except ValueError:
            print("❌ Geçersiz giriş!")
        except Exception as e:
            print(f"❌ Tahmin hatası: {e}")
        
        input("\\nDevam etmek için Enter'a basın...")
    
    def create_detailed_profile(self):
        """Detaylı kullanıcı profili oluştur"""
        print("\\n👤 DETAYLI KULLANICI PROFİLİ")
        print("-" * 35)
        
        try:
            # Temel bilgiler
            age = int(input("Yaşınız: "))
            gender = input("Cinsiyetiniz (male/female/other): ").strip().lower()
            
            # Konum bilgileri  
            print("\\nKonum bilgileri:")
            lat = float(input("Enlem: "))
            lon = float(input("Boylam: "))
            
            # Klinik bilgiler
            print("\\nKlinik durum:")
            print("1. Alerji tanısı yok")
            print("2. Hafif-orta alerji")
            print("3. Şiddetli alerji")
            print("4. Astım")
            
            clinical_choice = input("Klinik durumunuz (1-4): ").strip()
            clinical_map = {
                '1': 'none',
                '2': 'mild_moderate_allergy', 
                '3': 'severe_allergy',
                '4': 'asthma'
            }
            clinical_diagnosis = clinical_map.get(clinical_choice, 'none')
            
            # Aile geçmişi
            family_history = input("Ailede alerji geçmişi var mı? (y/n): ").strip().lower() == 'y'
            
            # Polen hassasiyetleri
            print("\\nPolen hassasiyetleriniz (y/n):")
            tree_allergies = {}
            tree_allergies['birch'] = input("Huş ağacı: ").strip().lower() == 'y'
            tree_allergies['olive'] = input("Zeytin: ").strip().lower() == 'y'
            tree_allergies['pine'] = input("Çam: ").strip().lower() == 'y'
            
            grass_allergies = {}
            grass_allergies['graminales'] = input("Çim poleni: ").strip().lower() == 'y'
            
            weed_allergies = {}
            weed_allergies['ragweed'] = input("Karaot: ").strip().lower() == 'y'
            weed_allergies['mugwort'] = input("Pelin: ").strip().lower() == 'y'
            
            # Besin alerjileri
            print("\\nBesin alerjileriniz (y/n):")
            food_allergies = {}
            food_allergies['apple'] = input("Elma: ").strip().lower() == 'y'
            food_allergies['nuts'] = input("Fındık/fıstık: ").strip().lower() == 'y'
            food_allergies['shellfish'] = input("Kabuklu deniz ürünleri: ").strip().lower() == 'y'
            
            # Çevresel tetikleyiciler
            print("\\nÇevresel tetikleyiciler (y/n):")
            env_triggers = {}
            env_triggers['dust_mites'] = input("Ev tozu akarı: ").strip().lower() == 'y'
            env_triggers['pet_dander'] = input("Hayvan tüyü: ").strip().lower() == 'y'
            env_triggers['mold'] = input("Küf: ").strip().lower() == 'y'
            env_triggers['air_pollution'] = input("Hava kirliliği: ").strip().lower() == 'y'
            env_triggers['smoke'] = input("Duman: ").strip().lower() == 'y'
            
            # UserPreferences nesnesi oluştur
            user = UserPreferences(
                age=age,
                gender=gender,
                location={'latitude': lat, 'longitude': lon},
                clinical_diagnosis=clinical_diagnosis,
                family_allergy_history=family_history,
                previous_allergic_reactions={
                    'anaphylaxis': False,
                    'severe_asthma': clinical_diagnosis in ['severe_allergy', 'asthma'],
                    'hospitalization': clinical_diagnosis == 'severe_allergy'
                },
                current_medications=[],
                tree_pollen_allergy=tree_allergies,
                grass_pollen_allergy=grass_allergies,
                weed_pollen_allergy=weed_allergies,
                food_allergies=food_allergies,
                environmental_triggers=env_triggers
            )
            
            # Grup belirleme
            group_result = self.classifier.determine_allergy_group(user)
            
            print(f"\\n📊 GRUP SINIFLANDIRMA SONUCU:")
            print(f"Grup: {group_result['group_name']} (ID: {group_result['group_id']})")
            print(f"Neden: {group_result['assignment_reason']}")
            
            # Risk tahmini yap mı?
            if input("\\nRisk tahmini yapmak ister misiniz? (y/n): ").strip().lower() == 'y':
                result = self.predictor.predict_allergy_risk(user, (lat, lon))
                self.display_prediction_result(result, f"({lat}, {lon})")
            
        except ValueError:
            print("❌ Geçersiz sayısal değer!")
        except Exception as e:
            print(f"❌ Profil oluşturma hatası: {e}")
        
        input("\\nDevam etmek için Enter'a basın...")
    
    def test_group_classification(self):
        """Grup sınıflandırma testi"""
        print("\\n📊 GRUP SINIFLANDIRMA TESTİ")
        print("-" * 35)
        
        # Demo kullanıcıları oluştur
        demo = AllerMindDemo()
        
        print("Demo kullanıcıları ve grup atamaları:\\n")
        
        for user_type, user_prefs in demo.demo_users.items():
            result = self.classifier.determine_allergy_group(user_prefs)
            
            print(f"👤 {user_type.upper()}:")
            print(f"  Yaş: {user_prefs.age}, Klinik: {user_prefs.clinical_diagnosis}")
            print(f"  ➜ GRUP {result['group_id']}: {result['group_name']}")
            print(f"  Neden: {result['assignment_reason']}")
            print(f"  Ağırlık: {result['model_weight']}")
            print()
        
        input("Devam etmek için Enter'a basın...")
    
    def city_comparison(self):
        """Şehir karşılaştırması"""
        print("\\n🏙️ ŞEHİR KARŞILAŞTIRMASI")
        print("-" * 25)
        
        # Test kullanıcısı oluştur
        user = create_sample_user_preferences()
        
        # Şehirler
        cities = {
            'İstanbul': (41.0082, 28.9784),
            'Ankara': (39.9334, 32.8597),
            'İzmir': (38.4192, 27.1287),
            'Antalya': (36.8969, 30.7133),
            'Trabzon': (41.0039, 39.7168)
        }
        
        print("Örnek kullanıcı için şehir karşılaştırması:\\n")
        
        results = []
        for city_name, location in cities.items():
            try:
                result = self.predictor.predict_allergy_risk(user, location)
                results.append((city_name, result.risk_score, result.risk_level))
                print(f"🔄 {city_name} analiz ediliyor...")
            except Exception as e:
                print(f"❌ {city_name} için hata: {e}")
        
        # Sonuçları sırala
        results.sort(key=lambda x: x[1], reverse=True)
        
        print("\\n📊 Risk sıralaması (yüksekten düşüğe):")
        for i, (city, risk_score, risk_level) in enumerate(results, 1):
            emoji = self._get_risk_emoji(risk_level)
            print(f"{i}. {city}: {risk_score:.3f} ({risk_level.upper()}) {emoji}")
        
        input("\\nDevam etmek için Enter'a basın...")
    
    def time_series_analysis(self):
        """Zaman serisi analizi"""
        print("\\n📅 ZAMAN SERİSİ ANALİZİ")
        print("-" * 25)
        
        # Test kullanıcısı ve konumu
        user = create_sample_user_preferences()
        
        print("Konum seçin:")
        print("1. İstanbul")
        print("2. Ankara")
        print("3. İzmir")
        
        location_choice = input("Seçim (1-3): ").strip()
        
        locations = {
            '1': ((41.0082, 28.9784), 'İstanbul'),
            '2': ((39.9334, 32.8597), 'Ankara'),
            '3': ((38.4192, 27.1287), 'İzmir')
        }
        
        if location_choice not in locations:
            print("❌ Geçersiz seçim!")
            return
        
        location, city_name = locations[location_choice]
        
        # Kaç gün analiz?
        try:
            days = int(input("Kaç günlük analiz? (1-14): "))
            if not (1 <= days <= 14):
                days = 7
        except ValueError:
            days = 7
        
        print(f"\\n🔄 {city_name} için {days} günlük analiz yapılıyor...")
        
        from datetime import datetime, timedelta
        
        base_date = datetime.now()
        daily_predictions = []
        
        for i in range(days):
            target_date = base_date + timedelta(days=i)
            
            try:
                result = self.predictor.predict_allergy_risk(user, location, target_date)
                daily_predictions.append({
                    'date': target_date.strftime('%Y-%m-%d'),
                    'day': target_date.strftime('%A'),
                    'risk_score': result.risk_score,
                    'risk_level': result.risk_level
                })
            except Exception as e:
                print(f"❌ {target_date.strftime('%Y-%m-%d')} için hata: {e}")
        
        if daily_predictions:
            print(f"\\n📈 {city_name} - {days} Günlük Risk Tahmini:")
            print("-" * 50)
            
            for pred in daily_predictions:
                emoji = self._get_risk_emoji(pred['risk_level'])
                print(f"{pred['date']} ({pred['day'][:3]}): {pred['risk_score']:.3f} ({pred['risk_level'].upper()}) {emoji}")
        
        input("\\nDevam etmek için Enter'a basın...")
    
    def run_demo_system(self):
        """Demo sistemi çalıştır"""
        print("\\n🎮 DEMO SİSTEMİ")
        print("-" * 15)
        
        demo = AllerMindDemo()
        
        print("1. Kapsamlı Demo")
        print("2. İnteraktif Demo")
        print("3. Geri dön")
        
        choice = input("Seçim (1-3): ").strip()
        
        if choice == '1':
            demo.run_comprehensive_demo()
        elif choice == '2':
            demo.run_interactive_demo()
        elif choice == '3':
            return
        else:
            print("❌ Geçersiz seçim!")
    
    def generate_report(self):
        """Rapor oluştur"""
        print("\\n📄 RAPOR OLUŞTURMA")
        print("-" * 20)
        
        print("1. Demo Raporu")
        print("2. Sistem Durum Raporu")
        print("3. Geri dön")
        
        choice = input("Seçim (1-3): ").strip()
        
        if choice == '1':
            report = generate_demo_report()
            print("✅ Demo raporu oluşturuldu!")
        elif choice == '2':
            self._generate_system_report()
        elif choice == '3':
            return
        else:
            print("❌ Geçersiz seçim!")
        
        input("\\nDevam etmek için Enter'a basın...")
    
    def show_system_info(self):
        """Sistem bilgilerini göster"""
        print("\\nℹ️  SİSTEM BİLGİLERİ")
        print("-" * 20)
        
        try:
            model_info = self.predictor.get_model_info()
            
            print(f"📊 Yüklü Modeller: {model_info['loaded_models']}")
            print(f"🔢 Özellik Sayısı: {len(model_info['data_loader_features'])}")
            print(f"⚙️ Ensemble Versiyonu: {model_info['ensemble_config'].get('version', 'N/A')}")
            
            print("\\n🎯 Risk Eşikleri:")
            for level, threshold in model_info['risk_thresholds'].items():
                print(f"  {level.capitalize()}: {threshold:.1f}")
            
            print("\\n🧬 İmmunolojik Gruplar:")
            for group_id in range(1, 6):
                if group_id in model_info['loaded_models']:
                    status = "✅ Aktif"
                else:
                    status = "❌ Eksik"
                print(f"  Grup {group_id}: {status}")
            
            # Veri durumu
            print("\\n💾 Veri Durumu:")
            if self.data_loader.validate_data_files():
                print("  ✅ Tüm veri dosyaları mevcut")
            else:
                print("  ⚠️ Bazı veri dosyaları eksik")
            
        except Exception as e:
            print(f"❌ Sistem bilgisi alınamadı: {e}")
        
        input("\\nDevam etmek için Enter'a basın...")
    
    def show_user_guide(self):
        """Kullanım kılavuzu göster"""
        print("\\n📖 KULLANIM KILAVUZU")
        print("-" * 20)
        
        guide_text = '''
🧬 ALLERMİND SİSTEMİ HAKKINDA

Bu sistem, kişiselleştirilmiş alerji risk tahmini yapar. Sistem 5 temel bileşenden oluşur:

1. 👤 KULLANICI PROFİLİ
   - Yaş, cinsiyet, konum
   - Klinik geçmiş ve tanılar
   - Polen, besin, çevresel hassasiyetler

2. 🧬 İMMUNOLOJİK GRUPLANDIRMA
   - Grup 1: Şiddetli Alerjik (IgE > 1000 IU/mL)
   - Grup 2: Hafif-Orta Alerjik (IgE 200-1000)
   - Grup 3: Genetik Yatkınlık
   - Grup 4: Teşhis Almamış
   - Grup 5: Hassas Çocuk/Yaşlı

3. 📊 VERİ ANALİZİ
   - Polen verileri (UPI değerleri)
   - Hava kalitesi (PM2.5, O3, NO2)
   - Hava durumu (sıcaklık, nem, rüzgar)

4. 🤖 MAKİNE ÖĞRENMESİ
   - Grup bazlı özelleştirilmiş modeller
   - Random Forest ve SVM algoritmaları
   - Ensemble tahmin sistemi

5. 🎯 RİSK TAHMİNİ
   - 0-1 arası risk skoru
   - Düşük/Orta/Yüksek/Şiddetli seviyeler
   - Kişiselleştirilmiş öneriler

⚠️ ÖNEMLİ NOTLAR:
- Bu sistem tıbbi tavsiye vermez
- Ciddi durumlar için doktora başvurun
- Sonuçlar sadece bilgilendirme amaçlıdır

📞 DESTEK:
Teknik sorunlar için README.md dosyasına bakın.
        '''
        
        print(guide_text)
        input("\\nDevam etmek için Enter'a basın...")
    
    def display_prediction_result(self, result, location_name):
        """Tahmin sonucunu görüntüle"""
        print(f"\\n🎯 {location_name} TAHMİN SONUÇLARI")
        print("=" * 50)
        
        # Ana sonuçlar
        risk_emoji = self._get_risk_emoji(result.risk_level)
        print(f"Risk Skoru: {result.risk_score:.3f}")
        print(f"Risk Seviyesi: {result.risk_level.upper()} {risk_emoji}")
        print(f"Güven Aralığı: {result.confidence:.2f}")
        print(f"Grup: {result.group_name} (ID: {result.group_id})")
        
        # Katkı faktörleri
        print("\\n🧮 KATKIDA BULUNAN FAKTÖRLER:")
        for factor, value in result.contributing_factors.items():
            if abs(value) > 0.05:  # Önemli faktörleri göster
                direction = "📈" if value > 0 else "📉"
                print(f"  {direction} {factor}: {value:.3f}")
        
        # Çevresel durumlar
        print("\\n🌡️ ÇEVRESEL DURUM:")
        for risk, value in result.environmental_risks.items():
            if value > 0:
                print(f"  {risk}: {value:.1f}")
        
        # Öneriler
        print("\\n💡 ÖNERİLER:")
        for i, rec in enumerate(result.recommendations[:5], 1):  # İlk 5 öneri
            print(f"  {i}. {rec}")
        
        print(f"\\n📊 Veri Kalitesi: {result.data_quality_score:.2f}")
        print(f"🕒 Tahmin Zamanı: {result.prediction_timestamp.strftime('%Y-%m-%d %H:%M')}")
    
    def _get_risk_emoji(self, risk_level: str) -> str:
        """Risk seviyesine göre emoji döndür"""
        emojis = {
            'low': '🟢',
            'moderate': '🟡', 
            'high': '🟠',
            'severe': '🔴'
        }
        return emojis.get(risk_level, '⚪')
    
    def _generate_system_report(self):
        """Sistem durum raporu oluştur"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_status': 'active',
            'models_loaded': len(self.predictor.models),
            'data_validation': self.data_loader.validate_data_files(),
            'feature_count': len(self.data_loader.get_feature_names()),
            'ensemble_version': self.predictor.ensemble_config.get('version', 'unknown')
        }
        
        report_file = f"/Users/elifdy/Desktop/allermind/aller-mind/DATA/WORK-MODEL/system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Sistem raporu kaydedildi: {report_file}")


def main():
    """Ana fonksiyon"""
    try:
        print("🧬 AllerMind Work-Model Sistemi")
        print("Versiyon 1.0 - 16 Eylül 2025")
        print()
        
        # Uygulamayı başlat
        app = AllerMindApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\\n👋 Program kullanıcı tarafından sonlandırıldı!")
    except Exception as e:
        print(f"\\n❌ Kritik hata: {e}")
        print("Lütfen README.md dosyasındaki troubleshooting bölümünü kontrol edin.")
    
    print("\\n🔚 AllerMind sistemi kapatıldı.")


if __name__ == "__main__":
    main()