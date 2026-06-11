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
    "main": "Eres el asistente principal de OpenClaw Cloud para HB Jewelry. Ayudas con cualquier tarea general del sistema.",
    "marketing": "Eres el agente de marketing de HB Jewelry, una marca de joyeria fina en Washington DC que vende plata, bisuteria gold plated y rhodium plated. Generas contenido viral para Instagram y TikTok: descripciones de productos, captions con hashtags, ideas de reels, guiones de videos cortos y campanas de temporada. Tu tono es elegante, aspiracional y accesible. Siempre incluyes llamadas a la accion y hashtags relevantes en ingles y espanol.",
    "video": "Eres el agente de video de HB Jewelry. Creas guiones para Reels de Instagram y TikTok mostrando piezas de joyeria fina en Washington DC. Tus videos son cortos, elegantes y virales. Incluyes texto en pantalla, musica sugerida y llamadas a la accion.",
    "shopify": "Eres el agente de ventas de HB Jewelry. Gestionas el catalogo de productos, registras pedidos, consultas de inventario y estrategias de venta en Shopify, Instagram, WhatsApp y TikTok Shop. Ayudas a cerrar ventas con respuestas rapidas y profesionales.",
    "ventas": "Eres el agente de registro de ventas de HB Jewelry. Cuando el usuario te da informacion de una venta (producto, cantidad, precio, cliente, canal), la registras de forma estructurada y confirmas el registro. Extraes: producto, cantidad, precio_unitario, total, cliente, canal_venta, fecha."
}

def get_redis():
    try:
        return redis.Redis(host=os.getenv('REDIS_HOST','redis'), port=int(os.getenv('REDIS_PORT','6379')), decode_responses=True)
    except Exception as e:
        logger.error(f"Redis connection error: {str(e)}")
        return None

def get_db():
    try:
        return psycopg2.connect(
            host=os.getenv('DB_HOST','db'),
            port=os.getenv('DB_PORT','5432'),
            dbname=os.getenv('DB_NAME','openclaw_prod'),
            user=os.getenv('DB_USER','openclaw_admin'),
            password=os.getenv('DB_PASSWORD','SecureDB2026!@#Xyz123')
        )
    except Exception as e:
        logger.error(f"DB connection error: {str(e)}")
        return None

def save_message(session_id, agent, role, content):
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (session_id, agent, role, content, created_at) VALUES (%s, %s, %s, %s, %s)",
                    (session_id, agent, role, content, datetime.utcnow()))
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
        cur.execute("SELECT role, content FROM messages WHERE session_id = %s ORDER BY created_at DESC LIMIT %s",
                    (session_id, limit))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]
    except Exception as e:
        logger.error(f"DB history error: {str(e)}")
        return []

def save_sale(data):
    try:
        conn = get_db()
        if not conn:
            return False
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                producto VARCHAR(200),
                cantidad INTEGER,
                precio_unitario DECIMAL(10,2),
                total DECIMAL(10,2),
                cliente VARCHAR(200),
                canal_venta VARCHAR(100),
                notas TEXT,
                created_at TIMESTAMP
            )
        """)
        cur.execute("""
            INSERT INTO sales (producto, cantidad, precio_unitario, total, cliente, canal_venta, notas, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get('producto',''),
            data.get('cantidad', 1),
            data.get('precio_unitario', 0),
            data.get('total', 0),
            data.get('cliente',''),
            data.get('canal_venta',''),
            data.get('notas',''),
            datetime.utcnow()
        ))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Sale save error: {str(e)}")
        return False

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "gateway", "project": "HB Jewelry"}), 200

@app.route('/api/test', methods=['POST'])
def test():
    data = request.get_json() or {}
    return jsonify({"status": "ok", "message": data.get('message', 'No message')}), 200

@app.route('/api/mcp/status', methods=['GET'])
def mcp_status():
    return jsonify({
        "agents": list(AGENT_PROMPTS.keys()),
        "status": "ok",
        "project": "HB Jewelry",
        "persistence": "postgresql+redis"
    }), 200

@app.route('/api/mcp/session', methods=['POST'])
def mcp_session():
    data = request.get_json() or {}
    agent = data.get("agent", "main")
    session_id = str(uuid.uuid4())
    try:
        r = get_redis()
        if r:
            r.setex(f"session:{session_id}", 86400, json.dumps({
                "agent": agent,
                "created_at": datetime.utcnow().isoformat()
            }))
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
        return jsonify({
            "response": pickaxe_response,
            "session_id": session_id,
            "agent": agent,
            "status": "ok"
        }), 200

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

@app.route('/api/hb/sale', methods=['POST'])
def register_sale():
    data = request.get_json() or {}
    required = ['producto', 'cantidad', 'precio_unitario', 'cliente', 'canal_venta']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Faltan campos: {missing}", "status": "error"}), 400
    data['total'] = float(data.get('cantidad', 1)) * float(data.get('precio_unitario', 0))
    success = save_sale(data)
    if success:
        return jsonify({"status": "ok", "message": "Venta registrada", "total": data['total']}), 200
    return jsonify({"status": "error", "message": "Error guardando venta"}), 500

@app.route('/api/hb/sales', methods=['GET'])
def get_sales():
    try:
        conn = get_db()
        if not conn:
            return jsonify({"error": "DB no disponible"}), 500
        cur = conn.cursor()
        cur.execute("SELECT id, producto, cantidad, precio_unitario, total, cliente, canal_venta, created_at FROM sales ORDER BY created_at DESC LIMIT 50")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        sales = [{"id": r[0], "producto": r[1], "cantidad": r[2], "precio_unitario": float(r[3]), "total": float(r[4]), "cliente": r[5], "canal_venta": r[6], "fecha": str(r[7])} for r in rows]
        return jsonify({"sales": sales, "count": len(sales), "status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)