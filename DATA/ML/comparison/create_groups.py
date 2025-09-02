import pandas as pd
import numpy as np

def create_allergy_groups():
    """
    AllerMind veri setine 5 farklı allerji grubu ekle
    """
    print("📊 Veri yükleniyor...")
    df = pd.read_csv('cleaned_combined_data.csv')
    print(f"✅ {len(df)} satır veri yüklendi")
    
    print("\n🔧 Allerji grupları oluşturuluyor...")
    
    # Normalize edilmiş faktörler (0-1 arası)
    df['temp_norm'] = (df['temperature_2m'] - df['temperature_2m'].min()) / (df['temperature_2m'].max() - df['temperature_2m'].min())
    df['humidity_norm'] = df['relative_humidity_2m'] / 100
    df['pm10_norm'] = df['pm10'] / df['pm10'].max()
    df['pm25_norm'] = df['pm2_5'] / df['pm2_5'].max()
    df['upi_norm'] = df['upi_value'] / df['upi_value'].max()
    df['plant_upi_norm'] = df['plant_upi_value'] / df['plant_upi_value'].max()
    
    # 5 farklı allerji grubu tanımla
    # Grup 1: Çocuklar (0-12 yaş) - En hassas grup
    df['group_1'] = (
        df['upi_norm'] * 0.4 +           # Pollen en önemli
        df['plant_upi_norm'] * 0.3 +     # Bitki polleni
        df['pm25_norm'] * 0.2 +          # İnce partiküller
        df['temp_norm'] * 0.1            # Sıcaklık
    ) * 10  # 0-10 risk skoru
    
    # Grup 2: Astımlılar - Hava kalitesine çok duyarlı
    df['group_2'] = (
        df['pm10_norm'] * 0.35 +         # Kaba partiküller
        df['pm25_norm'] * 0.35 +         # İnce partiküller
        df['humidity_norm'] * 0.15 +     # Nem
        df['upi_norm'] * 0.15            # Pollen
    ) * 10
    
    # Grup 3: Yaşlılar (65+) - Genel hassaslık
    df['group_3'] = (
        df['temp_norm'] * 0.3 +          # Sıcaklık değişimi
        df['humidity_norm'] * 0.25 +     # Nem oranı
        df['upi_norm'] * 0.25 +          # Pollen
        df['pm10_norm'] * 0.2            # Hava kalitesi
    ) * 10
    
    # Grup 4: Seasonal Allerji - Mevsimsel hassaslık
    df['group_4'] = (
        df['upi_norm'] * 0.5 +           # Ana pollen faktörü
        df['plant_upi_norm'] * 0.3 +     # Bitki polleni
        df['temp_norm'] * 0.1 +          # Sıcaklık
        df['humidity_norm'] * 0.1        # Nem
    ) * 10
    
    # Grup 5: Genel Nüfus - Ortalama hassaslık
    df['group_5'] = (
        df['upi_norm'] * 0.25 +          # Pollen
        df['pm10_norm'] * 0.25 +         # Hava kalitesi
        df['temp_norm'] * 0.25 +         # Sıcaklık
        df['humidity_norm'] * 0.25       # Nem
    ) * 10
    
    # Risk skorlarını 0-10 arasında sınırla
    for group in ['group_1', 'group_2', 'group_3', 'group_4', 'group_5']:
        df[group] = np.clip(df[group], 0, 10)
    
    print("✅ 5 allerji grubu oluşturuldu:")
    print("  - Group 1: Çocuklar (0-12 yaş)")
    print("  - Group 2: Astımlılar")
    print("  - Group 3: Yaşlılar (65+)")
    print("  - Group 4: Mevsimsel Allerji")
    print("  - Group 5: Genel Nüfus")
    
    # Geçici normalizasyon kolonlarını sil
    temp_cols = ['temp_norm', 'humidity_norm', 'pm10_norm', 'pm25_norm', 'upi_norm', 'plant_upi_norm']
    df = df.drop(columns=temp_cols)
    
    # Güncellenmiş veriyi kaydet
    df.to_csv('cleaned_combined_data.csv', index=False)
    print(f"\n💾 Veri güncellendi: {len(df)} satır, {len(df.columns)} kolon")
    
    # Grup istatistikleri
    print("\n📈 Grup İstatistikleri:")
    for group in ['group_1', 'group_2', 'group_3', 'group_4', 'group_5']:
        mean_risk = df[group].mean()
        std_risk = df[group].std()
        print(f"  {group}: Ortalama {mean_risk:.2f} ± {std_risk:.2f}")
    
    return df

if __name__ == "__main__":
    create_allergy_groups()
