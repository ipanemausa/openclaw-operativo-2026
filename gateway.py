from flask import Flask, jsonify, request, Response
import psycopg2
import os
import requests

app = Flask(__name__)

def check_db():
    try:
        db_user = os.environ.get("DB_USER", "oc_user")
        db_pass = os.environ.get("DB_PASS", "securepass")
        db_host = os.environ.get("DB_HOST", "db")
        db_name = os.environ.get("DB_NAME", "oc_db")
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return True
    except Exception:
        return False

@app.route("/", methods=["GET"])
def root():
    return "Gateway is running and connected!"

@app.route("/health", methods=["GET"])
def health():
    if check_db():
        return jsonify({"status": "ok", "db": "connected"})
    else:
        return jsonify({"status": "error", "db": "unreachable"}), 500

# 🔥 Bloque nuevo: proxy genérico hacia openclaw_app
@app.route('/<path:path>', methods=["GET", "POST"])
def proxy(path):
    resp = requests.request(
        method=request.method,
        url=f"http://openclaw_app:5000/{path}",
        headers={key: value for key, value in request.headers},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    return Response(resp.content, resp.status_code, resp.headers.items())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
