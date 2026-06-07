from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "video_agent"}), 200

@app.route('/process', methods=['POST'])
def process():
    return jsonify({"message": "Video processing endpoint"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
