#!/usr/bin/env python3
"""
AllerMind Tahmin Sistemi Test ve Örnek Kullanımlar
================================================

Bu dosya, allermind_predictor.py sisteminin test edilmesi ve
örnek kullanımları için yazılmıştır.
"""

from allermind_predictor import AllerMindPredictor
import pandas as pd
from datetime import datetime, timedelta

def test_basic_functionality():
    """Temel fonksiyonalite testleri"""
    print("🧪 TEMEL FONKSİYONALİTE TESTLERİ")
    print("="*50)
    
    # Predictor başlat
    predictor = AllerMindPredictor("pkl_models")
    predictor.load_models()
    
    if len(predictor.models) == 0:
        print("❌ Test başarısız: Model yüklenemedi")
        return False
    
    print(f"✅ {len(predictor.models)} model başarıyla yüklendi")
    
    # Tek grup testi
    print("\n🔍 Tek grup testi (Grup 1, Ankara)...")
    result = predictor.predict_for_group(1, "Ankara", "2025-09-11")
    
    if 'error' in result:
        print(f"❌ Tek grup testi başarısız: {result['error']}")
        return False
    
    print("✅ Tek grup testi başarılı")
    
    # Çoklu grup testi
    print("\n🔍 Çoklu grup testi (Tüm gruplar, İstanbul)...")
    results = predictor.predict_all_groups("Istanbul", "2025-09-11")
    
    if not results or len(results) == 0:
        print("❌ Çoklu grup testi başarısız")
        return False
    
    print(f"✅ Çoklu grup testi başarılı ({len(results)} grup)")
    
    return True

def test_different_cities():
    """Farklı şehirler için test"""
    print("\n🏙️ FARKLI ŞEHİRLER TESTİ")
    print("="*40)
    
    predictor = AllerMindPredictor("pkl_models")
    predictor.load_models()
    
    cities = ["Ankara", "Istanbul", "Izmir", "Bursa", "Antalya", "Konya"]
    
    for city in cities:
        print(f"\n📍 {city} için tahmin...")
        result = predictor.predict_for_group(1, city, "2025-09-11")
        
        if 'error' not in result:
            print(f"   Risk Skoru: {result['risk_skoru']}")
            print(f"   Risk Seviyesi: {result['risk_seviyesi']}")
            print(f"   ✅ Başarılı")
        else:
            print(f"   ❌ Hata: {result['error']}")

def test_different_dates():
    """Farklı tarihler için test"""
    print("\n📅 FARKLI TARİHLER TESTİ")
    print("="*40)
    
    predictor = AllerMindPredictor("pkl_models")
    predictor.load_models()
    
    # Gelecek 7 gün
    for i in range(7):
        test_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        print(f"\n📅 {test_date} için tahmin...")
        
        result = predictor.predict_for_group(2, "Ankara", test_date)
        
        if 'error' not in result:
            print(f"   Risk Skoru: {result['risk_skoru']}")
            print(f"   Güvenli Saat: {result['guvenli_saat_tahmini']}")
            print(f"   ✅ Başarılı")
        else:
            print(f"   ❌ Hata: {result['error']}")

def test_custom_data():
    """Özel veri ile test"""
    print("\n🎛️ ÖZEL VERİ TESTİ")
    print("="*30)
    
    predictor = AllerMindPredictor("pkl_models")
    predictor.load_models()
    
    # Yüksek polen senaryosu
    high_pollen_data = {
        'tree_pollen_index': 80.0,    # Çok yüksek
        'grass_pollen_index': 60.0,   # Yüksek
        'weed_pollen_index': 45.0,    # Yüksek
        'pm2_5': 15.0,                # Düşük
        'pm10': 25.0,                 # Düşük
        'no2': 20.0,                  # Düşük
        'ozone': 70.0,                # Normal
        'so2': 10.0,                  # Düşük
        'co': 1.0,                    # Düşük
        'temperature_2m': 25.0,       # İdeal
        'relative_humidity_2m': 65.0, # Normal
        'wind_speed_10m': 5.0,        # Düşük rüzgar
        'surface_pressure': 1013.0,   # Normal
        'uv_index': 6.0,              # Orta
        'visibility': 20.0,           # İyi
        'cloud_cover': 30.0,          # Az bulutlu
        'dew_point_2m': 15.0,         # Normal
        'precipitation': 0.0          # Yağmur yok
    }
    
    print("🌸 Yüksek polen senaryosu testi...")
    result = predictor.predict_for_group(1, "Ankara", "2025-09-11", high_pollen_data)
    
    if 'error' not in result:
        predictor.print_prediction_report(result)
    else:
        print(f"❌ Hata: {result['error']}")
    
    # Yüksek kirlilik senaryosu
    high_pollution_data = {
        'tree_pollen_index': 10.0,    # Düşük
        'grass_pollen_index': 8.0,    # Düşük
        'weed_pollen_index': 5.0,     # Düşük
        'pm2_5': 80.0,                # Çok yüksek
        'pm10': 120.0,                # Çok yüksek
        'no2': 100.0,                 # Çok yüksek
        'ozone': 150.0,               # Yüksek
        'so2': 40.0,                  # Yüksek
        'co': 3.5,                    # Yüksek
        'temperature_2m': 30.0,       # Sıcak
        'relative_humidity_2m': 40.0, # Düşük
        'wind_speed_10m': 2.0,        # Çok düşük rüzgar
        'surface_pressure': 1010.0,   # Düşük
        'uv_index': 9.0,              # Yüksek
        'visibility': 5.0,            # Kötü
        'cloud_cover': 80.0,          # Çok bulutlu
        'dew_point_2m': 18.0,         # Yüksek
        'precipitation': 0.0          # Yağmur yok
    }
    
    print("\n🏭 Yüksek kirlilik senaryosu testi...")
    result = predictor.predict_for_group(2, "Istanbul", "2025-09-11", high_pollution_data)
    
    if 'error' not in result:
        predictor.print_prediction_report(result)
    else:
        print(f"❌ Hata: {result['error']}")

