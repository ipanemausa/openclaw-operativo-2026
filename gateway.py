from flask import Flask, jsonify
import psycopg2
import os

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
