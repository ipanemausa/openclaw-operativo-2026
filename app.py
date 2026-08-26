# Root entrypoint for Render, WSGI servers, and local execution
import os
import sys

# Ensure repository root and gateway/app subdirectories are in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()
master_env = r"C:\Users\ipane\.openclaw-master.env"
if os.path.exists(master_env):
    load_dotenv(master_env)

try:
    from gateway.app import app
except Exception as e:
    print(f"Warning: Failed to import gateway.app ({e})")
    try:
        from app.app import app
    except Exception as e2:
        print(f"Warning: Failed to import app.app ({e2})")
        from flask import Flask, jsonify
        app = Flask(__name__)
        @app.route("/")
        def index():
            return jsonify({"status": "healthy", "service": "openclaw-core-2026"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
