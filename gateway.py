from flask import Flask, jsonify

app = Flask(__name__)

from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

def check_db():
    try:
        conn = psycopg2.connect(
            "dbname=ocdb user=postgres password=ocpass host=openclaw_db"
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

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "gateway": "running",
        "db_connected": check_db()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
