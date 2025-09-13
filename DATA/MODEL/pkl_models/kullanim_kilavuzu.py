
# MODEL KULLANIM ÖRNEĞİ:
import pickle
import numpy as np

# Model yükle
with open('pkl_models/Grup1_Siddetli_Alerjik_model.pkl', 'rb') as f:
    model_package = pickle.load(f)

model = model_package['model']
scaler = model_package['scaler']
features = model_package['features']

# Yeni veri için tahmin
new_data = {
    'upi_value': 3.5,
    'pm2_5': 25.0,
    'ozone': 85.0,
    'temperature_2m': 28.0,
    'relative_humidity_2m': 70.0,
    'uv_index': 7.0,
    # ... diğer özellikler
}

# Veriyi hazırla
X_new = np.array([[new_data[feat] for feat in features]])
X_new_scaled = scaler.transform(X_new)

# Tahmin yap
prediction = model.predict(X_new_scaled)[0]
print(f"Güvenli kalma süresi: {prediction:.1f} saat")



'''
Grup 1 Özellik listesi (26 özellik):
 1. upi_value
 2. plant_upi_value
 3. in_season
 4. plant_in_season
 5. pm2_5
 6. pm10
 7. ozone
 8. nitrogen_dioxide
 9. sulphur_dioxide
10. carbon_monoxide
11. temperature_2m
12. relative_humidity_2m
13. precipitation
14. snowfall
15. rain
16. cloud_cover
17. surface_pressure
18. wind_speed_10m
19. wind_direction_10m
20. soil_temperature_0_to_7cm
21. soil_moisture_0_to_7cm
22. sunshine_duration
23. uv_index
24. uv_index_clear_sky
25. dust
26. methane
'''