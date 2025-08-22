import pandas as pd
import numpy as np
import joblib
import os
import json

class AllergyPredictor:
    def __init__(self, model_dir='saved_models'):
        """
        Load trained models for prediction
        
        Parameters:
        model_dir (str): Directory containing saved models
        """
        self.model_dir = model_dir
        self.model = None
        self.features = None
        
        # Load model and features
        self._load_model()
    
    def _load_model(self):
        """Load the best trained model"""
        # First load features
        feature_path = os.path.join(self.model_dir, 'features.pkl')
        if os.path.exists(feature_path):
            self.features = joblib.load(feature_path)
        else:
            raise FileNotFoundError(f"Features file not found at {feature_path}")
        
        # Try to load the best model (gradient_boosting preferred)
        model_types = ['gradient_boosting', 'random_forest', 'svm']
        
        for model_type in model_types:
            model_path = os.path.join(self.model_dir, f'{model_type}.pkl')
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                self.model_type = model_type
                print(f"Loaded {model_type} model from {model_path}")
                break
        
        if self.model is None:
            raise FileNotFoundError(f"No trained models found in {self.model_dir}")
    
    def predict(self, weather_data, pollen_data=None):
        """
        Make allergy group predictions based on current environmental data
        
        Parameters:
        weather_data (dict): Current weather API response data
        pollen_data (dict, optional): Current pollen API response data
        
        Returns:
        dict: Prediction results with group, confidence, and recommendations
        """
        # Process weather data
        processed_data = self._process_input_data(weather_data, pollen_data)
        
        # Make prediction
        group, confidence, all_probs = self._predict_group(processed_data)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            group, confidence, processed_data, all_probs
        )
        
        # Return comprehensive result
        return {
            'allergy_group': int(group),
            'group_name': self._get_group_name(group),
            'confidence': float(confidence),
            'all_probabilities': {i+1: float(p) for i, p in enumerate(all_probs)},
            'recommendations': recommendations,
            'risk_level': self._calculate_risk_level(group, processed_data, confidence),
            'contributing_factors': self._identify_contributing_factors(group, processed_data)
        }
    
    def _process_input_data(self, weather_data, pollen_data=None):
        """Process API responses into model input format"""
        # Extract current weather conditions (assuming hourly data)
        if 'hourly' in weather_data:
            # Get latest hour data
            weather = {k: v[0] if isinstance(v, list) and len(v) > 0 else v 
                      for k, v in weather_data['hourly'].items()}
        else:
            weather = weather_data
        
        # Extract pollen data if available
        pollen = {}
        if pollen_data:
            if 'dailyInfo' in pollen_data and len(pollen_data['dailyInfo']) > 0:
                daily = pollen_data['dailyInfo'][0]
                if 'pollenTypeInfo' in daily:
                    for pollen_type in daily['pollenTypeInfo']:
                        code = pollen_type['code'].lower()
                        if 'indexInfo' in pollen_type:
                            pollen[code] = pollen_type['indexInfo'].get('value', 0)
        
        # Create DataFrame with required features
        df = pd.DataFrame([{
            # Weather features
            'temperature_2m': weather.get('temperature_2m', 20),
            'relative_humidity_2m': weather.get('relative_humidity_2m', 50),
            'precipitation': weather.get('precipitation', 0),
            'snowfall': weather.get('snowfall', 0),
            'rain': weather.get('rain', 0),
            'cloud_cover': weather.get('cloud_cover', 0),
            'surface_pressure': weather.get('surface_pressure', 1013),
            'wind_speed_10m': weather.get('wind_speed_10m', 5),
            'wind_direction_10m': weather.get('wind_direction_10m', 180),
            'soil_temperature_0_to_7cm': weather.get('soil_temperature_0_to_7cm', 15),
            'soil_moisture_0_to_7cm': weather.get('soil_moisture_0_to_7cm', 0.3),
            'sunshine_duration': weather.get('sunshine_duration', 0),
            
            # Air quality features
            'pm10': weather.get('pm10', 15),
            'pm2_5': weather.get('pm2_5', 10),
            'carbon_dioxide': weather.get('carbon_dioxide', 400),
            'carbon_monoxide': weather.get('carbon_monoxide', 150),
            'nitrogen_dioxide': weather.get('nitrogen_dioxide', 15),
            'sulphur_dioxide': weather.get('sulphur_dioxide', 10),
            'ozone': weather.get('ozone', 80),
            'aerosol_optical_depth': weather.get('aerosol_optical_depth', 0.2),
            'methane': weather.get('methane', 1500),
            'uv_index': weather.get('uv_index', 3),
            'uv_index_clear_sky': weather.get('uv_index_clear_sky', 4),
            'dust': weather.get('dust', 1),
            
            # Pollen features
            'grass': pollen.get('grass', 0),
            'tree': pollen.get('tree', 0),
            'weed': pollen.get('weed', 0)
        }])
        
        # Add missing features with default values
        for feature in self.features:
            if feature not in df.columns:
                df[feature] = 0
        
        return df[self.features]
    
    def _predict_group(self, data):
        """Make prediction and return group, confidence, and all probabilities"""
        # Get probability for each class
        probabilities = self.model.predict_proba(data)[0]
        
        # Get predicted class (1-based indexing)
        predicted_class = np.argmax(probabilities) + 1
        
        # Get confidence (probability of predicted class)
        confidence = probabilities[predicted_class - 1]
        
        return predicted_class, confidence, probabilities
    
    def _get_group_name(self, group):
        """Get descriptive name for allergy group"""
        group_names = {
            1: "Severe Allergic Asthma",
            2: "Mild to Moderate Allergic",
            3: "Possible Allergic/High Risk",
            4: "Not Yet Diagnosed",
            5: "Vulnerable Population"
        }
        return group_names.get(group, "Unknown Group")
    
    def _generate_recommendations(self, group, confidence, data, probabilities):
        """Generate personalized recommendations based on group and current conditions"""
        recommendations = []
        
        # Common recommendations for all groups
        if confidence < 0.4:
            recommendations.append(
                "Prediction confidence is low. Consider consulting with a healthcare provider for a personalized assessment."
            )
        
        # Group-specific recommendations
        if group == 1:  # Severe Allergic Asthma
            # Check pollen levels
            pollen_sum = data['tree'].values[0] + data['grass'].values[0] + data['weed'].values[0]
            if pollen_sum > 5:
                recommendations.append(
                    "⚠️ High pollen levels detected. Consider staying indoors with windows closed and use HEPA air purifiers."
                )
            
            # Check air quality indicators
            pm25 = data['pm2_5'].values[0]
            ozone = data['ozone'].values[0]
            no2 = data['nitrogen_dioxide'].values[0]
            
            if pm25 > 25 or ozone > 100 or no2 > 40:
                recommendations.append(
                    "⚠️ Poor air quality today. Consider wearing an N95 mask when outdoors and limit outdoor activities."
                )
            
            recommendations.append(
                "Keep rescue medication readily accessible and follow your asthma action plan."
            )
            
            recommendations.append(
                "Consider using a peak flow meter to monitor your lung function regularly."
            )
                
        elif group == 2:  # Mild to Moderate Allergic
            # Check pollen and air quality
            pollen_sum = data['tree'].values[0] + data['grass'].values[0] + data['weed'].values[0]
            pm10 = data['pm10'].values[0]
            
            if pollen_sum > 3:
                recommendations.append(
                    "Moderate pollen levels today. Consider taking your antihistamine medication before symptoms start."
                )
            
            if pm10 > 50:
                recommendations.append(
                    "Elevated particulate matter levels. Consider limiting prolonged outdoor activities."
                )
            
            recommendations.append(
                "Showering after being outdoors can help remove pollen from hair and skin."
            )
            
        elif group == 3:  # Possible Allergic/High Risk
            # Check air quality indicators
            pm25 = data['pm2_5'].values[0]
            ozone = data['ozone'].values[0]
            
            if pm25 > 20 or ozone > 80:
                recommendations.append(
                    "Current air quality may trigger respiratory symptoms. Monitor for any unusual reactions."
                )
            
            recommendations.append(
                "If you experience consistent symptoms like sneezing, itchy eyes, or breathing difficulties, consider consulting an allergist."
            )
            
            recommendations.append(
                "Keep a symptom diary to track any patterns in your reactions to different environments."
            )
            
        elif group == 4:  # Not Yet Diagnosed
            # General recommendations for air quality awareness
            aqi_factors = [data['pm10'].values[0], data['pm2_5'].values[0], data['ozone'].values[0]]
            if any(factor > 50 for factor in aqi_factors):
                recommendations.append(
                    "General air quality is reduced today. Consider limiting intense outdoor activities if you notice any discomfort."
                )
            
            recommendations.append(
                "Stay hydrated and maintain general respiratory health."
            )
            
        elif group == 5:  # Vulnerable Population
            # Temperature concerns
            temp = data['temperature_2m'].values[0]
            humidity = data['relative_humidity_2m'].values[0]
            pm25 = data['pm2_5'].values[0]
            
            if temp > 30:
                recommendations.append(
                    "⚠️ High temperatures can strain respiratory systems. Stay in air-conditioned environments and stay hydrated."
                )
            elif temp < 5:
                recommendations.append(
                    "⚠️ Cold air can trigger respiratory symptoms. Cover your nose and mouth with a scarf when outdoors."
                )
            
            if humidity > 80:
                recommendations.append(
                    "High humidity may increase mold growth. Use dehumidifiers indoors if available."
                )
            elif humidity < 30:
                recommendations.append(
                    "Low humidity can dry mucous membranes. Consider using a humidifier indoors."
                )
            
            if pm25 > 15:
                recommendations.append(
                    "⚠️ Sensitive individuals should limit outdoor exposure today due to elevated fine particulate matter."
                )
            
            recommendations.append(
                "Ensure all prescribed medications are readily available and follow healthcare provider guidelines carefully."
            )
        
        return recommendations
    
    def _calculate_risk_level(self, group, data, confidence):
        """Calculate overall risk level based on conditions"""
        risk_level = "Low"
        risk_score = 0
        
        # Base risk on prediction confidence
        if confidence > 0.8:
            risk_score += 2
        elif confidence > 0.6:
            risk_score += 1
        
        # Group-specific risk factors
        if group == 1:  # Severe Allergic Asthma
            # Most critical factors for Group 1
            pm25 = data['pm2_5'].values[0]
            pollen_sum = data['tree'].values[0] + data['grass'].values[0] + data['weed'].values[0]
            ozone = data['ozone'].values[0]
            no2 = data['nitrogen_dioxide'].values[0]
            
            if pm25 > 25: risk_score += 3
            elif pm25 > 12: risk_score += 2
            
            if pollen_sum > 9: risk_score += 3
            elif pollen_sum > 4: risk_score += 2
            
            if ozone > 100: risk_score += 2
            elif ozone > 80: risk_score += 1
            
            if no2 > 40: risk_score += 2
            elif no2 > 20: risk_score += 1
            
        elif group == 2:  # Mild to Moderate Allergic
            pm10 = data['pm10'].values[0]
            pollen_sum = data['tree'].values[0] + data['grass'].values[0]
            ozone = data['ozone'].values[0]
            
            if pm10 > 50: risk_score += 2
            elif pm10 > 30: risk_score += 1
            
            if pollen_sum > 6: risk_score += 2
            elif pollen_sum > 3: risk_score += 1
            
            if ozone > 100: risk_score += 1
            
        elif group == 3:  # Possible Allergic/High Risk
            pm25 = data['pm2_5'].values[0]
            pm10 = data['pm10'].values[0]
            ozone = data['ozone'].values[0]
            
            if pm25 > 20: risk_score += 2
            elif pm25 > 10: risk_score += 1
            
            if pm10 > 40: risk_score += 1
            
            if ozone > 80: risk_score += 1
            
        elif group == 4:  # Not Yet Diagnosed
            # General air quality indicators
            pm10 = data['pm10'].values[0]
            ozone = data['ozone'].values[0]
            
            if pm10 > 70: risk_score += 1
            
            if ozone > 120: risk_score += 1
            
        elif group == 5:  # Vulnerable Population
            # Temperature extremes, humidity extremes, and air quality
            temp = data['temperature_2m'].values[0]
            humidity = data['relative_humidity_2m'].values[0]
            pm25 = data['pm2_5'].values[0]
            
            if temp > 32 or temp < 0: risk_score += 3
            elif temp > 30 or temp < 5: risk_score += 2
            
            if humidity > 85 or humidity < 25: risk_score += 2
            elif humidity > 80 or humidity < 30: risk_score += 1
            
            if pm25 > 15: risk_score += 3
            elif pm25 > 7: risk_score += 2
        
        # Determine risk level
        if risk_score >= 5:
            risk_level = "High"
        elif risk_score >= 3:
            risk_level = "Medium"
        
        return risk_level
    
    def _identify_contributing_factors(self, group, data):
        """Identify key factors contributing to current risk"""
        factors = []
        
        if group == 1:  # Severe Allergic Asthma
            # Check pollen levels
            for pollen_type in ['tree', 'grass', 'weed']:
                if data[pollen_type].values[0] > 1:
                    factors.append({
                        "factor": f"{pollen_type.capitalize()} Pollen",
                        "value": float(data[pollen_type].values[0]),
                        "impact": "high" if data[pollen_type].values[0] > 4 else "medium"
                    })
            
            # Check air pollutants
            if data['pm2_5'].values[0] > 10:
                factors.append({
                    "factor": "Fine Particulate Matter (PM2.5)",
                    "value": float(data['pm2_5'].values[0]),
                    "impact": "high" if data['pm2_5'].values[0] > 25 else "medium"
                })
            
            if data['ozone'].values[0] > 80:
                factors.append({
                    "factor": "Ozone",
                    "value": float(data['ozone'].values[0]),
                    "impact": "high" if data['ozone'].values[0] > 100 else "medium"
                })
                
            if data['nitrogen_dioxide'].values[0] > 20:
                factors.append({
                    "factor": "Nitrogen Dioxide",
                    "value": float(data['nitrogen_dioxide'].values[0]),
                    "impact": "high" if data['nitrogen_dioxide'].values[0] > 40 else "medium"
                })
            
        elif group == 2:  # Mild to Moderate Allergic
            if data['pm10'].values[0] > 30:
                factors.append({
                    "factor": "Particulate Matter (PM10)",
                    "value": float(data['pm10'].values[0]),
                    "impact": "high" if data['pm10'].values[0] > 50 else "medium"
                })
                
            for pollen_type in ['tree', 'grass']:
                if data[pollen_type].values[0] > 1:
                    factors.append({
                        "factor": f"{pollen_type.capitalize()} Pollen",
                        "value": float(data[pollen_type].values[0]),
                        "impact": "high" if data[pollen_type].values[0] > 3 else "medium"
                    })
            
            if data['ozone'].values[0] > 80:
                factors.append({
                    "factor": "Ozone",
                    "value": float(data['ozone'].values[0]),
                    "impact": "medium"
                })
            
        elif group == 3:  # Possible Allergic/High Risk
            if data['pm2_5'].values[0] > 10:
                factors.append({
                    "factor": "Fine Particulate Matter (PM2.5)",
                    "value": float(data['pm2_5'].values[0]),
                    "impact": "high" if data['pm2_5'].values[0] > 20 else "medium"
                })
                
            if data['pm10'].values[0] > 30:
                factors.append({
                    "factor": "Particulate Matter (PM10)",
                    "value": float(data['pm10'].values[0]),
                    "impact": "medium"
                })
            
            if data['ozone'].values[0] > 80:
                factors.append({
                    "factor": "Ozone",
                    "value": float(data['ozone'].values[0]),
                    "impact": "medium"
                })
                
            # Add total pollen load
            pollen_sum = data['tree'].values[0] + data['grass'].values[0] + data['weed'].values[0]
            if pollen_sum > 2:
                factors.append({
                    "factor": "Total Pollen Load",
                    "value": float(pollen_sum),
                    "impact": "medium" if pollen_sum > 5 else "low"
                })
            
        elif group == 4:  # Not Yet Diagnosed
            # General air quality indicators
            if data['pm10'].values[0] > 50:
                factors.append({
                    "factor": "Particulate Matter (PM10)",
                    "value": float(data['pm10'].values[0]),
                    "impact": "medium"
                })
                
            if data['ozone'].values[0] > 100:
                factors.append({
                    "factor": "Ozone",
                    "value": float(data['ozone'].values[0]),
                    "impact": "medium"
                })
            
        elif group == 5:  # Vulnerable Population
            # Temperature extremes
            temp = data['temperature_2m'].values[0]
            if temp > 30 or temp < 5:
                factors.append({
                    "factor": "Temperature",
                    "value": float(temp),
                    "impact": "high" if temp > 32 or temp < 0 else "medium"
                })
                
            # Humidity extremes
            humidity = data['relative_humidity_2m'].values[0]
            if humidity > 80 or humidity < 30:
                factors.append({
                    "factor": "Humidity",
                    "value": float(humidity),
                    "impact": "high" if humidity > 85 or humidity < 25 else "medium"
                })
                
            # Fine particulate matter
            if data['pm2_5'].values[0] > 7:
                factors.append({
                    "factor": "Fine Particulate Matter (PM2.5)",
                    "value": float(data['pm2_5'].values[0]),
                    "impact": "high" if data['pm2_5'].values[0] > 15 else "medium"
                })
        
        return factors

