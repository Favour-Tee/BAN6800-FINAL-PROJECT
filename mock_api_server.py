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
    """Serve the web interface"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bosch FMCG Pricing API - Interactive Tester</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            
            .content {
                padding: 30px;
            }
            
            .url-section {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                border: 2px solid #dee2e6;
            }
            
            .url-section label {
                display: block;
                font-weight: 600;
                margin-bottom: 10px;
                color: #333;
            }
            
            .url-section input {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 1em;
                transition: border-color 0.3s;
            }
            
            .url-section input:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .url-section small {
                display: block;
                margin-top: 8px;
                color: #666;
            }
            
            .test-section {
                background: white;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
            }
            
            .test-section h3 {
                color: #333;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 1.3em;
            }
            
            .input-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }
            
            .input-group {
                display: flex;
                flex-direction: column;
            }
            
            .input-group label {
                font-weight: 600;
                margin-bottom: 5px;
                color: #555;
                font-size: 0.9em;
            }
            
            .input-group input,
            .input-group select {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 1em;
                transition: border-color 0.3s;
            }
            
            .input-group input:focus,
            .input-group select:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .button-group {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            
            button {
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .btn-primary:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .btn-secondary {
                background: #6c757d;
                color: white;
            }
            
            .btn-secondary:hover:not(:disabled) {
                background: #5a6268;
            }
            
            .btn-success {
                background: #28a745;
                color: white;
            }
            
            .btn-success:hover:not(:disabled) {
                background: #218838;
            }
            
            .btn-info {
                background: #17a2b8;
                color: white;
            }
            
            .btn-info:hover:not(:disabled) {
                background: #138496;
            }
            
            .result-box {
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 15px;
                border-radius: 6px;
                margin-top: 15px;
                display: none;
            }
            
            .result-box.show {
                display: block;
                animation: slideIn 0.3s ease-out;
            }
            
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(-10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .result-box h4 {
                color: #333;
                margin-bottom: 10px;
            }
            
            .result-box pre {
                background: white;
                padding: 15px;
                border-radius: 6px;
                overflow-x: auto;
                font-size: 0.9em;
                border: 1px solid #dee2e6;
                max-height: 400px;
                overflow-y: auto;
            }
            
            .status-badge {
                display: inline-block;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: 600;
                margin-left: 10px;
            }
            
            .status-success {
                background: #d4edda;
                color: #155724;
            }
            
            .status-error {
                background: #f8d7da;
                color: #721c24;
            }
            
            .status-loading {
                background: #fff3cd;
                color: #856404;
            }
            
            .prediction-result {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 10px;
                margin-top: 15px;
                display: none;
            }
            
            .prediction-result.show {
                display: block;
                animation: slideIn 0.3s ease-out;
            }
            
            .prediction-result h4 {
                margin-bottom: 15px;
                font-size: 1.3em;
            }
            
            .prediction-value {
                font-size: 3em;
                font-weight: bold;
                margin: 15px 0;
            }
            
            .confidence-range {
                font-size: 1em;
                opacity: 0.9;
                margin-top: 10px;
            }
            
            .quick-tests {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            
            .quick-test-card {
                background: white;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
                cursor: pointer;
                transition: all 0.3s;
                text-align: center;
            }
            
            .quick-test-card:hover {
                border-color: #667eea;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .quick-test-card .icon {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .quick-test-card h4 {
                color: #333;
                margin-bottom: 10px;
                font-size: 1.1em;
            }
            
            .quick-test-card p {
                color: #666;
                font-size: 0.9em;
            }
            
            .loader {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                animation: spin 1s linear infinite;
                display: inline-block;
                margin-left: 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .footer {
                text-align: center;
                padding: 20px;
                background: #f8f9fa;
                color: #666;
                font-size: 0.9em;
            }
            
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 1.8em;
                }
                
                .input-grid {
                    grid-template-columns: 1fr;
                }
                
                .prediction-value {
                    font-size: 2em;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 Bosch FMCG Pricing API Tester</h1>
                <p>Interactive testing interface for demand prediction model</p>
            </div>
            
            <div class="content">
                <!-- API URL Configuration -->
                <div class="url-section">
                    <label for="apiUrl">🔗 API Base URL</label>
                    <input 
                        type="text" 
                        id="apiUrl" 
                        placeholder="Enter your API URL (e.g., https://your-app.onrender.com)"
                        value=""
                    >
                    <small>Enter your Render deployment URL or use http://127.0.0.1:5000 for local testing</small>
                </div>
                
                <!-- Quick Health Check -->
                <div class="test-section">
                    <h3>🏥 API Status & Information</h3>
                    <p style="color: #666; margin-bottom: 15px;">Verify your API is running and get basic information</p>
                    <div class="button-group">
                        <button class="btn-success" onclick="testHealth()">
                            Check Health
                        </button>
                        <button class="btn-info" onclick="testInfo()">
                            API Info
                        </button>
                        <button class="btn-info" onclick="testModelInfo()">
                            Model Details
                        </button>
                    </div>
                    <div id="quickTestResult" class="result-box"></div>
                </div>
                
                <!-- Single Prediction -->
                <div class="test-section">
                    <h3>📊 Demand Prediction Calculator</h3>
                    <p style="color: #666; margin-bottom: 15px;">Enter product and market conditions to predict demand</p>
                    
                    <div class="input-grid">
                        <div class="input-group">
                            <label for="price">💰 Price ($)</label>
                            <input type="number" id="price" value="10.50" step="0.1" min="0">
                        </div>
                        <div class="input-group">
                            <label for="promotion">🎁 Promotion Active</label>
                            <select id="promotion">
                                <option value="0">No Promotion</option>
                                <option value="1">Promotion Active</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label for="competitorPrice">🏪 Competitor Price ($)</label>
                            <input type="number" id="competitorPrice" value="11.00" step="0.1" min="0">
                        </div>
                        <div class="input-group">
                            <label for="dayOfWeek">📅 Day of Week</label>
                            <select id="dayOfWeek">
                                <option value="1">Monday</option>
                                <option value="2">Tuesday</option>
                                <option value="3" selected>Wednesday</option>
                                <option value="4">Thursday</option>
                                <option value="5">Friday</option>
                                <option value="6">Saturday</option>
                                <option value="7">Sunday</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label for="month">📆 Month</label>
                            <select id="month">
                                <option value="1">January</option>
                                <option value="2">February</option>
                                <option value="3">March</option>
                                <option value="4">April</option>
                                <option value="5">May</option>
                                <option value="6" selected>June</option>
                                <option value="7">July</option>
                                <option value="8">August</option>
                                <option value="9">September</option>
                                <option value="10">October</option>
                                <option value="11">November</option>
                                <option value="12">December</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label for="inventoryLevel">📦 Inventory Level</label>
                            <input type="number" id="inventoryLevel" value="500" min="0">
                        </div>
                    </div>
                    <div class="button-group">
                        <button class="btn-primary" onclick="predictDemand()">
                            🚀 Predict Demand
                        </button>
                        <button class="btn-secondary" onclick="resetForm()">
                            🔄 Reset Form
                        </button>
                    </div>
                    <div id="predictionResult" class="prediction-result"></div>
                    <div id="predictionDetails" class="result-box"></div>
                </div>
                
                <!-- Quick Test Scenarios -->
                <div class="test-section">
                    <h3>⚡ Quick Test Scenarios</h3>
                    <p style="color: #666; margin-bottom: 15px;">Click any scenario to auto-fill the form and test</p>
                    <div class="quick-tests">
                        <div class="quick-test-card" onclick="loadScenario('standard')">
                            <div class="icon">📊</div>
                            <h4>Standard Pricing</h4>
                            <p>Normal pricing without promotion</p>
                        </div>
                        <div class="quick-test-card" onclick="loadScenario('promotion')">
                            <div class="icon">🎉</div>
                            <h4>Promotion Active</h4>
                            <p>Promotional pricing + weekend boost</p>
                        </div>
                        <div class="quick-test-card" onclick="loadScenario('high')">
                            <div class="icon">💰</div>
                            <h4>Premium Pricing</h4>
                            <p>High price strategy</p>
                        </div>
                        <div class="quick-test-card" onclick="loadScenario('competitive')">
                            <div class="icon">⚡</div>
                            <h4>Competitive Edge</h4>
                            <p>Aggressive pricing vs competitors</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>Bosch FMCG Pricing Optimization API | Developed for BAN6800 Final Project</p>
                <p style="margin-top: 5px; font-size: 0.85em;">© 2024 All Rights Reserved</p>
            </div>
        </div>

        <script>
            const scenarios = {
                standard: {
                    price: 10.50,
                    promotion: 0,
                    competitorPrice: 11.00,
                    dayOfWeek: 3,
                    month: 6,
                    inventoryLevel: 500
                },
                promotion: {
                    price: 9.00,
                    promotion: 1,
                    competitorPrice: 10.50,
                    dayOfWeek: 6,
                    month: 12,
                    inventoryLevel: 800
                },
                high: {
                    price: 15.00,
                    promotion: 0,
                    competitorPrice: 12.00,
                    dayOfWeek: 2,
                    month: 3,
                    inventoryLevel: 300
                },
                competitive: {
                    price: 8.50,
                    promotion: 1,
                    competitorPrice: 11.00,
                    dayOfWeek: 7,
                    month: 6,
                    inventoryLevel: 1000
                }
            };

            function getApiUrl() {
                const url = document.getElementById('apiUrl').value.trim();
                if (!url) {
                    alert('Please enter your API URL first!');
                    document.getElementById('apiUrl').focus();
                    return null;
                }
                return url;
            }

            function showLoading(elementId) {
                const element = document.getElementById(elementId);
                element.innerHTML = '<div class="loader"></div> Loading...';
                element.classList.add('show');
            }

            function showResult(elementId, html) {
                const element = document.getElementById(elementId);
                element.innerHTML = html;
                element.classList.add('show');
            }

            async function testHealth() {
                const apiUrl = getApiUrl();
                if (!apiUrl) return;
                
                showLoading('quickTestResult');
                try {
                    const response = await fetch(`${apiUrl}/health`);
                    const data = await response.json();
                    
                    const html = `
                        <h4>Health Check <span class="status-badge status-success">✓ HEALTHY</span></h4>
                        <pre>${JSON.stringify(data, null, 2)}</pre>
                    `;
                    showResult('quickTestResult', html);
                } catch (error) {
                    const html = `
                        <h4>Health Check <span class="status-badge status-error">✗ ERROR</span></h4>
                        <p style="color: #721c24; margin-top: 10px;"><strong>Error:</strong> ${error.message}</p>
                        <p style="color: #666; margin-top: 10px;">Make sure your API URL is correct and the service is running.</p>
                    `;
                    showResult('quickTestResult', html);
                }
            }

            async function testInfo() {
                const apiUrl = getApiUrl();
                if (!apiUrl) return;
                
                showLoading('quickTestResult');
                try {
                    const response = await fetch(`${apiUrl}/`);
                    const data = await response.json();
                    
                    const html = `
                        <h4>API Information <span class="status-badge status-success">✓ SUCCESS</span></h4>
                        <pre>${JSON.stringify(data, null, 2)}</pre>
                    `;
                    showResult('quickTestResult', html);
                } catch (error) {
                    const html = `
                        <h4>API Information <span class="status-badge status-error">✗ ERROR</span></h4>
                        <p style="color: #721c24; margin-top: 10px;"><strong>Error:</strong> ${error.message}</p>
                    `;
                    showResult('quickTestResult', html);
                }
            }

            async function testModelInfo() {
                const apiUrl = getApiUrl();
                if (!apiUrl) return;
                
                showLoading('quickTestResult');
                try {
                    const response = await fetch(`${apiUrl}/info`);
                    const data = await response.json();
                    
                    const html = `
                        <h4>Model Information <span class="status-badge status-success">✓ SUCCESS</span></h4>
                        <pre>${JSON.stringify(data, null, 2)}</pre>
                    `;
                    showResult('quickTestResult', html);
                } catch (error) {
                    const html = `
                        <h4>Model Information <span class="status-badge status-error">✗ ERROR</span></h4>
                        <p style="color: #721c24; margin-top: 10px;"><strong>Error:</strong> ${error.message}</p>
                    `;
                    showResult('quickTestResult', html);
                }
            }

            async function predictDemand() {
                const apiUrl = getApiUrl();
                if (!apiUrl) return;
                
                const predictionData = {
                    price: parseFloat(document.getElementById('price').value),
                    promotion: parseInt(document.getElementById('promotion').value),
                    competitor_price: parseFloat(document.getElementById('competitorPrice').value),
                    day_of_week: parseInt(document.getElementById('dayOfWeek').value),
                    month: parseInt(document.getElementById('month').value),
                    inventory_level: parseInt(document.getElementById('inventoryLevel').value)
                };

                document.getElementById('predictionResult').innerHTML = '<div class="loader"></div> Calculating demand prediction...';
                document.getElementById('predictionResult').classList.add('show');
                
                try {
                    const response = await fetch(`${apiUrl}/predict`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(predictionData)
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        const resultHtml = `
                            <h4>🎯 Predicted Demand</h4>
                            <div class="prediction-value">${data.predicted_demand.toFixed(2)} units</div>
                            <div class="confidence-range">
                                <strong>95% Confidence Interval:</strong><br>
                                ${data.confidence_interval.lower} - ${data.confidence_interval.upper} units
                            </div>
                        `;
                        document.getElementById('predictionResult').innerHTML = resultHtml;
                        
                        const detailsHtml = `
                            <h4>Full Response <span class="status-badge status-success">✓ SUCCESS</span></h4>
                            <pre>${JSON.stringify(data, null, 2)}</pre>
                        `;
                        showResult('predictionDetails', detailsHtml);
                    } else {
                        const errorHtml = `
                            <h4 style="color: white;">Prediction Failed</h4>
                            <p style="margin-top: 10px;">${data.error || 'Unknown error occurred'}</p>
                        `;
                        document.getElementById('predictionResult').innerHTML = errorHtml;
                        document.getElementById('predictionResult').style.background = 'linear-gradient(135deg, #f85032 0%, #e73827 100%)';
                    }
                } catch (error) {
                    const errorHtml = `
                        <h4 style="color: white;">Connection Failed</h4>
                        <p style="margin-top: 10px;"><strong>Error:</strong> ${error.message}</p>
                        <p style="margin-top: 10px;">Check if your API URL is correct and the service is running.</p>
                    `;
                    document.getElementById('predictionResult').innerHTML = errorHtml;
                    document.getElementById('predictionResult').style.background = 'linear-gradient(135deg, #f85032 0%, #e73827 100%)';
                }
            }

            function loadScenario(scenarioName) {
                const scenario = scenarios[scenarioName];
                document.getElementById('price').value = scenario.price;
                document.getElementById('promotion').value = scenario.promotion;
                document.getElementById('competitorPrice').value = scenario.competitorPrice;
                document.getElementById('dayOfWeek').value = scenario.dayOfWeek;
                document.getElementById('month').value = scenario.month;
                document.getElementById('inventoryLevel').value = scenario.inventoryLevel;
                
                // Scroll to prediction section smoothly
                document.querySelector('.test-section:nth-child(3)').scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                // Highlight the form briefly
                const section = document.querySelector('.test-section:nth-child(3)');
                section.style.border = '3px solid #667eea';
                setTimeout(() => {
                    section.style.border = '2px solid #e9ecef';
                }, 1000);
            }

            function resetForm() {
                loadScenario('standard');
                document.getElementById('predictionResult').classList.remove('show');
                document.getElementById('predictionDetails').classList.remove('show');
            }

            // Load saved API URL from localStorage if available
            window.addEventListener('DOMContentLoaded', () => {
                const currentUrl = window.location.origin;
                document.getElementById('apiUrl').value = currentUrl;
                localStorage.setItem('bosch_api_url', currentUrl);
                
                // Save URL to localStorage when changed
                document.getElementById('apiUrl').addEventListener('change', (e) => {
                    localStorage.setItem('bosch_api_url', e.target.value);
                });
            });
        </script>
    </body>
    </html>
    """

@app.route('/api')
def api_info():
    """API information endpoint"""
    return jsonify({
        'service': 'Bosch FMCG Pricing Optimization API',
        'version': '1.0',
        'status': 'active',
        'endpoints': {
            'predict': '/predict',
            'health': '/health',
            'info': '/info',
            'batch_predict': '/batch-predict'
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
    print("Web Interface: http://127.0.0.1:5000")
    print("API Endpoints:")
    print("  GET  /              - Web Interface")
    print("  GET  /api           - API information")
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