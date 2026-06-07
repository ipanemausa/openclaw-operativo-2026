from flask import Flask, jsonify, request
import os
import requests
import uuid
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("gateway")

# In-memory session store
ACTIVE_SESSIONS = {}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "gateway"}), 200

@app.route('/api/test', methods=['POST'])
def test():
    data = request.get_json() or {}
    return jsonify({"status": "ok", "message": data.get('message', 'No message')}), 200

@app.route('/api/mcp/status', methods=['GET'])
def mcp_status():
    logger.info("Received request for MCP status")
    return jsonify({
        "agents": ["main", "video", "marketing", "shopify"],
        "status": "ok"
    }), 200

@app.route('/api/mcp/session', methods=['POST'])
def mcp_session():
    data = request.get_json() or {}
    agent = data.get("agent", "main")
    
    session_id = str(uuid.uuid4())
    ACTIVE_SESSIONS[session_id] = agent
    logger.info(f"Created session {session_id} for agent {agent}")
    
    return jsonify({
        "session_id": session_id,
        "status": "ok"
    }), 200

@app.route('/api/mcp/message', methods=['POST'])
def mcp_message():
    data = request.get_json() or {}
    agent = data.get("agent", "main")
    message = data.get("message", "")
    session_id = data.get("session_id")
    
    logger.info(f"Received message request. Agent: {agent}, Message Length: {len(message)}")
    
    # Session Validation
    if session_id:
        if session_id not in ACTIVE_SESSIONS:
            logger.error(f"Session validation failed: Session ID {session_id} not found.")
            return jsonify({
                "response": "Error: Invalid session_id.",
                "status": "error"
            }), 401
        logger.info(f"Session validated successfully: {session_id} for agent {ACTIVE_SESSIONS[session_id]}")
    else:
        logger.warning("Session validation warning: request received without session_id.")
    
    # Connect with Pickaxe LLM
    api_key = os.getenv('PICKAXE_API_KEY', '')
    base_url = os.getenv('PICKAXE_API_URL', 'https://api.pickaxe.co/v1')
    timeout = int(os.getenv('PICKAXE_TIMEOUT', '60'))
    
    if not api_key:
        logger.error("Pickaxe API key is not configured in environment.")
        return jsonify({
            "response": "Error: Pickaxe API key is not configured.",
            "status": "error"
        }), 500

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "message": message
        }
        
        logger.info(f"Forwarding message to Pickaxe completions endpoint: {base_url}/completions")
        
        response = requests.post(
            f"{base_url}/completions",
            json=payload,
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        res_data = response.json()
        pickaxe_response = res_data.get('result', '')
        
        logger.info("Successfully received response from Pickaxe.")
        return jsonify({
            "response": pickaxe_response,
            "status": "ok"
        }), 200
    except requests.exceptions.Timeout as te:
        logger.error(f"Timeout communicating with Pickaxe after {timeout} seconds: {str(te)}")
        return jsonify({
            "response": "Error: Connection to Pickaxe timed out.",
            "status": "error"
        }), 504
    except Exception as e:
        logger.error(f"Error communicating with Pickaxe: {str(e)}")
        return jsonify({
            "response": f"Error communicating with Pickaxe: {str(e)}",
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)

