from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "shopify_integration"}), 200

@app.route('/sync', methods=['POST'])
def sync():
    return jsonify({"message": "Shopify sync endpoint"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
