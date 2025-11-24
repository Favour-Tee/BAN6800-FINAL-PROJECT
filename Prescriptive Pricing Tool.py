import pandas as pd
import numpy as np
import json
import xgboost as xgb
import joblib
from datetime import datetime

class BoschPricingOptimizer:
    """
    Prescriptive Pricing Tool for Bosch FMCG Products
    """
    
    def __init__(self, model_path, scaler_path, category_encoder_path, location_encoder_path):
        self.model = xgb.XGBRegressor()
        self.model.load_model(model_path)
        self.scaler = joblib.load(scaler_path)
        self.le_category = joblib.load(category_encoder_path)
        self.le_location = joblib.load(location_encoder_path)
        
        # Feature list (should match training)
        self.features = [
            'Price', 'Promotion', 'Supplier_Cost', 'Stock_Level', 'Replenishment_Lead_Time',
            'Month', 'Quarter', 'DayOfWeek', 'WeekOfYear', 'Is_Weekend', 'Year',
            'Profit_Margin', 'Margin_Percentage', 'Stock_Out_Risk', 'Avg_Category_Price', 'Price_Ratio_To_Avg',
            'Product_Category_Encoded', 'Store_Location_Encoded'
        ]
        
        # Pre-calculated elasticities (from model training)
        self.elasticities = {
            'Snacks': -1.4,
            'Beverages': -1.3,
            'Dairy': -0.9,
            'Household': -0.7,
            'Personal Care': -0.6
        }
    
    def prepare_features(self, product_data):
        """
        Prepare features for model prediction
        """
        # Create feature vector
        feature_vector = []
        
        # Add basic features
        for feature in self.features:
            if feature in product_data:
                feature_vector.append(product_data[feature])
            else:
                # Handle missing features with default values
                feature_vector.append(0.0)
        
        return np.array(feature_vector).reshape(1, -1)
    
    def forecast_demand(self, product_data):
        """
        Forecast demand for given product conditions
        """
        features = self.prepare_features(product_data)
        prediction = self.model.predict(features)[0]
        return max(0, prediction)  # Ensure non-negative
    
    def optimize_price(self, product_data, current_price, category, min_price=None, max_price=None):
        """
        Find optimal price that maximizes revenue
        """
        if min_price is None:
            min_price = current_price * 0.7  # 30% lower bound
        if max_price is None:
            max_price = current_price * 1.3  # 30% upper bound
        
        # Get base forecast at current price
        product_data['Price'] = current_price
        base_demand = self.forecast_demand(product_data)
        base_revenue = current_price * base_demand
        
        # Test price points
        price_points = np.linspace(min_price, max_price, 50)
        best_price = current_price
        best_revenue = base_revenue
        results = []
        
        for test_price in price_points:
            # Adjust demand based on price elasticity
            elasticity = self.elasticities.get(category, -1.0)
            price_change_pct = (test_price - current_price) / current_price
            demand_change_pct = elasticity * price_change_pct
            
            adjusted_demand = base_demand * (1 + demand_change_pct)
            test_revenue = test_price * adjusted_demand
            
            results.append({
                'price': test_price,
                'demand': adjusted_demand,
                'revenue': test_revenue,
                'price_change_pct': price_change_pct
            })
            
            if test_revenue > best_revenue:
                best_price = test_price
                best_revenue = test_revenue
        
        return {
            'current_price': current_price,
            'optimal_price': best_price,
            'current_revenue': base_revenue,
            'optimal_revenue': best_revenue,
            'revenue_increase_pct': (best_revenue - base_revenue) / base_revenue * 100,
            'price_change_pct': (best_price - current_price) / current_price * 100,
            'simulation_results': results
        }
    
    def generate_recommendations(self, products_data):
        """
        Generate pricing recommendations for multiple products
        """
        recommendations = []
        
        for product in products_data:
            try:
                result = self.optimize_price(
                    product_data=product,
                    current_price=product['Price'],
                    category=product['Product_Category']
                )
                
                recommendation = {
                    'Product_Category': product['Product_Category'],
                    'Store_Location': product['Store_Location'],
                    'Current_Price': result['current_price'],
                    'Recommended_Price': result['optimal_price'],
                    'Price_Change_Pct': result['price_change_pct'],
                    'Expected_Revenue_Increase_Pct': result['revenue_increase_pct'],
                    'Recommendation': 'INCREASE' if result['price_change_pct'] > 0 else 'DECREASE'
                }
                
                recommendations.append(recommendation)
                
            except Exception as e:
                print(f"Error processing {product['Product_Category']}: {str(e)}")
                continue
        
        return pd.DataFrame(recommendations)

# Example usage
if __name__ == "__main__":
    # Initialize the optimizer
    optimizer = BoschPricingOptimizer(
        model_path='best_xgboost_model.json',
        scaler_path='scaler.pkl',
        category_encoder_path='label_encoder_category.pkl',
        location_encoder_path='label_encoder_location.pkl'
    )
    
    # Sample product data for testing
    sample_products = [
        {
            'Product_Category': 'Snacks',
            'Store_Location': 'Urban',
            'Price': 12.50,
            'Promotion': 0,
            'Supplier_Cost': 8.00,
            'Stock_Level': 200,
            'Replenishment_Lead_Time': 3,
            'Month': 6,
            'Quarter': 2,
            'DayOfWeek': 2,
            'WeekOfYear': 25,
            'Is_Weekend': 0,
            'Year': 2024,
            'Avg_Category_Price': 12.30
        },
        {
            'Product_Category': 'Personal Care',
            'Store_Location': 'Urban',
            'Price': 15.00,
            'Promotion': 0,
            'Supplier_Cost': 9.00,
            'Stock_Level': 150,
            'Replenishment_Lead_Time': 5,
            'Month': 6,
            'Quarter': 2,
            'DayOfWeek': 2,
            'WeekOfYear': 25,
            'Is_Weekend': 0,
            'Year': 2024,
            'Avg_Category_Price': 14.80
        }
    ]
    
    # Add calculated features
    for product in sample_products:
        product['Profit_Margin'] = product['Price'] - product['Supplier_Cost']
        product['Margin_Percentage'] = (product['Profit_Margin'] / product['Price']) * 100
        product['Stock_Out_Risk'] = 1 if product['Stock_Level'] < 100 else 0
        product['Price_Ratio_To_Avg'] = product['Price'] / product['Avg_Category_Price']
        product['Product_Category_Encoded'] = optimizer.le_category.transform([product['Product_Category']])[0]
        product['Store_Location_Encoded'] = optimizer.le_location.transform([product['Store_Location']])[0]
    
    # Generate recommendations
    recommendations = optimizer.generate_recommendations(sample_products)
    
    print("PRICING OPTIMIZATION RECOMMENDATIONS")
    print("="*60)
    for _, row in recommendations.iterrows():
        print(f"\nProduct: {row['Product_Category']} ({row['Store_Location']})")
        print(f"Current Price: ${row['Current_Price']:.2f}")
        print(f"Recommended Price: ${row['Recommended_Price']:.2f}")
        print(f"Price Change: {row['Price_Change_Pct']:+.1f}%")
        print(f"Expected Revenue Increase: {row['Expected_Revenue_Increase_Pct']:+.1f}%")
        print(f"Action: {row['Recommendation']} price")
    
    # Save recommendations
    recommendations.to_csv('pricing_recommendations.csv', index=False)
    print(f"\nRecommendations saved to 'pricing_recommendations.csv'")