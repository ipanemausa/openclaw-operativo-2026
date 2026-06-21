from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/healthz', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "openclaw-app", "version": os.getenv('VERSION', '2026.5.27')}), 200

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "running", "service": "openclaw-app"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)