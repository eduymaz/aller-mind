# Allermind - Machine Learning Model for Allergy Prediction

This directory contains the machine learning component of the Allermind application, which predicts allergy group membership based on environmental data and provides personalized recommendations.

## Allergy Groups

The model classifies individuals into five distinct groups:

1. **Severe Allergic Asthma**: Individuals with diagnosed severe allergic asthma
2. **Mild to Moderate Allergic**: Individuals with diagnosed mild to moderate allergies
3. **Possible Allergic/High Risk**: Individuals with high risk for allergies but not yet fully symptomatic
4. **Not Yet Diagnosed**: General population without specific allergy diagnosis
5. **Vulnerable Population**: Babies, children, elderly, and chronic patients

## Directory Structure

```
ML/
├── model/                  # Core model functionality
│   ├── train_model.py      # Model training
│   ├── predict.py          # Making predictions with trained models
│   └── saved_models/       # Saved trained models
├── test/                   # Testing framework
│   ├── test_model.py       # Test runner
│   ├── generate_test_data.py # Generate synthetic test data
│   └── results/            # Test results
└── main.py                 # Command line interface
```

## Features

- **Multi-class Classification**: Predicts which of 4 allergy groups a user belongs to:
  1. Respiratory Allergies (sensitive to air pollution and pollen)
  2. Skin Allergies (sensitive to UV, temperature, humidity)
  3. Food Allergies (less affected by environmental factors)
  4. Insect Allergies (affected by temperature, humidity, soil conditions)

- **Continuous Learning**: Model can be retrained with new data to improve predictions

- **Personalized Recommendations**: Provides actionable advice based on current environmental conditions and predicted allergy group

- **Confidence Scoring**: Reports confidence level in predictions

- **Risk Assessment**: Evaluates current environmental risk level for each allergy group

## Getting Started

### Prerequisites

- Python 3.8+
- Required packages: pandas, numpy, scikit-learn, matplotlib, joblib

### Installation

```bash
pip install -r requirements.txt
```

### Training the Model

```bash
python main.py train --data ../../synthetic_combined_data.csv
```

### Testing the Model

```bash
python main.py test
```

### Making Predictions

```bash
python main.py predict --weather path/to/weather.json --pollen path/to/pollen.json
```

## Usage Examples

### Training with Custom Data

```bash
python main.py train --data my_data.csv --model-dir my_models
```

### Testing with Custom Test Data

```bash
python main.py test --test-data my_test_data.csv --model-dir my_models --output-dir my_results
```

### Making a Prediction and Saving Result

```bash
python main.py predict --weather current_weather.json --pollen current_pollen.json --output prediction_result.json
```

## Model Performance

The model has been trained and tested on synthetic data with the following results:

- Accuracy: ~85% (varies with training data)
- Performance on edge cases: ~80% accuracy

## How It Works

1. **Data Ingestion**: Environmental data from weather and pollen APIs is processed
2. **Feature Selection**: Key features are selected based on their relevance to allergy responses
3. **Classification**: Ensemble models (Random Forest, Gradient Boosting) classify users into allergy groups
4. **Recommendation Engine**: Based on the classification and current conditions, personalized recommendations are generated
5. **Continuous Improvement**: New data can be used to retrain and improve the model

## Contributing

If you'd like to contribute, please follow these guidelines:
- Add tests for new functionality
- Document your code
- Follow existing code style

## License

This project is licensed under the MIT License - see the LICENSE file for details.