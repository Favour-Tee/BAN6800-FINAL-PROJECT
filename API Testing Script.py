"""
Bosch FMCG Pricing API - Testing Script
Comprehensive API testing with visual output
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any

class BoschAPITester:
    """Test suite for Bosch Pricing API"""
    
    def __init__(self, base_url: str):
        """
        Initialize the API tester
        
        Args:
            base_url: Base URL of the API (e.g., https://your-app.onrender.com)
        """
        self.base_url = base_url.rstrip('/')
        self.test_results = []
    
    def print_header(self, text: str):
        """Print formatted header"""
        print("\n" + "="*70)
        print(f"  {text}")
        print("="*70)
    
    def print_test(self, test_name: str):
        """Print test name"""
        print(f"\n[TEST] {test_name}")
        print("-" * 70)
    
    def print_result(self, success: bool, message: str):
        """Print test result"""
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {message}")
    
    def test_health_check(self) -> bool:
        """Test the health check endpoint"""
        self.print_test("Health Check - GET /health")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(json.dumps(data, indent=2))
                self.print_result(True, "Health check passed")
                return True
            else:
                self.print_result(False, f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_result(False, f"Error: {str(e)}")
            return False
    
    def test_api_info(self) -> bool:
        """Test the API information endpoint"""
        self.print_test("API Information - GET /")
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(json.dumps(data, indent=2))
                self.print_result(True, "API info retrieved successfully")
                return True
            else:
                self.print_result(False, f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_result(False, f"Error: {str(e)}")
            return False
    
    def test_model_info(self) -> bool:
        """Test the model information endpoint"""
        self.print_test("Model Information - GET /info")
        
        try:
            response = requests.get(f"{self.base_url}/info", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(json.dumps(data, indent=2))
                self.print_result(True, "Model info retrieved successfully")
                return True
            else:
                self.print_result(False, f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_result(False, f"Error: {str(e)}")
            return False
    
    def test_single_prediction(self, test_data: Dict[str, Any], test_name: str) -> bool:
        """Test single prediction endpoint"""
        self.print_test(f"Single Prediction - {test_name}")
        
        print("Input Data:")
        print(json.dumps(test_data, indent=2))
        
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                headers={"Content-Type": "application/json"},
                json=test_data,
                timeout=10
            )
            
            print(f"\nResponse Status: {response.status_code}")
            data = response.json()
            print("\nResponse Data:")
            print(json.dumps(data, indent=2))
            
            if response.status_code == 200 and data.get('status') == 'success':
                predicted_demand = data.get('predicted_demand')
                self.print_result(True, f"Prediction successful: {predicted_demand} units")
                return True
            else:
                self.print_result(False, f"Prediction failed: {data.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            self.print_result(False, f"Error: {str(e)}")
            return False
    
    def test_batch_prediction(self) -> bool:
        """Test batch prediction endpoint"""
        self.print_test("Batch Prediction - Multiple Scenarios")
        
        batch_data = {
            "scenarios": [
                {
                    "price": 10.00,
                    "promotion": 0,
                    "competitor_price": 10.50,
                    "day_of_week": 1,
                    "month": 1,
                    "inventory_level": 500
                },
                {
                    "price": 9.00,
                    "promotion": 1,
                    "competitor_price": 10.50,
                    "day_of_week": 6,
                    "month": 6,
                    "inventory_level": 750
                },
                {
                    "price": 12.00,
                    "promotion": 0,
                    "competitor_price": 11.00,
                    "day_of_week": 3,
                    "month": 12,
                    "inventory_level": 400
                }
            ]
        }
        
        print("Input Data:")
        print(json.dumps(batch_data, indent=2))
        
        try:
            response = requests.post(
                f"{self.base_url}/batch-predict",
                headers={"Content-Type": "application/json"},
                json=batch_data,
                timeout=10
            )
            
            print(f"\nResponse Status: {response.status_code}")
            data = response.json()
            print("\nResponse Data:")
            print(json.dumps(data, indent=2))
            
            if response.status_code == 200 and data.get('status') == 'success':
                successful = data.get('successful', 0)
                total = data.get('total_scenarios', 0)
                self.print_result(True, f"Batch prediction successful: {successful}/{total} scenarios")
                return True
            else:
                self.print_result(False, f"Batch prediction failed")
                return False
                
        except Exception as e:
            self.print_result(False, f"Error: {str(e)}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling with invalid data"""
        self.print_test("Error Handling - Invalid Data")
        
        invalid_data = {
            "price": 10.00
            # Missing required fields
        }
        
        print("Input Data (Missing Fields):")
        print(json.dumps(invalid_data, indent=2))
        
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                headers={"Content-Type": "application/json"},
                json=invalid_data,
                timeout=10
            )
            
            print(f"\nResponse Status: {response.status_code}")
            data = response.json()
            print("\nResponse Data:")
            print(json.dumps(data, indent=2))
            
            if response.status_code == 400 and data.get('status') == 'error':
                self.print_result(True, "Error handling working correctly")
                return True
            else:
                self.print_result(False, "Error handling not working as expected")
                return False
                
        except Exception as e:
            self.print_result(False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        self.print_header("Bosch FMCG Pricing API - Comprehensive Testing")
        
        print(f"\nAPI Base URL: {self.base_url}")
        print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test scenarios
        test_scenarios = [
            {
                "name": "Standard Pricing (No Promotion)",
                "data": {
                    "price": 10.50,
                    "promotion": 0,
                    "competitor_price": 11.00,
                    "day_of_week": 3,
                    "month": 6,
                    "inventory_level": 500
                }
            },
            {
                "name": "Promotion Active + Weekend",
                "data": {
                    "price": 9.00,
                    "promotion": 1,
                    "competitor_price": 10.50,
                    "day_of_week": 6,
                    "month": 12,
                    "inventory_level": 800
                }
            },
            {
                "name": "High Price (Low Demand Expected)",
                "data": {
                    "price": 15.00,
                    "promotion": 0,
                    "competitor_price": 12.00,
                    "day_of_week": 2,
                    "month": 3,
                    "inventory_level": 300
                }
            },
            {
                "name": "Competitive Pricing",
                "data": {
                    "price": 8.50,
                    "promotion": 1,
                    "competitor_price": 11.00,
                    "day_of_week": 7,
                    "month": 6,
                    "inventory_level": 1000
                }
            }
        ]
        
        # Run tests
        results = []
        
        # Basic endpoint tests
        results.append(("Health Check", self.test_health_check()))
        results.append(("API Information", self.test_api_info()))
        results.append(("Model Information", self.test_model_info()))
        
        # Prediction tests
        for scenario in test_scenarios:
            success = self.test_single_prediction(scenario["data"], scenario["name"])
            results.append((f"Prediction: {scenario['name']}", success))
        
        # Batch prediction test
        results.append(("Batch Prediction", self.test_batch_prediction()))
        
        # Error handling test
        results.append(("Error Handling", self.test_error_handling()))
        
        # Summary
        self.print_header("Test Summary")
        
        total_tests = len(results)
        passed_tests = sum(1 for _, success in results if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\nDetailed Results:")
        for test_name, success in results:
            status = "[PASS]" if success else "[FAIL]"
            print(f"  {status} {test_name}")
        
        print("\n" + "="*70)
        print(f"Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        return passed_tests == total_tests


def main():
    """Main function to run tests"""
    print("Bosch FMCG Pricing API - Testing Tool")
    print("="*70)
    
    # Get API URL from user
    print("\nEnter your API URL:")
    print("  For Render: https://your-app-name.onrender.com")
    print("  For local: http://127.0.0.1:5000")
    
    api_url = input("\nAPI URL: ").strip()
    
    if not api_url:
        print("\nNo URL provided. Using default local URL...")
        api_url = "http://127.0.0.1:5000"
    
    # Create tester and run tests
    tester = BoschAPITester(api_url)
    
    try:
        all_passed = tester.run_all_tests()
        
        if all_passed:
            print("\n[SUCCESS] All tests passed! Your API is working perfectly.")
        else:
            print("\n[WARNING] Some tests failed. Please check the details above.")
    
    except KeyboardInterrupt:
        print("\n\nTesting interrupted by user.")
    except Exception as e:
        print(f"\n\n[ERROR] Testing failed: {str(e)}")


if __name__ == "__main__":
    main()