def create_comparison_report():
    """Grup karşılaştırma raporu oluştur"""
    print("\n📊 GRUP KARŞILAŞTIRMA RAPORU")
    print("="*50)
    
    predictor = AllerMindPredictor("pkl_models")
    predictor.load_models()
    
    cities = ["Ankara", "Istanbul", "Izmir"]
    
    comparison_data = []
    
    for city in cities:
        print(f"\n📍 {city} için tüm grupların karşılaştırması:")
        print("-" * 40)
        
        results = predictor.predict_all_groups(city, "2025-09-11")
        
        for group_id, result in results.items():
            if 'error' not in result:
                comparison_data.append({
                    'Şehir': city,
                    'Grup': f"Grup {group_id}",
                    'Grup Adı': result['grup_adi'],
                    'Risk Skoru': result['risk_skoru'],
                    'Risk Seviyesi': result['risk_seviyesi'],
                    'Güvenli Saat': result['guvenli_saat_tahmini']
                })
                
                print(f"Grup {group_id}: Risk {result['risk_skoru']}, "
                      f"Güvenli {result['guvenli_saat_tahmini']}h, "
                      f"{result['risk_seviyesi']}")
    
    # DataFrame oluştur
    df = pd.DataFrame(comparison_data)
    
    if not df.empty:
        print(f"\n📋 ÖZET TABLO:")
        print("="*80)
        print(df.to_string(index=False))
        
        # CSV olarak kaydet
        df.to_csv("allermind_karsilastirma_raporu.csv", index=False)
        print(f"\n💾 Rapor 'allermind_karsilastirma_raporu.csv' olarak kaydedildi")

def performance_test():
    """Performans testi"""
    print("\n⚡ PERFORMANS TESTİ")
    print("="*30)
    
    import time
    
    predictor = AllerMindPredictor("pkl_models")
    predictor.load_models()
    
    # 100 tahmin süre testi
    start_time = time.time()
    
    for i in range(100):
        result = predictor.predict_for_group(1, "Ankara", "2025-09-11")
    
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = total_time / 100
    
    print(f"📊 100 tahmin toplam süre: {total_time:.2f} saniye")
    print(f"📊 Ortalama tahmin süresi: {avg_time*1000:.2f} ms")
    print(f"📊 Saniyede tahmin sayısı: {100/total_time:.1f}")

def main():
    """Ana test fonksiyonu"""
    print("🌿 ALLERMIND TAHMİN SİSTEMİ TEST PAKETİ")
    print("="*60)
    print("Test başlıyor...\n")
    
    try:
        # Temel testler
        if not test_basic_functionality():
            print("❌ Temel testler başarısız!")
            return
        
        # Şehir testleri
        test_different_cities()
        
        # Tarih testleri
        test_different_dates()
        
        # Özel veri testleri
        test_custom_data()
        
        # Karşılaştırma raporu
        create_comparison_report()
        
        # Performans testi
        performance_test()
        
        print(f"\n{'='*60}")
        print("✅ TÜM TESTLER BAŞARIYLA TAMAMLANDI!")
        print("📝 Sistem kullanıma hazır.")
        
    except Exception as e:
        print(f"\n❌ TEST HATASI: {str(e)}")

if __name__ == "__main__":
    main()
