from flask import Flask, jsonify, request
import os
import requests
import uuid
import logging

app = Flask(__name__)
from flask_cors import CORS
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("gateway")

ACTIVE_SESSIONS = {}
ORCHESTRATOR_URL = os.getenv('ORCHESTRATOR_URL', 'http://claw-orchestrator:8090')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "gateway"}), 200

@app.route('/api/test', methods=['POST'])
def test():
    data = request.get_json() or {}
    return jsonify({"status": "ok", "message": data.get('message', 'No message')}), 200

@app.route('/api/mcp/status', methods=['GET'])
def mcp_status():
    return jsonify({"agents": ["main", "video", "marketing", "shopify"], "status": "ok"}), 200

@app.route('/api/mcp/session', methods=['POST'])
def mcp_session():
    data = request.get_json() or {}
    agent = data.get("agent", "main")
    session_id = str(uuid.uuid4())
    ACTIVE_SESSIONS[session_id] = agent
    return jsonify({"session_id": session_id, "status": "ok"}), 200

def send_to_orchestrator(message, agent, session_id):
    try:
        payload = {
            "mensaje": message,
            "agente":  agent,
            "session_id": session_id
        }
        r = requests.post(
            f"{ORCHESTRATOR_URL}/api/chat/input",
            json=payload,
            timeout=5
        )
        return r.json()
    except Exception as e:
        logger.error(f"Error enviando al orquestador: {e}")
        return None

@app.route('/api/mcp/message', methods=['POST'])
def mcp_message():
    data = request.get_json() or {}
    agent = data.get("agent", "main")
    message = data.get("message", "")
    session_id = data.get("session_id")

    logger.info(f"Mensaje recibido. Agente: {agent}, Longitud: {len(message)}")

    if session_id and session_id not in ACTIVE_SESSIONS:
        return jsonify({"response": "Error: Invalid session_id.", "status": "error"}), 401

    send_to_orchestrator(message, agent, session_id)

    api_key = os.getenv('PICKAXE_API_KEY', '')
    base_url = os.getenv('PICKAXE_API_URL', 'https://api.pickaxe.co/v1')
    timeout = int(os.getenv('PICKAXE_TIMEOUT', '60'))

    if not api_key:
        return jsonify({"response": "Error: Pickaxe API key no configurada.", "status": "error"}), 500

    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        response = requests.post(
            f"{base_url}/completions",
            json={"message": message},
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        pickaxe_response = response.json().get('result', '')
        logger.info("Respuesta recibida de Pickaxe.")
        return jsonify({"response": pickaxe_response, "status": "ok"}), 200
    except requests.exceptions.Timeout:
        return jsonify({"response": "Error: Timeout con Pickaxe.", "status": "error"}), 504
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}", "status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)