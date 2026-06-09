from flask import Flask, jsonify, request
import os
from hb_cotizacion import hb_bp, crear_tabla_cotizaciones

app = Flask(__name__)

app.register_blueprint(hb_bp)
crear_tabla_cotizaciones()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "gateway"
    }), 200

@app.route('/api/test', methods=['POST'])
def test():
    data = request.get_json() or {}
    return jsonify({
        "status": "ok",
        "message": data.get('message', 'No message')
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
