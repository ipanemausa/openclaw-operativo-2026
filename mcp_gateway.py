from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/route', methods=['POST'])
def route():
    data = request.get_json() or {}
    return jsonify({
        "status": "routed",
        "message": data.get('message', 'No message')
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
