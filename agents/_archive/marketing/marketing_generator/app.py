from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "marketing_generator"}), 200

@app.route('/generate', methods=['POST'])
def generate():
    return jsonify({"message": "Marketing copy generation endpoint"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
