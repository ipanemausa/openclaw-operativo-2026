from flask import Flask, request, jsonify
from config import Config
from generator import MarketingCopyGenerator
import os
import json

app = Flask(__name__)
app.config.from_object(Config)
generator = MarketingCopyGenerator()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'agent': 'marketing_generator'}), 200

@app.route('/api/generate-copy', methods=['POST'])
def generate_copy():
    """Generate marketing copy for a product"""
    try:
        data = request.get_json()
        
        if not data or 'product' not in data:
            return jsonify({'error': 'Product data required'}), 400
        
        product = data['product']
        copies = generator.generate_copy(product)
        
        return jsonify({
            'product': product.get('name'),
            'copies': copies,
            'config': {
                'style': Config.HB_JEWELRY_STYLE,
                'price_range': f"${Config.HB_JEWELRY_PRICE_MIN}-${Config.HB_JEWELRY_PRICE_MAX}",
                'target_age': f"{Config.HB_JEWELRY_AGE_MIN}-{Config.HB_JEWELRY_AGE_MAX}"
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-batch', methods=['POST'])
def generate_batch():
    """Generate marketing copy for multiple products"""
    try:
        data = request.get_json()
        
        if not data or 'products' not in data:
            return jsonify({'error': 'Products array required'}), 400
        
        products = data['products']
        results = generator.generate_batch_copy(products)
        
        # Save to file
        output_file = os.path.join(Config.OUTPUT_DIR, 'batch_copy_output.json')
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'message': 'Batch copy generated successfully',
            'results': results,
            'saved_to': output_file
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get HB Jewelry configuration"""
    return jsonify({
        'brand': 'HB Jewelry',
        'style': Config.HB_JEWELRY_STYLE,
        'price_range': {
            'min': Config.HB_JEWELRY_PRICE_MIN,
            'max': Config.HB_JEWELRY_PRICE_MAX
        },
        'target_audience': {
            'age_min': Config.HB_JEWELRY_AGE_MIN,
            'age_max': Config.HB_JEWELRY_AGE_MAX
        },
        'product_types': Config.HB_JEWELRY_PRODUCT_TYPES,
        'platforms': Config.PLATFORMS
    }), 200

if __name__ == '__main__':
    os.makedirs(Config.PRODUCTS_DIR, exist_ok=True)
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    app.run(host='0.0.0.0', port=Config.AGENT_PORT, debug=Config.DEBUG)
