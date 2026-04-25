"""
Webhook básico para recibir llamadas de Globy
Puerto: 8080
Autenticación: Bearer token
Logging: Registra todas las peticiones en logs/webhook.log
"""

from flask import Flask, request, jsonify
import os
import logging
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# Token de autenticación (cámbialo por uno seguro)
AUTH_TOKEN = os.getenv("GLOBY_WEBHOOK_TOKEN", "cambiar-este-token-ahora")

# Configurar logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "webhook.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.route("/health", methods=["GET"])
def health():
    logger.info("Health check requested")
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route("/task", methods=["POST"])
def execute_task():
    # Verificar autenticación
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {AUTH_TOKEN}":
        logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
        return jsonify({"error": "Unauthorized"}), 401
    
    # Obtener payload
    data = request.json
    task = data.get("task")
    params = data.get("params", {})
    
    # Log completo
    logger.info(f"Task received: {task} | Params: {params} | From: {request.remote_addr}")
    
    # Aquí irá la lógica de ejecución real
    result = {"status": "executed", "task": task, "result": "mock_response"}
    logger.info(f"Task executed: {task} | Result: {result['status']}")
    
    return jsonify(result), 200

if __name__ == "__main__":
    logger.info("Starting Globy Webhook Server on port 8080")
    app.run(host="0.0.0.0", port=8080, debug=True)
