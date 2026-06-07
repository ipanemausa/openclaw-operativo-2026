from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "slack-bot"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
