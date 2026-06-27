from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from datetime import datetime, timezone
import json, os, pathlib, redis, threading, time
import docker

app = Flask(__name__)
CORS(app)
HANDOFFS_DIR = pathlib.Path("/handoffs")
LOGS_DIR     = pathlib.Path("/logs")
ESTADO_PATH  = pathlib.Path("/app/claw-estado.json")
HANDOFFS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def load_estado():
    try:
        return json.loads(ESTADO_PATH.read_text(encoding="utf-8"))
    except:
        return {}

def save_estado(estado):
    ESTADO_PATH.write_text(json.dumps(estado, indent=2, ensure_ascii=False), encoding="utf-8")

def get_ready_tasks(tareas):
    ready = []
    for nombre, t in tareas.items():
        if t["estado"] != "pendiente":
            continue
        deps = t.get("depends_on", [])
        if all(tareas.get(d, {}).get("estado") == "completada" for d in deps):
            ready.append(nombre)
    return ready

def dag_worker():
    while True:
        try:
            estado = load_estado()
            tareas = estado.get("tareas", {})
            ready  = get_ready_tasks(tareas)
            for nombre in ready:
                redis_client.lpush("queue:tareas", nombre)
                tareas[nombre]["estado"] = "en_cola"
                print(f"[DAG] {nombre} en_cola", flush=True)
            if ready:
                estado["ultima_actualizacion"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                save_estado(estado)
        except Exception as e:
            print(f"[DAG] error: {e}", flush=True)
        time.sleep(10)

def task_executor():
    import task_executor as ex
    ex.run()

def get_stack_status():
    try:
        client = docker.from_env()
        containers = []
        for c in client.containers.list(all=True):
            ports = ",".join([str(v[0]["HostPort"]) for v in (c.ports or {}).values() if v])
            containers.append({"name": c.name, "status": c.status, "ports": ports})
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
    body       = request.get_json(force=True)
    prompt     = body.get("prompt", "")
    duration   = int(body.get("duration", 5))
    resolution = body.get("resolution", "1280x720")
    style      = body.get("style", "cinematic")
    if not prompt:
        return jsonify({"error": "prompt requerido"}), 400
    job_id = f"veo-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    redis_client.hset(f"veo:{job_id}", mapping={
        "prompt": prompt, "duration": str(duration),
        "resolution": resolution, "style": style,
        "status": "queued",
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
    return jsonify({"job_id": job_id, "status": data.get("status"),
                    "video_url": data.get("video_url", ""), "prompt": data.get("prompt"),
                    "created_at": data.get("created_at")})

@app.route("/api/chat/input", methods=["POST"])
def chat_input():
    body = request.get_json(force=True)
    mensaje = body.get("mensaje", "")
    agente  = body.get("agente", "main")
    if not mensaje:
        return jsonify({"error": "mensaje requerido"}), 400
    job_id = f"chat-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    redis_client.hset(f"chat:{job_id}", mapping={
        "mensaje": mensaje, "agente": agente,
        "status": "queued",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    redis_client.lpush("queue:chat", job_id)
    print(f"[CHAT] job {job_id} encolado — agente: {agente}", flush=True)
    return jsonify({"job_id": job_id, "status": "queued"}), 202

@app.route("/api/chat/status/<job_id>")
def chat_status(job_id):
    def generate():
        for _ in range(30):
            data = redis_client.hgetall(f"chat:{job_id}")
            status = data.get("status", "queued")
            respuesta = data.get("respuesta", "")
            yield f"data: {json.dumps({'status': status, 'respuesta': respuesta})}\n\n"
            if status == "completed":
                break
            time.sleep(1)
    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@app.route("/api/hb/productos", methods=["GET"])
def get_productos():
    keys = redis_client.keys("hb:producto:*")
    productos = [redis_client.hgetall(k) for k in sorted(keys)]
    return jsonify({"productos": productos})

@app.route("/api/hb/productos", methods=["POST"])
def add_producto():
    b = request.get_json(force=True)
    pid = f"hb:producto:{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    redis_client.hset(pid, mapping={
        "id": pid, "nombre": b.get("nombre",""), "precio": str(b.get("precio",0)),
        "stock": str(b.get("stock",0)), "categoria": b.get("categoria",""),
        "descripcion": b.get("descripcion",""),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    return jsonify({"status": "ok", "id": pid}), 201

@app.route("/api/hb/ventas", methods=["GET"])
def get_ventas():
    keys = redis_client.keys("hb:venta:*")
    ventas = [redis_client.hgetall(k) for k in sorted(keys)]
    return jsonify({"ventas": ventas})

@app.route("/api/hb/ventas", methods=["POST"])
def add_venta():
    b = request.get_json(force=True)
    vid = f"hb:venta:{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    redis_client.hset(vid, mapping={
        "id": vid, "producto": b.get("producto",""), "cantidad": str(b.get("cantidad",1)),
        "precio": str(b.get("precio",0)), "canal": b.get("canal",""),
        "cliente": b.get("cliente",""),
        "fecha": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    return jsonify({"status": "ok", "id": vid}), 201

@app.route("/api/hb/ordenes", methods=["GET"])
def get_ordenes():
    keys = redis_client.keys("hb:orden:*")
    ordenes = [redis_client.hgetall(k) for k in sorted(keys)]
    return jsonify({"ordenes": ordenes})

@app.route("/api/hb/ordenes", methods=["POST"])
def add_orden():
    b = request.get_json(force=True)
    oid = f"hb:orden:{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    redis_client.hset(oid, mapping={
        "id": oid, "cliente": b.get("cliente",""), "producto": b.get("producto",""),
        "cantidad": str(b.get("cantidad",1)), "precio": str(b.get("precio",0)),
        "canal": b.get("canal","Instagram"), "estado": b.get("estado","Pendiente"),
        "notas": b.get("notas",""),
        "fecha": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    return jsonify({"status": "ok", "id": oid}), 201

@app.route("/api/hb/ordenes/<oid>", methods=["PATCH"])
def update_orden(oid):
    b = request.get_json(force=True)
    key = oid if oid.startswith("hb:orden:") else f"hb:orden:{oid}"
    redis_client.hset(key, "estado", b.get("estado","Pendiente"))
    return jsonify({"status": "ok"})

@app.route("/handoff", methods=["POST"])
def create_handoff():
    body = request.get_json(force=True)
    ts   = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    h    = {
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

@app.route("/api/tareas", methods=["GET"])
def get_tareas():
    estado = load_estado()
    return jsonify({"tareas": estado.get("tareas", {})})

@app.route("/api/tareas/<nombre>/completar", methods=["POST"])
def completar_tarea(nombre):
    estado = load_estado()
    tareas = estado.get("tareas", {})
    if nombre not in tareas:
        return jsonify({"error": "tarea no encontrada"}), 404
    tareas[nombre]["estado"] = "completada"
    tareas[nombre]["completada_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    estado["ultima_actualizacion"]  = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    save_estado(estado)
    return jsonify({"tarea": nombre, "estado": "completada"})

if __name__ == "__main__":
    threading.Thread(target=dag_worker, daemon=True).start()
    threading.Thread(target=task_executor, daemon=True).start()
    app.run(host="0.0.0.0", port=8090, debug=False)