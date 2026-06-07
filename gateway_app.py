from flask import Flask, jsonify, request
import os
import requests
import uuid
import logging
import psycopg2
import redis
import json
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("gateway")

AGENT_PROMPTS = {
    "main": "Eres el asistente principal de OpenClaw Cloud. Ayudas con cualquier tarea general del sistema.",
    "marketing": "Eres el agente de marketing de OpenClaw. Generas contenido, campanas, posts para redes sociales y estrategias de marketing digital.",
    "video": "Eres el agente de video de OpenClaw. Ayudas con guiones, produccion, edicion y estrategia de contenido en video.",
    "shopify": "Eres el agente de ventas de OpenClaw. Gestionas productos, ventas, mercado libre y estrategias de e-commerce en Shopify."
}

def get_redis():
    try:
        return redis.Redis(host=os.getenv('REDIS_HOST','redis'), port=int(os.getenv('REDIS_PORT','6379')), decode_responses=True)
    except Exception as e:
        logger.error(f"Redis connection error: {str(e)}")
        return None

def get_db():
    try:
        return psycopg2.connect(host=os.getenv('DB_HOST','db'), port=os.getenv('DB_PORT','5432'), dbname=os.getenv('DB_NAME','openclaw_prod'), user=os.getenv('DB_USER','openclaw_prod'), password=os.getenv('DB_PASSWORD','openclaw_prod'))
    except Exception as e:
        logger.error(f"DB connection error: {str(e)}")
        return None

def save_message(session_id, agent, role, content):
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (session_id, agent, role, content, created_at) VALUES (%s, %s, %s, %s, %s)", (session_id, agent, role, content, datetime.utcnow()))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"DB save error: {str(e)}")

def get_history(session_id, limit=10):
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute("SELECT role, content FROM messages WHERE session_id = %s ORDER BY created_at DESC LIMIT %s", (session_id, limit))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]
    except Exception as e:
        logger.error(f"DB history error: {str(e)}")
        return []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "gateway"}), 200

@app.route('/api/test', methods=['POST'])
def test():
    data = request.get_json() or {}
    return jsonify({"status": "ok", "message": data.get('message', 'No message')}), 200

@app.route('/api/mcp/status', methods=['GET'])
def mcp_status():
    return jsonify({"agents": list(AGENT_PROMPTS.keys()), "status": "ok", "persistence": "postgresql+redis"}), 200

@app.route('/api/mcp/session', methods=['POST'])
def mcp_session():
    data = request.get_json() or {}
    agent = data.get("agent", "main")
    session_id = str(uuid.uuid4())
    try:
        r = get_redis()
        if r:
            r.setex(f"session:{session_id}", 86400, json.dumps({"agent": agent, "created_at": datetime.utcnow().isoformat()}))
        logger.info(f"Session {session_id} created for agent {agent}")
    except Exception as e:
        logger.error(f"Redis session error: {str(e)}")
    return jsonify({"session_id": session_id, "agent": agent, "status": "ok"}), 200

@app.route('/api/mcp/message', methods=['POST'])
def mcp_message():
    data = request.get_json() or {}
    agent = data.get("agent", "main")
    message = data.get("message", "")
    session_id = data.get("session_id", str(uuid.uuid4()))

    if agent not in AGENT_PROMPTS:
        agent = "main"

    history = get_history(session_id)
    api_key = os.getenv('PICKAXE_API_KEY', '')
    base_url = os.getenv('PICKAXE_API_URL', 'https://api.pickaxe.co/v1')
    timeout = int(os.getenv('PICKAXE_TIMEOUT', '60'))

    if not api_key:
        return jsonify({"response": "Error: Pickaxe API key not configured.", "status": "error"}), 500

    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"message": message}

        response = requests.post(f"{base_url}/completions", json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        res_data = response.json()
        pickaxe_response = res_data.get('result', '')

        save_message(session_id, agent, "user", message)
        save_message(session_id, agent, "assistant", pickaxe_response)

        logger.info(f"Agent:{agent} Session:{session_id} OK")
        return jsonify({"response": pickaxe_response, "session_id": session_id, "agent": agent, "status": "ok"}), 200

    except requests.exceptions.Timeout:
        return jsonify({"response": "Error: Pickaxe timeout.", "status": "error"}), 504
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"response": f"Error: {str(e)}", "status": "error"}), 500

@app.route('/api/mcp/history', methods=['GET'])
def mcp_history():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({"error": "session_id required"}), 400
    history = get_history(session_id, limit=50)
    return jsonify({"session_id": session_id, "history": history, "count": len(history)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
