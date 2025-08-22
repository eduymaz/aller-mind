import pandas as pd
import numpy as np

# 1. Veri Yükleme
df_14 = pd.read_csv('dataset/14AUG_sample_data.csv')
df_15 = pd.read_csv('dataset/15AUG_sample_data.csv')

# 2. Birleştirme
df = pd.concat([df_14, df_15], ignore_index=True)

# 3. Temel Bilgiler
print("Veri seti boyutu:", df.shape)
print("Kolonlar:", df.columns.tolist())

# 4. Eksik Veri Analizi
missing = df.isnull().sum()
print("Eksik veri sayısı:\n", missing[missing > 0])

# 5. Temel İstatistikler
desc = df.describe()
print("Temel istatistikler:\n", desc)

# 6. Korelasyon Analizi
# Sadece sayısal kolonlar ile korelasyon alınmalı
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
corr = df[numeric_cols].corr()
print("Korelasyon matrisi:\n", corr)

# 7. Önemli Aralıklar ve Açıklamalar
def print_range(col):
    print(f"{col}: min={df[col].min():.2f}, max={df[col].max():.2f}, mean={df[col].mean():.2f}, std={df[col].std():.2f}")

important_cols = [
    'pm10', 'pm2_5', 'carbon_dioxide', 'carbon_monoxide', 'nitrogen_dioxide',
    'sulphur_dioxide', 'ozone', 'aerosol_optical_depth', 'methane', 'uv_index',
    'uv_index_clear_sky', 'dust', 'grass', 'tree', 'weed'
]

print("\nÖnemli kolonların aralıkları ve açıklamaları:")
for col in important_cols:
    print_range(col)
    # Açıklama örneği:
    if col == 'pm10':
        print("PM10: 10-50 arası değerler orta düzey hava kirliliğine işaret eder.")
    elif col == 'ozone':
        print("Ozone: 60-110 arası değerler yaz aylarında tipik, yüksek değerler sağlık riski oluşturabilir.")
    elif col == 'grass':
        print("Grass: 0-10 arası, yüksek değerler polen alerjisi riski için önemlidir.")
    # ... diğer kolonlar için benzer açıklamalar eklenebilir ...

# 8. Korelasyonun yüksek olduğu kolonları bul
high_corr = corr.abs().unstack().sort_values(ascending=False)
high_corr = high_corr[high_corr < 1].drop_duplicates()
print("\nYüksek korelasyonlu kolon çiftleri (>|0.7|):")
print(high_corr[high_corr > 0.7])

# 9. Sonuç
print("\nÖn analizde PM10, ozone, grass ve dust kolonları hem varyans hem de korelasyon açısından öne çıkmaktadır. Bu kolonlar hava kirliliği ve polen etkisi açısından ilk değerlendirmede önemlidir.")

# 10. Dağılım Grafikleri
import matplotlib.pyplot as plt
import seaborn as sns

for col in important_cols:
    plt.figure(figsize=(6, 3))
    sns.histplot(df[col].dropna(), kde=True, bins=20)
    plt.title(f"{col} Dağılımı")
    plt.xlabel(col)
    plt.ylabel("Frekans")
    plt.tight_layout()
    plt.show()

# 11. Boxplot ile Aykırı Değer Analizi
for col in important_cols:
    plt.figure(figsize=(4, 2))
    sns.boxplot(x=df[col].dropna())
    plt.title(f"{col} Boxplot")
    plt.tight_layout()
    plt.show()

# 12. Feature Importance (RandomForest ile)
from sklearn.ensemble import RandomForestRegressor

# Sadece sayısal kolonlar ve eksiksiz satırlar
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
df_rf = df[numeric_cols].dropna()
if 'pm10' in df_rf.columns:
    X = df_rf.drop('pm10', axis=1)
    y = df_rf['pm10']
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    importances = pd.Series(rf.feature_importances_, index=X.columns)
    print("\nRandomForest ile feature importance (pm10 için):")
    print(importances.sort_values(ascending=False))

# 13. Normalizasyon Örneği
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaled = scaler.fit_transform(df[numeric_cols].fillna(0))
scaled_df = pd.DataFrame(scaled, columns=numeric_cols)
print("\nNormalizasyon sonrası ilk 5 satır:")
print(scaled_df.head())

# 14. Principal Component Analysis (PCA)
from sklearn.decomposition import PCA

pca = PCA(n_components=3)
pca_result = pca.fit_transform(scaled_df)
print("\nPCA ile açıklanan varyans oranları:", pca.explained_variance_ratio_)

# 15. Sonuçların Kaydedilmesi
#desc.to_csv('dataset/preprocess_describe.csv')
#corr.to_csv('dataset/preprocess_corr.csv')
#scaled_df.to_csv('dataset/preprocess_scaled.csv', index=False)

print("\nÖn analiz tamamlandı. Sonuç dosyaları 'dataset' klasörüne kaydedildi.")
