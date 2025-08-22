import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.train_model import AllergyModel
from generate_test_data import generate_test_data

class ModelTester:
    def __init__(self, model_dir='../model/saved_models', test_data_path=None):
        """
        Initialize the model tester
        
        Parameters:
        model_dir (str): Directory containing saved models
        test_data_path (str): Path to test data file, if None will generate test data
        """
        self.model_dir = model_dir
        self.test_data_path = test_data_path
        
        # Load model
        self.model = AllergyModel(model_dir)
        
        # Load or generate test data
        if test_data_path and os.path.exists(test_data_path):
            self.test_data = pd.read_csv(test_data_path)
        else:
            self.test_data = self._generate_test_data()
    
    def _generate_test_data(self, n_samples=500):
        """Generate synthetic test data"""
        print("Generating synthetic test data...")
        return generate_test_data(n_samples)
    
    def run_tests(self, output_dir='results'):
        """
        Run tests on the model using test data
        
        Parameters:
        output_dir (str): Directory to save test results
        
        Returns:
        dict: Test results
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Make predictions
        X, y_true = self.model.preprocess_data(self.test_data)
        predictions, probabilities = self.model.predict(self.test_data)
        
        # Calculate metrics
        accuracy = accuracy_score(y_true, predictions)
        report = classification_report(y_true, predictions, output_dict=True)
        
        # Plot confusion matrix
        plt.figure(figsize=(8, 6))
        cm = confusion_matrix(y_true, predictions)
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion Matrix - Test Data')
        plt.colorbar()
        tick_marks = np.arange(len(np.unique(y_true)))
        plt.xticks(tick_marks, np.unique(y_true), rotation=45)
        plt.yticks(tick_marks, np.unique(y_true))
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.savefig(os.path.join(output_dir, 'test_confusion_matrix.png'))
        
        # Feature importance
        if 'random_forest' in self.model.models:
            plt.figure(figsize=(12, 8))
            # Get feature importance from the classifier in the pipeline
            feature_importance = self.model.models['random_forest'].named_steps['clf'].feature_importances_
            # Sort features by importance
            indices = np.argsort(feature_importance)[::-1]
            
            plt.title('Feature Importance')
            plt.bar(range(X.shape[1]), feature_importance[indices], align='center')
            plt.xticks(range(X.shape[1]), np.array(X.columns)[indices], rotation=90)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'feature_importance.png'))
        
        # Save test results
        test_results = {
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'test_size': len(y_true)
        }
        
        # Print results
        print(f"Test Results - Accuracy: {accuracy:.4f}")
        print("Classification Report:")
        print(classification_report(y_true, predictions))
        
        return test_results
    
    def test_edge_cases(self, output_dir='results'):
        """
        Test model on edge cases
        
        Parameters:
        output_dir (str): Directory to save test results
        
        Returns:
        dict: Edge case test results
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Create edge cases
        edge_cases = []
        
        # Case 1: Extreme heat with high pollen
        edge_cases.append({
            'name': 'Extreme Heat with High Pollen',
            'data': pd.DataFrame([{
                'temperature_2m': 40,
                'relative_humidity_2m': 20,
                'precipitation': 0,
                'snowfall': 0,
                'rain': 0,
                'cloud_cover': 0,
                'surface_pressure': 1010,
                'wind_speed_10m': 5,
                'wind_direction_10m': 180,
                'soil_temperature_0_to_7cm': 35,
                'soil_moisture_0_to_7cm': 0.1,
                'sunshine_duration': 3600,
                'pm10': 20,
                'pm2_5': 10,
                'carbon_dioxide': 450,
                'carbon_monoxide': 130,
                'nitrogen_dioxide': 10,
                'sulphur_dioxide': 8,
                'ozone': 100,
                'aerosol_optical_depth': 0.3,
                'methane': 1600,
                'uv_index': 10,
                'uv_index_clear_sky': 11,
                'dust': 2,
                'grass': 8,
                'tree': 5,
                'weed': 7
            }]),
            'expected_group': 2  # Skin Allergies due to extreme heat and UV
        })
        
        # Case 2: High pollution
        edge_cases.append({
            'name': 'High Air Pollution',
            'data': pd.DataFrame([{
                'temperature_2m': 25,
                'relative_humidity_2m': 60,
                'precipitation': 0,
                'snowfall': 0,
                'rain': 0,
                'cloud_cover': 20,
                'surface_pressure': 1010,
                'wind_speed_10m': 3,
                'wind_direction_10m': 90,
                'soil_temperature_0_to_7cm': 22,
                'soil_moisture_0_to_7cm': 0.3,
                'sunshine_duration': 1800,
                'pm10': 80,
                'pm2_5': 50,
                'carbon_dioxide': 500,
                'carbon_monoxide': 200,
                'nitrogen_dioxide': 60,
                'sulphur_dioxide': 40,
                'ozone': 150,
                'aerosol_optical_depth': 0.7,
                'methane': 1800,
                'uv_index': 5,
                'uv_index_clear_sky': 6,
                'dust': 5,
                'grass': 2,
                'tree': 1,
                'weed': 2
            }]),
            'expected_group': 1  # Respiratory Allergies due to high pollution
        })
        
        # Case 3: Ideal conditions
        edge_cases.append({
            'name': 'Ideal Weather Conditions',
            'data': pd.DataFrame([{
                'temperature_2m': 22,
                'relative_humidity_2m': 50,
                'precipitation': 0,
                'snowfall': 0,
                'rain': 0,
                'cloud_cover': 10,
                'surface_pressure': 1013,
                'wind_speed_10m': 7,
                'wind_direction_10m': 180,
                'soil_temperature_0_to_7cm': 20,
                'soil_moisture_0_to_7cm': 0.25,
                'sunshine_duration': 2400,
                'pm10': 10,
                'pm2_5': 5,
                'carbon_dioxide': 410,
                'carbon_monoxide': 100,
                'nitrogen_dioxide': 5,
                'sulphur_dioxide': 3,
                'ozone': 50,
                'aerosol_optical_depth': 0.1,
                'methane': 1500,
                'uv_index': 4,
                'uv_index_clear_sky': 5,
                'dust': 0,
                'grass': 1,
                'tree': 0,
                'weed': 0
            }]),
            'expected_group': 3  # Food Allergies, as environmental triggers are minimal
        })
        
        # Case 4: Ideal for insects
        edge_cases.append({
            'name': 'Ideal Insect Conditions',
            'data': pd.DataFrame([{
                'temperature_2m': 30,
                'relative_humidity_2m': 80,
                'precipitation': 5,
                'snowfall': 0,
                'rain': 5,
                'cloud_cover': 40,
                'surface_pressure': 1005,
                'wind_speed_10m': 2,
                'wind_direction_10m': 270,
                'soil_temperature_0_to_7cm': 28,
                'soil_moisture_0_to_7cm': 0.7,
                'sunshine_duration': 1200,
                'pm10': 15,
                'pm2_5': 8,
                'carbon_dioxide': 420,
                'carbon_monoxide': 110,
                'nitrogen_dioxide': 8,
                'sulphur_dioxide': 5,
                'ozone': 60,
                'aerosol_optical_depth': 0.2,
                'methane': 1550,
                'uv_index': 6,
                'uv_index_clear_sky': 7,
                'dust': 1,
                'grass': 3,
                'tree': 1,
                'weed': 2
            }]),
            'expected_group': 4  # Insect Allergies due to warm, humid conditions
        })
        
        # Test each edge case
        results = []
        for case in edge_cases:
            predictions, probabilities = self.model.predict(case['data'])
            pred_group = predictions[0]
            pred_prob = probabilities[0][pred_group-1]
            
            results.append({
                'name': case['name'],
                'expected_group': case['expected_group'],
                'predicted_group': int(pred_group),
                'confidence': float(pred_prob),
                'success': pred_group == case['expected_group']
            })
            
            print(f"Edge Case: {case['name']}")
            print(f"  Expected Group: {case['expected_group']}")
            print(f"  Predicted Group: {pred_group} with confidence {pred_prob:.4f}")
            print(f"  Success: {'Yes' if pred_group == case['expected_group'] else 'No'}")
            print()
        
        # Calculate overall success rate
        success_rate = sum(1 for r in results if r['success']) / len(results)
        print(f"Edge Case Success Rate: {success_rate:.2%}")
        
        return {
            'edge_case_results': results,
            'success_rate': success_rate
        }

# Main execution
if __name__ == "__main__":
    # Create tester
    tester = ModelTester()
    
    # Run general tests
    test_results = tester.run_tests()
    
    # Run edge case tests
    edge_case_results = tester.test_edge_cases()