# Example usage
if __name__ == "__main__":
    # Example weather and pollen data (simplified)
    sample_weather_data = {
        "hourly": {
            "time": ["2025-08-14T00:00"],
            "temperature_2m": [28.5],
            "relative_humidity_2m": [65],
            "precipitation": [0],
            "cloud_cover": [20],
            "wind_speed_10m": [8.5],
            "pm10": [35.2],
            "pm2_5": [18.6],
            "ozone": [90.3],
            "uv_index": [6.2],
            "nitrogen_dioxide": [25.4]
        }
    }
    
    sample_pollen_data = {
        "dailyInfo": [
            {
                "pollenTypeInfo": [
                    {
                        "code": "GRASS",
                        "indexInfo": {"value": 3}
                    },
                    {
                        "code": "TREE",
                        "indexInfo": {"value": 2}
                    },
                    {
                        "code": "WEED",
                        "indexInfo": {"value": 1}
                    }
                ]
            }
        ]
    }
    
    try:
        # Initialize predictor
        predictor = AllergyPredictor()
        
        # Make prediction
        result = predictor.predict(sample_weather_data, sample_pollen_data)
        
        # Display results
        print("Allergy Prediction Results:")
        print(f"Group: {result['allergy_group']} - {result['group_name']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Risk Level: {result['risk_level']}")
        
        print("\nRecommendations:")
        for i, rec in enumerate(result['recommendations']):
            print(f"{i+1}. {rec}")
            
        print("\nContributing Factors:")
        for factor in result['contributing_factors']:
            print(f"- {factor['factor']}: {factor['value']} (Impact: {factor['impact']})")
            
        # Save sample output
        with open('sample_prediction.json', 'w') as f:
            json.dump(result, f, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")
