"""
Webhook básico para recibir llamadas de Globy
Puerto: 8080
Autenticación: Bearer token
"""

from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Token de autenticación (cámbialo por uno seguro)
AUTH_TOKEN = os.getenv("GLOBY_WEBHOOK_TOKEN", "cambiar-este-token-ahora")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route("/task", methods=["POST"])
def execute_task():
    # Verificar autenticación
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {AUTH_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401
    
    # Obtener payload
    data = request.json
    task = data.get("task")
    params = data.get("params", {})
    
    # Log
    print(f"[GLOBY] Task received: {task} | Params: {params}")
    
    # Aquí irá la lógica de ejecución real
    result = {"status": "executed", "task": task, "result": "mock_response"}
    
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
