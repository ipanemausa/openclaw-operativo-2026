import requests
import json
from config import Config
from typing import List, Dict, Optional

class ShopifyClient:
    """Shopify API client for product sync"""
    
    def __init__(self):
        self.store_url = Config.SHOPIFY_STORE_URL
        self.access_token = Config.SHOPIFY_ACCESS_TOKEN
        self.api_version = Config.SHOPIFY_API_VERSION
        self.base_url = f"https://{self.store_url}/admin/api/{self.api_version}"
        self.headers = {
            'X-Shopify-Access-Token': self.access_token,
            'Content-Type': 'application/json'
        }
    
    def get_products(self, limit: int = 100) -> Optional[List[Dict]]:
        """Fetch products from Shopify"""
        try:
            url = f"{self.base_url}/products.json?limit={limit}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json().get('products', [])
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")
        
        except Exception as e:
            raise Exception(f"Failed to fetch products: {str(e)}")
    
    def create_product(self, product_data: Dict) -> Optional[Dict]:
        """Create a new product in Shopify"""
        try:
            url = f"{self.base_url}/products.json"
            payload = {'product': product_data}
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code in [200, 201]:
                return response.json().get('product')
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")
        
        except Exception as e:
            raise Exception(f"Failed to create product: {str(e)}")
    
    def update_product(self, product_id: str, product_data: Dict) -> Optional[Dict]:
        """Update an existing product"""
        try:
            url = f"{self.base_url}/products/{product_id}.json"
            payload = {'product': product_data}
            response = requests.put(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json().get('product')
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")
        
        except Exception as e:
            raise Exception(f"Failed to update product: {str(e)}")
    
    def delete_product(self, product_id: str) -> bool:
        """Delete a product from Shopify"""
        try:
            url = f"{self.base_url}/products/{product_id}.json"
            response = requests.delete(url, headers=self.headers)
            
            return response.status_code == 200
        
        except Exception as e:
            raise Exception(f"Failed to delete product: {str(e)}")
    
    def get_inventory_levels(self, product_id: str) -> Optional[List[Dict]]:
        """Get inventory levels for a product"""
        try:
            url = f"{self.base_url}/products/{product_id}/inventory_levels.json"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json().get('inventory_levels', [])
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")
        
        except Exception as e:
            raise Exception(f"Failed to fetch inventory levels: {str(e)}")
    
    def test_connection(self) -> bool:
        """Test Shopify API connection"""
        try:
            url = f"{self.base_url}/shop.json"
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        
        except Exception as e:
            raise Exception(f"Connection failed: {str(e)}")
