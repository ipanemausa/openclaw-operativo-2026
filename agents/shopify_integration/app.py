from flask import Flask, request, jsonify
from config import Config
from shopify_client import ShopifyClient
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

try:
    shopify_client = ShopifyClient()
except Exception as e:
    shopify_client = None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'agent': 'shopify_integration'}), 200

@app.route('/api/shopify/test-connection', methods=['GET'])
def test_connection():
    """Test Shopify API connection"""
    try:
        if not shopify_client:
            return jsonify({'error': 'Shopify client not initialized. Check credentials.'}), 500
        
        if shopify_client.test_connection():
            return jsonify({'status': 'connected', 'message': 'Shopify connection successful'}), 200
        else:
            return jsonify({'status': 'failed', 'message': 'Shopify connection failed'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopify/products', methods=['GET'])
def get_products():
    """Fetch products from Shopify"""
    try:
        if not shopify_client:
            return jsonify({'error': 'Shopify client not initialized'}), 500
        
        limit = request.args.get('limit', 100, type=int)
        products = shopify_client.get_products(limit=limit)
        
        return jsonify({
            'count': len(products),
            'products': products
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopify/products', methods=['POST'])
def create_product():
    """Create a new product in Shopify"""
    try:
        if not shopify_client:
            return jsonify({'error': 'Shopify client not initialized'}), 500
        
        data = request.get_json()
        if not data or 'product' not in data:
            return jsonify({'error': 'Product data required'}), 400
        
        product = shopify_client.create_product(data['product'])
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopify/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product"""
    try:
        if not shopify_client:
            return jsonify({'error': 'Shopify client not initialized'}), 500
        
        data = request.get_json()
        if not data or 'product' not in data:
            return jsonify({'error': 'Product data required'}), 400
        
        product = shopify_client.update_product(product_id, data['product'])
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': product
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopify/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product from Shopify"""
    try:
        if not shopify_client:
            return jsonify({'error': 'Shopify client not initialized'}), 500
        
        success = shopify_client.delete_product(product_id)
        
        if success:
            return jsonify({'message': 'Product deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete product'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopify/inventory/<product_id>', methods=['GET'])
def get_inventory(product_id):
    """Get inventory levels for a product"""
    try:
        if not shopify_client:
            return jsonify({'error': 'Shopify client not initialized'}), 500
        
        inventory = shopify_client.get_inventory_levels(product_id)
        
        return jsonify({
            'product_id': product_id,
            'inventory_levels': inventory
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopify/config', methods=['GET'])
def get_config():
    """Get Shopify configuration"""
    return jsonify({
        'store_url': Config.SHOPIFY_STORE_URL,
        'api_version': Config.SHOPIFY_API_VERSION,
        'sync_interval': Config.SYNC_INTERVAL,
        'batch_size': Config.BATCH_SIZE
    }), 200

if __name__ == '__main__':
    os.makedirs(Config.CONFIG_DIR, exist_ok=True)
    os.makedirs(Config.LOGS_DIR, exist_ok=True)
    
    app.run(host='0.0.0.0', port=Config.AGENT_PORT, debug=Config.DEBUG)
