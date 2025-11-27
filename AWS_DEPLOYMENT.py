"""
Bosch FMCG Pricing Model - Mock API Server
Simulates AWS API Gateway endpoint locally for testing
"""

from flask import Flask, request, jsonify
import json
from datetime import datetime
import random

app = Flask(__name__)

# Simulated model prediction function
def predict_demand(input_data):
    """
    Simulate demand prediction based on input features
    """
    try:
        # Extract features
        price = float(input_data.get('price', 10))
        promotion = int(input_data.get('promotion', 0))
        competitor_price = float(input_data.get('competitor_price', 10))
        day_of_week = int(input_data.get('day_of_week', 1))
        month = int(input_data.get('month', 1))
        inventory_level = int(input_data.get('inventory_level', 500))
        
        # Simple demand prediction logic
        base_demand = 1000
        
        # Price elasticity
        price_factor = max(0, 1 - (price - 10) * 0.08)
        
        # Promotion effect
        promotion_boost = 1.25 if promotion == 1 else 1.0
        
        # Competitor pricing effect
        if competitor_price > price:
            competition_boost = 1.15
        elif competitor_price < price:
            competition_boost = 0.90
        else:
            competition_boost = 1.0
        
        # Day of week effect (weekend boost)
        day_factor = 1.1 if day_of_week in [6, 7] else 1.0
        
        # Seasonal effect
        seasonal_factor = 1.0 + 0.15 * abs(6 - month) / 6
        
        # Inventory effect
        inventory_factor = min(1.0, inventory_level / 500)
        
        # Calculate prediction
        prediction = (base_demand * price_factor * promotion_boost * 
                     competition_boost * day_factor * seasonal_factor * 
                     inventory_factor)
        
        # Add small random variation for realism
        prediction *= (1 + random.uniform(-0.05, 0.05))
        
        return max(0, round(prediction, 2))
        
    except Exception as e:
        raise ValueError(f"Prediction error: {str(e)}")

@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        'service': 'Bosch FMCG Pricing Optimization API',
        'version': '1.0',
        'status': 'active',
        'endpoints': {
            'predict': '/predict',
            'health': '/health',
            'info': '/info'
        },
        'documentation': 'https://api-docs.bosch-pricing.com'
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'bosch-pricing-predictor',
        'region': 'us-east-1'
    })

@app.route('/info')
def info():
    """API information endpoint"""
    return jsonify({
        'model_name': 'Bosch FMCG Demand Prediction Model',
        'model_version': '1.0',
        'framework': 'XGBoost',
        'features': [
            'price',
            'promotion',
            'competitor_price',
            'day_of_week',
            'month',
            'inventory_level'
        ],
        'description': 'Predicts product demand based on pricing and market conditions',
        'last_updated': '2024-11-27'
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint
    
    Example request:
    {
        "price": 10.50,
        "promotion": 1,
        "competitor_price": 11.00,
        "day_of_week": 3,
        "month": 6,
        "inventory_level": 500
    }
    """
    try:
        # Parse input
        if request.is_json:
            input_data = request.get_json()
        else:
            return jsonify({
                'error': 'Request must be JSON',
                'status': 'error'
            }), 400
        
        # Validate required fields
        required_fields = ['price', 'promotion', 'competitor_price', 
                          'day_of_week', 'month']
        missing_fields = [field for field in required_fields 
                         if field not in input_data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'status': 'error',
                'required_fields': required_fields
            }), 400
        
        # Make prediction
        prediction = predict_demand(input_data)
        
        # Calculate confidence interval (simulated)
        confidence_lower = round(prediction * 0.85, 2)
        confidence_upper = round(prediction * 1.15, 2)
        
        # Return response
        return jsonify({
            'predicted_demand': prediction,
            'confidence_interval': {
                'lower': confidence_lower,
                'upper': confidence_upper,
                'confidence_level': 0.95
            },
            'input_features': input_data,
            'model_version': '1.0',
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e),
            'status': 'error'
        }), 500

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """
    Batch prediction endpoint for multiple scenarios
    
    Example request:
    {
        "scenarios": [
            {"price": 10.0, "promotion": 1, ...},
            {"price": 11.0, "promotion": 0, ...}
        ]
    }
    """
    try:
        if not request.is_json:
            return jsonify({
                'error': 'Request must be JSON',
                'status': 'error'
            }), 400
        
        data = request.get_json()
        scenarios = data.get('scenarios', [])
        
        if not scenarios:
            return jsonify({
                'error': 'No scenarios provided',
                'status': 'error'
            }), 400
        
        # Make predictions for all scenarios
        predictions = []
        for i, scenario in enumerate(scenarios):
            try:
                prediction = predict_demand(scenario)
                predictions.append({
                    'scenario_id': i + 1,
                    'predicted_demand': prediction,
                    'input': scenario,
                    'status': 'success'
                })
            except Exception as e:
                predictions.append({
                    'scenario_id': i + 1,
                    'error': str(e),
                    'input': scenario,
                    'status': 'error'
                })
        
        return jsonify({
            'predictions': predictions,
            'total_scenarios': len(scenarios),
            'successful': sum(1 for p in predictions if p['status'] == 'success'),
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e),
            'status': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'available_endpoints': ['/predict', '/health', '/info', '/batch-predict']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    print("="*60)
    print("  Bosch FMCG Pricing API Server")
    print("="*60)
    print("\nServer starting...")
    print("API will be available at: http://127.0.0.1:5000")
    print("\nEndpoints:")
    print("  GET  /              - API information")
    print("  GET  /health        - Health check")
    print("  GET  /info          - Model information")
    print("  POST /predict       - Single prediction")
    print("  POST /batch-predict - Batch predictions")
    print("\nExample usage:")
    print('  curl -X POST http://127.0.0.1:5000/predict \\')
    print('       -H "Content-Type: application/json" \\')
    print('       -d \'{"price": 10.5, "promotion": 1, "competitor_price": 11.0,')
    print('            "day_of_week": 3, "month": 6, "inventory_level": 500}\'')
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Run server
    app.run(debug=True, host='0.0.0.0', port=5000)