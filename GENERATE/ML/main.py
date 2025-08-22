import os
import sys
import argparse
import pandas as pd
import json
from datetime import datetime

# Add necessary paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.train_model import AllergyModel
from model.predict import AllergyPredictor
from test.test_model import ModelTester

def train_model(data_path, model_dir='model/saved_models'):
    """Train the allergy prediction model"""
    print(f"Training model with data from {data_path}")
    
    # Load data
    data = pd.read_csv(data_path)
    print(f"Loaded data with shape: {data.shape}")
    
    # Create and train model
    model = AllergyModel(model_dir=model_dir)
    model.train(data)
    
    print(f"Model training complete. Models saved to {model_dir}")
    return model

def test_model(test_data_path=None, model_dir='model/saved_models', output_dir='test/results'):
    """Test the trained model"""
    print("Testing model...")
    
    # Create tester
    tester = ModelTester(model_dir=model_dir, test_data_path=test_data_path)
    
    # Run tests
    test_results = tester.run_tests(output_dir=output_dir)
    edge_case_results = tester.test_edge_cases(output_dir=output_dir)
    
    # Save test results
    results = {
        'general_tests': test_results,
        'edge_case_tests': edge_case_results,
        'timestamp': datetime.now().isoformat()
    }
    
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'test_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Test results saved to {os.path.join(output_dir, 'test_results.json')}")
    return results

def predict(weather_file, pollen_file=None, model_dir='model/saved_models', output_file=None):
    """Make predictions with the trained model"""
    print("Making prediction...")
    
    # Load data
    with open(weather_file, 'r') as f:
        weather_data = json.load(f)
    
    pollen_data = None
    if pollen_file:
        with open(pollen_file, 'r') as f:
            pollen_data = json.load(f)
    
    # Create predictor
    predictor = AllergyPredictor(model_dir=model_dir)
    
    # Make prediction
    result = predictor.predict(weather_data, pollen_data)
    
    # Display results
    print("\nAllergy Prediction Results:")
    print(f"Group: {result['allergy_group']} - {result['group_name']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Risk Level: {result['risk_level']}")
    
    print("\nRecommendations:")
    for i, rec in enumerate(result['recommendations']):
        print(f"{i+1}. {rec}")
    
    print("\nContributing Factors:")
    for factor in result['contributing_factors']:
        print(f"- {factor['factor']}: {factor['value']} (Impact: {factor['impact']})")
    
    # Save result if output file specified
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nResults saved to {output_file}")
    
    return result

def main():
    parser = argparse.ArgumentParser(description='Allergy Prediction Model')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train the model')
    train_parser.add_argument('--data', required=True, help='Path to training data CSV')
    train_parser.add_argument('--model-dir', default='model/saved_models', help='Directory to save models')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test the model')
    test_parser.add_argument('--test-data', help='Path to test data CSV (optional)')
    test_parser.add_argument('--model-dir', default='model/saved_models', help='Directory with saved models')
    test_parser.add_argument('--output-dir', default='test/results', help='Directory to save test results')
    
    # Predict command
    predict_parser = subparsers.add_parser('predict', help='Make a prediction')
    predict_parser.add_argument('--weather', required=True, help='Path to weather data JSON file')
    predict_parser.add_argument('--pollen', help='Path to pollen data JSON file (optional)')
    predict_parser.add_argument('--model-dir', default='model/saved_models', help='Directory with saved models')
    predict_parser.add_argument('--output', help='Path to save prediction results JSON (optional)')
    
    args = parser.parse_args()
    
    if args.command == 'train':
        train_model(args.data, args.model_dir)
    elif args.command == 'test':
        test_model(args.test_data, args.model_dir, args.output_dir)
    elif args.command == 'predict':
        predict(args.weather, args.pollen, args.model_dir, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
