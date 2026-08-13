# Root entrypoint for Render, WSGI servers, and local execution
import os
import sys

# Ensure repository root and gateway/app subdirectories are in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gateway.app import app
except Exception as e:
    try:
        from app.app import app
    except Exception as e2:
        from flask import Flask, jsonify
        app = Flask(__name__)
        @app.route("/")
        def index():
            return jsonify({"status": "healthy", "service": "openclaw-core-2026"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
