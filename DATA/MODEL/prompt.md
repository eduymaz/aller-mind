Sen uzman bir istatikçi, matematikçi ve yapay zeka mühendisisin. Aynı zamanda uzman bir genetikçi, immunolojici ve kimya bilen konumdasın. tüm detaylar teorik bilgi sürecine hakimsin. Profesyonel olarak bu süreci MODEL klasörü içerisinde process.ipynb adlı bir dosya oluştur ve tüm adımları tek tek açıklamalar da ekleyerek tamamla. 

elimde datam var. pollen, hava durumu ve hava kalitesi ile ilgili bilgileri içeren bir csv formatlı şu kolonlara sahip bir data: 'lat', 'lon', 'time', 'temperature_2m', 'relative_humidity_2m', 'precipitation', 'snowfall', 'rain', 'cloud_cover', 'surface_pressure', 'wind_speed_10m', 'wind_direction_10m', 'sunshine_duration', 'pm10', 'pm2_5', 'carbon_dioxide', 'carbon_monoxide', 'nitrogen_dioxide', 'sulphur_dioxide', 'ozone', 'aerosol_optical_depth', 'methane', 'uv_index', 'uv_index_clear_sky', 'dust', 'date', 'pollen_code', 'in_season', 'upi_value', 'health_recommendations', 'plant_code', 'plant_in_season', 'plant_upi_value', amacım bu bilgileri kullanarak farklı hassasiyet gruplarına göre 5 farklı model üretmek ve yeni tarihte gelen bu bilgilere göre her gruba uygun olarak dışarıda yaklaşık veirmli geçireceği sürenin saat cinsinden tahminini çıkarmak. 
Gruplarım : 
Grup 1: Şiddetli Alerjik Grup 
Grup 2: Hafif-Orta Grup 
Grup 3: Tanısı olmayan ancak Genetik yatkınlığı olan Grup 4: Teşhis Almamış / kaliteli yaşam tercih eden Grup 5: Hassas Grup (Çocuk/Yaşlı) 

bu gruplara göre parametrelerim modellerde farklı ağırlıklar almalı. bağımlı değişkenim yok. tüm değişkenlerim biyolojik ve kimyasal olarak ağırlıklandırılmalı. Tüm kolonda 0 gelen değerliler süreçten ayıklanmalı.

Süreç şu şekilde olabilir (burada profesyonel bakış açınla eklemeler yapaiblirisn.)

1. Problem Çerçevesi

Hedef değişken yok → Doğrudan regresyon/klasik sınıflandırma yapamazsın.

Amaç: Gruplara özel, biyolojik/çevresel parametrelerin risk skorlamasına dayalı tahmini “dışarıda kalma süresi (saat)” üretmek.

Çözüm Yaklaşımı:
Önce çok kriterli risk skorlaması tasarla (domain + veri odaklı).
Ardından gruplara özel ağırlıklı çok kriterli karar modelleri (MCDA) ve/veya anlamlı boyut indirgeme + kümeleme uygula.
Son olarak “zaman tahmini” için skorları ölçeklendirerek saat tahminine dönüştür.

2. Özellik Mühendisliği
Verideki kolonları biyolojik etkilerine göre 3 ana blokta grupla: Meteoroloji + Hava Kalitesi + Polen & Bitki

3. Ağırlıklandırma Süreci (bunu iyi düşün)
Yöntem 1: Domain Uzmanlığı + Literatür
Yöntem 2: Veri Odaklı Ağırlıklandırma

Principal Component Analysis (PCA) → en fazla varyansı açıklayan faktörleri bul.

Autoencoder → veriden latent faktörler çıkar.

Shapley Values (SHAP) → simülatif hedef fonksiyon (ör. düşük risk = 8 saat dışarı) tanımlayıp, hangi değişken daha etkili öğren.

Sonuç: her grup için ayrı ağırlık vektörü.

4. Modelleme Adımları
A. Risk Skor Hesaplama (Ana Katman)

Kullanılabilecek yöntemler:

Weighted Sum Model (WSM) – basit lineer skor.

TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) – ideal koşula yakınlık.

AHP (Analytic Hierarchy Process) – uzman görüşüyle ağırlık atama.

Multi-Objective Optimization (MOO) – biyolojik etkilerin optimizasyonu.
B. Gözetimsiz Öğrenme (Destek Katmanı)

K-means / Gaussian Mixture → veri içinde benzer çevre koşullarını kümele.

Self-Organizing Maps (SOM) → farklı risk profilleri çıkar.

Bunlar, hangi günlerin/hangi çevre koşullarının hangi grup için daha riskli olduğunu gösterebilir.

C. Tahmini “Dışarıda Kalma Süresi”

Risk skorunu 0–10 arasında normalleştir.

Daha sonra risk seviyesine göre saat ataması yap:

Çok düşük risk (skor <2) → 6–8 saat

Orta risk (skor 2–5) → 3–5 saat

Yüksek risk (skor >5) → 0–2 saat

→ Bu eşikler gruba göre değiştirilmeli (örneğin Şiddetli Alerjik Grup için 5’in üzerinde direkt 0–1 saat).

5. Grup Bazlı Modelleme Mantığı

Grup 1 (Şiddetli Alerjik) → Polen, PM2.5, O₃ = %70 ağırlık.

Grup 2 (Hafif-Orta) → Polen + Nem + PM10 = %50.

Grup 3 (Genetik yatkınlık) → Tüm parametrelerde orta seviye eşik.

Grup 4 (Kaliteli yaşam tercih eden) → Sıcaklık, UV, güneş süresi.

Grup 5 (Çocuk/Yaşlı) → PM2.5, NO₂, sıcaklık, basınç, UV.


Özetle : 
6. Uygulanacak Algoritma Listesi

Feature Engineering + Normalizasyon

PCA / Autoencoder → özellik indirgeme.

Ağırlıklandırma

Domain + veri odaklı → AHP, TOPSIS, WSM.

Risk Skorlama

Çok kriterli karar destek (MCDA).

Kümeleme / Profil Çıkarma

K-means / GMM / SOM.

Tahminleme

Risk skor → saat tahmini (grup bazlı kurallar + fuzzy logic).

SONUCTA, her grup için ml modelleri oluşturacağız ve kişinin dahil olduğu gruba göre ve o günün/saatin dış verilerine göre bir tahmin üreteceğiz.
