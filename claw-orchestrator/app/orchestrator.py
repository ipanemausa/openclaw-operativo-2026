from flask import Flask, jsonify, request
from datetime import datetime, timezone
import subprocess, json, os, pathlib, redis

app = Flask(__name__)

HANDOFFS_DIR = pathlib.Path("/handoffs")
LOGS_DIR     = pathlib.Path("/logs")
HANDOFFS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def get_stack_status():
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}|{{.Status}}|{{.Ports}}"],
            capture_output=True, text=True, timeout=5
        )
        containers = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("|")
                containers.append({
                    "name":   parts[0] if len(parts) > 0 else "",
                    "status": parts[1] if len(parts) > 1 else "",
                    "ports":  parts[2] if len(parts) > 2 else ""
                })
        return containers
    except Exception as e:
        return [{"error": str(e)}]

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "claw-orchestrator", "port": 8090})

@app.route("/stack")
def stack():
    return jsonify({"containers": get_stack_status()})

@app.route("/api/radio/input", methods=["POST"])
def radio_input():
    body = request.get_json(force=True)
    prompt     = body.get("prompt", "")
    duration   = int(body.get("duration", 5))
    resolution = body.get("resolution", "1280x720")
    style      = body.get("style", "cinematic")
    if not prompt:
        return jsonify({"error": "prompt requerido"}), 400
    job_id = f"veo-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    redis_client.hset(f"veo:{job_id}", mapping={
        "prompt":     prompt,
        "duration":   str(duration),
        "resolution": resolution,
        "style":      style,
        "status":     "queued",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    redis_client.lpush("queue:video_veo", job_id)
    return jsonify({"job_id": job_id, "status": "queued"}), 202

@app.route("/api/radio/publish", methods=["GET"])
def radio_publish():
    job_id = request.args.get("job_id")
    if not job_id:
        return jsonify({"error": "job_id requerido"}), 400
    data = redis_client.hgetall(f"veo:{job_id}")
    if not data:
        return jsonify({"error": "job no encontrado"}), 404
    return jsonify({
        "job_id":     job_id,
        "status":     data.get("status"),
        "video_url":  data.get("video_url", ""),
        "prompt":     data.get("prompt"),
        "created_at": data.get("created_at")
    })

@app.route("/handoff", methods=["POST"])
def create_handoff():
    body = request.get_json(force=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    h = {
        "id":             f"HO-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "timestamp":      ts,
        "from":           body.get("from", "claude"),
        "to":             body.get("to", "copilot"),
        "tareas_activas": body.get("tareas", []),
        "notas":          body.get("notas", "")
    }
    HANDOFFS_DIR.mkdir(exist_ok=True)
    (HANDOFFS_DIR / f"{h['id']}.json").write_text(json.dumps(h, indent=2, ensure_ascii=False))
    return jsonify({"handoff": h, "id": h["id"]})

@app.route("/handoffs")
def list_handoffs():
    files = sorted(HANDOFFS_DIR.glob("*.json"), reverse=True)[:20]
    return jsonify({"handoffs": [{"id": json.loads(f.read_text())["id"]} for f in files]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=False)